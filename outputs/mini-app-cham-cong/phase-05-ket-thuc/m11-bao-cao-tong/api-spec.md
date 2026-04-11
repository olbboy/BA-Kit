# API Specification — M11: Báo cáo Tổng

Base URL: `/api/v1`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /reports/dashboard | Dashboard quản lý (6 counter cards + biểu đồ) | MANAGER, SITE_HR, GLOBAL_HR | US-RPT-01 |
| GET | /reports/dashboard/trend | Xu hướng chuyên cần 7/30 ngày | MANAGER, SITE_HR, GLOBAL_HR | US-RPT-01 |
| GET | /reports/dashboard/violations | Top NV vi phạm trong tháng | MANAGER, SITE_HR | US-RPT-01 |
| POST | /reports/export | Xuất báo cáo (5 loại) | SITE_HR, GLOBAL_HR | US-RPT-02 |
| POST | /payroll/export | Xuất bảng lương (13 cột chuẩn) | SITE_HR, GLOBAL_HR | US-RPT-02 |
| GET | /reports/compliance | Báo cáo tuân thủ (vi phạm, xử phạt) | HR_ADMIN, GLOBAL_HR | US-RPT-03 |
| POST | /payroll/lock | Khóa kỳ lương (payroll lock) | HR_ADMIN, SYS_ADMIN | US-RPT-04 |
| GET | /payroll/lock/status | Trạng thái khóa kỳ lương hiện tại | SITE_HR, GLOBAL_HR | US-RPT-04 |

## Sample Request/Response

### GET /reports/dashboard
Query params: `?siteId=HN01&deptId=IT&date=2025-05-20`

Response `200`:
```json
{
  "date": "2025-05-20",
  "counters": {
    "totalEmployees": 120,
    "present": 98,
    "late": 7,
    "absent": 5,
    "onLeave": 10,
    "pendingApprovals": 6
  },
  "isDataPreliminary": true
}
```

### POST /reports/export
Request:
```json
{
  "reportType": "ATTENDANCE_SUMMARY",
  "period": "2025-05",
  "siteId": "HN01",
  "format": "XLSX"
}
```
Response `202`:
```json
{
  "jobId": "EXP-JOB-00234",
  "status": "PROCESSING",
  "estimatedSeconds": 15
}
```

### POST /payroll/export
Request:
```json
{
  "period": "2025-05",
  "siteId": "HN01",
  "format": "XLSX"
}
```
Response `202`:
```json
{
  "jobId": "PAY-JOB-00089",
  "columns": 13,
  "employeeCount": 120,
  "status": "PROCESSING"
}
```

### POST /payroll/lock
Request:
```json
{
  "period": "2025-05",
  "siteId": "HN01",
  "confirmationNote": "Đã kiểm tra đủ 120/120 NV"
}
```
Response `200`:
```json
{
  "period": "2025-05",
  "lockedAt": "2025-05-25T23:59:00Z",
  "lockedBy": "hr.admin@company.com"
}
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | INVALID_REPORT_TYPE | Loại báo cáo không hợp lệ |
| 403 | SCOPE_FORBIDDEN | Không có quyền xem dữ liệu scope này |
| 409 | PAYROLL_ALREADY_LOCKED | Kỳ lương đã bị khóa trước đó |
| 422 | INCOMPLETE_DATA | Còn NV chưa có dữ liệu đủ để xuất lương |
