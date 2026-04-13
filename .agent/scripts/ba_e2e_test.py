#!/usr/bin/env python3
"""
ba_e2e_test.py — End-to-end test runner for BA-Kit skills.

Orchestrates 5 test layers against the repo + fixture directory:

  L1 Static       YAML frontmatter, cross-refs, path refs, compile (this session)
  L2 Scripts      Python/shell helper smoke tests                  (stub, future)
  L3 Structure    Per-skill canonical sections + sanity             (this session)
  L4 Consistency  BRD↔US↔API↔DB alignment on fixture                (stub, future)
  L5 Chains       Cookbook scenarios + routing + phase coverage    (this session)

Zero external deps (stdlib only). Matches the existing ba_*.py convention.

Usage:
    python3 .agent/scripts/ba_e2e_test.py                          # all layers
    python3 .agent/scripts/ba_e2e_test.py --layers L1,L3,L5       # specific layers
    python3 .agent/scripts/ba_e2e_test.py --report plans/reports/test.md
    python3 .agent/scripts/ba_e2e_test.py --verbose
    python3 .agent/scripts/ba_e2e_test.py --fixture outputs/mini-app-cham-cong

Exit codes:
    0 — all checks pass
    1 — warnings only, no hard failures
    2 — at least one hard failure
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Literal


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_ROOT = REPO_ROOT / ".agent" / "skills"
SCRIPT_ROOT = REPO_ROOT / ".agent" / "scripts"
TEMPLATE_ROOT = REPO_ROOT / ".agent" / "templates"
DATA_ROOT = REPO_ROOT / ".agent" / "data"
DOCS_ROOT = REPO_ROOT / "docs"

COOKBOOK = DOCS_ROOT / "workflow-cookbook.md"
SPRINT_SPINE = DOCS_ROOT / "sprint-spine.md"
MASTER_SKILL = SKILL_ROOT / "ba-master" / "SKILL.md"
SETUP_SH = SCRIPT_ROOT / "setup.sh"

# Skills that are infrastructure, not BA-facing — exempt from structural/routing checks
CONNECTOR_EXEMPT = {"jira-connector", "confluence-connector"}
NON_SKILL_DIRS = {"_shared"}  # Holds system-prompt.md, not SKILL.md


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

Severity = Literal["pass", "warn", "fail", "skip"]


@dataclass
class Check:
    """One assertion with a result."""
    name: str
    target: str
    severity: Severity
    message: str = ""
    duration_ms: float = 0.0


@dataclass
class LayerVerdict:
    layer: str
    description: str
    checks: list[Check] = field(default_factory=list)
    duration_ms: float = 0.0

    @property
    def passed(self) -> int:
        return sum(1 for c in self.checks if c.severity == "pass")

    @property
    def failed(self) -> int:
        return sum(1 for c in self.checks if c.severity == "fail")

    @property
    def warned(self) -> int:
        return sum(1 for c in self.checks if c.severity == "warn")

    @property
    def skipped(self) -> int:
        return sum(1 for c in self.checks if c.severity == "skip")

    @property
    def total(self) -> int:
        return len(self.checks)

    @property
    def ok(self) -> bool:
        return self.failed == 0


@dataclass
class AggregateVerdict:
    layers: list[LayerVerdict]
    fixture: str
    started_at: str
    duration_ms: float
    repo_branch: str = ""
    repo_commit: str = ""

    @property
    def exit_code(self) -> int:
        if any(l.failed > 0 for l in self.layers):
            return 2
        if any(l.warned > 0 for l in self.layers):
            return 1
        return 0

    @property
    def verdict(self) -> str:
        code = self.exit_code
        return {0: "PASS", 1: "PASS-WITH-WARNINGS", 2: "FAIL"}[code]


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def find_skill_files() -> list[Path]:
    """All SKILL.md paths under .agent/skills/, excluding _shared."""
    skills = []
    for p in sorted(SKILL_ROOT.glob("*/SKILL.md")):
        if p.parent.name in NON_SKILL_DIRS:
            continue
        skills.append(p)
    return skills


def skill_names() -> set[str]:
    """Set of existing skill folder names (for cross-ref validation)."""
    return {p.parent.name for p in find_skill_files()}


def python_scripts() -> list[Path]:
    """All Python helper scripts under .agent/scripts/."""
    return sorted(SCRIPT_ROOT.glob("*.py"))


# ---------------------------------------------------------------------------
# YAML frontmatter parser (zero-dep, handles BA-Kit's simple schema)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split file into (frontmatter_dict, body). Minimal parser — handles
    only the keys BA-Kit uses: name, description, version, phase, inputs,
    outputs, downstream. Returns ({}, text) if no frontmatter.
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    fm_block = text[4:end].strip()
    body = text[end + 4:]

    data: dict = {}
    current_key: str | None = None
    for raw_line in fm_block.split("\n"):
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) and current_key:
            # Sub-item (list or multi-line)
            val = line.strip().lstrip("- ").strip()
            existing = data.get(current_key)
            if isinstance(existing, list):
                existing.append(val)
            else:
                data[current_key] = [val]
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            # Strip matching quotes
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
                val = val[1:-1]
            if not val:
                data[key] = None
            else:
                data[key] = val
            current_key = key
    return data, body


# ---------------------------------------------------------------------------
# L1 — Static validation
# ---------------------------------------------------------------------------

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
AGENT_REF = re.compile(r"@ba-[a-z][a-z0-9-]*")
PATH_REF_TEMPLATE = re.compile(r"\.agent/templates/([A-Za-z0-9_./\-]+\.md)")
PATH_REF_DATA = re.compile(r"\.agent/data/([A-Za-z0-9_./\-]+\.csv)")
PATH_REF_SCRIPT = re.compile(r"\.agent/scripts/([A-Za-z0-9_./\-]+\.(?:py|sh))")
CODE_FENCE = re.compile(r"```[\s\S]*?```")
INLINE_CODE = re.compile(r"`[^`\n]*`")


def _strip_code_fences(text: str) -> str:
    """Remove fenced code blocks AND inline `code spans` so regex doesn't
    match inside examples or reserved/future-work references."""
    text = CODE_FENCE.sub("", text)
    text = INLINE_CODE.sub("", text)
    return text


def check_yaml_frontmatter(skill_path: Path) -> Check:
    """Every SKILL.md must have valid frontmatter with name/description/version."""
    start = time.perf_counter()
    rel = str(skill_path.relative_to(REPO_ROOT))
    try:
        text = skill_path.read_text(encoding="utf-8")
    except Exception as e:
        return Check("yaml_frontmatter", rel, "fail", f"read error: {e}",
                     (time.perf_counter() - start) * 1000)

    fm, _ = parse_frontmatter(text)
    if not fm:
        return Check("yaml_frontmatter", rel, "fail", "no frontmatter block",
                     (time.perf_counter() - start) * 1000)
    missing = [k for k in ("name", "description", "version") if k not in fm or fm[k] is None]
    if missing:
        return Check("yaml_frontmatter", rel, "fail",
                     f"missing keys: {missing}",
                     (time.perf_counter() - start) * 1000)

    # name must match parent dir
    if fm["name"] != skill_path.parent.name:
        return Check("yaml_frontmatter", rel, "fail",
                     f"name '{fm['name']}' != parent dir '{skill_path.parent.name}'",
                     (time.perf_counter() - start) * 1000)

    # version must be semver
    if not SEMVER.match(str(fm["version"])):
        return Check("yaml_frontmatter", rel, "fail",
                     f"version '{fm['version']}' not semver",
                     (time.perf_counter() - start) * 1000)

    return Check("yaml_frontmatter", rel, "pass", "",
                 (time.perf_counter() - start) * 1000)


def check_cross_refs(skill_path: Path, known_skills: set[str]) -> Check:
    """Every @ba-X mention must resolve to an existing skill folder."""
    start = time.perf_counter()
    rel = str(skill_path.relative_to(REPO_ROOT))
    text = _strip_code_fences(skill_path.read_text(encoding="utf-8"))

    refs = set(AGENT_REF.findall(text))
    refs = {r[1:] for r in refs}  # strip leading @
    unknown = sorted(refs - known_skills)
    if unknown:
        return Check("cross_refs", rel, "fail",
                     f"unknown agents: {unknown}",
                     (time.perf_counter() - start) * 1000)
    return Check("cross_refs", rel, "pass",
                 f"{len(refs)} refs ok",
                 (time.perf_counter() - start) * 1000)


def check_path_refs(skill_path: Path) -> Check:
    """Every .agent/{templates,data,scripts}/X reference must exist on disk."""
    start = time.perf_counter()
    rel = str(skill_path.relative_to(REPO_ROOT))
    text = _strip_code_fences(skill_path.read_text(encoding="utf-8"))

    broken: list[str] = []
    for match in PATH_REF_TEMPLATE.finditer(text):
        target = TEMPLATE_ROOT / match.group(1)
        if not target.exists():
            broken.append(f"template:{match.group(1)}")
    for match in PATH_REF_DATA.finditer(text):
        target = DATA_ROOT / match.group(1)
        if not target.exists():
            broken.append(f"data:{match.group(1)}")
    for match in PATH_REF_SCRIPT.finditer(text):
        target = SCRIPT_ROOT / match.group(1)
        if not target.exists():
            broken.append(f"script:{match.group(1)}")

    if broken:
        return Check("path_refs", rel, "fail",
                     f"{len(broken)} broken: {broken[:3]}",
                     (time.perf_counter() - start) * 1000)
    return Check("path_refs", rel, "pass", "",
                 (time.perf_counter() - start) * 1000)


def check_python_compile(script_path: Path) -> Check:
    """py_compile each Python helper."""
    start = time.perf_counter()
    rel = str(script_path.relative_to(REPO_ROOT))
    proc = subprocess.run(
        [sys.executable, "-m", "py_compile", str(script_path)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return Check("python_compile", rel, "fail",
                     proc.stderr.strip().split("\n")[-1][:200],
                     (time.perf_counter() - start) * 1000)
    return Check("python_compile", rel, "pass", "",
                 (time.perf_counter() - start) * 1000)


def check_bash_syntax(script_path: Path) -> Check:
    """bash -n on shell scripts."""
    start = time.perf_counter()
    rel = str(script_path.relative_to(REPO_ROOT))
    if not script_path.exists():
        return Check("bash_syntax", rel, "skip", "not present",
                     (time.perf_counter() - start) * 1000)
    proc = subprocess.run(["bash", "-n", str(script_path)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        return Check("bash_syntax", rel, "fail", proc.stderr.strip()[:200],
                     (time.perf_counter() - start) * 1000)
    return Check("bash_syntax", rel, "pass", "",
                 (time.perf_counter() - start) * 1000)


def run_l1_static() -> LayerVerdict:
    """L1 — deterministic mechanical validation."""
    start = time.perf_counter()
    verdict = LayerVerdict("L1", "Static validation (YAML + cross-refs + paths + compile)")
    skills = find_skill_files()
    known = skill_names()

    for sk in skills:
        verdict.checks.append(check_yaml_frontmatter(sk))
        verdict.checks.append(check_cross_refs(sk, known))
        verdict.checks.append(check_path_refs(sk))

    for script in python_scripts():
        verdict.checks.append(check_python_compile(script))

    verdict.checks.append(check_bash_syntax(SETUP_SH))

    verdict.duration_ms = (time.perf_counter() - start) * 1000
    return verdict


# ---------------------------------------------------------------------------
# L2 — Script helper smoke tests
# ---------------------------------------------------------------------------

@dataclass
class HelperTest:
    """One subprocess smoke test. cmd strings support ${FIXTURE}, ${REPO},
    ${SCRIPT_DIR} substitution. setup() returns additional substitutions."""
    name: str
    cmd: list[str]
    expected_exit: int = 0
    stdout_contains: list[str] = field(default_factory=list)
    stderr_contains: list[str] = field(default_factory=list)
    cwd_temp: bool = False          # Run in an isolated temp dir
    env_unset: list[str] = field(default_factory=list)  # e.g., ["GEMINI_API_KEY"]
    setup: Callable | None = None   # Optional setup; returns None or dict
    timeout_sec: int = 30
    description: str = ""


def _substitute(cmd: list[str], fixture: Path) -> list[str]:
    """Replace placeholders in the command template."""
    repo = str(REPO_ROOT)
    script_dir = str(SCRIPT_ROOT)
    fix = str(fixture)
    return [
        token.replace("${FIXTURE}", fix)
             .replace("${REPO}", repo)
             .replace("${SCRIPT_DIR}", script_dir)
        for token in cmd
    ]


def run_helper_test(test: HelperTest, fixture: Path) -> Check:
    start = time.perf_counter()
    target = test.description or " ".join(test.cmd[:3])

    # Optional setup (e.g., create a sample file in temp dir)
    tmp_dir_ctx = None
    cwd = str(REPO_ROOT)
    if test.cwd_temp:
        tmp_dir_ctx = tempfile.TemporaryDirectory(prefix="ba-e2e-")
        cwd = tmp_dir_ctx.name

    env = os.environ.copy()
    for key in test.env_unset:
        env.pop(key, None)
    if test.cwd_temp:
        # Isolate HOME for helpers that write to ~/.ba-kit/
        env["HOME"] = cwd

    try:
        if test.setup is not None:
            test.setup(Path(cwd))
        cmd = _substitute(test.cmd, fixture)
        proc = subprocess.run(
            cmd,
            capture_output=True, text=True,
            cwd=cwd, env=env, timeout=test.timeout_sec,
        )
    except subprocess.TimeoutExpired:
        if tmp_dir_ctx:
            tmp_dir_ctx.cleanup()
        return Check(test.name, target, "fail",
                     f"timeout after {test.timeout_sec}s",
                     (time.perf_counter() - start) * 1000)
    except Exception as e:
        if tmp_dir_ctx:
            tmp_dir_ctx.cleanup()
        return Check(test.name, target, "fail",
                     f"launch error: {e}",
                     (time.perf_counter() - start) * 1000)

    # Verdict
    details: list[str] = []
    ok = True

    if proc.returncode != test.expected_exit:
        ok = False
        details.append(
            f"exit {proc.returncode} != {test.expected_exit}")
        if proc.stderr:
            details.append(f"stderr: {proc.stderr.strip()[:200]}")

    for needle in test.stdout_contains:
        if needle not in proc.stdout:
            ok = False
            details.append(f"stdout missing '{needle}'")

    for needle in test.stderr_contains:
        if needle not in proc.stderr:
            ok = False
            details.append(f"stderr missing '{needle}'")

    if tmp_dir_ctx:
        tmp_dir_ctx.cleanup()

    if ok:
        return Check(test.name, target, "pass",
                     f"exit {proc.returncode}",
                     (time.perf_counter() - start) * 1000)
    return Check(test.name, target, "fail", "; ".join(details),
                 (time.perf_counter() - start) * 1000)


def _setup_sample_file(cwd: Path) -> None:
    """Create a minimal markdown file for baseline smoke test."""
    (cwd / "sample.md").write_text("# Sample BRD\n\nRequirement: login.\n")
    # Also init git so ba_baseline history doesn't care
    subprocess.run(["git", "init", "-q"], cwd=str(cwd), check=False)


def _setup_git_init(cwd: Path) -> None:
    """Just git init, no extra files."""
    subprocess.run(["git", "init", "-q"], cwd=str(cwd), check=False)


def _build_l2_tests(fixture: Path) -> list[HelperTest]:
    """Conservative test matrix. Covers the 6 new v3.4 helpers + setup.sh
    + 3 legacy helpers. ba_core/batch_remediate/gen_docx are compile-only
    (covered by L1)."""
    py = sys.executable
    scripts = str(SCRIPT_ROOT)
    return [
        # --- Legacy helpers (smoke-only) ---
        HelperTest(
            name="ba_search_stats",
            cmd=[py, f"{scripts}/ba_search.py", "--stats"],
            stdout_contains=["domain"],
            description="ba_search.py --stats",
        ),
        HelperTest(
            name="coverage_checker_on_fixture",
            cmd=[py, f"{scripts}/coverage_checker.py", "${FIXTURE}"],
            stdout_contains=["HEALTHY", "User Stories: 53", "Modules: 12"],
            description="coverage_checker.py on fixture",
        ),

        # --- v3.4 helpers ---
        HelperTest(
            name="ba_as_built_scan",
            cmd=[py, f"{scripts}/ba_as_built.py", "scan",
                 "--project", "${FIXTURE}", "--base", "main"],
            stdout_contains=['"commits":', '"specs":'],
            description="ba_as_built.py scan on fixture",
        ),
        HelperTest(
            name="ba_baseline_empty_list",
            cmd=[py, f"{scripts}/ba_baseline.py", "list"],
            cwd_temp=True,
            stdout_contains=["No baselines yet"],
            description="ba_baseline.py list (empty)",
        ),
        HelperTest(
            name="ba_baseline_add_roundtrip",
            cmd=[py, f"{scripts}/ba_baseline.py", "add", "sample.md",
                 "--version", "v1.0", "--by", "e2e-tester",
                 "--rationale", "e2e smoke test baseline"],
            cwd_temp=True,
            setup=_setup_sample_file,
            stdout_contains=["Baselined sample.md as v1.0"],
            description="ba_baseline.py add (temp dir)",
        ),
        HelperTest(
            name="ba_baseline_reject_thin_rationale",
            cmd=[py, f"{scripts}/ba_baseline.py", "add", "sample.md",
                 "--version", "v1.0", "--by", "x", "--rationale", "ok"],
            cwd_temp=True,
            setup=_setup_sample_file,
            expected_exit=2,
            stderr_contains=["Rationale too thin"],
            description="ba_baseline.py rejects short rationale",
        ),
        HelperTest(
            name="ba_learn_stats_empty",
            cmd=[py, f"{scripts}/ba_learn.py", "stats"],
            cwd_temp=True,
            stdout_contains=["No learnings yet"],
            description="ba_learn.py stats (empty project)",
        ),
        HelperTest(
            name="ba_learn_add_show_roundtrip",
            cmd=[py, f"{scripts}/ba_learn.py", "add",
                 "--type", "pattern", "--key", "E2E_TEST",
                 "--insight", "Smoke test entry for runner verification",
                 "--confidence", "8"],
            cwd_temp=True,
            stdout_contains=["Added pattern/E2E_TEST"],
            description="ba_learn.py add (temp HOME)",
        ),
        HelperTest(
            name="ba_retro_on_repo",
            cmd=[py, f"{scripts}/ba_retro.py", "--window", "30d",
                 "--project", "ba-kit-antigravity"],
            stdout_contains=["Sprint Retro"],
            description="ba_retro.py on current repo",
            timeout_sec=20,
        ),
        HelperTest(
            name="ba_second_opinion_prompt",
            cmd=[py, f"{scripts}/ba_second_opinion.py", "prompt",
                 "--artifact", ".agent/skills/ba-shotgun/SKILL.md"],
            env_unset=["GEMINI_API_KEY", "OPENAI_API_KEY", "OLLAMA_HOST"],
            stdout_contains=["STRICT JSON", "ARTIFACT"],
            description="ba_second_opinion.py prompt mode",
        ),
        HelperTest(
            name="ba_setup_status",
            cmd=[py, f"{scripts}/ba_setup.py", "status"],
            stdout_contains=["BA-Kit Setup Status"],
            description="ba_setup.py status",
        ),
        HelperTest(
            name="ba_setup_reject_bad_url",
            cmd=[py, f"{scripts}/ba_setup.py", "jira",
                 "--url", "not-a-url",
                 "--token", "abcdefghijklmnopqrstuvwxyz123",
                 "--project", "PROJ"],
            expected_exit=2,
            stderr_contains=["must start with http"],
            description="ba_setup.py rejects malformed URL",
        ),
        HelperTest(
            name="ba_setup_reject_short_token",
            cmd=[py, f"{scripts}/ba_setup.py", "jira",
                 "--url", "https://jira.test.com",
                 "--token", "short",
                 "--project", "PROJ"],
            expected_exit=2,
            stderr_contains=["too short"],
            description="ba_setup.py rejects short token",
        ),

        # --- Shell ---
        HelperTest(
            name="setup_sh_list",
            cmd=["bash", f"{scripts}/setup.sh", "--list"],
            stdout_contains=["Detected BA-Kit host candidates"],
            description="setup.sh --list (no side effects)",
        ),
    ]


def run_l2_scripts(fixture: Path) -> LayerVerdict:
    """L2 — run smoke tests against each helper script."""
    start = time.perf_counter()
    verdict = LayerVerdict("L2", "Script helper smoke tests")

    tests = _build_l2_tests(fixture)
    for test in tests:
        check = run_helper_test(test, fixture)
        verdict.checks.append(check)

    verdict.duration_ms = (time.perf_counter() - start) * 1000
    return verdict


# ---------------------------------------------------------------------------
# L3 — Per-skill structure assertions
# ---------------------------------------------------------------------------

L3_PATTERNS = {
    "agency":            re.compile(r"<AGENCY>", re.IGNORECASE),
    "memory":            re.compile(r"<MEMORY>", re.IGNORECASE),
    "input_validation":  re.compile(r"##\s*[^\n]*Input Validation", re.IGNORECASE),
    "system_instructions": re.compile(r"##\s*System Instructions", re.IGNORECASE),
    "reflection":        re.compile(
        r"(Reflection|Review|Self-Critic)[^\n]*System\s*2"
        r"|System\s*2[^\n]*Reflection"
        r"|###\s*\d*\.?\s*Reflection Mode",
        re.IGNORECASE),
    "activation":        re.compile(r"Activation Phrase", re.IGNORECASE),
    "knowledge_ref":     re.compile(r"Knowledge Reference|Knowledge Base|Knowledge Search",
                                    re.IGNORECASE),
    "handoff":           re.compile(r"Handoff|@ba-[a-z-]+", re.IGNORECASE),
}

L3_REQUIRED_MIN = 5  # out of 8 sections — flexibility for legitimate variation


def check_skill_structure(skill_path: Path) -> Check:
    start = time.perf_counter()
    name = skill_path.parent.name
    rel = str(skill_path.relative_to(REPO_ROOT))

    if name in CONNECTOR_EXEMPT:
        return Check("structure", rel, "skip", "connector exempt",
                     (time.perf_counter() - start) * 1000)

    text = skill_path.read_text(encoding="utf-8")
    _, body = parse_frontmatter(text)

    hits = [key for key, pat in L3_PATTERNS.items() if pat.search(body)]
    missing = [key for key in L3_PATTERNS if key not in hits]

    # File sanity
    if len(body.split("\n")) < 50:
        return Check("structure", rel, "fail",
                     f"stub-sized (< 50 body lines); missing: {missing}",
                     (time.perf_counter() - start) * 1000)

    if len(hits) >= len(L3_PATTERNS):
        return Check("structure", rel, "pass",
                     f"all 8 sections present",
                     (time.perf_counter() - start) * 1000)
    if len(hits) >= L3_REQUIRED_MIN:
        return Check("structure", rel, "warn",
                     f"only {len(hits)}/8 sections; missing: {missing}",
                     (time.perf_counter() - start) * 1000)
    return Check("structure", rel, "fail",
                 f"only {len(hits)}/8 sections (min {L3_REQUIRED_MIN}); missing: {missing}",
                 (time.perf_counter() - start) * 1000)


def run_l3_structure() -> LayerVerdict:
    start = time.perf_counter()
    verdict = LayerVerdict("L3", "Per-skill canonical structure + sanity")
    for sk in find_skill_files():
        verdict.checks.append(check_skill_structure(sk))
    verdict.duration_ms = (time.perf_counter() - start) * 1000
    return verdict


# ---------------------------------------------------------------------------
# L4 — Cross-artifact consistency (deep lints on fixture)
# ---------------------------------------------------------------------------

US_ID_CONTENT = re.compile(r"^#\s+(US-[A-Z]+-\d+)\b", re.MULTILINE)
US_ID_INLINE = re.compile(r"\bUS-[A-Z]+-\d+\b")


@dataclass
class FixtureInventory:
    """Single-pass inventory of fixture artifacts + cross-references."""
    fixture: Path
    us_files: dict[str, Path] = field(default_factory=dict)      # US-ID → file path
    us_filename_slugs: dict[str, Path] = field(default_factory=dict)  # filename → path
    brd_files: list[Path] = field(default_factory=list)
    api_spec_files: list[Path] = field(default_factory=list)
    db_schema_files: list[Path] = field(default_factory=list)
    test_case_files: list[Path] = field(default_factory=list)
    rtm_file: Path | None = None

    brd_us_refs: dict[Path, set[str]] = field(default_factory=dict)
    api_spec_us_refs: dict[Path, set[str]] = field(default_factory=dict)
    test_case_us_refs: dict[Path, set[str]] = field(default_factory=dict)
    rtm_us_refs: set[str] = field(default_factory=set)

    duplicate_us_ids: dict[str, list[Path]] = field(default_factory=dict)

    @property
    def all_us_ids(self) -> set[str]:
        return set(self.us_files.keys())

    @property
    def has_content(self) -> bool:
        return bool(self.us_files or self.brd_files or self.api_spec_files)


def _extract_us_ids_from_text(text: str) -> set[str]:
    return set(US_ID_INLINE.findall(text))


def _extract_us_id_header(md_path: Path) -> str | None:
    """First '# US-X-Y: Title' line or None."""
    try:
        for line in md_path.read_text(encoding="utf-8").splitlines()[:5]:
            match = US_ID_CONTENT.match(line)
            if match:
                return match.group(1)
    except Exception:
        return None
    return None


def build_fixture_inventory(fixture: Path) -> FixtureInventory:
    """Single-pass scan of fixture — builds the inventory used by all lints."""
    inv = FixtureInventory(fixture=fixture)
    if not fixture.exists():
        return inv

    # Walk once, classify by name pattern
    for md in sorted(fixture.rglob("*.md")):
        name = md.name
        name_lower = name.lower()

        # User stories
        if name_lower.startswith("us-"):
            stem = md.stem
            us_id = _extract_us_id_header(md)
            if us_id is None:
                # Try deriving from filename (us-atten-01-slug.md → US-ATTEN-01)
                m = re.match(r"us-([a-z]+)-(\d+)", stem)
                if m:
                    us_id = f"US-{m.group(1).upper()}-{m.group(2).zfill(2)}"
            if us_id:
                if us_id in inv.us_files:
                    # Duplicate — record both paths
                    inv.duplicate_us_ids.setdefault(us_id, []).append(inv.us_files[us_id])
                    inv.duplicate_us_ids[us_id].append(md)
                else:
                    inv.us_files[us_id] = md
            inv.us_filename_slugs[stem] = md
            continue

        # BRDs (overview/BRD-*.md)
        if "BRD" in name or "overview" in str(md.parent):
            if name.lower().startswith("brd") or name.startswith("BRD"):
                inv.brd_files.append(md)
                text = md.read_text(encoding="utf-8", errors="ignore")
                inv.brd_us_refs[md] = _extract_us_ids_from_text(text)
                continue

        # API specs
        if name == "api-spec.md":
            inv.api_spec_files.append(md)
            text = md.read_text(encoding="utf-8", errors="ignore")
            inv.api_spec_us_refs[md] = _extract_us_ids_from_text(text)
            continue

        # DB schemas
        if name == "db-schema.md":
            inv.db_schema_files.append(md)
            continue

        # Test cases (one file per module)
        if name == "test-cases.md":
            inv.test_case_files.append(md)
            text = md.read_text(encoding="utf-8", errors="ignore")
            inv.test_case_us_refs[md] = _extract_us_ids_from_text(text)
            continue

        # RTM (single file at project root)
        if name == "RTM.md" and md.parent == fixture:
            inv.rtm_file = md
            text = md.read_text(encoding="utf-8", errors="ignore")
            inv.rtm_us_refs = _extract_us_ids_from_text(text)
            continue

    return inv


def _rel(p: Path, fixture: Path) -> str:
    try:
        return str(p.relative_to(fixture))
    except ValueError:
        return str(p)


def lint_us_id_uniqueness(inv: FixtureInventory) -> Check:
    """No two US files should declare the same US ID."""
    if not inv.us_files:
        return Check("us_id_uniqueness", str(inv.fixture), "skip",
                     "no US files")
    if inv.duplicate_us_ids:
        dup_summary = [
            f"{us_id}: {len(paths)} files"
            for us_id, paths in sorted(inv.duplicate_us_ids.items())
        ]
        return Check("us_id_uniqueness", str(inv.fixture), "fail",
                     f"{len(inv.duplicate_us_ids)} duplicates — {dup_summary[:3]}")
    return Check("us_id_uniqueness", str(inv.fixture), "pass",
                 f"{len(inv.us_files)} unique US IDs")


def lint_us_filename_alignment(inv: FixtureInventory) -> Check:
    """us-xxxx-NN-slug.md should have '# US-XXXX-NN: Title' as first content line."""
    mismatches: list[str] = []
    for us_id, path in inv.us_files.items():
        stem = path.stem  # e.g. us-atten-01-hub-cham-cong
        m = re.match(r"us-([a-z]+)-(\d+)", stem)
        if not m:
            continue
        expected_id = f"US-{m.group(1).upper()}-{m.group(2).zfill(2)}"
        if us_id != expected_id:
            mismatches.append(f"{path.name}→{us_id}!={expected_id}")
    if not inv.us_files:
        return Check("us_filename_alignment", str(inv.fixture), "skip",
                     "no US files")
    if mismatches:
        return Check("us_filename_alignment", str(inv.fixture), "warn",
                     f"{len(mismatches)} mismatches: {mismatches[:3]}")
    return Check("us_filename_alignment", str(inv.fixture), "pass",
                 f"{len(inv.us_files)} files aligned")


def lint_brd_us_refs(inv: FixtureInventory) -> list[Check]:
    """Every US-ID mentioned in a BRD must exist as a US file."""
    checks: list[Check] = []
    if not inv.brd_files:
        checks.append(Check("brd_us_refs", str(inv.fixture), "skip",
                            "no BRD files"))
        return checks
    all_us = inv.all_us_ids
    for brd in inv.brd_files:
        refs = inv.brd_us_refs.get(brd, set())
        unknown = sorted(refs - all_us)
        rel = _rel(brd, inv.fixture)
        if unknown:
            checks.append(Check("brd_us_refs", rel, "fail",
                                f"unknown US: {unknown[:5]}"))
        else:
            checks.append(Check("brd_us_refs", rel, "pass",
                                f"{len(refs)} refs ok"))
    return checks


def lint_api_spec_us_refs(inv: FixtureInventory) -> list[Check]:
    """Every US mentioned in api-spec.md's Ref column must exist."""
    checks: list[Check] = []
    if not inv.api_spec_files:
        checks.append(Check("api_spec_us_refs", str(inv.fixture), "skip",
                            "no api-spec files"))
        return checks
    all_us = inv.all_us_ids
    for spec in inv.api_spec_files:
        refs = inv.api_spec_us_refs.get(spec, set())
        unknown = sorted(refs - all_us)
        rel = _rel(spec, inv.fixture)
        if not refs:
            checks.append(Check("api_spec_us_refs", rel, "warn",
                                "no US refs in api-spec"))
        elif unknown:
            checks.append(Check("api_spec_us_refs", rel, "fail",
                                f"unknown US: {unknown[:5]}"))
        else:
            checks.append(Check("api_spec_us_refs", rel, "pass",
                                f"{len(refs)} refs ok"))
    return checks


