# US-HOL-03: Logic sync & batch job

---

**Hệ thống** tự động đồng bộ và quét dữ liệu lịch nghỉ lễ/đãi ngộ đãi ngộ hằng ngày,  
**SO THAT** dữ liệu chấm công và ngày nghỉ của nhân viên luôn được cập nhật chính xác tuyệt đối mà không cần HR phải can thiệp thủ công.

---

### **1. LUỒNG NGHIỆP VỤ (BUSINESS FLOW)**

1. **Tiến trình chạy tự động (Batch Job)**: Hệ thống thực hiện quét dữ liệu vào lúc 00:01 hằng ngày cho toàn bộ nhân sự đang hoạt động.
2. **Đồng bộ Ngày nghỉ lễ**: Đối soát ngày hiện tại với bảng danh mục ngày nghỉ (Lễ quốc gia/Nội bộ) ➔ Tự động gán trạng thái "Hợp lệ/Hưởng lương" trên Nhật ký chấm công.
3. **Xử lý Logic Nghỉ sinh nhật**: Kiểm tra ngày hiện tại có trùng với tháng sinh nhật của nhân viên không ➔ Kiểm tra status nhân viên có Chính thức không ➔ Tự động gán 01 ngày nghỉ phép có lương vào quỹ phép cá nhân tháng đó.
4. **Kích hoạt Chế độ khẩn cấp (Thiên tai)**: Khi Admin bật chế độ thiên tai và chọn khu vực ➔ Hệ thống lập tức quét danh sách nhân viên thuộc các văn phòng ở khu vực đó ➔ Gán trạng thái nghỉ khẩn cấp mà không tính là vắng mặt không phép.

---

### **2. QUYỀN TRUY CẬP (ACCESS CONTROL)**

| Nội dung | Quyền hạn | Ghi chú |
| --- | --- | --- |
| Tiến trình chạy tự động | Hệ thống | Hoàn toàn tự động, không có giao diện người dùng. |
| Theo dõi Nhật ký đồng bộ | Quản trị hệ thống | Xem lịch sử các lần chạy Batch job để xử lý nếu có lỗi. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Đồng bộ Ngày nghỉ lễ**

- Nếu ngày hôm nay là Ngày nghỉ lễ đã cấu hình ➔ Trạng thái trên App nhân viên phải hiển thị là "NGHỈ LỄ" và thanh tiến độ 8h phải được làm đầy ngay lập tức từ mốc 0h sáng.

#### **AC2. Logic Cộng phép sinh nhật**

- Hệ thống chỉ thực hiện cộng phép khi tài khoản nhân viên thỏa mãn điều kiện thâm niên làm việc chính thức.
- Nghiệp vụ này chỉ thực hiện 1 lần duy nhất trong tháng sinh nhật của nhân sự.

#### **AC3. Hiệu năng & Ràng buộc đồng bộ**

- Bộ mã nguồn xử lý ngầm (Backend) phải hoàn thành việc quét cho toàn bộ nhân sự trong thời gian dưới 5 phút hằng ngày.
- Trong trường hợp Batch job bị lỗi ➔ Phải có danh sách bản ghi lỗi để Admin có thể kích hoạt chạy lại thủ công (Retry).

---

### **4. ĐỊNH NGHĨA HOÀN THÀNH (DEFINITION OF DONE)**

1. **Độ chính xác:** Giả lập ngày 01/05 cho 1 nhân viên không đi làm ➔ Nhật ký phải báo 8h công "Hợp lệ" thành công.
2. **Độ tin cậy:** Batch job không bị treo hay lặp lại việc cộng phép 2 lần cho cùng một người trong tháng.
3. **Logs:** Toàn bộ lịch sử các lần đồng bộ phải được lưu vết rõ ràng trong cơ sở dữ liệu.
4. **Bảo mật:** Không cho phép bất kỳ API bên ngoài nào có thể can thiệp vào tiến trình quét tự động này.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| HL03-E1 | **Batch job fail giữa chừng** — Sync 1000 NV, lỗi tại NV thứ 500 | HIGH | Ghi log chi tiết. Đánh dấu NV lỗi. Tiếp tục xử lý NV còn lại. Retry failed batch sau 15 phút. |
| HL03-E2 | **Duplicate sync event** — 2 instance job chạy đồng thời | MEDIUM | Distributed lock (Redis). Instance thứ 2 skip nếu lock đã active. Log: "Sync already running, skipped." |
| HL03-E3 | **Config thay đổi giữa batch** — HR thay đổi policy khi batch đang chạy | LOW | Batch dùng snapshot config tại thời điểm bắt đầu. Thay đổi áp dụng cho batch tiếp theo. |
