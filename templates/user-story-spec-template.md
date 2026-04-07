# User Story Specification Template
## Template Skill — Vertical Domain User Story Specification

---

## 📌 SKILL METADATA

| Attribute | Value |
|-----------|-------|
| **Template ID** | TMPL-US-SPEC |
| **Category** | 🟢 Template |
| **Load When** | Building sprint-ready user story specs for regulated vertical domains |
| **Dependencies** | @ba-identity, @ba-elicitation, @ba-writing, @ba-nfr, @ba-agile |
| **Output** | Complete User Story Specification document |

---

## 🎯 WHEN TO USE THIS TEMPLATE

| Use This Template When | Don't Use When |
|------------------------|----------------|
| ✓ Regulated domain (healthcare, fintech, govtech) | ✗ Simple internal tool with no compliance |
| ✓ B2C + B2B dual-tenant product | ✗ Single-user SaaS with no enterprise tier |
| ✓ Third-party SDK/API integration with feasibility risk | ✗ Fully in-house technology stack |
| ✓ Agile team needing sprint-ready stories with compliance | ✗ Waterfall project (use SRS template) |
| ✓ Privacy-sensitive data (biometric, financial, health) | ✗ Non-sensitive data products |
| ✓ Multi-phase product with MVP → Phase 1 → Phase 2 | ✗ One-shot delivery with fixed scope |

### How This Differs from Other BA-Kit Templates

| Template | Focus | This Template Adds |
|----------|-------|--------------------|
| **Agile Artifacts** | Generic story/epic format | Compliance layer, Security Policy, Data Retention |
| **PRD** | Product scope (WHAT) | Per-story ACs, edge cases, vendor spike matrix |
| **SRS** | System behavior (HOW) | Agile-first structure with NFR woven in |
| **BRD** | Business case (WHY) | Implementation-ready stories with testable ACs |

---

## 📋 TEMPLATE BODY

> **Instructions:** Copy everything below the line. Replace all `[PLACEHOLDER]` markers with project-specific content. Sections marked `[VERTICAL ADAPTER]` contain domain-specific guidance — choose the adapter matching your vertical.

---

````markdown
# [PROJECT NAME] — [FEATURE/MODULE NAME]

## User Story Specification Document

| Attribute | Value |
| --- | --- |
| **Version** | V[X.Y] — [Month Year] |
| **Scope** | [Product/Platform Name] |
| **Owner** | [Organization Name] |
| **Audience** | Product Owners, Developers, QA Teams |
| **Vendor/Partner** | [Vendor Name] — [SDK/API Name] |
| **Legal Framework** | [Primary regulation] · [Interoperability standard] · [International standard — if applicable for future phase] |
| **Classification** | **CONFIDENTIAL — Internal Use Only** |

---

## Document History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| v1.0 | [Date] | [Team] | Initial draft. [X] User Stories across [Y] EPICs. |
| V[X.Y] | [Date] | [Team] | [Summary of changes, new stories, structural additions] |

---

## 1. Introduction

This document defines the user requirements for [FEATURE NAME] of [PRODUCT NAME] — integrating [VENDOR SDK/API] to [core value proposition]. Each requirement follows standard Agile User Story format.

### 1.1 User Story Format

Each User Story follows the standard format:

> As a [**role**], I want [**action/feature**], so that [**benefit/purpose**]

Accompanied by Acceptance Criteria (AC) — specific, testable conditions to verify Story completion.

### 1.2 Priority & Story Point Scale

| Priority | Meaning | Target Sprint |
| --- | --- | --- |
| **P0** | Must Have — Mandatory for MVP | Sprint [X]–[Y] (MVP) |
| **P1** | Should Have — Important for Phase 1 | Sprint [X]–[Y] |
| **P2** | Could Have — Valuable, can defer | [Quarter/Year]+ |

Story Points assess complexity as a composite of: Complexity + Effort + Risk/Uncertainty:

