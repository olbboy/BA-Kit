---
name: confluence-connector
description: "Manage Confluence Data Center via REST API. Use for `CQL` search, page CRUD, spaces, labels, comments, attachments, and bulk operations with PAT auth."
version: 1.0.0
---

# Confluence Data Center Connector

> ⚙️ **Infrastructure skill — not for direct BA invocation.**
> This skill is loaded automatically by `@ba-confluence` (the BA-facing wrapper). BAs should always use `@ba-confluence` for natural-language requests like *"publish this BRD to Confluence"*. This connector exists so the agent has a documented API surface to call into.

Use this skill to connect to and operate on Confluence Data Center instances via REST API with Personal Access Token authentication.

## Configuration

Set these environment variables before making any API calls. Ask the user to provide them if not set:

- **`CONFLUENCE_BASE_URL`**: Set to the base URL of the Confluence instance (e.g., `https://confluence.company.com`)
- **`CONFLUENCE_PAT`**: Set to the Personal Access Token for authentication

Store credentials in a `.env` file or export them in the shell.

### Authentication Header

Include this header in all requests:

```
Authorization: Bearer <CONFLUENCE_PAT>
Content-Type: application/json
```

### API Base Path

Target this base path for all calls:

```
{CONFLUENCE_BASE_URL}/rest/api/
```

## Content Storage Format

Use XHTML-based storage format when creating or updating pages. Pass content in the `body.storage` field with `"representation": "storage"`. Read `references/confluence-api-reference.md` for full storage format syntax, macros, and element reference.

### ⚠️ CRITICAL: Data Center Rendering Traps

**Code Macro Language Whitelist** — These are the ONLY safe `language` values:
```
SAFE:    text, javascript, java, python, sql, xml, html, css, bash, ruby, 
         groovy, csharp, c++, diff, php, scala, perl, yaml, powershell, none
BROKEN:  json, gherkin, typescript, mermaid, go, rust, kotlin, swift, toml
```
Map: `json→javascript`, `gherkin→text`, `typescript→javascript`. Add `title="JSON"` etc.

**Blocked Macros** — `ac:name="html"` is BLOCKED on DC. Never use it.

**Mermaid Plugin** — Use `ac:name="mermaid-macro"` (Stratus plugin). NOT `mermaid` or `mermaid-cloud`.

**Post-Upload Validation** — Always scan `body.view` (not `body.storage`) for `"Error rendering"` after upload. Storage accepts invalid params silently.

## Core Operations

Use these endpoints for page CRUD, search, spaces, comments, attachments, labels, and permissions.

### 1. Search Content (CQL)

Search pages with CQL. Use POST for complex queries:

```bash
curl -s -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/content/search?cql=type%3Dpage%20AND%20space%3DSPACEKEY&limit=25&start=0&expand=space,history,body.view"
```

**Common CQL patterns:**

- `type=page AND space=MYSPACE`
- `type=page AND title~"keyword"`
- `label=important AND modified >= -30d`
- `creator=currentUser() AND type=blogpost`

### 2. Create Page

Create a page in a specific space. Set `ancestors` to place it under a parent:

```bash
curl -s -X POST -H "Authorization: Bearer $CONFLUENCE_PAT" -H "Content-Type: application/json" \
  "$CONFLUENCE_BASE_URL/rest/api/content" \
  -d '{
    "type": "page",
    "title": "New Page Title",
    "space": {"key": "SPACEKEY"},
    "ancestors": [{"id": "PARENT_PAGE_ID"}],
    "body": {
      "storage": {
        "value": "<p>Page content in storage format</p>",
        "representation": "storage"
      }
    }
  }'
```

### 3. Get Page Content

Fetch a page with full content. Pass `expand` to include storage body, history, labels:

```bash
curl -s -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/content/{pageId}?expand=body.storage,history,metadata.labels,space,version"
```

Look up a page by space key and title:

```bash
curl -s -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/content?spaceKey=SPACEKEY&title=Page%20Title&expand=body.storage"
```

### 4. Update Page

Update requires the current version number. Increment version by 1:

```bash
curl -s -X PUT -H "Authorization: Bearer $CONFLUENCE_PAT" -H "Content-Type: application/json" \
  "$CONFLUENCE_BASE_URL/rest/api/content/{pageId}" \
  -d '{
    "type": "page",
    "title": "Updated Page Title",
    "version": {"number": 2},
    "body": {
      "storage": {
        "value": "<p>Updated content</p>",
        "representation": "storage"
      }
    }
  }'
```

### 5. Delete Page

Delete a page by ID:

```bash
curl -s -X DELETE -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/content/{pageId}?status=current"
```

