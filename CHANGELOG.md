# Changelog

All notable changes to BA-Kit Antigravity.

## [1.1.0] - 2026-04-11

### Added
- `ba-traceability` SKILL.md — RTM build, impact analysis, health check (was empty)
- `_shared/system-prompt.md` — shared identity fragment for all 25 agents
- `.agent/templates/` — 13 BA document templates (BRD, SRS, FRD, US, UC, TC, RTM, etc.)
- Examples added to 12 skills (P3 + P6)
- Workflow + Output Format sections added to 13 skills (P3 + P4+P5)

### Changed
- Standardized frontmatter: all 27 skills now have `version: 1.0.0`
- `docs/README.md` — navigation guide with agent activation reference
- 7 short skills expanded from ~80 → 150+ lines (metrics, conflict, export, root-cause, innovation, solution, identity)
- 6 C-grade skills expanded with Workflow/Output/Example (nfr, facilitation, process, prioritization, strategy, systems)

### Fixed
- `ba-traceability` was 0 lines (critical gap) — now 195 lines, Grade A

## [1.0.0] - 2026-04-10

### Initial Release
- 25 BA agent skills in `.agent/skills/`
- 4 Python scripts (ba_core, ba_search, coverage_checker, gen_docx)
- 23 CSV knowledge base files (809 entries across 23 domains)
- 7 BA ebooks (fundamentals, agile, techniques, career, leadership, systems thinking, requirements memory jogger)
- 6 documentation guides in `docs/`
- Confluence connector + Jira connector skills
- EAMS Mini App Chấm Công output (first project delivery)
