# AI Foundation Cho Business Analyst / AI Foundation for Business Analysts

> Hiểu trước, dùng sau. Understand first, use after.
> *— ITBA: "Hiểu → sau đó không cần prompt mẫu nữa → bạn tự làm"*

---

## Phần 1: AI Là Gì? / Part 1: What is AI?

### 1.1 Large Language Model (LLM) — Cỗ Máy Đoán Từ / The Word Prediction Engine

**🇻🇳 Tiếng Việt:**
LLM (Large Language Model) là một chương trình máy tính được huấn luyện trên hàng tỷ trang văn bản. Nó hoạt động bằng cách **dự đoán từ tiếp theo** dựa trên các từ trước đó.

Ví dụ: bạn gõ "Tôi muốn đặt..." trên điện thoại, bàn phím gợi ý "vé máy bay". LLM tương tự nhưng ở quy mô lớn hơn — viết bài, phân tích dữ liệu, tạo code.

**🇬🇧 English:**
An LLM (Large Language Model) is a program trained on billions of pages of text. It works by **predicting the next word** based on previous words — same as your phone keyboard suggesting the next word, but at scale.

**⚠️ Điều quan trọng / Key Point:**
- AI **không "hiểu"** như con người — nó nhận diện patterns / AI doesn't "understand" — it recognizes patterns
- AI **có thể sai** (Hallucination) — tự tin nói điều không đúng / AI can be confidently wrong
- BA-Kit xử lý vấn đề này bằng **System 2 Reflection** — agents tự kiểm tra trước khi trả lời

---

### 1.2 Tokens — Đơn Vị Đo Lường Của AI / The Unit of AI Measurement

**🇻🇳 Tiếng Việt:**
Token là đơn vị nhỏ nhất mà AI xử lý. Một token không nhất thiết là một từ — nó có thể là một phần của từ, một ký tự, hoặc một dấu câu.

**Quy tắc nhanh:**
- Tiếng Anh: 1 token ≈ 0.75 từ (4 ký tự)
- Tiếng Việt: 1 token ≈ 0.5 từ (do dấu và Unicode)
- 1 trang A4 ≈ 500-600 tokens

**🇬🇧 English:**
A token is the smallest unit AI processes. A token isn't necessarily a word — it can be part of a word, a character, or punctuation.

**Quick rules:**
- English: 1 token ≈ 0.75 words (4 characters)
- Vietnamese: 1 token ≈ 0.5 words (due to diacritics and Unicode)
- 1 A4 page ≈ 500-600 tokens

**Tại sao BA cần quan tâm / Why BAs should care:**

| Tài liệu / Document | Kích thước / Size | Tokens (ước tính / estimate) |
|---|---|---|
| 1 User Story | ~200 từ | ~300 tokens |
| BRD (10 trang) | ~5,000 từ | ~7,500 tokens |
| SRS (50 trang) | ~25,000 từ | ~37,500 tokens |
| Toàn bộ project specs | ~100 trang | ~75,000 tokens |

---

### 1.3 Context Window — Bộ Nhớ Ngắn Hạn / Short-Term Memory

**🇻🇳 Tiếng Việt:**
Context Window là "bộ nhớ RAM" của AI trong một cuộc trò chuyện. Nó quy định **AI nhớ được bao nhiêu nội dung** cùng lúc.

| Model | Context Window | Tương đương / Equivalent |
|---|---|---|
| GPT-4o | 128K tokens | ~200 trang A4 |
| Claude 3.5 Sonnet | 200K tokens | ~320 trang A4 |
| Gemini 2.0 | 1M tokens | ~1,600 trang A4 |

**Khi context "tràn"**: AI bắt đầu **quên** phần đầu cuộc trò chuyện. Nếu bạn thấy AI "quên" điều bạn nói cách đây 20 tin nhắn — đây là lý do.

**🇬🇧 English:**
The Context Window is AI's "RAM" during a conversation. It determines **how much content AI can remember** at once.

