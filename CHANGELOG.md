# Changelog

All notable changes to BA-Kit Antigravity.

## [1.5.0] - 2026-04-14 — E2E Quality Gate + Mini-App Chấm Công Showcase (Marketing v3.5.0)

### Added
- **Phase 08 — CI-integrated E2E quality gate**:
  - `.agent/scripts/ba_e2e_test.py` (1,389 LOC) — 5-layer orchestrator runner (L1 script smoke → L2 helper smoke → L3 skill frontmatter/sections → L4 deep BRD↔US↔API↔test consistency → L5 fixture coverage), `--report` markdown output, `--json` stable schema v1.0.0 (ensure_ascii=False for Vietnamese round-trip), `--fixture` selector
  - `.github/workflows/e2e-skills.yml` — GitHub Actions quality gate triggered on PR + push to `main`/`feat/**` touching `.agent/`, `docs/`, `outputs/`, or the workflow itself. Writes markdown to `GITHUB_STEP_SUMMARY`, uploads `reports/` artifact (14-day retention), posts sticky PR comment via `marocchino/sticky-pull-request-comment@v2`. Fails only on `FAIL`/`CRASH` verdict (warnings don't block). Python 3.11, stdlib only, 10-min timeout
  - README badge: GitHub Actions status linked to the `e2e-skills` workflow
  - L4 deep lints — single-pass `FixtureInventory` + 6 lint families (duplicate US IDs, BRD→US cross-refs, API-spec US refs, test-case US refs, RTM US refs, orphaned test cases). 34 checks on `mini-app-cham-cong` fixture
  - L2 helper smoke — 14 test cases covering `ba_as_built`, `ba_retro`, `ba_learn`, `ba_baseline`, `ba_second_opinion`, `ba_setup` stdlib interfaces
- **Mini-App Chấm Công — comprehensive BA dogfooding showcase** (`outputs/mini-app-cham-cong/`):
  - 4 BRDs (Nhân viên, Quản lý, HR-Admin, IT/System-Admin) + Demo Plan Sprint-8 + modules overview + Confluence manifest
  - 12 modules (M01-M12) with README + api-spec + db-schema + test-cases + US files each
  - 47 US files across M01-M11 (chấm công, OT, nghỉ phép, công tác, phân ca, chính sách, mobile, báo cáo) rewritten R3 with concrete Gherkin scenarios sourced from Edge Cases tables
  - 6 US files for M12 (quản trị hệ thống — chi nhánh, audit log, offboarding, chốt công, onboarding, data retention)
  - EAMS v2.1 (Employee Attendance Management Specification) with §15.3/§17.5/§17.6 expanded
  - RTM (Requirements Traceability Matrix) full cross-ref
  - AUDIT-REPORT R3 + INDEX + 111/111 Confluence sync complete (0 rendering errors)
- **`ba-wiki` canonical sections** — added `## Input Validation` + `## System Instructions` to the operation-based template so L3 frontmatter lint passes (6/8 → 8/8)

### Changed
- `coverage_checker.py` — recognizes lowercase `us-*` filenames + `test-cases.md` (case-insensitive US ID regex, dual filename patterns)
- README badges point to `branch=main` (was `feat/mini-app-cham-cong-docs`)
- Logo cache-bust v3.4.0 → v3.5.0 in both READMEs

### Fixed
- **Confluence DC rendering blockers**: added `json`/`gherkin` language mappings + `mermaid-macro` support to push scripts; fixed broken link in `overview/README`
- **R3 Gherkin remediation**: 47 US files (M01-M11) rewritten from abstract "Given a user, When they submit, Then success" → concrete scenarios with table-driven Edge Cases
- **M12 R3 remediation**: 6 US Gherkin rewrite + EAMS v2.1 §15.3/§17.5/§17.6 + API spec fixes (M03/M04/M09/M11) + BRD cross-ref fixes + Audit R3 + RTM update

### Migration notes
- No breaking changes. Existing v3.4.0 installs continue working
- To enable the new E2E quality gate on forks: copy `.github/workflows/e2e-skills.yml` + ensure `.agent/scripts/ba_e2e_test.py` is present
- Mini-app Chấm Công docs are a dogfooding showcase — reference material, not executable templates

## [1.4.0] - 2026-04-13 — Gstack Distillation (Marketing v3.4.0)

### Added
- **10 new agents** distilled from `garrytan/gstack` analysis:
  - `@ba-as-built` — spec drift detector (reads git diff, finds where code diverged from BRD/SRS/RTM)
  - `@ba-autoreview` — strict-sequential meta: consistency → quality-gate → traceability → auditor, optional `--dual-voice`
  - `@ba-retro` — time-windowed sprint retro (churn, gate rejection trends, cycle time, per-author leaderboard)
  - `@ba-learn` — per-project JSONL emergent memory (5 types, PII filter, auto-capture API)
  - `@ba-checkpoint` — session save/resume for long-running BA work
  - `@ba-challenger` — 5-vector adversarial red team (unstated / incentive / adversarial / scale-break / sunset)
  - `@ba-second-opinion` — cross-model independent review (Gemini / OpenAI / Ollama / manual, zero-dep `urllib`)
  - `@ba-baseline` — sha256-locked CCB baselines with append-only history + supersede semantics
  - `@ba-guard` — pre-flight change-control checker (off / warn / strict + optional git hook)
  - `@ba-shotgun` — N-variant generator for stories / AC / priority / emails (preference capture)
- **5 Python helpers** (zero external deps, stdlib only): `ba_as_built.py`, `ba_retro.py`, `ba_learn.py`, `ba_baseline.py`, `ba_second_opinion.py`
- **`setup.sh`** one-liner install with auto-host detection (antigravity / claude-code / cowork)
- **`docs/sprint-spine.md`** — unified 7-phase loop (Discover→Elicit→Define→Validate→Prioritize→Publish→Reflect)
- **`AGENTS.md` §7** — second-opinion provider auto-detection table (priority order: GEMINI > OPENAI > OLLAMA > manual)
- **`AGENTS.md` §8** — strict CCB workflow (3-step opt-in for regulated teams)

### Changed
- Agent count **33 → 43** across README, README.vi, agent-cheat-sheet, junior-start, antigravity-protocol, ai-foundation, usage-guide, _shared/system-prompt, ba-master, architecture-decisions
- README badges bumped: `Version-3.1.0 → 3.2.0`, `Agents-33 → 43`, logo cache-bust v3.1.0 → v3.2.0
- `ba-master/SKILL.md` Decision Matrix: +20 routing entries for 10 new skills, +Sprint Spine Agents registry section
- `ba-shotgun/SKILL.md` — added rationale block explaining N=3 default + "vary constraint axis instead of inflating count"

### Fixed
- **YAML frontmatter**: 23 SKILL.md files had unquoted `description: [Agentic] foo` causing strict parser failures. All quoted (`"[...]"`) — 45/45 now parse cleanly.
- `docs/sprint-spine.md` self-correction: "v3.1 has 33 agents" → "v3.1 had 33, v3.2 has 43"
- `docs/architecture-decisions.md` Production Readiness Score: agent count breakdown updated
- **BA-fit reframing** (4 v3.4 skills bumped 1.0.0 → 1.1.0): catch where gstack-imported mechanisms leaked engineer vocabulary into BA-facing skills.
  - `ba-as-built` — primary mode now reads delivered evidence pack (UAT reports, release notes, demo notes); git mode demoted to opt-in advanced for hybrid BA+dev teams
  - `ba-retro` — primary input now BA-Kit JSONL metric streams + file mtime; git log demoted to tertiary opt-in; output reframed from "commits/authors/sessions" to "gate pass rate / churn / stakeholder responsiveness"
  - `ba-baseline` — agent now uses natural-language conversation ("which doc / version / signer / rationale"); sha256 hidden entirely from BA output; integrity check runs silently
  - `ba-guard` — 3 modes (off / warn / strict) described in BA language; alerts say "BRD-HR was edited 2 days after sign-off — was this re-approved?" instead of "DRIFT detected: hash mismatch"; git pre-commit hook stays as opt-in advanced
  - Python helpers UNCHANGED (mechanism layer is correct for both modes; only SKILL.md presentation reframed)
- **BA-fit Phase 2** — spot-check 5 v3.1 skills + 2 wrappers + 2 connectors:
  - `ba-jira` + `ba-confluence` Prerequisites sections reframed: "one-time IT setup, not your daily job" with clear separation between IT setup and BA daily workflow
  - `jira-connector` + `confluence-connector` infrastructure header added: "loaded by ba-jira / ba-confluence, not for direct BA invocation"
  - 3 spot-checked v3.1 skills clean (ba-test-gen, ba-data, ba-process)
- **BA-fit Phase 3** — spot-check 5 more v3.1 skills + ship `@ba-setup`:
  - `ba-metrics` "Fix the build" engineer slang → "Fix the requirements process" (BA language)
  - 4 v3.1 skills clean (ba-solution, ba-innovation, ba-systems, ba-strategy)
  - **NEW skill `@ba-setup`** (44 agents total): one-time setup wizard with BA-friendly natural-language flow for Jira / Confluence / second-opinion provider configuration
  - **NEW helper `ba_setup.py`** (zero-dep stdlib): credential validation, atomic .env write (chmod 0600), placeholder rejection, masked token display, connectivity test via urllib
  - Closes the last identified BA-fit gap — BA never types `.env` files or CLI flags
- Cumulative: **15/46 skills spot-checked (33%)**, 0 hard issues, 4 minor surface edits applied. Confidence HIGH that remaining 31 are BA-appropriate.

## [1.3.1] - 2026-04-11

### Fixed
- Template paths corrected `templates/` → `.agent/templates/` across 9 SKILL.md files (21 references) and 7 doc files
- Stale agent count 32 → 26 corrected in README.md (6), README.vi.md (6), agent-cheat-sheet.md (1)
- `README.vi.md` line 149: "32 chuyên gia" → "26 chuyên gia"

## [1.3.0] - 2026-04-11

### Changed
- Knowledge entry count corrected 786 → 831 across 12 references in 8 files
- Template count corrected 13 → 14 across 4 files (prd-template.md was undocumented)
- `.claude-output/CLAUDE.md` fully rewritten: 19 → 26 agents, added Integration/Quality/Knowledge sections
- `docs/antigravity-protocol.md` updated to v3.0.0, added Quality & Knowledge agent sections
- `README.vi.md` repo structure fixed: correct template path, added Knowledge Search section
- Scenario count standardized to 23 across agent-cheat-sheet, junior-start, ai-foundation
- Prompt count corrected 28 → 33 in quick-start.md
- `ebooks/README.md` version footer updated v2.9.3 → v3.0.0

### Fixed
- Removed 4 phantom `AGENT.MD` references (file does not exist) in quick-start, contributing
- `docs/ai-foundation-for-ba.md` English half said "21 agents" while Vietnamese said "26" — unified to 26
- `docs/junior-start.md` typo `k#` → `#`, broken path `WORKFLOW-COOKBOOK.md` → `docs/workflow-cookbook.md`
- Logo cache-bust version updated v2.7.0 → v3.0.0 in both READMEs
- `.claude-output/MIGRATION-GUIDE.md` expected skill count 25+ → 26+
- Ebook count corrected 6 → 7 in ai-foundation-for-ba.md

## [1.2.0] - 2026-04-11

### Added
- `docs/agent-cheat-sheet.md` — 26-agent quick reference with workflow chains (was empty)
- `docs/prompt-library.md` — 33 copy-paste prompts organized by BA phase (was empty)
- `@ba-wiki` added to README, ba-master registry, and agent-cheat-sheet

### Changed
- `ba-writing/SKILL.md` — standardized AC format (Gherkin + Structured Bullets both accepted)
- Agent count updated 25 → 26 across all docs (README, README.vi, ba-master, .agent/README)
- Knowledge entry count corrected 809 → 786 across 6 files

### Fixed
- `coverage_checker.py` — AC counting regex now matches both `#### **ACn.` and `#### **3.n.` formats
- `coverage_checker.py` — happy path detection expanded for Vietnamese BA output keywords
- 9 ambiguous terms replaced with measurable metrics across 7 US output files
- `README.md` — broken tree rendering and duplicate brd-template entry
- Health Score: 78% AT RISK → 97% HEALTHY (post-fix)

## [1.1.0] - 2026-04-11

### Added
- `ba-traceability` SKILL.md — RTM build, impact analysis, health check (was empty)
- `_shared/system-prompt.md` — shared identity fragment for all 26 agents
- `.agent/templates/` — 13 BA document templates (BRD, SRS, FRD, US, UC, TC, RTM, etc.)
- Examples added to 12 skills (P3 + P6)
- Workflow + Output Format sections added to 13 skills (P3 + P4+P5)

### Changed
- Standardized frontmatter: all 28 skills now have `version: 1.0.0`
- `docs/README.md` — navigation guide with agent activation reference
- 7 short skills expanded from ~80 → 150+ lines (metrics, conflict, export, root-cause, innovation, solution, identity)
- 6 C-grade skills expanded with Workflow/Output/Example (nfr, facilitation, process, prioritization, strategy, systems)

### Fixed
- `ba-traceability` was 0 lines (critical gap) — now 195 lines, Grade A

## [1.0.0] - 2026-04-10

### Initial Release
- 26 BA agent skills in `.agent/skills/`
- 5 Python scripts (ba_core, ba_search, coverage_checker, gen_docx, batch_remediate)
- 23 CSV knowledge base files (786 entries across 23 domains)
- 7 BA ebooks (fundamentals, agile, techniques, career, leadership, systems thinking, requirements memory jogger)
- 6 documentation guides in `docs/`
- Confluence connector + Jira connector skills
- EAMS Mini App Chấm Công output (first project delivery)
