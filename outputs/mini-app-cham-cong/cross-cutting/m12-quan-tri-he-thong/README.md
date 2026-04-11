# 2.11.12. Quản trị hệ thống

---

| Thông tin | Nội dung |
| --- | --- |
| Target release | Version 1.0 (Sprint 10+) |
| Epic | STRATOS-ADMIN: Quản trị hệ thống tập trung |
| Document owner | BA Team |
| Stakeholder | System Admin, GLOBAL_HR, Super Admin |
| Status | Draft |
| Tham chiếu | EAMS v2.0 §11 (Ma trận quyền hạn), §12 (Cross-Module Policies) |

---

### **1. MỤC TIÊU**

- **Lý do tồn tại:** Hệ thống EAMS multi-tenant multi-site cần giao diện quản trị để cấu hình chi nhánh, xem audit log, và xử lý quy trình offboarding nhân viên.
- **Bài toán:** Cung cấp bộ công cụ quản trị cho System Admin và HR để vận hành hệ thống an toàn, tuân thủ, và có thể truy vết.
- **Giá trị mang lại:** Giảm rủi ro vận hành; đảm bảo compliance; rút ngắn thời gian xử lý offboarding từ 2 ngày xuống 30 phút.

---

### **2. MÔ TẢ QUY TRÌNH NGHIỆP VỤ**

```
System Admin / GLOBAL_HR
├── Quản lý chi nhánh (CRUD site)
│   └── Thêm / Sửa / Xóa / Deactivate site
├── Audit Log
│   └── Xem toàn bộ hoạt động hệ thống theo bộ lọc
└── Employee Offboarding
    └── Trigger workflow khi NV nghỉ việc → auto-cancel đơn, freeze phép, deactivate mapping
```

---

### **3. NHU CẦU NGƯỜI DÙNG**

| Persona | Nhu cầu cụ thể | Tài liệu / Căn cứ |
| --- | --- | --- |
| System Admin | Cần thêm chi nhánh mới khi công ty mở rộng, không cần dev can thiệp. | EAMS §11.1 |
| System Admin | Cần xem ai đã thay đổi dữ liệu gì, khi nào, để điều tra sự cố. | EAMS §12.2 |
| HR Admin | Cần quy trình offboarding tự động để không bỏ sót bước nào khi NV nghỉ việc. | EAMS §12.1 |

---

### **4. PHẠM VI CHỨC NĂNG**

| Mã | Chức năng | Mô tả chi tiết | User Story |
| --- | --- | --- | --- |
| F12.1 | Quản lý chi nhánh | CRUD site: Tên, mã, địa chỉ, timezone, trạng thái. Deactivate site (soft-delete). | [US-SYS-01](./US-SYS-01-Quản-lý-chi-nhánh.md) |
| F12.2 | Audit Log Viewer | Xem log hoạt động: filter theo user, module, action, time range. Export CSV. | [US-SYS-02](./US-SYS-02-Audit-log-viewer.md) |
| F12.3 | Employee Offboarding | Workflow tự động khi NV nghỉ việc: cancel đơn, freeze phép, deactivate mapping, re-route approval. | [US-SYS-03](./US-SYS-03-Employee-offboarding.md) |
| F12.4 | Chốt công tháng (Period Closing) | Cấu hình closingDay, graceDays, weekendRule per-site. Auto-lock kỳ. Exception unlock với audit trail. | [US-SYS-04](./US-SYS-04-Chốt-công-tháng.md) |
| F12.5 | Employee Onboarding Wizard | Quy trình 7 bước: profile → site → shift → Face ID → phép → approval chain → welcome. Hỗ trợ bulk. | [US-SYS-05](./US-SYS-05-Employee-onboarding.md) |

---

### **5. YÊU CẦU PHI CHỨC NĂNG**

- **Bảo mật:** Chỉ SYSTEM_ADMIN và SUPER_ADMIN truy cập được module này (trừ Offboarding: GLOBAL_HR có quyền).
- **Audit Log retention:** 3 năm (theo quy định nội bộ).
- **Offboarding SLA:** Toàn bộ workflow hoàn thành ≤ 5 phút sau khi trigger.

---

### **EDGE CASES & ERROR HANDLING (toàn module)**

| # | US | Case | Severity | Expected Behavior |
|---|-----|------|----------|-------------------|
| SY01-E1 | SYS-01 | **Xóa site có NV active** | CRITICAL | Chặn: "Site có [N] NV active. Chuyển NV trước khi deactivate." |
| SY02-E1 | SYS-02 | **Audit log > 1M records** | MEDIUM | Phân trang server-side (100/trang). Search indexed (Elasticsearch). Filter bắt buộc time range ≤ 90 ngày. |
| SY03-E1 | SYS-03 | **Offboarding NV đang có đơn APPROVED** — Leave approved cho tuần sau | HIGH | Auto-cancel leave request. Hoàn phép về balance. Push NV: "Đơn nghỉ phép đã bị hủy do quy trình nghỉ việc." |

---

### **6. ĐIỀU KIỆN GIẢ ĐỊNH**

1. Người dùng đã đăng nhập với role SYSTEM_ADMIN hoặc SUPER_ADMIN.
2. Hệ thống audit log đã được bật (config: `audit.enabled = true`).
3. Quy trình offboarding do HR trigger thủ công (không auto-trigger khi NV bị xóa).
