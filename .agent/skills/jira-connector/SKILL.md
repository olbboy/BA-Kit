---
name: jira-connector
description: >
  Connect to Jira Data Center via REST API using Personal Access Tokens (PAT).
  Use this skill whenever the user mentions "Jira", "issues", "tickets", "sprints",
  "boards", "JQL", "backlog", "epic", "story", "bug tracking", "issue transitions",
  "Jira search", "create ticket", "update issue", "sprint planning", or any task
  related to Jira project management. Also trigger when the user wants to automate
  Jira workflows, bulk-update issues, generate Jira reports, or integrate Jira
  with other tools. This skill handles full CRUD operations plus advanced features
  like transitions, attachments, sprints, and bulk operations on Jira Data Center.
version: 1.0.0
---

# Jira Data Center Connector

> ⚙️ **Infrastructure skill — not for direct BA invocation.**
> This skill is loaded automatically by `@ba-jira` (the BA-facing wrapper). BAs should always use `@ba-jira` for natural-language requests like *"publish these stories to Jira"*. This connector exists so the agent has a documented API surface to call into.

Connect to and operate on Jira Data Center instances using the REST API v2 with Personal Access Token authentication.

## Configuration

Before making any API calls, ensure these environment variables are set. If they are not set, ask the user to provide them:

- **`JIRA_BASE_URL`**: The base URL of the Jira instance (e.g., `https://jira.company.com` or `http://jira.company.com:8080/jira`)
- **`JIRA_PAT`**: The Personal Access Token for authentication

Store these in a `.env` file or export them in the shell. The helper scripts in `scripts/` read from these variables automatically.

### Authentication Header

All requests use Bearer token authentication:
```
Authorization: Bearer <JIRA_PAT>
Content-Type: application/json
```

### API Base Path

Jira Data Center uses API v2 (v3 is Cloud-only):
```
{JIRA_BASE_URL}/rest/api/2/
```

For Agile/Scrum features:
```
{JIRA_BASE_URL}/rest/agile/1.0/
```

## Core Operations

### 1. Search Issues (JQL)

Use POST for complex queries, GET for simple ones:

```bash
# GET - simple search
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_BASE_URL/rest/api/2/search?jql=project%3DPROJ%20AND%20status%3DOpen&maxResults=50&fields=key,summary,status,assignee"

# POST - complex search (preferred for long JQL)
curl -s -X POST -H "Authorization: Bearer $JIRA_PAT" -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/2/search" \
  -d '{
    "jql": "project = PROJ AND status = \"In Progress\" ORDER BY updated DESC",
    "startAt": 0,
    "maxResults": 50,
    "fields": ["key", "summary", "status", "assignee", "priority", "created", "updated"]
  }'
```

### 2. Create Issue

```bash
curl -s -X POST -H "Authorization: Bearer $JIRA_PAT" -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/2/issue" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Issue title",
      "description": "Detailed description",
      "issuetype": {"name": "Task"},
      "assignee": {"name": "username"},
      "priority": {"name": "Medium"}
    }
  }'
```

### 3. Get Issue Details

```bash
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_BASE_URL/rest/api/2/issue/PROJ-123?expand=names,renderedFields,changelog"
```

### 4. Update Issue

```bash
curl -s -X PUT -H "Authorization: Bearer $JIRA_PAT" -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/2/issue/PROJ-123" \
  -d '{
    "fields": {
      "summary": "Updated summary",
      "assignee": {"name": "newuser"},
      "priority": {"name": "High"}
    }
  }'
```

### 5. Delete Issue

```bash
curl -s -X DELETE -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_BASE_URL/rest/api/2/issue/PROJ-123?deleteSubtasks=true"
```

### 6. Transition Issue (Change Status)

```bash
# Step 1: Get available transitions
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_BASE_URL/rest/api/2/issue/PROJ-123/transitions"

# Step 2: Execute transition
curl -s -X POST -H "Authorization: Bearer $JIRA_PAT" -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/2/issue/PROJ-123/transitions" \
  -d '{
    "transition": {"id": "31"},
    "fields": {
      "resolution": {"name": "Done"}
    }
  }'
```

### 7. Comments

```bash
# Add comment
curl -s -X POST -H "Authorization: Bearer $JIRA_PAT" -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/2/issue/PROJ-123/comment" \
  -d '{"body": "This is a comment"}'

# Get comments
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_BASE_URL/rest/api/2/issue/PROJ-123/comment"
```

### 8. Attachments

```bash
# Upload attachment
curl -s -X POST -H "Authorization: Bearer $JIRA_PAT" \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@/path/to/file.pdf" \
  "$JIRA_BASE_URL/rest/api/2/issue/PROJ-123/attachments"
```

### 9. Projects

```bash
# List all projects
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_BASE_URL/rest/api/2/project"

# Get specific project
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_BASE_URL/rest/api/2/project/PROJ"
```

### 10. Sprints and Boards (Agile API)

```bash
# List boards
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_BASE_URL/rest/agile/1.0/board"

# Get sprints for board
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_BASE_URL/rest/agile/1.0/board/{boardId}/sprint"

# Create sprint
curl -s -X POST -H "Authorization: Bearer $JIRA_PAT" -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/agile/1.0/sprint" \
  -d '{
    "name": "Sprint 1",
    "originBoardId": 1,
    "startDate": "2026-03-01T00:00:00.000Z",
    "endDate": "2026-03-15T00:00:00.000Z",
    "goal": "Sprint goal"
  }'

# Move issues to sprint
curl -s -X POST -H "Authorization: Bearer $JIRA_PAT" -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/agile/1.0/sprint/{sprintId}/issue" \
  -d '{"issues": ["PROJ-1", "PROJ-2", "PROJ-3"]}'
```

## Helper Scripts

Use the Python helper scripts in `scripts/` for common operations. They handle authentication, pagination, error handling, and output formatting automatically.

### Quick Reference

| Script | Purpose |
|--------|---------|
| `scripts/jira_client.py` | Core API client library |
| `scripts/jira_search.py` | Search issues with JQL |
| `scripts/jira_crud.py` | Create/Read/Update/Delete issues |
| `scripts/jira_bulk.py` | Bulk operations on issues |
| `scripts/jira_sprint.py` | Sprint and board management |

Run any script with `--help` for usage details:
```bash
python3 scripts/jira_search.py --help
```

## Pagination

All list endpoints support pagination:
- `startAt`: Starting index (0-based)
- `maxResults`: Items per page
- Response includes `total`, `startAt`, `maxResults`, `isLast`

The helper scripts handle pagination automatically when using `--all` flag.

## Error Handling

Common HTTP status codes:
- **200**: Success
- **201**: Created
- **204**: No Content (successful delete)
- **400**: Bad Request (check JSON body)
- **401**: Unauthorized (check PAT)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found (check issue key/project)
- **429**: Rate Limited (implement backoff)

## Advanced Reference

For detailed endpoint specifications, CQL patterns, custom field handling, and webhook configuration, read `references/jira-api-reference.md`.

For bulk operation patterns and batch processing strategies, read `references/jira-bulk-operations.md`.
