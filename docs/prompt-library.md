# BA-Kit Prompt Library

> 48 copy-paste prompts tổ chức theo vòng đời BA. Thay `[placeholder]` bằng context thực tế rồi dán vào chat.

**Cách dùng:** Copy prompt → thay nội dung trong `[...]` → gửi.

---

## Phase 1: Discovery & Strategy (6 prompts)

### 1. Route Request
**Agent:** `@ba-master`

> Tôi muốn xây dựng `[tên hệ thống/tính năng]`. Phân tích yêu cầu và đề xuất chuỗi agent phù hợp để bắt đầu.

**Output:** Workflow chain gợi ý, agent sequence, dependencies.

---

### 2. Stakeholder Mapping
**Agent:** `@ba-identity`

> Dự án `[tên dự án]` phục vụ `[ngành/lĩnh vực]`. Tạo RACI matrix và Power/Interest grid cho các stakeholder chính. Đề xuất communication plan cho từng nhóm.

**Output:** RACI matrix, Power/Interest grid, communication plan template.

---

### 3. SWOT / PESTLE Analysis
**Agent:** `@ba-strategy`

> Thực hiện SWOT + PESTLE analysis cho `[tên dự án/tính năng]`. Bối cảnh: `[thị trường/ngành/khu vực địa lý]`. Ưu tiên yếu tố ảnh hưởng lớn nhất đến khả năng thành công.

**Output:** SWOT matrix, PESTLE breakdown, strategic recommendations.

---

### 4. Interview Prep
**Agent:** `@ba-questioning`

> Tôi có meeting với `[vai trò stakeholder]` về `[chủ đề]` vào `[ngày/giờ]`. Mục tiêu: `[quyết định cần đạt / thông tin cần khai thác]`. Chuẩn bị question set 3-tier (mở → thăm dò → xác nhận) cho tôi.

**Output:** Question set 3-tier, backup questions, red flags cần chú ý.

---

### 5. Feedback Loop Analysis
**Agent:** `@ba-systems`

> Phân tích các feedback loop và unintended consequences tiềm ẩn khi triển khai `[tên tính năng/quy trình]` trong bối cảnh `[mô tả hệ thống hiện tại]`.

**Output:** Causal loop diagram (text), risk scenarios, mitigation suggestions.

---

### 6. Persona Creation
**Agent:** `@ba-ux`

> Tạo Persona đầy đủ cho user type `[mô tả user]` trong dự án `[tên dự án]`. Bao gồm demographics, goals, frustrations, behaviors, và accessibility needs.

**Output:** Persona canvas, User Journey Map, pain points, opportunities.

**Power combo:** `@ba-questioning` (interview prep) → `@ba-ux` (persona) → `@ba-elicitation` (deep dive).

---

## Phase 2: Elicitation (5 prompts)

### 7. Funnel Interview
**Agent:** `@ba-elicitation`

> Phỏng vấn tôi theo phương pháp Funnel để khai thác requirements cho `[tên tính năng]`. Bắt đầu từ câu hỏi mở rộng nhất, thu hẹp dần đến chi tiết implementation.

**Output:** Structured requirements list, assumption log, open questions.

---

### 8. Edge Case Deep Dive
**Agent:** `@ba-elicitation`

> Tôi là `[vai trò stakeholder]`. Đặt câu hỏi 5W1H + worst-case scenarios để xác định nhu cầu thật sự đằng sau yêu cầu: "`[mô tả yêu cầu thô]`". Đừng accept câu trả lời đầu tiên.

**Output:** Refined requirements, edge cases catalog, hidden constraints.

---

### 9. Workshop Design
**Agent:** `@ba-facilitation`

> Thiết kế chương trình workshop `[thời lượng]` để thu thập requirements cho `[tên module/tính năng]` với `[số lượng]` người tham gia gồm `[danh sách vai trò]`. Bao gồm agenda, activities, và facilitation guide.

**Output:** Workshop agenda, activity templates, decision log template.

---

### 10. Assumption Challenge
**Agent:** `@ba-questioning`

> Review tài liệu sau và liệt kê tất cả assumptions ẩn cần được challenge, kèm câu hỏi cụ thể để validate từng assumption: `[dán nội dung tài liệu]`

**Output:** Assumption log, challenge questions, validation criteria.

