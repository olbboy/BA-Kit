# US-EMP-03: Danh sách nhân sự và tìm kiếm

---

**AS A** HR Admin,  
**I WANT TO** xem danh sách toàn bộ nhân sự kèm thông tin cơ bản và tìm kiếm (kết quả ≤ 0.5 giây),  
**SO THAT** tôi có thể tra cứu nhân viên trong ≤ 3 thao tác và quản lý thông tin chính xác.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** HR mở "Quản lý nhân sự" → Tab "Danh sách nhân sự".
2. **Hiển thị:** Bảng danh sách NV với các cột thông tin cơ bản.
3. **Tìm kiếm:** Thanh search hỗ trợ tìm theo Tên, Mã NV, Email — không phân biệt hoa/thường/dấu.
4. **Lọc:** Lọc theo Phòng ban, Trạng thái (Active/Inactive/Transferred), Chi nhánh.
5. **Chi tiết:** Nhấn vào NV → Xem profile đầy đủ.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Danh sách NV toàn site | SITE_HR, SITE_MANAGER | Chỉ xem NV thuộc site mình. |
| Danh sách NV toàn hệ thống | GLOBAL_HR, SYS_ADMIN | Xem tất cả site. |
| Ảnh chân dung NV | HR Admin | Validate có ảnh hay chưa phục vụ Face ID. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị bảng danh sách**

- Các cột: Ảnh, Mã NV, Họ tên, Email, Phòng ban, Trạng thái, Chi nhánh.
- Sắp xếp: Mặc định theo Tên A-Z. Cho phép sort theo từng cột.
- Phân trang: 50 NV/trang.
- Badge trạng thái: Active (Xanh), Inactive (Xám), Transferred (Vàng).

#### **AC2. Tìm kiếm nhân viên**

- Không phân biệt hoa/thường/dấu: "nguyen" → "Nguyễn Văn A".
- Tìm theo: Tên, Mã NV, Email.
- Kết quả trả về ≤ 0.5 giây.
- Highlight từ khóa trong kết quả.

#### **AC3. Bộ lọc**

- Phòng ban: Dropdown cây (chọn phòng ban → hiển thị NV thuộc phòng + phòng con).
- Trạng thái: Multi-select (Active, Inactive, Transferred).
- Chi nhánh: Dropdown (chỉ hiển thị site thuộc quyền quản lý).
- Kết hợp lọc: Lọc đồng thời nhiều điều kiện.

#### **AC4. Validate ảnh chân dung**

- Cột Ảnh hiển thị: Ảnh thumbnail nếu có; Icon placeholder + badge "Chưa có ảnh" nếu thiếu.
- HR có thể filter "Chưa có ảnh" để nhắc NV đăng ký Face ID.

---

### **4. DEFINITION OF DONE (DOD)**

1. **Hiệu năng:** Tải danh sách 5,000+ NV ≤ 2 giây với phân trang.
2. **Tìm kiếm unicode:** Kiểm thử với dấu tiếng Việt (ô, ơ, ư, ă, â, ê).
3. **RBAC:** SITE_HR không thể xem NV site khác → Phải trả danh sách rỗng.
4. **QA:** Kiểm thử sort + filter + search kết hợp; danh sách rỗng (site mới).

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM03-E1 | **Tìm kiếm không dấu** — VD: "Nguyen" tìm "Nguyễn" | MEDIUM | Full-text search không phân biệt dấu, hoa/thường. Sử dụng unaccent + ILIKE. |
| EM03-E2 | **Danh sách > 5000 NV** — Load time | MEDIUM | Phân trang server-side (50 NV/trang). Virtual scroll cho smooth UX. |
| EM03-E3 | **NV status TRANSFERRED** — Đang chuyển chi nhánh | LOW | Hiển thị badge "Đang chuyển" màu vàng. Cho phép xem nhưng không chỉnh sửa. |
