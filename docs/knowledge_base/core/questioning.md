# Questioning — Core BA Knowledge

> Kỹ năng đặt câu hỏi xuyên suốt vòng đời BA, không chỉ trong giai đoạn elicitation.
> Nâng cấp v2.0: tích hợp Paul-Elder Critical Thinking Framework.

## Tại sao Questioning là kỹ năng riêng?

Elicitation tập trung vào **khai thác requirements** (discovery phase). Questioning là kỹ năng nền tảng BA sử dụng **ở mọi giai đoạn**: review, planning, challenge, retro, domain learning, document analysis, conflict resolution.

## Phân biệt với Elicitation

| Khía cạnh | Elicitation | Questioning |
|-----------|-------------|-------------|
| Mục đích | Khai thác requirements ẩn | Chuẩn bị câu hỏi cho BẤT KỲ tình huống |
| Giai đoạn | Discovery phase | Toàn bộ lifecycle |
| Đầu vào | Stakeholder + domain | Situation + audience + goal |
| Đầu ra | Requirements thô | Question set + listening triggers |

## Nền tảng lý thuyết

### Paul-Elder Critical Thinking Framework
Framework chính cho kỹ năng questioning, gồm 3 trụ cột:
1. **8 Elements of Reasoning** — phân tích cấu trúc tư duy
2. **8 Intellectual Standards** — đánh giá chất lượng tư duy
3. **3 Question Types** — phân loại không gian câu hỏi

## 3 Loại Câu Hỏi (Question Types)

Trước khi hỏi, **phân loại vấn đề** để chọn chiến thuật đúng:

| Loại | Định nghĩa | Ví dụ BA | Chiến thuật |
|------|-----------|---------|------------|
| **One-System** (Thủ tục) | Có đáp án xác định, kiểm chứng được | Spec kỹ thuật, data lookup, compliance | Tìm method/data/source. Xác minh, không tranh luận |
| **No-System** (Sở thích) | Chủ quan, không có đáp án "đúng" | Màu UI, naming conventions | Ghi nhận preference, tiến tiếp |
| **Conflicting-System** (Phán đoán) | Nhiều quan điểm hợp lệ, cần lý luận | Architecture decisions, prioritization | Probe arguments từ mọi phía, áp dụng intellectual standards |

> **Bẫy phổ biến**: Nhầm judgment thành procedure → false certainty. Nhầm preference thành judgment → tranh luận phí thời gian.

## 8 Elements of Reasoning

Hệ thống 8 yếu tố để phân tích bất kỳ tình huống tư duy nào:

| # | Element | Câu hỏi mẫu | Ứng dụng BA |
|---|---------|-------------|-------------|
| 1 | **Purpose** | "Mục tiêu cuối cùng là gì?" | Phát hiện business goal thật đằng sau feature request |
| 2 | **Question at Issue** | "Câu hỏi chính xác cần trả lời là gì?" | Reframe yêu cầu mơ hồ thành câu hỏi rõ ràng |
| 3 | **Information** | "Dữ liệu/bằng chứng nào hỗ trợ? Còn thiếu gì?" | Validate assumptions bằng data |
| 4 | **Inferences** | "Kết luận này dựa trên gì? Có kết luận thay thế?" | Challenge premature conclusions |
| 5 | **Concepts** | "Thuật ngữ chính có được hiểu giống nhau?" | Expose terminology misalignment |
| 6 | **Assumptions** | "Điều gì được coi là đương nhiên? Nếu ngược lại thì sao?" | Surface hidden assumptions |
| 7 | **Implications** | "Nếu làm X, hệ quả bậc 2 là gì?" | Prevent unintended consequences |
| 8 | **Viewpoints** | "Góc nhìn nào đang thiếu?" | Đảm bảo tất cả bên liên quan có tiếng nói |

## 8 Intellectual Standards

Tiêu chuẩn đánh giá **chất lượng** câu hỏi:

| # | Standard | Tự kiểm tra |
|---|----------|-------------|
| 1 | **Clarity** | Người ngoài context có hiểu câu hỏi không? |
| 2 | **Precision** | Câu hỏi có đủ cụ thể để nhận được câu trả lời hữu ích? |
| 3 | **Accuracy** | Câu hỏi có dựa trên facts đã verified? |
| 4 | **Relevance** | Câu hỏi có liên quan trực tiếp đến vấn đề đang bàn? |
| 5 | **Depth** | Câu hỏi có đi vào complexity bên dưới bề mặt? |
| 6 | **Breadth** | Đã xem xét tất cả các góc nhìn liên quan? |
| 7 | **Logic** | Câu hỏi có follow logically từ những gì đã biết? |
| 8 | **Fairness** | Câu hỏi có công bằng với tất cả stakeholders? |

