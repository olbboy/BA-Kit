# US-HOL-04: API hiển thị

---

**AS A** Nhân viên,  
**I WANT TO** xem lịch nghỉ lễ chính thức và các ngày nghỉ đặc thù của cá nhân qua điện thoại,  
**SO THAT** cá nhân tôi có thể chủ động nắm bắt lịch trình làm việc và sắp xếp kế hoạch nghỉ ngơi hợp lý.

---

### **1. LUỒNG NGHIỆP VỤ (BUSINESS FLOW)**

1. **Truy cập Lịch cá nhân**: Nhân viên mở mục Lịch & Ngày nghỉ trên Mini App.
2. **Xem biểu đồ màu sắc**:    - Hệ thống gọi API để lấy danh sách ngày nghỉ của tháng hiện tại.
    - Hiển thị mã màu: Đỏ (Lễ quốc gia), Xanh lá (Lễ nội bộ/Sinh nhật), Trắng (Ngày làm việc).

3. **Xem chi tiết sự kiện**: Nhấn vào một ngày có mã màu ➔ Hiển thị tên ngày lễ và nội dung đãi ngộ đãi ngộ (VD: Nghỉ hưởng lương 100%).
4. **Cập nhật Trạng thái đặc biệt**: Hiển thị các thông tin: Đã cộng phép sinh nhật, Đã kích hoạt nghỉ thiên tai vùng, hoặc thông tin Hạn mức WFH đã sử dụng.

---

### **2. QUYỀN TRUY CẬP (ACCESS CONTROL)**

| Nội dung | Quyền hạn | Ghi chú |
| --- | --- | --- |
| Xem lịch trình cá nhân | Nhân viên | Chỉ xem được dữ liệu của chính mình. |
| Hiển thị thông tin chung | Toàn bộ nhân sự | Xem các ngày nghỉ lễ chung của toàn công ty. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị Calendar trên Mobile UI**

- Giao diện lịch tháng phải hiển thị rõ các mốc ngày nghỉ được tô màu để nhân viên dễ nhận diện.
- Trường hợp nhân viên có ngày sinh nhật trong tháng ➔ Ô ngày đó phải có biểu tượng Icon quà tặng hoặc Badge "Sinh nhật".

#### **AC2. API cung cấp dữ liệu Lịch cá nhân**

- Xây dựng bộ API hỗ trợ trả dữ liệu theo danh mục: Ngày lễ chung, Ngày nghỉ riêng (Sinh nhật), Trạng thái Vùng (Thiên tai).
- Tốc độ phản hồi API trả về cho App phải dưới 1 giây để đảm bảo trải nghiệm người dùng mượt mà.

#### **AC3. Hiển thị thông tin Chi tiết ngày nghỉ**

- Khi nhấn vào ngày nghỉ ➔ Hiển thị Popup hoặc nhãn mô tả: Tên Lễ, Loại hình nghỉ (Hưởng lương/Không lương/Theo luật).

---

### **4. ĐỊNH NGHĨA HOÀN THÀNH (DEFINITION OF DONE)**

1. **Trải nghiệm người dùng:** Lịch hiển thị trực quan, dễ hiểu, các mốc màu sắc khớp hoàn toàn với cấu hình Admin.
2. **Đồng bộ dữ liệu:** Khi Admin thay đổi 1 ngày nghỉ lễ trên Web ➔ Dữ liệu trên App nhân viên phải cập nhật ngay lập tức sau khi Refresh.
3. **Tương thích:** Hiển thị ổn định trên cả hệ điều hành iOS và Android của ứng dụng Mini App.
4. **Audit:** Ghi vết (Log) lịch sử truy cập lịch trình để đảm bảo tính sẵn sàng của dữ liệu.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| HL04-E1 | **API query year = null** — Client không gửi year param | LOW | Default: năm hiện tại. Response header: `X-Default-Year: 2026`. |
| HL04-E2 | **API rate limit** — Client gọi > 100 req/phút | MEDIUM | 429 Too Many Requests. Header: `Retry-After: 60`. |
| HL04-E3 | **Không có dữ liệu cho năm** — Query năm chưa có policy | LOW | Trả array rỗng `[]` với HTTP 200 (không phải 404). |
