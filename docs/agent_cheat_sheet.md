# 📋 BA-Kit Agent Cheat Sheet (v2.9.0)

> **Quick Reference Card: 21 Specialists at Your Fingertips**

---

## 🔴 THE COMMANDER
| Agent | Summon When | Example Prompt |
| :--- | :--- | :--- |
| **`@ba-master`** | You're lost | *"I have a problem, help me decide who to call."* |

---

## 🔵 THE CREATORS (Project Start)
| Agent | Summon When | Example Prompt |
| :--- | :--- | :--- |
| **`@ba-identity`** | New project | *"Who are the stakeholders? Map their power/interest."* |
| **`@ba-elicitation`**| Need requirements | *"Interview me about the Login feature."* |
| **`@ba-writing`** | Draft specs | *"Turn these notes into Gherkin User Stories."* |

---

## 🟡 THE ENGINEERS (Mid-Project)
| Agent | Summon When | Example Prompt |
| :--- | :--- | :--- |
| **`@ba-nfr`** | Define constraints | *"What are the ISO 25010 requirements for Payment?"* |
| **`@ba-process`** | Visualize flow | *"Draw the BPMN for the Checkout process."* |
| **`@ba-traceability`**| Track impact | *"What breaks if I change REQ-101?"* |
| **`@ba-conflict`** | Resolve fights | *"Sales vs Dev: Find a win-win."* |
| **`@ba-prioritization`**| Rank work | *"Apply WSJF to this feature list."* |
| **`@ba-solution`** | Check money | *"Calculate the 3-year ROI using Python."* |
| **`@ba-validation`** | QA check | *"Roast this spec. Find all the bugs."* |
| **`@ba-export`** | Publish | *"Export this to a DOCX for the client."* |

---

## 🟣 THE PRECOGS (Optimization)
| Agent | Summon When | Example Prompt |
| :--- | :--- | :--- |
| **`@ba-metrics`** | Audit quality | *"Is our defect rate stable? Show Control Chart."* |
| **`@ba-root-cause`** | Fix the system | *"Why do we keep having this bug? Use 5 Whys."* |
| **`@ba-innovation`**| Run experiments | *"Design an A/B test for Sign-Up conversion."* |

---

## 🟢 THE STRATEGISTS (eBook-Powered) — NEW in v2.7
| Agent | Summon When | Example Prompt |
| :--- | :--- | :--- |
| **`@ba-strategy`** | Need context | *"SWOT this market opportunity."* |
| **`@ba-facilitation`** | Run workshops | *"Plan a 2-hour requirements workshop."* |
| **`@ba-systems`** | Complex problems | *"Why does this keep happening? Map the loops."* |
| **`@ba-agile`** | Agile planning | *"Create a User Story Map for Checkout."* |

---

## 🔗 THE CONNECTORS (Integration) — NEW in v2.9
| Agent | Summon When | Example Prompt |
| :--- | :--- | :--- |
| **`@ba-jira`** | Publish to Jira | *"Create Jira tickets from these validated User Stories."* |
| **`@ba-confluence`** | Publish to wiki | *"Publish this BRD to Confluence space PROJ."* |

---

## ⚡ POWER COMBOS

| Scenario | Chain | Result |
| :--- | :--- | :--- |
| **Zero to MVP** | `elicitation` → `writing` → `prioritization` | Dev-Ready Backlog |
| **Stakeholder War** | `identity` → `conflict` → `solution` | Win-Win Agreement |
| **Production Crisis** | `root-cause` → `process` → `writing` | Permanent Fix Spec |
| **Compliance Audit** | `traceability` → `validation` → `export` | Auditor-Ready Proof |
| **Strategic Analysis** | `strategy` → `systems` → `elicitation` | Root Cause with Context |
| **Agile Kickoff** | `agile` → `facilitation` → `writing` | Sprint-Ready Backlog |
| **Workshop Success** | `facilitation` → `elicitation` → `prioritization` | Consensus Decisions |
| **Jira Pipeline** | `writing` → `validation` → `jira` | Dev-Ready Tickets |
| **Confluence Publish** | `writing` → `export` → `confluence` | Wiki Documentation |
| **Full Pipeline** | `writing` → `validation` → `jira` + `confluence` | Tickets + Docs |
| **PRD Pipeline** | `elicitation` → `writing` (PRD) → `prioritization` → `nfr` → `validation` | Validated PRD |
| **Stitch UI** | `writing` (specs) → Stitch MCP (screen) → `validation` (review) | Spec-Driven UI |

---

## 🧠 KEY PROTOCOLS

1.  **Context Injection**: Copy `templates/continuity_template.md` to root as `CONTINUITY.md`. Fill in Goal/Constraints.
2.  **Visual Input**: Drag & Drop images directly. Use `@[image] @ba-writing ...`
3.  **Math Verification**: Agents use Python. **Never stop them**.
4.  **Link Verification**: Agents use Grep. **Never stop them**.

---

*Print this page. Pin it next to your monitor.*

---

## Junior BA Learning Path

> Mới vào nghề? Đi theo lộ trình này. Từng bước, từng tuần.

### Level 1: Foundation (Tuần 1)

| Agent | Bạn sẽ học được gì | Bài tập thực hành |
|-------|-------------------|-------------------|
| `@ba-elicitation` | Cách đặt câu hỏi đúng để khai thác yêu cầu thật sự | Phỏng vấn một đồng nghiệp về quy trình làm việc hàng ngày của họ |
| `@ba-writing` | Cách viết requirements rõ ràng, không mơ hồ | Chuyển notes từ 1 buổi họp thành 3 User Stories hoàn chỉnh |
| `@ba-validation` | Cách phát hiện lỗi specs trước khi dev nhìn thấy | Tự review lại User Stories vừa viết theo tiêu chí INVEST |

### Level 2: Expansion (Tuần 2-3)

| Agent | Bạn sẽ học được gì | Bài tập thực hành |
|-------|-------------------|-------------------|
| `@ba-prioritization` | Cách sắp xếp feature theo giá trị và chi phí | Áp dụng MoSCoW cho product backlog hiện tại của dự án |
| `@ba-process` | Cách vẽ quy trình nghiệp vụ để mọi người cùng hiểu | Vẽ sơ đồ As-Is cho một business flow trong dự án |
| `@ba-nfr` | Cách định nghĩa quality attributes (performance, security...) | Viết 5 NFR cho dự án hiện tại theo ISO 25010 |

### Level 3: Strategy (Tháng 2+)

| Agent | Bạn sẽ học được gì | Bài tập thực hành |
|-------|-------------------|-------------------|
| `@ba-strategy` | Cách phân tích bức tranh business toàn cảnh | Chạy SWOT analysis cho sản phẩm đang làm |
| `@ba-conflict` | Cách đàm phán khi stakeholder bất đồng | Luyện tập Interest vs Position mapping với 2 stakeholder giả định |
| `@ba-solution` | Cách tính business value và thuyết phục bằng số | Tính ROI cho một tính năng đang được đề xuất trong dự án |

> **Quick start ngay bây giờ:** Xem `docs/JUNIOR-START.md` — hướng dẫn từng ngày cho tuần đầu tiên.
