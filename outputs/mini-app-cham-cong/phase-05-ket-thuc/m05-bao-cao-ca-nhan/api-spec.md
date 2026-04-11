# API Specification — M05-RPT: Báo cáo Cá nhân

Base URL: `/api/v1/reports/personal`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /reports/personal/dashboard | Dashboard hiệu suất cá nhân (score, giờ, phép, OT) | EMPLOYEE | US-RPTPRS-01 |
| GET | /reports/personal/kpi | Bảng KPI theo quý và highlights | EMPLOYEE | US-RPTPRS-02 |
| GET | /reports/personal/trend | Dữ liệu biểu đồ xu hướng chuyên cần | EMPLOYEE | US-RPTPRS-01 |

## Sample Request/Response

### GET /reports/personal/dashboard
Query params: `?month=2025-05`

Response `200`:
```json
{
  "period": "2025-05",
  "score": {
    "value": 92,
    "level": "GREEN",
    "onTimeDays": 22,
    "totalWorkingDays": 24
  },
  "hours": {
    "actual": 168.5,
    "required": 176,
    "progressPercent": 95.7
  },
  "leaves": {
    "approved": 2,
    "unit": "days"
  },
  "overtime": {
    "approvedHours": 12.5
  }
}
```

### GET /reports/personal/kpi
Query params: `?quarter=2025-Q2`

Response `200`:
```json
{
  "quarter": "2025-Q2",
  "attendance": { "score": 90, "trend": "UP" },
  "highlights": [
    { "type": "PERFECT_WEEK", "label": "Tuần không vi phạm", "count": 8 },
    { "type": "OT_HOURS", "label": "Tổng giờ OT", "value": 34.5 }
  ]
}
```

### GET /reports/personal/trend
Query params: `?view=weekly&periods=4`

Response `200`:
```json
{
  "view": "weekly",
  "data": [
    { "label": "Tuần 1", "score": 88, "lateDays": 1 },
    { "label": "Tuần 2", "score": 95, "lateDays": 0 },
    { "label": "Tuần 3", "score": 91, "lateDays": 1 },
    { "label": "Tuần 4", "score": 92, "lateDays": 0 }
  ]
}
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | INVALID_PERIOD | Kỳ báo cáo không hợp lệ |
| 404 | NO_DATA | Chưa có dữ liệu chấm công cho kỳ này |
| 422 | INSUFFICIENT_DATA | Chưa đủ dữ liệu (cần tối thiểu 1 tháng) |
