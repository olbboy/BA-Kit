<p align="center">
  <img src="docs/assets/logo.png?v=3.4.0" alt="BA-Kit Logo" width="200">
</p>

<div align="center">

[**🇬🇧 English**](README.md) | [**🇻🇳 Tiếng Việt**](README.vi.md)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.4.0-blue?style=for-the-badge" alt="Version 3.4.0">
  <img src="https://img.shields.io/badge/Agents-43-green?style=for-the-badge" alt="43 Agents">
  <img src="https://img.shields.io/badge/Platforms-Antigravity%20%7C%20Claude%20Code%20%7C%20CoWork-orange?style=for-the-badge" alt="3 Platforms">
  <img src="https://img.shields.io/badge/Capability-CMMI%20Level%205%20Enabler-purple?style=for-the-badge" alt="CMMI Level 5 Enabler">
</p>

<p align="center">
  <a href="https://github.com/olbboy/BA-Kit/actions/workflows/e2e-skills.yml">
    <img src="https://github.com/olbboy/BA-Kit/actions/workflows/e2e-skills.yml/badge.svg?branch=feat/mini-app-cham-cong-docs" alt="E2E Skills Test">
  </a>
</p>

<h1 align="center">BA-Kit</h1>
<h3 align="center">Biệt Đội Chuyên Gia Phân Tích Nghiệp Vụ</h3>

<p align="center">
  <strong>43 Chuyên gia cho Phân tích Yêu cầu Nghiệp vụ</strong><br>
  Tư duy Hệ thống 2 • Đa Nền tảng (Antigravity • Claude Code • Claude CoWork)
</p>

---

## 🎯 BA-Kit là gì?

BA-Kit không chỉ là một kho prompt; đây là một **Biệt đội Agent** cho các **nền tảng agentic AI**.

Nó thay thế mô hình "Một Chatbot duy nhất" bằng **43 Chuyên gia** chạy trên:
*   **Antigravity IDE** (Google DeepMind) — Agent Skills, MCP, System 2
*   **Claude Code** (Anthropic) — CLI: project-level reasoning, CI/CD, Git
*   **Claude CoWork** (Anthropic) — Desktop: non-technical BA, document synthesis

Triệu hồi chuyên gia: `@ba-writing` cho specs, `@ba-strategy` cho chiến lược, `@ba-facilitation` cho workshop.

Mỗi chuyên gia sử dụng **Tư duy Hệ thống 2** (Vòng Lặp Phản Tư) — tự phê bình trước khi trả lời để giảm hallucination.

---

## 🤖 Biệt Đội Chuyên Gia (43 Agents + 2 Connectors)

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

### 🟠 Khối Chất Lượng & Kiểm Toán (MỚI v3.0)
| Agent | Vai trò | Năng lực |
| :--- | :--- | :--- |
| **`@ba-test-gen`** | Kiến Trúc Sư QA | AC → Test Cases 7 loại (BVA, Decision Tables, State Transitions). |
| **`@ba-quality-gate`** | Giám Đốc Chất Lượng | Chấm điểm 5 cổng: PASS / CONDITIONAL / REJECT. |
| **`@ba-consistency`** | Kiểm Toán Viên | Kiểm tra đồng bộ US↔API↔DB↔BRD. |
| **`@ba-auditor`** | Tổng Kiểm Toán | Meta-agent: dashboard sức khỏe dự án + kế hoạch hành động. |

### 🔵 Lifecycle Agents (MỚI trong v3.1)
| Agent | Vai trò | Khả năng |
| :--- | :--- | :--- |
| **`@ba-questioning`** | Chuyên gia hỏi | Câu hỏi Context-Free, chuẩn bị phỏng vấn, phát hiện giả định. |
| **`@ba-communication`** | Truyền thông | Báo cáo trạng thái, tóm tắt điều hành, biên bản họp. |
| **`@ba-ux`** | Nghiên cứu UX | Persona, Journey Map, Empathy Map, JTBD, kiểm thử khả dụng. |
| **`@ba-data`** | Kiến trúc dữ liệu | ERD, Data Dictionary, DFD, Data Mapping, Migration. |
| **`@ba-change`** | Quản lý thay đổi | ADKAR, đánh giá sẵn sàng, kế hoạch đào tạo, Go-Live. |
| **`@ba-business-rules`** | Quản lý quy tắc | Decision Table, Decision Tree, Rule Catalog, phát hiện xung đột. |
| **`@ba-diagram`** | Visualizer | Mermaid v11 (24+ loại diagram), BA artifact→diagram, Confluence export. |

