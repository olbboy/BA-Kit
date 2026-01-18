# 🔮 SKILL: Systems Thinking (Tư Duy Hệ Thống)
## Nguồn: Thinking in Systems: A Primer (Donella H. Meadows)

---

## 📌 SKILL METADATA

| Thuộc tính | Giá trị |
|-----------|---------|
| **Skill ID** | EBOOK-05 |
| **Danh mục** | 🔴 Tư duy Chiến lược |
| **Nguồn sách** | Thinking in Systems: A Primer (Donella H. Meadows) |
| **Đầu ra** | Phân tích hệ thống, Tìm Leverage Points, Tránh hậu quả không mong muốn |

---

## 🎯 MỤC ĐÍCH

Skill này tổng hợp **tư duy hệ thống** — cách nhìn nhận tổ chức và phần mềm như các hệ thống phức tạp với các vòng phản hồi. Đây là kỹ năng nâng cao để **tránh giải pháp ngắn hạn gây hại dài hạn**.

---

## 🧠 KIẾN THỨC CỐT LÕI

### 1. Định Nghĩa Hệ Thống (System)

```
┌─────────────────────────────────────────────────────────────────┐
│                    WHAT IS A SYSTEM?                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  "A system is a set of elements interconnected in a way that   │
│   produces its own pattern of behavior over time."              │
│                                                                 │
│  CẤU TRÚC HỆ THỐNG:                                             │
│  ═══════════════════                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                           │  │
│  │   ELEMENTS + INTERCONNECTIONS + PURPOSE = SYSTEM          │  │
│  │                                                           │  │
│  │   • Elements: Các thành phần (Users, Data, Processes)     │  │
│  │   • Interconnections: Mối quan hệ (APIs, Workflows)       │  │
│  │   • Purpose: Mục đích (Mục tiêu kinh doanh)               │  │
│  │                                                           │  │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  VÍ DỤ:                                                         │
│  • Hệ thống ERP = Modules + Integrations + "Manage Resources"  │
│  • Hệ thống E-commerce = Products + Orders + "Sell Online"     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Stocks & Flows — Nền Tảng Của Mọi Hệ Thống

```
┌─────────────────────────────────────────────────────────────────┐
│                    STOCKS & FLOWS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│           INFLOW                            OUTFLOW             │
│              │                                 │                │
│              ▼                                 ▼                │
│         ┌────┴────┐                       ┌────┴────┐          │
│         │ ══════▶ │   ┌─────────────┐    │ ══════▶ │          │
│         │  Valve  │─▶ │   STOCK     │─▶  │  Valve  │          │
│         │         │   │ (Bể chứa)   │    │         │          │
│         └─────────┘   └─────────────┘    └─────────┘          │
│                                                                 │
│  VÍ DỤ TRONG SOFTWARE:                                          │
│  ═════════════════════                                          │
│  • Stock: Số lượng bug trong backlog                            │
│  • Inflow: Bugs mới được báo cáo                                │
│  • Outflow: Bugs được fix                                       │
│                                                                 │
│  → Nếu Inflow > Outflow liên tục, Stock sẽ tăng vô hạn!        │
│                                                                 │
│  VÍ DỤ TRONG BUSINESS:                                          │
│  ═════════════════════                                          │
│  • Stock: Số khách hàng                                         │
│  • Inflow: Khách mới (Marketing)                                │
│  • Outflow: Khách rời bỏ (Churn)                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Feedback Loops — Vòng Phản Hồi

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEEDBACK LOOPS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. REINFORCING LOOP (Vòng Tăng Cường / Snowball)               │
│  ═══════════════════════════════════════════════                │
│                                                                 │
│       ┌───────────────────┐                                     │
│       │   More Sales      │                                     │
│       └────────┬──────────┘                                     │
│                │                                                │
│                ▼                                                │
│       ┌────────┴──────────┐                                     │
│       │  More Revenue     │◄───┐                                │
│       └────────┬──────────┘    │                                │
│                │               │                                │
│                ▼               │                                │
│       ┌────────┴──────────┐    │                                │
│       │  More Marketing   │────┘                                │
│       │     Budget        │                                     │
│       └───────────────────┘                                     │
│                                                                 │
│  → Vòng lặp này có thể là TỐT (tăng trưởng) hoặc XẤU (nợ tech)  │
│                                                                 │
│  2. BALANCING LOOP (Vòng Cân Bằng / Thermostat)                 │
│  ═══════════════════════════════════════════════                │
│                                                                 │
│       ┌───────────────────┐                                     │
│       │  Room Too Hot     │                                     │
│       └────────┬──────────┘                                     │
│                │                                                │
│                ▼                                                │
│       ┌────────┴──────────┐                                     │
│       │  AC Turns On      │◄───┐                                │
│       └────────┬──────────┘    │                                │
│                │               │                                │
│                ▼               │                                │
│       ┌────────┴──────────┐    │                                │
│       │  Room Cools Down  │────┘ (Gap closes → AC off)          │
│       └───────────────────┘                                     │
│                                                                 │
│  → Vòng này giữ hệ thống ổn định quanh một mục tiêu             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Leverage Points — Điểm Đòn Bẩy

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEVERAGE POINTS                              │
│               (Sắp xếp từ YẾU đến MẠNH)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  12. Constants, Parameters (Số liệu, Hằng số) ← Yếu nhất       │
│  11. Buffer sizes (Kích thước Stock)                            │
│  10. Structure of Stocks & Flows                                │
│  9. Delays (Độ trễ phản hồi)                                    │
│  8. Strength of Balancing Loops                                 │
│  7. Strength of Reinforcing Loops                               │
│  6. Information Flows                                           │
│  5. Rules of the System (Policies)                              │
│  4. Power to change System Structure                            │
│  3. Goals of the System                                         │
│  2. Mindset or Paradigm                                         │
│  1. Power to Transcend Paradigms ← Mạnh nhất                   │
│                                                                 │
│  ÁP DỤNG CHO BA:                                                │
│  ═══════════════                                                │
│  • Thay đổi "số liệu" (12) là dễ nhất nhưng ít hiệu quả nhất   │
│  • Thay đổi "mục tiêu" (3) hoặc "quy tắc" (5) mạnh hơn nhiều   │
│  • Thay đổi "tư duy" (2) là transformation thực sự              │
│                                                                 │
│  VÍ DỤ:                                                         │
│  • Yếu: Tăng timeout từ 30s lên 60s (chữa triệu chứng)         │
│  • Mạnh: Refactor để async processing (thay đổi cấu trúc)      │
│  • Rất mạnh: Thay đổi KPI từ "# tickets closed" sang           │
│             "Customer Satisfaction" (thay đổi mục tiêu)        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5. Systems Archetypes — Các Mẫu Hệ Thống Phổ Biến