### 6. Space Management

List all spaces:

```bash
curl -s -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/space?limit=25&start=0"
```

Get space details:

```bash
curl -s -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/space/SPACEKEY"
```

Retrieve all pages in a space:

```bash
curl -s -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/space/SPACEKEY/content/page?limit=25&start=0"
```

Create a new space:

```bash
curl -s -X POST -H "Authorization: Bearer $CONFLUENCE_PAT" -H "Content-Type: application/json" \
  "$CONFLUENCE_BASE_URL/rest/api/space" \
  -d '{
    "key": "NEWSPACE",
    "name": "New Space Name",
    "type": "global",
    "description": {
      "plain": {"value": "Space description", "representation": "plain"}
    }
  }'
```

### 7. Comments

Fetch comments on a page:

```bash
curl -s -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/content/{pageId}/child/comment?expand=body.storage"
```

Post a comment on a page:

```bash
curl -s -X POST -H "Authorization: Bearer $CONFLUENCE_PAT" -H "Content-Type: application/json" \
  "$CONFLUENCE_BASE_URL/rest/api/content" \
  -d '{
    "type": "comment",
    "container": {"id": "PAGE_ID", "type": "page"},
    "body": {
      "storage": {
        "value": "<p>Comment text</p>",
        "representation": "storage"
      }
    }
  }'
```

### 8. Attachments

Upload a file attachment. Include the `X-Atlassian-Token: nocheck` header:

```bash
curl -s -X POST -H "Authorization: Bearer $CONFLUENCE_PAT" \
  -H "X-Atlassian-Token: nocheck" \
  -F "file=@/path/to/file.pdf" \
  "$CONFLUENCE_BASE_URL/rest/api/content/{pageId}/child/attachment"
```

List all attachments on a page:

```bash
curl -s -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/content/{pageId}/child/attachment"
```

### 9. Labels

Retrieve labels on a page:

```bash
curl -s -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/content/{pageId}/label"
```

Add a label to a page:

```bash
curl -s -X POST -H "Authorization: Bearer $CONFLUENCE_PAT" -H "Content-Type: application/json" \
  "$CONFLUENCE_BASE_URL/rest/api/content/{pageId}/label" \
  -d '[{"prefix": "global", "name": "my-label"}]'
```

Remove a label from a page:

```bash
curl -s -X DELETE -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/content/{pageId}/label/my-label"
```

### 10. Page Restrictions/Permissions

Get restrictions on a page:

```bash
curl -s -H "Authorization: Bearer $CONFLUENCE_PAT" \
  "$CONFLUENCE_BASE_URL/rest/api/content/{pageId}/restriction"
```

Add a read restriction for a user:

```bash
curl -s -X PUT -H "Authorization: Bearer $CONFLUENCE_PAT" -H "Content-Type: application/json" \
  "$CONFLUENCE_BASE_URL/rest/api/content/{pageId}/restriction/byOperation/read/user?userName=username"
```

## Helper Scripts

Use the Python helper scripts in `scripts/` for common operations. They handle authentication, pagination, error handling, and output formatting automatically.

### Quick Reference

| Script | Purpose |
|--------|---------|
| `scripts/confluence_client.py` | Import as core API client library |
| `scripts/confluence_search.py` | Run CQL searches with pagination |
| `scripts/confluence_crud.py` | Create, read, update, delete pages |
| `scripts/confluence_bulk.py` | Execute bulk operations and exports |

Run any script with `--help` for usage details:

```bash
python3 scripts/confluence_search.py --help
```

## Pagination

Pass pagination parameters to all list endpoints:

- `start`: Set the starting index (0-based)
- `limit`: Set items per page (default 25)
- Check response for `_links.next` for cursor-based navigation

Use the helper scripts to auto-paginate through all results.

## Expand Parameters

Add `?expand=` to include additional data: `body.storage`, `body.view`, `history`, `metadata.labels`, `space`, `version`, `children.attachment`, `restrictions`. Combine multiple with commas: `?expand=body.storage,history,metadata.labels`.

## Error Handling

Handle these HTTP status codes in responses:

- **200**: Success
- **201**: Created
- **204**: No Content (successful delete)
- **400**: Bad Request — check body format
- **401**: Unauthorized — check PAT
- **403**: Forbidden — verify permissions
- **404**: Not Found — check page ID/space key
- **409**: Conflict — version mismatch on update
- **429**: Rate Limited — implement exponential backoff

## Advanced Reference

Read `references/confluence-api-reference.md` for storage format examples, macro syntax, content properties, and CQL patterns. Read `references/confluence-bulk-operations.md` for bulk page creation, labeling, deletion, and export patterns.
