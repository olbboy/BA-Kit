# Changelog

All notable changes to BA-Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.9.3] - 2026-04-06

### The Standards & Completeness Update
*   **3 Critical Gaps Closed**:
    *   **PRD Template**: New `templates/prd-template.md` — 12-section Product Requirements Document with OKR-native goals, MoSCoW-integrated features, AI-specific NFR section, and traceability columns.
    *   **Design & Prototype Guide**: New `docs/design-prototype-guide.md` — Stitch MCP workflows (3 recipes), Figma MCP setup, v0/Lovable/Bolt vibe-coding pipeline, and tool decision matrix.
    *   **Prompt Library**: New `docs/prompt-library.md` — 28 copy-paste prompts organized by 6 BA workflow phases (Discovery → Delivery), each with agent assignment and power combos.
*   **Document Reorganization**: Standardized all file naming to kebab-case. Merged 3 overlapping architecture docs into single `docs/architecture-decisions.md`. Created `docs/README.md` navigation index.
*   **Header Standardization**: Removed legacy `SKILL-XX:` prefixes and emojis from all template and docs headers.
*   **AI-Slop Removal**: Purged all remaining AI-generated fingerprints (Cognitive Squad, World-Class, Super Ultra, Military-Grade, etc.) across 17 files. Zero AI-slop remaining.
*   **3 New Cookbook Scenarios**: Stitch MCP UI Pipeline (#21), Design System Alignment (#22), PRD-Driven Development (#23). Total: 23 scenarios.
*   **2 New Power Combos**: PRD Pipeline, Stitch UI added to agent cheat sheet.
*   **Cross-Reference Integrity**: All internal links updated to match renamed files. Zero stale references.

## [2.9.0] - 2026-04-06

### 🔗 The Integration & Foundation Update
*   **2 New Integration Agents**: `@ba-jira` (BA→Jira Transport Bridge with Transport Gate reflection) and `@ba-confluence` (BA→Confluence Publishing Bridge with Publishing Gate reflection). Squad now has **21 agents**.
*   **Multi-Platform Support**: BA-Kit now officially supports 3 agentic platforms: **Antigravity IDE** (primary), **Claude Code** (developer CLI), and **Claude CoWork** (non-technical desktop). Platform comparison tables and recommendation matrix added.
*   **Transport Gate Pattern**: New System 2 reflection variant — focuses on "deployment safety" (duplicate detection, field completeness, format correctness) rather than content quality.
*   **AI Foundation Module**: New `docs/ai-foundation-for-ba.md` — bilingual (Vi/En) educational document covering LLM, Tokens, Context Window, AI Agents, RAG, MCP, the 3 Platforms (Antigravity/Claude Code/Claude CoWork), Prompt Thinking, Security.
*   **AI Tools Guide**: New `docs/ai-tools-guide.md` — decision matrix for 9 tools across 3 platforms, input/output adapters (including Claude Code reverse engineering and Claude CoWork document synthesis), 6 multi-tool/multi-platform workflow recipes.
*   **Junior BA Week 0**: Added AI Foundation prerequisite to onboarding path with 3-platform choice guidance.
*   **Security**: `.env` files added to `.gitignore`. 3-platform security comparison table in Foundation doc.
*   **ba-master Routing**: 6 new routing rules for Jira, Confluence, Figma, vibe coding, and AI tool selection.
*   **6 New COOKBOOK Scenarios**: Jira Pipeline (#18), Confluence Publisher (#19), Multi-Tool Pipeline (#20) + Claude Code Reverse Engineering, Claude CoWork Synthesis, Multi-Platform CI.
*   **New Power Combos**: Jira Pipeline, Confluence Publish, Full Pipeline chains added to cheat sheet.

## [2.8.0] - 2026-04-03

### 🔍 The Knowledge Engine & Completion Update
*   **BM25+ Knowledge Engine**: Added Python-based BM25 search engine (`ba_core.py` + `ba_search.py`) with 786 indexed entries across 23 domains. Agents now search knowledge on-demand instead of loading entire files. 97% token reduction per search.
*   **7 New Domains**: ux-research (45 entries), business-rules (34), integration (35), compliance (35), communication (25), testing (30), data-analytics (24).
*   **4 New Templates**: Use Case Specification, Data Dictionary, Communication Plan, API Contract.
*   **Junior BA Onboarding**: Added `docs/JUNIOR-START.md` with 4-week learning path and progressive difficulty (beginner → intermediate → advanced).
*   **5 New COOKBOOK Scenarios**: API Integration, Compliance Audit, UX-First Requirements, Data Project, Testing Handoff.
*   **Adversarial Review**: Fixed 2 critical bugs (search_multi crash, MCP bind 0.0.0.0), 306 wrong agent references, PRC-032 CSV corruption. Quality score improved from 6.5 to 8.0.

## [2.7.0] - 2026-04-03

### 📚 The Memory Jogger & Strategic Update
*   **New Agents**: Added 4 strategic & eBook-powered agents (`@ba-strategy`, `@ba-facilitation`, `@ba-systems`, `@ba-agile`). Squad now has **19 agents**.
*   **Memory Jogger Integration**: Integrated Gottesdiener's "Software Requirements Memory Jogger" content into 10 agents — SRS templates, ambiguity detection lists, validation checklists, and prioritization frameworks.
*   **Protocol Expansion**: Added error handling protocol, handoff data contracts, and completion criteria to ANP spec.
*   **Security Hardening**: MCP bridge now uses cryptographic session IDs, auth middleware, session TTL, and graceful shutdown.
*   **Quality Audit**: Comprehensive 10-criteria quality assessment (7.2/10). Fixed terminology debt ("Swarm"→"Squad"), version consistency, and agent count references.

## [2.6.0] - 2026-01-20

### 🔧 The Agent Skills Migration
*   **Architecture**: Migrated from `.agent/workflows/` to `.agent/skills/` directory structure.
*   **Skill Format**: Adopted YAML frontmatter with `name` and `description` fields.
*   **MCP Bridge**: Added Perplexity SSE bridge for web search capabilities.
*   **Documentation**: Updated ANTIGRAVITY_PROTOCOL.md to reflect skills framework.

## [2.5.0] - 2026-01-07

### ⚔️ The Squad Protocol Update
*   **Terminology Overhaul**: Renamed "Swarm" (Bầy đàn) to **"Squad" (Biệt Đội)** across all documentation (Eng/Viet).
*   **New Feature**: Added **Continuity Ledger** (`templates/CONTINUITY.md`) for inter-agent memory sharing.
*   **Maturity Pivot**: Refined CMMI Level 5 claims to **"Level 5 Enabler"** (Exoskeleton Theory).
*   **Usage Guide**: Rewrote `USAGE-GUIDE` as **"The Antigravity Codex"**.

## [2.4.0] - 2026-01-07

### 🧠 The Antigravity Native Update (System 2 Swarm)

This major architectural release transitions BA-Kit from a collection of scripts/prompts to a full **Antigravity Native Swarm** of 15 self-correcting agents.

#### 🆕 System 2 Intelligence
*   **Reflective Loops**: All 15 agents now use a "Stop & Think" cognitive model. They critique their own drafts before answering.
*   **Tool Mandates**: Implemented strict rules to prevent LLM Hallucinations:
    *   **Math**: Agents MUST use `python` for ROI/NPV/SPC calculations.
    *   **Search**: Agents MUST use `grep` to verify file existence (Traceability).
    *   **Standards**: Agents MUST use `search_web` to verify ISO clauses.

#### 🤖 New Agents (CMMI Level 5)
*   **`@ba-metrics`**: The Data Scientist Agent. Uses Python to calculate Control Charts, Sigma Levels, and Defect Density.
*   **`@ba-root-cause`**: The Investigator Agent. Uses Fishbone and 5 Whys to find systemic issues.
*   **`@ba-innovation`**: The R&D Scientist Agent. Designs A/B tests and calculates Pilot ROI.

#### 📚 Documentation Overhaul
*   **README.md**: Completely rewritten to feature the "15 Agent Swarm".
*   **QUICK-START.md**: Simplified to "Install & Summon" (Antigravity Syntax).
*   **USAGE-GUIDE.md**: Deep dive into the "Cognitive Loop" and best practices.
*   **AGENT.MD**: Updated to be the "Single Source of Truth" for the Swarm Configuration.

#### 🛠️ Deprecation
*   **Legacy Python Scripts**: The old CLI wrappers (`python ba-agent.py`) are now secondary to the direct `@agent` syntax.

---

## [2.3.0] - 2026-01-07
### 🛡️ The Tool Hardening Update
*   Enforced "Mandatory Tool Use" for `@ba-solution` (Math) and `@ba-traceability` (Grep).
*   Completed "Deep Gap Analysis" of Antigravity potential.

## [2.2.0] - 2026-01-04

### 💎 The Professional Branding Update
*   New "Knowledge Block" Logo.
*   Context-Aware Template Organization.

---
(Previous versions preserved below...)