| SP | Meaning |
| --- | --- |
| 1 | Trivial — nearly zero thought required |
| 2 | Simple — done this before |
| 3 | Small — clear, low risk |
| 5 | Medium — needs further analysis |
| 8 | Complex — multiple components |
| 13 | Very complex — consider splitting |

### 1.3 End-user Personas

> **[VERTICAL ADAPTER]** Customize personas for your domain:
> - **Healthcare:** Patient (B2C) / Provider Organization (B2B) / System Admin
> - **FinTech:** Individual Customer (B2C) / Merchant/Enterprise (B2B) / Compliance Admin
> - **Smart City:** Citizen (B2C) / Operator/Agency (B2B) / Platform Admin
> - **EdTech:** Student/Parent (B2C) / Institution (B2B) / Content Admin

| End-user | Description |
| --- | --- |
| **Individual User (B2C)** | [Description of individual end-users. Include: registration method, login options (SSO providers), sub-segments (e.g., age groups, use cases).] |
| **Organization User (B2B)** | [Description of enterprise/org users. Include: license model, employee onboarding flow, admin capabilities, example org types.] |
| **System Administrator** | [Description of platform admins. Include: role-based access (Super Admin, Operation Admin, Finance Admin, etc.), portal URL, MFA requirement.] |

### 1.4 Platform & Technology

| Platform | Scope | Notes |
| --- | --- | --- |
| **iOS** | [Min version] | Native or cross-platform — TBD |
| **Android** | [Min version] | Native or cross-platform — TBD |
| **Web (Mobile)** | [Browser + version] | [Feature] via Web — verify [Vendor] Web SDK |
| **Web (Admin)** | [Browsers] | Portal /system-admin and /admin |

> **⚠️ ADR-001 (Required before [Infrastructure EPIC]):** Architecture decision (Native iOS/Android, React Native, Flutter, or Web-first PWA) **must be finalized before Sprint deploying [Infrastructure EPIC]**. This blocks all main flows. [Vendor] SDK compatibility per platform must be verified via spike test.

### 1.5 MVP Market Scope

| Market | Phase | Language |
| --- | --- | --- |
| **[Primary Market]** | MVP (P0) | [Default language] |
| **[Secondary Markets]** | Phase 1 (P1) | [Additional languages] |

> **Note:** MVP requires [default language] only. Multi-language support ([i18n story ID]) is P1. If business strategy shifts to multi-market MVP, escalate [i18n story] to P0.

---

## 2. Product Backlog Summary

> **Note on EPIC numbering:** EPIC numbers reflect the order added to the document (chronological), not implementation priority. See Section 2.1 EPIC Dependency Map for actual implementation sequence.

| Story ID | Story Name | Epic | Priority | SP | Dependencies |
| --- | --- | --- | --- | --- | --- |
| US-001 | [Story name] | EPIC-01 | P0 | [X] | — |
| US-002 | [Story name] | EPIC-01 | P0 | [X] | US-001 |
| ... | ... | ... | ... | ... | ... |

**Backlog Summary:**

| Priority Group | Stories | Story Points |
| --- | --- | --- |
| P0 — Must Have | [X] | [Y] SP |
| P1 — Should Have | [X] | [Y] SP |
| P2 — Could Have | [X] | [Y] SP |
| **Total** | **[X]** | **[Y] SP** |

---

### 2.1 EPIC Dependency Map

The diagram below shows mandatory implementation order between EPICs. Arrow A → B means A must complete before B.

**Pre-requisite (before all EPICs):**

```
ADR-001 (Architecture Decision: [options])
    → EPIC-[Infrastructure] (Technical Infrastructure)
        → Main flow
```

> **⚠️ ADR-001** must be completed before Sprint deploying [Infrastructure EPIC]. This decision directly affects: [list of impacted stories/capabilities].

**Critical Path:**

```
EPIC-[Account] → EPIC-[Auth] → EPIC-[Consent/Onboarding] → EPIC-[Core Feature] → EPIC-[Results] → EPIC-[Storage/Export]
```

