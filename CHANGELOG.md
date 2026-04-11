# Changelog

All notable changes to BA-Kit Antigravity.

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