| Archetype | Mô tả | Giải pháp |
|-----------|-------|-----------|
| **Fixes that Fail** | Giải pháp ngắn hạn gây hậu quả dài hạn | Tìm root cause, chấp nhận delay |
| **Shifting the Burden** | Nghiện giải pháp tạm thời | Tăng cường giải pháp gốc |
| **Limits to Growth** | Tăng trưởng rồi đụng trần | Xác định và mở rộng giới hạn |
| **Tragedy of the Commons** | Ai cũng khai thác tài nguyên chung | Quy tắc/hạn ngạch |
| **Escalation** | Hai bên chạy đua | Thỏa thuận ngừng leo thang |

---

## ✅ CHECKLIST SYSTEMS THINKING

- [ ] Đã vẽ sơ đồ Stocks & Flows cho vấn đề?
- [ ] Đã xác định Reinforcing và Balancing Loops?
- [ ] Đã tìm Leverage Points (không chỉ chữa triệu chứng)?
- [ ] Đã kiểm tra xem giải pháp có gây hậu quả không mong muốn?
- [ ] Đã xem xét Delays trong hệ thống?

---

## 🔗 KỸ NĂNG LIÊN QUAN

| Để làm... | Tham khảo Skill |
|-----------|-----------------|
| Root Cause Analysis | @ba-root-cause |
| Strategy Analysis | EBOOK-01 (Fundamentals - BABOK Strategy) |
| Agile Iteration | EBOOK-04 (Agile) |
