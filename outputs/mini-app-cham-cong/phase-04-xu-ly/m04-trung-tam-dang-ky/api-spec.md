# API Specification — M04: Trung tâm Đăng ký

Base URL: `/api/v1`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /leave-requests | Lấy danh sách đơn nghỉ của NV | EMPLOYEE, HR, MANAGER | US-REG-01 |
| POST | /leave-requests | Tạo đơn xin nghỉ phép mới | EMPLOYEE, HR | US-REG-01 |
| DELETE | /leave-requests/{id} | Yêu cầu hủy đơn nghỉ đã duyệt | EMPLOYEE | US-REG-01 |
| GET | /leave-requests/balance | Xem hạn mức phép còn lại | EMPLOYEE | US-REG-01 |
| GET | /shift-changes | Danh sách đơn đổi ca | EMPLOYEE, HR, MANAGER | US-REG-02 |
| POST | /shift-changes | Tạo đơn đăng ký đổi ca | EMPLOYEE | US-REG-02 |
| GET | /overtime-requests | Danh sách đơn tăng ca | EMPLOYEE, HR, MANAGER | US-REG-03 |
| POST | /overtime-requests | Tạo đơn đăng ký tăng ca | EMPLOYEE | US-REG-03 |
| GET | /leave-requests/tracking | Theo dõi trạng thái đơn từ | EMPLOYEE | US-REG-04 |
| GET | /leave-policies | Danh sách chính sách phép năm | HR, MANAGER | US-REG-05 |
| PUT | /leave-policies/{id} | Cập nhật cấu hình chính sách phép | HR_ADMIN | US-REG-05 |

## Sample Request/Response

### POST /leave-requests
Request:
```json
{
  "leaveType": "ANNUAL",
  "startDate": "2025-05-20",
  "endDate": "2025-05-22",
  "halfDay": null,
  "reason": "Nghỉ phép cá nhân",
  "attachments": []
}
```
Response `201`:
```json
{
  "id": "LR-2025-00123",
  "status": "PENDING",
  "workingDays": 3,
  "balanceAfter": { "remaining": 9, "pending": 3 }
}
```

### GET /leave-requests/balance
Response `200`:
```json
{
  "annual": { "total": 12, "used": 3, "pending": 0, "remaining": 9 },
  "carryover": { "days": 2, "expiresAt": "2025-03-31" }
}
```

### POST /overtime-requests
Request:
```json
{
  "date": "2025-05-20",
  "startTime": "18:00",
  "endTime": "21:00",
  "reason": "Hoàn thành deadline dự án"
}
```
Response `201`:
```json
{
  "id": "OT-2025-00045",
  "status": "PENDING",
  "hours": 3,
  "multiplier": 1.5
}
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | DUPLICATE_LEAVE | Đã có đơn nghỉ trùng ngày |
| 400 | INSUFFICIENT_BALANCE | Không đủ số ngày phép |
| 400 | ADVANCE_NOTICE_REQUIRED | Cần báo trước tối thiểu N ngày |
| 400 | ATTACHMENT_REQUIRED | Loại phép này yêu cầu đính kèm tài liệu |
| 409 | LEAVE_OT_CONFLICT | Xung đột với OT đã được duyệt ngày này |
| 423 | PERIOD_LOCKED | Kỳ công đã chốt, không thể tạo đơn |
