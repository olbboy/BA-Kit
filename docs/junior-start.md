# BA-Kit: Lộ Trình 4 Tuần cho BA Mới

> Bạn mới vào nghề BA? File này là điểm khởi đầu. Không cần đọc hết mọi thứ — chỉ cần làm theo từng tuần.

---

## Tuần 1: Foundation — 3 Agent Cốt Lõi

Tuần đầu tiên chỉ cần thành thạo 3 agent này. Đây là bộ ba BA dùng hàng ngày.

### @ba-elicitation — Thu thập yêu cầu

**Dùng khi:** Phỏng vấn stakeholder, khai thác pain point, không biết hỏi gì.

```
@ba-elicitation Tôi cần interview stakeholder về tính năng [TÊN TÍNH NĂNG].
Mục tiêu: hiểu pain point và kỳ vọng thực sự của họ.
Đề xuất 10 câu hỏi SPIN và ambiguity checklist.
```

**Bài tập:** Lấy một tính năng đang làm, dùng agent tạo 10 câu hỏi SPIN, rồi tự trả lời như thể bạn là stakeholder.

---

### @ba-writing — Viết User Story

**Dùng khi:** Có meeting notes hoặc yêu cầu thô, cần chuyển thành User Story chuẩn.

```
@ba-writing Đây là notes từ buổi họp: [DÁN NOTES VÀO ĐÂY]
Viết 3 User Stories theo format "As a... I want... So that..."
với Acceptance Criteria dạng Gherkin (Given/When/Then).
```

**Bài tập:** Lấy notes từ bài tập tuần trước (câu trả lời của stakeholder giả), viết 3 User Stories.

---

### @ba-validation — Kiểm tra chất lượng

**Dùng khi:** Trước khi gửi specs cho dev. Luôn chạy bước này.

```
@ba-validation Đây là User Story của tôi: [DÁN STORY VÀO ĐÂY]
Review theo tiêu chí INVEST và SMART.
Liệt kê tất cả lỗi, điểm mơ hồ, và thiếu sót.
```

**Bài tập:** Validate 3 User Stories từ bài tập trước. Fix theo feedback của agent.

---

## Tuần 2: Expansion — Mở Rộng Bộ Công Cụ

| Agent | Dùng khi nào | Prompt mẫu |
|-------|-------------|------------|
| `@ba-prioritization` | Backlog dài, không biết làm gì trước | `"Áp dụng MoSCoW cho danh sách feature này: [LIST]"` |
| `@ba-process` | Cần vẽ quy trình nghiệp vụ As-Is / To-Be | `"Vẽ BPMN cho quy trình [TÊN QUY TRÌNH]"` |
| `@ba-nfr` | Dev hỏi về performance, security, scalability | `"Đề xuất NFR cho hệ thống [TÊN HỆ THỐNG] theo ISO 25010"` |
| `@ba-questioning` | Cần đặt câu hỏi chiến lược, không chỉ thu thập | `"Tạo Question Bank cho domain [DOMAIN] — focus on hidden assumptions"` |

**Bài tập tuần 2:** Lấy backlog dự án thực (hoặc giả), dùng `@ba-prioritization` rank theo MoSCoW, sau đó dùng `@ba-process` vẽ quy trình cho top 3 features.

---

## Tuần 3: Strategy — Tư Duy Cấp Cao

| Agent | Dùng khi nào | Prompt mẫu |
|-------|-------------|------------|
| `@ba-strategy` | Phân tích business context toàn cảnh | `"SWOT analysis cho cơ hội thị trường này: [MÔ TẢ]"` |
| `@ba-conflict` | Stakeholder bất đồng, không ai chịu ai | `"Sales vs Dev đang conflict về [VẤN ĐỀ] — Harvard Method"` |
| `@ba-ux` | Cần hiểu user journey, pain points UX | `"Map user journey cho [PERSONA] khi thực hiện [TASK]"` |
| `@ba-data` | Cần xác định data requirements, analytics | `"Identify data entities và relationships cho [TÍNH NĂNG]"` |

**Bài tập tuần 3:** Chọn một feature đang tranh cãi trong team. Dùng `@ba-conflict` để tìm win-win solution, sau đó dùng `@ba-strategy` để justify quyết định bằng business value.

---

## Tuần 4: Advanced — Làm Chủ Toàn Bộ Squad

| Agent | Dùng khi nào | Prompt mẫu |
|-------|-------------|------------|
| `@ba-solution` | PM hỏi tính năng này có đáng làm không | `"Tính ROI 3 năm cho tính năng [X] — dùng Python, assumption rõ ràng"` |
| `@ba-diagram` | Cần diagram kỹ thuật hoặc flow | `"Vẽ sequence diagram cho luồng [TÊN LUỒNG]"` |
| `@ba-change` | Quản lý thay đổi requirements giữa chừng | `"Phân tích impact khi requirement [X] thay đổi sang [Y]"` |
| `@ba-business-rules` | Cần document business rules rõ ràng | `"Extract và formalize business rules từ spec này: [SPEC]"` |

**Bài tập tuần 4:** Chạy Chain đầy đủ cho một mini-project: `@ba-strategy` → `@ba-elicitation` → `@ba-writing` → `@ba-validation` → `@ba-test-gen` → `@ba-export`. Đây là workflow thực tế của một BA senior.

---

## Learning Path

```
TUẦN 1 — FOUNDATION
  @ba-elicitation → @ba-writing → @ba-validation
  Thu thập → Viết → Kiểm tra
       |
       v
TUẦN 2 — EXPANSION
  + @ba-prioritization + @ba-process + @ba-nfr + @ba-questioning
  Ưu tiên → Quy trình → Phi chức năng → Câu hỏi chiến lược
       |
       v
TUẦN 3 — STRATEGY
  + @ba-strategy + @ba-conflict + @ba-ux + @ba-data
  Chiến lược → Đàm phán → UX → Data
       |
       v
TUẦN 4 — ADVANCED
  + @ba-solution + @ba-diagram + @ba-change + @ba-business-rules
  ROI → Diagram → Quản lý thay đổi → Business Rules
       |
       v
EXPERT — FULL SQUAD ORCHESTRATION
  @ba-master → điều phối toàn bộ 33 agents
  Biết gọi ai, khi nào, theo chain nào
```

---

## Resources

| Tài nguyên | Nội dung |
|-----------|---------|
| `docs/agent-cheat-sheet.md` | Toàn bộ 33 agents + power combos |
| `docs/prompt-library.md` | 48 copy-paste prompts theo tình huống |
| `.agent/templates/` | 14 templates: BRD, SRS, FRD, PRD, RTM, v.v. |
| `python3 .agent/scripts/ba_search.py "keyword"` | Tìm trong 831 knowledge entries |
| `python3 .agent/scripts/coverage_checker.py outputs/<project>/` | Scan chất lượng specs tự động |

---

## Tips

- **Luôn hỏi "Tại sao?" trước khi viết requirements** — stakeholder nói "cần tính năng X" nhưng vấn đề thực là gì?
- **Dùng `@ba-validation` TRƯỚC khi gửi specs cho dev** — tự review trước, đỡ bị trả lại sau.
- **Không biết gọi agent nào?** Gọi `@ba-master` — nó sẽ route đến đúng specialist.
- **Bị lạc giữa chừng?** `python3 .agent/scripts/ba_search.py "từ khóa"` — 831 entries sẵn sàng.
- **Dùng CONTINUITY.md** để không phải lặp lại context mỗi lần đổi agent.

---

> **BA giỏi không phải người biết nhiều — mà là người hỏi đúng câu hỏi.**