## Concept Analysis (Wilson Method)

Khi requirements dùng thuật ngữ mơ hồ, áp dụng **4-case dissection**:
- **Model cases**: "Cho tôi ví dụ rõ ràng của [concept]"
- **Contrary cases**: "Cái gì chắc chắn KHÔNG PHẢI [concept]?"
- **Related cases**: "Cái gì tương tự nhưng khác biệt quan trọng?"
- **Borderline cases**: "Trường hợp [edge case] có tính là [concept] không?"

> Triggers: "real-time", "scalable", "secure", "user-friendly", "simple", "available", "approval"

## Prior Questions Decomposition

Trước khi tackle câu hỏi phức tạp, phân tách thành **prerequisite questions**:
1. Viết câu hỏi chính
2. Hỏi: "Cần trả lời câu hỏi nào TRƯỚC câu này?"
3. Lặp lại bước 2 cho mỗi prior question
4. Làm NGƯỢC từ câu hỏi đơn giản nhất

## Socratic Questioning Protocol

Kỹ thuật probing có hệ thống khi câu trả lời bề mặt chưa đủ:
1. **Tìm nền tảng**: "Dựa trên cơ sở nào? Giải thích reasoning?"
2. **Theo connections**: "Nếu đúng vậy, thì X cũng đúng?"
3. **Yêu cầu phát triển**: "Cho tôi ví dụ cụ thể?"
4. **Lộ presuppositions**: "Câu hỏi này giả định gì đã được trả lời?"
5. **Test phản ví dụ**: "Nếu ngược lại thì sao? Có case nào không đúng?"
6. **Xem xét hệ quả**: "Nếu theo logic này, kết quả thực tế là gì?"

## Bias Detection

### Egocentric Bias (BA tự kiểm tra)
- "Tôi có ưu tiên solution quen thuộc vì đã biết?"
- "Tôi có tránh câu hỏi khó vì seniority của stakeholder?"
- "Tôi có nhầm preference của mình với need của user?"

### Sociocentric Bias (Group-think)
- "Quyết định có bị driven bởi 'cách luôn làm' thay vì evidence?"
- "Có áp lực ngầm conform theo group position?"

### Stakeholder Bias
- "Họ có distort thông tin để phục vụ lợi ích cá nhân/team?"
- "Họ có nhầm convention tổ chức với actual requirements?"

## Interdisciplinary Domain Decomposition (NEW v2.1)

Khi requirement phức tạp cắt ngang nhiều domain, phân tách và hỏi riêng từng domain:

| Domain | BA Trigger | Câu hỏi chính |
|--------|-----------|---------------|
| Legal/Compliance | Regulation, GDPR, labor law | "Quy định nào áp dụng? Có tuân thủ?" |
| Financial | Budget, ROI, cost | "Chi phí bao nhiêu? Ai chịu? Opportunity cost nếu không làm?" |
| Technical | Architecture, performance | "Constraint kỹ thuật? Khả thi với stack hiện tại?" |
| Organizational | Roles, change | "Ai bị ảnh hưởng? Workflow thay đổi thế nào?" |
| UX | Usability, accessibility | "User có làm được? Accessibility needs?" |
| Data | Privacy, quality, migration | "Data gì cần? Từ đâu? Ai sở hữu?" |

**Quy tắc**: ≥1 câu hỏi per relevant domain → tránh blind spot.

## Decision-Making & Problem-Solving Questions (NEW v2.1)

### Khi giúp stakeholder DECIDE
1. "Thực sự cần quyết định không, hay đây chỉ là preference?"
2. "Tất cả alternatives là gì — kể cả 'không làm gì'?"
3. "Tiêu chí đánh giá là gì? Tiêu chí có fair cho tất cả?"
4. "Quyết định tốt nhất dựa trên evidence? Kế hoạch rollback?"

### Khi giúp team SOLVE PROBLEMS
1. "Vấn đề chính xác là gì? Cần tách thành sub-problems?"
2. "Mình tạo ra vấn đề hay external? Có thể giải quyết?"
3. "Thông tin gì cần? Có đang close-minded với cách diễn giải nào?"
4. "Short-term vs long-term options? Budget/time/power constraints?"
5. "Đã thực sự giải quyết chưa, hay vẫn tồn tại? Cần đổi strategy?"

## Questioning While Writing (NEW v2.1)

