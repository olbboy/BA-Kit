# BA-Kit Prompt Library / Thư Viện Prompt

> Copy-paste ready. Thay [placeholder] bằng context thực tế.
> *Copy-paste ready. Replace [placeholder] with your actual context.*

---

## Phase 1: Discovery & Elicitation / Khám Phá & Thu Thập Yêu Cầu

### 1.1 Stakeholder Interview — Opening
**Agent**: `@ba-elicitation`

> Tôi cần phỏng vấn [stakeholder role] về [topic/feature].
> Bắt đầu bằng câu hỏi mở để hiểu bức tranh toàn cảnh, sau đó đào sâu vào chi tiết.
> Ngữ cảnh dự án: [1-2 câu mô tả project].

**Expected Output**: 10-15 câu hỏi phỏng vấn theo Funnel pattern (Open → Probing → Closed)
**Power Combo**: Output → `@ba-writing` để chuyển thành specs

---

### 1.2 Stakeholder Interview — Deep Dive (Edge Cases)
**Agent**: `@ba-elicitation`

> Đây là transcript/notes từ buổi phỏng vấn trước:
> [paste notes]
>
> Tìm tất cả edge cases, exception flows, và câu hỏi chưa được trả lời.
> Tạo danh sách follow-up questions theo prioritized order.

**Expected Output**: Danh sách gaps + follow-up questions
**Variant**: Thêm "Format output as a table: Question | Why Important | Stakeholder to Ask"

---

### 1.3 Competitor Analysis
**Agent**: `@ba-strategy`

> Phân tích cạnh tranh cho [product/feature].
> Competitors: [list 3-5 competitors].
>
> Phân tích theo: Feature comparison, Pricing, UX strengths/weaknesses, Market positioning.
> Output dạng bảng so sánh (Feature Matrix).

**Expected Output**: Competitive feature matrix + gap analysis
**Power Combo**: Output → `@ba-elicitation` để validate với stakeholders

---

### 1.4 As-Is Process Discovery
**Agent**: `@ba-process`

> Mô tả quy trình hiện tại cho [process name]:
> [paste description hoặc attach screenshot]
>
> Phân tích:
> 1. Vẽ As-Is process (BPMN notation)
> 2. Xác định bottlenecks và waste (Lean 8 Wastes)
> 3. Đề xuất To-Be improvements

**Expected Output**: As-Is BPMN + bottleneck analysis + improvement suggestions
**Power Combo**: Output → `@ba-writing` → Feature Requirements

---

### 1.5 Stakeholder Mapping
**Agent**: `@ba-identity`

> Dự án: [project name]
> Liệt kê stakeholders: [list names/roles]
>
> Tạo:
> 1. Power/Interest Grid (4 quadrants)
> 2. RACI Matrix cho phase hiện tại
> 3. Communication strategy cho mỗi stakeholder group

**Expected Output**: Stakeholder map + RACI + communication recommendations

---

## Phase 2: Analysis & Specification / Phân Tích & Đặc Tả

### 2.1 User Story Writing — Basic
**Agent**: `@ba-writing`

> Viết User Stories cho [feature/module name].
> Context: [1-2 câu mô tả]
> Target user: [persona]
>
> Format: As a [user], I want [action] so that [benefit].
> Mỗi story kèm Acceptance Criteria (Gherkin: Given/When/Then).

**Expected Output**: 5-10 User Stories với Gherkin AC

---

### 2.2 User Story Writing — Advanced (Edge Cases + NFR)
**Agent**: `@ba-writing`

> Viết User Stories chi tiết cho [feature name]:
> [paste existing basic stories hoặc raw requirements]
>
> Cho mỗi story:
> 1. Happy path AC (Gherkin)
> 2. Sad path / Error scenarios (min 2 per story)
> 3. Edge cases (empty input, max length, concurrent access)
> 4. NFR constraints inline (performance, security)
> 5. Test data suggestions

**Expected Output**: Detailed stories với happy + sad + edge cases
**Power Combo**: Output → `@ba-validation` review

