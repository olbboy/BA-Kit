# BA-Kit Agent Cheat Sheet

Tham chiếu nhanh 32 agents — phân loại, khi nào dùng, output chính.

---

## Orchestrator

| Agent | Vai trò | Khi nào dùng | Output chính |
|-------|---------|--------------|--------------|
| **@ba-master** | Dispatcher trung tâm | Bắt đầu bất kỳ yêu cầu nào — master sẽ route tới đúng agent | Workflow chain có thứ tự |

---

## Core Workflow (Luồng chính)

| Agent | Vai trò | Khi nào dùng | Output chính |
|-------|---------|--------------|--------------|
| **@ba-identity** | Stakeholder mapping | Dự án mới, cần xác định ai là bên liên quan | RACI, Power/Interest Grid |
| **@ba-elicitation** | Khai thác yêu cầu | Chưa rõ requirements, cần phỏng vấn, làm rõ | Câu hỏi Funnel, 5W1H, danh sách yêu cầu thô |
| **@ba-writing** | Viết requirements | Có đủ thông tin, cần US/BRD/SRS/API spec | User Story, Gherkin AC, BRD draft |
| **@ba-validation** | Kiểm tra chất lượng | Sau khi viết xong, cần review | INVEST check, danh sách lỗi, yêu cầu cần làm rõ |
| **@ba-test-gen** | Sinh test cases từ AC | Có AC, cần test coverage | Test suite (Happy/Edge/Error/Security/Perf) |
| **@ba-traceability** | RTM và impact analysis | Cần truy vết, phân tích ảnh hưởng thay đổi | RTM, dependency graph, health report |
| **@ba-quality-gate** | Chấm điểm chất lượng | Trước khi giao handoff/release | Báo cáo PASS/CONDITIONAL/REJECT (8 chiều) |
| **@ba-consistency** | Kiểm tra đồng nhất | US mâu thuẫn với API spec hoặc DB schema | Mismatch report (US↔API↔DB↔BRD) |
| **@ba-auditor** | Audit toàn dự án | Cần báo cáo sức khỏe tổng thể | Executive health dashboard |
| **@ba-export** | Xuất tài liệu cuối | Cần DOCX/PDF chuyên nghiệp để giao KH | Enterprise DOCX (Pandoc) |

---

## Specialized (Chuyên sâu)

| Agent | Vai trò | Khi nào dùng | Output chính |
|-------|---------|--------------|--------------|
| **@ba-nfr** | Phi chức năng | Cần Performance, Security, Compliance (ISO 25010) | NFR spec, SLA, GDPR/PCI checklist |
| **@ba-process** | BPMN / quy trình | Cần vẽ luồng As-Is/To-Be, swimlane | BPMN diagram, bottleneck analysis |
| **@ba-prioritization** | Ưu tiên hóa | Quá nhiều requirements, cần cắt scope | MoSCoW/RICE/WSJF ranking |
| **@ba-conflict** | Giải quyết xung đột | Các bên liên quan bất đồng | ADR, win-win proposal (Harvard Method) |
| **@ba-agile** | Agile/MVP | Sprint planning, story mapping, hypothesis-driven | Story map, MVP backlog, experiment design |
| **@ba-facilitation** | Workshop | Cần tổ chức workshop khai thác requirements | Workshop plan (ODEC framework) |
| **@ba-systems** | Tư duy hệ thống | Cần phân tích vòng lặp, hậu quả không lường trước | Causal loop diagram, leverage points |
| **@ba-root-cause** | Tìm nguyên nhân gốc | Cần phân tích tại sao vấn đề xảy ra | Fishbone, 5 Whys, Pareto chart |
| **@ba-innovation** | Đổi mới / A/B | Cần thiết kế thí nghiệm, A/B test | Experiment brief, hypothesis statement |
| **@ba-metrics** | Đo lường chất lượng | Cần KPI, defect density, control chart | SPC metrics, quality dashboard |

---

## Strategic (Chiến lược)

| Agent | Vai trò | Khi nào dùng | Output chính |
|-------|---------|--------------|--------------|
| **@ba-strategy** | Bối cảnh kinh doanh | Cần phân tích môi trường, business context | SWOT, PESTLE, BMC, Porter's 5 Forces |
| **@ba-solution** | Business case / ROI | Cần so sánh giải pháp, tính ROI | Cost/Benefit, NPV, make-or-buy recommendation |

---

## Integration (Tích hợp công cụ)

| Agent | Vai trò | Khi nào dùng | Output chính |
|-------|---------|--------------|--------------|
| **@ba-jira** | Đồng bộ Jira | Cần tạo/cập nhật ticket Jira từ US | Jira issues, sprint backlog |
| **@ba-confluence** | Publish Confluence | Cần đăng tài liệu lên Confluence | Confluence page (Markdown → XHTML) |

---

## Lifecycle (Vòng đời BA — NEW in v3.1)

