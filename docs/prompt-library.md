# BA-Kit Prompt Library

> 33 copy-paste prompts tổ chức theo vòng đời BA. Mỗi prompt được thiết kế để kích hoạt đúng agent, đúng lúc.

**Cách dùng:** Copy prompt, thay nội dung trong `[...]`, dán vào chat.

---

## Phase 1: Project Initiation (Khởi động dự án)

Mục tiêu: Xác định bối cảnh, stakeholder, và chiến lược trước khi viết bất kỳ requirement nào.

```
1. @ba-master Tôi muốn xây dựng [tên hệ thống/tính năng]. Hãy phân tích yêu cầu và đề xuất chuỗi agent phù hợp để bắt đầu.
```

```
2. @ba-identity Dự án [tên dự án] phục vụ [ngành/lĩnh vực]. Hãy tạo RACI matrix và Power/Interest grid cho các stakeholder chính.
```

```
3. @ba-strategy Hãy thực hiện SWOT analysis cho [tên dự án/tính năng], tập trung vào bối cảnh [thị trường/ngành] tại Việt Nam.
```

```
4. @ba-identity Tạo communication plan cho dự án [tên dự án]: tần suất báo cáo, kênh liên lạc, và template status update cho từng nhóm stakeholder.
```

```
5. @ba-systems Phân tích các feedback loop và unintended consequences tiềm ẩn khi triển khai [tên tính năng/quy trình].
```

---

## Phase 2: Elicitation (Thu thập yêu cầu)

Mục tiêu: Khai thác yêu cầu thật sự từ stakeholder, không phải requirements giả định.

```
6. @ba-elicitation Phỏng vấn tôi theo phương pháp Funnel để khai thác requirements cho [tên tính năng]. Bắt đầu với câu hỏi mở rộng nhất.
```

```
7. @ba-elicitation Tôi là [vai trò stakeholder]. Hãy đặt câu hỏi 5W1H để xác định nhu cầu thật sự đằng sau yêu cầu: "[mô tả yêu cầu thô]".
```

```
8. @ba-facilitation Thiết kế chương trình workshop 2 giờ để thu thập requirements cho [tên module/tính năng] với [số lượng] người tham gia gồm [danh sách vai trò].
```

```
9. @ba-elicitation Đây là ghi chú từ buổi phỏng vấn stakeholder: [dán ghi chú thô]. Hãy phân tích và trích xuất requirements rõ ràng theo định dạng có cấu trúc.
```

```
10. @ba-agile Tạo User Story Map cho MVP của [tên sản phẩm/tính năng], phân chia theo backbone activities và walking skeleton.
```

---

## Phase 3: Writing (Viết tài liệu yêu cầu)

Mục tiêu: Chuyển hóa inputs thô thành artifacts chất lượng cao, có thể kiểm tra được.

```
11. @ba-writing Viết User Story đầy đủ cho tính năng: "[mô tả tính năng]". Bao gồm INVEST analysis, Acceptance Criteria Gherkin, RBAC matrix, và edge cases.
```

```
12. @ba-writing Tạo Business Requirements Document (BRD) cho [tên dự án] sử dụng template chuẩn. Context: [mô tả ngắn về mục tiêu kinh doanh và phạm vi].
```

```
13. @ba-writing Viết Software Requirements Specification (SRS - IEEE 29148) cho module [tên module]. Danh sách tính năng cần cover: [liệt kê tính năng].
```

```
14. @ba-writing Thiết kế API Specification cho endpoint [GET/POST/PUT/DELETE] `[path]`. Bao gồm request/response schema, error codes, rate limiting, và authentication.
```

```
15. @ba-writing Tạo database schema cho [tên entity/module]. Bao gồm ERD text, data dictionary, constraints, indexes, và business rules theo từng field.
```

```
16. @ba-process Vẽ BPMN diagram dạng text/Mermaid cho quy trình: [mô tả quy trình nghiệp vụ]. Bao gồm swimlane theo vai trò: [danh sách vai trò].
```

```
17. @ba-writing @[image] Đây là mockup/wireframe. Hãy phân tích và chuyển đổi thành Field Specifications đầy đủ với validation rules cho từng element UI.
```

---

## Phase 4: Validation (Kiểm tra chất lượng)

Mục tiêu: Phát hiện defects trước khi dev — không phải sau khi release.

```
18. @ba-validation Đây là User Story: [dán nội dung US]. Hãy thực hiện INVEST check đầy đủ và Ambiguity Scan, trả về Health Score và danh sách defects theo severity.
```

```
19. @ba-validation Quét toàn bộ tài liệu sau và liệt kê tất cả từ ngữ mơ hồ (ambiguity list) kèm đề xuất thay thế có metric cụ thể: [dán nội dung tài liệu].
```

```
20. @ba-quality-gate Đánh giá BRD/User Story sau theo thang điểm 8 chiều (PASS/CONDITIONAL/REJECT): [dán nội dung]. Trả về score chi tiết từng dimension.
```

