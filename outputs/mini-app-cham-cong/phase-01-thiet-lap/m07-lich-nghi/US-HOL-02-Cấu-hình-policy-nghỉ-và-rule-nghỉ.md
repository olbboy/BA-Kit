# US-HOL-02: Cấu hình policy nghỉ và rule nghỉ

---

**AS A** HR Admin,  
**I WANT TO** cấu hình các tham số luật cho các chế độ đãi ngộ đặc thù,  
**SO THAT** hệ thống tự động hóa được việc gán ngày nghỉ/WFH và ứng phó khẩn cấp mà không cần can thiệp thủ công.

---

### **1. BUSINESS FLOW**

1. **Cấu hình Ngày nghỉ Sinh nhật**:    - Admin thực hiện gạt Toggle [BẬT/TẮT] ➔ Hệ thống lưu trạng thái tham số.
    - Hiển thị điều kiện ràng buộc: Chỉ áp dụng cho Nhân viên chính thức.

2. **Cấu hình Chế độ Nghỉ thiên tai**:    - Kích hoạt chế độ khẩn cấp (Toggle).
    - Nhấn **"Thiết lập vùng ảnh hưởng"** ➔ Hệ thống mở danh mục Tỉnh/Thành ➔ Admin chọn vùng chịu ảnh hưởng ➔ Lưu.

3. **Cấu hình Hạn mức WFH**:    - Thiết lập số ngày tối đa được phép làm việc từ xa (VD: 02 ngày/tuần).

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Chức năng | Role | Ghi chú |
| --- | --- | --- |
| Bật/Tắt chế độ Nghỉ sinh nhật | HR Admin | Áp dụng toàn công ty. |
| Kích hoạt Chế độ Thiên tai | HR Manager | Chỉ quản lý cấp cao mới được phép kích hoạt khẩn cấp. |
| Thiết lập vùng ảnh hưởng | HR Admin | Áp dụng theo danh mục Văn phòng/Location. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Quản lý Toggle & Trạng thái Widget**

- Mỗi Card cấu hình bên phải phải hiển thị rõ trạng thái: **Xanh (Bật / Active)**, **Xám (Tắt / Inactive)**.
- Trình tự gạt Toggle phải mượt mà và gửi dữ liệu cập nhật về Backend ngay lập tức.

#### **AC2. Logic Ràng buộc nghỉ sinh nhật**

- Hệ thống chỉ được phép cộng công tự động cho nhân sự chính thức kể từ ngày tính toán.

#### **AC3. Cấu hình Vùng địa lý**

- Modal chọn vùng ảnh hưởng phải liệt kê đầy đủ 36 Tỉnh/Thành của Việt Nam.
- Khi Admin nhấn lưu ➔ Toàn bộ nhân viên có Office Location thuộc tỉnh đó sẽ được hệ thống gán trạng thái nghỉ tự động.

---

### **4. DEFINITION OF DONE (DOD)**

1. **Dữ liệu chính xác:** Khi gạt Toggle, giá trị trong Database phải thay đổi tương ứng ngay lập tức.
2. **Audit Log:** Mọi hành động Bật/Tắt hoặc thay đổi hạn mức phải được ghi vết cho mục đích hậu kiểm.
3. **Hiệu năng:** API lưu trữ phải phản hồi trong thời gian dưới 0.3s.
4. **UX Dashboard:** Trạng thái gạt nút phải đồng bộ hiển thị chính xác cho toàn bộ User Admin cùng lúc.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| HL02-E1 | **Policy trùng date range** — 2 policy nghỉ lễ cùng ngày cho cùng site | HIGH | Chặn: "Đã tồn tại policy nghỉ cho ngày [DD/MM] tại [Site]. Vui lòng chỉnh sửa policy hiện có." |
| HL02-E2 | **Rule nghỉ circular** — Rule A tham chiếu Rule B, Rule B tham chiếu Rule A | HIGH | Validation: phát hiện circular reference. Chặn lưu kèm message rõ ràng. |
| HL02-E3 | **Policy áp dụng retroactive** — Tạo policy cho ngày đã qua | MEDIUM | Cảnh báo: "Policy áp dụng cho ngày trong quá khứ. Dữ liệu chấm công lịch sử sẽ được tính lại." Yêu cầu xác nhận. |
