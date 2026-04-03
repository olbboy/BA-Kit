<p align="center">
  <img src="assets/logo.png?v=2.7.0" alt="BA-Kit Logo" width="200">
</p>

<div align="center">

[**🇬🇧 English**](README.md) | [**🇻🇳 Tiếng Việt**](README.vi.md)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.8-blue?style=for-the-badge" alt="Version 2.8">
  <img src="https://img.shields.io/badge/Agents-19-green?style=for-the-badge" alt="19 Agents">
  <img src="https://img.shields.io/badge/Protocol-Antigravity%20Native-orange?style=for-the-badge" alt="Antigravity Native">
  <img src="https://img.shields.io/badge/Capability-CMMI%20Level%205%20Enabler-purple?style=for-the-badge" alt="CMMI Level 5 Enabler">
  <img src="https://img.shields.io/badge/Knowledge-786%20Entries-teal?style=for-the-badge" alt="786 Knowledge Entries">
</p>

<h1 align="center">🏆 BA-Kit (Antigravity Edition)</h1>
<h3 align="center">The Cognitive Squad for Requirements Engineering</h3>

<p align="center">
  <strong>Transform your AI into a World-Class Business Analysis Team</strong><br>
  19 Self-Correcting Specialists • System 2 Reflection • eBook-Powered Knowledge
</p>


---

## 🎯 What is BA-Kit?

BA-Kit is not just a library of prompts; it is a **Cognitive Squad** designed for the **Antigravity Native Protocol (ANP)**.

It replaces the "Single Chatbot" paradigm with a **Team of 19 Specialists**:
*   Need a User Story? Summon **`@ba-writing`**.
*   Need strategic context? Summon **`@ba-strategy`**.
*   Need to run a workshop? Summon **`@ba-facilitation`**.

Each agent is equipped with **System 2 Thinking** (Reflective Loops) to "Stop & Think" before answering, ensuring hallucination-free High Assurance results.

---

## 🤖 The Agent Squad (19 Personas)

### 🔴 The Orchestrator
| Agent | Role | Capability |
| :--- | :--- | :--- |
| **`@ba-master`** | **Dispatcher** | Strategy, Routing, Context Management. |

### 🔵 Core Agents (The Foundation)
| Agent | Role | Capability |
| :--- | :--- | :--- |
| **`@ba-identity`** | Chief of Staff | Stakeholder Mapping, RACI, Competency Grid. |
| **`@ba-elicitation`**| Journalist | Funnel Questioning, "Colombo" Method. |
| **`@ba-writing`** | Architect | **Visual UI Scan**, Gherkin Drafting (BDD). |

### 🟡 Specialized Agents (The Experts)
| Agent | Role | Capability |
| :--- | :--- | :--- |
| **`@ba-validation`** | QA Lead | **Visual QA**, Edge Case Detection. |
| **`@ba-traceability`**| CCB Secretary| **Grep Verification** (No Hallucinations). |
| **`@ba-nfr`** | SRE Architect | **Web-Validated** ISO 25010 Standards. |
| **`@ba-process`** | Lean Master | **Whiteboard Vision**, BPMN Waste Analysis. |
| **`@ba-prioritization`**| Product Mgr | MoSCoW, RICE, WSJF Frameworks. |
| **`@ba-solution`** | Investor | **Python-Verified** ROI & NPV Math. |
| **`@ba-conflict`** | Mediator | Harvard Negotiation, ADR Drafting. |
| **`@ba-export`** | Publisher | Compliance Check, Pandoc Formatting. |

### 🟣 Advanced Agents
| Agent | Role | Capability |
| :--- | :--- | :--- |
| **`@ba-metrics`** | Data Scientist| **SPC Charts**, Defect Density, Cpk stats. |
| **`@ba-root-cause`**| Investigator | 5 Whys, Fishbone, Pareto Analysis. |
| **`@ba-innovation`**| R&D Scientist | **A/B Testing**, Hypothesis Designs. |

### 🟢 Strategic & eBook-Powered Agents (NEW in v2.7)
| Agent | Role | Capability |
| :--- | :--- | :--- |
| **`@ba-strategy`** | Strategist | PESTLE, SWOT, Business Model Canvas, Porter's 5 Forces. |
| **`@ba-facilitation`** | Facilitator | Workshop Design, ODEC Framework, Group Dynamics. |
| **`@ba-systems`** | Systems Analyst | Stocks & Flows, Leverage Points, System Archetypes. |
| **`@ba-agile`** | Agile Analyst | User Story Mapping, MVP Definition, Hypothesis-Driven. |

---

## 🚀 Quick Start (Antigravity Native)

### 1. Installation
Copy the workflows into your Agent's brain:
```bash
cp -r ba-kit/.agent/skills/* ~/.gemini/antigravity/skills/
```

### 2. Summoning
In your chat, simply type `@` followed by the Agent Name:
> **User**: *"@ba-writing I need a login feature."*

> **@ba-writing**: *"Architect online. I see you want a Login. Shall we use Email/OTP or Social Auth? Let's draft the Happy Path first..."*

### 3. The "Flash Mode"
You can switch agents instantly to handle complex tasks:
> **User**: *"This requirement seems risky. @ba-solution check the ROI."*

> **@ba-solution**: *"Investor here. I'll calculate the NPV using Python..."*

---

## 🧠 System 2 Intelligence (New in v2.4)

All agents now follow a **Reflective Cognitive Loop**:
1.  **Analysis (System 1)**: Fast pattern matching.
2.  **Action (System 1)**: Draft content.
3.  **Reflection (System 2)**: **STOP & THINK**.
    *   *Critic*: "Did I hallucinate that dependency?"
    *   *Action*: Verify with `grep` or `python`.
4.  **Output**: Verified, High-Precision Answer.

---

## 📁 Repository Structure

```
ba-kit/
│
├── .agent/skills/              # 🤖 The Brains (19 Agent Skills)
├── ebooks/                     # 📚 eBook Knowledge Base (6 Synthesized Skills)
├── docs/knowledge_base/        # 📖 The Knowledge (Core & Specialized)
├── templates/                  # 🟢 Templates (BRD, SRS, User Stories)
├── .agent/scripts/             # 🔍 BM25+ Knowledge Search Engine
├── .agent/data/                # 📊 786 Indexed Knowledge Entries (23 domains)
├── docs/                       # 📘 Protocol Documentation
│   └── ANTIGRAVITY_PROTOCOL.md #    The Technical Spec
└── README.md                   # 📄 This file
```

---

## 🔍 Knowledge Search Engine (New in v2.8)

BA-Kit now includes a **BM25+ Knowledge Search Engine** with **786 indexed entries** across **23 domains**.

```bash
# Search for any BA concept
python3 .agent/scripts/ba_search.py "acceptance criteria gherkin"

# Search specific domain
python3 .agent/scripts/ba_search.py "GDPR compliance" --domain compliance

# Search across all domains
python3 .agent/scripts/ba_search.py "stakeholder analysis" --multi-domain

# View statistics
python3 .agent/scripts/ba_search.py --stats
```

**23 Domains**: writing, elicitation, validation, nfr, process, prioritization, traceability, conflict, solution, systems, agile, identity, workshop, innovation, metrics, modeling, ux-research, business-rules, integration, compliance, communication, testing, data-analytics.

---

## 📄 License
MIT License. Free to use for personal and enterprise projects.

---

<p align="center">
  <strong>Built for the Antigravity Age.</strong><br>
  <em>Code Less. Think More.</em>
</p>
