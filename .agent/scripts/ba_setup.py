#!/usr/bin/env python3
"""
ba_setup.py — One-time setup wizard helper for BA-Kit external connectors.

Handles credential file management for jira / confluence connectors and the
second-opinion provider. The BA-facing @ba-setup agent calls this script;
the BA never types CLI flags directly.

Security model:
- Tokens never echoed to terminal (mask first 4 + last 3 chars)
- .env files chmod 0600 (owner read/write only)
- .gitignore checked + warned if .env not covered
- Atomic write via temp file + rename
- Connectivity test BEFORE declaring success

Usage:
    ba_setup.py jira       --url URL --token TOK [--project KEY]
    ba_setup.py confluence --url URL --token TOK [--space KEY]
    ba_setup.py test       jira | confluence | gemini | openai | ollama
    ba_setup.py status     [provider]      # show what's configured (masked)

Zero external dependencies — uses stdlib urllib only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import NamedTuple


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
JIRA_ENV = REPO_ROOT / ".agent" / "skills" / "jira-connector" / ".env"
CONF_ENV = REPO_ROOT / ".agent" / "skills" / "confluence-connector" / ".env"
GITIGNORE = REPO_ROOT / ".gitignore"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class ValidationError(Exception):
    """Raised when a credential value fails format validation."""


PLACEHOLDER_PATTERNS = [
    re.compile(r"^xxx+$", re.I),
    re.compile(r"^your[- _]?token", re.I),
    re.compile(r"^paste[- _]?here", re.I),
    re.compile(r"^todo$", re.I),
    re.compile(r"^changeme$", re.I),
    re.compile(r"^placeholder$", re.I),
    re.compile(r"^<.+>$"),
]


def validate_url(url: str) -> str:
    """Reject obviously malformed URLs. Return cleaned value."""
    url = url.strip().rstrip("/")
    if not url:
        raise ValidationError("URL is empty")
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValidationError(
            f"URL must start with http:// or https:// (got: {url[:30]})"
        )
    if " " in url:
        raise ValidationError("URL must not contain spaces")
    return url


def validate_token(token: str) -> str:
    """Reject placeholders, empty, or too-short tokens."""
    token = token.strip()
    if not token:
        raise ValidationError("Token is empty")
    if len(token) < 20:
        raise ValidationError(
            f"Token looks too short ({len(token)} chars; expected ≥ 20). "
            "Did you paste only part of it?"
        )
    if " " in token:
        raise ValidationError("Token must not contain spaces")
    for pat in PLACEHOLDER_PATTERNS:
        if pat.match(token):
            raise ValidationError(
                "Token looks like a placeholder. Paste a real token from your IT team."
            )
    return token


def validate_project_key(key: str | None) -> str | None:
    """Project keys are uppercase letters + digits (Jira convention)."""
    if not key:
        return None
    key = key.strip().upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9_]{1,9}", key):
        raise ValidationError(
            f"Project key '{key}' looks invalid. "
            "Jira keys are 2-10 uppercase letters/digits."
        )
    return key


def mask_token(token: str) -> str:
    """Return a masked version safe to print: first 4 + last 3 chars."""
    if len(token) <= 12:
        return "***" + token[-3:]
    return token[:4] + "*" * 6 + token[-3:]


# ---------------------------------------------------------------------------
# .env file management
# ---------------------------------------------------------------------------

def write_env_file(path: Path, values: dict[str, str]) -> None:
    """Atomic write with secure permissions.

    Strategy: write to .env.new, fsync, then rename. Backup any existing
    .env to .env.bak so the BA can recover if the new credentials fail.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    # Backup existing
    if path.exists():
        backup = path.with_suffix(".env.bak")
        backup.write_bytes(path.read_bytes())
        backup.chmod(0o600)

    # Atomic write
    tmp = path.with_suffix(".env.new")
    lines = [f"{k}={v}" for k, v in values.items()]
    tmp.write_text("\n".join(lines) + "\n")
    tmp.chmod(0o600)
    tmp.replace(path)
    path.chmod(0o600)


def read_env_file(path: Path) -> dict[str, str]:
    """Parse a simple KEY=VALUE .env file. Skip comments + blank lines."""
    if not path.exists():
        return {}
    out: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip()
    return out


def check_gitignore() -> tuple[bool, str]:
    """Return (covered, message). True if .env is gitignored."""
    if not GITIGNORE.exists():
        return False, "No .gitignore found at repo root — credentials risk being committed."
    text = GITIGNORE.read_text()
    patterns = ["*.env", ".env", "*/.env", "**/.env", ".agent/skills/*-connector/.env"]
    if any(p in text for p in patterns):
        return True, "✓ .gitignore covers .env files"
    return False, "⚠ .gitignore does NOT cover .env files. Add `.env` to .gitignore now."


