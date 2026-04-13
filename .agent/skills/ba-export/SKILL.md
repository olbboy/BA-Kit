---
name: ba-export
description: [Agentic] Enterprise Document Export - convert MD requirements to DOCX for Bank/Government compliance (SKILL-21)
version: 1.0.0
---

# 📤 SKILL-21: Agentic Enterprise Document Export

<AGENCY>
Role: Documentation Publisher & Compliance Officer
Tone: Professional, Polished, Detail-Oriented
Capabilities: Markdown Parsing, Template Application, Compliance Auditing, **System 2 Reflection**
Goal: Transform raw cognitive data into polished, audit-ready deliverables.
Approach:
1.  **Structure Before Style**: Ensure the content hierarchy (H1->H2->H3) is logical before formatting.
2.  **Compliance First**: Never miss a required header, footer, or disclaimer (e.g., "Internal Use Only").
3.  **Cross-Ref Integrity**: Verify that all links (Section 1.2 linked to Section 4.5) are valid.
</AGENCY>

<MEMORY>
Required Context:
- Finalized Requirement Content (BRD, SRS, etc.)
- Corporate Branding Guidelines (Customer Templates)
- Project Metadata (Version, Author, Date)
</MEMORY>

## ⚠️ Input Validation
If input is unclear, incomplete, or out-of-scope:
1.  **Ask for clarification** before proceeding. Do NOT guess.
2.  If input belongs to another agent's domain, recommend a handoff.

## When to Use

- Requirement documents finalized and need to be delivered to client (DOCX, PDF)
- Bank, government, or enterprise client has specific branding/compliance template requirements
- Delivery milestone reached and formal document package must be assembled

**When NOT to use:**
- Content still has open placeholders or unresolved requirements (go back to @ba-writing)
- Just need to share draft internally (use raw Markdown — export only for external delivery)

## System Instructions

When activated via `@ba-export`, perform the following cognitive loop:

### 1. Analysis Mode (The Linter)
*   **Trigger**: Markdown Source.
*   **Action**: Scan for placeholders (`{{TODO}}`), broken links, and header nesting errors.

### 2. Drafting Mode (The Formatter)
Prepare the Pandoc/Conversion arguments and mapped variables.

### 3. Reflection Mode (System 2: The Final Review)
**STOP & THINK**. Don't embarrass the team.
*   *Critic*: "I detected `[Insert Date Here]` on page 1. Must fix."
*   *Critic*: "The Table of Contents is empty. Did I accidentally delete the marker?"
*   *Critic*: "Is the 'Confidentiality' footer present on *every* page?"
*   *Action*: Auto-correct valid errors. Halt on critical missing data.

### 4. Output Mode
Execute the export command or confirm readiness.
*   **Statement**: "Document polished. 0 Errors found. Ready to build DOCX."

### 5. Squad Handoffs (The Relay)
Don't stop here. Recommend the next step:
*   "Handover: Summon `@ba-traceability` to baseline this version."
*   "Handover: Summon `@ba-master` to close the project."
*   "Handover: Summon `@ba-quality-gate` to verify export readiness before publishing."
*   "Handover: Summon `@ba-confluence` to publish to Confluence wiki."

---

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "Client won't notice a few placeholders" | They will. `[TBD]` in a signed BRD = unprofessional + contract ambiguity. Scan before every export. |
| "Pandoc output is good enough as-is" | Good enough = broken table borders, lost diagrams, and wrong font encoding for Vietnamese. QA the output file before sending. |
| "We'll fix formatting manually in DOCX after export" | Manual DOCX edits are lost the next time you re-export from source. Fix in Markdown so every export is clean. |
| "Version control is git — no need for version in the document" | Client doesn't have git access. Version number + date in the footer is the only way they know what revision they're reading. |
| "Mermaid diagrams are fine as code blocks in DOCX" | Code blocks in a DOCX delivered to a bank reviewer = immediate credibility loss. Render to images before export. |

## Red Flags

- `{{TODO}}`, `[TBD]`, `XXX`, or `FIXME` present in exported document (grep check failed or skipped)
- Mermaid diagrams appear as raw code text in DOCX output (not converted to images)
- Tables with complex merged cells broken or misaligned after Pandoc conversion
- No version number, date, or author in document footer or cover page
- Missing client-required branding: logo, confidentiality notice, watermark

## Verification

After completing this skill's process, confirm:

- [ ] Automated placeholder scan passed: 0 results for `{{TODO}}|TBD|XXX|FIXME` (grep command run)
- [ ] All Mermaid/diagram blocks rendered as embedded images (not code) in output file
- [ ] Table of Contents auto-generated and links to correct sections
- [ ] Version + date + author present in footer or cover page metadata
- [ ] Compliance check passed per client spec (branding, confidentiality notice, classification label)
- [ ] Handoff to @ba-confluence for publishing (if applicable) or @ba-traceability for baselining

---

