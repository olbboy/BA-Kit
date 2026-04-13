# BA-Kit Sprint Spine

> **The unified 7-phase loop that all 43 BA-Kit agents feed into.**
> Think→Plan→Build→Review→Test→Ship→Reflect — adapted for Requirements Engineering.

---

## Why a spine?

BA-Kit v3.1 had 33 agents + 17 cookbook scenarios. v3.2 grows to 43 (10 new from gstack distillation). That's powerful, but the user faces **paralysis of choice**: "Which agent first? Which scenario fits?"

Gstack (the reference for this design) solves this with a **single sprint loop** that every skill feeds into. One loop, many nodes.

This doc defines the equivalent for BA: **the Requirements Sprint Spine**.

---

## The 7 phases

```
Discover → Elicit → Define → Validate → Prioritize → Publish → Reflect
                                                                    │
                                                                    └──► (loop back)
```

| Phase | Question the phase answers | Output |
|-------|----------------------------|--------|
| **1. Discover** | "What's the business context? Who cares?" | Stakeholder map, strategic canvas, competency grid |
| **2. Elicit** | "What do stakeholders actually need?" | Interview notes, assumption list, raw backlog |
| **3. Define** | "What are the precise requirements?" | User stories, AC, NFRs, data models, business rules |
| **4. Validate** | "Are the requirements correct, complete, testable?" | Quality gate report, consistency report, test cases |
| **5. Prioritize** | "What ships first? What's the trade-off?" | MoSCoW/RICE/WSJF ranking, prioritized backlog |
| **6. Publish** | "How does this reach the team + systems?" | Jira tickets, Confluence pages, DOCX exports |
| **7. Reflect** | "What did we learn? What drifted?" | Retro, as-built drift, captured learnings |

---

## Agent → phase map

| Phase | Primary agents | Supporting agents |
|-------|---------------|-------------------|
| **1. Discover** | `@ba-identity`, `@ba-strategy`, `@ba-systems` | `@ba-questioning`, `@ba-ux` |
| **2. Elicit** | `@ba-elicitation`, `@ba-questioning`, `@ba-facilitation` | `@ba-wiki` (prior art), `@ba-ux` |
| **3. Define** | `@ba-writing`, `@ba-nfr`, `@ba-data`, `@ba-business-rules`, `@ba-process` | `@ba-diagram`, `@ba-ux` |
| **4. Validate** | `@ba-validation`, `@ba-consistency`, `@ba-quality-gate`, `@ba-test-gen`, `@ba-traceability` | `@ba-challenger` 🆕, `@ba-second-opinion` 🆕 |
| **5. Prioritize** | `@ba-prioritization`, `@ba-solution`, `@ba-conflict` | `@ba-agile`, `@ba-innovation` |
| **6. Publish** | `@ba-export`, `@ba-jira`, `@ba-confluence`, `@ba-communication` | `@ba-change` |
| **7. Reflect** | `@ba-retro` 🆕, `@ba-as-built` 🆕, `@ba-auditor`, `@ba-metrics` | `@ba-learn` 🆕, `@ba-root-cause` |

**Meta-agents (span all phases):**
- `@ba-master` — dispatcher
- `@ba-autoreview` 🆕 — runs phase 4 pipeline in one command
- `@ba-checkpoint` 🆕 — session save/resume (works at any phase)
- `@ba-wiki` — knowledge query (used anywhere)

---

## How to move between phases

Each phase has an **exit criterion**. Don't advance without satisfying it.

| From → To | Exit criterion |
|-----------|----------------|
| Discover → Elicit | Stakeholder map signed off, top 3 strategic drivers identified |
| Elicit → Define | ≥ 3 raw requirements captured per module; no "TBD" blockers |
| Define → Validate | Every requirement has acceptance criteria + owner |
| Validate → Prioritize | Quality gate PASS or CONDITIONAL (not REJECT); consistency clean |
| Prioritize → Publish | Ranking agreed by PM + stakeholders; dependencies mapped |
| Publish → Reflect | Tickets + docs delivered to downstream systems |
| Reflect → Discover | Retro action items feed next discovery loop |

---

## Hand-off contract (SKILL.md frontmatter v2)

Starting v3.2, every SKILL.md should declare its phase + data contract:

```yaml
---
name: ba-writing
description: ...
version: 1.1.0
phase: Define                    # 1 of 7 phases above
inputs:                          # What must exist before this skill runs
  - elicitation-notes.md
  - stakeholder-map.md
outputs:                         # What this skill produces
  - user-stories.md
  - acceptance-criteria.md
downstream:                      # Which skills consume my output
  - ba-validation
  - ba-test-gen
  - ba-consistency
---
```

Chains form automatically: if you run `@ba-writing` and its `downstream` field lists `@ba-validation`, the dispatcher (ba-master) can auto-suggest the next step.

---

## Consolidating the 17 cookbook scenarios

The existing `docs/workflow-cookbook.md` has 17 scenarios. They are **not deleted** — they become **variants** of the spine:

| Scenario | Spine entry point | Special variant |
|----------|-------------------|----------------|
| #1 "Startup Founder" | Discover → ... → Publish | Full loop, MoSCoW heavy |
| #2 "Legacy Migration" | Discover (as-is) → Define → Validate | Adds `@ba-process` at Discover |
| #3 "Stakeholder War" | Elicit → Prioritize (conflict branch) | `@ba-conflict` at Prioritize |
| #5 "Production Crisis" | Reflect → Define | Root cause loop |
| #8 "Compliance Audit" | Validate → Publish | `@ba-traceability` heavy |
| #17 "Testing Handoff" | Validate → Publish | `@ba-test-gen` + `@ba-traceability` |
| ... | ... | ... |

**Rule:** Every cookbook scenario must map to a contiguous path through the spine. If it doesn't, it's flagged as "scenario debt" and either normalized or removed.

---

## Running the spine as a single command

The new `@ba-autoreview` skill runs Phase 4 (Validate) end-to-end:

```
@ba-autoreview outputs/my-project/
  → Phase 0: Detect artifact types (BRD / US / API / DB)
  → Phase 4a: @ba-consistency    (cross-artifact alignment)
  → Phase 4b: @ba-quality-gate   (8-dim scoring)
  → Phase 4c: @ba-traceability   (RTM coverage)
  → Phase 4d: @ba-auditor        (synthesize health report)
  → (optional) @ba-second-opinion (cross-model review)
  → Single verdict: PASS / CONDITIONAL / REJECT
```

Future work: `@ba-autodiscover`, `@ba-autoelicit` etc. for other phases.

---

## Versioning

- **v1.0** (this doc, 2026-04-13): Define 7 phases + initial agent mapping.
- **v1.1** (target v3.2): Add frontmatter `phase:` to all 33 existing skills.
- **v2.0** (target v3.3): Runtime enforcement — ba-master blocks out-of-phase handoffs.