When the context "overflows", AI starts **forgetting** the beginning of the conversation.

**Liên kết BA-Kit / BA-Kit Connection:**
- `CONTINUITY.md` = persistent context ledger — giúp agents nhớ qua nhiều phiên / helps agents remember across sessions
- Knowledge Engine (BM25+) = chỉ load kiến thức liên quan, tiết kiệm 97% tokens / loads only relevant knowledge, saves 97% tokens

---

### 1.4 Ba Nền Tảng Chính Của BA-Kit / The Three Primary Platforms

BA-Kit chạy trên **3 nền tảng agentic**. Mỗi nền tảng có thế mạnh riêng:

**🇻🇳 Tiếng Việt:**

```
┌─────────────────────────────────────────────────────────────┐
│                     BA-Kit (26 Agents)                       │
│         Chạy trên / Runs on:                                │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Antigravity  │  │ Claude Code │  │   Claude CoWork     │ │
│  │ (Google      │  │ (Anthropic) │  │   (Anthropic)       │ │
│  │  DeepMind)   │  │             │  │                     │ │
│  │              │  │             │  │                     │ │
│  │ ★ Primary    │  │ ★ Developer │  │ ★ Knowledge Worker  │ │
│  │   IDE        │  │   CLI       │  │   Desktop App       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

#### 1.4.1 Antigravity (Google DeepMind) — Nền Tảng Chính / Primary Platform

**🇻🇳:** Antigravity là **AI Coding IDE** — môi trường phát triển tích hợp cho AI agents. Đây là nền tảng **ban đầu** mà BA-Kit được xây dựng, với hỗ trợ native sâu nhất.

**🇬🇧:** Antigravity is an AI Coding IDE — the **original** platform BA-Kit was built for, with the deepest native support.

**Tại sao Antigravity quan trọng / Why it matters:**
1. **Agent Skills Framework**: Tạo và gọi agents qua cú pháp `@` (`@ba-writing`). Mỗi skill = 1 file SKILL.md tự chứa. / Create and invoke agents via `@` syntax. Each skill = 1 self-contained SKILL.md.
2. **Tool Mandates**: Agents **bắt buộc** dùng Python (math), Grep (search), Web (standards) — không đoán mò. / Agents **must** use Python, Grep, Web Search — no guessing.
3. **MCP Protocol Native**: Kết nối Jira, Confluence, Perplexity, và bất kỳ MCP server nào. / Connect Jira, Confluence, Perplexity, any MCP server.
4. **System 2 Reflection**: Agents tự phê bình output trước khi trả lời. / Agents self-critique before responding.
5. **Knowledge Engine**: BM25+ search qua 786 entries, tiết kiệm 97% tokens. / BM25+ search across 786 entries, 97% token savings.
6. **File System Access**: Đọc/ghi file trực tiếp. / Direct file read/write.
7. **Local-First Security**: Chạy trên máy, không upload cloud. / Runs locally, no cloud upload.

**Khi nào dùng Antigravity / When to use:** Khi cần nhiều agents phối hợp, System 2 reflection, tool mandates, MCP integration.

---

#### 1.4.2 Claude Code (Anthropic) — Agentic Developer CLI

**🇻🇳:** Claude Code là **công cụ coding agentic** chạy qua terminal/CLI, phát triển bởi Anthropic. Nó hoạt động ở **project level** — đọc cả codebase, lập kế hoạch, thực thi, và lặp lại cho đến khi hoàn thành.

**🇬🇧:** Claude Code is an **agentic coding tool** running in terminal/CLI, developed by Anthropic. It operates at **project level** — reads entire codebases, plans multi-step approaches, executes, and iterates until tasks are complete.

**Tại sao Claude Code quan trọng / Why it matters:**
1. **Agentic Loop**: Hành động hướng mục tiêu, đánh giá kết quả, tự sửa lỗi. / Acts toward goals, evaluates results, self-corrects.
2. **Project-Level Understanding**: Đọc toàn bộ codebase, hiểu dependencies, trace qua modules. / Reads entire codebase, understands dependencies, traces across modules.
3. **CLAUDE.md Configuration**: Tương tự AGENT.MD/SKILL.md — file cấu hình instructions cho project. / Similar to AGENT.MD/SKILL.md — project-level instruction files.
4. **Auto Mode**: Tự động thực thi tasks an toàn mà không cần confirm từng bước. / Auto-execute safe tasks without step-by-step confirmation.
5. **Multi-Agent Coordination**: Dispatch nhiều agents làm việc song song trên các aspects khác nhau. / Dispatch multiple agents working in parallel.
6. **Git Workflow Native**: Branch, commit, PR tự động. / Automated branching, committing, PRs.
7. **Headless/CI Operation**: Chạy trên server, trigger qua API — phù hợp automation pipeline. / Run on servers, trigger via API — ideal for automation.

**Khi nào dùng Claude Code / When to use:** Khi bạn là **BA có kỹ năng technical** — cần đọc code, review architecture, tạo specs từ codebase, hoặc tích hợp BA workflow vào CI/CD pipeline. Phù hợp cho scenarios: reverse engineering specs từ code, code review, automated validation.

**BA-Kit trên Claude Code / BA-Kit on Claude Code:**
- BA-Kit skills load qua `CLAUDE.md` thay vì `AGENT.MD`
- Tool mandates tương thích (Python, shell, file access)
- Agentic loop = tương đương System 2 reflection
- Phù hợp cho: `@ba-validation` (code review), `@ba-traceability` (grep), `@ba-nfr` (standards check)

---

#### 1.4.3 Claude CoWork (Anthropic) — Desktop App Cho Knowledge Workers

**🇻🇳:** Claude CoWork là **ứng dụng desktop agentic** cho knowledge workers (không cần kỹ năng kỹ thuật). Ra mắt tháng 1/2026, nó cho phép delegate các công việc phức tạp, nhiều bước cho AI trên chính máy tính của bạn.

**🇬🇧:** Claude CoWork is an **agentic desktop application** for knowledge workers (no technical skills needed). Launched January 2026, it lets you delegate complex, multi-step work to AI on your own computer.

**Tại sao Claude CoWork quan trọng / Why it matters:**
1. **Desktop-Native**: Ứng dụng desktop macOS, truy cập sandboxed vào files/folders local. / macOS desktop app with sandboxed local file access.
2. **"Vibe Working"**: Nói mục tiêu → AI tự làm (tương tự "vibe coding" nhưng cho non-technical work). / State goals → AI handles execution.
3. **Multi-Step Workflows**: Tự động plan, execute, iterate trên nhiều bước — đọc nhiều tài liệu, tổng hợp, tạo output. / Auto plan, execute, iterate across steps — read multiple docs, synthesize, create outputs.
4. **Plugin System**: Mở rộng bằng plugins — kết nối CRM, databases, external apps. / Extend with plugins — connect CRM, databases, external apps.
5. **Slash Commands**: Custom automation triggers (`/analyze-brd`, `/create-stories`). / Custom automation triggers.
6. **Non-Technical Friendly**: Không cần biết CLI, code, hay terminal. Giao diện visual. / No CLI, code, or terminal knowledge needed. Visual interface.

**Khi nào dùng Claude CoWork / When to use:** Khi bạn là **BA truyền thống** (non-technical) — cần tổ chức tài liệu, tổng hợp meeting notes, tạo BRD/SRS từ nhiều nguồn, hoặc delegate công việc lặp lại (data extraction, file organization).

**BA-Kit trên Claude CoWork / BA-Kit on Claude CoWork:**
- BA-Kit skills load qua system instructions hoặc plugins
- File access = đọc specs, templates, knowledge base trên máy tính
- Slash commands = tạo shortcuts cho BA workflows (`/write-stories`, `/validate-spec`)
- Phù hợp cho: document synthesis, meeting notes → specs, stakeholder communication

---

#### So Sánh 3 Nền Tảng / Three-Platform Comparison

| Tính năng / Feature | Antigravity | Claude Code | Claude CoWork |
|---|---|---|---|
| **Nhà phát triển / Developer** | Google DeepMind | Anthropic | Anthropic |
| **Giao diện / Interface** | IDE (Desktop) | CLI (Terminal) | Desktop App |
| **Target User** | Developers + Technical BAs | Developers + DevOps | Knowledge Workers + BAs |
| **Agent Skills** (`@agent`) | ✅ Native | Via CLAUDE.md | Via Plugins/Instructions |
| **System 2 Reflection** | ✅ Native | ✅ Agentic Loop | Partial |
| **Tool Mandates** (Python/Grep) | ✅ Native | ✅ Full shell access | Sandboxed |
| **MCP Protocol** | ✅ Native | Partial | Via Plugins |
| **File System Access** | ✅ Full | ✅ Full | ✅ Sandboxed |
| **Multi-agent** | ✅ Skills | ✅ Multi-agent dispatch | Single agent + plugins |
| **Git Integration** | ✅ | ✅ Native (branch/commit/PR) | ❌ |
| **Headless/CI** | ✅ | ✅ Native | ❌ |
| **Non-technical friendly** | ⚠️ Medium | ❌ (CLI required) | ✅ High |
| **Local-first security** | ✅ | ✅ | ✅ |
| **BA-Kit Experience** | ★★★★★ Full | ★★★★ Strong | ★★★ Good |

**Khuyến nghị / Recommendation:**

| Bạn là ai / Who you are | Nền tảng chính / Primary Platform | Nền tảng phụ / Secondary |
|---|---|---|
| **Technical BA** (biết code, CLI) | **Antigravity** (full experience) | Claude Code (CI/CD automation) |
| **Traditional BA** (non-technical) | **Claude CoWork** (dễ dùng nhất) | Antigravity (khi cần full power) |
| **BA + DevOps** | **Claude Code** (pipeline automation) | Antigravity (squad orchestration) |
| **BA Team Lead** | **Antigravity** (orchestration) | Claude CoWork (delegate cho team) |

**Tóm lại:** Antigravity cho full orchestration. Claude Code cho CI/CD automation và project-level reasoning. Claude CoWork cho non-technical BAs. Chọn theo vai trò.

*Antigravity for full orchestration. Claude Code for CI/CD automation. Claude CoWork for non-technical BAs. Pick by role.*

---

## Phần 2: AI Agent — Tại Sao "Biệt Đội"? / Part 2: AI Agents — Why a "Squad"?

### 2.1 Single Chatbot vs Multi-Agent

**🇻🇳 Tiếng Việt:**

| | Single Chatbot | Multi-Agent (BA-Kit) |
|---|---|---|
| **Ví dụ** | Hỏi ChatGPT "viết BRD" | `@ba-strategy` → `@ba-elicitation` → `@ba-writing` |
| **Chuyên môn** | Jack of all trades | Mỗi agent = 1 chuyên gia |
| **Kiểm tra lỗi** | Không tự kiểm tra | System 2: tự phê bình trước khi trả lời |
| **Công cụ** | Chỉ dùng ngôn ngữ | Dùng Python (Math), Grep (Search), Web (Standards) |
| **Cộng tác** | 1 cuộc hội thoại | Agents chuyển giao cho nhau (Handoff Protocol) |
| **Nhớ** | Quên khi đổi topic | CONTINUITY.md = shared brain |

**🇬🇧 English:**

BA-Kit dùng 26 agents chuyên biệt, mỗi agent giỏi 1 lĩnh vực, phối hợp qua handoff protocol. / BA-Kit uses 21 specialized agents, each expert in one area, collaborating through a structured handoff protocol.

### 2.2 Cấu Trúc AI Agent / AI Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Platform: Antigravity / Claude Code / Claude CoWork       │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              BA-Kit Agent (1 of 21)                   │  │
│  │                                                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────────┐ │  │
│  │  │   LLM    │  │  Tools   │  │   Memory         │ │  │
│  │  │ (Brain)  │  │ (Hands)  │  │  (Notes)         │ │  │
│  │  └──────────┘  └──────────┘  └────────────────┘ │  │
│  │       ↑              ↑              ↑              │  │
│  │  Instructions   Python/Grep    CONTINUITY.md     │  │
│  │  SKILL.md or    Web Search     Knowledge Base    │  │
│  │  CLAUDE.md                                       │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──── MCP / Plugins ───┐ ┌──── File System ────┐    │
│  │ Perplexity │ Jira      │ │ Templates │ Specs   │    │
│  │ Confluence │ Others    │ │ Exports   │ Data    │    │
│  └───────────────────────┘ └──────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

- **Platform** = Nền tảng runtime (Antigravity/Claude Code/Claude CoWork) / Runtime platform
- **LLM** = Não bộ — suy luận, phân tích, viết / Brain — reasoning, analysis, writing
- **Tools** = Tay — thực thi (Python tính ROI, Grep tìm file) / Hands — execute (Python for ROI, Grep for search)
- **Memory** = Sổ tay — nhớ context dự án / Notebook — remembers project context
- **Instructions** = Kỹ năng huấn luyện / Trained skills (SKILL.md on Antigravity, CLAUDE.md on Claude Code, Plugins on CoWork)
- **MCP / Plugins** = Cổng kết nối — Jira, Confluence, Perplexity / Connection ports — external tools
- **File System** = Kho tài liệu — templates, specs, exports / Document storage

---

## Phần 3: Concepts Quan Trọng / Part 3: Key Concepts

### 3.1 RAG (Retrieval-Augmented Generation) — Tìm Trước, Trả Lời Sau

**🇻🇳 Tiếng Việt:**
RAG = AI **tìm kiếm kiến thức** từ nguồn đáng tin cậy TRƯỚC KHI trả lời, thay vì chỉ dựa vào training data.

**Tại sao quan trọng cho BA:**
- Không dùng RAG: AI đoán mò requirements template → có thể sai
- Dùng RAG: AI tìm trong knowledge base → trả lời chính xác theo BABOK/IEEE standards

**BA-Kit sử dụng RAG:**
```bash
python3 .agent/scripts/ba_search.py "acceptance criteria gherkin" --domain writing
# → Trả về 5 entries chính xác từ 786 knowledge entries
```

**🇬🇧 English:**
RAG = AI **searches knowledge** from trusted sources BEFORE answering, instead of relying solely on training data.

### 3.2 MCP (Model Context Protocol) — Cách AI Kết Nối Công Cụ

**🇻🇳 Tiếng Việt:**
MCP là giao thức chuẩn giúp AI **kết nối với tool bên ngoài** (Jira, Confluence, Perplexity, databases...) an toàn. Tương tự ổ cắm USB — bất kỳ tool nào hỗ trợ MCP đều "cắm" được vào AI.

**BA-Kit sử dụng MCP:**
- MCP Bridge → Perplexity (web search for `@ba-nfr` to verify ISO standards)
- Jira Connector → Jira Data Center (for `@ba-jira`)
- Confluence Connector → Confluence Data Center (for `@ba-confluence`)

MCP is a standard protocol that lets AI **connect to external tools** (Jira, Confluence, Perplexity, databases...) safely. Like a USB port — any MCP-compatible tool can plug in.

**MCP trên từng nền tảng / MCP on each platform:**

| Nền tảng / Platform | MCP Support | Ghi chú / Notes |
|---|---|---|
| **Antigravity** | ✅ Native | Cấu hình qua `mcp_config.json`, hỗ trợ đầy đủ nhất / Full support |
| **Claude Code** | ✅ Partial | Hỗ trợ qua shell commands và API calls / Via shell + API |
| **Claude CoWork** | Via Plugins | Mở rộng bằng plugin system / Extend via plugins |
| ChatGPT | ❌ | Không hỗ trợ / Not supported |
| Cursor | Partial | Hỗ trợ hạn chế / Limited support |

### 3.3 Fine-tuning vs Prompting vs RAG — Khi Nào Dùng Gì?

| Phương pháp / Method | Khi nào dùng / When to use | Chi phí / Cost | BA cần không? / BA needs? |
|---|---|---|---|
| **Prompting** | Hướng dẫn AI qua text | Miễn phí / Free | ✅ Hàng ngày / Daily |
| **RAG** | AI cần tra cứu knowledge base | Thấp / Low | ✅ BA-Kit tự động / BA-Kit auto |
| **Fine-tuning** | Cần AI chuyên biệt cho domain | Rất cao / Very high | ❌ Không cần cho BA / Not needed |

BA chỉ cần **Prompting + RAG**. BA-Kit tích hợp cả hai. / BAs only need Prompting + RAG. BA-Kit integrates both.

---

## Phần 4: Context Management / Part 4: Context Management

### 4.1 Tại Sao Context Là Vua / Why Context is King

**🇻🇳 Tiếng Việt:**

**Cùng 1 yêu cầu, khác context = kết quả hoàn toàn khác:**

| Prompt | Không có Context | Có Context |
|---|---|---|
| "Viết User Story cho Login" | Generic: Email/password, any app | Cụ thể: Mobile Banking, farmer 45-60 tuổi, Android giá rẻ, hỗ trợ SMS OTP vì vùng sâu |

Context bao gồm:
- **Ai** là user? (Persona) — Nông dân hay CEO?
- **Ở đâu** dùng? (Platform) — Mobile hay Desktop?
- **Tại sao** cần? (Business Goal) — Tiết kiệm chi phí hay tăng doanh thu?
- **Ràng buộc** gì? (Constraints) — Budget, timeline, technology stack

**🇬🇧 English:**
Same request, different context = completely different results. Context includes: WHO (persona), WHERE (platform), WHY (business goal), CONSTRAINTS (budget, timeline, tech).

### 4.2 Kỹ Thuật Quản Lý Context / Context Management Techniques

**1. CONTINUITY.md — Shared Brain (BA-Kit)**
```markdown
# Project: Mobile Banking for Farmers
## Goal: Increase financial inclusion in rural Vietnam
## Constraints: Android 8+, 3G network, Vietnamese only
## User Persona: Farmer, 45-60 years old, limited tech literacy
## Phase: MVP (Sprint 1-3)
```
→ Tất cả 26 agents đọc file này trước khi hành động / All 26 agents read this before acting.

**2. Chunking — Chia Nhỏ Tài Liệu / Break Documents into Pieces**
- SRS 50 trang? → Chia thành từng module (Login, Payment, Notification)
- Gửi AI từng phần, kèm context tổng quan

**3. Context Injection — Tiêm Bối Cảnh / Inject Background**
- Luôn bắt đầu bằng background info trước khi ra yêu cầu
- "Dự án của chúng tôi là... Target user là... Hiện đang sprint 3..."

### 4.3 Khi Nào Context Bị Mất / When Context Gets Lost

| Tình huống / Scenario | Nguyên nhân / Cause | Giải pháp / Solution |
|---|---|---|
| Cuộc trò chuyện mới | Context window reset | Gửi lại CONTINUITY.md |
| Trò chuyện quá dài | Context overflow | Tóm tắt trước khi tiếp tục |
| Đổi topic | AI confused | Tách thành conversation riêng |
| Đổi agent | Agent mới không biết context cũ | BA-Kit: Handoff Protocol chuyển context |

---

## Phần 5: Prompt Thinking / Part 5: Prompt Thinking

### 5.1 Triết Lý: Hiểu Rồi Thì Tự Viết / Philosophy: Understanding > Templates

**🇻🇳 Tiếng Việt:**
Prompt template giống như bánh xe tập — hữu ích lúc đầu, nhưng mục tiêu là **tự đạp xe không cần bánh phụ**.

Khi bạn hiểu **cấu trúc** của một prompt tốt, bạn có thể viết prompt cho BẤT KỲ tình huống nào — không phụ thuộc vào template.

**🇬🇧 English:**
Prompt templates are like training wheels — useful at first, but the goal is to ride without them.

### 5.2 Giải Phẫu Prompt Tốt / Anatomy of a Good Prompt

```
┌────────────────────────────────────────────┐
│ 1. ROLE      — Bạn là ai? / Who are you?  │
│ 2. TASK      — Làm gì? / What to do?      │
│ 3. CONTEXT   — Bối cảnh? / Background?    │
│ 4. FORMAT    — Output format? Table/List?  │
│ 5. CONSTRAINTS — Giới hạn? / Limits?      │
└────────────────────────────────────────────┘
```

**Ví dụ / Example:**

❌ **Yếu (Weak):** "Viết User Story cho Login"

✅ **Mạnh (Strong):**
```
[ROLE] Bạn là Senior BA với 10 năm kinh nghiệm ngân hàng
[TASK] Viết 3 User Stories cho tính năng Login
[CONTEXT] Mobile Banking app cho nông dân Việt Nam, 
         Android 8+, kết nối 3G, user 45-60 tuổi
