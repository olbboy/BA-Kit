# US-CAM-02: Mapping nhân viên - Camera

---

**AS A** HR Admin,  
**I WANT TO** mapping giữa personId của C-Vision và employeeId trong EAMS,  
**SO THAT** khi camera nhận diện khuôn mặt, hệ thống biết đó là nhân viên nào để ghi nhận chấm công đúng người.

---

### **1. BUSINESS FLOW**

1. **Xem danh sách mapping:** HR truy cập "Mapping nhân viên" → Bảng CVisionPersonMapping.
2. **Tạo mapping đơn lẻ:** Chọn NV từ danh sách → Nhập cvisionPersonId → Lưu.
3. **Bulk-create:** Tải template Excel → Điền cvisionPersonId + employeeCode → Upload → Validate → Tạo mapping hàng loạt.
4. **Xử lý lỗi:** Hiển thị danh sách mapping thất bại (personId không khớp, NV không tồn tại).

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| CRUD mapping | HR Admin, IT Admin | HR tạo mapping; IT hỗ trợ kỹ thuật. |
| Xem danh sách mapping | HR, Quản lý | Read-only. |
| Bulk-create | HR Admin | Chỉ HR cấp cao. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị danh sách mapping**

- Các cột: Mã NV, Họ tên, C-Vision Person ID, Trạng thái mapping (Active/Pending/Failed).
- Lọc: NV chưa mapping (hiển thị icon cảnh báo), NV đã mapping, Mapping lỗi.
- Badge: Mapped (Xanh), Unmapped (Đỏ), Pending (Vàng).

#### **AC2. Tạo mapping đơn lẻ**

- Chọn NV từ dropdown (search by tên/mã).
- Nhập cvisionPersonId (text field).
- Validate: cvisionPersonId không trùng với mapping khác.
- Sau khi lưu: NV có thể chấm công bằng Face ID ngay lập tức.

#### **AC3. Bulk-create mapping**

- Template Excel: Cột Mã NV, Cột C-Vision Person ID.
- Validate: Mã NV tồn tại, personId unique, không trùng mapping cũ.
- Kết quả: Modal hiển thị Thành công X / Thất bại Y + file lỗi.

#### **AC4. Xử lý mapping thất bại**

- Khi webhook C-Vision gửi personId chưa có mapping → Ghi vào danh sách "Chờ mapping".
- HR nhận thông báo: "X mốc chấm công chưa xác định nhân viên. Vui lòng kiểm tra mapping."
- Danh sách chờ hiển thị: personId, personName (từ C-Vision), ảnh capture, thời gian.

---

### **4. DEFINITION OF DONE (DOD)**

1. **End-to-end:** Tạo mapping → NV quẹt camera → Attendance record tạo đúng NV.
2. **Unmapped alert:** personId chưa mapping → Xuất hiện trong danh sách chờ.
3. **Bulk:** Import 500 mapping ≤ 15 giây.
4. **QA:** Kiểm thử trùng personId, NV không tồn tại, mapping cho NV multi-site.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| CM02-E1 | **NV chưa có ảnh khuôn mặt** — Mapping NV mới chưa enroll face | MEDIUM | Trạng thái mapping: PENDING_ENROLLMENT. Alert: "NV [Tên] cần chụp ảnh khuôn mặt tại bộ phận IT." |
| CM02-E2 | **1 NV map nhiều C-Vision ID** — NV enroll trên 2 device khác nhau | MEDIUM | Cho phép (multi-device). Bảng mapping hiển thị tất cả. De-dup attendance dựa trên employeeId. |
| CM02-E3 | **Bulk mapping file lỗi** — CSV chứa employeeCode không tồn tại | HIGH | Trả file lỗi kèm cột ghi chú. Không tạo mapping cho dòng lỗi. |
