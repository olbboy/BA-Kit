# BA-Kit: Hướng Dẫn Cho BA Mới (Junior Quick Start)

> Bạn mới vào team? Đừng lo — đây là tất cả những gì bạn cần để bắt đầu ngay hôm nay.
> BA-Kit chạy trên **3 nền tảng agentic chính / 3 primary agentic platforms**:
> - **Antigravity IDE** (Google DeepMind) — full experience, cho Technical BA
> - **Claude Code** (Anthropic) — agentic CLI, cho BA + DevOps
> - **Claude CoWork** (Anthropic) — desktop app dễ dùng nhất, cho BA truyền thống
> *Choose the platform that matches your skill level. See `docs/ai-foundation-for-ba.md` Section 1.4 for guidance.*

---

## Tuần 0: Nền Tảng AI ★ Bắt Buộc (AI Foundation ★ Required)

> 📖 Đọc `docs/ai-foundation-for-ba.md` trước khi bắt đầu.
> *Read `docs/ai-foundation-for-ba.md` before starting.*

### Checklist trước khi dùng BA-Kit / Pre-requisites:
- [ ] Hiểu LLM là gì và tại sao AI hallucinate / Understand LLMs and hallucinations
- [ ] Hiểu Tokens và Context Window / Understand Tokens and Context Window
- [ ] Hiểu tại sao Multi-Agent tốt hơn Single Chatbot / Understand Multi-Agent vs Single Chatbot
- [ ] Biết RAG và MCP là gì (BA-Kit dùng cả hai) / Know what RAG and MCP are
- [ ] Đọc qua CONTINUITY.md template / Review the CONTINUITY.md template
- [ ] Nắm được dữ liệu nào KHÔNG được đưa vào AI / Know what data NOT to share with AI
- [ ] Đọc `docs/ai-tools-guide.md` để biết khi nào dùng tool nào / Read the AI Tools Guide

**Thời gian:** 2-3 giờ tự học / **Time:** 2-3 hours self-study

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
| `@ba-test-gen` | Cần tạo test case từ AC | *"Generate test cases cho US-ATTEN-01 — 7 categories"* |
| `@ba-quality-gate` | Kiểm tra chất lượng BRD/US trước khi bàn giao | *"Chấm điểm BRD này theo 8 dimensions"* |

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

QUALITY MASTER (v3.0)
  + @ba-test-gen + @ba-quality-gate + @ba-consistency + @ba-auditor
  Test Cases → Quality Gate → Cross-Check → Audit

EXPERT
  @ba-master → full squad orchestration (điều phối toàn bộ 32 agents)
```

---

## Tài Nguyên

| Tài nguyên | Mô tả |
|-----------|-------|
| `docs/agent-cheat-sheet.md` | Toàn bộ 32 agents + Power Combos |
| `docs/workflow-cookbook.md` | 23 kịch bản thực tế từ A-Z |
| `.agent/templates/` | 14 template sẵn dùng cho mọi deliverable |
| `python3 .agent/scripts/ba_search.py "keyword"` | Tìm kiếm trong knowledge base |
| `python3 .agent/scripts/coverage_checker.py outputs/<project>/` | Scan sức khỏe dự án tự động |

> BA giỏi không phải người biết nhiều — mà là người hỏi đúng câu hỏi.
