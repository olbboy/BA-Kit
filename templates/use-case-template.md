# 🟢 SKILL-10: USE CASE TEMPLATE
## Template Skill - Use Case Specification

---

## 📌 SKILL METADATA

| Attribute | Value |
|-----------|-------|
| **Template ID** | TMPL-UC |
| **Category** | 🟢 Template |
| **Load When** | Documenting functional requirements as use cases |
| **Dependencies** | @ba-writing, @ba-process |
| **Output** | Complete Use Case Specification document |

---

## 🎯 WHEN TO USE USE CASE SPECIFICATION

| Use Use Case When | Don't Use Use Case When |
|-------------------|------------------------|
| ✓ Documenting actor-system interactions | ✗ High-level executive overview needed (use BRD) |
| ✓ Capturing goal-oriented functional flows | ✗ Data structure documentation (use Data Dictionary) |
| ✓ Complex multi-step business processes | ✗ Simple CRUD with no branching logic |
| ✓ Multiple actors with different goals | ✗ Agile sprints (use User Stories instead) |
| ✓ Need to trace requirements to test cases | ✗ Non-functional requirements (use NFR doc) |

---

## 📋 USE CASE TEMPLATE

```
═══════════════════════════════════════════════════════════════
                   USE CASE SPECIFICATION
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

═══════════════════════════════════════════════════════════════
USE CASE: [UC-XXX]
═══════════════════════════════════════════════════════════════

1. IDENTIFICATION
────────────────────────────────────────────────────────────────
┌────────────────────┬───────────────────────────────────────┐
│ UC ID              │ UC-[XXX]                              │
│ Name               │ [Verb + Noun, e.g., Submit Loan App]  │
│ Primary Actor      │ [Who initiates this use case]         │
│ Scope              │ [System or subsystem in scope]        │
│ Level              │ [User Goal / Summary / Sub-function]  │
│ Priority           │ [Must/Should/Could]                   │
└────────────────────┴───────────────────────────────────────┘

2. STAKEHOLDERS & INTERESTS
────────────────────────────────────────────────────────────────
┌──────────────────────┬──────────────────────────────────────┐
│ Stakeholder          │ Interest / Goal                      │
├──────────────────────┼──────────────────────────────────────┤
│ [Primary Actor]      │ [What they want to achieve]          │
│ [Secondary Actor]    │ [What they want to achieve]          │
│ [System/Service]     │ [What it provides/needs]             │
└──────────────────────┴──────────────────────────────────────┘

3. CONDITIONS
────────────────────────────────────────────────────────────────
Preconditions (must be true before use case begins):
  • [Condition 1 - e.g., User is authenticated]
  • [Condition 2 - e.g., Record exists in system]
  • [Condition 3]

Postconditions - Success Guarantee:
  • [State of system after successful completion]
  • [Side effects: notifications sent, records updated]

Postconditions - Minimal Guarantee (even on failure):
  • [What is always true after any execution path]
  • [e.g., No partial data committed without rollback]

4. MAIN SUCCESS SCENARIO
────────────────────────────────────────────────────────────────
Step  Actor        Action / System Response
────  ──────────   ──────────────────────────────────────────
 1.   [Actor]      [Initiates - e.g., navigates to page]
 2.   System       [System response / display]
 3.   [Actor]      [Provides input / selection]
 4.   System       [Validates input]
 5.   [Actor]      [Confirms / submits]
 6.   System       [Processes and stores data]
 7.   System       [Notifies actor of success]

5. EXTENSIONS / ALTERNATIVE FLOWS
────────────────────────────────────────────────────────────────
[Step]a. [Condition that triggers alternative]
  1.    [System detects condition]
  2.    [System response or actor action]
  3.    [Resume at step X / End use case]

[Step]b. [Another alternative condition]
  1.    [Response]
  2.    [Resolution or exit]

*a. [At any time] - [e.g., Actor cancels operation]
  1.    System discards unsaved data
  2.    System returns actor to previous screen
  3.    Use case ends

6. BUSINESS RULES REFERENCED
────────────────────────────────────────────────────────────────
┌─────────┬──────────────────────────────────────────────────┐
│ BR-ID   │ Rule Description                                 │
├─────────┼──────────────────────────────────────────────────┤
│ BR-[XX] │ [Rule that applies to this use case]             │
│ BR-[XX] │ [Rule that applies to this use case]             │
└─────────┴──────────────────────────────────────────────────┘

7. DATA REQUIREMENTS
────────────────────────────────────────────────────────────────
Input Data:
┌─────────────────┬──────────────┬──────────────────────────┐
│ Field           │ Type         │ Validation               │
├─────────────────┼──────────────┼──────────────────────────┤
│ [Field Name]    │ [String/Int] │ [Required, max 100 chars]│
│ [Field Name]    │ [Date]       │ [Must not be past date]  │
└─────────────────┴──────────────┴──────────────────────────┘

Output Data:
┌─────────────────┬──────────────┬──────────────────────────┐
│ Field           │ Type         │ Description              │
├─────────────────┼──────────────┼──────────────────────────┤
│ [Field Name]    │ [Type]       │ [What it represents]     │
└─────────────────┴──────────────┴──────────────────────────┘

8. UI REQUIREMENTS
────────────────────────────────────────────────────────────────
┌──────────────────┬──────────────────────────────────────────┐
│ Screen Reference │ [Wireframe ID / Screen Name]             │
│ Key UI Elements  │ [Form fields, buttons, validation msgs]  │
│ Navigation       │ [Entry point → flow → exit]              │
│ Accessibility    │ [WCAG level / special requirements]      │
└──────────────────┴──────────────────────────────────────────┘

9. NON-FUNCTIONAL CONSTRAINTS
────────────────────────────────────────────────────────────────
  • Performance : [e.g., Response within 2 seconds]
  • Security    : [e.g., Requires MFA for financial actions]
  • Availability: [e.g., Must work 24/7 including maintenance]
  • Audit       : [e.g., All actions logged with user + timestamp]

10. OPEN QUESTIONS
────────────────────────────────────────────────────────────────
┌────────┬────────────────────────────────┬──────────┬────────┐
│ Q-ID   │ Question                       │ Owner    │ Due    │
├────────┼────────────────────────────────┼──────────┼────────┤
│ Q-001  │ [Unresolved question]          │ [Name]   │ [Date] │
│ Q-002  │ [Unresolved question]          │ [Name]   │ [Date] │
└────────┴────────────────────────────────┴──────────┴────────┘
```

---

## ✅ USE CASE QUALITY CHECKLIST

```
☐ UC ID follows naming convention (UC-XXX)
☐ Primary actor clearly identified
☐ Scope and level defined
☐ All stakeholders and interests documented
☐ Preconditions are verifiable, not vague
☐ Main scenario written in active voice (actor does X)
☐ Each step is one action (not compound)
☐ All exception paths covered in extensions
☐ Business rules referenced by ID
☐ Input data fields match UI wireframe
☐ Non-functional constraints specified
☐ Open questions tracked with owner and due date
☐ Use case traceable to business requirement
```

---

## 🔗 RELATED SKILLS

| After Use Case... | Load |
|-------------------|------|
| Write test scenarios | @ba-process (Test Case Template) |
| Create UI specs | @ba-writing (Wireframe notes) |
| Build data model | @ba-writing (Data Dictionary) |

---

*Use this template to document complete, unambiguous use cases that drive development and testing.*
