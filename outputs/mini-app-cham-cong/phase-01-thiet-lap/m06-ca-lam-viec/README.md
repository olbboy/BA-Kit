# 2.11.2. Cấu hình ca làm việc

---

| Thông tin | Nội dung |
| --- | --- |
| Target release | Version 1.0 (Sprint 8) |
| Epic | STRATOS-ADMIN: Hệ thống Quản trị & Cấu hình tập trung |
| Document owner | BA Team |
| Stakeholder | HR Admin, Quản lý |
| Status | Open |
| Tham chiếu | EAMS v2.0 §4 (Quản lý ca làm việc) |

---

### **1. MỤC TIÊU**

- **Lý do tồn tại:** Doanh nghiệp có nhiều loại ca làm việc phức tạp (ca hành chính, ca đêm, ca xoay) cần được cấu hình linh hoạt và chính xác để hệ thống tự động tính công.
- **Bài toán:** Cung cấp công cụ cho HR thiết lập khung giờ In/Out, giờ nghỉ, giới hạn chấm công (Punch Limit) và gán nhân viên vào ca hàng loạt.
- **Giá trị mang lại:** Giảm 90% thời gian phân ca thủ công; đảm bảo tính chính xác khi tính giờ công, OT và trạng thái chuyên cần.

---

### **2. MÔ TẢ QUY TRÌNH NGHIỆP VỤ**

```
HR truy cập "Cấu hình ca làm việc"
        ↓
Xem danh sách ca hiện có (Thẻ ca bên trái)
        ↓
  ├─ Tạo ca mới: Nhập tên, chọn ngày, giờ In/Out, Break, Punch Limit
  ├─ Chỉnh sửa ca: Chọn thẻ ca → Cập nhật thông số
  └─ Import NV: Tải file Excel mẫu → Điền mã NV → Upload → Validate → Gán ca
        ↓
Hệ thống áp dụng cấu hình mới cho chấm công
```

---

### **3. NHU CẦU NGƯỜI DÙNG**

| Persona | Nhu cầu cụ thể | Tài liệu / Căn cứ |
| --- | --- | --- |
| HR Admin | Muốn tạo ca đêm xuyên ngày (20h-06h) mà hệ thống vẫn gán công đúng vào Ngày T. | Cấu hình giờ & ngày |
| HR Admin | Muốn giới hạn khung giờ check-in/out để loại bỏ dữ liệu quẹt thẻ "rác". | Punch Limit |
| HR Admin | Muốn gán ca cho 500+ nhân viên cùng lúc thay vì nhập từng người. | Import NV vào ca |

---

### **4. PHẠM VI CHỨC NĂNG**

| Mã | Chức năng | Mô tả chi tiết | User Story |
| --- | --- | --- | --- |
| F02.1 | Danh sách ca làm việc | Hiển thị các Thẻ ca kèm tên, giờ, số NV. Phân loại Active/Inactive. Sắp xếp theo giờ bắt đầu. | [US-SHIFT-01](./US-SHIFT-01-Danh-sách-ca-làm-việc.md) |
| F02.2 | Cấu hình giờ và ngày làm việc | Thiết lập tên ca, chọn ngày T2-CN, mốc giờ In/Out, ngày hiệu lực. Xử lý ca đêm tự động. | [US-SHIFT-02](./US-SHIFT-02-Cấu-hình-giờ-và-ngày-làm-việc.md) |
| F02.3 | Giới hạn thời gian chấm công | Thiết lập Punch Limit: số giờ check-in sớm / check-out muộn tối đa. Mốc quẹt ngoài khung bị bỏ qua. | [US-SHIFT-03](./US-SHIFT-03-Giới-hạn-thời-gian-chấm-công-(punch-limit).md) |
| F02.4 | Cấu hình giờ nghỉ | Thiết lập khung giờ nghỉ (Break) cho ca. Hệ thống tự trừ khi tính giờ làm thực tế. | [US-SHIFT-04](./US-SHIFT-04-Cấu-hình-giờ-nghỉ.md) |
| F02.5 | Import nhân viên vào ca | Tải file mẫu Excel, nhập Mã NV, upload và validate hàng loạt. Trả kết quả thành công/thất bại. | [US-SHIFT-05](./US-SHIFT-05-Import-nhân-viên-vào-ca.md) |
| F02.6 | Phân ca theo Pattern | Tạo pattern ca xoay (VD: Sáng→Chiều→Đêm→Nghỉ) tự lặp. Drag-drop builder, preview calendar, conflict resolution. | [US-SHIFT-06](./US-SHIFT-06-Phân-ca-theo-pattern.md) |

