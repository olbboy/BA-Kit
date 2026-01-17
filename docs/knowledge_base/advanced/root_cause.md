# 🟣 SKILL-19: ROOT CAUSE ANALYSIS & RESOLUTION (CAR)
## Advanced Skill - Process Optimization

---

## 📌 SKILL METADATA

| Attribute | Value |
|-----------|-------|
| **Skill ID** | SKILL-19 |
| **Category** | 🟣 Advanced |
| **Load When** | Defects rates exceed UCL, recurring issues, process optimization |
| **Dependencies** | SKILL-18 (SPC), SKILL-08 (Validation) |
| **Frameworks** | Six Sigma (DMAIC), Fishbone, 5 Whys, Pareto, ANOVA |
| **Output** | CAR Report, Process Improvement Proposal |

---

## 🎯 MỤC ĐÍCH

Skill này cung cấp phương pháp luận **Causal Analysis and Resolution (CAR)** để đạt mức tối ưu hóa quy trình. Không chỉ sửa lỗi (Correction), skill này giúp loại bỏ **nguyên nhân gốc rễ** (Root Cause) để ngăn ngừa lỗi tái diễn một cách có hệ thống.

---

## 🏗️ CAR PROCESS (Causal Analysis and Resolution)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ROOT CAUSE ANALYSIS WORKFLOW                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. DEFINE           2. MEASURE          3. ANALYZE          4. IMPROVE     │
│  ───────────         ───────────         ───────────         ───────────    │
│  ┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐    │
│  │ Problem │────────►│  Data   │────────►│  Root   │────────►│ Action  │    │
│  │ Statemnt│         │Collection│        │  Cause  │         │  Plan   │    │
│  └─────────┘         └─────────┘         └────┬────┘         └─────────┘    │
│                                               │                             │
│                                      ┌────────┴────────┐                    │
│                                      ▼                 ▼                    │
│                                 Qualitative       Quantitative              │
│                                 (Fishbone)        (Statistical)             │
│                                                                             │
│  5. CONTROL (Verify)                                                        │
│  ───────────────────                                                        │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                              │  │
│  │ Measure │───►│ Update  │───►│ Share   │                              │  │
│  │ Delta   │    │ Process │    │ Lessons │                              │  │
│  └─────────┘    └─────────┘    └─────────┘                              │  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🐟 ISHIKAWA (FISHBONE) DIAGRAM TEMPLATE

Sử dụng để brainstorm các nguyên nhân tiềm năng.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ISHIKAWA / FISHBONE DIAGRAM                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│      PEOPLE           PROCESS             TECHNOLOGY                        │
│      (Man)            (Method)            (Machine)                         │
│                                                                             │
│   Lack of training  │  Ambiguous spec     │  Legacy system              │   │
│   ───────────────>  │  ──────────────>    │  ──────────────>            │   │
│   Fatigue           │  Review skipped     │  Slow network               │   │
│   ───────────────>  │  ──────────────>    │  ──────────────>            │   │
│   New hire          │  No template        │  No auto-test               │   │
│   ───────────────>  │  ──────────────>    │  ──────────────>            │   │
│            \        │         \           │           \                 │   │
│             \       │          \          │            \     ┌────────────┐ │
│              \      │           \         │             \    │            │ │
│  ─────────────\─────┴────────────\────────┴──────────────\───┤  PROBLEM   │ │
│  ─────────────/──────────────────/───────────────────────/───┤  EFFECT    │ │
│              /                  /                       /    │            │ │
│             /                  /                       /     └────────────┘ │
│            /                  /                       /                     │
│   ───────────────>   ──────────────>      ──────────────>                   │
│   Unclear scope      Deadline pressure    Dev environment                   │
│   ───────────────>   ──────────────>      ──────────────>                   │
│   Changing reqs      Budget cuts          No test data                      │
│   ───────────────>   ──────────────>      ──────────────>                   │
│                                                                             │
│      INPUTS             ENVIRONMENT         MEASUREMENT                     │
│      (Material)         (Mother Nature)     (Measurement)                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ❓ 5 WHYS TEMPLATE

Kỹ thuật đào sâu để tìm nguyên nhân gốc rễ thực sự (không dừng lại ở triệu chứng).

### Template

| Level | Question | Answer (Example) |
|-------|----------|------------------|
| **Why 1** | Tại sao [Vấn đề] xảy ra? | Requirements bị hiểu sai bởi Dev team. |
| **Why 2** | Tại sao Dev team hiểu sai? | Mô tả trong ticket quá ngắn gọn, thiếu chi tiết. |
| **Why 3** | Tại sao mô tả quá ngắn gọn? | BA không có đủ thời gian để viết chi tiết. |
| **Why 4** | Tại sao BA không đủ thời gian? | BA phải tham gia quá nhiều cuộc họp không cần thiết. |
| **Why 5** | Tại sao tham gia nhiều họp? | Không có cơ chế từ chối họp hoặc ủy quyền. |
| **ROOT CAUSE** | **Quy trình quản lý thời gian và văn hóa họp không hiệu quả.** |

---

## 📊 PARETO CHART (80/20 Rule)

