# Hướng Dẫn Chọn AI Tool Cho BA / AI Tools Guide for BAs

> BA-Kit là core engine. Các tool khác cung cấp đầu vào và kênh đầu ra.
> *BA-Kit is the core engine. Other tools provide inputs and output channels.*

---

## Ma Trận Chọn Tool / Tool Selection Matrix

| BA Task | Best Tool | Tại sao / Why | Feed vào BA-Kit / Feed to BA-Kit |
|---------|-----------|-------------|--------------------------------|
| 💡 Brainstorm nhanh | ChatGPT / Gemini | Nhanh, creative, low-cost | Copy output → `@ba-writing` refine |
| 🎨 UI Mockup | Figma / v0 / Lovable | Visual-first, interactive | Screenshot → `@ba-writing` Visual Scan |
| 🖼️ **AI UI Gen** | **Stitch MCP** ★ | Native MCP, spec → screen | `@ba-writing` spec → generate → `@ba-validation` |
| 💻 Vibe Coding | Cursor / Lovable / Bolt | Prototype → code nhanh | Code output → `@ba-validation` review. Xem `docs/design-prototype-guide.md` |
| 🔍 Research | Perplexity / Grok | Real-time web, citations | Findings → `@ba-strategy` PESTLE input |
| 📊 Presentation | Gemini / Gamma | Slides, visual reports | Outline → `@ba-facilitation` workshop |
| 🧠 **AI Agent IDE** | **Antigravity** ★ | Agent Skills, MCP, local-first | **Nền tảng chính của BA-Kit** |
| 💻 **Agentic Dev CLI** | **Claude Code** ★ | Project-level, CI/CD, Git native | **Code review + BA spec automation** |
| 💼 **Knowledge Desktop** | **Claude CoWork** ★ | Vibe working, plugins, non-technical | **BA truyền thống, document synthesis** |
| 📝 **Deep Spec** | **Antigravity + BA-Kit** ★ | System 2, INVEST, templates | **Core competency** |
| ✅ **Test Cases** | **Antigravity + BA-Kit** ★ | RTM, UAT, Gherkin AC | **Core competency** |
| 📐 **Diagrams** | **Antigravity + BA-Kit** ★ | BPMN, Mermaid, Swimlane | **Core competency** |
| 🔗 **Jira/Confluence** | **Antigravity + BA-Kit** ★ | `@ba-jira`, `@ba-confluence` via MCP | **Core competency** |
| 🔄 **Code → Spec Reverse** | **Claude Code** ★ | Read codebase, extract specs | `@ba-writing` refine extracted specs |
| 📄 **Doc Synthesis** | **Claude CoWork** ★ | Multi-file reading, summarize | `@ba-writing` polish output |

---

## Input Adapters — Đưa Output Từ Tool Khác Vào BA-Kit

### Từ ChatGPT/Gemini → BA-Kit
```
1. Dùng ChatGPT: "Brainstorm 10 features cho app đặt xe"
2. Copy kết quả
3. @ba-writing: "Đây là notes từ brainstorm session: [paste]. 
   Hãy viết User Stories chuẩn INVEST với Gherkin AC."
4. @ba-validation: Review chất lượng
```

### Từ Figma/v0 → BA-Kit
```
1. Thiết kế UI trong Figma hoặc v0
2. Export/Screenshot
3. @ba-writing: [Upload image] "Scan UI này. Extract Field Specs, 
   buttons, validation rules, user interactions."
4. @ba-nfr: "Kiểm tra WCAG accessibility cho các elements vừa extract."
```

### Từ Perplexity/Grok → BA-Kit
```
1. Perplexity: "Research xu hướng Mobile Banking tại Việt Nam 2026"
2. Copy citation-backed findings
3. @ba-strategy: "Dựa trên research sau, chạy PESTLE for Mobile Banking project: [paste]"
4. @ba-elicitation: "Từ PESTLE, tạo 10 câu hỏi stakeholder interview"
```

---

