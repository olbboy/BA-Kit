#!/usr/bin/env python3
"""
ba_as_built.py — Spec drift detector for BA-Kit.

Compares git-tracked code changes against spec artifacts (BRD/SRS/RTM) and
surfaces three buckets:
    A. spec-only   — claimed in spec, no code (ghost features)
    B. code-only   — shipped in code, no spec (undocumented)
    C. both-differ — spec says X, code does Y (drift)

Used by the @ba-as-built agent as its read-side helper. Agent handles the
reflection/reporting; this script handles the mechanical git + grep work.

Usage:
    python3 ba_as_built.py scan   --project outputs/mini-app-cham-cong --base main
    python3 ba_as_built.py report --project outputs/mini-app-cham-cong --base main \\
                                  --out reports/as-built-drift-report.md

Read-only on the repo. Never modifies code or specs.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Commit:
    sha: str
    author: str
    date: str
    subject: str
    files: list[str]
    classification: str  # feat | fix | refactor | schema | api | other


@dataclass
class SpecArtifact:
    path: str
    type: str  # BRD | US | API | DB | TC | OTHER
    ids: list[str]


@dataclass
class Finding:
    bucket: str           # spec_only | code_only | both_differ
    severity: str         # H | M | L
    confidence: str       # H | M | L
    title: str
    evidence: dict        # {commit_sha, file_line, grep_result, ...}


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def _run(cmd: list[str]) -> str:
    """Run a git command, return stdout. Raise on non-zero exit."""
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"git failed: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout


def get_commits(base: str, head: str = "HEAD") -> list[Commit]:
    """Return commits in <base>..<head> with file lists and classification."""
    raw = _run([
        "git", "log", f"{base}..{head}",
        "--format=%H|%an|%aI|%s",
        "--name-only",
    ])
    commits: list[Commit] = []
    current: dict | None = None
    for line in raw.splitlines():
        if "|" in line and len(line.split("|")) >= 4:
            if current:
                commits.append(_finalize_commit(current))
            parts = line.split("|", 3)
            current = {
                "sha": parts[0][:7],
                "author": parts[1],
                "date": parts[2][:10],
                "subject": parts[3],
                "files": [],
            }
        elif line.strip() and current is not None:
            current["files"].append(line.strip())
    if current:
        commits.append(_finalize_commit(current))
    return commits


def _finalize_commit(d: dict) -> Commit:
    return Commit(
        sha=d["sha"],
        author=d["author"],
        date=d["date"],
        subject=d["subject"],
        files=d["files"],
        classification=_classify(d["subject"], d["files"]),
    )


def _classify(subject: str, files: list[str]) -> str:
    subj = subject.lower()
    if any("migration" in f or "schema" in f for f in files):
        return "schema"
    if any(re.search(r"(api|routes?|controllers?)/", f) for f in files):
        return "api"
    if subj.startswith("feat"):
        return "feat"
    if subj.startswith("fix"):
        return "fix"
    if subj.startswith("refactor"):
        return "refactor"
    return "other"


# ---------------------------------------------------------------------------
# Spec scanning
# ---------------------------------------------------------------------------

SPEC_ID_PATTERNS = {
    "BRD": re.compile(r"\bBIZ-\d+\b"),
    "US":  re.compile(r"\bUS-[A-Z0-9]+-\d+\b"),
    "API": re.compile(r"\bAPI-[A-Z0-9]+\b"),
    "DB":  re.compile(r"\bTBL_[A-Z0-9_]+\b"),
    "TC":  re.compile(r"\bTC-[A-Z0-9]+-\d+\b"),
}


def scan_specs(project_root: Path) -> list[SpecArtifact]:
    """Walk outputs/{project}/ and classify each markdown file by ID patterns."""
    artifacts: list[SpecArtifact] = []
    for md in project_root.rglob("*.md"):
        if any(part.startswith(".") for part in md.parts):
            continue
        text = md.read_text(errors="ignore")
        ids_by_type: dict[str, list[str]] = {}
        for spec_type, pattern in SPEC_ID_PATTERNS.items():
            found = pattern.findall(text)
            if found:
                ids_by_type.setdefault(spec_type, []).extend(set(found))
        if not ids_by_type:
            continue
        # Pick dominant type for this file
        dominant = max(ids_by_type.keys(), key=lambda k: len(ids_by_type[k]))
        all_ids = [i for lst in ids_by_type.values() for i in lst]
        artifacts.append(SpecArtifact(
            path=str(md),
            type=dominant,
            ids=sorted(set(all_ids)),
        ))
    return artifacts


# ---------------------------------------------------------------------------
# Drift computation
# ---------------------------------------------------------------------------

def compute_drift(commits: list[Commit], specs: list[SpecArtifact]) -> list[Finding]:
    """Produce Finding objects for each drift bucket.

    Heuristics are intentionally conservative — the agent applies System 2
    review on top of these raw findings before reporting to the user.
    """
    findings: list[Finding] = []

    # Bucket B: code-only — feat commits that don't map to any spec ID in the
    # same commit subject or files. This is coarse; the agent refines.
    all_spec_ids = {i for a in specs for i in a.ids}
    for c in commits:
        if c.classification != "feat":
            continue
        # Does the commit subject or any file name reference any known spec ID?
        haystack = c.subject + " " + " ".join(c.files)
        if not any(sid in haystack for sid in all_spec_ids):
            findings.append(Finding(
                bucket="code_only",
                severity="M",
                confidence="M",
                title=f"Undocumented feature: {c.subject}",
                evidence={
                    "commit_sha": c.sha,
                    "files": c.files[:5],
                    "author": c.author,
                    "date": c.date,
                },
            ))

    # Bucket A: spec-only — spec IDs mentioned in docs but never touched by
    # any commit in the range. Proxy: spec ID never appears in any commit
    # subject or file path. Again, coarse.
    referenced_in_code: set[str] = set()
    for c in commits:
        blob = c.subject + " " + " ".join(c.files)
        for sid in all_spec_ids:
            if sid in blob:
                referenced_in_code.add(sid)

    for artifact in specs:
        for sid in artifact.ids:
            if sid in referenced_in_code:
                continue
            findings.append(Finding(
                bucket="spec_only",
                severity="L",
                confidence="L",
                title=f"Spec ID {sid} not referenced in recent commits",
                evidence={
                    "spec_file": artifact.path,
                    "spec_type": artifact.type,
                    "note": "Low confidence — may be baselined/stable, not drift.",
                },
            ))

    # Bucket C: both-differ — requires pattern matches (e.g., HTTP status code
    # in spec vs code). Skeleton implementation: look for `status: 2\d\d` in
    # spec files and compare to code files. Extend per project.
    # Left as a hook for the agent to specialize.

    return findings


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def to_markdown(project: str, base: str, commits: list[Commit],
                specs: list[SpecArtifact], findings: list[Finding]) -> str:
    lines: list[str] = []
    lines.append(f"# As-Built Drift Report — {project}")
    lines.append(f"\n**Git range:** `{base}..HEAD` ({len(commits)} commits)")
    lines.append(f"**Spec files scanned:** {len(specs)}")
    lines.append(f"**Findings:** {len(findings)}")
    lines.append("")

    buckets = {"spec_only": [], "code_only": [], "both_differ": []}
    for f in findings:
        buckets[f.bucket].append(f)

    lines.append("## Executive summary\n")
    lines.append("| Bucket | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| 🟥 Spec-only (ghost features)    | {len(buckets['spec_only'])} |")
    lines.append(f"| 🟨 Code-only (undocumented)      | {len(buckets['code_only'])} |")
    lines.append(f"| 🟧 Both-but-differ (drift)       | {len(buckets['both_differ'])} |")
    lines.append("")

    for name, icon, items in [
        ("Spec-only findings",  "🟥", buckets["spec_only"]),
        ("Code-only findings",  "🟨", buckets["code_only"]),
        ("Both-but-differ",     "🟧", buckets["both_differ"]),
    ]:
        if not items:
            continue
        lines.append(f"## {icon} {name}\n")
        for idx, f in enumerate(items, 1):
            lines.append(f"### {idx}. {f.title}")
            lines.append(f"- **Severity:** {f.severity} | **Confidence:** {f.confidence}")
            lines.append(f"- **Evidence:**")
            for k, v in f.evidence.items():
                lines.append(f"  - `{k}`: {v}")
            lines.append("")

    lines.append("---")
    lines.append("\n> Review required. This script's output is raw — the "
                 "`@ba-as-built` agent applies System 2 review before it "
                 "becomes an action plan.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="BA-Kit spec drift detector")
    sub = p.add_subparsers(dest="cmd", required=True)

    scan = sub.add_parser("scan", help="Quick scan, JSON to stdout")
    scan.add_argument("--project", required=True, type=Path)
    scan.add_argument("--base", default="main")

    report = sub.add_parser("report", help="Full markdown report")
    report.add_argument("--project", required=True, type=Path)
    report.add_argument("--base", default="main")
    report.add_argument("--out", required=True, type=Path)

    args = p.parse_args(argv)

    if not args.project.exists():
        print(f"Project path not found: {args.project}", file=sys.stderr)
        return 2

    try:
        commits = get_commits(args.base)
    except RuntimeError as e:
        print(f"Git error: {e}", file=sys.stderr)
        return 2

    specs = scan_specs(args.project)
    findings = compute_drift(commits, specs)

    if args.cmd == "scan":
        payload = {
            "project": str(args.project),
            "base": args.base,
            "commits": [asdict(c) for c in commits],
            "specs": [asdict(s) for s in specs],
            "findings": [asdict(f) for f in findings],
        }
        print(json.dumps(payload, indent=2))
        return 0

    # report
    md = to_markdown(
        project=str(args.project),
        base=args.base,
        commits=commits,
        specs=specs,
        findings=findings,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(md)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