---

### 2.3 PRD Drafting
**Agent**: `@ba-writing`

> Tạo PRD cho [product/feature name].
> Dùng template từ `templates/prd_template.md`.
>
> Thông tin:
> - Problem: [1-2 câu]
> - Target users: [personas]
> - Core features: [list 3-5]
> - Success metrics: [1-2 KPIs]
> - Timeline: [deadline hoặc sprint count]
>
> Điền đủ 12 sections. Đánh dấu [TBD] cho phần chưa có data.

**Expected Output**: PRD draft (12 sections)
**Power Combo**: Output → `@ba-prioritization` (MoSCoW features) → `@ba-nfr` (NFR section)

---

### 2.4 BRD Drafting
**Agent**: `@ba-writing`

> Tạo BRD cho initiative [name].
> Dùng template từ `templates/brd_template.md`.
>
> Business context: [context]
> Problem statement: [problem]
> Proposed solution: [high-level solution]
> Expected ROI: [estimate hoặc "calculate for me"]

**Expected Output**: BRD draft (14 sections)
**Power Combo**: Output → `@ba-solution` (ROI verification with Python)

---

### 2.5 Use Case Specification
**Agent**: `@ba-writing`

> Viết Use Case cho [use case name].
> Primary Actor: [actor]
> System: [system name]
>
> Include:
> 1. Preconditions
> 2. Main Success Scenario (step by step)
> 3. Extensions (alternative flows)
> 4. Exception flows
> 5. Postconditions
> 6. Business Rules triggered

**Expected Output**: Structured use case specification

---

### 2.6 NFR Definition (ISO 25010)
**Agent**: `@ba-nfr`

> Định nghĩa Non-Functional Requirements cho [system/feature] theo ISO 25010.
>
> Context:
> - Users: [count + geographic distribution]
> - Data sensitivity: [High/Medium/Low]
> - Availability: [24/7 or business hours]
> - Compliance: [GDPR, SOC2, PDPA, etc.]
>
> Output cho 8 quality characteristics (ISO 25010):
> Performance, Compatibility, Usability, Reliability,
> Security, Maintainability, Portability, Functional Suitability.

**Expected Output**: NFR specification table với measurable targets
**Power Combo**: Output → paste into PRD Section 8

---

### 2.7 Data Dictionary
**Agent**: `@ba-writing`

> Tạo Data Dictionary cho [module/feature].
> Entities: [list entities hoặc paste ERD description]
>
> Cho mỗi field:
> - Field Name, Data Type, Length, Required (Y/N)
> - Validation Rules
> - Default Value
> - Sample Data
> - Source System (if integration)

**Expected Output**: Data dictionary table
**Power Combo**: Output → `@ba-validation` verify data types + constraints

---

## Phase 3: Validation & Quality / Kiểm Tra & Đảm Bảo Chất Lượng

### 3.1 Spec Review (The Roast)
**Agent**: `@ba-validation`

> Review đặc tả sau. Tìm mọi vấn đề:
> [paste spec]
>
> Đánh giá theo:
> 1. INVEST criteria (cho User Stories)
> 2. Completeness — thiếu edge case nào?
> 3. Consistency — có mâu thuẫn nội bộ?
> 4. Testability — mỗi requirement có test được không?
> 5. Ambiguity — từ nào mập mờ? (e.g., "fast", "user-friendly", "easy")
>
> Output: Health Score (0-100) + Defect List.

**Expected Output**: Health Score + categorized defect list
**Power Combo**: Defects → `@ba-writing` fix → re-run validation

---

### 3.2 INVEST Criteria Check
**Agent**: `@ba-validation`

> Check User Stories sau theo INVEST:
> [paste stories]
>
> Cho mỗi story đánh giá:
> I - Independent: có phụ thuộc story khác không?
> N - Negotiable: có rigid quá không?
> V - Valuable: user value rõ ràng?
> E - Estimable: team có thể estimate không?
> S - Small: fit trong 1 sprint không?
> T - Testable: AC có verify được không?
>
> Flag stories fail > 2 criteria.

