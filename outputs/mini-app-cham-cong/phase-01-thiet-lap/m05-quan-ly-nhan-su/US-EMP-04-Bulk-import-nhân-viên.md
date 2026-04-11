# US-EMP-04: Bulk Import nhân viên

---

**AS A** HR Admin,  
**I WANT TO** import danh sách nhân viên mới từ file Excel mẫu vào hệ thống,  
**SO THAT** tôi có thể onboard hàng trăm nhân viên khi mở chi nhánh mới mà không nhập thủ công từng người.

---

### **1. BUSINESS FLOW**

1. **Tải template:** HR nhấn "Tải file mẫu" → Hệ thống trả file .xlsx chuẩn.
2. **Nhập liệu:** HR điền thông tin NV vào file (Mã NV, Họ tên, Email, Phòng ban, Cấp bậc, Ngày sinh, Ngày vào làm).
3. **Upload:** HR nhấn "Import nhân viên" → Chọn file → Upload.
4. **Validate:** Hệ thống kiểm tra:
   - Mã NV unique (không trùng trong DB).
   - Email unique.
   - Phòng ban tồn tại trong hệ thống.
   - Định dạng ngày tháng hợp lệ.
5. **Kết quả:** Hiển thị modal: Thành công X / Thất bại Y. Trả file lỗi kèm cột ghi chú lý do.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Nút "Import nhân viên" | HR Admin | Chỉ HR có quyền import. |
| File Excel danh sách | HR Admin | SITE_HR chỉ import NV vào site mình. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. File mẫu (Template)**

- Các cột: Mã NV (*), Họ tên (*), Email (*), Phòng ban (*), Cấp bậc, Ngày sinh, Ngày vào làm, Chi nhánh, Ghi chú.
- (*) = bắt buộc.
- Sheet hướng dẫn: Giải thích từng cột + ví dụ mẫu.

#### **AC2. Validation Rules**

| Case | Lỗi | Ghi chú cột lỗi |
| --- | --- | --- |
| Mã NV trùng trong DB | Bỏ qua (Skip) | "Mã nhân viên đã tồn tại" |
| Mã NV trùng trong file | Lấy dòng đầu tiên | "Mã nhân viên trùng lặp trong file (dòng X)" |
| Email trùng | Lỗi | "Email đã tồn tại trong hệ thống" |
| Phòng ban không tồn tại | Lỗi | "Phòng ban [X] không tồn tại" |
| Email sai định dạng | Lỗi | "Định dạng email không hợp lệ" |
| Thiếu trường bắt buộc | Lỗi | "Thiếu [tên cột]" |

#### **AC3. Kết quả Import**

- Modal hiển thị:
  - Tổng bản ghi: Z
  - Thành công: X (Xanh)
  - Thất bại: Y (Đỏ)
- Nút "Tải file lỗi": File Excel chỉ chứa các dòng lỗi + cột "Lý do lỗi".
- Sau import thành công: Danh sách NV (US-EMP-03) cập nhật ngay.

#### **AC4. Giới hạn**

- Tối đa 5,000 bản ghi/lần import.
- Thời gian xử lý ≤ 30 giây.
- File > 5,000 dòng → Hiển thị lỗi "Vượt giới hạn, vui lòng chia nhỏ file".

---

### **4. DEFINITION OF DONE (DOD)**

1. **Dữ liệu:** Sau import, NV mới xuất hiện đúng trong danh sách và sơ đồ tổ chức.
2. **File lỗi:** Kiểm thử file có 50% lỗi → File trả về chỉ chứa dòng lỗi + lý do.
3. **Hiệu năng:** Import 5,000 NV ≤ 30 giây, không timeout.
4. **QA:** Kiểm thử file rỗng, file sai format (.csv, .doc), file unicode tiếng Việt.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM04-E1 | **Email trùng** — Import 2 NV cùng email | HIGH | Mark lỗi: "Email [X] đã tồn tại (NV: [Mã NV cũ])." Không import dòng trùng. |
| EM04-E2 | **Phòng ban không tồn tại** — File Excel chứa tên phòng ban sai | HIGH | Mark lỗi: "Phòng ban '[X]' không tồn tại. Tạo phòng ban trước hoặc sửa file." |
| EM04-E3 | **File > 5000 dòng** | MEDIUM | Chặn: "File vượt 5,000 bản ghi. Vui lòng chia nhỏ." |
| EM04-E4 | **Upload giữa chừng mất mạng** — Processed 2000/5000 dòng | HIGH | Transaction toàn file: rollback toàn bộ nếu lỗi giữa chừng. Hoặc: partial commit kèm report "2000 thành công, 3000 chưa xử lý." |