def lint_test_case_us_refs(inv: FixtureInventory) -> list[Check]:
    """Every US mentioned in test-cases.md must exist. Warn if a module's
    US files have no test-case coverage."""
    checks: list[Check] = []
    if not inv.test_case_files:
        checks.append(Check("test_case_us_refs", str(inv.fixture), "skip",
                            "no test-case files"))
        return checks
    all_us = inv.all_us_ids

    # Per-file: every ref must resolve
    for tc in inv.test_case_files:
        refs = inv.test_case_us_refs.get(tc, set())
        unknown = sorted(refs - all_us)
        rel = _rel(tc, inv.fixture)
        if not refs:
            checks.append(Check("test_case_us_refs", rel, "warn",
                                "no US refs"))
        elif unknown:
            checks.append(Check("test_case_us_refs", rel, "fail",
                                f"unknown US: {unknown[:5]}"))
        else:
            checks.append(Check("test_case_us_refs", rel, "pass",
                                f"{len(refs)} refs ok"))

    # Aggregate: which US have ANY test coverage?
    all_tested = set()
    for refs in inv.test_case_us_refs.values():
        all_tested.update(refs)
    untested = sorted(inv.all_us_ids - all_tested)
    if untested:
        checks.append(Check("us_test_coverage", str(inv.fixture), "warn",
                            f"{len(untested)}/{len(inv.all_us_ids)} US "
                            f"untested: {untested[:5]}"))
    else:
        checks.append(Check("us_test_coverage", str(inv.fixture), "pass",
                            f"all {len(inv.all_us_ids)} US covered"))
    return checks