[FORMAT] Mỗi story theo format "As a... I want... So that..." 
         với Acceptance Criteria dạng Gherkin
[CONSTRAINTS] Phải hỗ trợ SMS OTP, không dùng biometric
```

**BA-Kit shortcut:** Không cần viết ROLE — agents đã có role sẵn. Chỉ cần TASK + CONTEXT. / No need for ROLE — agents have pre-configured roles. Just provide TASK + CONTEXT.

### 5.3 Khi Nào Prompt Đơn Giản, Khi Nào Chi Tiết / When Simple, When Detailed

| Tình huống / Scenario | Prompt Level | Ví dụ / Example |
|---|---|---|
| BA-Kit trên Antigravity (role sẵn) | Đơn giản / Simple | `@ba-writing Viết User Stories cho Login` |
| BA-Kit trên Claude Code | Đơn giản / Simple | Describe task in CLAUDE.md context |
| BA-Kit trên Claude CoWork | Đơn giản / Simple | `/write-stories Login feature` |
| ChatGPT (no role) | Chi tiết / Detailed | Full 5-part prompt structure |
| Task lặp lại / Repeated | Template | Lưu prompt → dùng lại |
| Task phức tạp / Complex | Chain | Chia thành nhiều prompt nhỏ |

---

## Phần 6: Bảo Mật Khi Dùng AI / Part 6: AI Security & Privacy

### 6.1 Dữ Liệu KHÔNG Nên Đưa Vào AI / Data NOT to Share with AI

**🚨 NEVER:**
| Loại dữ liệu / Data Type | Ví dụ / Example | Rủi ro / Risk |
|---|---|---|
| Credentials | Passwords, API keys, tokens | Bị leak trong training data |
| PII thật | CMND, số tài khoản khách hàng thật | Vi phạm GDPR/PDPA |
| Proprietary algorithms | Core business logic source code | Mất lợi thế cạnh tranh |
| Unreleased financial data | Báo cáo tài chính chưa công bố | Vi phạm chứng khoán |

**✅ CÓ THỂ (với cẩn trọng / With caution):**
- Requirements specs (anonymized)
- Process diagrams
- Template documents
- Public knowledge

### 6.2 Company Policy Checklist

Trước khi dùng AI cho dự án, confirm với quản lý: / Before using AI for a project, confirm with management:

- [ ] Công ty cho phép dùng AI tools nào? / Which AI tools are approved?
- [ ] Dữ liệu nào được phép đưa vào AI? / What data can be shared with AI?
- [ ] AI output có cần human review trước khi gửi khách? / Does AI output need human review before client delivery?
- [ ] Có cần disclaimer khi dùng AI-generated content? / Is a disclaimer required for AI-generated content?
- [ ] Dữ liệu có được gửi lên cloud không, hay phải local? / Can data be sent to cloud, or must it stay local?

### 6.3 ★ Cách BA-Kit Xử Lý Bảo Mật Trên 3 Nền Tảng / How BA-Kit Handles Security Across 3 Platforms

| Component | Antigravity | Claude Code | Claude CoWork |
|---|---|---|---|
| **Runtime** | Local IDE | Local CLI | Local Desktop App |
| **Agent Skills** | SKILL.md (local) | CLAUDE.md (local) | Plugins (local) |
| **Tool Execution** | Local (Python/Grep) | Local (shell) | Sandboxed |
| **MCP / External** | Config-based | API calls | Plugin-based |
| **Jira/Confluence** | PAT via `.env` | PAT via env vars | Plugin config |
| **Knowledge Base** | 786 entries local | Via file access | Via file access |
| **Credentials** | `.gitignore` protected | Environment variables | App-level secure storage |
| **Data Location** | ✅ 100% local | ✅ 100% local | ✅ 100% local (sandboxed) |

Tất cả 3 nền tảng đều local-first — dữ liệu không rời máy. / All 3 platforms are local-first — data stays on your machine.

---

## Phần 7: Learning Path — Tự Học Tiếp / Part 7: Self-Study Path

### 7.1 Free Resources — Tài Nguyên Miễn Phí

| Resource | Nội dung / Content | Link |
|---|---|---|
| Google AI Essentials | AI concepts cơ bản | Coursera (free audit) |
| Prompt Engineering Guide | Deep dive prompting | dair-ai/Prompt-Engineering-Guide (GitHub) |
| BA-Kit Ebooks | 6 sách BA tổng hợp | `ebooks/` folder |
| LearnPrompting.org | Interactive prompt tutorials | learnprompting.org |

### 7.2 Recommended Courses — Khóa Học Đề Xuất

| Course | Platform | Focus |
|---|---|---|
| ITBA "Ứng Dụng AI Trong Công Việc" | ITBA | AI for BA (Vietnamese) |
| AI for Everyone (Andrew Ng) | Coursera | AI concepts for non-technical |
| ChatGPT Prompt Engineering | DeepLearning.AI | Prompting techniques |

### 7.3 Practice Path — Lộ Trình Thực Hành

```
WEEK 0: Đọc tài liệu này / Read this document
   ↓
