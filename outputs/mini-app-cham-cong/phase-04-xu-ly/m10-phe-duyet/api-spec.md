# API Specification — M10: Phê duyệt

Base URL: `/api/v1`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /approvals/inbox | Danh sách đơn chờ phê duyệt | MANAGER, DEPT_HEAD, SITE_HR, GLOBAL_HR | US-APPR-01 |
| GET | /approvals/{id} | Chi tiết đơn chờ duyệt | MANAGER, DEPT_HEAD, SITE_HR, GLOBAL_HR | US-APPR-01 |
| POST | /approvals/{id}/approve | Phê duyệt đơn | Approver tại level hiện tại | US-APPR-01 |
| POST | /approvals/{id}/reject | Từ chối đơn (bắt buộc lý do) | Approver tại level hiện tại | US-APPR-01 |
| POST | /approvals/batch | Phê duyệt hàng loạt nhiều đơn | MANAGER, SITE_HR, GLOBAL_HR | US-APPR-03 |
| GET | /approval-chains | Danh sách cấu hình chuỗi phê duyệt | HR_ADMIN, SYS_ADMIN | US-APPR-02 |
| POST | /approval-chains | Tạo chuỗi phê duyệt mới | HR_ADMIN, SYS_ADMIN | US-APPR-02 |
| PUT | /approval-chains/{id} | Cập nhật chuỗi phê duyệt | HR_ADMIN, SYS_ADMIN | US-APPR-02 |
| GET | /approval-chains/closing-date-config | Xem cấu hình ngày chốt công | HR_ADMIN | US-APPR-02 |
| PUT | /approval-chains/closing-date-config | Cập nhật ngày chốt công | HR_ADMIN, SYS_ADMIN | US-APPR-02 |

## Sample Request/Response

### GET /approvals/inbox
Query params: `?type=LEAVE&page=1&pageSize=20`

Response `200`:
```json
{
  "items": [
    {
      "id": "APR-2025-00089",
      "requestType": "LEAVE",
      "employeeName": "Nguyễn Văn A",
      "submittedAt": "2025-05-18T09:00:00Z",
      "requestPeriod": { "from": "2025-05-20", "to": "2025-05-22" },
      "currentLevel": 1,
      "totalLevels": 2,
      "priority": "HIGH"
    }
  ],
  "total": 14,
  "page": 1
}
```

### POST /approvals/{id}/reject
Request:
```json
{
  "reason": "Thời điểm này phòng ban đang thiếu nhân lực, vui lòng sắp xếp lại lịch."
}
```
Response `200`:
```json
{
  "id": "APR-2025-00089",
  "status": "REJECTED",
  "processedAt": "2025-05-18T10:15:00Z"
}
```

### POST /approvals/batch
Request:
```json
{
  "ids": ["APR-2025-00089", "APR-2025-00090"],
  "action": "APPROVE",
  "note": "Đã kiểm tra và phê duyệt loạt"
}
```
Response `200`:
```json
{
  "approved": 2,
  "failed": 0,
  "results": [
    { "id": "APR-2025-00089", "status": "APPROVED" },
    { "id": "APR-2025-00090", "status": "APPROVED" }
  ]
}
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | REJECT_REASON_REQUIRED | Lý do từ chối là bắt buộc (tối thiểu 10 ký tự) |
| 403 | NOT_CURRENT_APPROVER | Không phải approver của level hiện tại |
| 403 | SELF_APPROVE_FORBIDDEN | Không được tự phê duyệt đơn của chính mình |
| 409 | ALREADY_PROCESSED | Đơn đã được xử lý trước đó |
| 423 | PERIOD_LOCKED | Kỳ công đã chốt, không thể phê duyệt |