**Expected Output**: INVEST scorecard per story

---

### 3.3 Traceability Verification
**Agent**: `@ba-traceability`

> Verify traceability cho [project/module]:
>
> Business Objectives: [list OBJ-01, OBJ-02...]
> Features: [list F-001, F-002...]
> User Stories: [list US-001, US-002...]
>
> Check:
> 1. Forward trace: mỗi objective có feature support?
> 2. Backward trace: mỗi story trace về objective?
> 3. Orphans: feature/story nào không trace được?
> 4. Coverage gaps: objective nào chưa có feature?

**Expected Output**: Traceability matrix + gap report

---

### 3.4 Edge Case Discovery
**Agent**: `@ba-validation`

> Feature: [feature description]
>
> Generate edge cases cho:
> 1. Input boundaries (empty, max, special characters, Unicode)
> 2. Concurrency (2 users cùng lúc)
> 3. State transitions (mid-operation disconnect, timeout)
> 4. Permission combinations (admin vs user vs guest)
> 5. Data edge cases (zero amount, negative, overflow)
> 6. Integration failures (API down, timeout, malformed response)
>
> Output: table với Edge Case | Expected Behavior | Priority.

**Expected Output**: Edge case catalog with expected behaviors

---

## Phase 4: Design & Prototype / Thiết Kế & Prototype

### 4.1 UI Spec from Screenshot
**Agent**: `@ba-writing`

> (Attach screenshot/mockup)
>
> Scan UI này. Trích xuất:
> 1. Danh sách tất cả fields (Label, Type, Validation Rules)
> 2. Buttons và actions (Click → API call / Navigate)
> 3. Navigation flow (Back, Cancel, Submit destinations)
> 4. Error states (field validation, API errors)
> 5. Loading states
> 6. Responsive behavior (nếu suy luận được)

**Expected Output**: Field specification table + button action map

---

### 4.2 Stitch MCP — Screen from Spec
**Agent**: Direct MCP call

> generate_screen_from_text:
>   projectId: "[id]"
>   prompt: "Create a [screen type] screen with:
>     - [element 1]: [description]
>     - [element 2]: [description]
>     - [element 3]: [description]
>     Style: [Material Design 3 / iOS HIG / custom]
>     Colors: [primary color hex]
>     Layout: [single column / grid / tabs]"
>   deviceType: "MOBILE" or "DESKTOP"

**Expected Output**: Generated UI screen
**Power Combo**: Output → `@ba-validation` review against spec

---

### 4.3 Design System Definition
**Agent**: Direct MCP call

> create_design_system:
>   projectId: "[id]"
>   designSystem:
>     displayName: "[Brand Name] Design System"
>     colorScheme:
>       preset: "TONAL_SPOT"
>       seedColor: "[hex, e.g., #1A73E8]"
>     typography:
>       fontFamily: "[Inter / Roboto / custom]"
>     shape:
>       cornerRadius: "ROUNDED"
>     appearance:
>       mode: "LIGHT" or "DARK"

**Expected Output**: Design system tokens applied across project

---

### 4.4 Accessibility Audit Prompt
**Agent**: `@ba-nfr`

> Audit accessibility cho [screen/feature]:
> (Attach screenshot hoặc paste component list)
>
> Check theo WCAG 2.1 Level AA:
> 1. Color contrast (text vs background — min 4.5:1)
> 2. Focus indicators (keyboard navigation)
> 3. Alt text (images, icons)
> 4. Form labels (every input has associated label)
> 5. Error identification (programmatic, not color-only)
> 6. Touch targets (min 44x44px for mobile)

**Expected Output**: Accessibility compliance report + fix recommendations

---

## Phase 5: Delivery & Publishing / Bàn Giao & Xuất Bản

### 5.1 Jira Ticket Creation
**Agent**: `@ba-jira`

