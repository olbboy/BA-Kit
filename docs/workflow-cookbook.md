# BA-Kit Workflow Cookbook

> 15 kịch bản thực tế — copy workflow chain, thay context là chạy được.

**Cách đọc:** Mỗi scenario có Chain (chuỗi agent), When to Use, Step-by-step, và Pro Tip.

---

## Scenario 1: Zero to BRD (Dự án mới từ đầu)

**Chain:** `master → strategy → elicitation → writing → validation → quality-gate → export`
**Thời gian:** 2-4 giờ

**When to Use:** Client có ý tưởng mơ hồ, chưa có tài liệu nào. Cần đi từ 0 đến BRD bàn giao được.

**Steps:**
1. `@ba-master [mô tả dự án 1-2 câu]` — nhận workflow chain gợi ý và prioritized questions
2. `@ba-strategy` — SWOT/PESTLE analysis, xác định strategic fit và constraints
3. `@ba-elicitation` — Funnel interview để khai thác requirements thực sự
4. `@ba-writing` — Viết BRD + User Stories từ output elicitation
5. `@ba-validation` — INVEST check, ambiguity scan, health score
6. `@ba-quality-gate` — 8-dimension scoring (target: PASS hoặc CONDITIONAL)
7. `@ba-export` — Compile DOCX package bàn giao

**Pro Tip:** Dùng `@ba-master` ở bước 1 để không bỏ sót agent nào cần thiết cho domain cụ thể.

---

## Scenario 2: Sprint Planning (Chuẩn bị sprint)

**Chain:** `writing → validation → elicitation → prioritization → jira`
**Thời gian:** 1-2 giờ

**When to Use:** Sprint bắt đầu trong 2 ngày. PO vừa dump raw requirements, cần groom backlog và đảm bảo stories "Ready".

**Steps:**
1. `@ba-writing [raw requirement dump]` — chuyển text thô thành User Stories có Gherkin AC
2. `@ba-validation [stories]` — INVEST check, flag ambiguous stories
3. `@ba-elicitation [ambiguous stories]` — sinh clarifying questions gửi PO
4. `@ba-prioritization [refined stories]` — MoSCoW, cắt scope nếu cần
5. `@ba-jira [validated stories]` — tạo tickets với fields đầy đủ, assign sprint

**Pro Tip:** Health Score ≥ 80 là điều kiện cần trước khi chuyển bất kỳ story nào sang dev.

---

## Scenario 3: Screenshot to Jira (Từ mockup đến ticket)

**Chain:** `writing (visual scan) → validation → test-gen → jira`
**Thời gian:** 30-60 phút

**When to Use:** Designer gửi mockup/wireframe, cần tạo Jira tickets nhanh mà không mất thông tin.

**Steps:**
1. `@ba-writing @[image mockup]` — scan UI, extract Field Specs, validation rules, interaction states
2. `@ba-validation [field specs]` — INVEST check, phát hiện gaps so với AC chuẩn
3. `@ba-test-gen [validated specs]` — sinh test cases cover 7 categories
4. `@ba-jira [specs + test cases]` — tạo tickets kèm test cases trong Description

**Pro Tip:** Chụp cả error states và empty states trong mockup để `@ba-writing` không bỏ sót.

---

## Scenario 4: Stakeholder War (Xung đột giữa các bên)

**Chain:** `identity → conflict → solution → facilitation`
**Thời gian:** 1-2 giờ

**When to Use:** Hai hoặc nhiều stakeholder có yêu cầu mâu thuẫn, đang block dự án.

**Steps:**
1. `@ba-identity [stakeholder profiles]` — map Power/Interest grid, xác định influence level của từng bên
2. `@ba-conflict [conflict description]` — phân tích root conflict, đề xuất win-win options
3. `@ba-solution [win-win options]` — tính ROI/TCO của từng option để có data-driven argument
4. `@ba-facilitation` — thiết kế conflict resolution workshop với agenda cụ thể

