# API Specification — Module 09: Thông báo

Base URL: `/api/v1/notifications`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /notifications/channels | Danh sách kênh thông báo và trạng thái kết nối | HR_ADMIN, IT_ADMIN | US-NOTIF-01 |
| PUT | /notifications/channels/:channel | Bật/tắt kênh (push/email/popup) | HR_ADMIN | US-NOTIF-01 |
| PUT | /notifications/channels/priority | Cấu hình thứ tự ưu tiên và fallback kênh | HR_ADMIN | US-NOTIF-01 |
| GET | /notifications/events | Danh sách sự kiện trigger thông báo | HR_ADMIN | US-NOTIF-02 |
| PATCH | /notifications/events/:eventId | Bật/tắt trigger cho từng sự kiện | HR_ADMIN | US-NOTIF-02 |
| PUT | /notifications/events/:eventId/channels | Gán kênh cho sự kiện cụ thể | HR_ADMIN | US-NOTIF-02 |
| GET | /notifications/policy | Lấy cấu hình policy (batch/throttle/schedule) | HR_ADMIN | US-NOTIF-03 |
| PUT | /notifications/policy | Cập nhật policy gửi thông báo | HR_ADMIN | US-NOTIF-03 |
| GET | /notifications/preferences | Lấy tuỳ chọn thông báo cá nhân | EMPLOYEE | US-NOTIF-03 |
| PUT | /notifications/preferences | Cập nhật tuỳ chọn thông báo cá nhân | EMPLOYEE | US-NOTIF-03 |
| GET | /notifications | Lịch sử thông báo của user hiện tại | EMPLOYEE | US-NOTIF-01 |
| PATCH | /notifications/:id/read | Đánh dấu đã đọc | EMPLOYEE | US-NOTIF-01 |
| GET | /notifications/email-templates | Danh sách email templates theo nhóm | HR_ADMIN | US-NOTIF-04 |
| GET | /notifications/email-templates/:id | Chi tiết template + HTML body + biến | HR_ADMIN | US-NOTIF-04 |
| PUT | /notifications/email-templates/:id | Cập nhật template (WYSIWYG HTML) | HR_ADMIN | US-NOTIF-04 |
| POST | /notifications/email-templates/:id/preview | Preview email render với mock data | HR_ADMIN | US-NOTIF-04 |
| POST | /notifications/email-templates/:id/test-send | Gửi email test (5/ngày max) | HR_ADMIN | US-NOTIF-04 |
| GET | /notifications/email-templates/:id/versions | Lịch sử versions (max 10) | HR_ADMIN | US-NOTIF-04 |
| POST | /notifications/email-templates/:id/rollback | Rollback về version cũ | HR_ADMIN | US-NOTIF-04 |
| PUT | /notifications/branding | Cấu hình branding (logo, color, footer) | HR_ADMIN | US-NOTIF-04 |

## Sample Request/Response

### GET /notifications/channels

Response:
```json
{
  "channels": [
    { "id": "push", "label": "App Push", "enabled": true, "status": "CONNECTED" },
    { "id": "email", "label": "Email (SMTP)", "enabled": true, "status": "CONNECTED" },
    { "id": "popup", "label": "Popup Dashboard", "enabled": true, "status": "CONNECTED" }
  ],
  "fallbackChain": ["push", "email", "popup"]
}
```

### PUT /notifications/policy

Request:
```json
{
  "batchEnabled": true,
  "batchIntervalMinutes": 15,
  "throttleMaxPerHour": 10,
  "quietHours": { "start": "22:00", "end": "07:00" },
  "timezone": "Asia/Ho_Chi_Minh"
}
```

Response `200`:
```json
{
  "batchEnabled": true,
  "batchIntervalMinutes": 15,
  "throttleMaxPerHour": 10,
  "quietHours": { "start": "22:00", "end": "07:00" },
  "updatedAt": "2026-04-10T09:00:00Z"
}
```

### PATCH /notifications/events/:eventId

Request:
```json
{ "enabled": false }
```

Response `200`:
```json
{
  "eventId": "LATE_CHECKIN",
  "label": "Chấm công trễ",
  "enabled": false,
  "affectedChannels": ["push", "email"]
}
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | VALIDATION_ERROR | Cấu hình không hợp lệ |
| 409 | CHANNEL_DISABLE_IMPACT | Tắt kênh sẽ ảnh hưởng N loại thông báo bắt buộc |
| 422 | SMTP_CONNECTION_FAILED | Không kết nối được SMTP — kiểm tra cấu hình |
| 422 | PUSH_TOKEN_INVALID | Firebase/APNs token không hợp lệ |
