# 🛠️ SKILL: Requirements Memory Jogger (Quy Trình Yêu Cầu Phần Mềm)
## Nguồn: The Software Requirements Memory Jogger (Ellen Gottesdiener, GOAL/QPC, 2005)

---

## 📌 SKILL METADATA

| Thuộc tính | Giá trị |
|-----------|---------|
| **Skill ID** | EBOOK-07 |
| **Danh mục** | 🟣 Quy trình Phát triển & Quản lý Yêu cầu |
| **Nguồn sách** | The Software Requirements Memory Jogger (Ellen Gottesdiener, 2005, GOAL/QPC) |
| **Đầu ra** | Bộ mô hình phân tích, Quy trình phát triển yêu cầu, Mẫu SRS/URD, Ma trận truy vết |

---

## 🎯 MỤC ĐÍCH

Skill này tổng hợp **toàn bộ quy trình phát triển và quản lý yêu cầu phần mềm** từ cuốn Memory Jogger — một cuốn sổ tay thực chiến với hướng dẫn từng bước cho mọi kỹ thuật, từ xác định tầm nhìn sản phẩm đến quản lý thay đổi yêu cầu.

**Giá trị cốt lõi**: Không chỉ lý thuyết — cuốn sách cung cấp **"How do I do it?"** (Làm thế nào?) cho từng kỹ thuật, kèm ví dụ minh họa xuyên suốt bằng case study CVGC (Crystal Valley Glass Company).

---

## 🧠 KIẾN THỨC CỐT LÕI

### 1. Ba Tầng Yêu Cầu (Three Levels of Requirements)

```
┌─────────────────────────────────────────────────────────────────┐
│                THREE LEVELS OF REQUIREMENTS                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LEVEL 1: BUSINESS REQUIREMENTS (Yêu cầu Kinh doanh)          │
│  ═══════════════════════════════════════════════════            │
│  • WHY the project exists                                      │
│  • Business goals, objectives, vision                          │
│  • Product scope definition                                    │
│  • Success criteria and constraints                            │
│  • Owner: Sponsor, Product Champion                            │
│                                                                 │
│  LEVEL 2: USER REQUIREMENTS (Yêu cầu Người dùng)              │
│  ═══════════════════════════════════════════════                │
│  • WHAT users need to do with the system                       │
│  • Use cases, scenarios, analysis models                       │
│  • User workflow and interaction patterns                      │
│  • Quality expectations from user perspective                  │
│  • Owner: Users, Business Analysts                             │
│                                                                 │
│  LEVEL 3: SOFTWARE REQUIREMENTS (Yêu cầu Phần mềm)            │
│  ═══════════════════════════════════════════════════            │
│  • HOW the system must behave                                  │
│  • Functional requirements (capabilities)                      │
│  • Nonfunctional requirements (quality attributes)             │
│  • Design constraints, external interfaces                     │
│  • Owner: Analysts, Designers, Developers                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Vòng Đời Phát Triển Yêu Cầu (Requirements Development Lifecycle)

```
┌─────────────────────────────────────────────────────────────────┐
│           REQUIREMENTS DEVELOPMENT LIFECYCLE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                   │
│  │ SET THE  │──►│ ELICIT   │──►│ ANALYZE  │                   │
│  │  STAGE   │   │          │   │          │                   │
│  │ (Ch. 2)  │   │ (Ch. 3)  │   │ (Ch. 4)  │                   │
│  └──────────┘   └──────────┘   └──────────┘                   │
│       │                              │                          │
│       │         ┌──────────┐         │                          │
│       │         │ VALIDATE │◄────────┘                          │
│       │         │ (Ch. 6)  │                                    │
│       │         └──────────┘                                    │
│       │              │                                          │
│       │    ┌──────────┐   ┌──────────┐                         │
│       └───►│ SPECIFY  │──►│ MANAGE   │                         │
│            │ (Ch. 5)  │   │ (Ch. 7)  │                         │
│            └──────────┘   └──────────┘                         │
│                                                                 │
│  Key Principle: ITERATIVE — khong tuyến tính                   │
│  Validate sớm và thường xuyên, không đợi đến cuối             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Mô Hình 4W + H (The 4W+H Analysis Model Framework)