**Pro Tip:** Đừng đi thẳng vào `@ba-conflict` mà không có Power/Interest map — biết ai có quyền quyết định cuối cùng là critical.

---

## Scenario 5: Production Postmortem (Sự cố production)

**Chain:** `root-cause → validation → metrics → writing`
**Thời gian:** 1-3 giờ

**When to Use:** Defect nghiêm trọng được phát hiện ở production. Cần tìm root cause và ngăn tái phát.

**Steps:**
1. `@ba-root-cause [incident description]` — 5 Whys + Fishbone, xác định root cause thực sự
2. `@ba-validation [original requirements]` — so sánh implementation với AC gốc, phát hiện gap
3. `@ba-metrics [incident data]` — trend analysis, defect density, impact assessment
4. `@ba-writing` — viết corrected requirements và updated AC ngăn incident tái phát

**Pro Tip:** Yêu cầu `@ba-root-cause` phân loại root cause theo: Process gap, Communication gap, hay Technical gap — ba hướng fix khác nhau hoàn toàn.

---

## Scenario 6: Quality Audit (Kiểm tra toàn diện)

**Chain:** `consistency → quality-gate → traceability → auditor`
**Thời gian:** 2-3 giờ

**When to Use:** Trước milestone quan trọng (go-live, stakeholder review, compliance deadline). Cần snapshot chất lượng toàn project.

**Steps:**
1. `@ba-consistency [artifacts list]` — cross-artifact check: US vs API Spec vs DB Schema
2. `@ba-quality-gate [full artifact set]` — 8-dimension scoring, identify REJECT items
3. `@ba-traceability` — RTM: BRD → US → AC → Test Case, highlight coverage gaps
4. `@ba-auditor` — executive audit dashboard: Coverage Score, Risk Heatmap, open items

**Pro Tip:** Chạy scenario này ít nhất 1 lần trước sprint review để tránh bị surprise audit.

---

## Scenario 7: Confluence Documentation (Publish docs)

**Chain:** `writing → diagram → export → confluence`
**Thời gian:** 1-2 giờ

**When to Use:** BRD/SRS đã validated, cần publish lên Confluence với đầy đủ diagrams cho team review.

**Steps:**
1. `@ba-writing` — finalize document với đầy đủ sections, không còn placeholder
2. `@ba-diagram` — render BPMN flowchart, ERD, sequence diagrams dạng Mermaid
3. `@ba-export` — formatting check, verify cross-references, đảm bảo Confluence-ready
4. `@ba-confluence` — publish với page hierarchy đúng, labels, và embedded diagrams

**Pro Tip:** Dùng `@ba-diagram` trước `@ba-confluence` — agent sẽ tạo Confluence macro syntax sẵn, chỉ cần paste.

---

## Scenario 8: New Domain Discovery (Tìm hiểu domain mới)

**Chain:** `questioning → elicitation → ux → data → writing`
**Thời gian:** 3-5 giờ

**When to Use:** Bắt đầu module mới trong domain chưa quen. Cần build understanding từ đầu trước khi viết requirement.

**Steps:**
1. `@ba-questioning [domain + stakeholder]` — chuẩn bị question set 3-tier cho domain exploration
2. `@ba-elicitation` — funnel interview, khai thác mental model của domain expert
3. `@ba-ux [user type description]` — tạo Persona + User Journey Map
4. `@ba-data` — thiết kế ERD sơ bộ, xác định entities và relationships chính
5. `@ba-writing` — viết User Stories từ insights đã thu thập

**Pro Tip:** `@ba-questioning` ở bước 1 giúp bạn không hỏi những câu "ngây thơ" với domain expert — tạo impression tốt hơn.

---

## Scenario 9: Go-Live Readiness (Chuẩn bị triển khai)

**Chain:** `change → communication → facilitation → change`
**Thời gian:** 2-4 giờ

**When to Use:** System đã build xong, cần đảm bảo người dùng và tổ chức sẵn sàng adopt — không chỉ deploy xong là xong.