> Tạo Jira tickets từ User Stories sau trong project [PROJECT_KEY]:
> [paste validated stories]
>
> Cho mỗi ticket:
> - Summary = User Story title
> - Description = Full story + AC (Gherkin)
> - Issue Type = Story
> - Priority = dựa trên MoSCoW mapping
> - Labels = [module name]
> - Sprint = [Sprint N hoặc Backlog]

**Expected Output**: Jira tickets created with full AC
**Prerequisite**: Stories validated by `@ba-validation` (Health Score ≥ 80)

---

### 5.2 Confluence Publishing
**Agent**: `@ba-confluence`

> Publish document sau lên Confluence:
> Space: [SPACE_KEY]
> Parent page: [parent page title]
> Title: [document title]
> Labels: [label1, label2]
>
> Content:
> [paste markdown content]
>
> Format: Convert markdown → Confluence XHTML.
> Preserve: tables, code blocks, headings, links.

**Expected Output**: Confluence page created with proper formatting

---

### 5.3 Stakeholder Presentation Summary
**Agent**: `@ba-writing`

> Tạo Executive Summary (1-2 pages) từ PRD/BRD sau:
> [paste full document]
>
> Target audience: [C-level / VP / Team Lead]
> Presentation format: [Slide deck bullets / Email / Meeting brief]
>
> Include:
> 1. Problem (1 sentence)
> 2. Solution (1 sentence)
> 3. Key metrics (3 numbers)
> 4. Timeline (key milestones only)
> 5. Ask (budget/approval/resources needed)

**Expected Output**: Concise executive summary, presentation-ready

---

### 5.4 Sprint Planning Support
**Agent**: `@ba-agile`

> Sprint Planning cho Sprint [N]:
> Backlog items: [paste prioritized list]
> Team capacity: [X story points / X developer-days]
> Sprint duration: [2 weeks]
>
> Help:
> 1. Recommend sprint goal (1 sentence)
> 2. Select stories that fit capacity
> 3. Identify dependencies between selected stories
> 4. Flag risks for this sprint
> 5. Suggest acceptance criteria verification approach

**Expected Output**: Sprint plan with goal + selected stories + dependency map

---

## Phase 6: Strategy & Optimization / Chiến Lược & Tối Ưu

### 6.1 SWOT Analysis
**Agent**: `@ba-strategy`

> Chạy SWOT analysis cho [product/company/initiative]:
>
> Context:
> - Industry: [industry]
> - Key competitors: [list]
> - Current market position: [description]
> - Recent changes: [market shifts, new regulations, tech trends]
>
> Output: SWOT matrix (Strengths, Weaknesses, Opportunities, Threats)
> + Strategic implications + Recommended actions per quadrant.

**Expected Output**: SWOT matrix + action items

---

### 6.2 PESTLE Analysis
**Agent**: `@ba-strategy`

> PESTLE analysis cho [product/market entry/expansion]:
>
> Market: [country/region]
> Industry: [industry]
>
> Phân tích 6 factors:
> P - Political: [regulations, government stability]
> E - Economic: [GDP, inflation, exchange rates]
> S - Social: [demographics, culture, trends]
> T - Technological: [tech adoption, infrastructure]
> L - Legal: [laws, compliance requirements]
> E - Environmental: [sustainability, climate impact]

**Expected Output**: PESTLE factor analysis + risk/opportunity ranking

---

### 6.3 Root Cause Analysis (5 Whys)
**Agent**: `@ba-root-cause`

> Vấn đề: [problem statement]
> Frequency: [how often it occurs]
> Impact: [business impact]
>
> Chạy 5 Whys analysis:
> Why 1: Tại sao [problem] xảy ra?
> → Tiếp tục đào sâu 5 layers.
>
> Kết hợp Fishbone diagram (Ishikawa):
> Categories: People, Process, Technology, Policy, Environment.
>
> Output: Root cause + corrective actions + preventive actions.

**Expected Output**: 5 Whys chain + Fishbone + action plan
**Power Combo**: Output → `@ba-writing` → create Fix Spec

---