**Additional Dependencies:**
- EPIC-[History] ← depends on EPIC-[Storage] (needs stored data)
- EPIC-[Privacy] ← depends on EPIC-[Consent] + EPIC-[Storage]
- EPIC-[Org Management] ← depends on EPIC-[Auth] + EPIC-[Account]
- EPIC-[Payment] ← depends on EPIC-[Account] + EPIC-[Core Feature]

**Parallel (no mutual dependencies):**
- EPIC-[System Admin] — deploy in parallel with main flow
- EPIC-[App Lifecycle] — deploy in parallel
- EPIC-[Error & Support] — deploy in parallel

---

### 2.2 Vendor/Partner — Capability Verification Matrix

> **[VERTICAL ADAPTER]** Replace with your vendor's capabilities:
> - **Healthcare SDK:** Biometric measurements, device compatibility, offline mode
> - **FinTech API:** Payment methods, KYC verification, transaction types
> - **IoT Gateway:** Sensor protocols, device types, edge processing
> - **AI/ML Service:** Model accuracy, inference latency, supported inputs

> **⚠️ Required:** Complete spike test before Sprint 1 planning. Owner: Tech Lead + PO.

| SDK/API Capability | Dependent Stories | Required for MVP? | Fallback (if not supported) |
| --- | --- | --- | --- |
| **[Core Capability 1]** | US-[XXX] | ✅ YES (P0 blocker) | **Block MVP launch** — no fallback |
| **[Core Capability 2]** | US-[XXX] | ✅ YES | Server-side computation from other signals |
| **[Advanced Capability 1]** | US-[XXX] | ✅ YES (but mode deferrable) | Remove advanced mode, shift to P1 |
| **[Optional Capability 1]** | US-[XXX] | No (already P1) | Remove feature |
| **[Platform: iOS]** | US-[XXX] | ✅ YES | — |
| **[Platform: Android]** | US-[XXX] | ✅ YES | — |
| **[Platform: Web]** | US-[XXX] | Needs verification | Native app only, Web feature → P2 |

**Spike test deadline:** T-2 weeks before Sprint 1 planning.
**Output:** Spike test report confirming each row above, including SDK/API version tested and results.

---

## 3. User Stories by Epic

---

### EPIC-[XX] — [Epic Name]

> [1-2 sentence epic description. What user goal does this epic serve? What regulation/standard does it address?]

> **⚠️ [Vendor] SDK — Spike Verification Required:** [If applicable, state assumptions about vendor capabilities that need verification.]

#### US-[XXX] — [Story Title]

**Priority: P[0/1/2] · [X] SP**

*Precondition: [EPIC-XX — US-YYY (dependency description)] — if applicable*

As a **[persona]**, I want **[action/feature]**, so that *[benefit/purpose]*.

**Acceptance Criteria:**

- **AC1:** [Testable criterion — happy path]
- **AC2:** [Testable criterion — data/display requirements]
- **AC3:** [Testable criterion — business rule]
- **AC4:** [Testable criterion — technical constraint (e.g., on-device processing, encryption)]
- **AC5:** [Testable criterion — error/failure handling]
- **AC6:** [Testable criterion — edge case. Flag as: `(Edge case — [description])`]

> **Pattern Notes for Story Authors:**
> - Each AC must be independently testable by QA
> - Include at least 1 error/failure AC per story
> - Flag edge cases explicitly with `(Edge case — description)` prefix
> - For stories touching sensitive data, include data handling AC (encryption, retention, consent)
> - For stories with vendor dependency, include timeout/fallback AC
> - B2B vs B2C behavioral differences should be explicit ACs, not assumptions

---

