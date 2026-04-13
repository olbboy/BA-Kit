#!/usr/bin/env python3
"""
ba_baseline.py — Artifact baseline manager for BA-Kit.

Locks approved BA artifacts (BRD/US/API spec/etc) with sha256 hash + rationale.
Tracks version history. Detects drift. Feeds @ba-guard for change control.

Also hosts @ba-guard sub-commands so baseline + guard share one script and
one on-disk manifest (DRY).

Storage:
    .ba-kit/baselines/manifest.json   — current baselines
    .ba-kit/baselines/history.jsonl   — append-only audit trail
    .ba-kit/guard/config.json         — guard mode (off|warn|strict)
    .ba-kit/guard/audit.jsonl         — guard check history

Usage:
    # baseline
    ba_baseline.py add <file> --version v1.0 --by <who> --rationale "..."
    ba_baseline.py list
    ba_baseline.py status <file>
    ba_baseline.py check [--strict-exit]
    ba_baseline.py supersede <file> --from v1.0 --to v1.1 --rationale "..."
    ba_baseline.py history <file>

    # guard
    ba_baseline.py guard-status
    ba_baseline.py guard-enable <mode>
    ba_baseline.py guard-check [path]
    ba_baseline.py guard-install-hook

Zero external dependencies (stdlib only).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BASELINES_DIR = Path(".ba-kit/baselines")
GUARD_DIR = Path(".ba-kit/guard")
MANIFEST = BASELINES_DIR / "manifest.json"
HISTORY = BASELINES_DIR / "history.jsonl"
GUARD_CONFIG = GUARD_DIR / "config.json"
GUARD_AUDIT = GUARD_DIR / "audit.jsonl"


# ---------------------------------------------------------------------------
# Manifest IO
# ---------------------------------------------------------------------------

def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _load_manifest() -> dict:
    if not MANIFEST.exists():
        return {"version": 1, "baselines": []}
    return json.loads(MANIFEST.read_text())


def _save_manifest(data: dict) -> None:
    BASELINES_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(data, indent=2) + "\n")


def _append_history(entry: dict) -> None:
    BASELINES_DIR.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def _hash_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
            size += len(chunk)
    return f"sha256:{h.hexdigest()}", size


# ---------------------------------------------------------------------------
# Baseline sub-commands
# ---------------------------------------------------------------------------

def _find_latest(manifest: dict, artifact: str) -> dict | None:
    """Latest baseline entry for a given artifact path."""
    entries = [e for e in manifest["baselines"] if e["artifact"] == artifact]
    return max(entries, key=lambda e: e["baselined_at"]) if entries else None


def cmd_add(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2
    if len(args.rationale) < 10:
        print("Rationale too thin (need ≥ 10 chars) — CCB requires substance.",
              file=sys.stderr)
        return 2

    digest, size = _hash_file(path)
    manifest = _load_manifest()

    # Prevent re-adding same version
    existing = _find_latest(manifest, str(path))
    if existing and existing["baseline_version"] == args.version:
        print(f"Version {args.version} already baselined. Use `supersede`.",
              file=sys.stderr)
        return 2

    entry = {
        "artifact": str(path),
        "baseline_version": args.version,
        "sha256": digest,
        "size_bytes": size,
        "baselined_at": _now(),
        "baselined_by": args.by,
        "rationale": args.rationale,
        "ccb_required": True,
        "supersedes": None,
    }
    manifest["baselines"].append(entry)
    _save_manifest(manifest)
    _append_history({"op": "add", **entry})
    print(f"✓ Baselined {path} as {args.version} ({digest[:19]}...)")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    if not manifest["baselines"]:
        print("No baselines yet.")
        return 0
    # Show latest per artifact
    latest: dict[str, dict] = {}
    for e in manifest["baselines"]:
        existing = latest.get(e["artifact"])
        if not existing or e["baselined_at"] > existing["baselined_at"]:
            latest[e["artifact"]] = e

    print(f"## Baselined artifacts ({len(latest)})\n")
    print("| Artifact | Version | Baselined | By | Drift? |")
    print("|----------|---------|-----------|----|----|")
    for path, e in sorted(latest.items()):
        drift = _drift_status(Path(path), e["sha256"])
        print(f"| {path} | {e['baseline_version']} | {e['baselined_at'][:10]} "
              f"| {e['baselined_by']} | {drift} |")
    return 0


def _drift_status(path: Path, expected: str) -> str:
    if not path.exists():
        return "🚫 missing"
    current, _ = _hash_file(path)
    return "✅ clean" if current == expected else "🚨 drifted"


def cmd_status(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    entry = _find_latest(manifest, args.file)
    if not entry:
        print(f"Not baselined: {args.file}")
        return 1
    path = Path(args.file)
    if not path.exists():
        print(f"Baseline exists but file is missing: {args.file}")
        return 2
    current, size = _hash_file(path)
    print(f"Artifact: {args.file}")
    print(f"Baselined: {entry['baseline_version']} ({entry['baselined_at']} "
          f"by {entry['baselined_by']})")
    print(f"Rationale: {entry['rationale']}")
    print(f"Baseline hash: {entry['sha256']}")
    print(f"Current hash:  {current}")
    if current == entry["sha256"]:
        print("Status: ✅ clean")
        return 0
    print("Status: 🚨 DRIFTED — file modified since baseline")
    return 1


def cmd_check(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    latest: dict[str, dict] = {}
    for e in manifest["baselines"]:
        existing = latest.get(e["artifact"])
        if not existing or e["baselined_at"] > existing["baselined_at"]:
            latest[e["artifact"]] = e

    if not latest:
        print("No baselines to check.")
        return 0

    clean = 0
    drifted: list[str] = []
    missing: list[str] = []
    for path_str, entry in latest.items():
        path = Path(path_str)
        if not path.exists():
            missing.append(path_str)
            continue
        current, _ = _hash_file(path)
        if current == entry["sha256"]:
            clean += 1
        else:
            drifted.append(path_str)

    total = len(latest)
    print(f"Scanning {total} baselined artifacts...")
    print(f"✅ Clean: {clean}")
    if drifted:
        print(f"🚨 Drifted: {len(drifted)}")
        for p in drifted:
            print(f"   - {p}")
    if missing:
        print(f"🚫 Missing: {len(missing)}")
        for p in missing:
            print(f"   - {p}")

    _log_guard_check(total, clean, drifted, missing)

    if args.strict_exit and (drifted or missing):
        return 1
    return 0


def cmd_supersede(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2
    if len(args.rationale) < 10:
        print("Rationale too thin.", file=sys.stderr)
        return 2

    manifest = _load_manifest()
    prior = _find_latest(manifest, str(path))
    if not prior:
        print(f"No prior baseline for {path}. Use `add` first.", file=sys.stderr)
        return 2
    if prior["baseline_version"] != args.from_version:
        print(f"Latest baseline is {prior['baseline_version']}, "
              f"not {args.from_version}.", file=sys.stderr)
        return 2

    digest, size = _hash_file(path)
    entry = {
        "artifact": str(path),
        "baseline_version": args.to,
        "sha256": digest,
        "size_bytes": size,
        "baselined_at": _now(),
        "baselined_by": args.by,
        "rationale": args.rationale,
        "ccb_required": True,
        "supersedes": args.from_version,
    }
    manifest["baselines"].append(entry)
    _save_manifest(manifest)
    _append_history({"op": "supersede", **entry})
    print(f"✓ Superseded {args.from_version} → {args.to} for {path}")
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    manifest = _load_manifest()
    entries = [e for e in manifest["baselines"] if e["artifact"] == args.file]
    if not entries:
        print(f"No history for {args.file}")
        return 1
    entries.sort(key=lambda e: e["baselined_at"])
    print(f"## History for {args.file}\n")
    for e in entries:
        sup = f" (supersedes {e['supersedes']})" if e["supersedes"] else ""
        print(f"{e['baseline_version']}{sup} — {e['baselined_at']} "
              f"by {e['baselined_by']}")
        print(f"  Rationale: {e['rationale']}")
        print(f"  Hash: {e['sha256'][:27]}...")
        print()
    return 0


# ---------------------------------------------------------------------------
# Guard sub-commands
# ---------------------------------------------------------------------------

DEFAULT_GUARD_CONFIG = {
    "mode": "warn",
    "enforce_ccb_tag": True,
    "exempt_paths": ["outputs/*/drafts/*"],
}


def _load_guard_config() -> dict:
    if not GUARD_CONFIG.exists():
        GUARD_DIR.mkdir(parents=True, exist_ok=True)
        GUARD_CONFIG.write_text(json.dumps(DEFAULT_GUARD_CONFIG, indent=2))
        return dict(DEFAULT_GUARD_CONFIG)
    return json.loads(GUARD_CONFIG.read_text())


def _save_guard_config(cfg: dict) -> None:
    GUARD_DIR.mkdir(parents=True, exist_ok=True)
    GUARD_CONFIG.write_text(json.dumps(cfg, indent=2))


def _log_guard_check(total: int, clean: int,
                     drifted: list[str], missing: list[str]) -> None:
    GUARD_DIR.mkdir(parents=True, exist_ok=True)
    cfg = _load_guard_config()
    entry = {
        "ts": _now(),
        "mode": cfg["mode"],
        "total": total,
        "clean": clean,
        "drifted": len(drifted),
        "missing": len(missing),
        "drift_files": drifted,
    }
    with GUARD_AUDIT.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def cmd_guard_status(args: argparse.Namespace) -> int:
    cfg = _load_guard_config()
    manifest = _load_manifest()
    total = len({e["artifact"] for e in manifest["baselines"]})
    print(f"Mode: {cfg['mode']}")
    print(f"Baselined artifacts: {total}")
    print(f"Enforce CCB tag: {cfg['enforce_ccb_tag']}")
    print(f"Exempt paths: {cfg['exempt_paths']}")
    if GUARD_AUDIT.exists():
        last = GUARD_AUDIT.read_text().strip().split("\n")[-1]
        print(f"Last check: {json.loads(last).get('ts', '?')}")
    return 0


def cmd_guard_enable(args: argparse.Namespace) -> int:
    if args.mode not in {"off", "warn", "strict"}:
        print("Mode must be: off | warn | strict", file=sys.stderr)
        return 2
    cfg = _load_guard_config()
    cfg["mode"] = args.mode
    _save_guard_config(cfg)
    print(f"✓ Guard mode = {args.mode}")
    return 0


def cmd_guard_install_hook(args: argparse.Namespace) -> int:
    hook_path = Path(".git/hooks/pre-commit")
    if not hook_path.parent.exists():
        print("Not a git repo (no .git/hooks).", file=sys.stderr)
        return 2
    hook = (
        "#!/bin/sh\n"
        "# Installed by @ba-guard\n"
        "python3 .agent/scripts/ba_baseline.py check --strict-exit\n"
        "rc=$?\n"
        "if [ $rc -ne 0 ]; then\n"
        "  echo 'ba-guard: baselined artifacts drifted. "
        "Run @ba-guard check for details.'\n"
        "  exit 1\n"
        "fi\n"
    )
    hook_path.write_text(hook)
    hook_path.chmod(0o755)
    print(f"✓ Installed pre-commit hook at {hook_path}")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="BA-Kit baseline + guard manager")
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add")
    add.add_argument("file")
    add.add_argument("--version", required=True)
    add.add_argument("--by", required=True)
    add.add_argument("--rationale", required=True)
    add.set_defaults(func=cmd_add)

    lst = sub.add_parser("list")
    lst.set_defaults(func=cmd_list)

    status = sub.add_parser("status")
    status.add_argument("file")
    status.set_defaults(func=cmd_status)

    check = sub.add_parser("check")
    check.add_argument("--strict-exit", action="store_true")
    check.set_defaults(func=cmd_check)

    sup = sub.add_parser("supersede")
    sup.add_argument("file")
    sup.add_argument("--from", dest="from_version", required=True)
    sup.add_argument("--to", required=True)
    sup.add_argument("--by", default=os.environ.get("USER", "unknown"))
    sup.add_argument("--rationale", required=True)
    sup.set_defaults(func=cmd_supersede)

    hist = sub.add_parser("history")
    hist.add_argument("file")
    hist.set_defaults(func=cmd_history)

    # Guard sub-commands
    gs = sub.add_parser("guard-status")
    gs.set_defaults(func=cmd_guard_status)

    ge = sub.add_parser("guard-enable")
    ge.add_argument("mode")
    ge.set_defaults(func=cmd_guard_enable)

    gi = sub.add_parser("guard-install-hook")
    gi.set_defaults(func=cmd_guard_install_hook)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
