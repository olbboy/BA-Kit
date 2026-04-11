# API Specification — Module 05: Quản lý Nhân sự

Base URL: `/api/v1`

## Endpoints

| Method | Path | Mô tả | Auth | Ref |
|--------|------|--------|------|-----|
| GET | /employees | Danh sách nhân viên (filter: site, dept, status) | HR_ADMIN, SITE_HR | US-EMP-03 |
| POST | /employees | Tạo nhân viên mới | HR_ADMIN | US-EMP-03 |
| GET | /employees/:id | Chi tiết nhân viên | HR_ADMIN, SITE_HR | US-EMP-03 |
| PUT | /employees/:id | Cập nhật thông tin nhân viên | HR_ADMIN | US-EMP-03 |
| DELETE | /employees/:id | Vô hiệu hóa nhân viên (soft-delete) | HR_ADMIN | US-EMP-03 |
| POST | /employees/bulk-import | Import nhân viên hàng loạt từ file Excel/CSV | HR_ADMIN | US-EMP-04 |
| GET | /employees/presence | Dashboard hiện diện real-time (đang có mặt/vắng) | HR_ADMIN, SITE_HR | US-EMP-05 |
| GET | /departments | Danh sách phòng ban (filter: siteId) | HR_ADMIN, SITE_HR | US-EMP-02 |
| POST | /departments | Tạo phòng ban mới | HR_ADMIN | US-EMP-02 |
| PUT | /departments/:id | Cập nhật phòng ban | HR_ADMIN | US-EMP-02 |
| DELETE | /departments/:id | Xóa phòng ban (chặn nếu còn NV) | HR_ADMIN | US-EMP-02 |
| GET | /org-tree | Cây tổ chức (lazy-load theo depth) | HR_ADMIN, GLOBAL_HR | US-EMP-01 |
| PATCH | /org-tree/move | Điều chuyển node (drag-and-drop) | HR_ADMIN | US-EMP-01 |
| GET | /rank-catalog | Danh mục cấp bậc | HR_ADMIN, HR | US-EMP-06 |
| POST | /rank-catalog | Tạo cấp bậc mới | HR_ADMIN | US-EMP-06 |
| PUT | /rank-catalog/:id | Cập nhật cấp bậc | HR_ADMIN | US-EMP-06 |

## Sample Request/Response

### GET /org-tree?depth=3&siteId=site-001

Response:
```json
{
  "data": {
    "id": "org-root",
    "name": "Công ty ABC",
    "type": "ORGANIZATION",
    "childCount": 3,
    "children": [
      {
        "id": "site-001",
        "name": "Chi nhánh HCM",
        "type": "SITE",
        "childCount": 5,
        "children": [
          {
            "id": "dept-001",
            "name": "Phòng Kỹ thuật",
            "type": "DEPARTMENT",
            "employeeCount": 24,
            "children": []
          }
        ]
      }
    ]
  }
}
```

### POST /employees/bulk-import

Request: `multipart/form-data` — field `file` (xlsx/csv)

Response:
```json
{
  "imported": 45,
  "failed": 2,
  "errors": [
    { "row": 5, "field": "email", "message": "Email đã tồn tại" },
    { "row": 12, "field": "deptId", "message": "Phòng ban không hợp lệ" }
  ]
}
```

### GET /employees/presence?siteId=site-001

Response:
```json
{
  "total": 120,
  "present": 98,
  "absent": 15,
  "onLeave": 7,
  "updatedAt": "2026-04-10T08:30:00Z"
}
```

## Error Codes

| HTTP | Code | Message |
|------|------|---------|
| 400 | VALIDATION_ERROR | Dữ liệu đầu vào không hợp lệ |
| 409 | EMPLOYEE_EXISTS | Mã nhân viên hoặc email đã tồn tại |
| 409 | DEPT_HAS_EMPLOYEES | Không thể xóa phòng ban còn nhân viên |
| 409 | ORG_MOVE_CIRCULAR | Không thể chuyển đơn vị vào chính nó hoặc đơn vị con |
| 422 | IMPORT_PARTIAL_FAIL | Import hoàn tất nhưng có dòng lỗi — xem `errors[]` |
| 403 | FORBIDDEN | Không có quyền thao tác với site/dept này |