> **[VERTICAL ADAPTER] Domain-Specific Story Patterns:**
>
> **Healthcare:**
> - Medical content ACs require: "Sign-off artifact: [Medical Advisor Name] reviewed content on [date]"
> - Biometric data ACs require: "On-device processing, zero image persistence"
> - Age-restricted features require: "Only available for profiles ≥ [age] years old"
>
> **FinTech:**
> - Payment ACs require: "PCI-DSS compliant, no card data stored"
> - Transaction ACs require: "Idempotency key per transaction, orphan payment reconciliation"
> - KYC ACs require: "eKYC verification level [X] per [regulation]"
>
> **Smart City:**
> - Camera/sensor ACs require: "QCVN [standard] compliance, data anonymization at edge"
> - Public data ACs require: "k-anonymity threshold ≥ [value]"
>
> **EdTech:**
> - Minor data ACs require: "Guardian consent for users under [age]"
> - Content ACs require: "Age-appropriate content filtering per [regulation]"

---

### Standard EPIC Categories

> Use this checklist to ensure your backlog covers all necessary functional areas. Not all EPICs are required for every project — mark N/A where not applicable.

| # | EPIC Category | Description | Required? |
| --- | --- | --- | --- |
| 1 | **Onboarding & Consent** | First-time user flow, explicit consent, legal compliance | ✅ Always |
| 2 | **Core Feature Preparation** | Device checks, permissions, guidance before core action | ✅ Always |
| 3 | **Core Feature Execution** | The primary value-generating action | ✅ Always |
| 4 | **Results & Interpretation** | Displaying, explaining, and acting on results | ✅ Always |
| 5 | **History & Trends** | Historical data, trend analysis, longitudinal tracking | Usually |
| 6 | **Data Storage & Export** | PHR/data persistence, sharing, PDF/report export | Usually |
| 7 | **Privacy & Data Rights** | Privacy settings, data deletion, DSAR | ✅ Regulated |
| 8 | **System Administration** | Admin portal, user management, audit log | ✅ Always |
| 9 | **Authentication & i18n** | SSO, enterprise login, language selection | ✅ Always |
| 10 | **Organization Management** | B2B org admin, employee provisioning, aggregate reports | If B2B |
| 11 | **Payment & Subscription** | Service packages, payment gateway, billing history | If monetized |
| 12 | **Account & Profile** | Registration, profile management, password, deletion | ✅ Always |
| 13 | **App Lifecycle** | Biometric lock, force update, notifications, offline sync | Usually |
| 14 | **Error & Support** | Error handling, help/FAQ, feedback/reporting | ✅ Always |
| 15 | **Technical Infrastructure** | Server setup, monitoring, notification service | ✅ Always |

---

## 4. Non-Functional Requirements (NFR)

| NFR Group | Metric | Requirement | Priority |
| --- | --- | --- | --- |
| Performance | [Core Feature] | [Timing constraint, e.g., ≤ 40 seconds total] | P0 |
| Performance | API Gateway | Response ≤ [X]ms | P0 |
| Security | Sensitive Data | [Zero persistence / encryption policy] | P0 |
| Security | Encryption | [Algorithm] at rest, [Protocol] in transit | P0 |
| Privacy | Data Minimization | Only send minimum necessary data to [vendor/partner] | P0 |
| Compliance | DPIA Coverage | 100% of flows processing [sensitive data type] have DPIA | P0 |
| Usability | Core UX Flow | ≤ [X] steps from menu to [result/output] | P1 |
| Usability | Multi-language | Support [X] languages: [list] | P1 |
| Availability | Uptime SLA | [X]% SLA ([Y] hours downtime/year) | P0 |
| Scalability | Concurrent Users | Support [X] concurrent users | P0 |
| Security | Share/Export Token | Single-use token, expires after [X] minutes, HTTPS only | P1 |
| Security | Admin Portal | MFA required. Session expires after [X] minutes. IP whitelist mandatory. | P0 |
| Compatibility | Admin Browser | [Browser list with min versions]. Responsive min [X]px. | P1 |
| Accessibility | WCAG 2.1 AA | Contrast ratio ≥ 4.5:1, screen reader support, touch target ≥ 44px | P1 |
| Security | API Rate Limiting | [X] req/min general, [Y] req/min auth, [Z] req/min DSAR. HTTP 429 on exceed. | P0 |
| Interoperability | [Standard] Mapping | Technical mapping document due **[deadline relative to sprint]**. | P0 |

