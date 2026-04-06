# PRD Template / Product Requirements Document

---

## Metadata

| Attribute | Value |
|-----------|-------|
| **Template ID** | TMPL-PRD |
| **Category** | Template |
| **Load When** | Defining product features for development |
| **Dependencies** | @ba-elicitation, @ba-writing, @ba-prioritization, @ba-nfr |
| **Output** | Complete PRD document |

---

## When to Use PRD / Khi Nào Dùng PRD

| Dùng PRD Khi | Không Dùng PRD Khi |
|--------------|-------------------|
| Product team cần alignment về WHAT to build | Chỉ cần business justification (dùng BRD) |
| Feature phức tạp, cần multiple sprints | Bug fix hoặc hotfix đơn giản |
| Cross-functional teams cần shared context | Technical implementation details (dùng SRS) |
| Stakeholder sign-off trước khi dev | Internal tooling nhỏ, team tự quyết |
| AI/ML features cần define accuracy targets | API spec chi tiết (dùng API Contract) |

### PRD vs BRD vs SRS vs FRD

| Document | Focus | Audience | Question |
|----------|-------|----------|----------|
| **BRD** | Business case, WHY | Executives, sponsors | "Tại sao làm?" |
| **PRD** | Product scope, WHAT | Product + Engineering | "Làm gì, cho ai?" |
| **SRS** | System behavior, HOW | Engineering | "Hệ thống hoạt động thế nào?" |
| **FRD** | Functional detail, HOW exactly | Dev team | "Mỗi function làm gì cụ thể?" |

---

## PRD Template