**Steps:**
1. `@ba-change [user groups + old system]` — ADKAR assessment, xác định barrier points theo từng nhóm
2. `@ba-communication` — soạn change announcement tailored cho từng audience (end users, managers, IT)
3. `@ba-facilitation` — thiết kế training workshop cho user adoption
4. `@ba-change` — go-live checklist: readiness criteria, rollback plan, hypercare plan

**Pro Tip:** ADKAR barrier thường nằm ở "Ability" (thiếu training) hoặc "Reinforcement" (không có incentive) — đừng assume là Awareness.

---

## Scenario 10: Data-Driven Feature (Tính năng phụ thuộc dữ liệu)

**Chain:** `data → business-rules → writing → test-gen`
**Thời gian:** 2-3 giờ

**When to Use:** Feature liên quan đến data transformation, reporting, hoặc business logic phức tạp (pricing engine, eligibility check, v.v.).

**Steps:**
1. `@ba-data [module description]` — thiết kế ERD + Data Dictionary, xác định data flows
2. `@ba-business-rules [business logic description]` — Decision Table, kiểm tra completeness và conflicts
3. `@ba-writing [data + business rules]` — viết User Stories với data acceptance criteria cụ thể
4. `@ba-test-gen` — sinh test cases cover data validation, boundary values, và business rule exceptions

**Pro Tip:** Decision Table từ `@ba-business-rules` thường expose contradiction mà stakeholder không biết đang tồn tại.

---

## Scenario 11: UX-Driven Feature (Thiết kế UX trước)

**Chain:** `ux → questioning → writing → validation → diagram`
**Thời gian:** 2-3 giờ

**When to Use:** Feature mới quan trọng về trải nghiệm người dùng, cần hiểu user trước khi viết bất kỳ requirement nào.

**Steps:**
1. `@ba-ux [user type]` — tạo Persona đầy đủ và User Journey Map
2. `@ba-questioning [journey pain points]` — chuẩn bị câu hỏi để validate assumptions với real users
3. `@ba-writing [persona + journey insights]` — viết User Stories từ góc nhìn user, không phải system
4. `@ba-validation` — INVEST check, ambiguity scan
5. `@ba-diagram` — vẽ sequence diagram cho key user flows

**Pro Tip:** Dùng `@ba-ux` để tạo "Job-to-be-done" statements trước — giúp `@ba-writing` viết stories đúng problem space.

---

## Scenario 12: Agile Kickoff (Bắt đầu Agile project)

**Chain:** `agile → facilitation → writing → prioritization`
**Thời gian:** 3-5 giờ

**When to Use:** Project mới chuyển sang Agile hoặc bắt đầu Agile từ đầu. Cần setup backlog, ceremonies, và definition of ready/done.

**Steps:**
1. `@ba-agile` — tạo User Story Map, xác định MVP và release slicing
2. `@ba-facilitation` — thiết kế kickoff workshop agenda: team agreements, DoR/DoD, working agreements
3. `@ba-writing [story map]` — viết User Stories đầy đủ cho Sprint 1-2
4. `@ba-prioritization [full backlog]` — MoSCoW ranking, capacity planning cho sprint đầu

**Pro Tip:** `@ba-agile` giỏi tạo Walking Skeleton — dùng đó để team align về architecture trước khi estimate.

---

## Scenario 13: Compliance Audit (Kiểm tra tuân thủ)

**Chain:** `nfr → validation → traceability → export`
**Thời gian:** 2-4 giờ

**When to Use:** Auditor đến kiểm tra. Cần chứng minh requirements cover compliance và có test evidence.

**Steps:**
1. `@ba-nfr [regulation: GDPR/PCI-DSS/ISO 27001]` — map system requirements vào compliance obligations
2. `@ba-validation` — audit mọi requirement: có compliance mapping không? có test case không?
3. `@ba-traceability` — RTM từ regulation → requirement → test case → evidence, highlight gaps
4. `@ba-export` — package compliance matrix dạng DOCX theo format auditor yêu cầu

