# 🟢 SKILL-09: BRD TEMPLATE
## Template Skill - Business Requirements Document

---

## 📌 SKILL METADATA

| Attribute | Value |
|-----------|-------|
| **Template ID** | TMPL-BRD |
| **Category** | 🟢 Template |
| **Load When** | Creating Business Requirements Document |
| **Dependencies** | @ba-identity, @ba-elicitation, @ba-writing |
| **Output** | Complete BRD document |

---

## 🎯 WHEN TO USE BRD

| Use BRD When | Don't Use BRD When |
|--------------|-------------------|
| ✓ Starting new project/initiative | ✗ Already have approved BRD |
| ✓ Need executive approval | ✗ Small enhancements only |
| ✓ Significant investment required | ✗ Technical specs needed (use SRS) |
| ✓ Multiple stakeholder alignment | ✗ Agile team (use User Stories) |
| ✓ Business case justification | ✗ Detailed functional specs (use FRD) |

---

## 📋 BRD TEMPLATE

```
═══════════════════════════════════════════════════════════════
                BUSINESS REQUIREMENTS DOCUMENT
                      [Project Name]
═══════════════════════════════════════════════════════════════

Document Control
────────────────────────────────────────────────────────────────
Version: [X.Y]
Date: [YYYY-MM-DD]
Author: [Name]
Status: [Draft/Review/Approved]

Version History
┌─────────┬────────────┬──────────┬─────────────────────────────┐
│ Version │ Date       │ Author   │ Changes                     │
├─────────┼────────────┼──────────┼─────────────────────────────┤
│ 0.1     │ YYYY-MM-DD │ [Name]   │ Initial draft               │
│ 1.0     │ YYYY-MM-DD │ [Name]   │ Approved version            │
└─────────┴────────────┴──────────┴─────────────────────────────┘

Approval
┌──────────────────┬────────────┬─────────────┬────────────────┐
│ Name             │ Role       │ Signature   │ Date           │
├──────────────────┼────────────┼─────────────┼────────────────┤
│                  │ Sponsor    │             │                │
│                  │ PM         │             │                │
│                  │ Business   │             │                │
└──────────────────┴────────────┴─────────────┴────────────────┘

═══════════════════════════════════════════════════════════════
                    TABLE OF CONTENTS
═══════════════════════════════════════════════════════════════
1. Executive Summary
2. Project Background
3. Business Objectives
4. Current State Analysis
5. Proposed Solution
6. Stakeholder Analysis
7. Business Requirements
8. Scope
9. Constraints & Assumptions
10. Risk Assessment
11. Success Criteria
12. Timeline & Milestones
13. Budget Overview
14. Appendices

═══════════════════════════════════════════════════════════════
1. EXECUTIVE SUMMARY
═══════════════════════════════════════════════════════════════

[2-3 paragraphs summarizing:]
• Business problem/opportunity
• Proposed solution
• Expected benefits
• Investment required
• Key success metrics

═══════════════════════════════════════════════════════════════
2. PROJECT BACKGROUND
═══════════════════════════════════════════════════════════════

2.1 Business Context
────────────────────────────────────────────────────────────────
[Describe the business context, market conditions, or 
organizational situation driving this initiative]

2.2 Problem Statement
────────────────────────────────────────────────────────────────
[Clear, concise statement of the business problem]

Format: [Stakeholder] experiences [problem] which results in 
[business impact].

2.3 Opportunity Statement
────────────────────────────────────────────────────────────────
[If opportunity-driven, describe the opportunity]

═══════════════════════════════════════════════════════════════
3. BUSINESS OBJECTIVES
═══════════════════════════════════════════════════════════════

3.1 Primary Objectives
────────────────────────────────────────────────────────────────
┌────────┬─────────────────────────────────┬───────────────────┐
│ ID     │ Objective                       │ Measure           │
├────────┼─────────────────────────────────┼───────────────────┤
│ OBJ-01 │ [SMART objective]               │ [How measured]    │
│ OBJ-02 │ [SMART objective]               │ [How measured]    │
│ OBJ-03 │ [SMART objective]               │ [How measured]    │
└────────┴─────────────────────────────────┴───────────────────┘

3.2 Strategic Alignment
────────────────────────────────────────────────────────────────
[How does this align with organizational strategy?]

═══════════════════════════════════════════════════════════════
4. CURRENT STATE ANALYSIS
═══════════════════════════════════════════════════════════════

4.1 Current Process/System
────────────────────────────────────────────────────────────────
[Description or diagram of current state]

4.2 Pain Points
────────────────────────────────────────────────────────────────
┌────────┬─────────────────────────────────┬───────────────────┐
│ ID     │ Pain Point                      │ Impact            │
├────────┼─────────────────────────────────┼───────────────────┤
│ PP-01  │ [Description]                   │ [Business impact] │
│ PP-02  │ [Description]                   │ [Business impact] │
└────────┴─────────────────────────────────┴───────────────────┘

4.3 Gap Analysis
────────────────────────────────────────────────────────────────
[What's missing between current and desired state?]

═══════════════════════════════════════════════════════════════
5. PROPOSED SOLUTION
═══════════════════════════════════════════════════════════════

5.1 Solution Overview
────────────────────────────────────────────────────────────────
[High-level description of proposed solution]

5.2 Future State Vision
────────────────────────────────────────────────────────────────
[Description or diagram of desired future state]

5.3 Expected Benefits
────────────────────────────────────────────────────────────────
┌────────┬─────────────────────────────────┬───────────────────┐
│ Type   │ Benefit                         │ Estimated Value   │
├────────┼─────────────────────────────────┼───────────────────┤
│ Quant. │ [e.g., Reduce processing time]  │ [e.g., 30%]       │
│ Quant. │ [e.g., Increase revenue]        │ [e.g., $500K/yr]  │
│ Qual.  │ [e.g., Improve satisfaction]    │ [e.g., NPS +20]   │
└────────┴─────────────────────────────────┴───────────────────┘

5.4 Solution Alternatives Considered
────────────────────────────────────────────────────────────────
┌──────────────┬───────────────────┬──────────────────────────┐
│ Alternative  │ Pros              │ Cons / Why Not Selected  │
├──────────────┼───────────────────┼──────────────────────────┤
│ Option A     │                   │                          │
│ Option B     │                   │                          │
│ Do Nothing   │                   │                          │
└──────────────┴───────────────────┴──────────────────────────┘

═══════════════════════════════════════════════════════════════
6. STAKEHOLDER ANALYSIS
═══════════════════════════════════════════════════════════════

6.1 Stakeholder Register
────────────────────────────────────────────────────────────────
┌──────────────┬────────────┬──────────────┬──────────────────┐
│ Stakeholder  │ Role       │ Interest     │ Influence        │
├──────────────┼────────────┼──────────────┼──────────────────┤
│ [Name/Group] │ [Role]     │ [H/M/L]      │ [H/M/L]          │
└──────────────┴────────────┴──────────────┴──────────────────┘

6.2 User Groups
────────────────────────────────────────────────────────────────
[Describe primary user groups who will use the solution]

═══════════════════════════════════════════════════════════════
7. BUSINESS REQUIREMENTS
═══════════════════════════════════════════════════════════════

7.1 High-Level Requirements
────────────────────────────────────────────────────────────────
┌────────┬─────────────────────────────────┬───────────────────┐
│ BR-ID  │ Requirement                     │ Priority          │
├────────┼─────────────────────────────────┼───────────────────┤
│ BR-001 │ The solution shall [capability] │ Must              │
│        │ to achieve [business goal]      │                   │
├────────┼─────────────────────────────────┼───────────────────┤
│ BR-002 │ The solution shall [capability] │ Should            │
│        │ to achieve [business goal]      │                   │
├────────┼─────────────────────────────────┼───────────────────┤
│ BR-003 │ The solution shall [capability] │ Could             │
│        │ to achieve [business goal]      │                   │
└────────┴─────────────────────────────────┴───────────────────┘

═══════════════════════════════════════════════════════════════
8. SCOPE
═══════════════════════════════════════════════════════════════

8.1 In Scope
────────────────────────────────────────────────────────────────
• [Item 1]
• [Item 2]
• [Item 3]

8.2 Out of Scope
────────────────────────────────────────────────────────────────
• [Item 1] - [Reason]
• [Item 2] - [Reason]

8.3 Future Considerations
────────────────────────────────────────────────────────────────
• [Items for future phases]

═══════════════════════════════════════════════════════════════
9. CONSTRAINTS & ASSUMPTIONS
═══════════════════════════════════════════════════════════════

9.1 Constraints
────────────────────────────────────────────────────────────────
┌────────┬─────────────────────────────────┬───────────────────┐
│ ID     │ Constraint                      │ Impact            │
├────────┼─────────────────────────────────┼───────────────────┤
│ C-001  │ Budget limited to $X            │ Scope limitation  │
│ C-002  │ Must go live by [date]          │ Timeline fixed    │
│ C-003  │ Must integrate with [system]    │ Technical dep.    │
└────────┴─────────────────────────────────┴───────────────────┘

9.2 Assumptions
────────────────────────────────────────────────────────────────
┌────────┬─────────────────────────────────┬───────────────────┐
│ ID     │ Assumption                      │ If False          │
├────────┼─────────────────────────────────┼───────────────────┤
│ A-001  │ [Assumption]                    │ [Impact]          │
│ A-002  │ [Assumption]                    │ [Impact]          │
└────────┴─────────────────────────────────┴───────────────────┘

═══════════════════════════════════════════════════════════════
10. RISK ASSESSMENT
═══════════════════════════════════════════════════════════════

┌────────┬────────────────┬────────┬────────┬─────────────────┐
│ ID     │ Risk           │ Prob.  │ Impact │ Mitigation      │
├────────┼────────────────┼────────┼────────┼─────────────────┤
│ R-001  │ [Description]  │ H/M/L  │ H/M/L  │ [Strategy]      │
│ R-002  │ [Description]  │ H/M/L  │ H/M/L  │ [Strategy]      │
└────────┴────────────────┴────────┴────────┴─────────────────┘

═══════════════════════════════════════════════════════════════
11. SUCCESS CRITERIA
═══════════════════════════════════════════════════════════════

┌────────┬─────────────────────────┬──────────────────────────┐
│ ID     │ Criterion               │ Target / Measure         │
├────────┼─────────────────────────┼──────────────────────────┤
│ SC-001 │ [Success metric]        │ [Specific target]        │
│ SC-002 │ [Success metric]        │ [Specific target]        │
└────────┴─────────────────────────┴──────────────────────────┘

═══════════════════════════════════════════════════════════════
12. TIMELINE & MILESTONES
═══════════════════════════════════════════════════════════════

┌─────────────────────────┬────────────────┬──────────────────┐
│ Milestone               │ Target Date    │ Dependencies     │
├─────────────────────────┼────────────────┼──────────────────┤
│ BRD Approval            │ [Date]         │ -                │
│ Requirements Complete   │ [Date]         │ BRD Approval     │
│ Design Complete         │ [Date]         │ Requirements     │
│ Development Complete    │ [Date]         │ Design           │
│ UAT Complete            │ [Date]         │ Development      │
│ Go-Live                 │ [Date]         │ UAT              │
└─────────────────────────┴────────────────┴──────────────────┘

═══════════════════════════════════════════════════════════════
13. BUDGET OVERVIEW
═══════════════════════════════════════════════════════════════

13.1 Cost Estimate
────────────────────────────────────────────────────────────────
┌─────────────────────────┬────────────────────────────────────┐
│ Category                │ Estimated Cost                     │
├─────────────────────────┼────────────────────────────────────┤
│ Development             │ $                                  │
│ Infrastructure          │ $                                  │
│ Licenses                │ $                                  │
│ Training                │ $                                  │
│ Contingency             │ $                                  │
├─────────────────────────┼────────────────────────────────────┤
│ TOTAL                   │ $                                  │
└─────────────────────────┴────────────────────────────────────┘

13.2 ROI Analysis
────────────────────────────────────────────────────────────────
[Brief ROI calculation or reference to business case]

═══════════════════════════════════════════════════════════════
14. APPENDICES
═══════════════════════════════════════════════════════════════

A. Glossary
B. References
C. Supporting Documents
D. Process Diagrams (if any)
```

---

## ✅ BRD QUALITY CHECKLIST

```
☐ Executive summary is compelling
☐ Problem/opportunity clearly stated
☐ Objectives are SMART
☐ Current state documented
☐ Benefits are quantified where possible
☐ Stakeholders identified
☐ Scope clearly defined (in/out)
☐ Constraints and assumptions listed
☐ Risks identified with mitigations
☐ Success criteria measurable
☐ Timeline realistic
☐ Budget aligned with scope
☐ Approval signatures obtained
```

---

## 🔗 RELATED SKILLS

| After BRD... | Load |
|--------------|------|
| Detail requirements | @ba-writing (SRS/FRD) |
| Agile breakdown | @ba-writing (User Stories) |
| Prioritize features | @ba-prioritization |

---

*Use this template to create comprehensive BRDs that secure stakeholder buy-in.*