> **Đây là framework cốt lõi** của cuốn sách — ánh xạ 5 câu hỏi cơ bản sang các mô hình phân tích cụ thể.

```
┌─────────────────────────────────────────────────────────────────┐
│                    4W + H FRAMEWORK                             │
│           (Mapping Focus Questions → Analysis Models)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WHO? (Ai?)                                                    │
│  ══════════                                                    │
│  • Stakeholder Categories → Xác định các bên liên quan         │
│  • Actor Table → Định nghĩa vai trò tương tác với hệ thống    │
│  • Actor Map → Minh họa quan hệ giữa các actor                │
│  • Personas → Mô tả actor như archetype thực tế                │
│                                                                 │
│  WHAT? (Cái gì?)                                               │
│  ═══════════════                                               │
│  • Glossary → Định nghĩa thuật ngữ kinh doanh                 │
│  • Context Diagram → Ranh giới hệ thống + thực thể bên ngoài  │
│  • Data Model → Cấu trúc dữ liệu logic (entities & relations) │
│  • Class Model → Biến thể OOP của Data Model                  │
│  • Dialog Map → Kiến trúc giao diện người dùng                │
│  • Prototype → Mockup giao diện                               │
│                                                                 │
│  WHEN? (Khi nào?)                                              │
│  ════════════════                                              │
│  • Event-Response Table → Sự kiện kích hoạt hệ thống          │
│  • State Diagram → Vòng đời dữ liệu & chuyển trạng thái      │
│  • State-Data Matrix → Thuộc tính thay đổi theo trạng thái    │
│                                                                 │
│  WHY? (Tại sao?)                                               │
│  ════════════════                                              │
│  • Business Policies → Chính sách & quy định bên ngoài        │
│  • Business Rules → Kiểm soát hành vi hệ thống                │
│  • Decision Tables → Quy tắc phức tạp dạng bảng              │
│  • Decision Trees → Quy tắc phức tạp dạng cây                │
│                                                                 │
│  HOW? (Như thế nào?)                                           │
│  ═══════════════════                                           │
│  • Process Map → Luồng quy trình kinh doanh                   │
│  • Use Cases → Nhiệm vụ hệ thống thực hiện cho actor          │
│  • Use Case Diagram → Actor + Use Cases trực quan              │
│  • Scenarios → Ví dụ cụ thể đi qua use case                   │
│  • Stories → Mô tả use case từ góc nhìn người dùng            │
│  • Activity Diagram → Luồng phức tạp trong use case           │
│  • Data Flow Diagram → Input/Process/Output                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Tám Đặc Điểm Yêu Cầu Chất Lượng Cao

| # | Đặc điểm | Ý nghĩa | Anti-pattern |
|---|----------|---------|-------------|
| 1 | **Correct** | Chính xác phản ánh nhu cầu | Sai nghiệp vụ, hiểu nhầm |
| 2 | **Unambiguous** | Chỉ hiểu theo 1 cách duy nhất | "Nhanh", "Dễ", "Thân thiện" |
| 3 | **Complete** | Đủ thông tin để thiết kế & kiểm thử | TBD tràn lan |
| 4 | **Consistent** | Không mâu thuẫn với yêu cầu khác | Response time vs Security |
| 5 | **Ranked** | Có thứ tự ưu tiên rõ ràng | Mọi thứ đều "Must Have" |
| 6 | **Verifiable** | Có thể kiểm thử được | "Hệ thống phải nhanh" |
| 7 | **Modifiable** | Dễ thay đổi mà không ảnh hưởng lan | Yêu cầu trùng lặp |
| 8 | **Traceable** | Truy vết được nguồn gốc & tác động | Orphan requirements |

---

## 📋 15 MÔ HÌNH PHÂN TÍCH CHI TIẾT

### MODEL 01: Vision Statement (Tuyên bố Tầm nhìn)

**Mục đích**: Định nghĩa sản phẩm trong 1 đoạn văn ngắn, tạo sự đồng thuận về mục tiêu.

**Template**:
```
FOR         [target customer/user]
WHO         [statement of need or opportunity]
THE         [product name]
IS          [product category]
THAT        [key benefit, compelling reason to buy/use]
UNLIKE      [primary competitive alternative]
OUR PRODUCT [statement of primary differentiation]
```

**Steps**:
1. Identify targeted customer segments
2. Identify stakeholder needs and benefits
3. Identify the product (name, category)
4. List reasons why customers will buy/use
5. List competitive alternatives
6. State unique differentiation
7. Write the statement and circulate for revision

---

### MODEL 02: Glossary (Bảng Thuật ngữ)

**Mục đích**: Tạo ngôn ngữ chung, loại bỏ nhập nhằng thuật ngữ kinh doanh.

**Steps**:
1. Scan vision statement for business terms
2. Identify terms from elicitation activities
3. Identify synonyms, homonyms, abbreviations
4. Write clear definitions in active voice
5. Get stakeholder agreement on all definitions
6. Maintain throughout requirements lifecycle

**Format**: `Term | Definition | Synonyms | Source`

---

### MODEL 03: Context Diagram (Biểu đồ Bối cảnh)

**Mục đích**: Xác định ranh giới hệ thống và các thực thể bên ngoài tương tác với hệ thống.

**Steps**:
1. Name the system (draw as single circle/rectangle at center)
2. Identify external entities (people, systems, organizations)
3. Draw data flows between system and external entities
4. Name each data flow with business terminology
5. Review for missing entities/flows by checking vision and events

**Links**: External entities → Actor Table; Data flows → Data Model; Events → Event-Response Table

---

### MODEL 04: Event-Response Table (Bảng Sự kiện - Phản hồi)

**Mục đích**: Xác định các sự kiện kích hoạt hệ thống hành động, cùng với phản hồi mong đợi.

**3 loại sự kiện**:
| Loại | Kích hoạt bởi | Ví dụ |
|------|--------------|-------|
| **Business Event** | Con người bên ngoài | Khách hàng yêu cầu báo giá |
| **Temporal Event** | Thời gian | Cuối tháng → tạo hóa đơn |
| **Signal Event** | Hệ thống bên ngoài | Thanh toán đến từ ngân hàng |

**Format per row**: Event Name | Event Type | Stimulus | Response | Actor

**Steps**:
1. Brainstorm events from vision and context diagram
2. Categorize each event (Business/Temporal/Signal)
3. Identify the stimulus (what triggers the event)
4. Define the expected system response
5. Add missing events from user interviews

**Links**: Events → Use Cases (each event triggers one or more UCs); Events → State Diagram transitions

---

### MODEL 05: Business Policies (Chính sách Kinh doanh)

**Mục đích**: Xác định các chính sách, quy định, tiêu chuẩn bên ngoài ảnh hưởng đến hệ thống.

**Steps**:
1. Identify external policies, standards, regulations
2. Identify internal organizational policies
3. Decompose policies into business rules
4. Identify rules enforced in software vs. business processes
5. Validate with compliance and legal stakeholders

---

### MODEL 06: Actor Table & Actor Map (Bảng & Sơ đồ Actor)

**Mục đích**: Định nghĩa ai tương tác trực tiếp với hệ thống và quan hệ giữa các vai trò.

**Actor Table Format**:
| Actor | Description | Type | Use Cases | Frequency |
|-------|-------------|------|-----------|-----------|

**Actor Categories**:
- **Direct Users**: Tương tác trực tiếp với hệ thống
- **Indirect Users**: Nhận output hoặc bị ảnh hưởng bởi hệ thống
- **External Systems**: Gửi/nhận dữ liệu tự động

**Personas** (Variation): Mô tả actor như một nhân vật thực tế với tên, vai trò, kỹ năng, mục tiêu, thái độ

**Steps**:
1. Review context diagram for external entities
2. Identify human actors and their roles
3. Identify system actors (external interfaces)
4. Write brief description for each
5. Create Actor Map showing role hierarchies and relationships

---

### MODEL 07: Use Cases (Ca sử dụng)

**Mục đích**: Mô tả các nhiệm vụ hệ thống thực hiện để đáp ứng mục tiêu của actor.

**Use Case Template**:
```
USE CASE NAME:    [Verb + Noun, e.g., "Schedule Job"]
USE CASE ID:      [UC-nnn]
PRIMARY ACTOR:    [Who initiates?]
PRECONDITIONS:    [What must be true before?]
TRIGGER:          [What event starts this?]
BASIC FLOW:
  1. Actor does X
  2. System responds with Y
  3. ...
