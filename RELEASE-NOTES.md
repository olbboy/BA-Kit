# Release 2.9.3: The Standards & Completeness Update

**Date:** 2026-04-06
**Codename:** "Standards & Completeness"

BA-Kit v2.9.3 closes the 3 remaining critical gaps and standardizes the entire documentation suite.

---

## What's New?

### 1. PRD Template (NEW)
Product Requirements Document template — the missing bridge between BRD (business case) and SRS (system spec):
*   12 sections covering Problem → Features → NFR → Release Criteria
*   OKR-native goals with baseline → target → date format
*   MoSCoW-integrated feature matrix with objective traceability
*   AI-specific NFR section (model accuracy, inference latency, hallucination rate)
*   Quality checklist (16 items across 4 categories)
*   Location: `templates/prd-template.md`

### 2. Design & Prototype Guide (NEW)
Comprehensive guide for spec → UI → validated prototype workflows:
*   **Stitch MCP**: 3 recipes — Spec→Screen, Design System, BA Feedback Loop
*   **Figma MCP**: Config template + 2 workflows (Figma→Specs, Specs→Figma review)
*   **Vibe Coding Pipeline**: Spec-First and Prototype-First patterns with anti-pattern warnings
*   Decision matrix: when to use which tool (Stitch vs Figma vs v0 vs Lovable vs Bolt)
*   Location: `docs/design-prototype-guide.md`

### 3. Prompt Library (NEW)
28 copy-paste prompts organized by BA workflow phase:
*   Phase 1: Discovery & Elicitation (5 prompts)
*   Phase 2: Analysis & Specification (7 prompts)
*   Phase 3: Validation & Quality (4 prompts)
*   Phase 4: Design & Prototype (4 prompts)
*   Phase 5: Delivery & Publishing (4 prompts)
*   Phase 6: Strategy & Optimization (6 prompts)
*   Each prompt includes: agent, expected output, power combo
*   Location: `docs/prompt-library.md`

### 4. Document Reorganization
*   All filenames standardized to kebab-case (14 renames)
*   3 overlapping architecture docs merged into 1: `docs/architecture-decisions.md`
*   New navigation index: `docs/README.md`
*   All template headers cleaned (removed legacy SKILL-XX prefixes)

### 5. AI-Slop Purge (Complete)
*   Zero AI-generated marketing filler remaining across entire codebase
*   Removed: "Cognitive Squad", "World-Class", "Super Ultra", "Military-Grade", "Legendary"
*   Consistent professional tone throughout all documentation

### 6. New Cookbook Scenarios
*   Scenario 21: Stitch MCP UI Pipeline
*   Scenario 22: Design System Alignment
*   Scenario 23: PRD-Driven Development

---

# Release 2.7.0: The eBook-Powered Intelligence

### 1. 🟢 4 New Strategic & eBook-Powered Agents
We synthesized knowledge from 16 Business Analysis eBooks into 4 new agents:

| Agent | Role | Knowledge Source |
| :--- | :--- | :--- |
| **`@ba-strategy`** | Strategic Analysis | PESTLE, SWOT, Canvas, Porter's 5 Forces |
| **`@ba-facilitation`** | Workshop Facilitation | Penny Pullan (Making Workshops Work) |
| **`@ba-systems`** | Systems Thinking | Donella Meadows (Thinking in Systems) |
| **`@ba-agile`** | Agile BA Practices | Robertson & Robertson (BA Agility) |

### 2. 📚 eBook Knowledge Base
New `ebooks/` folder containing 6 synthesized skill files:
*   `ebook-fundamentals.md` (BABOK, BCS, PMI, Dummies)
*   `ebook-techniques.md` (99 Tools, Wiegers, UML)
*   `ebook-leadership.md` (Pullan, Carnegie, Sinek)
*   `ebook-agile.md` (Robertson & Robertson)
*   `ebook-systems-thinking.md` (Donella Meadows)
*   `ebook-career.md` (Brandenburg, Carkenord)

### 3. 🎯 Enhanced ba-master Orchestrator
*   **Decision Matrix**: 18 routing rules for precise agent dispatching
*   **3-Tier Agent Registry**: Core, Advanced, Strategic/eBook-Powered
*   **Knowledge Reference**: All 19 agents now link to source knowledge

### 4. 📋 Knowledge Reference Section
All skills now include `## 📚 Knowledge Reference` linking to eBooks and standards.

---

# 🚀 Release 2.6.0: The Agent Skills Migration

**Date:** 2026-01-17
**Codename:** "Skills Migration"

We have completed the Full Migration to the **Agent Skills Framework**.

---

## 🌟 Major Refactoring

