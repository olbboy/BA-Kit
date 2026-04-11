# API Specification — Module 06: Ca làm việc

Base URL: `/api/v1`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /shifts | Danh sách ca (filter: siteId, status) | HR, MANAGER | US-SHIFT-01 |
| POST | /shifts | Tạo ca làm việc mới | HR | US-SHIFT-01 |
| GET | /shifts/:id | Chi tiết ca (giờ, ngày, nghỉ, punch-limit) | HR | US-SHIFT-01 |
| PUT | /shifts/:id | Cập nhật cấu hình ca | HR | US-SHIFT-02 |
| DELETE | /shifts/:id | Xóa ca (chặn nếu còn NV active) | HR | US-SHIFT-01 |
| PATCH | /shifts/:id/status | Bật/tắt trạng thái Active ca | HR | US-SHIFT-01 |
| PUT | /shifts/:id/work-hours | Cấu hình giờ làm việc (start/end/grace-period) | HR | US-SHIFT-02 |
| PUT | /shifts/:id/work-days | Cấu hình ngày làm việc trong tuần | HR | US-SHIFT-02 |
| PUT | /shifts/:id/breaks | Cấu hình giờ nghỉ giữa ca | HR | US-SHIFT-04 |
| PUT | /shifts/:id/punch-limit | Cấu hình giới hạn thời gian chấm công | HR | US-SHIFT-03 |
| GET | /shifts/:id/employees | Danh sách NV thuộc ca | HR | US-SHIFT-01 |
| POST | /shifts/:id/employees/import | Import NV vào ca từ file | HR | US-SHIFT-05 |
| POST | /shifts/:id/employees | Thêm NV vào ca (bulk assign) | HR | US-SHIFT-05 |
| DELETE | /shifts/:id/employees/:empId | Xóa NV khỏi ca | HR | US-SHIFT-05 |
| GET | /shift-assignments | Lịch phân ca theo NV hoặc ca (filter: empId, shiftId, month) | HR | US-SHIFT-06 |
| POST | /shift-assignments/pattern | Phân ca theo pattern (lặp tuần/tháng) | HR | US-SHIFT-06 |
| GET | /shift-assignments/team | Lịch phân ca team (Manager view: tuần/tháng) | MANAGER, DEPT_HEAD | US-SHIFT-07 |
| GET | /shift-assignments/team/gaps | Phát hiện thiếu nhân lực (gap detection) | MANAGER, DEPT_HEAD | US-SHIFT-07 |
| POST | /shift-assignments/team/request-change | Đề xuất đổi ca (Manager gửi HR) | MANAGER, DEPT_HEAD | US-SHIFT-07 |

## Sample Request/Response

### POST /shifts

Request:
```json
{
  "name": "Ca sáng",
  "siteId": "site-001",
  "startTime": "08:00",
  "endTime": "17:00",
  "gracePeriodMinutes": 15,
  "workDays": ["MON","TUE","WED","THU","FRI"],
  "breaks": [{ "startTime": "12:00", "endTime": "13:00", "label": "Nghỉ trưa" }],
  "punchLimitMinutes": 30,
  "status": "ACTIVE"
}
```

Response `201`:
```json
{
  "id": "shift-001",
  "name": "Ca sáng",
  "startTime": "08:00",
  "endTime": "17:00",
  "gracePeriodMinutes": 15,
  "totalWorkHours": 8,
  "employeeCount": 0,
  "status": "ACTIVE",
  "createdAt": "2026-04-10T07:00:00Z"
}
```

### POST /shift-assignments/pattern

Request:
```json
{
  "shiftId": "shift-001",
  "employeeIds": ["emp-001", "emp-002"],
  "pattern": "WEEKLY",
  "startDate": "2026-04-14",
  "endDate": "2026-06-30"
}
```

Response `200`:
```json
{ "assigned": 2, "periodsCreated": 12 }
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | VALIDATION_ERROR | Dữ liệu cấu hình ca không hợp lệ |
| 409 | SHIFT_HAS_EMPLOYEES | Không thể xóa ca đang có nhân viên |
| 409 | EMPLOYEE_ALREADY_IN_SHIFT | Nhân viên đã thuộc ca này |
| 409 | CONCURRENT_EDIT | Ca đã được cập nhật bởi người khác — tải lại |
| 422 | IMPORT_PARTIAL_FAIL | Import NV hoàn tất nhưng có dòng lỗi |
