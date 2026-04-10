# US-ATTEN-02: Thống kê hiệu suất tháng

---

**AS A** Nhân viên,  
**I WANT TO** xem các thẻ thống kê tóm tắt về tỷ lệ đúng giờ, số ngày nghỉ và giờ tăng ca lũy kế trong tháng hiện tại,  
**SO THAT** tôi có thể tự đánh giá hiệu suất chuyên cần và chủ động theo dõi quỹ lương/phép dự kiến mà không cần hỏi bộ phận Nhân sự.

---

### **1. BUSINESS FLOW**

1. Truy cập: Người dùng mở Web Mini App ➔ Hệ thống tự động lấy mốc Tháng hiện tại.
2. Khởi tạo dữ liệu: Backend thực hiện quét toàn bộ nhật ký từ ngày 01 đến ngày hiện tại của nhân viên ➔ Tính toán 03 chỉ số (Đúng giờ, Ngày nghỉ, Tăng ca).
3. Hiển thị: Dữ liệu được đẩy về giao diện và hiển thị tại khối 03 thẻ thống kê nằm ngay dưới Hub Chấm công.
4. Cập nhật: Dữ liệu tự động làm mới mỗi khi nhân viên thực hiện thao tác quẹt camera hoặc có đơn từ được duyệt.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Tỷ lệ Đúng giờ (%) | Nhân viên, HR, Quản lý | ABAC: Chỉ hiển thị dữ liệu thuộc User_ID đang đăng nhập. |
| Tổng số ngày nghỉ | Nhân viên, HR, Quản lý | Lấy từ Status = Approved của Module Đơn từ. |
| Giờ Tăng ca (OT) | Nhân viên, HR, Quản lý | Chỉ tính các mốc quẹt ngoài giờ ca chính thức. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **3.1. Thẻ "Đúng giờ (%)"**

- Công thức: Tỷ lệ = (Tổng số ngày đi làm đúng giờ / Tổng số ngày phát sinh dữ liệu chấm công) * 100.
- Logic:    - Ngày đúng giờ: Là ngày có Giờ vào <= Giờ bắt đầu ca.
    - Không tính các ngày Nghỉ lễ, Nghỉ phép vào mẫu số để tránh làm sai lệch tỷ lệ.
    - Làm tròn: Hiển thị 0 chữ số thập phân (VD: 95%).

**3.2. Thẻ "Tổng số ngày nghỉ"**

- Công thức: Tổng nghỉ = SUM(Số đơn Nghỉ phép/Nghỉ lễ được phê duyệt).
- Đơn vị: Cho phép hiển thị số lẻ 0.5 (Nghỉ nửa buổi) hoặc số nguyên (Nghỉ cả ngày).
- Case:    - Chỉ đếm các đơn có trạng thái Approved trong tháng hiện tại.
    - Bao gồm cả nghỉ có lương và không lương (tổng hợp chung).

**3.3. Thẻ "Tăng ca"**

- Công thức: Tổng OT = SUM (Thời gian OT đã được approved bởi HR).
- Đơn vị: Hiển thị dạng giờ (VD: 04.5h).
- Kịch bản bản web: Dữ liệu cần phản hồi ngay lập tức sau khi được duyệt đơn. Nếu là ca hành chính (Kết thúc 17:30), quẹt ra lúc 19:00 ➔Log OT ➔ Được duyệt OT ➔ Hiển thị ngay 1.5h tăng ca sau khi dữ liệu đồng bộ.

#### **3.4. Tương thích Giao diện Web**

- Khối 03 thẻ phải tự động co giãn theo chiều rộng màn hình

---

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| A02-E1 | **Ngày đầu tháng — division by zero** — Ngày 01 chưa có dữ liệu chấm công, mẫu số = 0 | HIGH | Hiển thị "Chưa có dữ liệu" thay vì 0% hoặc NaN. Thẻ thống kê hiện "--" cho tất cả metrics. |
| A02-E2 | **NV gia nhập giữa tháng** — NV vào làm ngày 15, mẫu số chỉ tính từ ngày 15 | MEDIUM | Mẫu số = số ngày làm việc kể từ `employee.joinDate` (không phải ngày 01). Hiển thị ghi chú "(Tính từ dd/MM)" bên cạnh tỷ lệ. |
| A02-E3 | **NV nghỉ dài hạn (thai sản 6 tháng)** — Không có dữ liệu chấm công nhiều tháng liên tiếp | MEDIUM | Hiển thị trạng thái đặc biệt "Đang nghỉ dài hạn — Thai sản". Ẩn thẻ thống kê chuyên cần, chỉ hiển thị thông tin nghỉ phép. |

---

### **4. DEFINITION OF DONE (DOD)**

1. **Phân quyền**: Đảm bảo nhân viên không xem được thống kê của đồng nghiệp qua Web Inspect.
2. **Độ chính xác**: Kiểm thử với dữ liệu thực ➔ Con số thống kê phải khớp hoàn toàn với danh sách Nhật ký Chấm công (US-ATTEN-03).
3. **Tải dữ liệu**: Thời gian truy xuất 03 mốc dữ liệu không quá 1.5 giây khi vào trang.
4. **QA**: Xác nhận Test case pass 100% — **bao gồm case: ngày đầu tháng, NV mới giữa tháng, NV nghỉ dài hạn**.
