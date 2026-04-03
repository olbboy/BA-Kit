# BA-Kit: Hướng Dẫn Cho BA Mới (Junior Quick Start)

> Bạn mới vào team? Đừng lo — đây là tất cả những gì bạn cần để bắt đầu ngay hôm nay.

---

## Tuần 1: 3 Agent Cơ Bản

### Ngày 1-2: Thu thập yêu cầu — `@ba-elicitation`

**Việc cần làm:** Phỏng vấn stakeholder, khai thác pain point, tạo danh sách câu hỏi làm rõ.

**Copy-paste prompt này:**
```
@ba-elicitation Tôi cần interview stakeholder về tính năng [TÊN TÍNH NĂNG].
Mục tiêu: hiểu pain point và kỳ vọng thực sự của họ.
Đề xuất 10 câu hỏi SPIN và ambiguity checklist.
```

**Tại sao:** Yêu cầu sai từ đầu = dev làm lại từ đầu. Hỏi đúng ngay từ buổi đầu tiên.

---

### Ngày 3-4: Viết User Story — `@ba-writing`

**Việc cần làm:** Chuyển meeting notes thành User Stories chuẩn Gherkin, có AC rõ ràng.

**Copy-paste prompt này:**
```
@ba-writing Đây là notes từ buổi họp với stakeholder: [DÁN NOTES VÀO ĐÂY]
Hãy viết 3 User Stories theo format "As a... I want... So that..."
với Acceptance Criteria dạng Gherkin (Given/When/Then).
```

**Tại sao:** User Story chuẩn = dev hiểu đúng, tester có test case, không cần họp lại.

---

### Ngày 5: Review chất lượng — `@ba-validation`

**Việc cần làm:** Tự kiểm tra specs trước khi gửi cho dev. Bắt lỗi trước khi bị bắt.

**Copy-paste prompt này:**
```
@ba-validation Đây là User Story của tôi: [DÁN STORY VÀO ĐÂY]
Hãy review theo tiêu chí INVEST và SMART.
Liệt kê tất cả lỗi, điểm mơ hồ, và thiếu sót.
```

**Tại sao:** Một lỗi specs = nhiều giờ dev fix + nhiều cuộc họp không cần thiết.

---

## Tuần 2: Mở Rộng Kỹ Năng

| Agent | Dùng khi nào | Prompt mẫu |
|-------|-------------|------------|
| `@ba-prioritization` | Backlog quá dài, team không biết làm gì trước | *"Áp dụng MoSCoW cho danh sách feature này: [LIST]"* |
| `@ba-process` | Cần vẽ quy trình nghiệp vụ (As-Is / To-Be) | *"Vẽ BPMN cho quy trình Checkout của chúng tôi"* |
| `@ba-nfr` | Dev hỏi về performance, security, scalability | *"Đề xuất NFR cho hệ thống Payment theo ISO 25010"* |

---

## Tuần 3-4: Nâng Cao

| Agent | Dùng khi nào | Prompt mẫu |
|-------|-------------|------------|
| `@ba-strategy` | Cần phân tích business context toàn cảnh | *"SWOT analysis cho cơ hội thị trường này"* |
| `@ba-conflict` | Stakeholder bất đồng, không ai chịu ai | *"Sales vs Dev đang conflict — tìm win-win cho cả hai"* |
| `@ba-solution` | PM hỏi tính năng này có đáng làm không | *"Tính ROI 3 năm cho tính năng [X] bằng Python"* |

---

## Tips Cho Junior BA

- **Luôn hỏi "Tại sao?" trước khi viết requirements** — stakeholder nói "cần tính năng X" nhưng vấn đề thực là gì?
- **Dùng `@ba-validation` TRƯỚC KHI gửi specs cho dev** — tự review trước, đỡ xấu hổ sau.
- **Không ngại hỏi lại stakeholder** — `@ba-elicitation` sẽ tạo ambiguity detection list cho bạn.
- **Bị lạc không biết gọi ai?** Gọi `@ba-master` — nó sẽ chỉ đường.
- **Search knowledge base:** `python3 .agent/scripts/ba_search.py "MoSCoW"` hoặc `"INVEST"` hoặc `"BPMN"`

---

## Progression Map

```
BEGINNER (Tuần 1)
  @ba-elicitation → @ba-writing → @ba-validation
  Thu thập → Viết → Kiểm tra

INTERMEDIATE (Tuần 2-3)
  + @ba-prioritization + @ba-process + @ba-nfr
  Ưu tiên → Quy trình → Phi chức năng

ADVANCED (Tháng 2+)
  + @ba-strategy + @ba-systems + @ba-solution + @ba-metrics
  Chiến lược → Hệ thống → ROI → Đo lường

EXPERT
  @ba-master → full squad orchestration (điều phối toàn bộ agents)
```

---

## Tài Nguyên

| Tài nguyên | Mô tả |
|-----------|-------|
| `docs/agent_cheat_sheet.md` | Toàn bộ 19 agents + Power Combos |
| `WORKFLOW-COOKBOOK.md` | 12 kịch bản thực tế từ A-Z |
| `templates/` | Template sẵn dùng cho mọi deliverable |
| `python3 .agent/scripts/ba_search.py "keyword"` | Tìm kiếm trong knowledge base |

> **Nhớ nhé:** BA giỏi không phải người biết nhiều — mà là người hỏi đúng câu hỏi.