| Agent | Vai trò | Khi nào dùng | Output chính |
|-------|---------|--------------|--------------|
| **@ba-questioning** | Chuẩn bị câu hỏi | Trước meeting, review, phỏng vấn, khi cần challenge assumptions | Question set 3-tier (Must/Should/Could), listening triggers |
| **@ba-communication** | Truyền thông BA | Cần status report, executive summary, meeting minutes, email draft | Reports, summaries, minutes theo audience |
| **@ba-ux** | Nghiên cứu UX | Cần persona, user journey, empathy map, usability test | Persona cards, journey maps, test protocols |
| **@ba-data** | Kiến trúc dữ liệu | Cần ERD, data dictionary, DFD, data mapping, migration plan | ERD (Mermaid), data dictionary, mapping tables |
| **@ba-change** | Quản lý thay đổi | Triển khai hệ thống mới, cần training plan, go-live checklist | ADKAR assessment, training plan, go-live checklist |
| **@ba-business-rules** | Quản lý quy tắc nghiệp vụ | Cần decision table, rule catalog, kiểm tra conflict | Decision tables, rule catalogs, conflict reports |

---

## Knowledge (Quản lý tri thức)

| Agent | Vai trò | Khi nào dùng | Output chính |
|-------|---------|--------------|--------------|
| **@ba-wiki** | Quản lý tri thức | Nạp kiến thức mới, truy vấn context dự án, kiểm tra wiki | Wiki pages, knowledge synthesis |

---

## Common Workflow Chains (Luồng phổ biến)

### 1. Tính năng mới (New Feature — full cycle)
```
@ba-strategy       → Xác định business context, tại sao cần tính năng này
@ba-elicitation    → Khai thác chi tiết yêu cầu từ stakeholder
@ba-writing        → Viết User Stories + Gherkin AC
@ba-validation     → INVEST check, phát hiện mơ hồ
@ba-test-gen       → Sinh test cases từ AC
@ba-export         → Xuất BRD/SRS final
```

### 2. Sprint Planning nhanh
```
@ba-writing        → Chuyển raw requirements → User Stories có AC
@ba-validation     → Review INVEST, flag ambiguous stories
@ba-elicitation    → Sinh clarifying questions cho PO
@ba-prioritization → MoSCoW ranking, cắt scope phù hợp sprint
@ba-jira           → Tạo tickets lên Jira
```

### 3. Kiểm soát chất lượng tài liệu
```
@ba-consistency    → Cross-check US↔API↔DB↔BRD
@ba-quality-gate   → Chấm điểm 8 chiều, PASS/FAIL
@ba-traceability   → Kiểm tra RTM coverage
@ba-auditor        → Executive health dashboard tổng thể
```

### 4. Giải quyết xung đột stakeholder
```
@ba-identity       → Map stakeholders (Power/Interest Grid)
@ba-conflict       → Tìm win-win, viết ADR
@ba-solution       → Tính ROI để hỗ trợ quyết định
@ba-facilitation   → Thiết kế workshop alignment session
```

---

## Quick Activation Examples (Copy-paste sẵn)

```
# Bắt đầu dự án mới
@ba-master "Dự án mới: [tên dự án]. Tôi cần bắt đầu từ đâu?"

# Viết User Story từ mô tả thô
@ba-writing "Viết User Story cho tính năng: [mô tả ngắn]. Định dạng: INVEST + Gherkin AC."

# Review tài liệu hiện có
@ba-validation "Review User Stories sau đây theo INVEST criteria và phát hiện điểm mơ hồ: [dán US vào đây]"

# Sinh test cases
@ba-test-gen "Sinh test cases cho AC sau: [dán AC vào đây]. Cần cover: Happy, Edge, Error, Security."

# Phân tích ảnh hưởng thay đổi
@ba-traceability "Thay đổi [tên tính năng] ảnh hưởng tới những US/component nào? Đây là RTM hiện tại: [link/nội dung]"

# Xuất tài liệu cuối
@ba-export "Xuất BRD thành DOCX. Template chuẩn, logo công ty ở header. Nội dung: [dán markdown vào đây]"
```

---

## Decision Matrix nhanh

| Tình huống | Agent đầu tiên | Agent tiếp theo |
|------------|----------------|-----------------|
| Chưa biết bắt đầu từ đâu | `@ba-master` | — |
| Cần phỏng vấn stakeholder | `@ba-elicitation` | `@ba-writing` |
| Có yêu cầu thô, cần viết US | `@ba-writing` | `@ba-validation` |
| US đã viết, cần test | `@ba-test-gen` | `@ba-quality-gate` |
| Stakeholders bất đồng | `@ba-conflict` | `@ba-identity` |
| Cần ưu tiên backlog | `@ba-prioritization` | `@ba-agile` |
| Cần phân tích NFR/Security | `@ba-nfr` | `@ba-validation` |
| Cần tạo ticket Jira | `@ba-jira` | `@ba-writing` |
| Cần publish lên Confluence | `@ba-confluence` | `@ba-export` |
| Cần audit toàn bộ dự án | `@ba-auditor` | `@ba-quality-gate` |
| Chuẩn bị câu hỏi cho meeting | `@ba-questioning` | `@ba-elicitation` |
| Cần viết status report / email | `@ba-communication` | `@ba-identity` |
| Cần tạo persona / journey map | `@ba-ux` | `@ba-writing` |
| Cần ERD / data dictionary | `@ba-data` | `@ba-writing` |
| Cần plan go-live / training | `@ba-change` | `@ba-communication` |
| Cần decision table / rule catalog | `@ba-business-rules` | `@ba-validation` |

---

*Xem thêm: `docs/workflow-cookbook.md` (23 scenarios chi tiết) | `docs/prompt-library.md` (45 prompts) | `.agent/README.md`*