---

### 11. User Story Map
**Agent:** `@ba-agile`

> Tạo User Story Map cho MVP của `[tên sản phẩm/tính năng]`. Phân chia theo backbone activities và walking skeleton. Đề xuất release slicing cho 3 sprint đầu.

**Output:** Story map (text/table), backbone activities, walking skeleton, sprint plan.

---

## Phase 3: Writing & Modeling (8 prompts)

### 12. User Story (INVEST + Gherkin)
**Agent:** `@ba-writing`

> Viết User Story đầy đủ cho tính năng: "`[mô tả tính năng]`". Bao gồm INVEST analysis, Acceptance Criteria theo format Gherkin (Given/When/Then), RBAC matrix, và edge cases quan trọng.

**Output:** User Story hoàn chỉnh, Gherkin AC, RBAC table, edge case list.

---

### 13. BRD
**Agent:** `@ba-writing`

> Tạo Business Requirements Document (BRD) cho `[tên dự án]`. Context: `[mô tả ngắn về mục tiêu kinh doanh, phạm vi, và constraints]`. Dùng template chuẩn với đầy đủ sections.

**Output:** BRD hoàn chỉnh với executive summary, business objectives, scope, stakeholders, requirements.

---

### 14. SRS (IEEE 29148)
**Agent:** `@ba-writing`

> Viết Software Requirements Specification (IEEE 29148) cho module `[tên module]`. Danh sách tính năng cần cover: `[liệt kê tính năng]`. Phân biệt rõ functional vs non-functional requirements.

**Output:** SRS đúng chuẩn IEEE 29148 với functional requirements, NFR, constraints, và assumptions.

---

### 15. API Specification
**Agent:** `@ba-writing`

> Thiết kế API Specification cho endpoint `[GET/POST/PUT/DELETE]` `[path]`. Bao gồm: request/response schema, error codes, rate limiting, authentication method, và example payloads.

**Output:** API spec (OpenAPI-style), error code table, example curl commands.

---

### 16. BPMN Process Diagram
**Agent:** `@ba-process`

> Vẽ BPMN diagram dạng Mermaid cho quy trình: `[mô tả quy trình nghiệp vụ]`. Swimlanes theo vai trò: `[danh sách vai trò]`. Bao gồm cả happy path và exception flows.

**Output:** Mermaid BPMN source, swimlane diagram, exception handling notes.

---

### 17. ERD + Data Dictionary
**Agent:** `@ba-data`

> Thiết kế ERD (Mermaid erDiagram) + Data Dictionary cho module `[tên module]`. Entities chính: `[liệt kê entities]`. Bao gồm constraints, indexes, audit fields, và business rules theo từng field.

**Output:** ERD Mermaid source, Data Dictionary table, constraints list.

**Power combo:** `@ba-data` (ERD) → `@ba-business-rules` (decision tables) → `@ba-writing` (SRS data section).

---

### 18. Decision Table
**Agent:** `@ba-business-rules`

> Tạo Decision Table cho quy trình `[mô tả quy trình]`. Liệt kê tất cả conditions, actions. Kiểm tra completeness (không có rule gaps) và conflicts (không có contradictions).

**Output:** Decision table, completeness check report, conflict detection results.

---

### 19. Visual UI Scan
**Agent:** `@ba-writing`

> `@[image]` Đây là mockup/wireframe. Phân tích và chuyển đổi thành Field Specifications đầy đủ: tên field, kiểu dữ liệu, validation rules, error messages, và interaction states cho từng element UI.

**Output:** Field Spec table, validation rules, error state catalog.

**Power combo:** `@ba-writing` (visual scan) → `@ba-validation` (INVEST check) → `@ba-jira` (tạo tickets).

---

## Phase 4: Validation & Testing (6 prompts)

### 20. INVEST Check + Ambiguity Scan
**Agent:** `@ba-validation`

> Đây là User Story: `[dán nội dung US]`. Thực hiện INVEST check đầy đủ và Ambiguity Scan. Trả về Health Score (0-100) và danh sách defects theo severity (Critical/Major/Minor).

**Output:** Health Score, INVEST breakdown, ambiguity list với đề xuất thay thế.

---

### 21. Quality Gate Scoring
**Agent:** `@ba-quality-gate`

