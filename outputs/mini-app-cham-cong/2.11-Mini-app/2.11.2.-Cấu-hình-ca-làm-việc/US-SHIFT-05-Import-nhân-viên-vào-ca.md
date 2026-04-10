# US-SHIFT-05: Import nhân viên vào ca

---

**AS A** HR,  
**I WANT TO** tải tệp Excel danh sách nhân viên và tải lên hệ thống để gán vào ca làm việc hiện tại hàng loạt,  
**SO THAT** tôi có thể triển khai lịch phân ca cho quy mô nhân sự lớn trong ≤ 30 giây cho 500 bản ghi và chính xác (0 sai sót format), tránh sai sót khi nhập liệu thủ công từng người.

---

### **1. BUSINESS FLOW**

1. Chuẩn bị: HR tải Template từ hệ thống về máy tính.
2. Nhập liệu: HR điền danh sách Mã nhân viên cần gán vào ca vào file Excel.
3. Tải lên: Tại màn hình Cấu hình ca, HR nhấn nút "Import nhân viên" ➔ Chọn file đã chuẩn bị.
4. Xử lý: Hệ thống đọc file ➔ Kiểm tra tính hợp lệ của Mã nhân viên (ID) ➔ Kiểm tra xung đột lịch làm việc của từng người.
5. Hoàn tất: Hệ thống thông báo kết quả (Số lượng thành công / Số lượng thất bại) và cập nhật danh sách Avatar tại Thẻ ca.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| File Excel danh sách nhân sự | HR | Có quyền đọc/ghi dữ liệu nhân sự của phòng ban được giao. |
| Nút "Import nhân viên" | HR | Chỉ hiển thị với Role HR. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Cung cấp File mẫu (Template Download)**

- Hệ thống phải cung cấp liên kết "Tải file mẫu" định dạng .xlsx.
- File mẫu bao gồm các cột bắt buộc: Mã nhân viên (Employee_ID), Tên nhân viên (Chỉ xem), Phòng ban (Chỉ xem), Ca làm việc (ID ca), Ghi chú.

#### **AC2. Quy tắc Kiểm tra Hợp lệ (Validation Rules)**

Khi HR tải file lên, hệ thống phải thực hiện Check-sum:

- **Case 1 (Mã NV không tồn tại)**: Mã nhân viên không có trong Module 05 ➔ Trả file excel lọc case lỗi và hiển thị lỗi ở cột ghi chú: Mã nhân viên không tồn tại
- **Case 2 (Nhân viên trùng ca)**: Nhân viên đã được gán vào ca này trước đó ➔ Giữ nguyên (Skip) hoặc Cập nhật (Update) mốc thời gian áp dụng hiện tại.
- **Case 3 (Nhân viên trùng khung giờ ca khác)**: Nhân viên đang ở ca khác có khung giờ chồng lấn (VD: Đã ở ca Hành chính, không thể gán vào ca Sáng cùng giờ) ➔ Trả file excel lọc case lỗi và hiển thị lỗi ở cột ghi chú: "Xung đột lịch ca kíp".

#### **AC3. Phản hồi Kết quả Import (Batch Result Feedback)**

Hệ thống hiển thị Modal thông báo kết quả chi tiết:

- Số bản ghi thành công: [X]
- Số bản ghi thất bại: [Y]
- Danh sách lỗi: Hiển thị rõ dòng Excel nào bị lỗi và nguyên nhân ở cột ghi chú.

#### **AC4. Đồng bộ Dữ liệu (Real-time Sync)**

- Sau khi Import thành công, danh sách nhân sự tham gia ca trên thẻ ca phải được cập nhật ngay lập tức mà không cần F5 (Làm mới trang).

---

### **4. DEFINITION OF DONE (DOD)**

1. **Dung lượng**: Hệ thống hỗ trợ xử lý file Excel lên đến 5,000 bản ghi/lần Import mà không bị đơ trình duyệt.
2. **Độ chính xác**: Kiểm thử với dữ liệu thực ➔ Sau khi Import, nhân viên A mở App phải thấy ngay cấu hình Ca làm việc mới trong Nhật ký (Module 01).
3. **UI/UX**: Modal hiển thị kết quả Import phải rành mạch, dễ hiểu cho người dùng Non-tech.
4. **QA**: Xác nhận 100% nhân viên trong file Import được gán đúng ID Ca (Shift_ID) vào Database.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SH05-E1 | **File Excel lỗi format** — Cột thiếu, data type sai | HIGH | Trả file lỗi kèm cột "Lý do lỗi" cho mỗi dòng. Không import dòng lỗi. Hiển thị: "X/Y bản ghi thành công, Z lỗi." |
| SH05-E2 | **NV đã thuộc ca khác** — Import NV đang active ở ca cũ | MEDIUM | Cảnh báo: "[N] NV đang thuộc ca khác. Chọn: (A) Chuyển sang ca mới, (B) Bỏ qua, (C) Thêm ca phụ." |
| SH05-E3 | **Mã NV không tồn tại** — File chứa mã NV không có trong hệ thống | HIGH | Mark as ERROR. Ghi nhận vào file kết quả: "Mã NV [X] không tồn tại trong hệ thống." |
| SH05-E4 | **Import file > 5000 dòng** — Vượt giới hạn batch | MEDIUM | Hiển thị: "File vượt quá 5,000 bản ghi. Vui lòng chia nhỏ file." Chặn upload. |
| SH05-E5 | **Duplicate trong file** — Cùng 1 mã NV xuất hiện 2 lần | MEDIUM | Lấy dòng cuối cùng (last-write-wins). Log warning: "Mã NV [X] bị trùng tại dòng [A] và [B], lấy dòng [B]." |
