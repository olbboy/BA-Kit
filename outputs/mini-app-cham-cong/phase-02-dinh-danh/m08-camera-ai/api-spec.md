# API Specification — Module 08: Camera AI

Base URL: `/api/v1`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /cameras | Danh sách camera (filter: siteId, status, direction) | IT_ADMIN, HR_ADMIN | US-CAM-01 |
| POST | /cameras | Đăng ký camera mới | IT_ADMIN | US-CAM-01 |
| GET | /cameras/:id | Chi tiết camera | IT_ADMIN | US-CAM-01 |
| PUT | /cameras/:id | Cập nhật cấu hình camera | IT_ADMIN | US-CAM-01 |
| PATCH | /cameras/:id/status | Bật/tắt camera (Active/Inactive) | IT_ADMIN | US-CAM-01 |
| DELETE | /cameras/:id | Xóa camera (soft-delete) | IT_ADMIN | US-CAM-01 |
| GET | /cameras/health | Dashboard health check tất cả camera | IT_ADMIN | US-CAM-03 |
| GET | /cameras/:id/health | Trạng thái sức khoẻ camera đơn lẻ | IT_ADMIN | US-CAM-03 |
| GET | /camera-mappings | Danh sách mapping camera ↔ nhân viên | HR_ADMIN, IT_ADMIN | US-CAM-02 |
| POST | /camera-mappings | Tạo mapping camera ↔ nhân viên | HR_ADMIN | US-CAM-02 |
| DELETE | /camera-mappings/:id | Xóa mapping | HR_ADMIN | US-CAM-02 |
| GET | /enrollment | Danh sách NV đã/chưa đăng ký khuôn mặt | HR_ADMIN | US-CAM-04 |
| POST | /enrollment/start | Bắt đầu wizard đăng ký Face ID (bước 1) | HR_ADMIN | US-CAM-04 |
| POST | /enrollment/:sessionId/capture | Upload ảnh khuôn mặt (bước 2) | HR_ADMIN | US-CAM-04 |
| POST | /enrollment/:sessionId/confirm | Xác nhận và hoàn tất đăng ký (bước 3) | HR_ADMIN | US-CAM-04 |
| DELETE | /enrollment/:empId | Xóa dữ liệu khuôn mặt nhân viên | HR_ADMIN | US-CAM-04 |
| POST | /webhooks/cvision | Nhận sự kiện nhận diện từ C-Vision | SYSTEM (API Key) | US-CAM-01 |

## Sample Request/Response

### POST /cameras

Request:
```json
{
  "deviceId": "cvision-cam-001",
  "name": "Cổng vào Tầng 1",
  "siteId": "site-001",
  "directionType": "IN_ONLY",
  "confidenceThreshold": 0.85,
  "status": "ACTIVE"
}
```

Response `201`:
```json
{
  "id": "cam-001",
  "deviceId": "cvision-cam-001",
  "name": "Cổng vào Tầng 1",
  "siteId": "site-001",
  "directionType": "IN_ONLY",
  "confidenceThreshold": 0.85,
  "status": "ACTIVE",
  "lastHeartbeatAt": null,
  "createdAt": "2026-04-10T08:00:00Z"
}
```

### POST /webhooks/cvision

Request (từ C-Vision):
```json
{
  "deviceId": "cvision-cam-001",
  "personId": "cvision-person-042",
  "confidence": 0.92,
  "timestamp": "2026-04-10T08:03:17Z",
  "eventType": "FACE_RECOGNIZED"
}
```

Response `200`:
```json
{ "received": true, "attendanceRecordId": "att-20260410-0803" }
```

### POST /enrollment/start

Request:
```json
{ "employeeId": "emp-001", "notes": "Đăng ký lần đầu" }
```

Response `201`:
```json
{ "sessionId": "enroll-sess-abc123", "expiresAt": "2026-04-10T09:00:00Z", "step": 1 }
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | VALIDATION_ERROR | Dữ liệu camera không hợp lệ |
| 409 | DEVICE_ID_EXISTS | Device ID đã được đăng ký tại site khác |
| 422 | CONFIDENCE_OUT_OF_RANGE | confidenceThreshold phải trong khoảng 0.70–0.99 |
| 422 | CVISION_DEVICE_NOT_FOUND | Device chưa đăng ký trên C-Vision — webhook sẽ bị reject |
| 400 | WEBHOOK_SIGNATURE_INVALID | Chữ ký webhook không hợp lệ |
| 409 | ENROLLMENT_SESSION_EXPIRED | Phiên đăng ký đã hết hạn — bắt đầu lại |