### 1. 🧬 Skill-Based Architecture
*   **Old**: Monolithic `.agent/workflows/` folder.
*   **New**: Modular `.agent/skills/<skill-name>/` structure.
*   **Benefit**: Each specialist is now self-contained, cleaner, and ready for future "Skill Resource" expansion.

### 2. 📝 Template Standardization
*   Refactored `templates/SKILL-XX-...` to clean, semantic names:
    *   `brd_template.md`
    *   `srs_template.md`
    *   `frd_template.md`
    *   `agile_artifacts.md`
*   Updated internal metadata to reference `@ba-*` agents instead of legacy `SKILL-XX` IDs.

### 3. 📚 Knowledge Base Cleanup
*   Renamed `docs/knowledge_base/` files to remove legacy numbering.
*   Ensured better readability and logical grouping.

---

# 🚀 Release 2.5.0: The Antigravity Squad Protocol

**Date:** 2026-01-07
**Codename:** "The Specialist Squad"

We have evolved. No longer a "Swarm" of bots, we are now an **Agent Squad** of 15 Specialists.
This release brings structured, verifiable requirements engineering to your workflow.

---

## 🌟 What's New?

### 1. ⚔️ The "Squad" Terminology Pivot
We have deprecated the biological "Swarm" metaphor in favor of the professional **"Squad" (Biệt Đội)** concept.
*   **Old**: Insects, Instincts, Swarm Intelligence.
*   **New**: Specialists, Collaboration, Mission Control.
*   **Why**: To align with our **System 2** (Critical Thinking) architecture. We don't just buzz; we think.

### 2. 📒 The Continuity Ledger (Shared Memory)
The Squad now shares a "Working Brain" via `templates/CONTINUITY.md`.
*   **Context Injection**: Define your Goal & Constraints once.
*   **Squad Synchronization**: All 15 agents read this file before acting.
*   **Result**: Zero repetition. Maximum alignment.

### 3. 🛡️ "Level 5 Enabler" Maturity
We have refined our claim from "Level 5 Organization" to **"High-Assurance Enabler"**.
*   We provide the **Tools** (SPC, Root Cause, Python).
*   You provide the **Agency**.
*   Together, we achieve **CMMI Level 5 behaviors**.

---

## 🚀 Release 2.4.0: The Antigravity Native Update

**Date:** 2026-01-07
**Codename:** "System 2 Swarm"

We are proud to announce the biggest architectural shift in the history of BA-Kit.
We have moved beyond "Python Scripts" to a true **Cognitive Swarm** powered by the **Antigravity Native Protocol (ANP)**.

---

## 🌟 What's New?

### 1. 🧠 System 2 Intelligence (The Reflective Loop)
Agents no longer just "output text". They now follow a strict cognitive process:
*   **System 1**: Draft the answer.
*   **System 2**: "Stop & Think" - Critique the draft for errors, hallucinations, or vague logic.
*   **Output**: The verified result.

### 2. 🛡️ Tool Mandates (Hardened Reliability)
We have eliminated common LLM errors by forcing agents to use tools:
*   **Math**: `@ba-solution` and `@ba-metrics` MUST use Python. No more mental math errors.
*   **Traceability**: `@ba-traceability` MUST use `grep` to verify links. No more hallucinated dependencies.
*   **Standards**: `@ba-nfr` MUST use `search_web` to verify ISO/GDPR clauses.

### 3. 🤖 The Full 15-Agent Roster
We have unlocked the "Level 5" capabilities with 3 new agents:
*   **`@ba-metrics`**: Statistical Process Control (SPC) expert.
*   **`@ba-root-cause`**: Deep investigator (5 Whys).
*   **`@ba-innovation`**: R&D scientist (A/B Testing).

### 4. 📖 The Workflow Cookbook
A new guide `WORKFLOW-COOKBOOK.md` containing **10 Battle-Tested Scenarios** (Startup, Enterprise, Crisis, etc.) to help you chain agents together for complex problem solving.

---

## 📦 Migration Guide

If you are coming from v1.x or v2.0 (Python Script era):

1.  **Stop** running `python ba-agent.py`.
2.  **Copy** the workflows:
    ```bash
    cp -r ba-kit/.agent/workflows/ ~/.gemini/antigravity/workflows/
    ```
3.  **Summon** via Chat:
    > "Hi @ba-identity, let's start a project."

---

## 🏆 Credits

Developed with the **System 2 Reflective Reasoning** methodology.
*   **Architecture**: Antigravity Native Protocol v2.4
*   **Compliance**: CMMI Level 5, ISO 25010, IEEE 29148.

*Code Less. Think More.*
