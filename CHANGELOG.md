# Changelog

All notable changes to BA-Kit Antigravity.

## v3.3.0 — 2026-04-13

### Added — Full Anti-Rationalization Pattern Coverage

Complete rollout of anti-rationalization pattern to all remaining 28 BA agents. All 33 agents now have the 4 anti-slack sections.

**28 agents updated** (organized by thematic batches):

- **Batch A — Core Workflow** (7): ba-identity, ba-nfr, ba-process, ba-prioritization, ba-solution, ba-conflict, ba-export
- **Batch B — Advanced Analysis** (7): ba-metrics, ba-root-cause, ba-innovation, ba-strategy, ba-facilitation, ba-systems, ba-agile
- **Batch C — Quality & Modeling** (7): ba-test-gen, ba-quality-gate, ba-consistency, ba-auditor, ba-traceability, ba-data, ba-business-rules
- **Batch D — UX/Delivery/Integration** (7): ba-ux, ba-communication, ba-change, ba-diagram, ba-jira, ba-confluence, ba-wiki

Each updated SKILL.md now includes:
- `## When to Use` — explicit triggers + exclusions
- `## Common Rationalizations` — ≥4 domain-specific excuses with factual rebuttals
- `## Red Flags` — ≥4 observable signs the skill is being violated
- `## Verification` — ≥4 evidence-based exit criteria with handoff reference

### Stats
- **Pattern coverage:** 5/33 → **33/33** (100%)
- **New rationalizations:** 140+ (28 × 5 average)
- **New red flags:** 140+
- **New verification items:** 140+
- **All rationalizations pass specificity test** (no copy-pasteable generic filler)

### Methodology
Delivered via 4 parallel subagents working on 7 files each, with domain seeds packed into prompts (realistic BA anti-patterns per agent). Quality review: automated section count check + manual specificity/observability/evidence checks on sample files.

---

## v3.2.0 — 2026-04-13

### Added — Anti-Rationalization Framework
- **docs/skill-anatomy.md** — Formal spec for BA-Kit skill format (required sections, design principles)
- **`.agent/skills/using-ba-kit/`** — Meta skill: intent-to-skill mapping, lifecycle navigation, anti-slack enforcement
- **`.claude/commands/ba-*.md`** — 6 lifecycle slash commands for Claude Code users:
  - `/ba-discover` — identity → strategy → questioning → elicitation → ux
  - `/ba-analyze` — process / data / systems / business-rules
  - `/ba-specify` — writing → nfr → traceability → diagram
  - `/ba-validate` — validation → quality-gate → consistency → test-gen → auditor
  - `/ba-deliver` — export → jira → confluence → communication → change
  - `/ba-audit` — auditor → traceability → consistency → metrics

### Enhanced — Anti-Rationalization Pattern Applied to Key Agents
5 flagship agents updated with new sections (pattern from addyosmani/agent-skills):
- `@ba-master`, `@ba-elicitation`, `@ba-writing`, `@ba-validation`, `@ba-questioning`
- Each gets:
  - **When to Use / When NOT to Use** — explicit triggers and exclusions
  - **Common Rationalizations** — table of excuses + factual rebuttals (prevents skill-skipping)
  - **Red Flags** — observable signs the skill is being violated
  - **Verification** — exit criteria checklist with evidence requirements

### Changed
- `@ba-master` routing table: added `@using-ba-kit` as fallback for ambiguous intent
- `docs/README.md`: added Lifecycle Commands section + Skill Anatomy link

### Philosophy
> "Skills are processes, not prose. Every skill encodes hard-won engineering judgment as step-by-step workflows with anti-slack mechanisms." — pattern inspired by production-grade engineering skills

---

## v3.1.1 — 2026-04-13

### Changed
- **License**: MIT → CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial 4.0 International)
- **docs/README.md**: Rewritten as onboarding navigation guide with ASCII flowchart reading path
- **All 11 docs files**: Complete rewrite for consistency, accuracy, and new-user clarity
  - prompt-library.md: 48 prompts across 10 lifecycle phases
  - workflow-cookbook.md: 15 scenarios (consolidated from 23, removed duplicates)
  - quick-start.md, usage-guide.md, junior-start.md, contributing.md: restructured
  - architecture-decisions.md: 3 new ADRs for v3.1 decisions
  - antigravity-protocol.md: 33 agents roster + diagram tool mandate
  - ai-foundation-for-ba.md, ai-tools-guide.md, design-prototype-guide.md: updated counts

### Fixed
- All stale agent counts (19/21/26) eliminated across docs
- All broken links in docs/README.md resolved
- Scenario count inconsistency (23→15) fixed in cheat sheet and ai-foundation
- Prompt count inconsistency (28/33/45→48) fixed across all files

---

## v3.1.0 — 2026-04-12

### Added — 7 New Lifecycle Agents
- `@ba-questioning` — Paul-Elder Critical Thinking Framework, interview prep, assumption surfacing
- `@ba-communication` — Audience-adapted status reports, executive summaries, meeting minutes
- `@ba-ux` — Persona, journey mapping, empathy maps, JTBD, UX psychology, usability testing
- `@ba-data` — ERD, data dictionary, DFD, data mapping, migration planning
- `@ba-change` — ADKAR assessment, training needs, go-live planning, benefits realization
- `@ba-business-rules` — Decision tables, decision trees, rule catalog, conflict detection
- `@ba-diagram` — Mermaid v11 (24+ types), BA artifact→diagram mapping, Confluence export

### Enhanced
- `@ba-questioning` v2.1 — 8 Elements of Reasoning, Intellectual Standards, Wilson Method, Socratic Protocol, bias detection
- `@ba-ux` v2.0 — UX Psychology (Cognitive Load, Decision Architecture, Key Laws), heuristic evaluation, usability test protocol
- `@ba-agile` — Estimation facilitation (Planning Poker, T-shirt sizing, story splitting)
- `@ba-wiki` — Glossary management (ubiquitous language, synonym detection)
- `@ba-confluence` — Mermaid diagram handling (Stratus mermaid-macro for DC, pre-render SVG)
- `@ba-master` — Routing table expanded with 15+ new entries for all new agents

### Knowledge Base
- 3 new knowledge base files: questioning.md, communication.md, change_management.md
- 831 entries across 23 domains (unchanged from v3.0)

### Documentation
- 48 copy-paste prompts (was 33)
- Agent cheat sheet updated for 33 agents
- Prompt library expanded with 5 new phases
- .gitignore reorganized: Python artifacts, Claude session state, outputs/, diagrams

### Infrastructure
- outputs/ removed from git tracking (project deliverables are per-instance)
- .claude/session-state/ removed from git tracking (local per-machine)
- __pycache__/*.pyc cleaned from tracking

---

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