```
21. @ba-consistency Kiểm tra tính nhất quán cross-artifact giữa: User Story [US-XXX], API Spec [tên endpoint], và DB Schema [tên bảng]. Báo cáo mọi mismatch.
```

```
22. @ba-nfr Định nghĩa Non-Functional Requirements theo ISO 25010 cho tính năng [tên tính năng]. Tập trung: Performance, Security, Reliability. Mọi metric phải có threshold đo được.
```

---

## Phase 5: Testing (Sinh test cases)

Mục tiêu: Biến Acceptance Criteria thành test cases có thể thực thi ngay.

```
23. @ba-test-gen Sinh test suite đầy đủ từ Acceptance Criteria của [US-XXX]. Cover 7 categories: Happy Path, Edge Case, Error Handling, Security, Concurrency, Data Validation, Performance.
```

```
24. @ba-test-gen Tạo UAT script cho tính năng [tên tính năng] dành cho [vai trò người dùng]. Bao gồm preconditions, test steps, expected results, và pass/fail criteria.
```

```
25. @ba-quality-gate Chạy coverage analysis cho project tại [đường dẫn outputs]. Báo cáo: tỷ lệ US có đủ 3 AC (happy/edge/error), missing scenarios, và ambiguous terms detected.
```

```
26. @ba-validation So sánh implementation thực tế [mô tả hoặc screenshot] với Acceptance Criteria gốc [dán AC]. Liệt kê mọi deviation theo severity level.
```

---

## Phase 6: Integration (Tích hợp công cụ)

Mục tiêu: Đồng bộ artifacts vào Jira/Confluence — không copy-paste thủ công.

```
27. @ba-jira Tạo Jira tickets từ các User Stories sau: [dán danh sách US]. Ánh xạ: Story Title → Summary, Acceptance Criteria → Description, Priority → Priority field.
```

```
28. @ba-jira Đồng bộ trạng thái backlog: import stories từ [nguồn] vào Sprint [số]. Gán cho team member theo RACI matrix đã định nghĩa.
```

```
29. @ba-confluence Publish BRD của [tên module] lên Confluence space [tên space]. Format Markdown → XHTML. Tạo page hierarchy: Project > Module > BRD.
```

```
30. @ba-confluence Tạo Requirements Wiki page cho [tên tính năng] trên Confluence: executive summary, stakeholder table, US list có link đến Jira, và decision log.
```

---

## Phase 7: Export & Closure (Xuất tài liệu & đóng dự án)

Mục tiêu: Đóng gói artifacts thành tài liệu bàn giao chuyên nghiệp.

```
31. @ba-export Compile toàn bộ artifacts của [tên dự án] thành DOCX bàn giao. Bao gồm: BRD, SRS, RTM, và Test Suite. Format theo chuẩn [tên client/tổ chức].
```

```
32. @ba-auditor Chạy full project health audit cho [tên dự án]. Output: executive dashboard gồm Coverage Score, Risk Heatmap, và danh sách open items cần xử lý trước closure.
```

```
33. @ba-traceability Tạo Requirements Traceability Matrix (RTM) đầy đủ: BRD → User Story → Acceptance Criteria → Test Case. Highlight mọi requirement chưa có test coverage.
```

---

## Pro Tips: Power-User Combinations

### Combo 1: Zero-to-BRD trong 4 bước

Dùng khi bắt đầu dự án mới từ đầu, không có tài liệu gốc.

```
Bước 1: @ba-master [mô tả dự án] — nhận workflow chain
Bước 2: @ba-elicitation — phỏng vấn thu thập requirements
Bước 3: @ba-writing — viết BRD + User Stories từ output bước 2
Bước 4: @ba-quality-gate — score và phê duyệt trước khi chuyển dev
```

### Combo 2: Sprint-Ready Validation Pipeline

Dùng trước mỗi sprint planning để đảm bảo stories đủ chất lượng.

```
@ba-validation [US] → @ba-test-gen [validated AC] → @ba-consistency [US + API + DB] → @ba-quality-gate [full artifact set]
```

### Combo 3: Screenshot-to-Jira Ticket

Dùng khi có mockup từ designer, cần tạo ticket nhanh cho dev.

```
@ba-writing @[image mockup] → @ba-validation [output] → @ba-jira [validated stories]
```

### Combo 4: Post-Mortem và Root Cause

Dùng sau khi phát hiện requirement defect ở môi trường production.

```
@ba-root-cause [mô tả defect] → @ba-validation [requirements gốc] → @ba-metrics [trend analysis] → @ba-writing [corrected requirements]
```

---

> Tip: Tạo `CONTINUITY.md` ở root project (copy từ `templates/continuity-template.md`) để mọi agent tự đọc context — không cần nhắc lại project goal sau mỗi prompt.