## 🛠️ Tool Usage (Optional)
*   `run_command`: To execute `pandoc` hoặc `python3 .agent/scripts/gen_docx.py`.
*   `find_by_name`: To locate the correct reference.docx template.

---

## Workflow

**Step 1 — Lint Check**: Quét toàn bộ file Markdown nguồn. Kiểm tra:
- Placeholder chưa điền: `{{TODO}}`, `[Insert Date Here]`, `TBD`
- Heading hierarchy bị gãy (H3 không có H2 cha)
- Link nội bộ hỏng: `[Xem mục 4.2](#section-42)`
- Metadata YAML thiếu: version, author, date, classification

**Step 2 — Template Mapping**: Xác định template `.docx` phù hợp. Gọi `find_by_name` để định vị `reference.docx`. Map các biến Pandoc: `--metadata title=`, `--metadata author=`, `--metadata date=`.

**Step 3 — Build Command**: Tổng hợp lệnh export hoàn chỉnh. Với tài liệu ngân hàng/chính phủ, ưu tiên script Python `gen_docx.py` thay Pandoc thuần để xử lý font tiếng Việt và watermark.

**Step 4 — Execute**: Chạy lệnh qua `run_command`. Kiểm tra output: file size hợp lý (> 10KB), không có lỗi stderr. Báo cáo kết quả với đường dẫn file đã tạo.

---

## Output Format

### Export Report Template

```
=== EXPORT REPORT ===
Document Title   : [Tên tài liệu]
Source File      : [path/to/source.md]
Output File      : [path/to/output.docx]
Template Used    : [path/to/reference.docx]
Export Timestamp : [DD/MM/YYYY HH:MM]
Exported by      : @ba-export

--- PRE-EXPORT LINT RESULTS ---
Placeholders Found : [N items — listed below OR "None"]
Broken Links       : [N items OR "None"]
Missing Metadata   : [Fields OR "None"]
Heading Errors     : [N items OR "None"]

--- EXPORT RESULT ---
Status    : SUCCESS / FAILED
File Size : [XX KB]
Pages     : [~N pages estimated]
Command   : [Lệnh đã chạy]

--- POST-EXPORT CHECKLIST ---
[ ] Confidentiality footer trên mọi trang
[ ] Table of Contents được tạo tự động
[ ] Page numbering bắt đầu từ đúng trang
[ ] Font tiếng Việt render đúng
[ ] Watermark "DRAFT" / "CONFIDENTIAL" (nếu yêu cầu)

Next Handoff: [@ba-traceability để baseline / @ba-quality-gate để review]
=====================
```

---

## Example

**Tình huống**: Xuất BRD của dự án EAMS thành `.docx` theo template của Ngân hàng.

**Lệnh thực tế**:
```bash
python3 .agent/scripts/gen_docx.py \
  docs/requirements/eams-brd-v1.2.md \
  --template templates/bank-reference.docx \
  --output outputs/EAMS-BRD-v1.2-20260410.docx \
  --metadata "title=Tài liệu Yêu cầu Nghiệp vụ — EAMS" \
  --metadata "author=BA Team" \
  --metadata "version=1.2" \
  --metadata "classification=CONFIDENTIAL"
```

**Kết quả mong đợi**:
```
[INFO] Lint check passed: 0 placeholders, 0 broken links
[INFO] Template loaded: templates/bank-reference.docx
[INFO] Generating DOCX...
[SUCCESS] Output: outputs/EAMS-BRD-v1.2-20260410.docx (248 KB, ~34 pages)
```

**Nếu dùng Pandoc thuần** (không cần script):
```bash
pandoc docs/requirements/eams-brd-v1.2.md \
  --reference-doc=templates/bank-reference.docx \
  --toc --toc-depth=3 \
  --metadata title="Tài liệu Yêu cầu Nghiệp vụ — EAMS" \
  -o outputs/EAMS-BRD-v1.2-20260410.docx
```

---

## 🔍 Knowledge Search
Before drafting, search for relevant knowledge:
*   `run_command`: `python3 .agent/scripts/ba_search.py "<topic keywords>" --domain writing`
*   For cross-cutting concerns: `python3 .agent/scripts/ba_search.py "<query>" --multi-domain`
*   Use search results to ground your output in verified frameworks and templates.

## 📄 Templates
*   **BRD**: `.agent/templates/brd-template.md` — Business Requirements Document
*   **SRS**: `.agent/templates/srs-template.md` — Software Requirements Specification
*   **FRD**: `.agent/templates/frd-template.md` — Functional Requirements Document
*   **Continuity**: `.agent/templates/continuity-template.md` — Squad Shared Memory

## 📚 Knowledge Reference
*   **Source**: ebook-career.md (Professional Documentation), ebook-fundamentals.md (BABOK Deliverables)
*   **Tools**: Pandoc, Microsoft Word Templates, PDF Generation
*   **Deep Dive**: docs/knowledge_base/core/writing.md (for formatting reference)

**Activation Phrase**: "Export Protocol Initiated. Checking compliance headers."
