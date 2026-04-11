# API Specification — Module 01: Chấm công

Base URL: `/api/v1/attendance`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /attendance/today | Hub chấm công: trạng thái, mốc In/Out, thanh tiến độ hôm nay | EMPLOYEE, HR | US-ATTEN-01 |
| GET | /attendance/stats | Thống kê hiệu suất tháng (ngày đúng giờ, trễ, vắng, OT) | EMPLOYEE, HR | US-ATTEN-02 |
| GET | /attendance/logs | Nhật ký chấm công (phân trang, accordion theo ngày) | EMPLOYEE, HR | US-ATTEN-03 |
| GET | /attendance/logs/:date | Chi tiết nhật ký ngày cụ thể | EMPLOYEE, HR | US-ATTEN-03 |
| GET | /attendance/violations | Danh sách cảnh báo vi phạm (filter: type, month) | EMPLOYEE, HR | US-ATTEN-04 |
| PATCH | /attendance/violations/:id/read | Đánh dấu đã đọc cảnh báo | EMPLOYEE | US-ATTEN-04 |
| POST | /attendance/manual-entry | Nhập chấm công thủ công (HR xác nhận) | HR | US-ATTEN-05 |
| PUT | /attendance/manual-entry/:id | Chỉnh sửa bản ghi thủ công chờ duyệt | HR | US-ATTEN-05 |
| GET | /attendance/manual-entry | Danh sách bản ghi thủ công (filter: status, empId) | HR | US-ATTEN-05 |

## Sample Request/Response

### GET /attendance/today?empId=emp-001

Response:
```json
{
  "employeeId": "emp-001",
  "date": "2026-04-10",
  "shift": { "id": "shift-001", "name": "Ca sáng", "start": "08:00", "end": "17:00" },
  "status": "CHECKED_IN",
  "checkIn": "2026-04-10T08:05:00Z",
  "checkOut": null,
  "workedMinutes": 265,
  "requiredMinutes": 480,
  "progressPercent": 55,
  "lateMinutes": 5,
  "syncedAt": "2026-04-10T08:07:00Z"
}
```

### GET /attendance/stats?empId=emp-001&month=2026-04

Response:
```json
{
  "month": "2026-04",
  "totalWorkDays": 22,
  "onTime": 17,
  "late": 3,
  "absent": 1,
  "onLeave": 1,
  "overtimeHours": 4.5,
  "attendanceRate": 95.5
}
```

### GET /attendance/logs?empId=emp-001&month=2026-04&page=1&limit=20

Response:
```json
{
  "data": [
    {
      "date": "2026-04-10",
      "status": "ON_TIME",
      "checkIn": "08:05",
      "checkOut": "17:02",
      "workedHours": 8.0,
      "lateMinutes": 0,
      "earlyLeaveMinutes": 0,
      "source": "CAMERA_AI"
    }
  ],
  "pagination": { "page": 1, "limit": 20, "total": 22 }
}
```

### POST /attendance/manual-entry

Request:
```json
{
  "employeeId": "emp-007",
  "date": "2026-04-09",
  "checkIn": "08:00",
  "checkOut": "17:00",
  "reason": "Camera bị lỗi không ghi nhận",
  "evidenceUrl": "https://storage/.../proof.jpg"
}
```

Response `201`:
```json
{
  "id": "manual-001",
  "status": "PENDING_APPROVAL",
  "createdBy": "hr-001",
  "createdAt": "2026-04-10T09:00:00Z"
}
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | VALIDATION_ERROR | Dữ liệu nhập thủ công không hợp lệ |
| 404 | NO_SHIFT_ASSIGNED | Nhân viên chưa được gán ca làm việc |
| 409 | DUPLICATE_MANUAL_ENTRY | Đã có bản ghi thủ công cho ngày này |
| 422 | DATE_LOCKED | Ngày chấm công đã bị chốt — không thể chỉnh sửa |
| 403 | FORBIDDEN | Chỉ HR được nhập chấm công thủ công |