## Output Adapters — Export BA-Kit Output Sang Tool Khác

### BA-Kit → Google Docs / Notion
```
1. @ba-writing + @ba-validation: Tạo BRD/SRS validated
2. @ba-export: Export thành Markdown polished
3. Copy/paste vào Google Docs hoặc Notion
   (Markdown → rich text auto-conversion)
```

### BA-Kit → Figma
```
1. @ba-writing: Visual Scan → extract Field Specs
2. Dùng specs để hướng dẫn Figma design:
   "Button [Save] → triggers API POST /orders
    Field [Email] → regex validation required
    Error state → show inline error message"
```

### BA-Kit → Cursor/Lovable (Vibe Coding)
```
1. @ba-writing: Tạo User Stories + AC (Gherkin)
2. @ba-nfr: Định nghĩa tech constraints
3. Copy specs → Cursor/Lovable prompt:
   "Implement these User Stories: [paste stories + AC]
    Tech stack: React + Node.js
    Follow these NFRs: [paste NFR specs]"
4. @ba-validation: Review generated code vs specs
```

### BA-Kit → Jira / Confluence (Native trên Antigravity)
```
1. Bất kỳ BA artifacts nào
2. @ba-jira: Publish trực tiếp qua MCP
3. @ba-confluence: Publish trực tiếp qua MCP
   (Không cần copy/paste — automated pipeline)
```

### Claude Code → BA-Kit (Reverse Engineering)
```
1. Claude Code: "Đọc codebase Payment module. Extract business rules,
   validation logic, và API contracts."
2. Claude Code generates tech specs từ code
3. @ba-writing: "Chuyển tech specs này thành User Stories với 
   Gherkin AC. Đảm bảo trả về ngôn ngữ business."
4. @ba-validation: Review chất lượng (INVEST check)
```

### Claude CoWork → BA-Kit (Document Synthesis)
```
1. Claude CoWork: "Đọc 5 file meeting notes trong folder /meetings/.
   Tổng hợp thành requirements summary."
2. CoWork tự động đọc, tổng hợp, tạo draft
3. @ba-writing: "Từ summary này, viết User Stories chuẩn INVEST."
4. @ba-validation: Quality gate
```

---

## Platform Comparison / So Sánh Platform

| Feature | ChatGPT | Gemini | Cursor | Antigravity | Claude Code | Claude CoWork |
|---------|---------|--------|--------|-------------|-------------|---------------|
| **Nhà phát triển** | OpenAI | Google | Anysphere | Google DeepMind | Anthropic | Anthropic |
| **Giao diện** | Web | Web | IDE | IDE | CLI | Desktop App |
| **Target** | Everyone | Everyone | Developers | Dev + Tech BA | Dev + DevOps | Knowledge Workers |
| Chat AI cơ bản | ★★★★★ | ★★★★ | ★★★ | ★★★★ | ★★★★ | ★★★★ |
| Brainstorm | ★★★★★ | ★★★★ | ★★ | ★★★ | ★★★ | ★★★★ |
| Code Gen | ★★★★ | ★★★ | ★★★★★ | ★★★ | ★★★★★ | ★★ |
| Deep Spec (BRD/SRS) | ★★ | ★★ | ★ | ★★★★★ | ★★★★ | ★★★ |
| Diagrams | ★★ | ★★ | ★ | ★★★★★ | ★★★ | ★★ |
| Math/ROI | ★★★ | ★★★ | ★★ | ★★★★★ | ★★★★ | ★★ |
| Agent Skills (`@`) | ❌ | ❌ | ❌ | ★★★★★ | Via CLAUDE.md | Via Plugins |
| System 2 | ❌ | ❌ | ❌ | ★★★★★ | ★★★★ (Agentic) | ★★★ |
| MCP Protocol | ❌ | ❌ | Partial | ★★★★★ | ★★★ (Shell) | Via Plugins |
| Git Native | ❌ | ❌ | ★★★ | ★★★ | ★★★★★ | ❌ |
| Headless/CI | ❌ | ❌ | ❌ | ★★★ | ★★★★★ | ❌ |
| Non-tech friendly | ★★★★★ | ★★★★★ | ★★ | ★★★ | ★★ | ★★★★★ |
| Local-first | ❌ (Cloud) | ❌ (Cloud) | ✅ | ✅ | ✅ | ✅ |
| BA-Kit Support | ❌ | ❌ | ❌ | ★★★★★ | ★★★★ | ★★★ |

