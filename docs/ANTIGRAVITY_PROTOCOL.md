# 🧠 Antigravity Native Protocol (ANP)

**Version:** 2.6.0 (Agent Skills Framework)
**Date:** 2026-01-17
**Status:** PRODUCTION READY (SKILLS MIGRATED)

## 1. The Core Philosophy
The **Antigravity Native Protocol (ANP)** enables "Direct Persona Injection".
Instead of running a script (`./ba-agent`), you (The User) directly **summon the expert** into the LLM context.

## 2. The Summoning Syntax (`@`)
We repurpose the `@` symbol to represent **Agent Context Switching**.

### 🔴 The Orchestrator
| Command | Role | Native Capabilities |
| :--- | :--- | :--- |
| **`@ba-master`** | **Dispatcher** | **Squad Planning**, Routing, Strategy. |

### 🔵 Core Workflows (The Foundation)
| Command | Role | Native Capabilities |
| :--- | :--- | :--- |
| **`@ba-identity`** | **Chief of Staff** | Persona Routing, Stakeholder Mapping. |
| **`@ba-elicitation`**| **Journalist** | Funnel Questioning, "Colombo" Method. |
| **`@ba-writing`** | **Architect** | **Vision (UI Scan)**, Gherkin Drafting. |

### 🟡 Specialized Workflows (The Experts)
| Command | Role | Native Capabilities |
| :--- | :--- | :--- |
| **`@ba-validation`** | **QA Lead** | **Visual QA**, Edge Case Detection. |
| **`@ba-traceability`**| **CCB Sec** | **Grep Verification** (No Hallucinations). |
| **`@ba-nfr`** | **SRE Architect** | **Web-Validated** ISO Standards. |
| **`@ba-process`** | **Lean Master**| **Whiteboard Vision**, Waste Analysis. |
| **`@ba-prioritization`**| **Product Mgr** | MoSCoW, RICE, WSJF Frameworks. |
| **`@ba-solution`** | **Investor** | **Python-Verified** ROI & NPV Math. |
| **`@ba-conflict`** | **Mediator** | Harvard Negotiation, ADR Drafting. |
| **`@ba-export`** | **Publisher** | Compliance Check, formatting. |

### 🟣 Advanced Workflows (CMMI Level 5 - Optimization)
| Command | Role | Native Capabilities |
| :--- | :--- | :--- |
| **`@ba-metrics`** | **Data Scientist**| **SPC Charts**, Defect Density, Cpk stats. |
| **`@ba-root-cause`**| **Investigator**| 5 Whys, Fishbone, Pareto Analysis. |
| **`@ba-innovation`**| **R&D Scientist**| **A/B Testing**, Hypothesis Designs. |

## 3. Tool Usage Mandates (Hardening)
To prevent "LLM Hallucinations", specific agents MUST use specific tools.

| Agent | Risk | Mandatory Tool |
| :--- | :--- | :--- |
| **@ba-solution** | Bad Math | `run_command(python)` |
| **@ba-metrics** | Bad Stats | `run_command(python)` |
| **@ba-traceability**| Broken Links | `grep_search` |
| **@ba-nfr** | Old Standards | `search_web` |
| **@ba-innovation** | Bad P-Values | `run_command(python)` |

## 4. System 2 Thinking (Reflective Loop)
Antigravity Agents are now self-correcting.

1.  **Analysis Mode (System 1)**: Fast pattern matching. Read input -> Identify Gaps.
2.  **Action Mode (System 1)**: Draft content / Generate Questions.
3.  **Reflection Mode (System 2)**: **STOP & THINK**.
    *   *Critic*: "Is this specific enough? Is it testable? Did I hallucinate?"
    *   *Refiner*: Rewrite the output to address the Critic's concerns.
4.  **Output Mode**: Present the finalized, polished thinking.

## 5. Implementation Status
**100% Active**. All 15 agents are online and natively supported.
