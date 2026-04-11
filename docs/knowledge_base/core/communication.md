# Communication — Core BA Knowledge

> Truyền thông hiệu quả: đúng thông điệp, đúng người, đúng format, đúng thời điểm.

## Tại sao Communication là kỹ năng riêng?

BA tạo ra nhiều artifacts nhưng giá trị chỉ được thực hiện khi stakeholders HIỂU và HÀNH ĐỘNG dựa trên chúng. Communication không phải "viết BRD" (đó là writing) — mà là adapt và deliver thông tin phù hợp audience.

## Audience Adaptation Matrix

| Audience | Quan tâm | Format | Ngôn ngữ | Chi tiết |
|----------|---------|--------|----------|---------|
| C-suite / Sponsor | ROI, Risk, Timeline | 1 trang, slides | Business, không jargon | Chỉ high-level |
| Product Manager | Scope, Priority | Bullet points, tables | Mix business + tech | Medium |
| Dev Team | Specs, AC, API | Markdown, Gherkin | Technical, chính xác | Maximum |
| QA / Tester | Test criteria | Test cases, scenarios | Structured, testable | High |
| End Users | Thay đổi gì, dùng sao | Guides, FAQs | Đơn giản, thân thiện | Minimal |

## Nguyên tắc chính

### 1. Pyramid Principle (Barbara Minto)
- Dẫn bằng KẾT LUẬN trước
- Hỗ trợ bằng evidence
- Chi tiết chỉ khi được hỏi

### 2. One Page Rule
Nếu không tóm được trong 1 trang → chưa đủ rõ ràng.

### 3. Action-Oriented
Mọi communication kết thúc bằng: Ai → Làm gì → Khi nào.

## Loại communication artifacts

| Artifact | Khi nào | Template |
|----------|---------|---------|
| Status Report | Hàng tuần/sprint | RAG status, achievements, risks, next steps |
| Executive Summary | Trước khi giao BRD dài | Bottom line, key facts, recommendation |
| Meeting Minutes | Sau mỗi cuộc họp | Decisions, actions, parking lot |
| Scope Change Notice | Khi thay đổi scope | Impact, options, recommendation |
| Escalation | Khi bị block | Problem, impact, options, recommendation |
| Sprint Review Prep | Trước sprint review | Demo script, achievements, blockers |

## RAG Status Convention
- 🟢 **Green**: On track, no issues
- 🟡 **Amber**: At risk, needs attention but not blocked
- 🔴 **Red**: Blocked, needs immediate action/decision

## Anti-Patterns
- ❌ Gửi BRD 50 trang cho CEO → Viết Executive Summary 1 trang
- ❌ Dùng jargon kỹ thuật với end user → Adapt ngôn ngữ
- ❌ "Không có vấn đề gì" khi velocity giảm 20% → Transparent reporting
- ❌ Meeting không có minutes → Decisions và actions bị quên

## Agents liên quan
- **@ba-communication**: Agent chính cho kỹ năng này
- **@ba-identity**: Stakeholder mapping (ai nhận thông tin gì)
- **@ba-export**: Format cuối cùng (DOCX, PDF)
- **@ba-facilitation**: Communication trong workshop

## Sources
- Minto — The Pyramid Principle
- BABOK v3 — Underlying Competencies: Communication Skills
- Pullan — Making Workshops Work (Stakeholder Communication)