def lint_rtm_consistency(inv: FixtureInventory) -> list[Check]:
    """RTM.md should reference every US file, and vice versa."""
    checks: list[Check] = []
    if inv.rtm_file is None:
        checks.append(Check("rtm_consistency", str(inv.fixture), "skip",
                            "no RTM.md"))
        return checks
    all_us = inv.all_us_ids

    # Every US ref in RTM should resolve
    unknown_in_rtm = sorted(inv.rtm_us_refs - all_us)
    if unknown_in_rtm:
        checks.append(Check("rtm_refs_valid", "RTM.md", "fail",
                            f"unknown US: {unknown_in_rtm[:5]}"))
    else:
        checks.append(Check("rtm_refs_valid", "RTM.md", "pass",
                            f"{len(inv.rtm_us_refs)} RTM refs ok"))

    # Every US file should be mentioned in RTM
    missing_from_rtm = sorted(all_us - inv.rtm_us_refs)
    if missing_from_rtm:
        checks.append(Check("rtm_us_coverage", "RTM.md", "warn",
                            f"{len(missing_from_rtm)}/{len(all_us)} US not in RTM: "
                            f"{missing_from_rtm[:5]}"))
    else:
        checks.append(Check("rtm_us_coverage", "RTM.md", "pass",
                            "all US in RTM"))
    return checks