```
═══════════════════════════════════════════════════════════════
                PRODUCT REQUIREMENTS DOCUMENT
                      [Product/Feature Name]
═══════════════════════════════════════════════════════════════

Document Control
────────────────────────────────────────────────────────────────
Version: [X.Y]
Date: [YYYY-MM-DD]
Author: [Name, Role]
Status: [Draft / In Review / Approved / Superseded]
Product: [Product Name]
Squad/Team: [Team Name]

Version History
┌─────────┬────────────┬──────────┬─────────────────────────────┐
│ Version │ Date       │ Author   │ Changes                     │
├─────────┼────────────┼──────────┼─────────────────────────────┤
│ 0.1     │ YYYY-MM-DD │ [Name]   │ Initial draft               │
│ 0.2     │ YYYY-MM-DD │ [Name]   │ Added user flows            │
│ 1.0     │ YYYY-MM-DD │ [Name]   │ Approved for development    │
└─────────┴────────────┴──────────┴─────────────────────────────┘

Approval
┌──────────────────┬────────────┬─────────────┬────────────────┐
│ Name             │ Role       │ Decision    │ Date           │
├──────────────────┼────────────┼─────────────┼────────────────┤
│                  │ Product    │ [Y/N/Defer] │                │
│                  │ Eng Lead   │ [Y/N/Defer] │                │
│                  │ Design     │ [Y/N/Defer] │                │
│                  │ QA Lead    │ [Y/N/Defer] │                │
└──────────────────┴────────────┴─────────────┴────────────────┘


═══════════════════════════════════════════════════════════════
1. PRODUCT OVERVIEW & VISION
═══════════════════════════════════════════════════════════════

1.1 One-Liner
────────────────────────────────────────────────────────────────
[1 câu mô tả product/feature — dùng format: 
"[Product] giúp [target user] [đạt được gì] bằng cách [cơ chế]"]

Ví dụ: "Smart Checkout giúp khách hàng e-commerce hoàn tất 
thanh toán trong < 30 giây bằng cách auto-fill thông tin và 
one-tap payment."

1.2 Background & Context
────────────────────────────────────────────────────────────────
[Bối cảnh kinh doanh, thị trường, hoặc nội bộ dẫn đến nhu cầu
này. Tham khảo BRD nếu đã có.]

Reference: [Link to BRD / Epic / Strategic Initiative]

1.3 Product Vision Statement
────────────────────────────────────────────────────────────────
FOR [target user]
WHO [pain point / need]
THE [product name] IS A [product category]
THAT [key benefit]
UNLIKE [current alternative / competitor]
OUR PRODUCT [key differentiator]


═══════════════════════════════════════════════════════════════
2. PROBLEM STATEMENT
═══════════════════════════════════════════════════════════════

2.1 Problem Definition
────────────────────────────────────────────────────────────────
[Stakeholder/User] gặp vấn đề [problem description] 
dẫn đến [measurable business impact].

2.2 Evidence & Data
────────────────────────────────────────────────────────────────
┌──────────────────────────────┬────────────────────────────────┐
│ Data Point                   │ Source                         │
├──────────────────────────────┼────────────────────────────────┤
│ [e.g., 40% cart abandonment] │ [e.g., GA4 Q1 2026 report]    │
│ [e.g., 15 support tickets/d] │ [e.g., Jira Service Desk]     │
│ [e.g., NPS dropped to 32]   │ [e.g., Quarterly survey]      │
└──────────────────────────────┴────────────────────────────────┘

2.3 Current Workarounds
────────────────────────────────────────────────────────────────
[How users currently solve this problem — manual process, 
competing product, or "just deal with it"]


═══════════════════════════════════════════════════════════════
3. TARGET USERS & PERSONAS
═══════════════════════════════════════════════════════════════

3.1 Primary Persona
────────────────────────────────────────────────────────────────
Name: [Persona Name]
Role: [Job title / demographic]
Goal: [What they want to achieve]
Frustration: [Current pain point]
Tech Comfort: [Low / Medium / High]
Usage Frequency: [Daily / Weekly / Monthly]

3.2 Secondary Personas
────────────────────────────────────────────────────────────────
┌────────────────┬─────────────────┬──────────────────────────┐
│ Persona        │ Key Need        │ Difference from Primary  │
├────────────────┼─────────────────┼──────────────────────────┤
│ [Name]         │ [Need]          │ [How they differ]        │
│ [Name]         │ [Need]          │ [How they differ]        │
└────────────────┴─────────────────┴──────────────────────────┘

3.3 Anti-Personas (Not Target Users)
────────────────────────────────────────────────────────────────
[Explicitly state who this is NOT for — prevents scope creep]
• [Anti-persona 1]: [Why excluded]
• [Anti-persona 2]: [Why excluded]


═══════════════════════════════════════════════════════════════
4. GOALS & SUCCESS METRICS
═══════════════════════════════════════════════════════════════

4.1 Objectives & Key Results (OKRs)
────────────────────────────────────────────────────────────────
Objective 1: [Qualitative goal statement]
  KR1: [Metric] from [baseline] to [target] by [date]
  KR2: [Metric] from [baseline] to [target] by [date]

Objective 2: [Qualitative goal statement]
  KR1: [Metric] from [baseline] to [target] by [date]

4.2 North Star Metric
────────────────────────────────────────────────────────────────
[Single metric that best captures product success]
Current: [value]  →  Target: [value]  →  Timeframe: [date]

4.3 Guardrail Metrics (Must Not Degrade)
────────────────────────────────────────────────────────────────
┌────────────────────────────┬──────────┬─────────────────────┐
│ Metric                     │ Current  │ Acceptable Range    │
├────────────────────────────┼──────────┼─────────────────────┤
│ [e.g., Page load time]     │ [value]  │ [must stay below X] │
│ [e.g., Error rate]         │ [value]  │ [must stay below X] │
│ [e.g., Accessibility score]│ [value]  │ [must stay above X] │
└────────────────────────────┴──────────┴─────────────────────┘


═══════════════════════════════════════════════════════════════
5. PRODUCT SCOPE
═══════════════════════════════════════════════════════════════

5.1 In Scope (This Release)
────────────────────────────────────────────────────────────────
• [Feature/capability 1]
• [Feature/capability 2]
• [Feature/capability 3]

5.2 Out of Scope (Explicitly Excluded)
────────────────────────────────────────────────────────────────
┌────────────────────────────┬──────────────────────────────────┐
│ Item                       │ Reason for Exclusion             │
├────────────────────────────┼──────────────────────────────────┤
│ [Feature X]                │ [Deferred to Phase 2]            │
│ [Integration Y]            │ [Pending partner agreement]      │
│ [Platform Z]               │ [Insufficient user demand]       │
└────────────────────────────┴──────────────────────────────────┘

5.3 Future Considerations (Backlog)
────────────────────────────────────────────────────────────────
• Phase 2: [Items planned for next release]
• Phase 3: [Longer-term vision items]


═══════════════════════════════════════════════════════════════
6. FEATURE REQUIREMENTS (Prioritized)
═══════════════════════════════════════════════════════════════

6.1 Feature Matrix
────────────────────────────────────────────────────────────────
┌────────┬───────────────────────┬────────┬──────┬────────────┐
│ ID     │ Feature               │ MoSCoW │ OBJ  │ Effort     │
├────────┼───────────────────────┼────────┼──────┼────────────┤
│ F-001  │ [Feature name]        │ Must   │ OBJ-1│ [S/M/L/XL] │
│ F-002  │ [Feature name]        │ Must   │ OBJ-1│ [S/M/L/XL] │
│ F-003  │ [Feature name]        │ Should │ OBJ-2│ [S/M/L/XL] │
│ F-004  │ [Feature name]        │ Could  │ OBJ-2│ [S/M/L/XL] │
│ F-005  │ [Feature name]        │ Won't  │ --   │ --         │
└────────┴───────────────────────┴────────┴──────┴────────────┘

OBJ = Objective traceability (link back to Section 4)
MoSCoW = @ba-prioritization output

6.2 Feature Details
────────────────────────────────────────────────────────────────

Feature F-001: [Feature Name]
┌─────────────────┬────────────────────────────────────────────┐
│ Description     │ [What this feature does — user outcome]   │
├─────────────────┼────────────────────────────────────────────┤
│ User Story      │ As a [user], I want [action]              │
│                 │ so that [benefit]                          │
├─────────────────┼────────────────────────────────────────────┤
│ Acceptance      │ GIVEN [precondition]                       │
│ Criteria        │ WHEN [action]                              │
│ (Gherkin)       │ THEN [expected result]                     │
├─────────────────┼────────────────────────────────────────────┤
│ Edge Cases      │ • [Edge case 1]: [Expected behavior]      │
│                 │ • [Edge case 2]: [Expected behavior]      │
├─────────────────┼────────────────────────────────────────────┤
│ Dependencies    │ [F-xxx, API-xxx, or external system]      │
├─────────────────┼────────────────────────────────────────────┤
│ Design Ref      │ [Link to Figma/Stitch screen]             │
└─────────────────┴────────────────────────────────────────────┘

[Repeat for each feature F-002, F-003, ...]


═══════════════════════════════════════════════════════════════
7. USER FLOWS & WIREFRAME REFERENCES
═══════════════════════════════════════════════════════════════

7.1 Core User Flows
────────────────────────────────────────────────────────────────
Flow 1: [Flow Name, e.g., "New User Registration"]

  [Start] → [Step 1] → [Decision?]
                          ├─ Yes → [Step 2a] → [End: Success]
                          └─ No  → [Step 2b] → [Error State]

Flow 2: [Flow Name]
  [Describe or link to BPMN diagram from @ba-process]

7.2 Wireframes / Prototypes
────────────────────────────────────────────────────────────────
┌─────────────────────┬──────────────┬─────────────────────────┐
│ Screen              │ Tool         │ Link                    │
├─────────────────────┼──────────────┼─────────────────────────┤
│ Login               │ Stitch MCP   │ [project/screen URL]    │
│ Dashboard           │ Figma        │ [figma URL]             │
│ Settings            │ v0           │ [v0 URL]                │
└─────────────────────┴──────────────┴─────────────────────────┘

See: docs/design-prototype-guide.md for Stitch MCP and 
Figma MCP workflow instructions.


═══════════════════════════════════════════════════════════════
8. NON-FUNCTIONAL REQUIREMENTS
═══════════════════════════════════════════════════════════════

8.1 Performance
────────────────────────────────────────────────────────────────
┌───────────────────────────┬──────────────────────────────────┐
│ Metric                    │ Target                           │
├───────────────────────────┼──────────────────────────────────┤
│ Page Load Time (P95)      │ < [X] seconds                    │
│ API Response Time (P95)   │ < [X] ms                         │
│ Concurrent Users          │ [X] simultaneous                 │
│ Uptime SLA                │ [X]% monthly                     │
└───────────────────────────┴──────────────────────────────────┘

8.2 Security & Privacy
────────────────────────────────────────────────────────────────
• Authentication: [Method — OAuth2, SSO, MFA]
• Data encryption: [At-rest, in-transit]
• Compliance: [GDPR, SOC2, HIPAA, PDPA, etc.]
• Data retention: [Policy]

8.3 Accessibility
────────────────────────────────────────────────────────────────
• Target: WCAG 2.1 Level [AA/AAA]
• Screen reader support: [Yes/No]
• Keyboard navigation: [Full/Partial]

8.4 AI-Specific Considerations (if applicable)
────────────────────────────────────────────────────────────────
┌───────────────────────────┬──────────────────────────────────┐
│ Parameter                 │ Target                           │
├───────────────────────────┼──────────────────────────────────┤
│ Model Accuracy            │ [e.g., Precision > 90%]          │
│ Inference Latency (P95)   │ < [X] ms                         │
│ Hallucination Rate        │ < [X]%                           │
│ Data Requirements         │ [Training data size/quality]     │
│ Fallback Behavior         │ [What happens when model fails]  │
│ Bias Mitigation           │ [Approach]                       │
└───────────────────────────┴──────────────────────────────────┘

Full NFR analysis: run @ba-nfr for ISO 25010 breakdown.


═══════════════════════════════════════════════════════════════
9. RELEASE CRITERIA / DEFINITION OF DONE
═══════════════════════════════════════════════════════════════

9.1 Release Readiness Checklist
────────────────────────────────────────────────────────────────
┌───┬──────────────────────────────────┬───────────┬───────────┐
│ # │ Criterion                        │ Required  │ Status    │
├───┼──────────────────────────────────┼───────────┼───────────┤
│ 1 │ All Must features implemented    │ Yes       │ [ ]       │
│ 2 │ All AC verified (manual/auto)    │ Yes       │ [ ]       │
│ 3 │ UAT passed with target personas  │ Yes       │ [ ]       │
│ 4 │ Performance targets met          │ Yes       │ [ ]       │
│ 5 │ Security review completed        │ Yes       │ [ ]       │
│ 6 │ Accessibility audit passed       │ Depends   │ [ ]       │
│ 7 │ Documentation updated            │ Yes       │ [ ]       │
│ 8 │ Rollback plan documented         │ Yes       │ [ ]       │
│ 9 │ Monitoring & alerts configured   │ Yes       │ [ ]       │
│10 │ Stakeholder sign-off obtained    │ Yes       │ [ ]       │
└───┴──────────────────────────────────┴───────────┴───────────┘

9.2 Rollback Criteria
────────────────────────────────────────────────────────────────
[Conditions that trigger automatic rollback]
• Error rate exceeds [X]%
• Key metric drops below [threshold]
• [Critical user flow] failure rate > [X]%


═══════════════════════════════════════════════════════════════
10. DEPENDENCIES, ASSUMPTIONS & CONSTRAINTS
═══════════════════════════════════════════════════════════════

10.1 Dependencies
────────────────────────────────────────────────────────────────
┌─────────┬─────────────────────┬──────────────┬───────────────┐
│ ID      │ Dependency          │ Owner        │ Due Date      │
├─────────┼─────────────────────┼──────────────┼───────────────┤
│ DEP-001 │ [API from Team X]   │ [Team X]     │ [Date]        │
│ DEP-002 │ [3rd party service] │ [Vendor]     │ [Date]        │
└─────────┴─────────────────────┴──────────────┴───────────────┘

10.2 Assumptions
────────────────────────────────────────────────────────────────
┌─────────┬──────────────────────────┬──────────────────────────┐
│ ID      │ Assumption               │ If False, Then           │
├─────────┼──────────────────────────┼──────────────────────────┤
│ ASM-001 │ [Assumption]             │ [Impact + mitigation]    │
│ ASM-002 │ [Assumption]             │ [Impact + mitigation]    │
└─────────┴──────────────────────────┴──────────────────────────┘

10.3 Constraints
────────────────────────────────────────────────────────────────
• Budget: [Amount or range]
• Timeline: [Fixed date or flexible]
• Technology: [Must use X stack / Must integrate with Y]
• Regulatory: [Compliance requirements]


═══════════════════════════════════════════════════════════════
11. RISKS & OPEN QUESTIONS
═══════════════════════════════════════════════════════════════

11.1 Known Risks
────────────────────────────────────────────────────────────────
┌─────────┬─────────────────┬────────┬────────┬────────────────┐
│ ID      │ Risk            │ Prob.  │ Impact │ Mitigation     │
├─────────┼─────────────────┼────────┼────────┼────────────────┤
│ RSK-001 │ [Description]   │ H/M/L  │ H/M/L  │ [Strategy]     │
│ RSK-002 │ [Description]   │ H/M/L  │ H/M/L  │ [Strategy]     │
└─────────┴─────────────────┴────────┴────────┴────────────────┘

11.2 Open Questions (To Be Resolved)
────────────────────────────────────────────────────────────────
┌─────────┬──────────────────────────┬──────────┬──────────────┐
│ ID      │ Question                 │ Owner    │ Due Date     │
├─────────┼──────────────────────────┼──────────┼──────────────┤
│ OQ-001  │ [Question]               │ [Person] │ [Date]       │
│ OQ-002  │ [Question]               │ [Person] │ [Date]       │
└─────────┴──────────────────────────┴──────────┴──────────────┘


═══════════════════════════════════════════════════════════════
12. APPENDICES
═══════════════════════════════════════════════════════════════

A. Glossary
────────────────────────────────────────────────────────────────
┌────────────────┬─────────────────────────────────────────────┐
│ Term           │ Definition                                  │
├────────────────┼─────────────────────────────────────────────┤
│ [Term]         │ [Definition]                                │
└────────────────┴─────────────────────────────────────────────┘

B. Related Documents
────────────────────────────────────────────────────────────────
• BRD: [link]
• SRS: [link]
• API Contract: [link]
• Design (Figma/Stitch): [link]

C. Change Log
────────────────────────────────────────────────────────────────
[Record significant requirement changes after approval]
┌────────────┬────────────────────────┬────────────┬──────────┐
│ Date       │ Change                 │ Reason     │ Approved │
├────────────┼────────────────────────┼────────────┼──────────┤
│ YYYY-MM-DD │ [What changed]         │ [Why]      │ [By who] │
└────────────┴────────────────────────┴────────────┴──────────┘
```

