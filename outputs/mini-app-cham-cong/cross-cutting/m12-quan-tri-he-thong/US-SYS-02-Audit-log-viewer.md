# US-SYS-02: Audit Log Viewer

---

**AS A** System Admin,  
**I WANT TO** xem toàn bộ nhật ký hoạt động của hệ thống (ai làm gì, khi nào, dữ liệu gì thay đổi) với bộ lọc đa tiêu chí (User, Module, Action, Date range),  
**SO THAT** tôi có thể điều tra sự cố, đảm bảo compliance, và truy vết mọi thay đổi dữ liệu nhạy cảm trong hệ thống.

---

### **1. BUSINESS FLOW**

1. **Truy cập**: Admin vào "Audit Log" → Hệ thống hiển thị log mới nhất (24h gần nhất).
2. **Filter**: Chọn bộ lọc: User, Module, Action, Date range (bắt buộc ≤ 90 ngày).
3. **Xem chi tiết**: Click vào 1 record → Hiển thị: old_value, new_value, IP address, user agent.
4. **Export**: Nút "Export CSV" → tải file log theo filter hiện tại.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin | Role | Ghi chú |
| --- | --- | --- |
| Xem Audit Log | SYSTEM_ADMIN, SUPER_ADMIN | Toàn bộ log. |
| Xem Log phạm vi site | GLOBAL_HR_ADMIN | Chỉ log liên quan NV thuộc scope. |
| Export CSV | SYSTEM_ADMIN, SUPER_ADMIN | GLOBAL_HR: export giới hạn 10,000 records. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Bảng log chính**

| Cột | Mô tả |
| --- | --- |
| Timestamp | Ngày giờ UTC + timezone hiển thị |
| User | Tên + Role người thực hiện |
| Module | Module bị ảnh hưởng (Attendance, Leave, Shift, Employee...) |
| Action | CREATE / UPDATE / DELETE / LOGIN / EXPORT |
| Target | Đối tượng bị ảnh hưởng (NV ID, Shift ID...) |
| Summary | Mô tả ngắn (VD: "Updated shift 'Ca Sáng': startTime 08:00 → 08:30") |

#### **AC2. Bộ lọc**

- **User**: Autocomplete theo tên/email.
- **Module**: Dropdown multi-select.
- **Action**: Dropdown multi-select.
- **Date range**: Date picker, bắt buộc, tối đa 90 ngày.
- **Keyword**: Free-text search trong Summary.

#### **AC3. Chi tiết record**

- `old_value` / `new_value`: JSON diff hiển thị dạng side-by-side.
- Metadata: IP address, User-Agent, Request ID.
- Related records: Link đến đối tượng bị ảnh hưởng (nếu còn tồn tại).

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SY02-E1 | **Log > 1 triệu records** — Query tháng peak | MEDIUM | Phân trang server-side (100/trang). Elasticsearch indexed. Bắt buộc filter date range ≤ 90 ngày. |
| SY02-E2 | **Export > 100,000 records** | MEDIUM | Async export: "File đang được tạo. Email khi hoàn tất." Giới hạn 100K rows/file. |
| SY02-E3 | **Log sensitive data** — Password change, salary info | HIGH | Mask sensitive fields: `old_value: "***"`, `new_value: "***"`. Chỉ log field name đã thay đổi. |
| SY02-E4 | **Admin xóa audit log** | CRITICAL | KHÔNG cho phép. Audit log là append-only. Không có nút Delete. Retention tự động 3 năm. |

---

### **DEFINITION OF DONE (DOD)**

1. **AC Verified**: Filter, detail view, export hoạt động đúng.
2. **Performance**: Query 90 ngày trả kết quả ≤ 3 giây (indexed).
3. **Security**: Sensitive data masked. Log append-only (no delete).
4. **Retention**: Auto-purge records > 3 năm.
5. **Edge Cases Tested**: Large dataset, async export, sensitive masking.
