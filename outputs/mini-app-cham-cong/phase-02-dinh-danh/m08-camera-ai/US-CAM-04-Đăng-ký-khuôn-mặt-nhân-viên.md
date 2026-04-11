# US-CAM-04: Đăng ký khuôn mặt nhân viên (Face ID Enrollment)

---

**AS A** Nhân viên mới,  
**I WANT TO** tự đăng ký khuôn mặt cho hệ thống chấm công AI thông qua quy trình 3 bước trên Mini App,  
**SO THAT** tôi có thể chấm công bằng nhận diện khuôn mặt ngay từ ngày đầu đi làm mà không cần nhờ bộ phận IT.

---

### **1. BUSINESS FLOW**

1. **Bước 1 — Xác nhận thông tin cá nhân:** NV xác nhận Họ tên, Mã NV, Phòng ban, Email (dữ liệu tự lấy từ hệ thống, NV chỉ verify).
2. **Bước 2 — Chụp ảnh khuôn mặt:** NV sử dụng camera điện thoại chụp ảnh chân dung theo hướng dẫn (góc thẳng, ánh sáng đủ, không đeo kính đen). Hệ thống kiểm tra chất lượng ảnh tự động.
3. **Bước 3 — Đồng bộ C-Vision:** Hệ thống gửi ảnh sang C-Vision API để tạo personId mới. Khi thành công → tự động tạo CVisionPersonMapping (personId ↔ employeeId). NV nhận thông báo "Đăng ký thành công — bạn có thể chấm công bằng Face ID".
4. **Kích hoạt:** Sau khi mapping active, mốc quẹt tiếp theo từ camera sẽ được ghi nhận cho NV.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Khởi tạo đăng ký Face ID | Nhân viên | Chỉ đăng ký cho chính mình. |
| Phê duyệt đăng ký | HR Admin | HR xác nhận danh tính trước khi kích hoạt (tùy cấu hình). |
| Xem trạng thái enrollment | Nhân viên, HR | NV xem của mình; HR xem toàn bộ NV chưa đăng ký. |
| Xóa / Re-enroll Face ID | HR Admin | Khi NV cần chụp lại (thay đổi ngoại hình). |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Bước 1 — Xác nhận thông tin**

- Hiển thị: Họ tên, Mã NV, Phòng ban, Chi nhánh, Email (read-only từ hệ thống).
- NV nhấn "Xác nhận" để tiếp tục. Nếu thông tin sai → hiển thị "Liên hệ HR để cập nhật".
- Chặn nếu NV đã đăng ký Face ID (status = ENROLLED): "Bạn đã đăng ký. Liên hệ HR để đăng ký lại".

#### **AC2. Bước 2 — Chụp ảnh khuôn mặt**

- Mở camera trước (front-facing) của điện thoại.
- Hiển thị khung oval hướng dẫn vị trí khuôn mặt.
- Kiểm tra chất lượng tự động:
  - Phát hiện khuôn mặt trong khung (face detection).
  - Ánh sáng đủ (không quá tối hoặc quá sáng).
  - Không bị che (khẩu trang, kính đen → cảnh báo).
  - Góc thẳng (không nghiêng quá 15°).
- Nếu không đạt → hiển thị gợi ý cụ thể: "Vui lòng tháo khẩu trang" / "Ánh sáng không đủ".
- Cho phép chụp lại (tối đa 5 lần/phiên).

#### **AC3. Bước 3 — Đồng bộ C-Vision**

- Gửi ảnh đến C-Vision API (endpoint: POST /persons).
- Chờ phản hồi (timeout: 30 giây). Hiển thị progress indicator.
- Thành công → tạo CVisionPersonMapping + hiển thị "Đăng ký thành công".
- Thất bại → hiển thị lỗi cụ thể: "Không thể đồng bộ. Vui lòng thử lại sau".
- Thời gian đồng bộ: ảnh từ App đến C-Vision nhận diện được trong 60 giây.

#### **AC4. Trạng thái Enrollment**

| Trạng thái | Mô tả |
| --- | --- |
| NOT_ENROLLED | NV chưa đăng ký. Hiển thị nút "Đăng ký Face ID". |
| PENDING | Ảnh đã gửi, đang chờ C-Vision xử lý. |
| ENROLLED | Đăng ký thành công. NV có thể chấm công Face ID. |
| FAILED | Đăng ký thất bại. Cho phép thử lại. |
| RE_ENROLLMENT | HR yêu cầu đăng ký lại (thay đổi ngoại hình). |

---

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| CAM04-E1 | **C-Vision API timeout** — Không phản hồi trong 30 giây | HIGH | Retry tự động 1 lần. Nếu vẫn fail → "Hệ thống đang bận. Thử lại sau 5 phút." Lưu ảnh local để retry. |
| CAM04-E2 | **Ảnh trùng với NV khác** — C-Vision phát hiện khuôn mặt đã đăng ký | CRITICAL | Chặn đăng ký. Alert HR: "Khuôn mặt trùng với NV [Mã]. Kiểm tra danh tính." Không tạo mapping. |
| CAM04-E3 | **NV thay đổi ngoại hình** — Giảm cân, để râu, phẫu thuật | MEDIUM | HR trigger re-enrollment. NV nhận push: "HR yêu cầu cập nhật ảnh Face ID." Wizard mở lại từ Bước 2. Mapping cũ deactivate, tạo mapping mới. |
| CAM04-E4 | **Nhiều NV đăng ký đồng thời** — Ngày onboard 200 NV mới | MEDIUM | Queue-based: C-Vision API rate limit 10 request/phút. Hiển thị "Đang trong hàng đợi. Vị trí: X/200." NV không cần đợi — nhận push khi xong. |

---

### **4. DEFINITION OF DONE (DOD)**

1. **End-to-end:** NV mới đăng ký Face ID → ra cổng quẹt camera → AttendanceRecord tạo đúng.
2. **Chất lượng ảnh:** Kiểm thử trong điều kiện ánh sáng kém, góc nghiêng, có khẩu trang → cảnh báo đúng.
3. **Bảo mật:** Ảnh khuôn mặt truyền qua HTTPS. Lưu trữ theo Data Retention Policy (90 ngày).
4. **QA:** Kiểm thử: enrollment thành công, API timeout, ảnh trùng, re-enrollment, onboard hàng loạt.
