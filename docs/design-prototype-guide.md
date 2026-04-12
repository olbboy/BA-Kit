# Design, Prototype & Vibe Coding Guide / Hướng Dẫn Thiết Kế & Tạo Prototype

> Từ spec → UI screen → validated prototype. Không tool nào làm hết — dùng đúng tool cho đúng bước.
> *From spec → UI screen → validated prototype. No single tool does everything — use the right tool for each step.*

---

## 1. Tool Landscape / Bản Đồ Công Cụ

| Tool | Loại | Tích hợp BA-Kit | Vai trò trong pipeline |
|------|------|-----------------|----------------------|
| **Stitch MCP** (Google) | AI UI Generator | Native MCP — gọi trực tiếp | Spec → Screen, Design System |
| **Figma MCP** | Design Read/Write | MCP config — đọc/ghi Figma file | Figma → Field Specs extraction |
| **v0** (Vercel) | Code Generator | Export → Review | Prompt → React component |
| **Lovable** | Full-stack prototype | Export → Review | Prompt → working app |
| **Bolt** (StackBlitz) | In-browser dev | Export → Review | Prompt → deployable prototype |
| **`@ba-ux`** | BA-Kit UX Agent | Native — không cần tool bên ngoài | UX Research, Persona Validation trước khi prototype |
| **`@ba-diagram`** | BA-Kit Diagram Agent | Native — Mermaid v11 | Flowchart, BPMN, ERD cho tài liệu thiết kế |

### Khi nào dùng tool nào / When to Use What

| Tình huống | Tool phù hợp | Lý do |
|-----------|-------------|-------|
| Cần UX research trước khi thiết kế | **`@ba-ux`** | Persona validation, usability check trước prototype |
| Cần UI nhanh từ text spec | **Stitch MCP** | Native MCP, generate trực tiếp từ prompt |
| Đã có Figma design, cần specs | **Figma MCP** | Đọc design → `@ba-writing` Visual Scan |
| Cần React component prototype | **v0** | Optimized cho React/Next.js output |
| Cần full-stack working app | **Lovable** | Database + API + UI trong 1 prompt |
| Cần edit code trực tiếp | **Bolt** | In-browser IDE, iterate nhanh |
| Chỉ cần Field Specs từ screenshot | **`@ba-writing`** | Visual Scan — không cần tool bên ngoài |
| Cần diagram/flowchart cho tài liệu | **`@ba-diagram`** | Mermaid v11, BPMN, ERD — không ASCII |

---

## 2. Stitch MCP Workflows

Stitch MCP kết nối trực tiếp với Antigravity qua Model Context Protocol.
Các thao tác chính:
- `create_project` — tạo project mới
- `generate_screen_from_text` — tạo screen từ text prompt
- `edit_screens` — sửa screen hiện có
- `create_design_system` — tạo design system (colors, fonts, shapes)
- `apply_design_system` — áp design system lên screens
- `list_projects`, `list_screens`, `get_screen` — xem thông tin

### Recipe A: Spec → Screen (Spec-First)

Khi đã có User Story hoặc PRD, tạo UI screen trực tiếp.

```
Bước 1: Viết spec
  @ba-writing "Viết User Story cho màn hình Login với Gherkin AC"

Bước 2: Tạo project trong Stitch
  → create_project(title: "Login Feature")

Bước 3: Generate screen từ spec
  → generate_screen_from_text(
      projectId: "<id>",
      prompt: "Login screen with email/password fields, 
               social login buttons (Google, Apple), 
               forgot password link, remember me checkbox.
               Follow Material Design 3.",
      deviceType: "MOBILE"
    )

Bước 4: Review
  → get_screen() để xem kết quả
  → @ba-validation "Review UI này với spec ban đầu"

Bước 5: Iterate
  → edit_screens(prompt: "Add loading state, error state for invalid credentials")
```

### Recipe B: Design System → Consistent Screens

Khi cần nhiều screens thống nhất brand identity.

```
Bước 1: Tạo design system
  → create_design_system(
      projectId: "<id>",
      designSystem: {
        displayName: "MyApp Design System",
        colorScheme: { preset: "TONAL_SPOT", seedColor: "#1A73E8" },
        typography: { fontFamily: "Inter" },
        shape: { cornerRadius: "ROUNDED" },
        appearance: { mode: "LIGHT" }
      }
    )

Bước 2: Generate screens (repeat cho mỗi screen)
  → generate_screen_from_text(prompt: "Dashboard with KPI cards...")
  → generate_screen_from_text(prompt: "Settings page with profile...")

Bước 3: Apply design system
  → apply_design_system(assetId: "<ds_id>", selectedScreenInstances: [...])

Bước 4: Validate consistency
  → @ba-validation "So sánh các screens — font, color, spacing có nhất quán không?"
```

### Recipe C: Iterate with BA Feedback Loop

BA → Stitch → Validate → Fix → Ship.

```
Bước 1: @ba-writing viết Feature Spec (field specs, validation rules, error states)
Bước 2: generate_screen_from_text() từ spec
Bước 3: @ba-validation review screen against spec
         → Output: "Missing: error state for empty email, loading spinner"
Bước 4: edit_screens(prompt: "Add error state for empty email field, add loading spinner on submit")
Bước 5: @ba-validation re-review → Pass
Bước 6: @ba-export package specs + screen references
```

