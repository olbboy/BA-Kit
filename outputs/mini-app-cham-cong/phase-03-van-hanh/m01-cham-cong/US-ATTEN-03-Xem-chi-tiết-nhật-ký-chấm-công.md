# US-ATTEN-03: Xem chi tiết nhật ký chấm công

---

### **USER STORY - US-1.1: TRA CỨU NHẬT KÝ & ẢNH ĐỐI SOÁT**

**AS A** Nhân viên,  
**I WANT TO** tra cứu danh sách nhật ký chấm công hàng ngày và mở xem ảnh Face ID thu được từ Camera,  
**SO THAT** tôi có thể chủ động đối soát dữ liệu thực tế và có minh chứng chính xác khi cần gửi giải trình.

---

### **1. BUSINESS FLOW**

1. **Dữ liệu đầu vào**: Hệ thống C-Vision lưu mốc Timestamp và Face Snapshot khi nhân viên quẹt thẻ thành công.
2. **Khởi tạo danh sách**: Mini App thực hiện truy vấn và sắp xếp dữ liệu theo thứ tự: Mới nhất ở trên cùng.
3. **Hành động trên Web App**:    - Nhân viên cuộn chuột để xem lịch sử **3 **ngày gần nhất tại Trang chủ.
    - Nhấn vào biểu tượng mũi tên xuống (Mũi tên Accordion) tại ngày bất kỳ.

4. **Phản hồi**: Hệ thống mở rộng phần nội dung, hiển thị ảnh chụp thực tế và thông tin chi tiết mốc quẹt In/Out.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Lịch sử mốc quẹt (In/Out) | Nhân viên, HR, Quản lý | ABAC: Chỉ hiển thị lịch sử của chính chủ tài khoản. |
| Ảnh Face Snapshot (Ảnh chụp) | Nhân viên, HR, Quản lý | ABAC: Bảo mật dữ liệu hình ảnh cá nhân. |
| Địa điểm Camera | Toàn bộ các Role | Hiển thị tên sảnh/cửa nơi nhân viên quẹt thẻ. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **3.1. Hiển thị danh sách Nhật ký**

- Sắp xếp: Phải hiển thị theo quy tắc Ngày mới nhất ➔ Ngày cũ nhất.
- Thông tin hiển thị trên mỗi dòng: Thứ, Ngày, Nội dung (Vào trễ/Đúng giờ), Badge trạng thái (Đúng giờ - Xanh | Trễ - Đỏ).
- Case:    - Mặc định chỉ hiển thị tối đa **3** ngày gần nhất tại màn Trang chủ.
    - Nhấn nút "Xem tất cả" ➔ Hệ thống chuyển hướng sang màn hình Nhật ký đầy đủ (có tính năng lọc ngày).

#### **3.2. Tương tác Accordion**

- Thao tác: Nhân viên nhấn vào biểu tượng mũi tên (v) ở cuối mỗi dòng.
- Thông tin hiển thị khi mở rộng:    - Ảnh chụp: Hiển thị ảnh chân dung của nhân viên tại thời điểm quét Camera AI.
    - Thời gian đầy đủ: Hiển thị mốc [Giờ : Phút : Giây].
    - Tên Camera/Địa điểm: Hiển thị sảnh tòa nhà hoặc văn phòng nơi ghi nhận dữ liệu.

- Web App Logic: Khi mở Accordion của ngày A ➔ Tự động đóng Accordion của ngày B (nếu đang mở) — chỉ hiển thị 1 Accordion mở tại một thời điểm trên điện thoại.

#### **3.3. Xử lý Trạng thái đặc biệt**

- Nếu là ngày nghỉ/lễ: Hiển thị Badge "NGHỈ PHÉP" (màu xanh dương) hoặc "NGHỈ LỄ" (Màu xanh dương), hoặc "NGHỈ KHÔNG LƯƠNG" (màu đỏ)
- Nếu là ngày đi làm trễ X phút: Hiển thị Badge "TRỄ X PHÚT" (Màu Đỏ).
- Nếu là ngày quên chấm công: Hiển thị Badge "Quên check-out" (Màu vàng) và có button "Giải trình" cho phép chuyển thẳng sang màn "Giải trình công"
- Nếu đang làm việc (Chưa Check-out): Giờ Ra hiển thị `--:--`.

---

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| A03-E1 | **Ảnh Face ID không khả dụng** — C-Vision không trả ảnh (lỗi mạng, hết dung lượng) | MEDIUM | Hiển thị placeholder "Ảnh không khả dụng" + icon retry. Không block hiển thị mốc giờ. Lazy-load ảnh riêng biệt. |
| A03-E2 | **Giải trình đang PENDING** — Ngày có đơn giải trình chưa duyệt | LOW | Hiển thị Badge phụ "Đang giải trình" (Vàng) bên cạnh Badge trạng thái chính. Tooltip: "Đơn giải trình đang chờ duyệt". |
| A03-E3 | **Data retention — Ảnh Face ID** — Thời gian lưu trữ ảnh cá nhân | CRITICAL | **Chính sách bắt buộc:** Ảnh Face ID lưu tối đa 90 ngày kể từ ngày chấm công (tuân thủ NĐ 13/2023 về BVDL cá nhân). Sau 90 ngày: ảnh bị xóa, Accordion hiển thị "Ảnh đã hết hạn lưu trữ". Mốc giờ + metadata vẫn giữ. |

---

### **4. DEFINITION OF DONE (DOD)**

1. **Chất lượng ảnh**: Ảnh snapshot từ Camera AI phải được hiển thị rõ nét, tốc độ tải ảnh ≤ 2 giây trên 3G, không block rendering trang (lazy-load).
2. **Độ đồng nhất**: Dữ liệu giờ công trong nhật ký phải khớp 100% với dữ liệu hiển thị tại Thẻ Hub (US-ATTEN-01).
3. **Giao diện Web**: Hiệu ứng mở rộng/thu gọn mượt.
4. **Phản quyền**: Đảm bảo nhân viên không thể thay đổi hoặc can thiệp vào dữ liệu nhật ký này (Read-only).
5. **Data retention**: Kiểm thử ảnh > 90 ngày → hiển thị "Ảnh đã hết hạn lưu trữ" + mốc giờ vẫn hiển thị đúng.
