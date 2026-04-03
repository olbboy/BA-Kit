# 📖 BA-Kit Workflow Cookbook (10 Real-World Scenarios)

**"How do I use these agents in a real fight?"**

This cookbook provides **10 Battle-Tested Workflows** ("Recipes") for common complex scenarios.
Each recipe shows exactly which agents to summon (`@`) and in what order to achieve a specific outcome.

---

## 🟢 SCENARIO 1: The "Startup Founder" (Zero to MVP)
**Context**: A client has a "vague idea" for an app but no details.
**Goal**: Turn a 1-sentence idea into a Dev-Ready Backlog.

**The Chain:**
1.  **`@ba-elicitation`**: "I have an idea for 'Uber for Dog Walkers'. Interview me to find the features."
    *   *(Agent uses Funnel Questioning to define User Personas and Core Loop)*
2.  **`@ba-writing`**: "Based on that interview, draft the MVP Feature List."
3.  **`@ba-prioritization`**: "Apply MoSCoW mapping to these features. We only have budget for 3 months."
    *   *(Agent cuts scope ruthlessly)*
4.  **`@ba-writing`**: "Write Gherkin User Stories for the MUST HAVE features only."

---

## 🟡 SCENARIO 2: The "Legacy Migration" (The Rewrite)
**Context**: You are replacing an old Excel-based process with a Web App.
**Goal**: Ensure no data logic is lost during the migration.

**The Chain:**
1.  **`@ba-process`**: "Analyze this description of the current Excel process. Draw the As-Is BPMN diagram."
    *   *(Agent identifies bottlenecks)*
2.  **`@ba-writing`**: "Extract the data entities and relationships from these Excel headers."
3.  **`@ba-nfr`**: "We are moving from Local Excel to Cloud. Define the Security and Performance constraints."
4.  **`@ba-traceability`**: "Map the old Excel Formulas to the new System Requirements. Ensure 100% coverage."

---

## 🔴 SCENARIO 3: The "Stakeholder War" (Conflict Resolution)
**Context**: Sales wants "Feature A" (Fast entry). Compliance wants "Feature B" (Slow validation). They are blocking the project.
**Goal**: Unblock the team.

**The Chain:**
1.  **`@ba-identity`**: "Map these two stakeholders (Sales VP vs Compliance Officer) on the Power/Interest Grid."
2.  **`@ba-conflict`**: "They are fighting about the 'Customer Onboarding' flow. Sales wants it < 2 mins. Compliance wants 5 documents. Find a win-win."
    *   *(Agent proposes "Automated Background Check" - Fast AND Secure)*
3.  **`@ba-solution`**: "Calculate the ROI of buying an Automated KYC tool ($5/check) vs losing 20% of leads."

---

## 🔵 SCENARIO 4: The "Agile Sprint Planning" (The Grunt Work)
**Context**: Sprint starts in 2 days. The Product Owner just gave you a raw requirement dump.
**Goal**: Groom the backlog and get Use Stories "Ready".

**The Chain:**
1.  **`@ba-writing`**: "Convert this raw text dump into User Stories with Acceptance Criteria."
2.  **`@ba-validation`**: "Review these stories for INVEST criteria. Flag any ambiguous ones."
    *   *(Agent finds 'User interface should be fast' and flags it)*
3.  **`@ba-elicitation`**: "Generate 3 clarifying questions for the PO about the ambiguous stories."

---

## 🟣 SCENARIO 5: The "Production Crisis" (Root Cause Analysis)
**Context**: Users are reporting "Data disappears". The Dev team is blaming the Network team.
**Goal**: Find the actual breakdown and prevent it.

**The Chain:**
1.  **`@ba-root-cause`**: "Incident: Users claim data vanishes after clicking Save. Act as Lead Investigator. Use 5 Whys."
    *   *(Agent drills down: Save -> Timeout -> No Retry Logic -> UI Design)*
2.  **`@ba-process`**: "Draw the 'Unhappy Path' for a Network Timeout situation."
3.  **`@ba-writing`**: "Write a Requirement for 'Offline Mode / Retry Logic' to fix this forever."

---

## 🟢 SCENARIO 6: The "API Integration" (Technical Spec)
**Context**: You need to integrate with a 3rd party Payment Gateway.
**Goal**: Write a tech spec for developers.