Sử dụng để ưu tiên giải quyết các nguyên nhân gây ra nhiều tác động nhất.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PARETO ANALYSIS: Defect Causes                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Count (Frequency)                                         Cumulative %     │
│   │                                                                    │    │
│ 50│   █ (45%)                                                 100% ────┤    │
│   │   █                                                     /          │    │
│ 40│   █                                                   _/ (90%)     │    │
│   │   █                                                 _/             │    │
│ 30│   █                                               _/               │    │
│   │   █          █ (25%)                            _/                 │    │
│ 20│   █          █                                _/                   │    │
│   │   █          █          █ (15%)             _/                     │    │
│ 10│   █          █          █          █      _/                       │    │
│   │   █          █          █          █    _/                         │    │
│  0└───┴──────────┴──────────┴──────────┴───┴───────────────────────────┘    │
│      Missing    Ambiguous   Conflict   Typos                                │
│      Scenario     Reqs        Reqs                                          │
│                                                                             │
│  ACTION: Tập trung giải quyết "Missing Scenario" và "Ambiguous Reqs"        │
│          sẽ loại bỏ 70% lỗi (45% + 25%).                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📈 QUANTITATIVE CAUSAL ANALYSIS (Advanced)

Đối với quy trình tối ưu hóa, phân tích định tính (Fishbone) cần được hỗ trợ bởi dữ liệu thống kê.

### 1. Correlation Analysis (Phân tích tương quan)
*   **Mục đích**: Kiểm tra xem yếu tố X có ảnh hưởng đến Y không.
*   **Ví dụ**: Xem xét mối tương quan giữa "Độ dài User Story" (X) và "Số lượng Defect" (Y).
*   **Công cụ**: Scatter Plot, Pearson Correlation Coefficient (r).

### 2. Hypothesis Testing (Kiểm định giả thuyết)
*   **Scenario**: "Có phải việc Reviewing Requirements giúp giảm Defect?"
*   **Null Hypothesis (H0)**: Không có sự khác biệt về số bug giữa nhóm "Có Review" và "Không Review".
*   **Alternative Hypothesis (H1)**: Nhóm "Có Review" có ít bug hơn đáng kể.
*   **Test**: T-Test (nếu dữ liệu phân phối chuẩn) hoặc Mann-Whitney U Test.

### 3. ANOVA (Analysis of Variance)
*   **Scenario**: So sánh hiệu quả của 3 phương pháp Elicitation khác nhau.
*   **Kết quả**: P-value < 0.05 => Có sự khác biệt có ý nghĩa thống kê.

---

## 📝 CAR REPORT TEMPLATE

```markdown
# CAUSAL ANALYSIS REPORT (CAR-202X-001)

## 1. Problem Description
*   **Incident**: High defect rate in Payment Module payment gateway integration.
*   **Impact**: 15% of transactions failing in UAT.
*   **Frequency**: Occurred in Sprint 4, 5, 6.

## 2. Analysis Method
*   [x] Fishbone Diagram
*   [x] 5 Whys
*   [ ] Scatter Plot

## 3. Root Cause Identified
*   **Primary Cause**: Thiếu quy trình cập nhật API Documentation từ bên thứ 3 (Vendor).
*   **Contributing Factor**: Mock server không đồng bộ với Production endpoint thật.

## 4. Corrective Action (Fix existing)
*   Hotfix code để handle response format mới.

## 5. Preventive Action (Prevent recurrence)
*   [Process Change] Tạo job tự động check API Spec của Vendor hàng ngày.
*   [Training] Đào tạo team về "Contract Testing".

## 6. ROI Calculation
*   **Cost of Implement**: 4 hours (Scripting)
*   **Saved Cost**: 20 hours/sprint (Debugging) * 10 sprints = 200 hours.
*   **ROI**: (200 - 4) / 4 = 4900%
```

---

## ✅ CAR CHECKLIST (Level 5)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAR PROCESS CHECKLIST                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SELECTION:                                                                 │
│  ☐ Defect/Issue exceeds control limits (UCL from SKILL-18)                  │
│  ☐ Issue is recurring or high impact                                        │
│  ☐ Benefit of analysis outweighs cost                                       │
│                                                                             │
│  ANALYSIS:                                                                  │
│  ☐ Multidisciplinary team involved (BA, Dev, QA)                            │
│  ☐ Fishbone diagram completed                                               │
│  ☐ 5 Whys drilled down to systemic cause                                    │
│  ☐ Data validates the root cause (not just opinion)                         │
│                                                                             │
│  ACTION:                                                                    │
│  ☐ Corrective action taken (fix the symptom)                                │
│  ☐ Preventive action planned (fix the system)                               │
│  ☐ Process assets updated (checklists, templates, guidelines)               │
│  ☐ Change communicated to all relevant teams                                │
│                                                                             │
│  EVALUATION:                                                                │
│  ☐ Effectiveness of action measured after implementation                    │
│  ☐ ROI calculated                                                           │
│  ☐ Lessons learned added to organizational repository                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔗 RELATED SKILLS

| For... | Load |
|--------|------|
| Identifying outliers | SKILL-18 (SPC) |
| Measuring impact | SKILL-17 (Evaluation) |
| Preventing defects | SKILL-08 (Validation) |

---

*Use this skill to move from "Firefighting" to "Fire Prevention".*
