# BRD Quản lý (Manager & Trưởng phòng)

---

| Thông tin | Nội dung |
| --- | --- |
| Target release | Version 1.0 |
| Epic | STRATOS-MGR: Quản lý duyệt đơn & giám sát team |
| Document owner | BA Team |
| Stakeholder | Manager, Trưởng phòng (DEPT_HEAD), Ban Giám đốc |
| Status | Open |

---

### **1. MỤC TIÊU**

- **Lý do tồn tại:** Quản lý cần công cụ duyệt đơn nhanh, giám sát chuyên cần team, và xem báo cáo phòng ban trên mobile.
- **Bài toán:** Thay thế quy trình duyệt đơn giấy/email, cung cấp dashboard team real-time, cảnh báo vi phạm kịp thời.
- **Giá trị mang lại:** Giảm 70% thời gian duyệt đơn; tăng khả năng giám sát team từ xa.

---

### **2. PHẠM VI VAI TRÒ**

| Vai trò | Scope | Khác biệt |
| --- | --- | --- |
| MANAGER | Team trực thuộc (employee.managerId = self) | Duyệt cấp 1, xem data team |
| DEPT_HEAD | Toàn phòng ban | Duyệt cấp 2, xem data phòng |
| SITE_MANAGER | Toàn chi nhánh | Xem báo cáo site, fallback approval |

---

### **3. PHẠM VI CHỨC NĂNG**

| Mã | Chức năng | Mô tả | Module | User Story |
| --- | --- | --- | --- | --- |
| MF01 | Dashboard team | Xem chuyên cần team: Có mặt / Trễ / Vắng / Nghỉ phép. Biểu đồ xu hướng 7/30 ngày. | m01, m11 | US-ATTEN-02, US-RPT-01 |
| MF02 | Inbox phê duyệt | Danh sách đơn chờ duyệt (Nghỉ/OT/Giải trình/Đổi ca). Badge số lượng. Xem chi tiết + duyệt/từ chối kèm lý do. | m10 | US-APPR-01 |
| MF03 | Phê duyệt hàng loạt | Chọn nhiều đơn cùng loại → duyệt/từ chối batch (tối đa 50). | m10 | US-APPR-03 |
| MF04 | Xem chấm công team | Xem nhật ký chấm công của NV thuộc team. Ảnh Face ID, mốc In/Out. | m01 | US-ATTEN-03 |
| MF05 | Cảnh báo team | Xem danh sách vi phạm của NV trong team: muộn, sớm, vắng. Nhắc NV giải trình. | m01 | US-ATTEN-04 |
| MF06 | Báo cáo phòng ban | Biểu đồ chuyên cần theo phòng ban. Top NV vi phạm. Không xuất payroll (chỉ HR). | m11 | US-RPT-01 |
| MF07 | Delegation khi nghỉ | Khi Manager đi nghỉ → hệ thống tự chuyển đơn sang SITE_MANAGER hoặc SITE_HR (fallback chain). | m10 | US-APPR-02 |
| MF08 | Xem đơn Công tác/WFH team | Xem request công tác hoặc WFH của NV thuộc team. Duyệt/từ chối kèm lý do. | m02 | US-REG-06 |

---

### **4. YÊU CẦU PHI CHỨC NĂNG**

- Giao diện web + mobile Mini App.
- Duyệt đơn trong 2 tap trên mobile (xem → duyệt/từ chối).
- Push notification khi có đơn mới cần duyệt.
- RBAC: Manager chỉ thấy NV team mình; DEPT_HEAD thấy toàn phòng.

---

### **5. ĐIỀU KIỆN GIẢ ĐỊNH**

1. Cấu hình tổ chức đã thiết lập (Manager → NV relationship) qua Module 05.
2. Cấu hình chuỗi phê duyệt đã được HR thiết lập qua Module 10.
3. NV đã gửi đơn qua Module 04 (Đăng ký) hoặc Module 03 (Giải trình).