# ---------------------------------------------------------------------------
# Connectivity tests
# ---------------------------------------------------------------------------

def _http_get(url: str, headers: dict, timeout: int = 15) -> tuple[int, str]:
    """Single GET, returns (status, body). No external deps."""
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore") if e.fp else ""
        return e.code, body
    except urllib.error.URLError as e:
        raise RuntimeError(f"Cannot reach server: {e.reason}") from e


def test_jira(env: dict[str, str]) -> tuple[bool, str]:
    base = env.get("JIRA_BASE_URL")
    pat = env.get("JIRA_PAT")
    if not (base and pat):
        return False, "JIRA_BASE_URL or JIRA_PAT missing from .env"
    url = f"{base}/rest/api/2/myself"
    headers = {"Authorization": f"Bearer {pat}", "Content-Type": "application/json"}
    try:
        status, body = _http_get(url, headers)
    except RuntimeError as e:
        return False, str(e)
    if status == 200:
        try:
            user = json.loads(body)
            display = user.get("displayName") or user.get("name") or "unknown user"
            email = user.get("emailAddress", "no-email")
            return True, f"Logged in as {display} ({email})"
        except json.JSONDecodeError:
            return True, "Connected (could not parse user info, but auth worked)"
    if status == 401:
        return False, "Authentication failed (401). Token may be wrong, expired, or revoked."
    if status == 403:
        return False, "Forbidden (403). Token is valid but lacks permissions."
    return False, f"Unexpected response (HTTP {status})"


def test_confluence(env: dict[str, str]) -> tuple[bool, str]:
    base = env.get("CONFLUENCE_BASE_URL")
    pat = env.get("CONFLUENCE_PAT")
    if not (base and pat):
        return False, "CONFLUENCE_BASE_URL or CONFLUENCE_PAT missing from .env"
    url = f"{base}/rest/api/space?limit=1"
    headers = {"Authorization": f"Bearer {pat}", "Content-Type": "application/json"}
    try:
        status, body = _http_get(url, headers)
    except RuntimeError as e:
        return False, str(e)
    if status == 200:
        try:
            data = json.loads(body)
            n = data.get("size", 0)
            return True, f"Connected — can list spaces (saw {n} on first page)"
        except json.JSONDecodeError:
            return True, "Connected (could not parse spaces response)"
    if status == 401:
        return False, "Authentication failed (401). Token may be wrong, expired, or revoked."
    return False, f"Unexpected response (HTTP {status})"


def test_gemini() -> tuple[bool, str]:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return False, "GEMINI_API_KEY not set in shell environment"
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    try:
        status, _ = _http_get(url, {})
    except RuntimeError as e:
        return False, str(e)
    if status == 200:
        return True, "Gemini API key works"
    if status == 400:
        return False, "API key rejected by Gemini (400)"
    return False, f"Unexpected response (HTTP {status})"


def test_openai() -> tuple[bool, str]:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return False, "OPENAI_API_KEY not set in shell environment"
    headers = {"Authorization": f"Bearer {key}"}
    try:
        status, _ = _http_get("https://api.openai.com/v1/models", headers)
    except RuntimeError as e:
        return False, str(e)
    if status == 200:
        return True, "OpenAI API key works"
    if status == 401:
        return False, "OpenAI API key rejected (401)"
    return False, f"Unexpected response (HTTP {status})"


def test_ollama() -> tuple[bool, str]:
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    try:
        status, body = _http_get(f"{host.rstrip('/')}/api/tags", {})
    except RuntimeError as e:
        return False, str(e)
    if status == 200:
        try:
            data = json.loads(body)
            n = len(data.get("models", []))
            return True, f"Ollama running with {n} model(s) available"
        except json.JSONDecodeError:
            return True, "Ollama responding"
    return False, f"Unexpected response (HTTP {status})"


TESTS = {
    "jira":       lambda: test_jira(read_env_file(JIRA_ENV)),
    "confluence": lambda: test_confluence(read_env_file(CONF_ENV)),
    "gemini":     test_gemini,
    "openai":     test_openai,
    "ollama":     test_ollama,
}


# ---------------------------------------------------------------------------
# CLI sub-commands
# ---------------------------------------------------------------------------

def cmd_jira(args: argparse.Namespace) -> int:
    try:
        url = validate_url(args.url)
        token = validate_token(args.token)
        project = validate_project_key(args.project)
    except ValidationError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 2

    values = {"JIRA_BASE_URL": url, "JIRA_PAT": token}
    if project:
        values["JIRA_DEFAULT_PROJECT"] = project

    write_env_file(JIRA_ENV, values)
    print(f"✓ Wrote {JIRA_ENV}")
    print(f"  URL: {url}")
    print(f"  Token: {mask_token(token)}")
    if project:
        print(f"  Default project: {project}")

    covered, msg = check_gitignore()
    print(f"  {msg}")
    if not covered:
        print("  → Add this line to .gitignore now:  .env")

    print("\nRunning connectivity test...")
    ok, info = test_jira(read_env_file(JIRA_ENV))
    if ok:
        print(f"✓ Connected to your Jira instance.\n  - {info}")
        print("\nYou can now use @ba-jira to publish stories, search tickets, manage sprints.")
        return 0
    print(f"✗ Could not connect.\n  - {info}", file=sys.stderr)
    print(f"\nPrevious config (if any) preserved at {JIRA_ENV.with_suffix('.env.bak')}",
          file=sys.stderr)
    return 1