ALTERNATIVE FLOWS:
  3a. If condition, then...
POSTCONDITIONS:   [What is true after success?]
BUSINESS RULES:   [BR-nn references]
```

**Variations**:
- **Use Case Diagram**: Actors (stick figures) + UCs (ovals) + System Boundary
- **Use Case Map**: Shows dependencies between UCs
- **Use Case Packages**: Groups UCs into higher-level system functions
- **Scenarios**: Specific paths through a UC with concrete data
- **Stories**: UC paths from user perspective (narrative form)
- **Activity Diagrams**: Complex UC flows with forks, joins, decisions

**Steps**:
1. Name the use case (strong action verb + noun)
2. Identify primary actor and trigger
3. Write the basic flow (happy path)
4. Identify alternative and exception flows
5. Define pre- and post-conditions
6. Reference business rules
7. Walk through with stakeholders

---

### MODEL 08: Dialog Map (Sơ đồ Giao diện)

**Mục đích**: Minh họa kiến trúc giao diện người dùng — luồng điều hướng giữa các màn hình.

**Steps**:
1. Identify primary dialogs (screens, pages) from use cases
2. Identify transitions between dialogs (user navigation paths)
3. Draw navigation paths with labels showing triggers
4. Add decision points for conditional navigation
5. Validate by walking through scenarios

**Variation — Dialog Hierarchy**: Shows screens arranged as a tree structure for web page navigation.

**Variation — Prototype**: Exploratory or Evolutionary — để validate UI requirements.

---

### MODEL 09: Data Model (Mô hình Dữ liệu)

**Mục đích**: Mô tả cấu trúc dữ liệu logic, các thực thể và quan hệ giữa chúng.

**Components**:
- **Entities**: Groups of related data (rectangles)
- **Attributes**: Data elements within entities
- **Relationships**: Named connections between entities with cardinality
- **Cardinality**: 1:1, 1:M, M:M
- **Optionality**: Required (mandatory) vs Optional

**Steps**:
1. Identify entities from nouns in vision, events, use cases
2. Define attributes for each entity
3. Name relationships using active verbs (avoid "has", "uses")
4. Determine cardinality and optionality for each relationship
5. Normalize the model (remove redundancy)
6. Create Data Dictionary with attribute details

**Variations**:
- **Class Model** (OOP): Entities → Classes with methods
- **Data Dictionary**: Flat list of all attributes with types, constraints
- **Data Tables**: Sample data for validation

**Links**: Entities ↔ Glossary terms; Attributes ↔ Business Rules; Entities ↔ State Diagram

---

### MODEL 10: State Diagram (Biểu đồ Trạng thái)

**Mục đích**: Minh họa vòng đời dữ liệu — các trạng thái và sự kiện chuyển đổi trạng thái.

**Steps**:
1. Select critical entities from the data model
2. List all possible lifecycle states for each entity
3. Reduce states to those within product scope
4. Arrange states in time-ordered sequence
5. Identify triggering events for each transition
6. Review related requirements for missing elements

**Variation — State-Data Matrix**: Shows which attributes change during each state transition.

**Links**: Each state → data in data model; Each transition → event in event-response table; Transitions → use cases; States → business rules

---

### MODEL 11: Business Rules (Quy tắc Kinh doanh)

**Mục đích**: Xác định các kiểm soát chi phối hành vi hệ thống, phân biệt rule trong phần mềm vs. quy trình thủ công.

**4 loại Business Rules**:

| Category | Meaning | Example |
|----------|---------|---------|
| **Terms** (+ Derivations, Inferences) | Định nghĩa khái niệm kinh doanh | "A Job is a set of services provided to a Customer" |
| **Facts** | Kết nối giữa các terms | "Each Job belongs to one Customer" |
| **Constraints** | Ngăn cấm hành vi | "Overdue Customers cannot schedule Jobs" |
| **Action Enablers** | Kích hoạt hành động khi điều kiện đúng | "If Repeat Customer's Jobs exceed $5,000, offer 15% discount" |

**Atomic Business Rule Templates**:
```
If <condition> then <action>
On <event> then <action>
On <event> if <condition> then <action>
If <condition> then <conclusion>
<[qualified] term> <verb phrase> <non-verb phrase>
<[qualified] term> must | must not <verb phrase> <non-verb phrase>
```

**Steps**:
1. Identify sources: policies, events, use cases, data model, states
2. Ask discovery questions (What decisions? What must be true? What can go wrong?)
3. Document each rule as declarative statement (no sequencing)
4. Categorize: Term / Fact / Constraint / Action Enabler
5. Determine: enforced in software or by business process?
6. Assign: BR-ID, Owner, Effective Date, Source, Associated Use Cases
7. Analyze for consistency and necessity

**Variations**:
- **Decision Tables**: Complex rules in tabular format (conditions × actions)
- **Decision Trees**: Graphical alternative showing sequential conditions

---

### MODEL 12: Prioritized Requirements (Yêu cầu Ưu tiên)

**Mục đích**: Xếp hạng yêu cầu để phân bổ nguồn lực và quyết định phạm vi triển khai.

**Technique A — Weighted Criteria Matrix** (3-6-9 scoring):
1. Organize requirements at same level of detail
2. Assemble stakeholder team (<7 people)
3. Identify criteria (value, cost, risk, time-to-market, etc.)
4. Weight criteria (pairwise comparison)
5. Score requirements against criteria (3=Weak, 6=Medium, 9=Strong)
6. Calculate total, decide delivery order

**Technique B — Value/Cost/Risk Formula**:
```
Priority = Value% (Benefit + Penalty) / (Cost% + Risk%)
```
Sort descending — highest priority first.

**Technique C — MoSCoW with 20% Rule**:
| Rank | Meaning | Constraint |
|------|---------|-----------|
| Must | Mandatory, product unusable without it | Max 20% |
| Should | Important, significant loss without it | Max 20% |
| Could | Nice-to-have, can postpone | Max 20% |
| Won't | Not considered now | Max 20% |

---

## 📝 MẪU TÀI LIỆU (Document Templates)

### User Requirements Document (URD) Outline

```
1. Introduction
   1.1 Purpose and background
   1.2 Overview of business and user needs
   1.3 Document overview and conventions
   1.4 References