> **[VERTICAL ADAPTER] Domain-Specific NFRs:**
> - **Healthcare:** Add FHIR Resource Mapping, medical disclaimer, scan accuracy thresholds
> - **FinTech:** Add PCI-DSS compliance, transaction latency, reconciliation frequency
> - **Smart City:** Add ONVIF compliance, video retention, edge processing latency
> - **EdTech:** Add COPPA/children's data, content delivery CDN latency

---

### 4.1 Data Retention Matrix

| Data Type | Retention Period | Deletion Trigger | Legal Basis | Related Story |
| --- | --- | --- | --- | --- |
| [Core data record] | [X] years | Auto-expiry | [Regulation — article] | US-[XXX] |
| [Core data — user deletion request] | Delete within [X] days | User request via US-[XXX] | [Regulation — right to erasure] | US-[XXX] |
| [Full account — user deletion] | Disable immediately, permanent delete after [X] days | User request via US-[XXX] | [Regulation — right to erasure] | US-[XXX] |
| [B2B employee data — offboarding] | Retain [X] days, allow export | Admin disable via US-[XXX] | [Labor/data law] | US-[XXX] |
| [Offline/local data] | [X] days or [Y] records | Expiry / limit reached | N/A (local only) | US-[XXX] |
| [Unpaid orders] | [X] hours | Auto-expiry | N/A | US-[XXX] |
| [Consent record] | Permanent (immutable) | Never delete | [Regulation — legal evidence] | US-[XXX] |
| [Audit log] | [X] years minimum | Auto-expiry | [Regulation — compliance audit] | US-[XXX] |
| [Share/export token] | [X] minutes | Expiry / consumed | N/A | US-[XXX] |
| [Invitation email token] | [X] hours | Auto-expiry | N/A | US-[XXX] |
| [Password reset token] | [X] hour(s) | Expiry / consumed | N/A | US-[XXX] |

**Priority Rule:** Legal requirement > User deletion request > Default retention.

**Note:** Consent records and audit logs are immutable records — not affected by account deletion or data deletion requests.

---

### 4.2 Unified Security Policy Table

> **Purpose:** Eliminate contradictions between stories (e.g., one story says 5 attempts lockout, another says 3). All stories MUST reference this table instead of self-defining security policies.

| Policy | B2C (Individual) | B2B (Organization) | System Admin | Story References |
| --- | --- | --- | --- | --- |
| Password policy | ≥[X] chars, uppercase, number, special char | Same as B2C; or IdP policy if SAML/OIDC | ≥[Y] chars, uppercase, lowercase, number, special char | US-[account], US-[b2b-login], US-[admin-login] |
| Account lockout | [N] failures → lock [X] minutes | [N] failures → lock [X] min + email org admin | [N] failures → lock [Y] min + email Super Admin | US-[account] AC[X], US-[b2b] AC[X] |
| Password history | [N] recent passwords | [N] recent passwords | [M] recent passwords | US-[password-mgmt] AC[X] |
| Session timeout | [X] days inactive | [X] days inactive | [Y] minutes inactive | US-[session] AC[X], NFR Table |
| MFA | Not required (has Biometric Lock) | Not required (has IdP MFA) | Required | US-[biometric], NFR Table |
| Re-authentication | Delete data, delete account, DSAR | Delete data, delete account, DSAR | All sensitive operations | US-[delete], US-[account-delete], US-[dsar] |

---

### 4.3 Compliance Applicability Matrix

> **[VERTICAL ADAPTER]** Replace regulation columns for your jurisdiction:
> - **Vietnam Healthcare:** NĐ 13/2023 + HIPAA (future) + GDPR (future)
> - **Vietnam FinTech:** NĐ 13/2023 + PCI-DSS + SBV Circulars
> - **Vietnam Smart City:** NĐ 13/2023 + QCVN 135 + GDPR (future)
> - **Vietnam EdTech:** NĐ 13/2023 + NĐ 56 (children) + GDPR (future)

