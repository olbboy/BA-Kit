# Questioning — Core BA Knowledge

> Kỹ năng đặt câu hỏi xuyên suốt vòng đời BA, không chỉ trong giai đoạn elicitation.

## Tại sao Questioning là kỹ năng riêng?

Elicitation tập trung vào **khai thác requirements** (discovery phase). Questioning là kỹ năng nền tảng BA sử dụng **ở mọi giai đoạn**: review, planning, challenge, retro, domain learning.

## Phân biệt với Elicitation

| Khía cạnh | Elicitation | Questioning |
|-----------|-------------|-------------|
| Mục đích | Khai thác requirements ẩn | Chuẩn bị câu hỏi cho BẤT KỲ tình huống |
| Giai đoạn | Discovery phase | Toàn bộ lifecycle |
| Đầu vào | Stakeholder + domain | Situation + audience + goal |
| Đầu ra | Requirements thô | Question set + listening triggers |

## Kỹ thuật chính

### 1. Context-Free Questions (Gause & Weinberg)
Câu hỏi áp dụng được cho BẤT KỲ sản phẩm/dự án nào:
- "Sản phẩm này giải quyết vấn đề gì?"
- "Sản phẩm này có thể TẠO RA vấn đề gì?"
- "Ai có thông tin về dự án mà chưa được hỏi?"
- "Nếu dự án thất bại, lý do có khả năng nhất là gì?"

### 2. Meta-Questions
Câu hỏi về chính việc hỏi:
- "Có câu hỏi nào tôi nên hỏi nhưng chưa hỏi?"
- "Câu hỏi nào tôi đang ngại hỏi? Tại sao?"

### 3. Assumption Surfacing
1. Liệt kê assumptions rõ ràng (stated in document)
2. Phát hiện assumptions ẩn (unstated but required)
3. Challenge: "Bằng chứng nào hỗ trợ assumption này?"
4. Đánh giá risk: "Nếu assumption sai, hậu quả gì?"

### 4. Tiered Question Sets
- **Tier 1 (Must-Ask)**: 3-5 câu quyết định thành công cuộc họp
- **Tier 2 (Should-Ask)**: 3-5 câu đào sâu
- **Tier 3 (Could-Ask)**: 2-3 câu khám phá biên

### 5. Listening Triggers
Chuẩn bị sẵn follow-up: "Nếu họ nói X → hỏi tiếp Y"
- Phát hiện red flags trong câu trả lời
- Nhận biết khi cần chuyển hướng câu hỏi

## Question Quality Checklist
- [ ] Mục đích rõ ràng (tại sao hỏi câu này?)
- [ ] Open vs Closed — chọn có chủ đích
- [ ] Không leading ("Bạn có đồng ý rằng...?" → sai)
- [ ] Không compound (1 câu = 1 ý)
- [ ] Không giả định câu trả lời
- [ ] Có ít nhất 1 meta-question

## Situation-Specific Question Banks

| Tình huống | Focus |
|-----------|-------|
| Meeting lần đầu | WHY, WHO, WHAT — context-free |
| Review spec | Assumptions, ambiguity, gaps |
| Sprint planning | Feasibility, dependencies, risks |
| Scope change | Why now? Impact? Cost? Alternative? |
| Feasibility challenge | What specifically blocks? Constraint type? |
| Post-mortem | Timeline, contributing factors, non-blame |
| Domain discovery | Terminology, process, exceptions |

## Agents liên quan
- **@ba-questioning**: Agent chính cho kỹ năng này
- **@ba-elicitation**: Khai thác requirements (sử dụng questioning techniques)
- **@ba-facilitation**: Workshop questioning
- **@ba-conflict**: Probing positions vs interests

## Sources
- Gause & Weinberg — Exploring Requirements (Context-Free Questions)
- BABOK v3 — Elicitation & Collaboration Knowledge Area
- Gottesdiener — Requirements Memory Jogger (Meta-Questions)