---

### **5. LOẠI CA HỖ TRỢ** *(Nguồn: EAMS v2.0 §4.1)*

| Loại ca | Mô tả | Ví dụ |
| --- | --- | --- |
| FIXED | Ca cố định | 08:00 - 17:00 |
| FLEXIBLE | Ca linh hoạt (core hours) | 10:00-15:00 core, ±2h |
| ROTATING | Ca xoay | Sáng/Chiều/Đêm luân phiên |
| SPLIT | Ca chia (2 buổi) | 08:00-12:00, 14:00-18:00 |
| FREE | Tự do | Chỉ cần đủ giờ/ngày |

---

### **6. YÊU CẦU PHI CHỨC NĂNG**

- **Hiệu năng:** Tải danh sách ca ≤ 1.5 giây; Import ≤ 5,000 NV/lần trong ≤ 30 giây.
- **Tính nhất quán:** Thay đổi cấu hình ca phải đồng bộ ngay xuống Dashboard NV.
- **Bảo mật:** Chỉ HR Admin mới có quyền CRUD ca và import nhân viên.

---

### **EDGE CASES & ERROR HANDLING (toàn module)**

| # | US | Case | Severity | Expected Behavior |
|---|-----|------|----------|-------------------|
| S01-E1 | SHIFT-01 | **Xóa ca có NV tương lai** — Ca đang có 200 NV assigned từ tuần sau | HIGH | Chặn xóa. Hiển thị "Không thể xóa — còn X nhân viên được gán. Chuyển NV trước hoặc chuyển ca sang Inactive". Cho phép toggle Inactive thay vì hard delete. |
| S02-E1 | SHIFT-02 | **Ca 24h (bảo vệ/security)** — Ca 00:00-00:00 | MEDIUM | Logic Ca đêm phát hiện sai khi Giờ Vào = Giờ Ra. Quy ước: nếu startTime == endTime → ca 24h. workingHours bắt buộc nhập thủ công. |
| S02-E2 | SHIFT-02 | **Thời gian hiệu lực chồng chéo** — Ca A (01/01-31/12) và Ca B (01/06-31/12) cùng NV | HIGH | Unique constraint: tenant + employee + date. Khi import/gán ca → validate: nếu NV đã có ca Active tại ngày X → hiển thị lỗi "Xung đột với ca [Tên ca] từ dd/MM". |
| S03-E1 | SHIFT-03 | **Punch limit = 0** — HR set giới hạn Check-In sớm = 0 giờ | LOW | Cảnh báo: "Punch limit = 0 sẽ chặn mọi mốc chấm công ngoài khung ca chính xác. Bạn có chắc?" Yêu cầu confirm trước khi lưu. |
| S04-E1 | SHIFT-04 | **Nhiều khung nghỉ (2+ breaks)** — Ca có nghỉ sáng 10:00-10:15 + nghỉ trưa 12:00-13:00 | MEDIUM | Hỗ trợ mảng breaks[] (EAMS §4.2). UI cho phép "Thêm khung nghỉ" button. Mỗi break: startTime, endTime, isPaid. Tổng thời gian nghỉ = SUM(breaks). |
| S05-E1 | SHIFT-05 | **NV Inactive trong file import** — File Excel chứa NV đã nghỉ việc | HIGH | Validation: kiểm tra employee.status. NV Inactive/Transferred → ghi vào file lỗi: "Nhân viên [Mã] đã Inactive — không thể gán ca". Skip bản ghi đó. |
| S05-E2 | SHIFT-05 | **File Excel chứa formulas** — Cell chứa =VLOOKUP() thay vì giá trị | MEDIUM | Backend parse values-only (read cell.value, ignore formulas). Nếu cell trả về null/error → ghi file lỗi: "Ô [column][row] chứa công thức lỗi". |

---

### **7. ĐIỀU KIỆN GIẢ ĐỊNH**

1. Người dùng đã đăng nhập với role HR Admin hoặc cao hơn.
2. Hệ thống đã khởi tạo tenant, site và danh sách nhân sự (Module 05).
3. Danh mục ngày nghỉ đã được cấu hình (Module 07) để xử lý ca đúng ngày lễ.
