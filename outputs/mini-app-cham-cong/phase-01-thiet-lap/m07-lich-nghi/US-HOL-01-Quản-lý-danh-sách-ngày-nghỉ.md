# US-HOL-01: Quản lý danh sách ngày nghỉ

---

**AS A** HR Admin,  
**I WANT TO** thiết lập và quản lý danh sách các ngày nghỉ lễ chính thức và nội bộ của công ty,  
**SO THAT** hệ thống có căn cứ để tự động tính công "Hợp lệ" cho nhân viên mà họ không cần phải chấm công vào những ngày này.

---

### **1. BUSINESS FLOW**

1. **Xem tổng quan (Read)**: Admin truy cập màn hình Cấu hình Lịch, hệ thống tự hiển thị Lịch 12 tháng của năm hiện tại.
2. **Khởi tạo Holiday (Create)**:    - Admin nhấn vào 1 ngày trên Calendar HOẶC nhấn nút  **"Thêm ngày nghỉ tùy chỉnh"** 
    - Nhập các thông tin: Tên lễ (VD: Tết Nguyên Đán), Loại (Quốc gia/Nội bộ), Khoảng ngày (Start/End).
    - Hệ thống Validate xem có bị trùng lặp với lịch cũ hay không.

3. **Chỉnh sửa (Update)**: Admin nhấn vào một Card lễ trong danh sách bên cạnh ➔ Chỉnh sửa thông tin ➔ Lưu.
4. **Xóa (Delete)**: Cho phép xóa các ngày nghỉ nội bộ hoặc ngày nghỉ tùy chỉnh (Hệ thống cảnh báo trước khi xóa).
5. **Thiết lập khác**:    - **Nghỉ sinh nhật:** Gạt Toggle [BẬT] ➔ Áp dụng luật cộng 1 ngày công/tháng sinh nhật (Lưu ý: Chỉ áp dụng cho NV chính thức).
    - **Nghỉ thiên tai:** Quản lý bật chế độ khẩn cấp và nhấn **"Thiết lập vùng ảnh hưởng"** để gán cho các tỉnh/thành cụ thể.
    - **Đăng ký WFH:** Thiết lập hạn mức mặc định (VD: 02 ngày/tuần).

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Danh sách ngày nghỉ lễ | HR Admin, IT Admin, Manager | Manager chỉ có quyền View. |
| Thao tác Thêm/Sửa/Xóa | HR Admin | Chỉ Admin cấp cao mới được quyền sửa lịch lễ của công ty. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị Calendar & Badge**

- Hiển thị đúng ngày lễ theo mã màu: **Lễ Quốc gia (Đỏ)**, **Lễ Công ty (Xanh biển)**.
- Khi có sự kiện trùng ngày, hiển thị Badge nhỏ mô tả tên ngày lễ ngay trên ô ngày của Calendar (VD: mốc 01/05, mốc 19/05).

#### **AC2. Quản lý Card List (Lịch lễ)**

- Mỗi thẻ lễ phải hiển thị: Tên lễ, Khoảng ngày & Tổng số ngày nghỉ thực tế.
- Nút "Ba chấm" trên từng thẻ cho phép: Sửa hoặc Xóa lịch lễ tùy chỉnh.

#### **AC3. Logic tham số Chế độ (Side Widgets)**

- **Nghỉ sinh nhật:** Phải thỏa mãn điều kiện **Nhân viên chính thức **mới được hệ thống tự động cộng công.
- **Thiết lập vùng ảnh hưởng:** Khi nhấn nút, mở ra danh sách Tỉnh/Thành để Admin check chọn (multi-select checkbox) khu vực được nghỉ bão/lụt.
- **Hạn mức WFH:** Badge hiển thị đúng con số hiện tại đã cấu hình (02 ngày/tuần).

#### **AC4. Logic Tự động gán Công (Auto-Attendance Logic)**

Đây là phần nghiệp vụ cốt lõi quan trọng:

- Bất kỳ nhân viên nào có ngày sinh hoặc lịch ca trùng với `sh_holiday_config` ➔ Trạng thái chấm công tự động chuyển thành **"HỢP LỆ/HƯỞNG LƯƠNG"** vào lúc 0:01 sáng ngày hôm đó.
- Hệ thống KHÔNG được hiển thị lỗi "Quên quẹt thẻ" (Anomaly) vào các ngày này.

#### **AC5. Ràng buộc dữ liệu (Validation Rules)**

- Tên ngày lễ không được để trống (Max 100 ký tự).
- Không được gán 2 ngày lễ chồng lấn (Overlap) lên nhau trên cùng một lịch làm việc.

---

### **4. DEFINITION OF DONE (DOD)**

1. **UI/UX**: Giao diện hiển thị đúng 100% trên cả trình duyệt Web và giao diện xem trên Mini App (Read-only).
2. **API**: Cung cấp đầy đủ các API CRUD cho bảng `sh_holiday_config`.
3. **Dữ liệu (Database)**: Các mốc ngày nghỉ được lưu trữ chính xác, truy vấn theo năm ≤ 0.5 giây (indexed by year).
4. **Kiểm thử (QA)**: Đã kiểm thử trường hợp gán nghỉ Tết ➔ Nhân viên không quẹt thẻ ➔ Dashboard vẫn báo 8h công "Hợp lệ".

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| HL01-E1 | **Ngày nghỉ trùng cuối tuần** — VD: 30/4 rơi vào Chủ nhật | MEDIUM | HR quyết định: (A) Nghỉ bù T2, (B) Không nghỉ bù. Hệ thống hiển thị cảnh báo khi tạo. |
| HL01-E2 | **Xóa ngày nghỉ đã có đơn nghỉ phép** — NV đã approved leave trùng ngày | HIGH | Chặn xóa. Hiển thị: "[N] đơn nghỉ phép đã approved trùng ngày này. Hủy đơn trước khi xóa." |
| HL01-E3 | **Ngày nghỉ thiên tai — scope vùng** — Chỉ áp dụng 1 số tỉnh | MEDIUM | Chọn scope: Toàn quốc / Tỉnh cụ thể. Chỉ NV có Primary Site tại tỉnh đó mới bị ảnh hưởng. |
