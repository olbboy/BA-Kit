# 🛠️ SKILL: BA Techniques (Kỹ Thuật Thực Hành)
## Nguồn: 99 Essential Tools, Software Requirements (Wiegers), UML Distilled (Fowler)

---

## 📌 SKILL METADATA

| Thuộc tính | Giá trị |
|-----------|---------|
| **Skill ID** | EBOOK-02 |
| **Danh mục** | 🟢 Kỹ thuật Thực hành |
| **Nguồn sách** | BA Techniques: 99 Tools (Paul, Cadle), Software Requirements 3rd (Wiegers, Beatty), UML Distilled (Fowler) |
| **Đầu ra** | Bộ công cụ kỹ thuật, Mô hình hóa, Đặc tả yêu cầu |

---

## 🎯 MỤC ĐÍCH

Skill này tổng hợp **99+ kỹ thuật thực hành** được sử dụng trong công việc BA hàng ngày, từ việc khai thác thông tin đến mô hình hóa và đặc tả yêu cầu phần mềm.

---

## 🧠 KIẾN THỨC CỐT LÕI

### 1. 99 Essential Tools — Phân Loại Theo Mục Đích

```
┌─────────────────────────────────────────────────────────────────┐
│                    99 TOOLS - CATEGORIZATION                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STRATEGY & CONTEXT (Hiểu bối cảnh)                             │
│  ═══════════════════════════════════                            │
│  • PESTLE Analysis (Political, Economic, Social, Tech, Legal)   │
│  • SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)│
│  • Porter's Five Forces                                         │
│  • Business Model Canvas                                        │
│  • Value Chain Analysis                                         │
│                                                                 │
│  INVESTIGATION & ELICITATION (Khai thác)                        │
│  ═══════════════════════════════════════                        │
│  • Structured Interview                                         │
│  • Questionnaire Design                                         │
│  • Workshop Facilitation                                        │
│  • Observation (Shadowing)                                      │
│  • Document Analysis                                            │
│  • Rich Pictures                                                │
│  • Mind Mapping                                                 │
│                                                                 │
│  MODELING & ANALYSIS (Mô hình hóa)                              │
│  ═════════════════════════════════                              │
│  • Use Case Diagrams                                            │
│  • User Stories (INVEST)                                        │
│  • Process Mapping (BPMN, Swimlanes)                            │
│  • Data Flow Diagrams (DFD)                                     │
│  • Entity Relationship Diagrams (ERD)                           │
│  • State Machine Diagrams                                       │
│  • Decision Tables                                              │
│  • Decision Trees                                               │
│                                                                 │
│  DEFINITION & DOCUMENTATION (Đặc tả)                            │
│  ═══════════════════════════════════                            │
│  • Requirements Catalog                                         │
│  • Use Case Specifications                                      │
│  • Functional Requirements Template                             │
│  • Non-Functional Requirements Template                         │
│  • Business Rules Catalog                                       │
│                                                                 │
│  PRIORITIZATION & SELECTION (Ưu tiên)                           │
│  ════════════════════════════════════                           │
│  • MoSCoW Prioritization                                        │
│  • Requirements Ranking                                         │
│  • Timeboxing/Budgeting                                         │
│  • Cost-Benefit Analysis                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Software Requirements (Wiegers) — The Requirements Engineering Bible

```
┌─────────────────────────────────────────────────────────────────┐
│                    WIEGERS FRAMEWORK                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  REQUIREMENTS DEVELOPMENT:                                      │
│  ══════════════════════════                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Elicit     │─►│  Analyze    │─►│  Specify    │             │
│  │  (Gather)   │  │  (Organize) │  │  (Document) │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                                  │                    │
│         │              ┌───────────────────┘                    │
│         │              ▼                                        │
│         │      ┌─────────────┐                                  │
│         └─────►│  Validate   │                                  │
│                │  (Confirm)  │                                  │
│                └─────────────┘                                  │
│                                                                 │
│  REQUIREMENTS MANAGEMENT:                                       │
│  ════════════════════════                                       │
│  • Baseline requirements                                        │
│  • Change Control Process                                       │
│  • Version Control                                              │
│  • Traceability Matrix                                          │
│  • Impact Analysis                                              │
│                                                                 │
│  QUALITY ATTRIBUTES (INVEST + More):                            │
│  ═══════════════════════════════════                            │
│  │ I │ Independent - Không phụ thuộc chéo                      │
│  │ N │ Negotiable - Có thể thương lượng                        │
│  │ V │ Valuable - Mang lại giá trị                             │
│  │ E │ Estimable - Có thể ước lượng                            │
│  │ S │ Small - Đủ nhỏ để phát triển trong 1 sprint             │
│  │ T │ Testable - Có thể kiểm thử                              │
│  └───┴─────────────────────────────────────────────────────────│
│                                                                 │
│  + Correct, Unambiguous, Complete, Consistent, Ranked,         │
│    Verifiable, Modifiable, Traceable                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Lưu ý quan trọng từ Wiegers:**
> "Một yêu cầu tồi sẽ truyền bệnh cho cả dự án. Chi phí sửa lỗi yêu cầu ở giai đoạn Testing cao gấp 50-200 lần so với giai đoạn Requirements."

