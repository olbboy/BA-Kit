# Confluence Data Center — Rendering Rules

> **Source:** Production debugging on CTS Knowledge Hub (kms.cmcts.com.vn), April 2026.
> **Scope:** Confluence DC 10.x with Stratus Mermaid plugin v3.0.1+

---

## 1. Code Macro Language Whitelist

The `<ac:structured-macro ac:name="code">` macro validates `language` against a **strict whitelist**.
Invalid values cause: `Error rendering macro 'code': Invalid value specified for parameter`.

### Safe Languages (Verified)

```
text, javascript, java, python, sql, xml, html, css, bash, ruby,
groovy, csharp, c++, diff, php, scala, perl, yaml, powershell, none
```

### Broken Languages (Cause Render Error)

```
json, gherkin, typescript, mermaid, go, rust, kotlin, swift, toml, hcl
```

### Language Mapping Table

| Source (Markdown) | Confluence DC | Title Param | Notes |
|-------------------|---------------|-------------|-------|
| `json` | `javascript` | `title="JSON"` | DC does NOT support json |
| `gherkin` | `text` | `title="Gherkin Scenarios"` | Not in any whitelist |
| `typescript` / `ts` | `javascript` | `title="TypeScript"` | |
| `mermaid` | N/A | — | Use `mermaid-macro` plugin |
| `go` | `text` | `title="Go"` | |
| `rust` | `text` | `title="Rust"` | |
| `kotlin` | `text` | `title="Kotlin"` | |
| `toml` | `text` | `title="TOML"` | |

---

## 2. Blocked Macros

| Macro | Status | Error |
|-------|--------|-------|
| `ac:name="html"` | **BLOCKED** | `Unknown macro: 'html'`. Content silently stripped. |

> **Security:** HTML macro is disabled on most production DC instances. Admin must explicitly enable it. Never assume availability.

---

## 3. Mermaid Diagram Plugin

**Plugin:** [Mermaid Diagrams for Confluence](https://marketplace.atlassian.com/apps/1226567) by Stratus Add-ons

| Macro Name | Hosting | Result |
|-----------|---------|--------|
| **`mermaid-macro`** | **Data Center** | ✅ **Correct** |
| `mermaid` | DC | ❌ Unknown macro placeholder |
| `mermaid-cloud` | DC | ❌ "Diagram could not be found" |
| `html` + CDN | DC | ❌ Blocked |
| `language="mermaid"` code block | DC | ❌ Raw text |

### Correct XHTML

```xml
<ac:structured-macro ac:name="mermaid-macro">
  <ac:plain-text-body><![CDATA[
graph TD
    A --> B
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

---

## 4. Validation Method

### Rule: ALWAYS validate via `body.view`, NEVER `body.storage`

- **Storage API** (`body.storage`): Permissive — accepts invalid language params without error
- **View Renderer** (`body.view`): Strict — throws `InvalidValueException` at render time

### Post-Upload Validation Scan

```python
from confluence_xhtml import validate_rendered_pages

broken_pages = validate_rendered_pages(client, page_ids)
# Returns list of page IDs with rendering errors
```

Or manually:
```python
for pid in page_ids:
    data = api_get(f'/rest/api/content/{pid}?expand=body.view')
    view = data['body']['view']['value']
    if 'Error rendering' in view or 'Unknown macro' in view:
        print(f'BROKEN: {pid}')
```

---

## 5. Discovery Protocol for Unknown Plugins

When encountering a new Confluence plugin, use this protocol to discover the correct macro name:

```python
# 1. Create test pages with candidate names
candidates = ['mermaid', 'mermaid-macro', 'mermaid-cloud', 'mermaiddiagram']

for name in candidates:
    body = f'<ac:structured-macro ac:name="{name}"><ac:plain-text-body><![CDATA[graph LR; A-->B]]></ac:plain-text-body></ac:structured-macro>'
    page = create_page(title=f'_test_{name}', body=body)
    
    # 2. Read body.view to check rendering
    view = get_page(page['id'], expand='body.view')
    rendered = view['body']['view']['value']
    
    if 'Unknown macro' not in rendered and 'error' not in rendered.lower():
        print(f'✅ Working macro name: {name}')
    
    # 3. Delete test page
    delete_page(page['id'])
```