> Đánh giá artifact sau theo thang điểm 8 chiều (PASS/CONDITIONAL/REJECT): `[dán nội dung BRD/SRS/US]`. Trả về score chi tiết từng dimension và action items để đạt PASS.

**Output:** 8-dimension score card, gate decision (PASS/CONDITIONAL/REJECT), remediation list.

---

### 22. Cross-Artifact Consistency Check
**Agent:** `@ba-consistency`

> Kiểm tra tính nhất quán cross-artifact giữa: User Story `[US-XXX]`, API Spec `[tên endpoint]`, và DB Schema `[tên bảng]`. Báo cáo mọi mismatch và đề xuất resolution.

**Output:** Consistency report, mismatch table, resolution recommendations.

---

### 23. NFR (ISO 25010)
**Agent:** `@ba-nfr`

> Định nghĩa Non-Functional Requirements theo ISO 25010 cho tính năng `[tên tính năng]`. Tập trung: Performance, Security, Reliability. Mọi metric phải có threshold đo được (ví dụ: p95 < 200ms).

**Output:** NFR catalog với measurable thresholds, acceptance criteria cho từng NFR.

---

### 24. 7-Category Test Suite
**Agent:** `@ba-test-gen`

> Sinh test suite đầy đủ từ Acceptance Criteria của `[US-XXX/tên tính năng]`. Cover 7 categories: Happy Path, Edge Case, Error Handling, Security, Concurrency, Data Validation, Performance.

**Output:** Test suite table với test ID, category, steps, expected results.

---

### 25. UAT Script
**Agent:** `@ba-test-gen`

> Tạo UAT script cho tính năng `[tên tính năng]` dành cho `[vai trò người dùng]`. Bao gồm: preconditions, test steps, expected results, pass/fail criteria, và rollback procedure.

**Output:** UAT script hoàn chỉnh, test data requirements, sign-off checklist.

---

## Phase 5: Visualization (3 prompts)

### 26. Flowchart BPMN
**Agent:** `@ba-diagram`

> Vẽ flowchart BPMN với swimlanes cho quy trình `[mô tả quy trình]`. Actors: `[danh sách vai trò]`. Output cả Mermaid source và hướng dẫn embed Confluence.

**Output:** Mermaid flowchart source, Confluence macro embedding code.

---

### 27. ERD (Mermaid)
**Agent:** `@ba-diagram`

> Vẽ ERD (Mermaid erDiagram) cho module `[tên module]`. Entities: `[danh sách entities]`. Include PK/FK, cardinality, và data types chính.

**Output:** Mermaid erDiagram source, relationship descriptions.

---

### 28. Sequence Diagram
**Agent:** `@ba-diagram`

> Vẽ sequence diagram cho luồng `[mô tả interaction]`. Actors: `[danh sách]`. Bao gồm happy path, error handling, và timeout scenarios. Confluence-ready format.

**Output:** Mermaid sequence diagram source, interaction notes.

---

## Phase 6: Communication & Change (4 prompts)

### 29. Status Report
**Agent:** `@ba-communication`

> Viết status report Sprint `[N]` cho `[tên project]`. Audience: `[Sponsor/PM/Dev/Stakeholder]`. Dữ liệu: `[hoàn thành X US, block Y items, risk Z]`. Tone: professional, action-oriented.

**Output:** Status report theo format chuẩn, next actions, escalation items.

---

### 30. Executive Summary
**Agent:** `@ba-communication`

> Tóm tắt tài liệu sau thành Executive Summary 1 trang cho C-suite. Chỉ giữ business impact, key decisions needed, và risks: `[dán BRD/SRS hoặc mô tả nội dung]`

**Output:** 1-page executive summary, key decisions table, risk highlights.

---

### 31. Meeting Minutes
**Agent:** `@ba-communication`

> Soạn meeting minutes cho cuộc họp vừa kết thúc. Participants: `[danh sách]`. Nội dung thảo luận: `[dán notes thô]`. Bao gồm decisions made, action items (ai làm gì, deadline), và open questions.

**Output:** Formatted meeting minutes, action items table, follow-up schedule.

---

### 32. ADKAR Assessment
**Agent:** `@ba-change`

