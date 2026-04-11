# API Specification — M03: Giải trình

Base URL: `/api/v1`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /anomalies | Danh sách lỗi chấm công cần giải trình | EMPLOYEE, MANAGER, HR | US-EXPL-01 |
| GET | /anomalies/{id} | Chi tiết một lỗi chấm công | EMPLOYEE, MANAGER, HR | US-EXPL-01 |
| GET | /anomalies/closing-date | Kiểm tra ngày chốt công tháng hiện tại | EMPLOYEE | US-EXPL-01 |
| POST | /corrections | Tạo yêu cầu sửa chấm công (giải trình) | EMPLOYEE | US-EXPL-02 |
| GET | /corrections | Danh sách yêu cầu sửa công đã tạo | EMPLOYEE, MANAGER, HR | US-EXPL-02 |
| GET | /corrections/{id} | Chi tiết yêu cầu sửa công | EMPLOYEE, MANAGER, HR | US-EXPL-02 |
| DELETE | /corrections/{id} | Hủy yêu cầu sửa công (chưa duyệt) | EMPLOYEE | US-EXPL-02 |
| POST | /corrections/unlock | Yêu cầu mở khóa ngoại lệ sau chốt công | GLOBAL_HR, SYS_ADMIN | US-EXPL-01 |

## Sample Request/Response

### GET /anomalies
Query params: `?month=2025-05&status=PENDING`

Response `200`:
```json
{
  "closingDate": "2025-05-25",
  "items": [
    {
      "id": "ANO-2025-00078",
      "date": "2025-05-13",
      "type": "MISSING_CHECKOUT",
      "checkIn": "08:05",
      "checkOut": null,
      "status": "AWAITING_EXPLANATION",
      "isActionable": true
    }
  ],
  "total": 1
}
```

### POST /corrections
Request (loại ADD):
```json
{
  "anomalyId": "ANO-2025-00078",
  "action": "MODIFY",
  "requestedCheckIn": "08:05",
  "requestedCheckOut": "17:30",
  "reason": "Quên quẹt thẻ lúc ra về",
  "evidence": ["evidence-img-uuid.jpg"]
}
```
Response `201`:
```json
{
  "id": "COR-2025-00031",
  "status": "PENDING",
  "anomalyId": "ANO-2025-00078"
}
```

### GET /anomalies/closing-date
Response `200`:
```json
{
  "closingDate": "2025-05-25",
  "isWorkingDay": true,
  "pendingAnomaliesCount": 3,
  "urgentCount": 1
}
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | INVALID_ACTION | Loại hành động không hợp lệ (ADD/MODIFY/DELETE) |
| 403 | PERIOD_CLOSED | Đã quá ngày chốt công, không thể giải trình |
| 404 | ANOMALY_NOT_FOUND | Không tìm thấy lỗi chấm công |
| 409 | CORRECTION_EXISTS | Đã có yêu cầu giải trình cho ngày này |
| 422 | HR_ADJUSTED | Ngày công này đã được HR điều chỉnh thủ công |