> **Scope:** MVP applies to [primary market] only. International regulation columns for future phase reference.

| Legal Requirement | [Primary Regulation] | [Int'l Regulation 1] | [Int'l Regulation 2] | Mapped Story | V[X.Y] Status |
| --- | --- | --- | --- | --- | --- |
| Data collection consent | [Article — explicit consent] | [Article] | [Section] | US-[consent] | ✅ Covered |
| Right of access (DSAR) | [Article — right of access] | [Article] | [Section] | US-[dsar] | ✅ Covered |
| Right to erasure | [Article — right to delete] | [Article] | N/A | US-[delete-data], US-[delete-account] | ✅ Covered |
| Data portability | [Article — portability] | [Article] | N/A | US-[export], US-[dsar] | ✅ Covered |
| Minor data protection | [Article — minors] | [Article] | N/A | US-[consent] AC[X], US-[multi-profile] AC[X] | ✅ Covered |
| DPIA for sensitive data | [Article — DPIA] | [Article] | N/A | NFR Table | ✅ Covered |
| Audit trail | [Article — logging] | [Article] | [Section] | US-[audit-log] | ✅ Covered |
| Data encryption | [Article — technical measures] | [Article] | [Section] | NFR Table | ✅ Covered |
| Data retention limits | [Article — retention] | [Article] | [Section] | Data Retention Matrix | ✅ Covered |

---

## 5. Definition of Ready & Done

### 5.1 Definition of Ready (DoR)

A User Story enters sprint when ALL conditions are TRUE:

- User Story is clearly written and confirmed by Product Owner.
- All Acceptance Criteria are specific and testable.
- Dependencies on vendors ([Vendor Name]...) are confirmed via email or written agreement.
- UI/UX wireframes or related design documents are available before implementation.
- Story Points are estimated by the development team during planning/preview.
- Legal and compliance review is completed for any flow processing [sensitive data type] or personal information.

> **[VERTICAL ADAPTER] Additional DoR checks:**
> - **Healthcare:** Medical content reviewed by medical advisor
> - **FinTech:** Payment flow reviewed by compliance team
> - **Smart City:** Camera/sensor specs confirmed by hardware vendor
> - **EdTech:** Content appropriateness reviewed for target age group

### 5.2 Definition of Done (DoD)

A User Story is considered done when and only when ALL conditions are met:

- Pass all test cases confirmed by QA.
- Pass integration test cases.
- [Sensitive data type] and personal data handling satisfies signed consent content.
- External data exchange satisfies [interoperability standard] validator.
- Consent logs must be immutable records — no function can modify or delete after creation.
- Pass Smoke Test on PRODUCTION environment.
- Product Owner confirms Story/module deployment success.

---

## Appendix A — Glossary

> **Instructions:** Include all domain-specific terms used in user stories. Non-technical stakeholders should be able to understand every term.

| Term | Definition |
| --- | --- |
| [Domain Technology] | [Plain-language explanation of the core technology used] |
| [Vendor SDK/API] | [What it does, where it runs (on-device vs cloud), offline capability] |
| [Interoperability Standard] | [Full name — standard description] |
| [Data Record Type] | [What data this represents in the system] |
| [Risk Assessment Model] | [Clinical/financial/operational risk model name and description] |
| [Primary Regulation] | [Full regulation name, jurisdiction, effective date] |
| DPIA | Data Protection Impact Assessment — mandatory for [sensitive data type] processing |
| DSAR | Data Subject Access Request — subject's right to access personal data |
| k-anonymity | Anonymization technique ensuring each record is indistinguishable from at least k-1 others |
| IdP | Identity Provider — external identity service (e.g., Azure AD, Google Workspace) |
| DPO | Data Protection Officer — personal data protection officer per [regulation] |
| Edge AI | AI model running directly on user's device (on-device), no data sent to server |
| ADR | Architecture Decision Record — documents important technical decisions |