def run_l4_consistency(fixture: Path) -> LayerVerdict:
    """L4 — cross-artifact consistency using coverage_checker + deep lints."""
    start = time.perf_counter()
    verdict = LayerVerdict("L4", "Cross-artifact consistency on fixture")

    if not fixture.exists():
        verdict.checks.append(Check(
            "fixture_exists", str(fixture), "skip",
            "fixture not present",
        ))
        verdict.duration_ms = (time.perf_counter() - start) * 1000
        return verdict

    # Shallow: coverage_checker baseline
    proc = subprocess.run(
        [sys.executable, str(SCRIPT_ROOT / "coverage_checker.py"),
         str(fixture), "--json"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        verdict.checks.append(Check(
            "coverage_checker_run", str(fixture), "fail",
            f"exit {proc.returncode}: {proc.stderr[:200]}",
        ))
    else:
        try:
            data = json.loads(proc.stdout)
            health = data["scores"]["overall"].get("health_score", 0)
            status = data["scores"]["overall"].get("health_status", "?")
            severity: Severity = "pass" if health >= 80 else (
                "warn" if health >= 60 else "fail")
            verdict.checks.append(Check(
                "fixture_health_score", str(fixture), severity,
                f"{health}% {status}",
            ))
        except json.JSONDecodeError as e:
            verdict.checks.append(Check(
                "coverage_checker_parse", str(fixture), "fail",
                f"JSON parse error: {e}",
            ))

    # Deep lints: build inventory once, run 6 lint families
    inv = build_fixture_inventory(fixture)
    if not inv.has_content:
        verdict.checks.append(Check(
            "fixture_empty", str(fixture), "skip",
            "no US/BRD/API/test-case files found",
        ))
    else:
        verdict.checks.append(lint_us_id_uniqueness(inv))
        verdict.checks.append(lint_us_filename_alignment(inv))
        verdict.checks.extend(lint_brd_us_refs(inv))
        verdict.checks.extend(lint_api_spec_us_refs(inv))
        verdict.checks.extend(lint_test_case_us_refs(inv))
        verdict.checks.extend(lint_rtm_consistency(inv))

    verdict.duration_ms = (time.perf_counter() - start) * 1000
    return verdict


# ---------------------------------------------------------------------------
# L5 — Workflow chain dry runs
# ---------------------------------------------------------------------------

SCENARIO_HEADER = re.compile(r"^##\s*.*SCENARIO\s*\d+:", re.IGNORECASE | re.MULTILINE)
SPINE_PHASES = ["Discover", "Elicit", "Define", "Validate",
                "Prioritize", "Publish", "Reflect"]


def parse_cookbook_scenarios(text: str) -> list[tuple[str, str]]:
    """Split cookbook into (title, body) pairs."""
    lines = text.split("\n")
    scenarios: list[tuple[str, str]] = []
    current_title: str | None = None
    current_body: list[str] = []
    for line in lines:
        if SCENARIO_HEADER.match(line):
            if current_title is not None:
                scenarios.append((current_title, "\n".join(current_body)))
            current_title = line.strip("# ").strip()
            current_body = []
        elif current_title is not None:
            current_body.append(line)
    if current_title is not None:
        scenarios.append((current_title, "\n".join(current_body)))
    return scenarios


def check_cookbook_chains(known_skills: set[str]) -> list[Check]:
    """Every @ba-X referenced in a scenario chain must exist."""
    if not COOKBOOK.exists():
        return [Check("cookbook_exists", str(COOKBOOK), "fail", "not found")]

    text = COOKBOOK.read_text(encoding="utf-8")
    scenarios = parse_cookbook_scenarios(text)
    checks: list[Check] = []

    if not scenarios:
        checks.append(Check("cookbook_parse", "docs/workflow-cookbook.md",
                            "fail", "no SCENARIO headers matched"))
        return checks

    for title, body in scenarios:
        refs = {r[1:] for r in AGENT_REF.findall(body)}
        unknown = sorted(refs - known_skills)
        if unknown:
            checks.append(Check("scenario_refs", f"cookbook::{title[:60]}",
                                "fail", f"unknown: {unknown}"))
        else:
            checks.append(Check("scenario_refs", f"cookbook::{title[:60]}",
                                "pass", f"{len(refs)} agents"))

    checks.append(Check("scenario_count",
                        "docs/workflow-cookbook.md",
                        "pass", f"{len(scenarios)} scenarios parsed"))
    return checks


def check_master_routing(known_skills: set[str]) -> list[Check]:
    """ba-master Decision Matrix must route to every ba-* skill."""
    if not MASTER_SKILL.exists():
        return [Check("master_exists", str(MASTER_SKILL), "fail", "not found")]

    text = MASTER_SKILL.read_text(encoding="utf-8")
    routed = {r[1:] for r in AGENT_REF.findall(text)}
    # Skills worth routing (exclude ba-master itself + connectors)
    routable = {s for s in known_skills
                if s != "ba-master" and s not in CONNECTOR_EXEMPT}
    missing_routes = sorted(routable - routed)
    checks: list[Check] = []
    if missing_routes:
        checks.append(Check("master_routing", "ba-master/SKILL.md",
                            "fail",
                            f"{len(missing_routes)} unrouted: {missing_routes[:5]}"))
    else:
        checks.append(Check("master_routing", "ba-master/SKILL.md",
                            "pass",
                            f"{len(routable)} skills routed"))
    return checks


def check_sprint_spine_phases(known_skills: set[str]) -> list[Check]:
    """Sprint spine document must mention all 7 phases and map agents to them."""
    if not SPRINT_SPINE.exists():
        return [Check("sprint_spine_exists", str(SPRINT_SPINE), "fail",
                      "not found")]

    text = SPRINT_SPINE.read_text(encoding="utf-8")
    checks: list[Check] = []
    missing_phases = [p for p in SPINE_PHASES if p not in text]
    if missing_phases:
        checks.append(Check("phases_mentioned", "docs/sprint-spine.md",
                            "fail", f"missing: {missing_phases}"))
    else:
        checks.append(Check("phases_mentioned", "docs/sprint-spine.md",
                            "pass", "all 7 phases present"))

    # Agent refs in sprint-spine should all resolve — strip code spans first
    # so "Future work: `ba-autofoo`" isn't flagged as a broken agent ref
    stripped = _strip_code_fences(text)
    refs = {r[1:] for r in AGENT_REF.findall(stripped)}
    unknown = sorted(refs - known_skills)
    if unknown:
        checks.append(Check("spine_agent_refs", "docs/sprint-spine.md",
                            "fail", f"unknown: {unknown}"))
    else:
        checks.append(Check("spine_agent_refs", "docs/sprint-spine.md",
                            "pass", f"{len(refs)} agents"))
    return checks


def run_l5_chains() -> LayerVerdict:
    start = time.perf_counter()
    verdict = LayerVerdict("L5", "Workflow chains + routing + sprint spine")
    known = skill_names()

    verdict.checks.extend(check_cookbook_chains(known))
    verdict.checks.extend(check_master_routing(known))
    verdict.checks.extend(check_sprint_spine_phases(known))

    verdict.duration_ms = (time.perf_counter() - start) * 1000
    return verdict


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

LAYER_RUNNERS = {
    "L1": lambda fixture: run_l1_static(),
    "L2": lambda fixture: run_l2_scripts(fixture),
    "L3": lambda fixture: run_l3_structure(),
    "L4": lambda fixture: run_l4_consistency(fixture),
    "L5": lambda fixture: run_l5_chains(),
}


def _git_info() -> tuple[str, str]:
    """Return (branch, short_sha) — empty strings if git unavailable."""
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=REPO_ROOT,
        ).stdout.strip()
        sha = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=REPO_ROOT,
        ).stdout.strip()
        return branch, sha
    except Exception:
        return "", ""