---

## PRD Quality Checklist

```
Section 1-3: Foundation
  ☐ One-liner is concrete (no buzzwords)
  ☐ Problem has quantitative evidence
  ☐ Primary persona has specific frustration + usage frequency
  ☐ Anti-personas defined (scope protection)

Section 4-5: Scope
  ☐ OKRs have baseline → target → date
  ☐ North Star metric identified
  ☐ Guardrail metrics protect existing quality
  ☐ Out-of-scope items have documented reasons

Section 6-7: Features
  ☐ Each feature has MoSCoW priority
  ☐ Each feature traces to an Objective (OBJ column)
  ☐ Acceptance Criteria in Gherkin format
  ☐ Edge cases documented per feature
  ☐ Wireframe/prototype links present

Section 8-9: Quality
  ☐ Performance targets have P95 thresholds
  ☐ Security requirements match compliance needs
  ☐ AI-specific section filled (if applicable)
  ☐ Release criteria checklist complete
  ☐ Rollback criteria defined

Section 10-12: Risk
  ☐ Dependencies have owners and dates
  ☐ Assumptions have "If False" contingencies
  ☐ Open questions have owners and deadlines
  ☐ Glossary covers domain-specific terms
```

---

## Related BA-Kit Agents

| Step | Agent | Action |
|------|-------|--------|
| Problem & Users | `@ba-elicitation` | Interview stakeholders, define personas |
| Feature Priority | `@ba-prioritization` | Apply MoSCoW/WSJF to feature list |
| Acceptance Criteria | `@ba-writing` | Gherkin AC per feature |
| NFR | `@ba-nfr` | ISO 25010 breakdown |
| User Flows | `@ba-process` | BPMN diagrams |
| Wireframes | Stitch MCP / Figma MCP | See design-prototype-guide.md |
| ROI/Business Case | `@ba-solution` | Python-verified calculations |
| Validation | `@ba-validation` | Health Score check on complete PRD |
| Publish | `@ba-confluence` | Push to Confluence |
| Tickets | `@ba-jira` | Create Jira epics/stories from features |

### PRD Power Combo

```
@ba-elicitation → @ba-writing (PRD draft) → @ba-prioritization (MoSCoW) 
  → @ba-nfr (NFR section) → @ba-validation (quality check) 
  → @ba-jira (create tickets)
```
