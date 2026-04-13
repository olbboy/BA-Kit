#!/usr/bin/env python3
"""
ba_second_opinion.py — Cross-model reviewer for BA-Kit.

Invokes a second LLM (Gemini / OpenAI / Ollama) to independently review a
BA artifact, then outputs JSON for @ba-second-opinion to reconcile against
the primary verdict.

Providers (auto-detected via env vars):
    GEMINI_API_KEY → Gemini 1.5 Pro (Google)
    OPENAI_API_KEY → GPT-4o (OpenAI)
    OLLAMA_HOST    → local Ollama (default: http://localhost:11434)
    (none)         → manual mode: print prompt + wait for user to paste response

Zero external dependencies — uses stdlib urllib only.

Usage:
    ba_second_opinion.py review --artifact outputs/.../US.md \\
                                --out reports/second.json
    ba_second_opinion.py review --artifact X.md --provider ollama --model llama3
    ba_second_opinion.py prompt --artifact X.md        # print prompt only

The prompt is normalized so any model can answer with the same JSON schema.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


CANONICAL_PROMPT = """You are reviewing a Business Analysis artifact for quality. Your job:

1. Read the artifact below.
2. Flag issues in 4 dimensions:
   - ambiguity    (vague language, undefined terms)
   - missing_edge_cases (happy-path-only scenarios)
   - unstated_assumptions (things that must be true but aren't written)
   - testability  (can a tester execute this?)
3. For each issue, give:
   - severity: H | M | L
   - location: line number or section header
   - evidence: quote from the artifact
   - mitigation: specific edit
4. Output verdict: PASS | CONDITIONAL | REJECT

Output STRICT JSON. No prose outside the JSON. Schema:

{
  "verdict": "PASS|CONDITIONAL|REJECT",
  "findings": [
    {
      "dimension": "ambiguity|missing_edge_cases|unstated_assumptions|testability",
      "severity": "H|M|L",
      "location": "line 42 | §3.2",
      "evidence": "quoted text",
      "mitigation": "specific edit"
    }
  ]
}

<ARTIFACT>
{artifact_text}
</ARTIFACT>
"""


# ---------------------------------------------------------------------------
# Provider detection
# ---------------------------------------------------------------------------

def detect_provider(explicit: str | None) -> str:
    if explicit and explicit != "auto":
        return explicit
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("OLLAMA_HOST"):
        return "ollama"
    return "manual"


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def _post_json(url: str, payload: dict, headers: dict, timeout: int = 120) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore") if e.fp else ""
        raise RuntimeError(f"HTTP {e.code}: {body[:500]}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"URL error: {e.reason}") from e


# ---------------------------------------------------------------------------
# Provider implementations
# ---------------------------------------------------------------------------

def review_gemini(prompt: str, model: str) -> dict:
    key = os.environ["GEMINI_API_KEY"]
    url = (f"https://generativelanguage.googleapis.com/v1beta/"
           f"models/{model}:generateContent?key={key}")
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2048},
    }
    resp = _post_json(url, payload, {"Content-Type": "application/json"})
    text = resp["candidates"][0]["content"]["parts"][0]["text"]
    return {"raw": text, "provider": "gemini", "model": model}


def review_openai(prompt: str, model: str) -> dict:
    key = os.environ["OPENAI_API_KEY"]
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2048,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    }
    resp = _post_json(url, payload, headers)
    text = resp["choices"][0]["message"]["content"]
    return {"raw": text, "provider": "openai", "model": model}


def review_ollama(prompt: str, model: str) -> dict:
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    url = f"{host.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3},
    }
    resp = _post_json(url, payload, {"Content-Type": "application/json"})
    return {"raw": resp.get("response", ""), "provider": "ollama", "model": model}


def review_manual(prompt: str, model: str) -> dict:
    """Print prompt, tell user to paste into another model, wait for paste."""
    print("=" * 70)
    print("MANUAL MODE — no API key configured.")
    print("1. Copy the prompt below into Gemini / ChatGPT / Claude.ai.")
    print("2. Copy the JSON response back here (Ctrl-D to end input).")
    print("=" * 70)
    print(prompt)
    print("=" * 70)
    print("Paste JSON response then Ctrl-D:")
    pasted = sys.stdin.read()
    return {"raw": pasted, "provider": "manual", "model": "user-chosen"}


PROVIDERS = {
    "gemini": (review_gemini, "gemini-1.5-pro"),
    "openai": (review_openai, "gpt-4o"),
    "ollama": (review_ollama, "llama3"),
    "manual": (review_manual, "manual"),
}


# ---------------------------------------------------------------------------
# Core review flow
# ---------------------------------------------------------------------------

def build_prompt(artifact_path: Path) -> str:
    text = artifact_path.read_text()
    # Simple substitution to avoid f-string brace conflicts
    return CANONICAL_PROMPT.replace("{artifact_text}", text)


def parse_review_json(raw: str) -> dict | None:
    """Extract the JSON block from model output. Models often wrap in ```json."""
    raw = raw.strip()
    # Strip code fences
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = [l for l in lines if not l.startswith("```")]
        raw = "\n".join(lines)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to find first { ... last }
        start = raw.find("{")
        end = raw.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(raw[start:end + 1])
            except json.JSONDecodeError:
                return None
    return None


# ---------------------------------------------------------------------------
# Sub-commands
# ---------------------------------------------------------------------------

def cmd_prompt(args: argparse.Namespace) -> int:
    path = Path(args.artifact)
    if not path.exists():
        print(f"Artifact not found: {path}", file=sys.stderr)
        return 2
    print(build_prompt(path))
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    path = Path(args.artifact)
    if not path.exists():
        print(f"Artifact not found: {path}", file=sys.stderr)
        return 2

    provider = detect_provider(args.provider)
    if provider not in PROVIDERS:
        print(f"Unknown provider: {provider}", file=sys.stderr)
        return 2

    prompt = build_prompt(path)
    review_fn, default_model = PROVIDERS[provider]
    model = args.model or default_model

    print(f"Using provider: {provider} (model: {model})", file=sys.stderr)

    try:
        result = review_fn(prompt, model)
    except Exception as e:
        print(f"Provider call failed: {e}", file=sys.stderr)
        if args.fallback == "manual":
            print("Falling back to manual mode...", file=sys.stderr)
            result = review_manual(prompt, model)
        else:
            return 3

    parsed = parse_review_json(result["raw"])
    output = {
        "artifact": str(path),
        "provider": result["provider"],
        "model": result["model"],
        "raw": result["raw"],
        "parsed": parsed,
        "parse_ok": parsed is not None,
    }

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(output, indent=2))
        print(f"Wrote {out_path}", file=sys.stderr)
    else:
        print(json.dumps(output, indent=2))

    return 0 if parsed else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="BA-Kit second-opinion reviewer")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("prompt", help="Print canonical prompt for an artifact")
    pr.add_argument("--artifact", required=True)
    pr.set_defaults(func=cmd_prompt)

    rv = sub.add_parser("review", help="Run review via configured provider")
    rv.add_argument("--artifact", required=True)
    rv.add_argument("--provider", default="auto",
                    help="auto | gemini | openai | ollama | manual")
    rv.add_argument("--model", default=None)
    rv.add_argument("--out", default=None)
    rv.add_argument("--fallback", default="manual", choices=["manual", "fail"])
    rv.set_defaults(func=cmd_review)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
