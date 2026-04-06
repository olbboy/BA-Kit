<p align="center">
  <img src="assets/logo.png?v=2.7.0" alt="BA-Kit Logo" width="200">
</p>

<div align="center">

[**🇬🇧 English**](README.md) | [**🇻🇳 Tiếng Việt**](README.vi.md)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.7.0-blue?style=for-the-badge" alt="Version 2.7.0">
  <img src="https://img.shields.io/badge/Agents-19-green?style=for-the-badge" alt="19 Agents">
  <img src="https://img.shields.io/badge/Protocol-Antigravity%20Native-orange?style=for-the-badge" alt="Antigravity Native">
  <img src="https://img.shields.io/badge/Capability-CMMI%20Level%205%20Enabler-purple?style=for-the-badge" alt="CMMI Level 5 Enabler">
</p>

<h1 align="center">🏆 BA-Kit (Phiên Bản Antigravity)</h1>
<h3 align="center">Biệt Đội Chuyên Gia Phân Tích Nghiệp Vụ</h3>

<p align="center">
  <strong>21 Chuyên gia cho Phân tích Yêu cầu Nghiệp vụ</strong><br>
  Tư duy Hệ thống 2 • Đa Nền tảng (Antigravity • Claude Code • Claude CoWork)
</p>

---

## 🎯 BA-Kit là gì?

BA-Kit không chỉ là một kho prompt; đây là một **Biệt đội Agent** cho các **nền tảng agentic AI**.

Nó thay thế mô hình "Một Chatbot duy nhất" bằng **21 Chuyên gia** chạy trên:
*   **Antigravity IDE** (Google DeepMind) — Agent Skills, MCP, System 2
*   **Claude Code** (Anthropic) — CLI: project-level reasoning, CI/CD, Git
*   **Claude CoWork** (Anthropic) — Desktop: non-technical BA, document synthesis

Triệu hồi chuyên gia: `@ba-writing` cho specs, `@ba-strategy` cho chiến lược, `@ba-facilitation` cho workshop.

Mỗi chuyên gia sử dụng **Tư duy Hệ thống 2** (Vòng Lặp Phản Tư) — tự phê bình trước khi trả lời để giảm hallucination.

---

## 🤖 Biệt Đội Chuyên Gia (19 Personas)

### 🔴 Bộ Chỉ Huy
| Agent | Vai trò | Năng lực |
| :--- | :--- | :--- |
| **`@ba-master`** | **Tổng Chỉ Huy** | Lập Kế hoạch, Điều phối, Quản lý Ngữ cảnh. |

### 🔵 Khối Sáng Tạo (Nền Tảng)
| Agent | Vai trò | Năng lực |
| :--- | :--- | :--- |
| **`@ba-identity`** | Tham Mưu Trưởng | Ánh xạ Stakeholder, RACI, Bảng Năng lực. |
| **`@ba-elicitation`**| Nhà Báo | Kỹ thuật Phỏng vấn Phễu, "Colombo" Method. |
| **`@ba-writing`** | Kiến Trúc Sư | **Quét UI Thị giác**, Soạn Gherkin (BDD). |

### 🟡 Khối Kỹ Thuật (Chuyên Gia)
| Agent | Vai trò | Năng lực |
| :--- | :--- | :--- |
| **`@ba-validation`** | Trưởng QA | **QA Thị giác**, Phát hiện Edge Case. |
| **`@ba-traceability`**| Thư ký CCB| **Grep Xác minh** (Không Ảo giác). |
| **`@ba-nfr`** | Kiến Trúc SRE | Tiêu chuẩn ISO 25010 **Xác minh Web**. |
| **`@ba-process`** | Bậc Thầy Lean | **Thị giác Bảng trắng**, Phân tích Lãng phí BPMN. |
| **`@ba-prioritization`**| Product Mgr | Khung MoSCoW, RICE, WSJF. |
| **`@ba-solution`** | Nhà Đầu Tư | ROI & NPV **Xác minh Python**. |
| **`@ba-conflict`** | Nhà Ngoại Giao | Đàm phán Harvard, Soạn ADR. |
| **`@ba-export`** | Nhà Xuất Bản | Kiểm tra Compliance, Định dạng Pandoc. |