### 6.4 ROI Calculation
**Agent**: `@ba-solution`

> Tính ROI cho [investment/feature]:
>
> Costs:
> - Development: [estimate]
> - Infrastructure: [monthly cost]
> - Licenses: [annual cost]
> - Training: [one-time cost]
>
> Benefits:
> - Revenue increase: [estimate or formula]
> - Cost reduction: [estimate]
> - Time savings: [hours/week × rate]
>
> Calculate:
> 1. ROI % (3-year horizon)
> 2. NPV (discount rate: [X]%)
> 3. Payback period (months)
>
> Dùng Python. Show calculations.

**Expected Output**: Python-verified ROI, NPV, payback period with formulas

---

### 6.5 Workshop Planning
**Agent**: `@ba-facilitation`

> Lên kế hoạch workshop [type]:
> - Type: [Requirements Discovery / Design Thinking / Retrospective / Prioritization]
> - Duration: [X hours]
> - Participants: [count + roles]
> - Objective: [1 sentence]
> - Constraints: [remote/in-person, tools available]
>
> Output:
> 1. Agenda (time-boxed activities)
> 2. Materials needed
> 3. Facilitation techniques for each activity
> 4. Expected outputs
> 5. Follow-up actions

**Expected Output**: Detailed workshop agenda + facilitation guide

---

### 6.6 System Causal Loop Analysis
**Agent**: `@ba-systems`

> Vấn đề lặp đi lặp lại: [recurring problem]
>
> Context: [system description — actors, processes, feedback loops]
>
> Phân tích:
> 1. Vẽ Causal Loop Diagram (CLD)
> 2. Identify reinforcing loops (R) và balancing loops (B)
> 3. Tìm Leverage Points (điểm đòn bẩy)
> 4. Xác định System Archetype (Fixes that Fail? Shifting the Burden? etc.)
> 5. Đề xuất interventions tại leverage points

**Expected Output**: CLD + archetype identification + intervention strategy

---

## Index — Quick Lookup / Tra Cứu Nhanh

| Cần làm gì | Prompt # | Agent |
|-------------|----------|-------|
| Phỏng vấn stakeholder | 1.1, 1.2 | `@ba-elicitation` |
| Phân tích đối thủ | 1.3 | `@ba-strategy` |
| Document quy trình hiện tại | 1.4 | `@ba-process` |
| Map stakeholders | 1.5 | `@ba-identity` |
| Viết User Stories | 2.1, 2.2 | `@ba-writing` |
| Viết PRD | 2.3 | `@ba-writing` |
| Viết BRD | 2.4 | `@ba-writing` |
| Viết Use Case | 2.5 | `@ba-writing` |
| Định nghĩa NFR | 2.6 | `@ba-nfr` |
| Tạo Data Dictionary | 2.7 | `@ba-writing` |
| Review/Roast spec | 3.1 | `@ba-validation` |
| Check INVEST | 3.2 | `@ba-validation` |
| Verify traceability | 3.3 | `@ba-traceability` |
| Tìm edge cases | 3.4 | `@ba-validation` |
| Scan UI → specs | 4.1 | `@ba-writing` |
| Tạo screen (Stitch) | 4.2 | Stitch MCP |
| Tạo design system | 4.3 | Stitch MCP |
| Audit accessibility | 4.4 | `@ba-nfr` |
| Tạo Jira tickets | 5.1 | `@ba-jira` |
| Publish Confluence | 5.2 | `@ba-confluence` |
| Tóm tắt cho management | 5.3 | `@ba-writing` |
| Sprint planning | 5.4 | `@ba-agile` |
| SWOT analysis | 6.1 | `@ba-strategy` |
| PESTLE analysis | 6.2 | `@ba-strategy` |
| Root cause (5 Whys) | 6.3 | `@ba-root-cause` |
| Tính ROI | 6.4 | `@ba-solution` |
| Lên kế hoạch workshop | 6.5 | `@ba-facilitation` |
| Phân tích hệ thống | 6.6 | `@ba-systems` |