def run_all(layers: list[str], fixture: Path, verbose: bool) -> AggregateVerdict:
    start = time.perf_counter()
    verdicts: list[LayerVerdict] = []
    for layer in layers:
        runner = LAYER_RUNNERS.get(layer)
        if runner is None:
            v = LayerVerdict(layer, "unknown layer")
            v.checks.append(Check("layer_unknown", layer, "fail",
                                  f"no runner registered for {layer}"))
            verdicts.append(v)
            continue
        try:
            if verbose:
                print(f"Running {layer}...", file=sys.stderr)
            v = runner(fixture)
        except Exception as e:
            v = LayerVerdict(layer, f"crashed: {e}")
            v.checks.append(Check("layer_crash", layer, "fail", str(e)[:300]))
        verdicts.append(v)
        if verbose:
            print(f"  {v.passed} pass / {v.warned} warn / {v.failed} fail / "
                  f"{v.skipped} skip ({v.duration_ms:.0f}ms)", file=sys.stderr)

    branch, sha = _git_info()
    return AggregateVerdict(
        layers=verdicts,
        fixture=str(fixture),
        started_at=datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        duration_ms=(time.perf_counter() - start) * 1000,
        repo_branch=branch,
        repo_commit=sha,
    )


# ---------------------------------------------------------------------------
# JSON reporter (stable schema for CI consumption)
# ---------------------------------------------------------------------------