def cmd_confluence(args: argparse.Namespace) -> int:
    try:
        url = validate_url(args.url)
        token = validate_token(args.token)
    except ValidationError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 2

    values = {"CONFLUENCE_BASE_URL": url, "CONFLUENCE_PAT": token}
    if args.space:
        values["CONFLUENCE_DEFAULT_SPACE"] = args.space.strip().upper()

    write_env_file(CONF_ENV, values)
    print(f"✓ Wrote {CONF_ENV}")
    print(f"  URL: {url}")
    print(f"  Token: {mask_token(token)}")
    if args.space:
        print(f"  Default space: {args.space.strip().upper()}")

    covered, msg = check_gitignore()
    print(f"  {msg}")

    print("\nRunning connectivity test...")
    ok, info = test_confluence(read_env_file(CONF_ENV))
    if ok:
        print(f"✓ Connected to your Confluence instance.\n  - {info}")
        print("\nYou can now use @ba-confluence to publish docs, import pages.")
        return 0
    print(f"✗ Could not connect.\n  - {info}", file=sys.stderr)
    return 1


def cmd_test(args: argparse.Namespace) -> int:
    if args.provider not in TESTS:
        print(f"Unknown provider: {args.provider}. "
              f"Choose: {', '.join(TESTS.keys())}", file=sys.stderr)
        return 2
    ok, info = TESTS[args.provider]()
    icon = "✓" if ok else "✗"
    print(f"{icon} {args.provider}: {info}")
    return 0 if ok else 1


def cmd_status(args: argparse.Namespace) -> int:
    print("## BA-Kit Setup Status\n")

    # Jira
    jira_env = read_env_file(JIRA_ENV)
    if jira_env.get("JIRA_BASE_URL"):
        print(f"✓ Jira configured")
        print(f"  URL: {jira_env['JIRA_BASE_URL']}")
        if jira_env.get("JIRA_PAT"):
            print(f"  Token: {mask_token(jira_env['JIRA_PAT'])}")
        if jira_env.get("JIRA_DEFAULT_PROJECT"):
            print(f"  Default project: {jira_env['JIRA_DEFAULT_PROJECT']}")
    else:
        print("✗ Jira not configured (run: @ba-setup jira)")

    print()

    # Confluence
    conf_env = read_env_file(CONF_ENV)
    if conf_env.get("CONFLUENCE_BASE_URL"):
        print(f"✓ Confluence configured")
        print(f"  URL: {conf_env['CONFLUENCE_BASE_URL']}")
        if conf_env.get("CONFLUENCE_PAT"):
            print(f"  Token: {mask_token(conf_env['CONFLUENCE_PAT'])}")
    else:
        print("✗ Confluence not configured (run: @ba-setup confluence)")

    print()

    # Second-opinion (env var driven)
    if os.environ.get("GEMINI_API_KEY"):
        print(f"✓ Gemini configured (env: GEMINI_API_KEY)")
    elif os.environ.get("OPENAI_API_KEY"):
        print(f"✓ OpenAI configured (env: OPENAI_API_KEY)")
    elif os.environ.get("OLLAMA_HOST"):
        print(f"✓ Ollama configured (env: OLLAMA_HOST)")
    else:
        print("○ Second-opinion: manual mode (no API key set, paste-into-other-tool)")

    print()
    covered, msg = check_gitignore()
    print(msg)
    return 0


# ---------------------------------------------------------------------------
# CLI wiring
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="BA-Kit one-time setup wizard helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    jira = sub.add_parser("jira", help="Configure Jira connector")
    jira.add_argument("--url", required=True)
    jira.add_argument("--token", required=True)
    jira.add_argument("--project", default=None)
    jira.set_defaults(func=cmd_jira)

    conf = sub.add_parser("confluence", help="Configure Confluence connector")
    conf.add_argument("--url", required=True)
    conf.add_argument("--token", required=True)
    conf.add_argument("--space", default=None)
    conf.set_defaults(func=cmd_confluence)

    test = sub.add_parser("test", help="Test connectivity for a provider")
    test.add_argument("provider", choices=sorted(TESTS.keys()))
    test.set_defaults(func=cmd_test)

    status = sub.add_parser("status", help="Show what's configured (masked)")
    status.set_defaults(func=cmd_status)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
