# US-SHIFT-01: Danh sách ca làm việc

---

**AS A** HR,  
**I WANT TO** xem danh sách tổng hợp tất cả các ca làm việc hiện có kèm theo các thông số tóm tắt (Giờ làm, Giờ nghỉ, Số lượng nhân sự),  
**SO THAT** tôi có thể nắm bắt hiện trạng trong ≤ 2 giây tải trang phân bổ khung giờ làm việc và thực hiện các điều chỉnh (Chỉnh sửa/Xóa/Thêm mới) khi cần thiết.

---

### **1. BUSINESS FLOW**

1. Hành động: HR truy cập vào màn hình "Cấu hình ca làm việc".
2. Khởi tạo: Hệ thống truy vấn danh mục ca làm từ Database ➔ Tính toán số lượng nhân sự thực tế đang thuộc từng ca.
3. Hiển thị: Hệ thống hiển thị danh sách dạng các Thẻ nằm ở cột bên trái của giao diện chính.
4. Tương tác chi tiết: Khi HR nhấn vào một Thẻ ca bất kỳ ➔ Hệ thống tải thông tin chi tiết của ca đó lên màn hình cấu hình ở cột bên phải.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin | Role | Ghi chú |
| --- | --- | --- |
| Danh sách toàn bộ ca | HR, Quản lý cấp cao | Chỉ hiển thị các ca thuộc chi nhánh/vùng quản lý. |
| Danh sách nhân sự trong ca | HR | Chỉ HR mới xem được danh sách và avatar nhân viên chi tiết. |
| Nút "Tạo ca làm" | HR | Chỉ HR mới có quyền khởi tạo ca mới. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị thông tin Thẻ ca**

Mỗi Thẻ ca phải hiển thị đầy đủ các trường thông tin sau:

- Tên ca: Hiển thị rõ ràng (VD: Ca sáng, ca tối).
- Badge Phân loại: Hiển thị nhãn Active (Hoạt động) hoặc Inactive (Không hoạt động).
- Working Hours: Giờ bắt đầu - Giờ kết thúc (Định dạng: HH:MM AM/PM).
- Số phút nghỉ: Giờ bắt đầu - Giờ kết thúc (Định dạng: HH:MM AM/PM).
- Ảnh đại diện:    - Hiển thị tối đa 03 Avatar nhân viên đầu tiên.
    - Hiển thị số lượng nhân viên còn lại dưới dạng badge (VD: +24, +12).

#### **AC2. Logic Phân loại & Sắp xếp**

- Ưu tiên: Các ca có nhãn Hoạt động luôn được đẩy lên đầu danh sách.
- Sắp xếp: Các ca cùng loại được sắp xếp theo Thứ tự thời gian bắt đầu ca (Sớm nhất trên cùng).
- Trạng thái: Các ca ở trạng thái Hoạt động (Active) được hiển thị bình thường; các ca bị tắt Toggle Hoạt động sẽ bị làm mờ (Opacity 50%).

#### **AC3. Phản hồi Tương tác**

- Active State: Thẻ ca đang được chọn sẽ có viền màu xanh để HR biết đang cấu hình cho ca nào.
- Nút "Xem tất cả": Khi nhấn vào nút này ➔ Chuyển sang màn hình quản lý chi tiết toàn bộ ca (dạng bảng Excel) để xử lý dữ liệu lớn.
- Thời gian tải: Tốc độ hiển thị danh sách ca không được quá 1.5 giây sau khi vào trang.

#### **AC4. Advanced View**

- Link "Manage All": Khi nhấn vào, hệ thống mở giao diện liệt kê toàn bộ danh sách nhân viên của ca đó để Admin thực hiện Xóa/Thêm thủ công.

---

### **4. DEFINITION OF DONE (DOD)**

1. Dữ liệu chính xác: Số lượng nhân sự hiển thị trên Card (`+24`) phải khớp tuyệt đối với danh sách nhân viên thực tế trong Database của ca đó.
2. UI/UX: Danh sách Card phải hỗ trợ cuộn (Scroll) nếu số lượng ca vượt quá chiều cao màn hình.
3. Tương thích: Hiển thị tốt trên trình duyệt Chrome, Edge và Safari.
4. QA: Đã kiểm thử việc chuyển đổi qua lại giữa các ca mà không xảy ra hiện tượng "trôi" dữ liệu cũ từ ca này sang ca kia.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SH01-E1 | **Ca không có nhân viên** — Ca mới tạo chưa gán NV | LOW | Thẻ ca hiển thị "0 nhân viên", avatar section trống. Không ẩn thẻ. |
| SH01-E2 | **Số lượng ca > 50** — Doanh nghiệp lớn có nhiều ca | MEDIUM | Danh sách hỗ trợ virtual scroll, lazy load mỗi batch 20 thẻ. Search bar cho phép tìm theo tên ca. |
| SH01-E3 | **Ca bị xóa khi đang có NV** — HR xóa ca có 100 NV đang active | HIGH | Chặn xóa. Hiển thị: "Không thể xóa ca đang có [N] nhân viên. Vui lòng chuyển NV sang ca khác trước." |
| SH01-E4 | **Concurrent edit** — 2 HR cùng sửa 1 ca | MEDIUM | Optimistic locking: HR sửa sau nhận cảnh báo "Ca đã được cập nhật bởi [Tên HR]. Vui lòng tải lại." |
