# US-SHIFT-02: Cấu hình giờ và ngày làm việc

---

**AS A** HR,  
**I WANT TO** thiết lập tên ca, chọn ngày làm việc, các mốc giờ làm/nghỉ và giới hạn chấm công chi tiết cho từng ca,  
**SO THAT** hệ thống có căn cứ tự động so khớp dữ liệu quét thực tế để tính toán chính xác trạng thái chuyên cần (Đúng giờ/Sớm/Trễ) và tổng giờ công.

---

### **1. BUSINESS FLOW**

1. Nhập liệu (Input): Admin điền Tên ca làm việc và chọn các ngày trong tuần (T2-CN) mà ca này áp dụng.
2. Thiết lập giờ In/Out: Chọn mốc giờ "Vào ca" và "Tan ca".
3. Cài đặt Giới hạn (Punch Logic): Quy định số giờ tối đa cho phép nhân viên Check-in sớm hoặc Check-out muộn so với khung ca chính thức.
4. Thiết lập khung Nghỉ: Chọn mốc "Bắt đầu nghỉ" và "Kết thúc nghỉ".
5. Cấu hình Hiệu lực: Chọn "Ngày bắt đầu" và "Ngày kết thúc" để giới hạn chu kỳ sống của cấu hình ca này.
6. Lưu dữ liệu: Nhấn "Tạo mới" hoặc "Cập nhật" ➔ Hệ thống lưu và bắt đầu áp dụng quy tắc chấm công mới.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Toàn bộ Form cấu hình | HR | Chỉ HR mới được chỉnh sửa các mốc giờ làm việc. |
| Toggle "Hoạt động" | HR | Thay đổi trạng thái áp dụng của ca ngay lập tức. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Nhập thông tin & Ngày làm việc**

- Tên ca: Phải là trường bắt buộc, không cho phép để trống.
- Chọn ngày:    - T2-T6 mặc định được chọn. T7, CN cho phép bật/tắt toggle cho từng ngày.
    - Dữ liệu trả về: Lưu dạng mảng (VD: [2, 3, 4, 5, 6]).

#### **AC2. Logic Cấu hình Giờ Làm & Xử lý Ca đêm**

- Vào ca / Tan ca (Check-in/Out):    - Kiểm tra định dạng thời gian (HH:MM AM/PM).
    - Logic Ca đêm: Nếu Giờ Vào Ca > Giờ Tan Ca (VD: 10:00 PM > 06:00 AM) ➔ Hệ thống tự động đánh dấu đây là ca Xuyên ngày để gán công vào ngày T.

#### **AC3. Giới hạn thời gian chấm công**

- Cho phép Check-In sớm tối đa (giờ): (Mặc định: 3 giờ).    - Nếu NV quét trước Giờ Vào Ca - 3h ➔ Hệ thống ghi nhận nhưng không tính là điểm danh hợp lệ của ca, tính là quên check-in

- Cho phép Check-out muộn tối đa (giờ): (Mặc định: 3 giờ).    - Nếu NV quét sau Giờ Tan Ca + 3h ➔ Hệ thống dừng cập nhật mốc giờ ra (Giữ mốc muộn nhất trong khung 3h), tính là quên check-out

#### **AC4. Ngày bắt đầu & Ngày kết thúc**

- Hệ thống chỉ cho phép lưu nếu Ngày bắt đầu < Ngày kết thúc.
- Ngoài khoảng thời gian này, Dashboard của nhân viên thuộc ca này sẽ Tự động ẩn thanh tiến độ 8h.

#### **AC5. Quản lý Thời gian Nghỉ**

- Bắt đầu nghỉ / Kết thúc nghỉ:    - Phải nằm trong khung thời gian Vào ca/Tan ca.
    - Hệ thống tự động tính: Thời gian làm thực tế = (Giờ Tan - Giờ Vào) - (Kết thúc nghỉ - Bắt đầu nghỉ).
    - Số phút này được hiển thị tóm tắt tại Thẻ ca.

---

### **4. DEFINITION OF DONE (DOD)**

1. Validation: Chặn lưu đơn nếu giờ nghỉ nằm ngoài khung giờ làm việc.
2. Độ đồng bộ: Mọi thay đổi trong form cấu hình phải được cập nhật ngay lập tức xuống Thẻ ca tương ứng ở cột bên trái.
3. Hủy thay đổi: Nút "Xóa thay đổi" phải reset toàn bộ form về dữ liệu ban đầu hoặc xóa trắng nếu là tạo mới.
4. QA: Kiểm thử với kịch bản ca đêm và ca gãy.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SH02-E1 | **Giờ kết thúc < Giờ bắt đầu** — VD: 22:00 - 06:00 (Ca đêm) | HIGH | Hệ thống nhận diện ca đêm (cross-midnight). Tự động set endDate = startDate + 1. Hiển thị badge "Ca đêm". |
| SH02-E2 | **Giờ trùng với ca khác** — 2 ca có overlapping time window | MEDIUM | Cảnh báo (không chặn): "Khung giờ trùng với ca [Tên ca]. NV không thể thuộc cả 2 ca cùng ngày." |
| SH02-E3 | **Ca có 0h working** — Giờ bắt đầu = Giờ kết thúc | HIGH | Validation chặn: "Tổng giờ làm phải > 0. Vui lòng kiểm tra lại khung giờ." |
| SH02-E4 | **Ngày áp dụng trong quá khứ** — HR set effective date đã qua | MEDIUM | Cảnh báo: "Ngày hiệu lực trong quá khứ. Dữ liệu chấm công lịch sử sẽ KHÔNG bị tính lại." Cho phép tiếp tục. |