**Kết luận / Conclusion:**
- Dùng **ChatGPT/Gemini** cho brainstorm, research, quick tasks
- Dùng **Cursor/Lovable** cho code generation
- Dùng **Figma/v0** cho visual design
- Dùng **Antigravity** cho **full BA-Kit experience**: specs, validation, traceability, MCP integration
- Dùng **Claude Code** cho **technical BA**: code review, reverse engineering specs, CI/CD pipeline
- Dùng **Claude CoWork** cho **traditional BA**: document synthesis, meeting notes, easy delegation
- BA-Kit: Antigravity (full), Claude Code (strong), Claude CoWork (good)

---

## Workflow Recipes — Multi-Tool Pipelines

### Recipe 1: "Figma → Antigravity → Jira" (Design-First)
```
[Figma] → Design Payment UI
[Antigravity] @ba-writing: Scan → Field Specs + User Stories
[Antigravity] @ba-validation: INVEST check (Health Score ≥ 80)
[Antigravity] @ba-jira: Create Jira tickets from validated stories
[Cursor] → Implement from specs + Jira tickets
```

### Recipe 2: "Research → Antigravity → Confluence" (Strategy-First)
```
[Perplexity] → Research market trends
[Antigravity] @ba-strategy: SWOT / PESTLE analysis
[Antigravity] @ba-elicitation: Stakeholder interview questions
[Antigravity] @ba-writing: BRD draft
[Antigravity] @ba-confluence: Publish BRD to Confluence wiki
```

### Recipe 3: "ChatGPT → Antigravity → Jira + Confluence" (Full Pipeline)
```
[ChatGPT] → Quick brainstorm feature list
[Antigravity] @ba-writing: Convert to INVEST User Stories
[Antigravity] @ba-validation: Quality gate
[Antigravity] @ba-jira: Stories → Jira tickets
[Antigravity] @ba-confluence: Specs → Confluence docs
[Antigravity] @ba-traceability: RTM linking Jira + Confluence
```

### Recipe 4: "Claude Code → Antigravity" (Reverse Engineering)
```
[Claude Code] → Read Payment module codebase
[Claude Code] → Extract business rules + API contracts
[Antigravity] @ba-writing: Convert tech specs → business language
[Antigravity] @ba-validation: INVEST quality check
[Antigravity] @ba-jira: Create regression test tickets
```

### Recipe 5: "Claude CoWork → Antigravity → Jira" (Non-Technical BA)
```
[Claude CoWork] → Read 10 meeting notes from /meetings/
[Claude CoWork] → Synthesize into requirements summary
[Antigravity] @ba-writing: Convert → formal User Stories
[Antigravity] @ba-validation: Quality gate
[Antigravity] @ba-jira: Publish to Jira sprint backlog
```

### Recipe 6: "Multi-Platform CI Pipeline" (Advanced)
```
[Antigravity] @ba-writing: Create specs + stories
[Antigravity] @ba-validation: Quality gate
[Antigravity] @ba-jira: Publish to Jira
[Claude Code] → Auto-implement from Jira tickets (headless)
[Claude Code] → Run tests, fix failures, create PR
[Antigravity] @ba-validation: Review generated code vs specs
```

---

> Dùng tool phù hợp cho từng bước. Không tool nào làm tốt mọi thứ.
> *Use the right tool for each step. No single tool does everything well.*
>
> Antigravity = full power. Claude Code = CI/CD automation. Claude CoWork = non-technical BA.
