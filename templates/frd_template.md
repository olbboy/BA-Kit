# 🟢 SKILL-11: FRD TEMPLATE
## Template Skill - Functional Requirements Document

---

## 📌 SKILL METADATA

| Attribute | Value |
|-----------|-------|
| **Template ID** | TMPL-FRD |
| **Category** | 🟢 Template |
| **Load When** | Detailed functional specifications needed |
| **Dependencies** | @ba-writing, @ba-process, @ba-nfr |
| **Output** | Complete FRD document |

---

## 🎯 SRS vs FRD: WHEN TO USE WHICH

| Aspect | SRS | FRD |
|--------|-----|-----|
| **Scope** | Entire system (FR + NFR) | Functional details only |
| **Audience** | All stakeholders | Dev & QA primarily |
| **Depth** | Moderate | Very detailed |
| **Format** | IEEE/ISO standard | Flexible, practical |
| **Best For** | Contract, compliance | Implementation guide |

**Use FRD when:**
- ✓ Need deep functional detail for developers
- ✓ Module-by-module specification
- ✓ Working with UI mockups
- ✓ Detailed business rules

---

## 📋 FRD TEMPLATE

```
═══════════════════════════════════════════════════════════════
            FUNCTIONAL REQUIREMENTS DOCUMENT
                    [Module/Feature Name]
═══════════════════════════════════════════════════════════════

Document Control
────────────────────────────────────────────────────────────────
Document ID: [Project]-FRD-[Module]-[Version]
Version: [X.Y.Z]
Date: [YYYY-MM-DD]
Author: [Name]
Status: [Draft/Review/Approved]

Version History
┌─────────┬────────────┬──────────┬─────────────────────────────┐
│ Version │ Date       │ Author   │ Changes                     │
├─────────┼────────────┼──────────┼─────────────────────────────┤
│         │            │          │                             │
└─────────┴────────────┴──────────┴─────────────────────────────┘

Approval
┌──────────────────┬────────────┬─────────────┬────────────────┐
│ Name             │ Role       │ Signature   │ Date           │
├──────────────────┼────────────┼─────────────┼────────────────┤
│                  │ Product    │             │                │
│                  │ Tech Lead  │             │                │
│                  │ QA Lead    │             │                │
└──────────────────┴────────────┴─────────────┴────────────────┘

═══════════════════════════════════════════════════════════════
                    TABLE OF CONTENTS
═══════════════════════════════════════════════════════════════
1. Introduction
2. Module Overview
3. User Roles & Permissions
4. Functional Requirements
5. Business Rules
6. Data Requirements
7. Integration Requirements
8. UI Specifications
9. Reporting Requirements
10. Appendices

═══════════════════════════════════════════════════════════════
1. INTRODUCTION
═══════════════════════════════════════════════════════════════

1.1 Purpose
────────────────────────────────────────────────────────────────
This FRD defines the detailed functional requirements for the 
[Module Name] module of [System Name].

1.2 Scope
────────────────────────────────────────────────────────────────
This document covers:
• [Feature/Function 1]
• [Feature/Function 2]
• [Feature/Function 3]

Out of Scope:
• [Excluded item 1]
• [Excluded item 2]

1.3 References
────────────────────────────────────────────────────────────────
• BRD: [Document reference]
• SRS: [Document reference]
• UI Mockups: [Link/Location]

1.4 Glossary
────────────────────────────────────────────────────────────────
┌──────────────┬───────────────────────────────────────────────┐
│ Term         │ Definition                                    │
├──────────────┼───────────────────────────────────────────────┤
│              │                                               │
└──────────────┴───────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
2. MODULE OVERVIEW
═══════════════════════════════════════════════════════════════

2.1 Module Description
────────────────────────────────────────────────────────────────
[Describe what this module does and its business purpose]

2.2 Module Context
────────────────────────────────────────────────────────────────
[How this module fits with other modules]

┌─────────────────────────────────────────────────────────────┐
│                    MODULE CONTEXT                           │
│                                                             │
│    ┌──────────┐      ┌──────────────┐      ┌──────────┐    │
│    │ Module A │ ───► │ THIS MODULE  │ ───► │ Module B │    │
│    └──────────┘      └──────────────┘      └──────────┘    │
│                            │                               │
│                            ▼                               │
│                      ┌──────────┐                          │
│                      │ Module C │                          │
│                      └──────────┘                          │
└─────────────────────────────────────────────────────────────┘

2.3 Process Flow Overview
────────────────────────────────────────────────────────────────
[High-level process flow diagram]

═══════════════════════════════════════════════════════════════
3. USER ROLES & PERMISSIONS
═══════════════════════════════════════════════════════════════

3.1 Roles in This Module
────────────────────────────────────────────────────────────────
┌──────────────┬─────────────────────────────────────────────┐
│ Role         │ Description                                 │
├──────────────┼─────────────────────────────────────────────┤
│ [Role 1]     │ [What this role does in this module]        │
│ [Role 2]     │ [What this role does in this module]        │
└──────────────┴─────────────────────────────────────────────┘

3.2 Permission Matrix
────────────────────────────────────────────────────────────────
┌──────────────┬────────┬────────┬────────┬────────┬─────────┐
│ Function     │ Admin  │ Manager│ User   │ Viewer │ Guest   │
├──────────────┼────────┼────────┼────────┼────────┼─────────┤
│ Create       │   ✓    │   ✓    │   ✓    │   ✗    │   ✗     │
│ Read         │   ✓    │   ✓    │   ✓    │   ✓    │   ✓     │
│ Update       │   ✓    │   ✓    │   Own  │   ✗    │   ✗     │
│ Delete       │   ✓    │   ✓    │   ✗    │   ✗    │   ✗     │
│ Approve      │   ✓    │   ✓    │   ✗    │   ✗    │   ✗     │
│ Export       │   ✓    │   ✓    │   ✓    │   ✓    │   ✗     │
└──────────────┴────────┴────────┴────────┴────────┴─────────┘

═══════════════════════════════════════════════════════════════
4. FUNCTIONAL REQUIREMENTS
═══════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────
4.1 FUNCTION: [Function Name]
────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────┐
│ FR-[MOD]-001: [Requirement Title]                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ DESCRIPTION:                                                │
│ The system SHALL [detailed action description]              │
│ WHEN [trigger/condition]                                    │
│ SO THAT [business value/purpose].                           │
│                                                             │
│ ─────────────────────────────────────────────────────────── │
│ DETAILED SPECIFICATIONS:                                    │
│                                                             │
│ Input:                                                      │
│ ┌────────────┬──────────┬───────────┬─────────────────────┐ │
│ │ Field      │ Type     │ Required  │ Validation          │ │
│ ├────────────┼──────────┼───────────┼─────────────────────┤ │
│ │ [field1]   │ String   │ Yes       │ Max 100 chars       │ │
│ │ [field2]   │ Integer  │ Yes       │ Range: 1-999        │ │
│ │ [field3]   │ Date     │ No        │ Future dates only   │ │
│ └────────────┴──────────┴───────────┴─────────────────────┘ │
│                                                             │
│ Processing:                                                 │
│ 1. [Step 1 description]                                     │
│ 2. [Step 2 description]                                     │
│ 3. [Step 3 description]                                     │
│                                                             │
│ Output:                                                     │
│ • [Output 1]: [Description]                                 │
│ • [Output 2]: [Description]                                 │
│                                                             │
│ ─────────────────────────────────────────────────────────── │
│ ACCEPTANCE CRITERIA:                                        │
│                                                             │
│ Scenario 1: [Happy Path]                                    │
│ Given [precondition]                                        │
│ When [action]                                               │
│ Then [expected result]                                      │
│ And [additional result]                                     │
│                                                             │
│ Scenario 2: [Validation Error]                              │
│ Given [precondition]                                        │
│ When [invalid action]                                       │
│ Then [error handling]                                       │
│                                                             │
│ Scenario 3: [Edge Case]                                     │
│ Given [edge condition]                                      │
│ When [action]                                               │
│ Then [expected behavior]                                    │
│                                                             │
│ ─────────────────────────────────────────────────────────── │
│ UI REFERENCE: [Screen name / Mockup link]                   │
│                                                             │
│ BUSINESS RULES: BR-001, BR-003                              │
│                                                             │
│ PRIORITY: Must                                              │
│ SOURCE: [Stakeholder/Document]                              │
│ TRACE: BR-XXX → FR-[MOD]-001 → TC-XXX                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘

[Repeat for each functional requirement]

────────────────────────────────────────────────────────────────
4.2 FUNCTION: [Function Name]
────────────────────────────────────────────────────────────────
[Repeat structure]

═══════════════════════════════════════════════════════════════
5. BUSINESS RULES
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│ BR-001: [Business Rule Name]                                │
├─────────────────────────────────────────────────────────────┤
│ Description:                                                │
│ [Clear statement of the business rule]                      │
│                                                             │
│ Condition:                                                  │
│ IF [condition] THEN [action/constraint]                     │
│                                                             │
│ Example:                                                    │
│ [Concrete example of rule application]                      │
│                                                             │
│ Exception:                                                  │
│ [Any exceptions to this rule]                               │
│                                                             │
│ Applied To: FR-[MOD]-001, FR-[MOD]-003                      │
│ Source: [Policy/Stakeholder/Regulation]                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ BR-002: [Business Rule Name]                                │
├─────────────────────────────────────────────────────────────┤
│ [Rule details...]                                           │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
6. DATA REQUIREMENTS
═══════════════════════════════════════════════════════════════

6.1 Data Entities
────────────────────────────────────────────────────────────────

ENTITY: [Entity Name]
┌─────────────────────────────────────────────────────────────┐
│ Description: [What this entity represents]                  │
│                                                             │
│ Attributes:                                                 │
│ ┌────────────────┬──────────┬───────┬─────────────────────┐ │
│ │ Attribute      │ Type     │ Null? │ Description         │ │
│ ├────────────────┼──────────┼───────┼─────────────────────┤ │
│ │ id             │ UUID     │ No    │ Primary key         │ │
│ │ name           │ String   │ No    │ Display name        │ │
│ │ status         │ Enum     │ No    │ Active/Inactive     │ │
│ │ created_at     │ DateTime │ No    │ Creation timestamp  │ │
│ │ created_by     │ UUID     │ No    │ FK to User          │ │
│ └────────────────┴──────────┴───────┴─────────────────────┘ │
│                                                             │
│ Relationships:                                              │
│ • [Entity A] 1:N [This Entity]                              │
│ • [This Entity] N:M [Entity B]                              │
│                                                             │
│ Constraints:                                                │
│ • [Constraint description]                                  │
└─────────────────────────────────────────────────────────────┘

6.2 Data Validation Rules
────────────────────────────────────────────────────────────────
┌──────────────────┬─────────────────────────────────────────┐
│ Field            │ Validation Rule                         │
├──────────────────┼─────────────────────────────────────────┤
│ Email            │ Valid email format, max 255 chars       │
│ Phone            │ E.164 format, digits only               │
│ Date of Birth    │ Past date, age >= 18                    │
│ Amount           │ Positive number, max 2 decimals         │
└──────────────────┴─────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
7. INTEGRATION REQUIREMENTS
═══════════════════════════════════════════════════════════════

7.1 Internal Integrations
────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────┐
│ INT-001: Integration with [Module Name]                     │
├─────────────────────────────────────────────────────────────┤
│ Purpose: [Why this integration]                             │
│ Direction: [Inbound/Outbound/Bidirectional]                 │
│ Trigger: [When integration occurs]                          │
│                                                             │
│ Data Exchanged:                                             │
│ • [Data element 1]                                          │
│ • [Data element 2]                                          │
│                                                             │
│ Error Handling:                                             │
│ • [Error scenario]: [Handling]                              │
└─────────────────────────────────────────────────────────────┘

7.2 External Integrations
────────────────────────────────────────────────────────────────
[Reference to SI specifications in SRS or separate document]

═══════════════════════════════════════════════════════════════
8. UI SPECIFICATIONS
═══════════════════════════════════════════════════════════════

8.1 Screen: [Screen Name]
────────────────────────────────────────────────────────────────

Screen ID: UI-[MOD]-001
Mockup: [Link to mockup]

┌─────────────────────────────────────────────────────────────┐
│ Purpose:                                                    │
│ [What user accomplishes on this screen]                     │
│                                                             │
│ Access: [Who can access]                                    │
│ Navigation From: [Previous screens]                         │
│ Navigation To: [Next screens]                               │
│                                                             │
│ ─────────────────────────────────────────────────────────── │
│ UI ELEMENTS:                                                │
│                                                             │
│ ┌─────────────┬──────────┬─────────────┬─────────────────┐  │
│ │ Element     │ Type     │ Required    │ Behavior        │  │
│ ├─────────────┼──────────┼─────────────┼─────────────────┤  │
│ │ txtName     │ Text     │ Yes         │ Max 100 chars   │  │
│ │ ddlStatus   │ Dropdown │ Yes         │ Active/Inactive │  │
│ │ dtpDate     │ Date     │ No          │ Future only     │  │
│ │ btnSave     │ Button   │ N/A         │ Submit form     │  │
│ │ btnCancel   │ Button   │ N/A         │ Return to list  │  │
│ └─────────────┴──────────┴─────────────┴─────────────────┘  │
│                                                             │
│ ─────────────────────────────────────────────────────────── │
│ VALIDATION MESSAGES:                                        │
│                                                             │
│ • txtName empty: "Name is required"                         │
│ • txtName > 100: "Name cannot exceed 100 characters"        │
│ • dtpDate in past: "Date must be in the future"             │
│                                                             │
│ ─────────────────────────────────────────────────────────── │
│ BUTTON BEHAVIORS:                                           │
│                                                             │
│ btnSave:                                                    │
│ • Enabled when: All required fields valid                   │
│ • On click: Validate → Save → Show success → Redirect       │
│ • On error: Show error message, stay on page                │
│                                                             │
│ btnCancel:                                                  │
│ • If changes made: Show "Discard changes?" confirmation     │
│ • On confirm: Discard and return to list                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

8.2 Screen: [Screen Name]
────────────────────────────────────────────────────────────────
[Repeat for each screen]

═══════════════════════════════════════════════════════════════
9. REPORTING REQUIREMENTS
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│ RPT-001: [Report Name]                                      │
├─────────────────────────────────────────────────────────────┤
│ Purpose: [What this report shows]                           │
│ Audience: [Who uses this report]                            │
│ Frequency: [On-demand/Daily/Weekly/Monthly]                 │
│                                                             │
│ Parameters:                                                 │
│ • Date Range (required)                                     │
│ • Status (optional, default: All)                           │
│ • Department (optional, default: User's dept)               │
│                                                             │
│ Columns:                                                    │
│ ┌─────────────────┬───────────┬───────────────────────────┐ │
│ │ Column          │ Type      │ Notes                     │ │
│ ├─────────────────┼───────────┼───────────────────────────┤ │
│ │ Date            │ Date      │ Sortable                  │ │
│ │ Name            │ String    │ Sortable, filterable      │ │
│ │ Status          │ String    │ Filterable                │ │
│ │ Amount          │ Currency  │ Sum at footer             │ │
│ └─────────────────┴───────────┴───────────────────────────┘ │
│                                                             │
│ Export Formats: PDF, Excel, CSV                             │
│                                                             │
│ Sample Layout: [Link to mockup]                             │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
10. APPENDICES
═══════════════════════════════════════════════════════════════

Appendix A: Mockups/Wireframes
────────────────────────────────────────────────────────────────
[Links or embedded images]

Appendix B: State Diagrams
────────────────────────────────────────────────────────────────
[Entity state transitions]

Appendix C: Process Flow Diagrams
────────────────────────────────────────────────────────────────
[Detailed process flows]
```

---

## ✅ FRD QUALITY CHECKLIST

```
COMPLETENESS:
☐ All functions documented
☐ All UI screens specified
☐ All business rules captured
☐ Data requirements defined
☐ Integration points documented

DETAIL LEVEL:
☐ Input/Processing/Output specified
☐ Validation rules clear
☐ Error messages defined
☐ Button behaviors documented
☐ Acceptance criteria testable

CONSISTENCY:
☐ Terminology matches SRS/BRD
☐ Field names match data dictionary
☐ UI elements match mockups
☐ Business rules cross-referenced
```

---

## 🔗 RELATED SKILLS

| For... | Load |
|--------|------|
| NFR specifications | @ba-nfr |
| Business rules analysis | @ba-elicitation |
| UI prototyping validation | @ba-validation |

---

*Use this template for detailed functional specifications that developers can implement directly.*