---

## Appendix B — UI/UX Artifacts Checklist

> **Purpose:** Checklist for UX Design team to ensure all wireframes/prototypes are created before Sprint Planning.

| EPIC | Required Screens | DoR Story | Status |
| --- | --- | --- | --- |
| EPIC-[Onboarding] | Consent screen (layered), Minor consent prompt | US-[consent] | ☐ Not started |
| EPIC-[Pre-scan] | [Device check], [Guidance overlay], [Countdown] | US-[prep stories] | ☐ Not started |
| EPIC-[Core Feature] | [Result dashboard], [Detail cards] | US-[core stories] | ☐ Not started |
| EPIC-[Interpretation] | [Explanation overlay], [Recommendation panel], [Alert] | US-[interpretation] | ☐ Not started |
| EPIC-[History] | [History list + filter], [Trend chart] | US-[history] | ☐ Not started |
| EPIC-[Export] | [Data export], [Share flow], [PDF layout] | US-[export] | ☐ Not started |
| EPIC-[Privacy] | [Privacy settings], [Delete confirm], [DSAR flow] | US-[privacy] | ☐ Not started |
| EPIC-[Admin] | [Admin dashboard], [User management], [Audit log] | US-[admin] | ☐ Not started |
| EPIC-[Auth] | [Login (SSO + Enterprise)], [Language selector] | US-[auth] | ☐ Not started |
| EPIC-[Org Mgmt] | [Org admin portal], [Employee list], [Aggregate report] | US-[org] | ☐ Not started |
| EPIC-[Payment] | [Package comparison], [Checkout], [Payment history] | US-[payment] | ☐ Not started |
| EPIC-[Account] | [Registration], [Profile edit], [Password reset] | US-[account] | ☐ Not started |
| EPIC-[Lifecycle] | [Biometric lock], [Force update], [Notification settings] | US-[lifecycle] | ☐ Not started |
| EPIC-[Support] | [Error states], [Help/FAQ], [Feedback report] | US-[support] | ☐ Not started |

---

## Appendix C — Vertical Domain Adaptation Guide

> **Purpose:** Quick reference for instantiating this template for specific industry verticals.

### C.1 Persona Mapping

| Template Role | Healthcare | FinTech | Smart City | EdTech |
| --- | --- | --- | --- | --- |
| Individual (B2C) | Patient, Chronic patient, Elderly | Bank customer, Investor | Citizen, Resident | Student, Parent |
| Organization (B2B) | Hospital, Clinic, Insurance | Merchant, Enterprise, Bank | Government agency, Utility | School, University |
| System Admin | Platform Operations | Compliance Officer | Control Center Operator | Content Administrator |

### C.2 Regulation Mapping