**The Chain:**
1.  **`@ba-elicitation`**: "Analyze this Stripe API Documentation URL. Summary the key constraints."
2.  **`@ba-process`**: "Draw the Sequence Diagram for a Successful Payment."
3.  **`@ba-nfr`**: "Define the error handling and timeout SLAs for this integration."
4.  **`@ba-writing`**: "Write the 'Payment Failed' User Story including specific Error Codes."

---

## 🟡 SCENARIO 7: The "Visual UX Design" (Screen First)
**Context**: You have a screenshot/mockup of a UI. You need requirements.
**Goal**: Generate specs from visual input.

**The Chain:**
1.  **`@ba-writing`**: "(Drag Image) Scan this UI. List every button, field, and interaction state."
2.  **`@ba-validation`**: "Compare this UI list against our standard Accessibility (WCAG) NFRs. What is missing?"
    *   *(Agent notes: 'Missing Alt Text', 'Contrast too low')*
3.  **`@ba-writing`**: "Draft the 'View Profile' Use Case specification based on the corrected list."

---

## 🔴 SCENARIO 8: The "Compliance Audit" (The Paperwork)
**Context**: The Auditors are coming. They need proof that "Requirement 1.2" was tested.
**Goal**: Pass the audit.

**The Chain:**
1.  **`@ba-traceability`**: "Scan all my markdown files. Generate a Traceability Matrix (Requirement -> Test Case)."
    *   *(Agent uses Grep to verify links)*
2.  **`@ba-validation`**: "Identify any Requirement that DOES NOT have a linked Test Case."
3.  **`@ba-export`**: "Export this Matrix to a formal DOCX using the 'Bank Template'."

---

## 🔵 SCENARIO 9: The "Innovative Pivot" (The Lab)
**Context**: Metrics show users are dropping off at the "Sign Up" page.
**Goal**: Propose a fix and prove it works.

**The Chain:**
1.  **`@ba-metrics`**: "Analyze these drop-off numbers. Is this variation normal?"
2.  **`@ba-innovation`**: "Propose 3 A/B tests to improve Sign-Up conversion. Suggest a Radical option."
    *   *(Agent suggests 'Social Login' or 'Magic Link')*
3.  **`@ba-solution`**: "Calculate the potential Revenue lift if conversion improves by 2%."

---

## 🟣 SCENARIO 10: The "Vendor Selection" (RFP)
**Context**: We need to buy a CRM. Salesforce vs HubSpot.
**Goal**: Make a data-driven choice.

**The Chain:**
1.  **`@ba-elicitation`**: "Draft 10 questions for the RFP (Request for Proposal) focusing on Security and Customization."
2.  **`@ba-prioritization`**: "Here are the answers from Salesforce and HubSpot. Rank them based on our 'Must Have' criteria."
3.  **`@ba-solution`**: "Compare the 3-year TCO (Total Cost of Ownership) of both options."

---

**Tip**: You can copy-paste these scenario prompts directly into the Antigravity chat!

---

## 🔁 SCENARIO 11: The "Validation Rejection Loop" (Quality Gate)
**Context**: `@ba-validation` has rejected a draft. The team needs to fix and re-submit.
**Goal**: Iterate until the Health Score passes the quality gate (≥ 80).

**The Chain:**
1.  **`@ba-validation`**: "Review these User Stories." → Health Score: 45. Critical defects found.
2.  **`@ba-writing`**: "Fix these 5 defects flagged by validation: [list from defect report]."
3.  **`@ba-validation`**: "Re-review the fixed stories." → Health Score: 85. Passed.
4.  **`@ba-export`**: "Package the validated stories for stakeholder review."

**Key Rule**: Max 3 iterations. If still failing after 3, escalate to `@ba-master` for strategy reassessment.

---

## 🔄 SCENARIO 12: The "Strategic Pivot" (New in v2.7)
**Context**: Market conditions changed. The project needs to re-evaluate its strategic direction.
**Goal**: Reassess strategy and realign requirements.

**The Chain:**
1.  **`@ba-strategy`**: "Re-run PESTLE analysis with new market data: [context]."
2.  **`@ba-systems`**: "Map the ripple effects of this strategic change on the system."
3.  **`@ba-traceability`**: "Calculate blast radius — which requirements are affected?"
4.  **`@ba-prioritization`**: "Re-prioritize the backlog given the new strategic direction."
5.  **`@ba-facilitation`**: "Plan a stakeholder workshop to communicate the pivot."