### 3. UML Distilled (Fowler) — Mô Hình Hóa Tinh Gọn

```
┌─────────────────────────────────────────────────────────────────┐
│                    UML ESSENTIAL DIAGRAMS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STRUCTURE DIAGRAMS (Cấu trúc):                                 │
│  ══════════════════════════════                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ CLASS DIAGRAM                                            │   │
│  │ • Entities, Attributes, Methods                          │   │
│  │ • Relationships: Association, Aggregation, Composition   │   │
│  │ • Inheritance (Generalization)                           │   │
│  │ • Multiplicity (1..*, 0..1, etc.)                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  BEHAVIOR DIAGRAMS (Hành vi):                                   │
│  ════════════════════════════                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ USE CASE DIAGRAM                                         │   │
│  │ • Actors (Stick figures)                                 │   │
│  │ • Use Cases (Ovals)                                      │   │
│  │ • Relationships: Include, Extend, Generalization         │   │
│  │ • System Boundary                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ SEQUENCE DIAGRAM                                         │   │
│  │ • Lifelines (Actors, Objects)                            │   │
│  │ • Messages (Arrows: sync, async, return)                 │   │
│  │ • Activation Bars                                        │   │
│  │ • Combined Fragments (alt, opt, loop)                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ACTIVITY DIAGRAM                                         │   │
│  │ • Initial/Final Nodes                                    │   │
│  │ • Actions, Decisions (Diamond)                           │   │
│  │ • Fork/Join (Parallel)                                   │   │
│  │ • Swimlanes (Partitions)                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ STATE MACHINE DIAGRAM                                    │   │
│  │ • States (Rounded rectangles)                            │   │
│  │ • Transitions (Arrows with events/guards/actions)        │   │
│  │ • Entry/Exit/Do Activities                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Triết lý Fowler:**
> "Chỉ dùng UML khi nó giúp giao tiếp hiệu quả hơn. Đừng vẽ diagram chỉ vì quy trình yêu cầu."

---

## 📋 TECHNIQUE SELECTION MATRIX

| Nhu cầu | Kỹ thuật đề xuất |
|---------|------------------|
| Hiểu bối cảnh kinh doanh | PESTLE, SWOT, Business Model Canvas |
| Thu thập yêu cầu từ SME | Interview, Workshop, Observation |
| Mô tả luồng nghiệp vụ | BPMN, Activity Diagram, Swimlanes |
| Mô tả dữ liệu | ERD, Class Diagram, Data Dictionary |
| Mô tả tương tác hệ thống | Use Case Diagram, Sequence Diagram |
| Mô tả trạng thái | State Machine Diagram |
| Mô tả logic quyết định | Decision Table, Decision Tree |
| Ưu tiên yêu cầu | MoSCoW, RICE, WSJF |

---

## ✅ CHECKLIST KỸ THUẬT

- [ ] Đã chọn đúng kỹ thuật cho context hiện tại?
- [ ] Đã áp dụng INVEST cho User Stories?
- [ ] Đã tạo Traceability Matrix (Wiegers)?
- [ ] Chỉ dùng UML khi thực sự cần (Fowler)?
- [ ] Đã validate kết quả kỹ thuật với stakeholder?

---

## 🔗 KỸ NĂNG LIÊN QUAN

| Để làm... | Tham khảo Skill |
|-----------|-----------------|
| Nền tảng BA | EBOOK-01 (Fundamentals) |
| Workshop facilitation | EBOOK-03 (Leadership) |
| Kỹ thuật Agile | EBOOK-04 (Agile) |