### 📘 Knowledge Agent (MỚI trong v3.0)
| Agent | Vai trò | Khả năng |
| :--- | :--- | :--- |
| **`@ba-wiki`** | Quản lý tri thức | Nạp kiến thức 2 tầng, truy vấn wiki, tài liệu sống, **quản lý glossary**. |

### 🌀 Sprint Spine Agents (MỚI trong v3.4 — Gstack Distillation)
| Agent | Phase | Khả năng |
| :--- | :--- | :--- |
| **`@ba-as-built`** | Reflect | **Phát hiện lệch spec** — so sánh BRD/SRS/RTM với delivery evidence (UAT reports, release notes, demo notes) để tìm chỗ "thực tế ≠ spec". |
| **`@ba-autoreview`** | Validate | Meta tuần tự nghiêm ngặt: `consistency → quality-gate → traceability → auditor`, tùy chọn `--dual-voice`. |
| **`@ba-retro`** | Reflect | Sprint retro: gate pass rate, churn, stakeholder responsiveness — đọc từ BA-Kit metric streams (không cần git). |
| **`@ba-learn`** | Reflect | Bộ nhớ JSONL theo project (5 loại, lọc PII, API auto-capture). |
| **`@ba-checkpoint`** | any | Lưu/tiếp tục session cho BA workflow dài (workshop nhiều ngày). |
| **`@ba-challenger`** | Validate | Red team 5 vector (unstated / incentive / adversarial / scale-break / sunset). |
| **`@ba-second-opinion`** | Validate | Review từ model khác — Gemini / OpenAI / Ollama / manual (zero-dep `urllib`). |
| **`@ba-baseline`** | Publish | CCB baseline với version + signer + date + rationale. Agent hỏi BA bằng natural language; integrity check chạy ngầm. |
| **`@ba-guard`** | any | Cảnh báo change-control bằng BA language: "BRD-HR đã edit 2 ngày sau sign-off — có re-approve không?" 3 modes (off / warn / strict). |
| **`@ba-shotgun`** | Define | Sinh N variant cho stories / AC / priority / emails (capture preference vào `@ba-learn`). |

> 📐 **Sprint Spine** — toàn bộ 43 agents map vào vòng lặp 7 phase: **Discover → Elicit → Define → Validate → Prioritize → Publish → Reflect**. Xem [`docs/sprint-spine.md`](docs/sprint-spine.md) để biết chi tiết mapping agent → phase.

---

## 🚀 Bắt Đầu Nhanh

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

1.  Sao chép `.agent/templates/continuity-template.md` ra thư mục gốc.
2.  Điền Mục tiêu và Ràng buộc của bạn.
3.  **Kết quả**: Tất cả 26 chuyên gia đọc file này trước khi hành động!

---

## 📁 Cấu Trúc Repository

```
ba-kit/
│
├── .agent/skills/                # 43 Agent Skills + 2 Connectors
├── .agent/scripts/               # BM25+ Knowledge Search Engine
├── .agent/data/                  # 831 Indexed Knowledge Entries (23 domains)
│
├── docs/                         # Tài liệu & Hướng dẫn
│   ├── README.md                 # Mục lục tài liệu
│   ├── agent-cheat-sheet.md      # 43 agents tổng quan
│   ├── prompt-library.md         # 48 prompt theo workflow phase
│   ├── design-prototype-guide.md # Stitch MCP, Figma, vibe coding
│   ├── ai-foundation-for-ba.md   # Nền tảng AI cho BA
│   └── knowledge_base/           # Kho tri thức BA
│
├── .agent/templates/             # 14 Templates (PRD, BRD, SRS, FRD, Test Case, ...)
├── .agent/scripts/               # Scripts tự động (RTM scanner, export, search)
│
└── README.md                     # File này
```

---

## 🔍 Công Cụ Tìm Kiếm Tri Thức (BM25+)

BA-Kit tích hợp **BM25+ Knowledge Search Engine** với **831 entries** trên **23 domains**.

```bash
# Tìm kiếm bất kỳ khái niệm BA
python3 .agent/scripts/ba_search.py "acceptance criteria gherkin"

# Tìm trong domain cụ thể
python3 .agent/scripts/ba_search.py "GDPR compliance" --domain compliance

# Tìm trên tất cả domains
python3 .agent/scripts/ba_search.py "stakeholder analysis" --multi-domain
```

---

## 📄 Giấy Phép

MIT License. Miễn phí sử dụng cho dự án cá nhân và doanh nghiệp.

---

<p align="center">
  <strong>Antigravity • Claude Code • Claude CoWork</strong><br>
  <em>Code Ít Hơn. Tư Duy Nhiều Hơn.</em>
</p>