Khi BA VIẾT spec (BRD/SRS/US), tự hỏi:
- **Purpose**: Reader hiểu tôi muốn họ quyết định/làm gì không?
- **Concepts**: Key terms có thể bị hiểu khác nhau bởi 2 reader không?
- **Assumptions**: Tôi có nên state rõ assumptions không?
- **Fairness**: Tôi có present opposing viewpoints fairly?
- **Precision**: Đủ detail để implement không cần guess?
- **Clarity**: Mỗi paragraph có đúng MỘT cách interpret?

## 7 Intellectual Virtues cho BA (NEW v2.1)

| Virtue | Tự kiểm tra |
|--------|-------------|
| **Intellectual Humility** | "Tôi biết gì và KHÔNG biết gì về domain này?" |
| **Intellectual Courage** | "Tôi có dám challenge quyết định phổ biến khi evidence nói khác?" |
| **Intellectual Empathy** | "Tôi có thể state lập luận của đối phương chính xác đến mức họ đồng ý?" |
| **Intellectual Integrity** | "Tôi có apply cùng standard cho assumption của mình và stakeholder?" |
| **Intellectual Perseverance** | "Tôi có willing đào sâu requirement mơ hồ, hay lấy easy answer?" |
| **Confidence in Reason** | "Tôi thay đổi position vì evidence hay vì ai nói?" |
| **Intellectual Autonomy** | "Kết luận là của tôi hay tôi chỉ agree với tiếng nói to nhất?" |

## Kỹ thuật từ v1.0 (giữ nguyên)

### Context-Free Questions (Gause & Weinberg)
Câu hỏi áp dụng được cho BẤT KỲ sản phẩm/dự án nào:
- "Sản phẩm này giải quyết vấn đề gì?"
- "Sản phẩm này có thể TẠO RA vấn đề gì?"
- "Ai có thông tin về dự án mà chưa được hỏi?"
- "Nếu dự án thất bại, lý do có khả năng nhất là gì?"

### Meta-Questions
Câu hỏi về chính việc hỏi:
- "Có câu hỏi nào tôi nên hỏi nhưng chưa hỏi?"
- "Câu hỏi nào tôi đang ngại hỏi? Tại sao?"

### Assumption Surfacing
1. Liệt kê assumptions rõ ràng (stated in document)
2. Phát hiện assumptions ẩn (unstated but required)
3. Challenge: "Bằng chứng nào hỗ trợ assumption này?"
4. Đánh giá risk: "Nếu assumption sai, hậu quả gì?"

### Tiered Question Sets
- **Tier 1 (Must-Ask)**: 3-5 câu quyết định thành công cuộc họp
- **Tier 2 (Should-Ask)**: 3-5 câu đào sâu
- **Tier 3 (Could-Ask)**: 2-3 câu khám phá biên

### Listening Triggers
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
- [ ] Đã audit 8 Intellectual Standards
- [ ] Đã classify question type (One/No/Conflicting)
- [ ] Đã check bias (ego, socio, stakeholder)

## Document Questioning Framework

Khi review BRD/Spec/Proposal, phân tích **Author's Reasoning**:
- **Purpose**: Mục đích tác giả? Có justified?
- **Question**: Document trả lời câu hỏi gì? Đúng câu hỏi chưa?
- **Information**: Evidence có relevant? Accurate? Đủ complex?
- **Concepts**: Key ideas có được clarified?
- **Assumptions**: Tác giả có nhận biết assumptions ẩn?
- **Inferences**: Kết luận có follow từ evidence?
- **Point of View**: Có xem xét alternative viewpoints?
- **Implications**: Có nhận biết consequences?

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
| Document review | Author's Reasoning analysis (8 elements) |
| Concept disambiguation | Wilson's 4 cases |
| Strategic planning | Prior questions chain |
| Stakeholder conflict | Socratic probing + bias detection |

## Agents liên quan
- **@ba-questioning**: Agent chính cho kỹ năng này
- **@ba-elicitation**: Khai thác requirements (sử dụng questioning techniques)
- **@ba-facilitation**: Workshop questioning
- **@ba-conflict**: Probing positions vs interests + bias detection
- **@ba-root-cause**: Causal analysis khi Socratic probing phát hiện vấn đề sâu

## Sources
- **Elder & Paul** — The Art of Asking Essential Questions (Paul-Elder Critical Thinking Framework, 8 Elements of Reasoning, 8 Intellectual Standards, 3 Question Types, Socratic Questioning)
- **Wilson** — Thinking With Concepts (4-Case Concept Analysis)
- **Gause & Weinberg** — Exploring Requirements (Context-Free Questions)
- **BABOK v3** — Elicitation & Collaboration Knowledge Area
- **Gottesdiener** — Requirements Memory Jogger (Meta-Questions)
