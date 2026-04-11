# Antigravity Native Protocol

**Version:** 2.7.0 (Agent Skills Framework)
**Date:** 2026-04-03
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

### 🟢 Strategic & eBook-Powered (v2.7)
| Command | Role | Native Capabilities |
| :--- | :--- | :--- |
| **`@ba-strategy`** | **Strategist** | PESTLE, SWOT, Business Model Canvas, Porter's 5 Forces. |
| **`@ba-facilitation`** | **Facilitator** | Workshop Design, ODEC, Group Dynamics. |
| **`@ba-systems`** | **Systems Analyst** | Stocks & Flows, Leverage Points, System Archetypes. |
| **`@ba-agile`** | **Agile Analyst** | User Story Mapping, MVP, Hypothesis-Driven. |

### 🔗 Integration Agents (NEW in v2.9)
| Command | Role | Native Capabilities |
| :--- | :--- | :--- |
| **`@ba-jira`** | **Jira Bridge** | Story→Ticket Transport, Sprint Planning, Transport Gate Reflection. |
| **`@ba-confluence`** | **Confluence Bridge** | Markdown→XHTML Publishing, Document Import, Version Tracking. |

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
**100% Active**. All 26 agents are online and natively supported.

## 6. Error Handling Protocol
When an agent cannot complete its task:

| State | Agent Action | User Action |
| :--- | :--- | :--- |
| **Ambiguous Input** | Ask 1-3 clarifying questions. Do NOT proceed with assumptions. | Provide clarification or redirect to `@ba-elicitation`. |
| **Out of Scope** | Declare "This is outside my expertise" and recommend the correct agent. | Summon the recommended agent. |
| **Missing Context** | Request the specific missing information. Check `CONTINUITY.md` first. | Update CONTINUITY.md or provide inline. |
| **Tool Failure** | Report the failure. Provide best-effort analysis with explicit "[UNVERIFIED]" tag. | Retry or accept unverified output. |
| **Conflict Detected** | Flag the contradiction. Do NOT resolve silently. Recommend `@ba-conflict`. | Summon `@ba-conflict` to mediate. |

## 7. Handoff Data Contract
When agents recommend a handoff, the following context MUST be communicated:

| Field | Description | Example |
| :--- | :--- | :--- |
| **From** | Source agent | `@ba-elicitation` |
| **To** | Target agent | `@ba-writing` |
| **Context** | Summary of work done | "Interviewed 3 stakeholders. Key findings: ..." |
| **Artifacts** | Files created or referenced | `elicitation_notes.md`, `stakeholder_map.md` |
| **Open Questions** | Unresolved items for the next agent | "Payment flow unclear — needs PO input" |

**Format**: Agents should end their output with a structured handoff block:
```
> **Handoff → @ba-[target]**
> Context: [1-2 sentence summary]
> Artifacts: [file list]
> Open Questions: [if any]
```

## 8. Workflow Completion Criteria
A workflow chain is complete when ALL of the following are met:

1. **Validation Pass**: `@ba-validation` has reviewed the final output with Health Score ≥ 80.
2. **Traceability Check**: `@ba-traceability` confirms all requirements trace to business needs (no orphans).
3. **Stakeholder Sign-off**: The user (acting as stakeholder proxy) explicitly approves.
4. **Export Ready**: `@ba-export` has performed a compliance check with 0 critical errors.

**Iteration Rule**: If `@ba-validation` rejects output (Health Score < 80):
1. Return output to the drafting agent (usually `@ba-writing`).
2. Fix identified defects.
3. Re-submit to `@ba-validation`.
4. Maximum 3 iterations before escalating to user.

## 9. Knowledge Search Engine (BM25+)
Agents now have access to a searchable knowledge base via BM25+ text ranking.

**Usage**:
```
run_command: python3 .agent/scripts/ba_search.py "<query>" --domain <domain>
```

**23 Domains**: writing, elicitation, validation, nfr, process, prioritization, traceability, conflict, solution, systems, agile, identity, workshop, innovation, metrics, modeling, ux-research, business-rules, integration, compliance, communication, testing, data-analytics.

**Architecture**:
| Component | File | Purpose |
| :--- | :--- | :--- |
| BM25 Engine | `.agent/scripts/ba_core.py` | Search ranking algorithm (0 dependencies) |
| CLI | `.agent/scripts/ba_search.py` | Agent-facing search interface |
| Knowledge Data | `.agent/data/*.csv` | 786 entries across 23 CSV files |

**Token Efficiency**: ~460 tokens per search vs ~25,000 tokens loading full files (97% reduction).