> Thực hiện ADKAR assessment cho `[nhóm user]` khi chuyển từ `[hệ thống/quy trình cũ]` sang `[hệ thống/quy trình mới]`. Xác định barrier point và đề xuất change management actions cụ thể.

**Output:** ADKAR scorecard, barrier analysis, change management action plan.

---

## Phase 7: Integration (4 prompts)

### 33. Create Jira Tickets
**Agent:** `@ba-jira`

> Tạo Jira tickets từ các User Stories sau: `[dán danh sách US]`. Ánh xạ: Story Title → Summary, Acceptance Criteria → Description, Priority → Priority field. Kiểm tra duplicates trước khi tạo.

**Output:** Jira ticket list với fields đầy đủ, duplicate check report.

---

### 34. Sync Backlog
**Agent:** `@ba-jira`

> Đồng bộ backlog: import `[danh sách stories]` vào Sprint `[số]`. Gán cho team member theo RACI matrix `[mô tả RACI]`. Set story points dựa trên complexity estimate.

**Output:** Sprint backlog updated, assignment list, unresolved items report.

---

### 35. Publish Confluence Page
**Agent:** `@ba-confluence`

> Publish `[tên tài liệu: BRD/SRS/Module Spec]` lên Confluence space `[tên space]`. Format Markdown → XHTML. Tạo page hierarchy: `[Project > Module > Document]`. Kiểm tra duplicate pages.

**Output:** Confluence page URL, page hierarchy, version conflict report.

---

### 36. Create Requirements Wiki
**Agent:** `@ba-confluence`

> Tạo Requirements Wiki page cho `[tên tính năng]` trên Confluence: executive summary, stakeholder table, US list có link đến Jira, decision log, và open questions.

**Output:** Wiki page hoàn chỉnh với embedded Jira links, decision log table.

---

## Phase 8: Export & Closure (4 prompts)

### 37. Compile DOCX
**Agent:** `@ba-export`

> Compile toàn bộ artifacts của `[tên dự án]` thành DOCX bàn giao. Bao gồm: BRD, SRS, RTM, và Test Suite. Format theo chuẩn `[tên client/tổ chức]`. Kiểm tra cross-references trước khi export.

**Output:** DOCX package, table of contents, cross-reference validation report.

---

### 38. Full Health Audit
**Agent:** `@ba-auditor`

> Chạy full project health audit cho `[tên dự án]`. Output: executive dashboard gồm Coverage Score, Risk Heatmap, Quality Metrics, và danh sách open items phải xử lý trước closure.

**Output:** Audit dashboard, Coverage Score, Risk Heatmap, open items list.

---

### 39. RTM (Requirements Traceability Matrix)
**Agent:** `@ba-traceability`

> Tạo Requirements Traceability Matrix (RTM) đầy đủ: BRD → User Story → Acceptance Criteria → Test Case → Implementation. Highlight mọi requirement chưa có test coverage.

**Output:** RTM table, coverage gap report, untested requirements list.

---

### 40. Ingest Learnings
**Agent:** `@ba-wiki`

> Ingest lessons learned từ dự án `[tên dự án]` vào knowledge base. Source: `[retrospective notes / post-mortem report]`. Phân loại theo: Process, Technical, Communication, Stakeholder.

**Output:** Knowledge entries added, categorization summary, reusable templates extracted.

---

## Phase 9: Estimation & Prioritization (3 prompts)

### 41. MoSCoW Ranking
**Agent:** `@ba-prioritization`

> Áp dụng MoSCoW framework cho danh sách features sau: `[liệt kê features]`. Constraints: budget `[X]`, timeline `[Y sprint]`, team size `[Z]`. Justify từng classification với business impact.

**Output:** MoSCoW matrix, justification table, MVP scope recommendation.

---

### 42. Estimation Facilitation
**Agent:** `@ba-agile`

> Facilitate estimation session cho `[danh sách User Stories]`. Dùng Planning Poker scale. Bao gồm: complexity factors, dependency risks, và confidence level cho mỗi estimate.

**Output:** Story points table, complexity breakdown, velocity projection.

---

### 43. ROI Calculation
**Agent:** `@ba-solution`

> Tính ROI cho `[tên giải pháp/tính năng]`. Inputs: investment `[X VND/USD]`, expected benefits `[mô tả]`, timeframe `[Y tháng]`. So sánh với alternative `[mô tả alternative]`.