WEEK 1-2: Làm quen AI tools cơ bản / Learn basic AI tools
   ChatGPT/Gemini (brainstorm) + Perplexity (research)
   Thử viết prompt 5-part structure
   ↓
WEEK 3-4: Chọn nền tảng & cài BA-Kit / Choose platform & install BA-Kit
   Technical BA → Antigravity (full experience)
   Non-technical BA → Claude CoWork (dễ dùng nhất)
   DevOps BA → Claude Code (CI/CD power)
   BA-Kit Junior Start (docs/junior-start.md)
   @ba-elicitation → @ba-writing → @ba-validation
   ↓
MONTH 2: BA-Kit full squad orchestration
   Workflow Cookbook (20 scenarios)
   Kết nối Jira/Confluence (MCP/Plugins/API)
   ↓
MONTH 3+: Advanced
   Multi-platform workflows (Claude Code CI + Antigravity orchestration)
   Multi-tool workflows (Figma → Antigravity → Jira)
   Claude CoWork slash commands for BA automation
   Custom agent creation
   Xem `docs/ai-tools-guide.md` cho multi-tool recipes
```

---

> AI giúp BA nhanh hơn, nhưng không thay thế khả năng **hỏi đúng câu hỏi** và **hiểu đúng vấn đề**.
>
> *AI makes BAs faster, but doesn't replace the ability to ask the right questions and understand the real problem.*