2. Current system or situation
   2.1 Background, objectives, scope
   2.2 Current business processes
   2.3 People, organizations, locations
3. Justification for the new system
   3.1 Rationale for the new system
   3.2 Overview of system and impacted processes
   3.3 Affected people, roles, organizations
   3.4 Priorities and scope of change
   3.5 Impact on operations, organization, people
   3.6 Impact on policies, regulations, business rules
4. New functionality
   4.1 Users and user profiles
   4.2 New or changed user capabilities
   4.3 Impact on existing processes and systems
   4.4 Interfaces with other systems
   4.5 User support and documentation
5. Evaluation of proposed system
   5.1 Advantages, disadvantages, limitations
   5.2 Change management plan
   5.3 Operational issues
   5.4 Alternatives considered
Appendices: Glossary, Data Dictionary, Context Diagram, Use Cases
```

### Software Requirements Specification (SRS) Outline

```
1. Introduction
   1.1 Purpose
   1.2 Document conventions
   1.3 References
2. Overall description
   2.1 Product overview
   2.2 Product stakeholders and users
   2.3 Product features
   2.4 User documentation
   2.5 Assumptions and dependencies
   2.6 Design and implementation constraints
3. Functional requirements
   3.1 Feature 1 (decomposed to FR statements)
   3.2 Feature 2
   3.3 Feature 3
