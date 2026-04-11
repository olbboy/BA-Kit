# API Specification — Module 07: Lịch nghỉ

Base URL: `/api/v1`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /holidays | Danh sách ngày nghỉ (filter: year, type) | HR_ADMIN, MANAGER | US-HOL-01 |
| POST | /holidays | Tạo ngày nghỉ mới | HR_ADMIN | US-HOL-01 |
| GET | /holidays/:id | Chi tiết ngày nghỉ | HR_ADMIN | US-HOL-01 |
| PUT | /holidays/:id | Cập nhật ngày nghỉ | HR_ADMIN | US-HOL-01 |
| DELETE | /holidays/:id | Xóa ngày nghỉ (chặn nếu có đơn approved) | HR_ADMIN | US-HOL-01 |
| GET | /holiday-policies | Lấy toàn bộ cấu hình policy nghỉ | HR_ADMIN | US-HOL-02 |
| PUT | /holiday-policies/birthday | Cấu hình policy nghỉ sinh nhật | HR_ADMIN | US-HOL-02 |
| PUT | /holiday-policies/wfh | Cấu hình hạn mức WFH mặc định | HR_ADMIN | US-HOL-02 |
| PUT | /holiday-policies/disaster | Bật/tắt chế độ khẩn cấp thiên tai + scope vùng | HR_ADMIN | US-HOL-02 |
| POST | /holiday-policies/sync | Trigger batch job đồng bộ lịch nghỉ → attendance | HR_ADMIN | US-HOL-03 |
| GET | /holiday-policies/sync/status | Trạng thái batch job gần nhất | HR_ADMIN | US-HOL-03 |
| GET | /holidays/calendar | Lịch nghỉ cá nhân theo tháng (Mini App view) | EMPLOYEE, HR | US-HOL-04 |

## Sample Request/Response

### POST /holidays

Request:
```json
{
  "name": "Tết Nguyên Đán",
  "type": "NATIONAL",
  "startDate": "2026-01-28",
  "endDate": "2026-02-02",
  "scope": "NATIONWIDE",
  "compensationRule": "NEXT_WORKDAY"
}
```

Response `201`:
```json
{
  "id": "hol-001",
  "name": "Tết Nguyên Đán",
  "type": "NATIONAL",
  "startDate": "2026-01-28",
  "endDate": "2026-02-02",
  "totalDays": 6,
  "createdAt": "2026-04-10T08:00:00Z"
}
```

### PUT /holiday-policies/disaster

Request:
```json
{
  "enabled": true,
  "provinceIds": ["HCM", "BD", "DN"],
  "effectiveDate": "2026-04-10",
  "reason": "Bão số 3"
}
```

Response `200`:
```json
{
  "enabled": true,
  "affectedProvinces": 3,
  "affectedEmployees": 342,
  "effectiveDate": "2026-04-10"
}
```

### GET /holidays/calendar?month=2026-04&empId=emp-001

Response:
```json
{
  "month": "2026-04",
  "holidays": [
    { "date": "2026-04-30", "name": "Ngày Giải phóng", "type": "NATIONAL" },
    { "date": "2026-05-01", "name": "Quốc tế Lao động", "type": "NATIONAL" }
  ],
  "wfhAllowance": { "perWeek": 2, "usedThisWeek": 1 }
}
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | VALIDATION_ERROR | Tên ngày nghỉ không hợp lệ hoặc để trống |
| 409 | HOLIDAY_OVERLAP | Ngày nghỉ trùng lấn với lịch hiện có |
| 409 | HOLIDAY_HAS_LEAVES | Có đơn nghỉ phép đã duyệt trùng ngày — hủy đơn trước |
| 422 | BATCH_ALREADY_RUNNING | Batch job đang chạy — vui lòng chờ hoàn tất |
