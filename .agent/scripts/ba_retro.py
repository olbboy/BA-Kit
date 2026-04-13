#!/usr/bin/env python3
"""
ba_retro.py — Requirements sprint retrospective computer for BA-Kit.

Reads git log (only commits touching outputs/**/*.md) plus JSONL event streams
from .ba-kit/metrics/ and produces a time-windowed retro report anchored to
concrete commits.

Used by the @ba-retro agent as its mechanical data source. The agent applies
narrative reflection on top.

Usage:
    python3 ba_retro.py --window 7d
    python3 ba_retro.py --window 14d --project mini-app-cham-cong
    python3 ba_retro.py --compare --window 7d
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SESSION_GAP_MINUTES = 45  # gstack /retro convention
HEALTHY_CHURN_MAX = 0.20  # 20% threshold before flagging

METRICS_DIR = Path(".ba-kit/metrics")
RETROS_DIR = Path(".ba-kit/retros")


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

@dataclass
class Commit:
    sha: str
    author: str
    ts: datetime
    subject: str
    files: list[str]
    insertions: int = 0
    deletions: int = 0


@dataclass
class RetroMetrics:
    window: str
    project: str
    shipped: int = 0
    churned: int = 0
    churn_rate: float = 0.0
    commits_total: int = 0
    session_count: int = 0
    domain_hotspots: list[tuple[str, int]] = field(default_factory=list)
    authors: dict[str, dict] = field(default_factory=dict)
    gate_pass_rate: float | None = None
    rtm_coverage: float | None = None
    drift_findings: int | None = None
    cycle_time_days: float | None = None


# ---------------------------------------------------------------------------
# Git
# ---------------------------------------------------------------------------

def parse_window(window: str) -> timedelta:
    m = re.fullmatch(r"(\d+)([hdw])", window)
    if not m:
        raise ValueError(f"Invalid window: {window}. Use 24h, 7d, 14d, 4w")
    n, unit = int(m.group(1)), m.group(2)
    return {"h": timedelta(hours=n),
            "d": timedelta(days=n),
            "w": timedelta(weeks=n)}[unit]


def get_commits(since: datetime, pattern: str = "outputs/**/*.md") -> list[Commit]:
    """Return commits touching the given pattern since given datetime."""
    since_iso = since.strftime("%Y-%m-%dT%H:%M:%S")
    raw = subprocess.run(
        ["git", "log", f"--since={since_iso}",
         "--format=%H|%an|%aI|%s", "--numstat", "--", pattern],
        capture_output=True, text=True, check=False,
    )
    if raw.returncode != 0:
        return []

    commits: list[Commit] = []
    current: Commit | None = None
    for line in raw.stdout.splitlines():
        if "|" in line and len(line.split("|")) >= 4 and not line[0].isdigit():
            if current:
                commits.append(current)
            sha, author, ts, subject = line.split("|", 3)
            current = Commit(
                sha=sha[:7],
                author=author,
                ts=datetime.fromisoformat(ts),
                subject=subject,
                files=[],
            )
        elif line.strip() and current:
            parts = line.split("\t")
            if len(parts) == 3:
                ins, dels, path = parts
                current.files.append(path)
                try:
                    current.insertions += int(ins)
                    current.deletions += int(dels)
                except ValueError:
                    pass
    if current:
        commits.append(current)
    return commits


# ---------------------------------------------------------------------------
# Metrics computation
# ---------------------------------------------------------------------------

def compute_sessions(commits: list[Commit]) -> int:
    """Group commits with < 45min gap → 1 session."""
    if not commits:
        return 0
    sorted_c = sorted(commits, key=lambda c: c.ts)
    sessions = 1
    for prev, cur in zip(sorted_c, sorted_c[1:]):
        gap = (cur.ts - prev.ts).total_seconds() / 60
        if gap > SESSION_GAP_MINUTES:
            sessions += 1
    return sessions


def extract_domain(path: str) -> str | None:
    """outputs/{project}/modules/{domain}/... → {domain}

    Strips git rename syntax `{old => new}` and picks the post-rename path.
    """
    # Collapse git rename syntax: "a/{b => c}/d" → "a/c/d"
    if "{" in path and "=>" in path:
        path = re.sub(r"\{[^}]*=>\s*([^}]+)\}", r"\1", path)
        path = path.replace("//", "/")
    m = re.match(r"outputs/[^/]+/modules/([^/]+)/", path)
    if m:
        return m.group(1)
    m = re.match(r"outputs/[^/]+/([^/]+)/", path)
    return m.group(1) if m else None


def compute_domain_hotspots(commits: list[Commit], top: int = 5) -> list[tuple[str, int]]:
    c = Counter()
    for commit in commits:
        for f in commit.files:
            d = extract_domain(f)
            if d:
                c[d] += 1
    return c.most_common(top)


def compute_author_leaderboard(commits: list[Commit]) -> dict[str, dict]:
    leaderboard: dict[str, dict] = defaultdict(
        lambda: {"commits": 0, "new_artifacts": 0, "insertions": 0, "focus": Counter()}
    )
    for c in commits:
        leaderboard[c.author]["commits"] += 1
        leaderboard[c.author]["insertions"] += c.insertions
        for f in c.files:
            d = extract_domain(f)
            if d:
                leaderboard[c.author]["focus"][d] += 1
    # Convert Counter to top-2 list
    for author, data in leaderboard.items():
        focus = data["focus"].most_common(2)
        data["focus"] = [d[0] for d in focus]
    return dict(leaderboard)


def compute_churn(commits: list[Commit]) -> tuple[int, float]:
    """Artifacts edited ≥ 3 times = churned."""
    file_hits = Counter()
    for c in commits:
        for f in c.files:
            file_hits[f] += 1
    total_files = len(file_hits)
    if total_files == 0:
        return 0, 0.0
    churned = sum(1 for hits in file_hits.values() if hits >= 3)
    return churned, churned / total_files


# ---------------------------------------------------------------------------
# Optional JSONL metrics
# ---------------------------------------------------------------------------

def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def load_autoreview_metrics(project: str, since: datetime) -> dict:
    runs = load_jsonl(METRICS_DIR / f"autoreview-{project}.jsonl")
    recent = [r for r in runs if datetime.fromisoformat(r.get("ts", "")) >= since]
    if not recent:
        return {}
    pass_count = sum(1 for r in recent if r.get("verdict") == "PASS")
    return {
        "run_count": len(recent),
        "pass_rate": pass_count / len(recent),
        "avg_findings": sum(r.get("findings_total", 0) for r in recent) / len(recent),
    }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def render(metrics: RetroMetrics, window: str, prior: dict | None = None) -> str:
    lines: list[str] = []
    lines.append(f"# Requirements Sprint Retro — {window} — {datetime.now():%Y-%m-%d}")
    lines.append("")
    lines.append(
        f"> **Tweetable:** {metrics.shipped} new artifacts shipped across "
        f"{len(metrics.domain_hotspots)} domains in {metrics.session_count} sessions."
    )
    lines.append("")

    lines.append("## 📥 Activity summary\n")
    lines.append(f"- Total commits: **{metrics.commits_total}**")
    lines.append(f"- New artifacts: **{metrics.shipped}**")
    lines.append(f"- Churned (≥3 edits): **{metrics.churned}** "
                 f"({metrics.churn_rate:.0%})")
    lines.append(f"- Sessions (<45min gap): **{metrics.session_count}**")
    lines.append("")

    if metrics.domain_hotspots:
        lines.append("## 🔥 Domain hotspots\n")
        lines.append("| Rank | Domain | Edits |")
        lines.append("|------|--------|-------|")
        for i, (d, n) in enumerate(metrics.domain_hotspots, 1):
            lines.append(f"| {i} | {d} | {n} |")
        lines.append("")

    if metrics.authors:
        lines.append("## 👤 Per-author leaderboard\n")
        lines.append("| Author | Commits | Focus |")
        lines.append("|--------|---------|-------|")
        sorted_authors = sorted(
            metrics.authors.items(),
            key=lambda x: x[1]["commits"],
            reverse=True,
        )
        for name, data in sorted_authors:
            focus = ", ".join(data["focus"]) or "—"
            lines.append(f"| {name} | {data['commits']} | {focus} |")
        lines.append("")

    if metrics.gate_pass_rate is not None:
        lines.append("## 🛡️ Quality gate snapshot\n")
        lines.append(f"- Gate pass rate: **{metrics.gate_pass_rate:.0%}**")
        lines.append("")

    if metrics.churn_rate > HEALTHY_CHURN_MAX:
        lines.append("## ⚠️ Concerns\n")
        lines.append(f"- Churn rate {metrics.churn_rate:.0%} exceeds "
                     f"healthy threshold of {HEALTHY_CHURN_MAX:.0%}. "
                     "Investigate top-edited artifacts; likely elicitation gap.")
        lines.append("")

    lines.append("---")
    lines.append("> Raw metrics below. The `@ba-retro` agent applies narrative "
                 "reflection before presenting to users.")
    return "\n".join(lines)


def snapshot(metrics: RetroMetrics) -> dict:
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "window": metrics.window,
        "project": metrics.project,
        "shipped": metrics.shipped,
        "churned": metrics.churned,
        "churn_rate": metrics.churn_rate,
        "session_count": metrics.session_count,
        "commits_total": metrics.commits_total,
        "hotspot_domains": [d for d, _ in metrics.domain_hotspots],
        "authors": {k: {kk: vv for kk, vv in v.items() if kk != "focus_counter"}
                    for k, v in metrics.authors.items()},
        "gate_pass_rate": metrics.gate_pass_rate,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="BA-Kit requirements sprint retro")
    p.add_argument("--window", default="7d", help="24h, 7d, 14d, 4w")
    p.add_argument("--project", default="default", help="Project slug for metrics lookup")
    p.add_argument("--out", type=Path, default=None, help="Output markdown path")
    p.add_argument("--compare", action="store_true",
                   help="Include delta vs prior same-length window (future work)")
    args = p.parse_args(argv)

    try:
        delta = parse_window(args.window)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2

    since = datetime.now(timezone.utc) - delta
    commits = get_commits(since)
    if not commits:
        print(f"No commits touching outputs/**/*.md in the last {args.window}.")
        return 0

    churned, churn_rate = compute_churn(commits)
    metrics = RetroMetrics(
        window=args.window,
        project=args.project,
        shipped=sum(1 for c in commits if c.subject.startswith(("feat", "docs"))),
        churned=churned,
        churn_rate=churn_rate,
        commits_total=len(commits),
        session_count=compute_sessions(commits),
        domain_hotspots=compute_domain_hotspots(commits),
        authors=compute_author_leaderboard(commits),
    )

    # Optional: enrich with autoreview metrics if stream exists
    ar = load_autoreview_metrics(args.project, since)
    if ar:
        metrics.gate_pass_rate = ar["pass_rate"]

    report = render(metrics, args.window)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report)
        print(f"Wrote {args.out}")
    else:
        print(report)

    # Save snapshot for future comparisons
    RETROS_DIR.mkdir(parents=True, exist_ok=True)
    snap_path = RETROS_DIR / f"{args.project}-{datetime.now():%Y-%m-%d}.json"
    snap_path.write_text(json.dumps(snapshot(metrics), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