---

## 3. Figma MCP Setup

### Cấu hình / Configuration

Thêm vào `mcp_config.json` (Antigravity):

```json
{
  "figma": {
    "command": "npx",
    "args": ["-y", "@anthropic/figma-mcp-server"],
    "env": {
      "FIGMA_ACCESS_TOKEN": "<your-figma-pat>"
    }
  }
}
```

Lấy Figma PAT: `Figma → Settings → Personal access tokens → Generate`

### Workflow: Figma → BA Specs

```
Bước 1: Figma MCP đọc design file
  → figma.get_file(fileKey: "abc123")

Bước 2: Export screenshot từ Figma
  → figma.get_image(fileKey: "abc123", nodeId: "frame-1")

Bước 3: @ba-writing Visual Scan
  → "@ba-writing (attach screenshot) Scan UI này. Trích xuất:
     - Danh sách fields (label, type, validation)
     - Button actions
     - Navigation flow
     - Error states (nếu có)"

Bước 4: @ba-nfr bổ sung
  → "@ba-nfr Thêm WCAG accessibility constraints cho các elements đã scan"

Bước 5: @ba-validation verify
  → "@ba-validation So sánh Figma design với specs vừa tạo. Flag bất kỳ gap nào."
```

### Workflow: BA Specs → Figma Feedback

```
Bước 1: @ba-writing tạo spec cho feature mới
Bước 2: Gửi spec cho designer, designer implement trong Figma
Bước 3: Figma MCP đọc lại design
Bước 4: @ba-validation "So sánh spec gốc với Figma design. Tìm deviations."
         → Output: "Figma thiếu error state cho field X", "Button Y không match spec"
```

---

## 4. Vibe Coding Pipeline

"Vibe coding" = tạo code từ ý tưởng mà không viết spec trước. BA-Kit đảm bảo output có chất lượng.

### Pattern A: Spec-First (Khuyến nghị)

```
1. @ba-ux → UX research, persona validation, usability heuristics
2. @ba-elicitation → thu thập yêu cầu
3. @ba-writing → viết PRD/User Stories
4. @ba-diagram → vẽ flowchart / user flow (Mermaid) cho docs
5. @ba-validation → validate specs (Health Score ≥ 80)
6. Copy validated specs → v0 / Lovable / Bolt
7. @ba-validation → review generated code against specs
```

### Pattern B: Prototype-First (Khám phá)

```
1. Prompt trực tiếp vào v0/Lovable/Bolt
   → "Build a task management app with kanban board"
2. Export/screenshot prototype
3. @ba-writing → "(attach screenshot) Reverse-engineer specs từ prototype"
4. @ba-validation → validate reverse-engineered specs
5. Iterate prototype based on validation feedback
```

### Anti-Pattern: Vibe Coding Không Kiểm Soát

```
Prompt → v0 → Ship → Bug → Patch → Bug → ...

Vấn đề:
- Không có acceptance criteria → không biết đúng hay sai
- Không có NFR → performance và security không xác định
- Không traceability → không biết requirement nào đã cover

Giải pháp: Luôn chạy @ba-validation review sau khi vibe coding.
```

### v0/Lovable/Bolt → BA-Kit Review Prompts

Khi đã có prototype output, dùng prompts sau để review:

```
@ba-validation "Review prototype code này:
1. So sánh với User Stories — feature nào missing?
2. Check error handling — edge cases nào bỏ sót?
3. Check accessibility — WCAG 2.1 AA compliance
4. Check security — input validation, XSS, CSRF"

@ba-nfr "Prototype đang chạy. Đánh giá:
- Response time target cho mỗi action
- Data validation rules cần thêm
- Scalability concerns"
```

---

## 5. Decision Matrix / Ma Trận Quyết Định

| Criteria | Stitch MCP | Figma MCP | v0 | Lovable | Bolt |
|----------|-----------|-----------|-----|---------|------|
| **Speed** | Nhanh (native MCP) | Trung bình | Nhanh | Nhanh | Nhanh |
| **Fidelity** | Medium-High | High (pixel-perfect) | Medium | Medium | Medium |
| **Code output** | Không | Không | React/Next.js | Full-stack | Full-stack |
| **Design system** | Có (built-in) | Có (Figma components) | Không | Không | Không |
| **BA-Kit integration** | Native (MCP) | MCP (config needed) | Manual (export) | Manual (export) | Manual (export) |
| **Cost** | Free (Google) | Figma license | Free tier limited | Free tier limited | Free tier limited |
| **Best for** | Quick UI mockup | Production design | React prototypes | Full MVP | Quick prototype |

### Flowchart quyết định

```
Bước 0: UX Research cần thiết không?
  ├─ Có → @ba-ux (persona, usability research) → tiếp tục bên dưới
  └─ Không → tiếp tục bên dưới

Bạn có Figma design sẵn?
  ├─ Có → Figma MCP → @ba-writing Visual Scan
  └─ Không
       ├─ Cần mockup nhanh? → Stitch MCP
       ├─ Cần working code? → v0 / Lovable / Bolt
       └─ Chỉ cần specs? → @ba-writing (text-based, no tool needed)

Cần diagram cho tài liệu? → @ba-diagram (Mermaid: flowchart / BPMN / ERD)
```