| Template Slot | Healthcare | FinTech | Smart City | EdTech |
| --- | --- | --- | --- | --- |
| Primary regulation | NĐ 13/2023 | NĐ 13/2023 | NĐ 13/2023 | NĐ 13/2023 |
| Sector regulation | Luật Khám Chữa Bệnh | SBV Circulars, PCI-DSS | QCVN 135, Luật CNTT | NĐ 56 (children's data) |
| Int'l standard (future) | HIPAA, GDPR | PSD2, GDPR | GDPR, ISO 27001 | COPPA, GDPR |
| Interoperability | HL7 FHIR R4 | ISO 20022, Open Banking | ONVIF, MQTT | IMS LTI, xAPI |

### C.3 Vendor/Partner Pattern

| Template Slot | Healthcare | FinTech | Smart City | EdTech |
| --- | --- | --- | --- | --- |
| Vendor type | Medical AI SDK | Payment gateway API | Camera/IoT SDK | LMS/Video API |
| Spike test focus | Measurement accuracy, device compat | Transaction types, KYC levels | Protocol support, edge processing | Content delivery, concurrent streams |
| Fallback strategy | Block MVP if core metrics fail | Alternative payment provider | Reduce sensor types | Degrade to async content |

### C.4 Data Sensitivity Classification

| Template Slot | Healthcare | FinTech | Smart City | EdTech |
| --- | --- | --- | --- | --- |
| Highest sensitivity | Biometric, PHI | Financial transactions, KYC | Facial recognition, location | Minor PII, learning records |
| DPIA mandatory for | All biometric flows | All KYC + transaction flows | All camera + location flows | All minor data flows |
| Retention baseline | 10 years (health records) | 5 years (financial records) | 90 days (video), 5 years (logs) | Duration of enrollment + 2 years |

````

---

## ✅ QUALITY CHECKLIST

```
Section 0: Document Control
  ☐ Version history is complete
  ☐ Confidentiality classification set
  ☐ Vendor/partner named and scoped

Section 1: Introduction
  ☐ Persona model matches domain (B2C/B2B/Admin)
  ☐ Platform matrix complete with min versions
  ☐ ADR-001 blocker documented
  ☐ MVP market scope explicit

Section 2: Backlog
  ☐ All stories have ID, EPIC, Priority, SP, Dependencies
  ☐ EPIC Dependency Map shows critical path
  ☐ Vendor Capability Matrix complete with fallbacks
  ☐ Spike test deadline set

Section 3: User Stories
  ☐ Each story follows "As a [persona]..." format
  ☐ Each story has ≥3 ACs (happy path + error + edge case)
  ☐ INVEST criteria satisfied (especially S and T)
  ☐ No story > 13 SP (split if needed)
  ☐ Cross-persona differences explicit in ACs
  ☐ Vendor-dependent stories flagged
  ☐ Sensitive data stories include encryption/consent ACs

Section 4: NFR Framework
  ☐ Performance targets have specific thresholds
  ☐ Security Policy Table eliminates cross-story contradictions
  ☐ Data Retention Matrix covers all data types
  ☐ Compliance Matrix maps all regulations to stories
  ☐ Accessibility (WCAG 2.1 AA) included
  ☐ API rate limiting defined per endpoint type

Section 5: DoR & DoD
  ☐ DoR includes compliance/legal checkpoint
  ☐ DoD includes interoperability validator check
  ☐ DoD includes consent log immutability check

Appendices
  ☐ Glossary covers all domain terms
  ☐ UI/UX Artifacts checklist complete per EPIC
  ☐ Vertical adapter applied for domain
```

---

## 🔗 RELATED BA-KIT SKILLS

| Step | Agent | Action |
|------|-------|--------|
| Stakeholder & Personas | `@ba-identity` | Map stakeholders, define RACI |
| Elicitation | `@ba-elicitation` | Interview, workshop, Colombo method |
| Story Writing | `@ba-writing` | Draft stories with Gherkin ACs |
| Story Prioritization | `@ba-prioritization` | Apply MoSCoW / WSJF |
| NFR Analysis | `@ba-nfr` | ISO 25010 breakdown, performance targets |
| Validation | `@ba-validation` | INVEST check, edge case detection |
| Process Flows | `@ba-process` | BPMN diagrams for complex flows |
| Compliance | `@ba-strategy` | Regulatory landscape analysis |
| Wireframes | Stitch MCP / Figma MCP | See design-prototype-guide.md |
| Publish | `@ba-confluence` | Push to Confluence |
| Tickets | `@ba-jira` | Create Jira epics/stories |

### Power Combo

```
@ba-elicitation → @ba-identity (personas) → @ba-writing (stories + ACs)
  → @ba-nfr (NFR section) → @ba-prioritization (MoSCoW)
  → @ba-validation (INVEST + edge cases) → @ba-jira (tickets)
```

---

*Use this template to create sprint-ready, compliance-aware User Story Specifications for regulated vertical domains. Battle-tested through healthcare vertical with 37-fix review process.*
