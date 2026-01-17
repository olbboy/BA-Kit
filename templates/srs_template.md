# 🟢 SKILL-10: SRS TEMPLATE (IEEE 29148)
## Template Skill - Software Requirements Specification

---

## 📌 SKILL METADATA

| Attribute | Value |
|-----------|-------|
| **Template ID** | TMPL-SRS |
| **Category** | 🟢 Template |
| **Load When** | Creating detailed software requirements |
| **Dependencies** | @ba-writing, @ba-nfr, @ba-traceability |
| **Standard** | ISO/IEC/IEEE 29148:2018 |
| **Output** | Complete SRS document |

---

## 🎯 WHEN TO USE SRS

| Use SRS When | Don't Use SRS When |
|--------------|-------------------|
| ✓ Waterfall/V-Model projects | ✗ Pure Agile (use User Stories) |
| ✓ Contract-based development | ✗ Early exploration phase (use BRD) |
| ✓ Regulatory/compliance needs | ✗ Simple internal tools |
| ✓ Outsourced development | ✗ Rapid prototyping |
| ✓ Complex system integration | ✗ Already have detailed FRD |

---

## 📋 SRS TEMPLATE (IEEE 29148)

```
═══════════════════════════════════════════════════════════════
            SOFTWARE REQUIREMENTS SPECIFICATION
                      [System Name]
              Based on ISO/IEC/IEEE 29148:2018
═══════════════════════════════════════════════════════════════

Document Control
────────────────────────────────────────────────────────────────
Document ID: [Project]-SRS-[Version]
Version: [X.Y.Z]
Date: [YYYY-MM-DD]
Status: [Draft/Review/Approved/Baseline]
Classification: [Internal/Confidential]

Version History
┌─────────┬────────────┬──────────┬─────────────────────────────┐
│ Version │ Date       │ Author   │ Changes                     │
├─────────┼────────────┼──────────┼─────────────────────────────┤
│         │            │          │                             │
└─────────┴────────────┴──────────┴─────────────────────────────┘

Approval Signatures
┌──────────────────┬────────────┬─────────────┬────────────────┐
│ Name             │ Role       │ Signature   │ Date           │
├──────────────────┼────────────┼─────────────┼────────────────┤
│                  │ Sponsor    │             │                │
│                  │ Product    │             │                │
│                  │ Tech Lead  │             │                │
│                  │ QA Lead    │             │                │
└──────────────────┴────────────┴─────────────┴────────────────┘

═══════════════════════════════════════════════════════════════
                    TABLE OF CONTENTS
═══════════════════════════════════════════════════════════════
1. Introduction
   1.1 Purpose
   1.2 Scope
   1.3 Product Overview
   1.4 Definitions, Acronyms, Abbreviations
   1.5 References
2. System Overview
   2.1 System Context
   2.2 System Functions
   2.3 User Characteristics
   2.4 Constraints
   2.5 Assumptions and Dependencies
3. System Features
   3.1 [Feature 1]
   3.2 [Feature 2]
   ...
4. External Interface Requirements
   4.1 User Interfaces
   4.2 Hardware Interfaces
   4.3 Software Interfaces
   4.4 Communication Interfaces
5. Non-Functional Requirements
   5.1 Performance Requirements
   5.2 Security Requirements
   5.3 Reliability Requirements
   5.4 Availability Requirements
   5.5 Maintainability Requirements
   5.6 Portability Requirements
6. Other Requirements
7. Appendices

═══════════════════════════════════════════════════════════════
1. INTRODUCTION
═══════════════════════════════════════════════════════════════

1.1 Purpose
────────────────────────────────────────────────────────────────
This Software Requirements Specification (SRS) describes the 
functional and non-functional requirements for [System Name].

Intended Audience:
• Project Managers - for planning and tracking
• Developers - for implementation guidance
• QA Team - for test case development
• Stakeholders - for requirements validation

1.2 Scope
────────────────────────────────────────────────────────────────
Product Name: [Name]
Product Version: [Version]

The [System Name] will:
• [High-level capability 1]
• [High-level capability 2]
• [High-level capability 3]

The system will NOT:
• [Explicit exclusion 1]
• [Explicit exclusion 2]

1.3 Product Overview
────────────────────────────────────────────────────────────────

1.3.1 Product Perspective
[Is this a new system, replacement, or enhancement?]
[How does it fit in the larger system/organization?]

1.3.2 Product Functions (Summary)
┌──────────────────────────────────────────────────────────────┐
│                    FUNCTION SUMMARY                          │
├──────────────────────────────────────────────────────────────┤
│ • [Function 1]: [Brief description]                          │
│ • [Function 2]: [Brief description]                          │
│ • [Function 3]: [Brief description]                          │
└──────────────────────────────────────────────────────────────┘

1.3.3 User Classes and Characteristics
┌──────────────┬─────────────────────┬────────────────────────┐
│ User Class   │ Description         │ Characteristics        │
├──────────────┼─────────────────────┼────────────────────────┤
│ Admin        │ System administrator│ Technical, full access │
│ Manager      │ Business manager    │ Reports, approvals     │
│ End User     │ Daily operator      │ Core transactions      │
│ Guest        │ Unauthenticated     │ Limited view access    │
└──────────────┴─────────────────────┴────────────────────────┘

1.3.4 Operating Environment
• Operating System: [e.g., Windows 10+, macOS 12+, Ubuntu 22+]
• Browser: [e.g., Chrome 100+, Firefox 100+, Safari 15+]
• Database: [e.g., PostgreSQL 14+]
• Runtime: [e.g., Node.js 18+, Java 17+]

1.3.5 Design and Implementation Constraints
• [Constraint 1]: [Description]
• [Constraint 2]: [Description]

1.3.6 Assumptions and Dependencies
┌────────┬─────────────────────────────────┬───────────────────┐
│ ID     │ Assumption/Dependency           │ Impact if Invalid │
├────────┼─────────────────────────────────┼───────────────────┤
│ A-001  │ [Assumption]                    │ [Impact]          │
│ D-001  │ [Dependency on external system] │ [Impact]          │
└────────┴─────────────────────────────────┴───────────────────┘

1.4 Definitions, Acronyms, Abbreviations
────────────────────────────────────────────────────────────────
┌──────────────┬───────────────────────────────────────────────┐
│ Term         │ Definition                                    │
├──────────────┼───────────────────────────────────────────────┤
│ [Term]       │ [Definition]                                  │
│ [Acronym]    │ [Full form and meaning]                       │
└──────────────┴───────────────────────────────────────────────┘

1.5 References
────────────────────────────────────────────────────────────────
┌────────┬────────────────────────┬────────────┬───────────────┐
│ ID     │ Document               │ Version    │ Location      │
├────────┼────────────────────────┼────────────┼───────────────┤
│ REF-01 │ Business Requirements  │ 1.0        │ [Link/Path]   │
│ REF-02 │ System Architecture    │ 1.0        │ [Link/Path]   │
└────────┴────────────────────────┴────────────┴───────────────┘

═══════════════════════════════════════════════════════════════
2. SYSTEM OVERVIEW
═══════════════════════════════════════════════════════════════

2.1 System Context
────────────────────────────────────────────────────────────────
[Context diagram showing system and external entities]

┌─────────────────────────────────────────────────────────────┐
│                     SYSTEM CONTEXT                          │
│                                                             │
│    ┌─────────┐                         ┌─────────┐         │
│    │  User   │ ◄──────────────────────►│ System  │         │
│    └─────────┘                         │  Name   │         │
│                                        │         │         │
│    ┌─────────┐                         │         │         │
│    │External │ ◄──────────────────────►│         │         │
│    │System A │                         └─────────┘         │
│    └─────────┘                              ▲              │
│                                             │              │
│    ┌─────────┐                              │              │
│    │External │ ◄────────────────────────────┘              │
│    │System B │                                             │
│    └─────────┘                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
3. SYSTEM FEATURES
═══════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────
3.1 FEATURE: [Feature Name]
────────────────────────────────────────────────────────────────

3.1.1 Description
[Brief description of the feature and its purpose]

Priority: [Must/Should/Could]
Source: [BR-ID or Stakeholder]

3.1.2 Functional Requirements

┌─────────────────────────────────────────────────────────────┐
│ FR-001: [Requirement Title]                                 │
├─────────────────────────────────────────────────────────────┤
│ Description:                                                │
│ The system SHALL [action] WHEN [condition]                  │
│ SO THAT [purpose].                                          │
│                                                             │
│ Rationale: [Why this requirement exists]                    │
│                                                             │
│ Acceptance Criteria:                                        │
│ • Given [context], When [action], Then [result]             │
│ • Given [context], When [action], Then [result]             │
│                                                             │
│ Business Rules:                                             │
│ • BR-001: [Rule description]                                │
│                                                             │
│ Priority: [Must/Should/Could]                               │
│ Source: [Stakeholder/Document]                              │
│ Dependencies: [Related REQ-IDs]                             │
│ Trace: BR-XXX → FR-001 → TC-XXX                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FR-002: [Requirement Title]                                 │
├─────────────────────────────────────────────────────────────┤
│ Description:                                                │
│ The system SHALL [action] WHEN [condition].                 │
│                                                             │
│ Acceptance Criteria:                                        │
│ • [Criterion 1]                                             │
│ • [Criterion 2]                                             │
│                                                             │
│ Priority: [Must/Should/Could]                               │
│ Source: [Stakeholder/Document]                              │
└─────────────────────────────────────────────────────────────┘

[Repeat FR template for each requirement in this feature]

────────────────────────────────────────────────────────────────
3.2 FEATURE: [Feature Name]
────────────────────────────────────────────────────────────────
[Repeat structure for each feature]

═══════════════════════════════════════════════════════════════
4. EXTERNAL INTERFACE REQUIREMENTS
═══════════════════════════════════════════════════════════════

4.1 User Interfaces
────────────────────────────────────────────────────────────────

UI-001: [Screen/Interface Name]
┌─────────────────────────────────────────────────────────────┐
│ Purpose: [What this interface is for]                       │
│                                                             │
│ Description:                                                │
│ [Detailed description of the interface]                     │
│                                                             │
│ Elements:                                                   │
│ • [Element 1]: [Type, purpose, validation]                  │
│ • [Element 2]: [Type, purpose, validation]                  │
│                                                             │
│ Navigation:                                                 │
│ • From: [Previous screen(s)]                                │
│ • To: [Next screen(s)]                                      │
│                                                             │
│ Mockup Reference: [Link to mockup/wireframe]                │
└─────────────────────────────────────────────────────────────┘

4.2 Hardware Interfaces
────────────────────────────────────────────────────────────────
┌────────┬─────────────────────────────────────────────────────┐
│ HI-001 │ [Hardware interface description]                    │
│        │ Protocol: [Protocol details]                        │
│        │ Data: [Data exchanged]                              │
└────────┴─────────────────────────────────────────────────────┘

4.3 Software Interfaces
────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────┐
│ SI-001: Integration with [External System Name]             │
├─────────────────────────────────────────────────────────────┤
│ Purpose: [Why we integrate]                                 │
│ Interface Type: [REST API/SOAP/File/Message Queue]          │
│ Protocol: [HTTP/HTTPS/SFTP/etc.]                            │
│ Data Format: [JSON/XML/CSV]                                 │
│ Authentication: [API Key/OAuth/Certificate]                 │
│                                                             │
│ Operations:                                                 │
│ ┌────────────┬───────────┬───────────┬────────────────────┐ │
│ │ Operation  │ Direction │ Frequency │ Data               │ │
│ ├────────────┼───────────┼───────────┼────────────────────┤ │
│ │ Get Users  │ Inbound   │ On-demand │ User list          │ │
│ │ Send Order │ Outbound  │ Real-time │ Order details      │ │
│ └────────────┴───────────┴───────────┴────────────────────┘ │
│                                                             │
│ Error Handling:                                             │
│ • [Error scenario]: [Handling approach]                     │
└─────────────────────────────────────────────────────────────┘

4.4 Communication Interfaces
────────────────────────────────────────────────────────────────
┌────────┬─────────────────────────────────────────────────────┐
│ CI-001 │ Email Notifications                                 │
│        │ Protocol: SMTP                                      │
│        │ Triggers: [When emails are sent]                    │
│        │ Content: [What emails contain]                      │
├────────┼─────────────────────────────────────────────────────┤
│ CI-002 │ Push Notifications                                  │
│        │ Protocol: Firebase Cloud Messaging                  │
│        │ Triggers: [When notifications sent]                 │
└────────┴─────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
5. NON-FUNCTIONAL REQUIREMENTS
═══════════════════════════════════════════════════════════════

5.1 Performance Requirements
────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────┐
│ NFR-PERF-001: Response Time                                 │
├─────────────────────────────────────────────────────────────┤
│ The system SHALL respond to user requests within:           │
│ • Page load: < 3 seconds                                    │
│ • API calls: < 1 second (95th percentile)                   │
│ • Search queries: < 2 seconds                               │
│                                                             │
│ Conditions: Up to 500 concurrent users                      │
│ Measurement: Application Performance Monitoring tool        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ NFR-PERF-002: Throughput                                    │
├─────────────────────────────────────────────────────────────┤
│ The system SHALL support:                                   │
│ • 1,000 transactions per minute (normal)                    │
│ • 2,000 transactions per minute (peak)                      │
│ • 10,000 concurrent users                                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ NFR-PERF-003: Scalability                                   │
├─────────────────────────────────────────────────────────────┤
│ The system SHALL scale horizontally to handle               │
│ 3x expected load without performance degradation.           │
└─────────────────────────────────────────────────────────────┘

5.2 Security Requirements
────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────┐
│ NFR-SEC-001: Authentication                                 │
├─────────────────────────────────────────────────────────────┤
│ The system SHALL:                                           │
│ • Require multi-factor authentication for admin users       │
│ • Enforce password policy (min 12 chars, complexity)        │
│ • Lock accounts after 5 failed login attempts               │
│ • Expire sessions after 30 minutes of inactivity            │
│                                                             │
│ Compliance: OWASP ASVS Level 2                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ NFR-SEC-002: Authorization                                  │
├─────────────────────────────────────────────────────────────┤
│ The system SHALL implement role-based access control:       │
│                                                             │
│ ┌──────────┬────────────────────────────────────────────┐   │
│ │ Role     │ Permissions                                │   │
│ ├──────────┼────────────────────────────────────────────┤   │
│ │ Admin    │ Full access to all functions               │   │
│ │ Manager  │ Read/Write own dept, Reports               │   │
│ │ User     │ Read/Write own records                     │   │
│ │ Guest    │ Read-only public data                      │   │
│ └──────────┴────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ NFR-SEC-003: Data Protection                                │
├─────────────────────────────────────────────────────────────┤
│ The system SHALL:                                           │
│ • Encrypt data at rest using AES-256                        │
│ • Encrypt data in transit using TLS 1.3                     │
│ • Mask sensitive data (PII) in logs                         │
│ • Comply with [GDPR/HIPAA/PCI-DSS as applicable]            │
└─────────────────────────────────────────────────────────────┘

5.3 Reliability Requirements
────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────┐
│ NFR-REL-001: Availability                                   │
├─────────────────────────────────────────────────────────────┤
│ The system SHALL maintain 99.9% availability                │
│ (excluding planned maintenance).                            │
│                                                             │
│ • Maximum unplanned downtime: 8.76 hours/year               │
│ • Planned maintenance window: Sundays 02:00-06:00 UTC       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ NFR-REL-002: Disaster Recovery                              │
├─────────────────────────────────────────────────────────────┤
│ • RTO (Recovery Time Objective): 4 hours                    │
│ • RPO (Recovery Point Objective): 1 hour                    │
│ • Backup frequency: Hourly incremental, Daily full          │
│ • Backup retention: 30 days                                 │
│ • DR testing: Quarterly                                     │
└─────────────────────────────────────────────────────────────┘

5.4 Usability Requirements
────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────┐
│ NFR-USA-001: Accessibility                                  │
├─────────────────────────────────────────────────────────────┤
│ The system SHALL comply with WCAG 2.1 Level AA.             │
│                                                             │
│ Specifically:                                               │
│ • Screen reader compatible                                  │
│ • Keyboard navigation for all functions                     │
│ • Color contrast ratio minimum 4.5:1                        │
│ • Alt text for all images                                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ NFR-USA-002: Learnability                                   │
├─────────────────────────────────────────────────────────────┤
│ • New users SHALL complete core tasks within 30 minutes     │
│   without training                                          │
│ • Online help available for all features                    │
│ • Consistent UI patterns across modules                     │
└─────────────────────────────────────────────────────────────┘

5.5 Maintainability Requirements
────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────┐
│ NFR-MNT-001: Logging & Monitoring                           │
├─────────────────────────────────────────────────────────────┤
│ • All transactions SHALL be logged with timestamp, user,    │
│   action, and result                                        │
│ • Logs SHALL be retained for 90 days                        │
│ • System health metrics exposed via monitoring endpoint     │
└─────────────────────────────────────────────────────────────┘

5.6 Portability Requirements
────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────┐
│ NFR-PRT-001: Deployment                                     │
├─────────────────────────────────────────────────────────────┤
│ • System SHALL be containerized (Docker)                    │
│ • Deployable on AWS, Azure, or GCP                          │
│ • No vendor-specific cloud services required                │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
6. OTHER REQUIREMENTS
═══════════════════════════════════════════════════════════════

6.1 Legal & Compliance
────────────────────────────────────────────────────────────────
• [Regulation 1]: [Requirement]
• [Regulation 2]: [Requirement]

6.2 Documentation Requirements
────────────────────────────────────────────────────────────────
• User manual
• Administrator guide
• API documentation
• Training materials

═══════════════════════════════════════════════════════════════
7. APPENDICES
═══════════════════════════════════════════════════════════════

Appendix A: Data Dictionary
────────────────────────────────────────────────────────────────
┌──────────────┬──────────┬───────────────┬───────────────────┐
│ Field        │ Type     │ Constraints   │ Description       │
├──────────────┼──────────┼───────────────┼───────────────────┤
│ user_id      │ UUID     │ PK, Not Null  │ Unique identifier │
│ email        │ String   │ Unique, 255   │ User email        │
│ created_at   │ DateTime │ Not Null      │ Creation timestamp│
└──────────────┴──────────┴───────────────┴───────────────────┘

Appendix B: Traceability Matrix
────────────────────────────────────────────────────────────────
[Reference to RTM document or include summary matrix]

Appendix C: UI Mockups
────────────────────────────────────────────────────────────────
[Links to wireframes/mockups]

Appendix D: Use Case Diagrams
────────────────────────────────────────────────────────────────
[Links to UML diagrams]
```

---

## ✅ SRS QUALITY CHECKLIST

```
COMPLETENESS:
☐ All sections filled
☐ All features documented
☐ NFRs defined with metrics
☐ External interfaces specified
☐ Data dictionary included

QUALITY:
☐ Requirements use SHALL/SHOULD/MAY
☐ Each requirement has acceptance criteria
☐ No ambiguous terms
☐ Requirements are testable
☐ Traceability established

REVIEW:
☐ Technical review completed
☐ Stakeholder validation done
☐ No open TBDs
☐ Approval signatures obtained
```

---

## 🔗 RELATED SKILLS

| For... | Load |
|--------|------|
| NFR details | @ba-nfr |
| Validation | @ba-validation |
| Traceability | @ba-traceability |
| Agile breakdown | @ba-writing (User Stories) |

---

*Use this template for comprehensive software specifications in traditional methodologies.*