4. External interface requirements
   4.1 User interfaces
   4.2 Hardware interfaces
   4.3 Software interfaces
5. Quality attributes
Appendices: Glossary, Analysis Models, Priority/Attributes, Trace Matrices
```

### Functional Requirement Sentence Template

```
[<restriction>] <subject> <action verb> [<observable result>] [<qualifier>]

Where:
  [<restriction>]    = Conditions under which requirement must be satisfied
  <subject>          = Who/what performs the task ("the system" or actor)
  <action verb>      = Task being performed
  [<observable result>] = Outcome of the action
  [<qualifier>]      = Quality attributes for the requirement
  [ ] = optional components

Examples:
  "The system shall allow a scheduler to select services for the job."
  "When no contractor is available, the system shall display nearby postal codes."
  "When approved, the system shall generate a dispatch ticket within 30 seconds."
```

---

## 🔍 VALIDATION TECHNIQUES

### 4 Kỹ thuật Validation

| Technique | When to Use | Deliverable |
|-----------|-------------|-------------|
| **Peer Review** | Right mix of reviewers available; quality-focused culture | Reviewed Requirements |
| **User Acceptance Tests** | Users willing and available; tests saved for final testing | Acceptance Test Cases |
| **Model Validation** | Models exist; tests can be devised from scenarios | Validated Models |
| **Operational Prototype** | User expectations manageable; developers + tools available | Working Prototype |

### SRS Inspection Checklist (from Appendix D)

- **Correctness**: Solution-independent? Free from errors? Cross-references correct?
- **Clarity**: Single interpretation? Uniquely identified? Consistent detail level?
- **Completeness**: All interfaces defined? All inputs/outputs specified? All tasks covered? Business rules documented? Quality attributes with metrics?
- **Consistency**: No conflicts? Trade-offs specified? Standard format?
- **Relevancy**: Each requirement necessary for vision? Boundaries identified? Priorities included? Traceable to origin?
- **Feasibility**: Achievable with existing tech? Within approved resources?
- **Verifiability**: Can be tested? Test criteria derivable? Basis for test plans?

### User Acceptance Test Severity Levels

| Level | Severity | Definition |
|-------|----------|-----------|
| 1 | Critical | Impossible to continue testing or accept the system |
| 2 | Major | Testing can continue, system cannot be deployed |
| 3 | Medium | System deployed with departure from agreed functionality |
| 4 | Minor | Correctable, will not impact business functionality |
| 5 | Cosmetic | Colors, fonts, interface displays — future correction |

---

## 🔄 REQUIREMENTS MANAGEMENT

### Change Control Process

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Submit   │──►│ Review   │──►│ Decide   │──►│ Update   │
│ Change   │   │ Request  │   │ (CCB)    │   │ Baseline │
│ Request  │   │ (Valid?) │   │          │   │          │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
                    │               │
                    ▼               ▼
               [Invalid:       [Reject →
                Revise]         Notify +
                                Record]
```

