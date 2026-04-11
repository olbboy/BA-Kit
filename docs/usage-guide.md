# BA-Kit Usage Guide

> **"We don't just chat. We think, we link, and we remember."**

Welcome to the **BA-Kit Agent Squad**.
This is not a chatbot. It is a **Multi-Agent Expert System** for structured Business Analysis, running on Antigravity IDE, Claude Code, and Claude CoWork.

---

## 🌌 The Philosophy: Three Pillars of Intelligence

To use this kit effectively, understand how the squad works.

### 1. 🧠 System 2 Cognition (The Brain)
Standard AI answers instantly (System 1). This is prone to hallucination.
**Our Agents Stop & Think.**
*   **Reflection Loop**: Before speaking, every agent critiques its own draft.
*   **Tool Mandates**: They don't guess math (they use Python). They don't guess links (they use Grep).
*   **Skill-Based**: Each agent is a self-contained "Skill" unit (`.agent/skills/`), ensuring modularity.

### 2. 🤝 Squad Collaboration (The Network)
Agents are no longer isolated. They form a **Collaborative Network (DAG)**.
*   **Old Way**: You call `@ba-writing`. It finishes. You wonder what to do next.
*   **New Way**: `@ba-writing` finishes and *advises you*: "Handover: Summon `@ba-validation` to QA this draft."

### 3. 📒 Mission Log (The Memory)
The Squad shares a "Working Brain" via `CONTINUITY.md` (derived from `templates/continuity-template.md`).
*   **Problem**: "I told `@ba-elicitation` we are an Agile team, but `@ba-nfr` thinks we are Waterfall."
*   **Solution**: You define the Context ONCE in the Mission Log. All 26 agents read it before acting.

---

## 🚦 The Roster: 26 Specialists, One Mission

| Agent | The Archetype | When to Summon |
| :--- | :--- | :--- |
| **COMMANDER** | | |
| **`@ba-master`** | *Mission Control* | "I'm lost. Review my situation and tell me who to call." |
| **CREATIVE SQUAD** | | |
| **`@ba-identity`** | *Chief of Staff* | "New project. Who are the stakeholders? Who matters?" |
| **`@ba-elicitation`**| *The Journalist* | "I need Requirements. Interview me." (Funnel Method) |
| **`@ba-writing`** | *The Architect*| "Turn these raw notes into Gherkin User Stories." |
| **ENGINEERING SQUAD**| | |
| **`@ba-nfr`** | *The SRE* | "Define the Non-Functional Constraints (ISO 25010)." |
| **`@ba-process`** | *Lean Master* | "Visualize this messy workflow as a BPMN diagram." |
| **`@ba-traceability`**| *Graph Theorist*| "What happens if I change this requirement? Trace the impact." |
| **`@ba-conflict`** | *The Diplomat* | "Sales and Eng are fighting. Help us negotiate (Harvard Method)." |
| **OPTIMIZATION SQUAD**| | |
| **`@ba-validation`** | *The Critic* | "Roast this spec. Find every bug and logical fallacy." |
| **`@ba-prioritization`**| *The Strategist*| "We have too many features. Rank them (WSJF/RICE)." |
| **`@ba-solution`** | *The Investor* | "Calculate the ROI of this feature. Use Python." |
| **`@ba-export`** | *The Publisher* | "Compile everything into a compliant DOCX for the client." |
| **PRECOG SQUAD (Level 5)**| | |
| **`@ba-metrics`** | *Data Scientist* | "Is our Quality Control stable? Show me the Control Chart." |
| **`@ba-root-cause`** | *The Detective* | "We failed. Find the Root Cause (5 Whys)." |
| **`@ba-innovation`** | *The Futurist* | "Design an A/B test to prove this idea works." |
| **STRATEGIC SQUAD (v2.7)** | | |
| **`@ba-strategy`** | *The Strategist* | "SWOT this opportunity. Analyze the market context." |
| **`@ba-facilitation`** | *The Facilitator* | "Plan a 2-hour requirements workshop." |
| **`@ba-systems`** | *Systems Analyst* | "Map the feedback loops causing this issue." |
| **`@ba-agile`** | *Agile Analyst* | "Create a User Story Map for the MVP." |
| **INTEGRATION SQUAD (v2.9)** | | |
| **`@ba-jira`** | *Jira Bridge* | "Create Jira tickets from these validated stories." |
| **`@ba-confluence`** | *Wiki Publisher* | "Publish this BRD to Confluence." |
| **QUALITY SQUAD (v3.0)** | | |
| **`@ba-test-gen`** | *QA Architect* | "Generate test cases from US-ATTEN-01's AC." |
| **`@ba-quality-gate`** | *Quality Officer* | "Score this BRD — is it sprint-ready?" |
| **`@ba-consistency`** | *Integration Auditor* | "Check if the API spec matches the US." |
| **`@ba-auditor`** | *Chief Auditor* | "Run full project health audit. Dashboard please." |

---

## ⚔️ Tactical Protocols

### Protocol 1: The "Context Injection"
**Stop repeating yourself.**
1.  Copy `templates/continuity-template.md` to your root as `CONTINUITY.md`.
2.  Fill it out: `Goal: MVP Release`. `Constraint: Mobile Only`.
3.  **Result**: Every agent now knows this (Skills read this automatically).

### Protocol 2: The "Visual Stimulus"
**Stop describing UI.**
1.  Take a screenshot of a whiteboard or mockup.
2.  Drag & Drop it into the chat.
3.  Command: `@[image] @ba-writing Convert this UI into Field Specifications.`

### Protocol 3: The "Hypothesis Check"
**Stop guessing.**
1.  Don't say "I think this is a good idea."
2.  Command: `@ba-solution Calculate the Net Present Value (NPV) if adoption is 5%.`
3.  Watch the agent write a Python script to prove you right (or wrong).

### Protocol 4: The "Knowledge Search" (New in v2.8)
**Stop loading entire files.**
1.  When an agent needs specific knowledge, it searches the 831-entry knowledge base.
2.  Command: `python3 .agent/scripts/ba_search.py "your question" --domain writing`
3.  **Result**: Top 3 relevant entries (~460 tokens) instead of entire ebook (~25,000 tokens).
4.  **23 domains** available. Use `--list-domains` to see all.

### Protocol 5: The "Health Scan" (New in v3.0)
**Stop assuming your project is complete.**
1.  Run the automated coverage checker on your project.
2.  Command: `python3 .agent/scripts/coverage_checker.py outputs/your-project/ --verbose`
3.  **Result**: Health Score (0-100%), missing happy/edge/error scenarios per US, ambiguous terms detected.
4.  Command: `@ba-auditor` for a full executive health dashboard.

---

## 🚀 How to Begin (Zero-Shot)

You do not need to learn complex prompts. The Agents know what to do.

**Just Type:**
> `@ba-master I want to build a payment gateway.`

**The Squad will take over:**
1.  `@ba-master` will analyze the request.
2.  It will route you to `@ba-identity` to identify who is paying.
3.  `@ba-identity` will route you to `@ba-elicitation` to gather needs.
4.  The **Chain Reaction** begins.

*Welcome to System 2.*
