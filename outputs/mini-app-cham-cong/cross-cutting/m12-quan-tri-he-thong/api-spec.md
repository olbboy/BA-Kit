# API Specification — M12: Quản trị Hệ thống

Base URL: `/api/v1/admin`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /admin/sites | Danh sách chi nhánh | SYSTEM_ADMIN, SUPER_ADMIN | US-SYS-01 |
| POST | /admin/sites | Tạo chi nhánh mới | SYSTEM_ADMIN, SUPER_ADMIN | US-SYS-01 |
| PUT | /admin/sites/{id} | Cập nhật thông tin chi nhánh | SYSTEM_ADMIN, SUPER_ADMIN | US-SYS-01 |
| DELETE | /admin/sites/{id} | Deactivate chi nhánh (soft delete) | SYSTEM_ADMIN, SUPER_ADMIN | US-SYS-01 |
| GET | /admin/audit-logs | Xem audit log (có filter) | GLOBAL_HR, SYS_ADMIN | US-SYS-02 |
| POST | /admin/audit-logs/export | Xuất audit log ra file | GLOBAL_HR, SYS_ADMIN | US-SYS-02 |
| POST | /admin/offboarding | Kích hoạt quy trình offboarding NV | HR_ADMIN, SYS_ADMIN | US-SYS-03 |
| GET | /admin/offboarding/{employeeId}/status | Trạng thái offboarding của NV | HR_ADMIN, SYS_ADMIN | US-SYS-03 |
| GET | /admin/period-closing | Xem trạng thái chốt công hiện tại (per-site) | HR_ADMIN, SITE_HR | US-SYS-04 |
| PUT | /admin/period-closing/config | Cấu hình closingDay, graceDays, weekendRule cho site | SYS_ADMIN | US-SYS-04 |
| POST | /admin/period-closing/lock | Trigger chốt công thủ công (ngoài cron) | GLOBAL_HR, SYS_ADMIN | US-SYS-04 |
| POST | /admin/period-closing/unlock | Exception unlock cho NV + ngày cụ thể | GLOBAL_HR, SYS_ADMIN | US-SYS-04 |
| GET | /admin/period-closing/history | Lịch sử các kỳ chốt (timestamp, actor) | HR_ADMIN | US-SYS-04 |
| POST | /admin/onboarding | Khởi tạo quy trình onboarding NV mới | HR_ADMIN, SYS_ADMIN | US-SYS-05 |
| GET | /admin/onboarding/{employeeId}/status | Trạng thái onboarding wizard (7 bước) | HR_ADMIN | US-SYS-05 |
| POST | /admin/onboarding/batch | Bulk onboarding nhiều NV cùng lúc | HR_ADMIN, SYS_ADMIN | US-SYS-05 |
| GET | /admin/retention-policies | Danh sách data retention policy per category | SYS_ADMIN, SUPER_ADMIN | US-SYS-06 |
| PUT | /admin/retention-policies/:category | Cập nhật retention cho category (retentionDays, archivePolicy) | SYS_ADMIN, SUPER_ADMIN | US-SYS-06 |
| GET | /admin/retention-policies/dashboard | Dashboard compliance + dung lượng + sắp hết hạn | SYS_ADMIN, GLOBAL_HR | US-SYS-06 |
| POST | /admin/retention-policies/preview | Preview impact trước khi áp dụng policy mới | SYS_ADMIN | US-SYS-06 |
| POST | /admin/retention-policies/purge | Trigger purge thủ công (double confirm) | SUPER_ADMIN | US-SYS-06 |
| POST | /admin/retention-policies/archive | Trigger archive thủ công | SYS_ADMIN | US-SYS-06 |
| GET | /admin/retention-policies/compliance | Xuất báo cáo compliance (PDF) | SYS_ADMIN, GLOBAL_HR | US-SYS-06 |
| POST | /admin/retention-policies/erasure-request | Right to Erasure cho 1 NV (NĐ 13/2023) | SUPER_ADMIN | US-SYS-06 |

## Sample Request/Response

### POST /admin/sites
Request:
```json
{
  "name": "Chi nhánh Hà Nội",
  "code": "HN01",
  "address": "123 Nguyễn Huệ, Hà Nội",
  "timezone": "Asia/Ho_Chi_Minh",
  "closingDay": 25
}
```
Response `201`:
```json
{
  "id": "site-uuid-001",
  "code": "HN01",
  "status": "ACTIVE",
  "createdAt": "2025-05-20T10:00:00Z"
}
```

### GET /admin/audit-logs
Query params: `?action=SITE_UPDATE&userId=abc&from=2025-05-01&to=2025-05-31&page=1`

Response `200`:
```json
{
  "items": [
    {
      "id": "LOG-00456",
      "action": "SITE_UPDATE",
      "actor": "admin@company.com",
      "target": "site/HN01",
      "changes": { "closingDay": { "from": 25, "to": 28 } },
      "timestamp": "2025-05-15T14:30:00Z",
      "ip": "192.168.1.10"
    }
  ],
  "total": 1
}
```

### POST /admin/offboarding
Request:
```json
{
  "employeeId": "EMP-00123",
  "lastWorkingDate": "2025-05-31",
  "reason": "RESIGNATION",
  "targetSiteId": null
}
```
Response `202`:
```json
{
  "jobId": "OFF-JOB-00012",
  "employeeId": "EMP-00123",
  "status": "INITIATED",
  "steps": ["DEACTIVATE_BIOMETRIC", "CLOSE_PENDING_REQUESTS", "TRANSFER_APPROVALS"]
}
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | DUPLICATE_SITE_CODE | Mã chi nhánh đã tồn tại |
| 400 | IMMUTABLE_FIELD | Không được phép sửa mã chi nhánh |
| 409 | SITE_HAS_ACTIVE_EMPLOYEES | Chi nhánh còn NV active, cần chuyển trước khi deactivate |
| 404 | EMPLOYEE_NOT_FOUND | Không tìm thấy nhân viên |
| 422 | OFFBOARDING_IN_PROGRESS | NV đang trong quy trình offboarding |