### 🟣 Khối Tiên Tri (Level 5 Enabler)
| Agent | Vai trò | Năng lực |
| :--- | :--- | :--- |
| **`@ba-metrics`** | Nhà Khoa học Dữ liệu| **Biểu đồ SPC**, Mật độ Lỗi, Cpk. |
| **`@ba-root-cause`**| Thám Tử | 5 Whys, Fishbone, Pareto. |
| **`@ba-innovation`**| Nhà Khoa học R&D | **A/B Testing**, Thiết kế Giả thuyết. |

### 🟢 Khối Chiến Lược & eBook (MỚI v2.7)
| Agent | Vai trò | Năng lực |
| :--- | :--- | :--- |
| **`@ba-strategy`** | Chiến Lược Gia | PESTLE, SWOT, Business Model Canvas. |
| **`@ba-facilitation`** | Điều Phối Viên | Thiết kế Workshop, ODEC Framework. |
| **`@ba-systems`** | Phân Tích Hệ Thống | Stocks & Flows, Điểm Đòn Bẩy. |
| **`@ba-agile`** | Phân Tích Agile | User Story Mapping, MVP, Hypothesis-Driven. |

---

## 🚀 Bắt Đầu Nhanh (Antigravity Native)

### 1. Cài Đặt
Sao chép workflows vào "bộ não" của Agent:
```bash
cp -r ba-kit/.agent/skills/* ~/.gemini/antigravity/skills/
```

### 2. Triệu Hồi
Trong khung chat, chỉ cần gõ `@` theo sau là Tên Agent:
> **User**: *"@ba-writing Tôi cần tính năng đăng nhập."*

> **@ba-writing**: *"Kiến Trúc Sư nhận lệnh. Anh muốn Login bằng Email/OTP hay Mạng xã hội? Để soạn Happy Path trước..."*

### 3. "Chế Độ Flash"
Bạn có thể chuyển đổi agent ngay lập tức để xử lý các tác vụ phức tạp:
> **User**: *"Yêu cầu này có vẻ rủi ro. @ba-solution kiểm tra ROI đi."*

> **@ba-solution**: *"Nhà Đầu Tư đây. Để tính NPV bằng Python..."*

---

## 🧠 Trí Tuệ Hệ Thống 2 (Mới trong v2.4+)

Tất cả các agent đều tuân theo **Vòng Lặp Nhận Thức Phản Tư**:
1.  **Phân tích (Hệ thống 1)**: Khớp mẫu nhanh.
2.  **Hành động (Hệ thống 1)**: Phác thảo nội dung.
3.  **Phản Tư (Hệ thống 2)**: **DỪNG & NGHĨ**.
    *   *Phê bình*: "Tôi có ảo giác dependency đó không?"
    *   *Hành động*: Xác minh bằng `grep` hoặc `python`.
4.  **Đầu ra**: Câu trả lời Đã Xác minh, Độ Chính xác Cao.

---

## 📒 Hồ Sơ Tác Chiến (Continuity Ledger)

**Mới trong v2.7.0**: Biệt đội chia sẻ một "Bộ nhớ Làm việc".

1.  Sao chép `templates/CONTINUITY.md` ra thư mục gốc.
2.  Điền Mục tiêu và Ràng buộc của bạn.
3.  **Kết quả**: Tất cả 19 chuyên gia đọc file này trước khi hành động!

---

## 📁 Cấu Trúc Repository

```
ba-kit/
│
├── .agent/skills/              # 🤖 Bộ não (19 Agent Skills)
├── ebooks/                     # 📚 eBook Knowledge Base (6 Skills)
├── docs/knowledge_base/        # 📖 Kho Tri thức
├── templates/                  # 🟢 Templates (BRD, SRS, User Stories)
├── docs/                       # 📘 Tài liệu Giao thức
│   └── ANTIGRAVITY_PROTOCOL.md #    Đặc tả Kỹ thuật
└── README.md                   # 📄 File này
```

---

## 📄 Giấy Phép

MIT License. Miễn phí sử dụng cho dự án cá nhân và doanh nghiệp.

---

<p align="center">
  <strong>Được xây dựng cho Kỷ nguyên Antigravity.</strong><br>
  <em>Code Ít Hơn. Tư Duy Nhiều Hơn.</em>
</p>