**Output:** ROI calculation, payback period, break-even analysis, recommendation.

---

## Phase 10: Problem Solving (5 prompts)

### 44. Root Cause Analysis (5 Whys + Fishbone)
**Agent:** `@ba-root-cause`

> Incident: `[mô tả vấn đề/defect cụ thể]`. Thực hiện 5 Whys và Fishbone diagram (6M: Man, Machine, Method, Material, Measurement, Mother Nature). Xác định root cause và preventive actions.

**Output:** 5 Whys chain, Fishbone diagram (text), root cause statement, preventive action plan.

---

### 45. Stakeholder Conflict Resolution
**Agent:** `@ba-conflict`

> `[Stakeholder A]` muốn `[yêu cầu A]`. `[Stakeholder B]` muốn `[yêu cầu B]`. Hai yêu cầu mâu thuẫn tại `[điểm xung đột cụ thể]`. Đề xuất win-win solution và negotiation strategy.

**Output:** Conflict analysis, win-win options, negotiation script, escalation path.

---

### 46. A/B Test Design
**Agent:** `@ba-innovation`

> Thiết kế A/B test cho `[tính năng/hypothesis]`. Control: `[hiện trạng]`. Variants: `[đề xuất thay đổi]`. Bao gồm: sample size, success metrics, duration, và statistical significance threshold.

**Output:** A/B test plan, sample size calculation, metrics dashboard template.

---

### 47. Feasibility Probing
**Agent:** `@ba-questioning`

> Dev team/stakeholder nói `[yêu cầu X]` "bất khả thi" / "quá phức tạp". Chuẩn bị câu hỏi feasibility probing để hiểu constraint cụ thể, tách "technical constraint" vs "effort concern", và tìm creative alternatives.

**Output:** Feasibility question set, constraint categorization, alternative options to explore.

---

### 48. Quality Dashboard
**Agent:** `@ba-metrics`

> Tạo Quality Dashboard cho `[tên project/sprint]`. Metrics cần track: Requirements Completeness, Defect Density, Test Coverage, Requirement Stability. Data hiện tại: `[dán data thô]`.

**Output:** Quality Dashboard (table/chart), trend analysis, quality gate thresholds.

---

## Power Combos (5 combos)

### Combo 1: Zero to BRD
Dùng khi bắt đầu dự án mới từ đầu, không có tài liệu gốc.

```
@ba-master [mô tả dự án ngắn]
→ @ba-strategy [SWOT/PESTLE]
→ @ba-elicitation [funnel interview]
→ @ba-writing [BRD + User Stories]
→ @ba-quality-gate [score và phê duyệt]
→ @ba-export [package bàn giao]
```

**Thời gian:** 2-4 giờ.

---

### Combo 2: Sprint-Ready Validation Pipeline
Dùng trước sprint planning để đảm bảo stories đủ chất lượng.

```
@ba-validation [US] → @ba-test-gen [validated AC] → @ba-consistency [US + API + DB] → @ba-quality-gate [full artifact set]
```

**Kết quả cần:** Health Score ≥ 80 trước khi chuyển dev.

---

### Combo 3: Screenshot to Jira
Dùng khi có mockup từ designer, cần tạo ticket nhanh cho dev.

```
@ba-writing @[image mockup] → @ba-validation [INVEST check] → @ba-test-gen [test cases] → @ba-jira [create tickets]
```

---

### Combo 4: Production Postmortem
Dùng sau khi phát hiện defect nghiêm trọng ở production.

```
@ba-root-cause [mô tả defect] → @ba-validation [requirements gốc] → @ba-metrics [trend analysis] → @ba-writing [corrected requirements]
```

---

### Combo 5: New Domain Discovery
Dùng khi bắt đầu module mới cần cả user research lẫn data design.

```
@ba-questioning [meeting prep] → @ba-ux [persona + journey] → @ba-elicitation [deep dive] → @ba-writing [US + AC] → @ba-data [ERD + data dictionary] → @ba-business-rules [decision tables]
```

---

> **Tip:** Tạo `CONTINUITY.md` ở root project (copy từ `.agent/templates/continuity-template.md`) để mọi agent tự đọc context — không cần nhắc lại project goal sau mỗi prompt.
