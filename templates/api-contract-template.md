# 🟢 SKILL-13: API CONTRACT TEMPLATE
## Template Skill - API Integration Contract

---

## 📌 SKILL METADATA

| Attribute | Value |
|-----------|-------|
| **Template ID** | TMPL-API |
| **Category** | 🟢 Template |
| **Load When** | Documenting API integrations and interface contracts |
| **Dependencies** | @ba-writing, @ba-nfr |
| **Output** | Complete API Integration Contract document |

---

## 🎯 WHEN TO USE API CONTRACT

| Use API Contract When | Don't Use When |
|-----------------------|----------------|
| ✓ System-to-system integration required | ✗ UI-only feature with no backend changes |
| ✓ Third-party provider or consumer involved | ✗ Internal DB query with no exposed interface |
| ✓ Contract must be agreed before development | ✗ Fully internal library call (use inline docs) |
| ✓ SLA / rate limits need formal agreement | ✗ Prototype / throwaway integration spike |
| ✓ Multiple teams consuming the same endpoint | ✗ Event sourcing with no request/response model |

---

## 📋 API CONTRACT TEMPLATE

```
═══════════════════════════════════════════════════════════════
                    API INTEGRATION CONTRACT
                      [System / Product Name]
═══════════════════════════════════════════════════════════════

Document Control
────────────────────────────────────────────────────────────────
Version: [X.Y]
Date: [YYYY-MM-DD]
Author: [Name]
Status: [Draft/Review/Approved]
Provider: [Team or system exposing the API]
Consumer: [Team or system calling the API]

Version History
┌─────────┬────────────┬──────────┬─────────────────────────────┐
│ Version │ Date       │ Author   │ Changes                     │
├─────────┼────────────┼──────────┼─────────────────────────────┤
│ 0.1     │ YYYY-MM-DD │ [Name]   │ Initial draft               │
│ 1.0     │ YYYY-MM-DD │ [Name]   │ Agreed by both parties      │
└─────────┴────────────┴──────────┴─────────────────────────────┘

═══════════════════════════════════════════════════════════════
SECTION 1: API ENDPOINT SPECIFICATION
═══════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────
ENDPOINT: [GET / POST / PUT / PATCH / DELETE] /api/v1/[resource]
────────────────────────────────────────────────────────────────
┌──────────────────────┬───────────────────────────────────────┐
│ Description          │ [What this endpoint does]             │
│ API Version          │ v[X]                                  │
│ Base URL             │ https://[host]/api/v[X]               │
│ Environment          │ [Dev / UAT / Production URL]          │
│ Authentication       │ [Bearer Token / API Key / OAuth 2.0] │
│ Content-Type         │ application/json                      │
│ Rate Limit           │ [e.g., 100 req/min per client]        │
│ Timeout SLA          │ [e.g., p95 response < 500ms]          │
└──────────────────────┴───────────────────────────────────────┘

REQUEST
────────────────────────────────────────────────────────────────
Headers:
┌─────────────────────────┬────────────┬──────────────────────┐
│ Header                  │ Required   │ Description          │
├─────────────────────────┼────────────┼──────────────────────┤
│ Authorization           │ Yes        │ Bearer {access_token}│
│ X-Correlation-ID        │ Yes        │ UUID for tracing     │
│ X-API-Key               │ Conditional│ If API key auth used │
│ Accept-Language         │ No         │ Default: en-US       │
└─────────────────────────┴────────────┴──────────────────────┘

Path Parameters:
┌────────────────┬──────────┬──────────┬──────────────────────┐
│ Parameter      │ Type     │ Required │ Description          │
├────────────────┼──────────┼──────────┼──────────────────────┤
│ {id}           │ string   │ Yes      │ Resource UUID        │
└────────────────┴──────────┴──────────┴──────────────────────┘

Query Parameters:
┌────────────────┬──────────┬──────────┬──────────────────────┐
│ Parameter      │ Type     │ Required │ Description          │
├────────────────┼──────────┼──────────┼──────────────────────┤
│ page           │ integer  │ No       │ Page number, min 1   │
│ pageSize       │ integer  │ No       │ Default 20, max 100  │
│ filter         │ string   │ No       │ [Field:value format] │
└────────────────┴──────────┴──────────┴──────────────────────┘

Request Body (JSON Schema):
{
  "fieldName": "string",         // Required. [Description]
  "amount": 0.00,                // Required. Decimal(10,2). Min: 0
  "category": "A|B|C",          // Required. Enum: A, B, C
  "optionalField": "string",     // Optional. Max 255 chars
  "nested": {
    "subField": "string"         // Required if nested present
  },
  "items": [                     // Optional array
    {
      "itemId": "string",        // Required. UUID
      "quantity": 1              // Required. Min: 1, Max: 9999
    }
  ]
}

RESPONSE
────────────────────────────────────────────────────────────────
Success: HTTP 200 OK (or 201 Created for POST)
{
  "status": "success",
  "data": {
    "id": "uuid-string",
    "fieldName": "string",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "updatedAt": "YYYY-MM-DDTHH:MM:SSZ"
  },
  "meta": {
    "page": 1,
    "pageSize": 20,
    "totalCount": 150
  }
}

Error Responses:
┌──────────┬────────────────────────────────────────────────┐
│ HTTP     │ Scenario                                       │
├──────────┼────────────────────────────────────────────────┤
│ 400      │ Validation failure / malformed request body   │
│ 401      │ Missing or invalid authentication token       │
│ 403      │ Authenticated but not authorized for resource │
│ 404      │ Resource not found                            │
│ 409      │ Conflict (duplicate, state mismatch)          │
│ 422      │ Semantically invalid (business rule failure)  │
│ 429      │ Rate limit exceeded                           │
│ 500      │ Internal server error                         │
│ 503      │ Service unavailable / circuit breaker open    │
└──────────┴────────────────────────────────────────────────┘

Error Body Schema:
{
  "status": "error",
  "errorCode": "VALIDATION_FAILED",   // Machine-readable code
  "message": "Human-readable summary",
  "details": [
    {
      "field": "fieldName",
      "issue": "must not be blank"
    }
  ],
  "correlationId": "uuid-for-tracing",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
}

EXAMPLE
────────────────────────────────────────────────────────────────
Request:
  POST /api/v1/orders HTTP/1.1
  Host: api.example.com
  Authorization: Bearer eyJhbGciOiJSUzI1...
  X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000
  Content-Type: application/json

  {
    "fieldName": "Sample value",
    "amount": 99.99,
    "category": "A"
  }

Response (201 Created):
  {
    "status": "success",
    "data": {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "fieldName": "Sample value",
      "createdAt": "2024-01-15T09:30:00Z"
    }
  }

[Repeat endpoint block above for each API endpoint]

═══════════════════════════════════════════════════════════════
SECTION 2: WEBHOOK SPECIFICATION
═══════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────
EVENT: [event.category.action — e.g., order.payment.completed]
────────────────────────────────────────────────────────────────
┌──────────────────────┬───────────────────────────────────────┐
│ Event Name           │ [event.category.action]               │
│ Trigger              │ [When this event fires]               │
│ Delivery Method      │ HTTP POST to consumer webhook URL     │
│ Content-Type         │ application/json                      │
│ Security             │ HMAC-SHA256 signature in header       │
│ Signature Header     │ X-Webhook-Signature                   │
│ Retry Policy         │ 3 retries: 5s, 30s, 5min backoff     │
│ Timeout              │ Consumer must respond within 10s      │
│ Expected Response    │ HTTP 2xx (any 2xx = acknowledged)     │
└──────────────────────┴───────────────────────────────────────┘

Payload Schema:
{
  "eventId": "uuid",             // Unique event identifier
  "eventType": "event.name",    // Event name
  "eventVersion": "1.0",        // Schema version
  "occurredAt": "ISO-8601",     // When event happened
  "source": "system-name",      // Originating system
  "data": {
    // Event-specific payload fields
    "resourceId": "uuid",
    "resourceType": "string",
    "changes": {}               // What changed (before/after if applicable)
  }
}

HMAC Validation (consumer responsibility):
  1. Compute HMAC-SHA256 of raw request body using shared secret
  2. Compare with X-Webhook-Signature header value
  3. Reject if mismatch (respond 401)
  4. Reject if timestamp in payload > 5 minutes old (replay protection)

═══════════════════════════════════════════════════════════════
SECTION 3: INTEGRATION CHECKLIST
═══════════════════════════════════════════════════════════════

Consumer Implementation Checklist:
┌────────────────────────────────────────────┬─────────────────┐
│ Requirement                                │ Status          │
├────────────────────────────────────────────┼─────────────────┤
│ Authentication token rotation implemented  │ ☐ Not started   │
│ All 4xx errors handled without retry       │ ☐ Not started   │
│ Retry with exponential backoff for 5xx     │ ☐ Not started   │
│ Idempotency key sent on POST/PUT           │ ☐ Not started   │
│ X-Correlation-ID logged for all requests   │ ☐ Not started   │
│ Webhook signature validated                │ ☐ Not started   │
│ Webhook duplicate delivery handled         │ ☐ Not started   │
│ Circuit breaker configured                 │ ☐ Not started   │
│ Rate limit handling (429 + Retry-After)    │ ☐ Not started   │
│ Timeout set at client level (<= SLA)       │ ☐ Not started   │
│ Alerting on sustained 4xx/5xx error rate   │ ☐ Not started   │
│ API version pinned (no auto-upgrade)       │ ☐ Not started   │
└────────────────────────────────────────────┴─────────────────┘

═══════════════════════════════════════════════════════════════
SECTION 4: SERVICE LEVEL AGREEMENT (SLA)
═══════════════════════════════════════════════════════════════

┌────────────────────────┬───────────────────────────────────┐
│ SLA Dimension          │ Target                            │
├────────────────────────┼───────────────────────────────────┤
│ Availability           │ 99.9% monthly uptime              │
│ Planned Maintenance    │ Max 4h/month, notified 72h ahead  │
│ Latency p50            │ < 100ms                           │
│ Latency p95            │ < 500ms                           │
│ Latency p99            │ < 2000ms                          │
│ Throughput             │ [X] requests/second sustained     │
│ Rate Limit             │ [X] req/min per client token      │
│ Error Rate Target      │ < 0.1% 5xx over rolling 24h      │
│ Incident Response      │ SEV-1: 30min / SEV-2: 4h          │
│ Data Retention (logs)  │ 90 days                           │
└────────────────────────┴───────────────────────────────────┘

Breach Procedure:
  1. Provider notifies consumer within [X hours] of SLA breach
  2. Root cause analysis delivered within [X business days]
  3. Remediation plan agreed within [X business days]
```

---

## ✅ API CONTRACT QUALITY CHECKLIST

```
☐ All endpoints documented with method + full path
☐ Authentication mechanism specified
☐ Every request field has type, required flag, validation rules
☐ All HTTP error codes covered with example error body
☐ Webhook HMAC validation steps documented
☐ Retry policy defined (backoff, max attempts)
☐ Rate limits specified (per client, per endpoint if different)
☐ SLA targets agreed and signed off by both parties
☐ Correlation ID tracing required in contract
☐ Integration checklist completed by consumer team
☐ API version strategy documented (deprecation notice period)
☐ Example request and response provided for each endpoint
```

---

## 🔗 RELATED SKILLS

| After API Contract... | Load |
|-----------------------|------|
| Define data fields in depth | @ba-writing (Data Dictionary) |
| Document non-functional needs | @ba-nfr |
| Write integration test cases | @ba-process |

---

*Use this template to create unambiguous API contracts that eliminate integration surprises between provider and consumer teams.*