**Pro Tip:** `@ba-traceability` có thể scan file system để auto-generate RTM — chỉ cần cung cấp đúng file paths.

---

## Scenario 14: Meeting Prep → Action Items (Từ họp đến hành động)

**Chain:** `questioning → facilitation → communication → jira`
**Thời gian:** 30-90 phút

**When to Use:** Chuẩn bị cho cuộc họp quan trọng, và sau đó chuyển output thành action items có track được.

**Steps:**
1. `@ba-questioning [meeting objective + attendees]` — chuẩn bị agenda, question set, desired outcomes
2. `@ba-facilitation` — thiết kế meeting structure để đảm bảo đạt mục tiêu trong thời gian
3. `@ba-communication [meeting notes thô]` — soạn minutes chuẩn: decisions, action items, owners, deadlines
4. `@ba-jira [action items]` — tạo Jira tasks từ action items, assign owner, set due dates

**Pro Tip:** Gửi agenda (output bước 1-2) trước meeting ít nhất 24h — tăng meeting effectiveness rõ rệt.

---

## Scenario 15: Full Pipeline (End-to-end)

**Chain:** `strategy → elicitation → writing → validation → test-gen → jira + confluence`
**Thời gian:** 1-2 ngày

**When to Use:** Feature lớn hoặc project phức tạp cần đi qua toàn bộ BA lifecycle trước khi dev bắt đầu.

**Steps:**
1. `@ba-strategy` — SWOT/PESTLE, xác định strategic alignment và success metrics
2. `@ba-elicitation` — funnel interview, khai thác requirements từ tất cả stakeholders
3. `@ba-writing` — BRD + SRS + User Stories với Gherkin AC
4. `@ba-validation + @ba-consistency` — quality check toàn diện (parallel)
5. `@ba-test-gen` — 7-category test suite cho mọi stories
6. `@ba-jira` — tạo Epic + Stories trong Jira với test cases
7. `@ba-confluence` — publish BRD/SRS lên Confluence với diagrams

**Pro Tip:** Bước 4 chạy `@ba-validation` và `@ba-consistency` song song để tiết kiệm thời gian — output không phụ thuộc nhau.

---

## Quick Reference

| Scenario | Chain Length | Time | Trigger |
|---|---|---|---|
| 1. Zero to BRD | 7 agents | 2-4h | Dự án mới, không có tài liệu |
| 2. Sprint Planning | 5 agents | 1-2h | Sprint bắt đầu trong 2 ngày |
| 3. Screenshot to Jira | 4 agents | 30-60m | Designer gửi mockup |
| 4. Stakeholder War | 4 agents | 1-2h | Conflict block dự án |
| 5. Production Postmortem | 4 agents | 1-3h | Defect production nghiêm trọng |
| 6. Quality Audit | 4 agents | 2-3h | Trước milestone/go-live |
| 7. Confluence Docs | 4 agents | 1-2h | Cần publish docs |
| 8. New Domain | 5 agents | 3-5h | Domain chưa quen |
| 9. Go-Live Readiness | 4 agents | 2-4h | Chuẩn bị deploy |
| 10. Data Feature | 4 agents | 2-3h | Business logic/data phức tạp |
| 11. UX Feature | 5 agents | 2-3h | Feature quan trọng về UX |
| 12. Agile Kickoff | 4 agents | 3-5h | Bắt đầu Agile project |
| 13. Compliance Audit | 4 agents | 2-4h | Auditor kiểm tra |
| 14. Meeting → Action | 4 agents | 30-90m | Họp quan trọng cần track |
| 15. Full Pipeline | 7 agents | 1-2 ngày | Feature/project lớn |

---

> **Tip:** Bắt đầu với `@ba-master [mô tả situation]` nếu không chắc scenario nào phù hợp — agent sẽ recommend đúng chain.
