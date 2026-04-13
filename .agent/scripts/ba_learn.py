#!/usr/bin/env python3
"""
ba_learn.py — Per-project emergent memory for BA-Kit.

JSONL-backed memory store for patterns, pitfalls, preferences, and
stakeholder habits discovered during BA work. Used by the @ba-learn agent
and by other skills as an auto-capture target.

Storage: ~/.ba-kit/projects/{slug}/learnings.jsonl
One line = one learning. Deduplicated by (type, key) — latest wins.

Usage:
    ba_learn.py add --type pitfall --key X --insight "..." --confidence 8
    ba_learn.py show [--limit 20]
    ba_learn.py search "query"
    ba_learn.py stats
    ba_learn.py export --to AGENTS.md --min-confidence 7
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


VALID_TYPES = {"pattern", "pitfall", "preference", "ambiguity", "stakeholder"}

PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),               # US SSN
    re.compile(r"\b\d{16}\b"),                          # credit card
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),  # email
    re.compile(r"\b(?:bearer|api[_-]?key)[\s:=]+[A-Za-z0-9_\-]{10,}\b", re.I),
]


def _store_root() -> Path:
    return Path(os.path.expanduser("~/.ba-kit/projects"))


def _project_slug() -> str:
    """Derive project slug from git remote or CWD basename."""
    try:
        import subprocess
        r = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=False,
        )
        if r.returncode == 0 and r.stdout.strip():
            url = r.stdout.strip()
            # Extract repo name from URL
            name = url.rstrip("/").split("/")[-1].removesuffix(".git")
            return name
    except Exception:
        pass
    return Path.cwd().name


def _jsonl_path(slug: str | None = None) -> Path:
    slug = slug or _project_slug()
    path = _store_root() / slug / "learnings.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _has_pii(text: str) -> bool:
    return any(p.search(text) for p in PII_PATTERNS)


def _load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries: list[dict] = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def _dedupe(entries: list[dict]) -> list[dict]:
    """Keep latest entry per (type, key)."""
    by_key: dict[tuple[str, str], dict] = {}
    for e in entries:
        k = (e.get("type", ""), e.get("key", ""))
        existing = by_key.get(k)
        if not existing or e.get("ts", "") > existing.get("ts", ""):
            by_key[k] = e
    return list(by_key.values())


def _save(path: Path, entries: list[dict]) -> None:
    """Rewrite the file with deduplicated entries."""
    path.write_text("\n".join(json.dumps(e) for e in entries) + "\n")


# ---------------------------------------------------------------------------
# Public API (importable from other skills)
# ---------------------------------------------------------------------------

def capture(
    skill: str,
    type: str,
    key: str,
    insight: str,
    confidence: int = 5,
    source: str = "observed",
    artifacts: list[str] | None = None,
    slug: str | None = None,
) -> bool:
    """Append a learning. Returns True if saved, False if rejected.

    Used by other BA-Kit skills as an auto-capture hook:

        from ba_learn import capture
        capture(
          skill="ba-validation",
          type="pitfall",
          key="OFFLINE_MODE_AC_CHURN",
          insight="Offline mode AC rewrites 5x — elicitation gap with PO",
          confidence=8,
          artifacts=["outputs/.../US-ATTEN-03.md"],
        )
    """
    if type not in VALID_TYPES:
        return False
    if confidence < 3 and source != "user-stated":
        return False
    if _has_pii(insight):
        return False

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "skill": skill,
        "type": type,
        "key": key,
        "insight": insight,
        "confidence": max(1, min(10, int(confidence))),
        "source": source,
        "artifacts": artifacts or [],
    }
    path = _jsonl_path(slug)
    entries = _dedupe(_load(path) + [entry])
    _save(path, entries)
    return True


# ---------------------------------------------------------------------------
# CLI sub-commands
# ---------------------------------------------------------------------------

def cmd_add(args: argparse.Namespace) -> int:
    ok = capture(
        skill="ba-learn",
        type=args.type,
        key=args.key,
        insight=args.insight,
        confidence=args.confidence,
        source="user-stated",
        artifacts=args.artifacts or [],
        slug=args.slug,
    )
    if not ok:
        print("Rejected: check type, confidence ≥ 3, no PII", file=sys.stderr)
        return 2
    print(f"✓ Added {args.type}/{args.key}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    entries = sorted(_load(_jsonl_path(args.slug)),
                     key=lambda e: e.get("ts", ""), reverse=True)[:args.limit]
    if not entries:
        print("No learnings yet.")
        return 0
    grouped: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        grouped[e.get("type", "other")].append(e)
    for t in sorted(grouped):
        print(f"\n### {t.capitalize()} ({len(grouped[t])})")
        for e in grouped[t]:
            conf = e.get("confidence", "?")
            print(f"- `{e.get('key', '?')}` (conf {conf}): {e.get('insight', '')[:100]}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    q = args.query.lower()
    results = [
        e for e in _load(_jsonl_path(args.slug))
        if q in (e.get("insight", "") + " " + e.get("key", "")).lower()
    ]
    if args.type:
        results = [e for e in results if e.get("type") == args.type]
    # Sort by confidence desc, then ts desc
    results.sort(key=lambda e: (-e.get("confidence", 0), e.get("ts", "")), reverse=False)
    if not results:
        print("No matches.")
        return 0
    for e in results[:20]:
        print(f"[{e.get('type')}] {e.get('key')} (conf {e.get('confidence')}): "
              f"{e.get('insight', '')}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    entries = _load(_jsonl_path(args.slug))
    if not entries:
        print("No learnings yet.")
        return 0
    type_counts = Counter(e.get("type", "") for e in entries)
    conf_buckets = Counter(
        "high" if e.get("confidence", 0) >= 8
        else "medium" if e.get("confidence", 0) >= 5
        else "low"
        for e in entries
    )
    print(f"Total entries: {len(entries)}")
    print("By type: " + " ".join(f"{t}({n})" for t, n in type_counts.most_common()))
    print("By confidence: " + " ".join(f"{b}({n})" for b, n in conf_buckets.items()))
    if entries:
        oldest = min(e.get("ts", "") for e in entries)
        print(f"Oldest: {oldest[:10]}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    entries = [
        e for e in _load(_jsonl_path(args.slug))
        if e.get("confidence", 0) >= args.min_confidence
    ]
    if not entries:
        print("Nothing to export at this confidence threshold.")
        return 0
    grouped: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        grouped[e.get("type", "other")].append(e)

    lines = ["## 🧠 BA-Kit Learnings (auto-generated)\n"]
    for t in sorted(grouped):
        lines.append(f"### {t.capitalize()}")
        for e in grouped[t]:
            lines.append(f"- {e.get('insight', '')} (confidence: {e.get('confidence')})")
        lines.append("")
    block = "\n".join(lines)

    if args.to:
        target = Path(args.to)
        existing = target.read_text() if target.exists() else ""
        # Replace or append block
        marker_start = "<!-- BA-LEARN:START -->"
        marker_end = "<!-- BA-LEARN:END -->"
        wrapped = f"\n{marker_start}\n{block}\n{marker_end}\n"
        if marker_start in existing:
            pre, _, rest = existing.partition(marker_start)
            _, _, post = rest.partition(marker_end)
            target.write_text(pre + wrapped.strip() + post)
        else:
            target.write_text(existing + wrapped)
        print(f"✓ Exported to {target}")
    else:
        print(block)
    return 0


# ---------------------------------------------------------------------------
# CLI wiring
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="BA-Kit emergent memory")
    p.add_argument("--slug", default=None, help="Project slug override")
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add")
    add.add_argument("--type", required=True, choices=sorted(VALID_TYPES))
    add.add_argument("--key", required=True)
    add.add_argument("--insight", required=True)
    add.add_argument("--confidence", type=int, default=5)
    add.add_argument("--artifacts", nargs="*")
    add.set_defaults(func=cmd_add)

    show = sub.add_parser("show")
    show.add_argument("--limit", type=int, default=20)
    show.set_defaults(func=cmd_show)

    srch = sub.add_parser("search")
    srch.add_argument("query")
    srch.add_argument("--type", choices=sorted(VALID_TYPES))
    srch.set_defaults(func=cmd_search)

    stats = sub.add_parser("stats")
    stats.set_defaults(func=cmd_stats)

    exp = sub.add_parser("export")
    exp.add_argument("--to", help="Write to file instead of stdout")
    exp.add_argument("--min-confidence", type=int, default=7)
    exp.set_defaults(func=cmd_export)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