JSON_SCHEMA_VERSION = "1.0.0"


def emit_json(agg: AggregateVerdict) -> str:
    """Structured JSON for CI integration. Stable schema v1.0.0."""
    payload = {
        "$schema_version": JSON_SCHEMA_VERSION,
        "fixture": agg.fixture,
        "repo_branch": agg.repo_branch,
        "repo_commit": agg.repo_commit,
        "started_at": agg.started_at,
        "duration_ms": round(agg.duration_ms, 1),
        "exit_code": agg.exit_code,
        "verdict": agg.verdict,
        "totals": {
            "passed": sum(l.passed for l in agg.layers),
            "warned": sum(l.warned for l in agg.layers),
            "failed": sum(l.failed for l in agg.layers),
            "skipped": sum(l.skipped for l in agg.layers),
            "total": sum(l.total for l in agg.layers),
        },
        "layers": [
            {
                "layer": l.layer,
                "description": l.description,
                "duration_ms": round(l.duration_ms, 1),
                "totals": {
                    "passed": l.passed,
                    "warned": l.warned,
                    "failed": l.failed,
                    "skipped": l.skipped,
                    "total": l.total,
                },
                "checks": [
                    {
                        "name": c.name,
                        "target": c.target,
                        "severity": c.severity,
                        "message": c.message,
                        "duration_ms": round(c.duration_ms, 2),
                    }
                    for c in l.checks
                ],
            }
            for l in agg.layers
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Markdown reporter
# ---------------------------------------------------------------------------

VERDICT_EMOJI = {"PASS": "✅", "PASS-WITH-WARNINGS": "⚠️", "FAIL": "🛑"}
SEVERITY_EMOJI = {"pass": "✓", "warn": "⚠", "fail": "✗", "skip": "○"}


def emit_markdown(agg: AggregateVerdict) -> str:
    lines: list[str] = []
    lines.append(f"# BA-Kit E2E Test Report — {agg.started_at[:10]}")
    lines.append("")
    lines.append(f"**Branch:** {agg.repo_branch or '?'}")
    lines.append(f"**Commit:** {agg.repo_commit or '?'}")
    lines.append(f"**Fixture:** {agg.fixture}")
    lines.append(f"**Started:** {agg.started_at}")
    lines.append(f"**Duration:** {agg.duration_ms / 1000:.1f}s")
    emoji = VERDICT_EMOJI.get(agg.verdict, "?")
    lines.append(f"**Verdict:** {emoji} {agg.verdict}")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("| Layer | Description | Pass | Warn | Fail | Skip | Duration |")
    lines.append("|-------|-------------|------|------|------|------|----------|")
    tot_pass = tot_warn = tot_fail = tot_skip = 0
    for l in agg.layers:
        lines.append(f"| {l.layer} | {l.description} | "
                     f"{l.passed} | {l.warned} | {l.failed} | {l.skipped} | "
                     f"{l.duration_ms:.0f}ms |")
        tot_pass += l.passed
        tot_warn += l.warned
        tot_fail += l.failed
        tot_skip += l.skipped
    lines.append(f"| **Total** | — | **{tot_pass}** | **{tot_warn}** | "
                 f"**{tot_fail}** | **{tot_skip}** | "
                 f"**{agg.duration_ms:.0f}ms** |")
    lines.append("")

    for l in agg.layers:
        lines.append(f"## {l.layer} — {l.description}")
        lines.append("")
        if not l.checks:
            lines.append("*(no checks)*")
            lines.append("")
            continue
        # Group failures first
        fails = [c for c in l.checks if c.severity == "fail"]
        warns = [c for c in l.checks if c.severity == "warn"]
        skips = [c for c in l.checks if c.severity == "skip"]
        if fails:
            lines.append("### 🛑 Failures")
            lines.append("")
            for c in fails:
                lines.append(f"- **{c.name}** `{c.target}` — {c.message}")
            lines.append("")
        if warns:
            lines.append("### ⚠️ Warnings")
            lines.append("")
            for c in warns:
                lines.append(f"- **{c.name}** `{c.target}` — {c.message}")
            lines.append("")
        if skips:
            lines.append(f"### ○ Skipped ({len(skips)})")
            lines.append("")
            for c in skips:
                lines.append(f"- **{c.name}** `{c.target}` — {c.message}")
            lines.append("")
        passed = [c for c in l.checks if c.severity == "pass"]
        lines.append(f"### ✓ Passed: {len(passed)}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("Generated by `.agent/scripts/ba_e2e_test.py`")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="BA-Kit end-to-end test runner")
    p.add_argument("--layers", default="L1,L2,L3,L4,L5",
                   help="Comma-separated layers to run (default: all)")
    p.add_argument("--fixture", default="outputs/mini-app-cham-cong",
                   help="Fixture project path (default: outputs/mini-app-cham-cong)")
    p.add_argument("--report", default=None,
                   help="Markdown report output path (default: print to stdout)")
    p.add_argument("--json", dest="json_out", default=None,
                   help="JSON report output path (for CI integration)")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args(argv)

    layers = [l.strip().upper() for l in args.layers.split(",") if l.strip()]
    fixture = Path(args.fixture)

    agg = run_all(layers, fixture, args.verbose)
    report = emit_markdown(agg)
    json_payload = emit_json(agg)

    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"Report: {out}", file=sys.stderr)
    elif not args.json_out:
        print(report)

    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json_payload, encoding="utf-8")
        print(f"JSON: {out}", file=sys.stderr)

    print(f"Verdict: {agg.verdict} (exit {agg.exit_code}) — "
          f"{agg.duration_ms / 1000:.1f}s", file=sys.stderr)
    return agg.exit_code


if __name__ == "__main__":
    sys.exit(main())