**CCB (Change Control Board)**: <10 members, balance of business + technical, clear decision process.

### Requirements Attributes

| Attribute | Purpose |
|-----------|---------|
| Rationale | Purpose for the requirement |
| Priority | Relative importance (Must/Should/Could/Won't) |
| Status | Current state (Proposed→Approved→Tested→Deferred→Rejected) |
| Status Date | Date of current status assignment |
| Owner | Person responsible for verification |
| Source | Origin (regulation, customer, derived) |
| Complexity | High / Medium / Low |
| Volatility | Likelihood of change during implementation |
| Supporting Material | References to regulations, standards, manuals |

### Requirements Trace Matrix (RTM)

**Forward Tracing**: Requirements → Design → Code → Tests
**Backward Tracing**: Tests → Code → Design → Requirements

| Requirement | Use Case | Design Component | Code Module | Test Case | Status |
|-------------|----------|-----------------|-------------|-----------|--------|
| SCH-3.2 | UC1, UC3 | DE-436 | CVSC9897 | ACTSC421 | Approved |

---

## ⚖️ CHANGE-DRIVEN vs RISK-DRIVEN CALIBRATION

| Factor | Risk-Driven | Change-Driven |
|--------|-------------|---------------|
| **Criticality** | Mission/Safety/Financial critical | Business-critical but not life-threatening |
| **Requirements** | Determinable in advance, relatively stable | Dynamic, volatile, emergent |
| **Team** | Large (12+), distributed, mixed experience | Small (7-), collocated, experienced |
| **Documentation** | Extensive — shared externally, regulatory | Minimal — internal, face-to-face focus |
| **User Involvement** | Formally managed, contractual | Collocated, informal daily/weekly |
| **Models** | Multiple detailed models verified against each other | Stories/scenarios, informal representations |
| **Validation** | Inspections + prototypes + model validation | User acceptance tests primarily |
| **Iterations** | Longer (1 month+) | Shorter (days/weeks) |

---

## 📐 PROJECT TYPE ADAPTATION

| Project Type | Chief Concern | Suggested Models |
|-------------|---------------|-----------------|
| **New Development** | Balance completeness with speed | Vision, Context Diagram, Events, Actors, Use Cases, Rules, Data Model, Quality Attributes |
| **Enhancement** | Unreliable existing documentation | As-Is + To-Be: Context, Actors, Data, Use Cases, Rules, Quality |
| **Correction** | Introducing new errors with changes | Business Rules, Data Model, Use Cases, UAT, Quality |
| **Adaptation** | Not losing existing functionality | Quality Attributes, External Interfaces, Use Cases |
| **COTS** | Selecting/configuring the right package | Process Map, Actors, Use Cases, Rules, Data Model, UAT, Quality |

---

## 🚫 AMBIGUOUS WORDS TO AVOID (Appendix F)

> Khi viết yêu cầu, **TUYỆT ĐỐI TRÁNH** các từ/cụm từ sau:

`adequate`, `appropriate`, `as appropriate`, `as quickly as possible`, `at least`, `automatically`, `bad`, `best practice`, `better`, `but not limited to`, `capability of`, `clearly`, `compatible`, `completely`, `could`, `easy`, `effective`, `efficient`, `etc.`, `excellent`, `fast`, `fault-tolerant`, `flexible`, `good`, `however`, `ideally`, `if possible`, `intuitive`, `large`, `lightweight`, `low`, `many`, `maximize`, `may`, `minimal`, `minimize`, `most`, `nearly`, `necessary`, `needed`, `normal`, `often`, `optimize`, `optionally`, `portable`, `possible`, `practical`, `provide for`, `quality`, `quickly`, `rapid`, `readily`, `reasonable`, `relevant`, `robust`, `safely`, `seamless`, `several`, `should`, `significant`, `simple`, `sometimes`, `substantial`, `sufficient`, `suitable`, `support`, `target`, `timely`, `to be determined (TBD)`, `transparent`, `typically`, `user-friendly`, `usually`, `when necessary`, `where appropriate`, `worse`

**Cách sửa**: Thay mỗi từ mơ hồ bằng một **metric cụ thể có thể kiểm thử**.
- ❌ "The system shall respond quickly"
- ✅ "The system shall respond within 3 seconds for 98% of queries"

---

## 📊 QUALITY ATTRIBUTES & METRICS (Appendix E)

### Operational Environment

| Attribute | Meaning | Metrics |
|-----------|---------|---------|
| **Performance** | Speed, throughput, capacity | Response time, concurrent users, data volume |
| **Reliability** | Probability of no failure | MTBF, failure rate, probability of failure on demand |
| **Robustness** | Behavior under failure conditions | Restart time, % events causing failure |
| **Security** | Resist unauthorized access | # unauthorized attempts, % blocked |
| **Usability** | Ease of effective use | Time to competence, error rate, training time |

### Deployment Environment

| Attribute | Meaning | Metrics |
|-----------|---------|---------|
| **Availability** | System up-time | % time available for user access |
| **Flexibility** | Ability to extend | Effort/cost to add new features |
| **Interoperability** | Data/service exchange | Effort/cost for integration |
| **Installability** | Ease of deployment | Time to load and configure |
| **Portability** | Move to other environments | Cost/effort to migrate |
| **Recoverability** | Recovery from failures | Time to return to prior state |
| **Scalability** | Expand users/capabilities | User growth range, % capacity growth |
| **Safety** | No harm to people/environment | Acceptable accident rate by severity |

### Development Environment

| Attribute | Meaning | Metrics |
|-----------|---------|---------|
| **Efficiency** | Resource utilization | % memory/CPU/disk during operations |
| **Maintainability** | Ease of changes | Time/cost to fix or add features |
| **Reusability** | Components in other systems | Cost to integrate into other apps |
| **Testability** | Ease of testing | Cost per defect found, test coverage |

---

## 📋 REQUIREMENTS RETROSPECTIVE QUESTIONS (Appendix G)

### Setting the Stage
- How well did we define and communicate the product vision?
- How clear was our scope? How might we make it clearer?

### Stakeholder Involvement
- Did we identify the right stakeholders?
- Were customers involved appropriately?
- Did customers believe we made good use of their time?

### Requirements Development
- Did we choose the right analysis models?
- How effectively did we verify the analysis models?
- Did we have enough documentation? Was any unnecessary?
- Did developers find our documentation useful?

### Requirements Management
- Have we controlled changes in a timely manner?
- How volatile are the requirements and why?
- Did our change control guard against scope creep?

### Overall Assessment
- What do we want to remember to do again?
- What surprises or issues have there been?
- What are the top two things we should improve?

---

## 🔗 LIÊN KẾT GIỮA CÁC MÔ HÌNH (Model Threading)

```
┌─────────────────────────────────────────────────────────────────┐
│                HOW MODELS THREAD TOGETHER                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Vision Statement ──► Context Diagram ──► Event-Response Table │
│         │                    │                     │            │
│         │                    ▼                     ▼            │
│         │              Actor Table ◄──────► Use Cases           │
│         │                    │                │    │            │
│         ▼                    ▼                │    │            │
│     Glossary           Actor Map              │    │            │
│         │                                     │    │            │
│         ▼                                     │    │            │
│     Data Model ◄──────────────────────────────┘    │            │
│         │                                          │            │
│         ▼                                          ▼            │
│   State Diagram ◄──────────────────────── Business Rules        │
│         │                                     ▲    │            │
│         │                                     │    │            │
│         └─────────────► Dialog Map ───────────┘    │            │
│                              │                     │            │
│                              ▼                     ▼            │
│                         Scenarios ──────► Prioritized Reqs      │
│                                                                 │
│  KEY INSIGHT: No single model describes all requirements.       │
│  Elements of one model link to and uncover elements in another. │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ CHECKLIST MEMORY JOGGER

- [ ] Đã tạo Vision Statement với template For/Who/The/Is/That/Unlike?
- [ ] Đã xây dựng Glossary từ vision statement và elicitation?
- [ ] Đã vẽ Context Diagram xác định ranh giới hệ thống?
- [ ] Đã tạo Event-Response Table cho tất cả events?
- [ ] Đã xác định Business Policies & Rules?
- [ ] Đã tạo Actor Table với đầy đủ vai trò?
- [ ] Đã viết Use Cases theo template chuẩn?
- [ ] Đã tạo Data Model/ERD?
- [ ] Đã vẽ State Diagram cho entities phức tạp?
- [ ] Đã viết functional requirements với sentence template?
- [ ] Đã loại bỏ ambiguous words (Appendix F)?
- [ ] Đã quantify quality attributes với metrics cụ thể?
- [ ] Đã prioritize bằng Weighted Criteria hoặc Value/Cost/Risk?
- [ ] Đã tạo Requirements Trace Matrix?
- [ ] Đã validate bằng Peer Review hoặc Model Validation?
- [ ] Đã thiết lập Change Control Process?
- [ ] Đã chọn đúng mô hình cho loại dự án (New/Enhancement/COTS)?

---

## 🔗 KỸ NĂNG LIÊN QUAN

| Để làm... | Tham khảo Skill |
|-----------|-----------------| 
| Nền tảng BA | EBOOK-01 (Fundamentals) |
| Kỹ thuật thực hành | EBOOK-02 (Techniques - 99 Tools + Wiegers + UML) |
| Leadership & Workshop | EBOOK-03 (Leadership) |
| Agile / Scrum | EBOOK-04 (Agile) |
| Systems Thinking | ebook-systems-thinking.md |
