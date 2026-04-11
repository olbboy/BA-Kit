# US-EMP-01: Sơ đồ cơ cấu tổ chức

---

**AS A** HR Admin,  
**I WANT TO** xem sơ đồ cơ cấu tổ chức dạng cây trực quan với khả năng mở rộng/thu gọn và kéo thả điều chuyển,  
**SO THAT** tôi có thể nắm bắt toàn cảnh cấu trúc nhân sự và thực hiện điều chuyển tổ chức bằng drag-and-drop trực quan.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** HR mở "Quản lý nhân sự" → Tab "Sơ đồ tổ chức".
2. **Hiển thị:** Hệ thống render cây: Tổ chức → Chi nhánh (Site) → Phòng ban → Nhóm → Nhân viên.
3. **Tương tác:**
   - Expand/Collapse từng nhánh.
   - Tìm kiếm NV (trả kết quả ≤ 0.5 giây) → Highlight vị trí trên cây.
   - Kéo thả phòng ban/nhóm sang cấp cha khác (điều chuyển).
4. **Lưu:** Khi kéo thả → Hệ thống confirm → Lưu thay đổi cấu trúc.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Sơ đồ tổ chức (toàn bộ) | HR Admin, GLOBAL_HR | GLOBAL_HR xem tất cả site. |
| Sơ đồ chi nhánh | SITE_HR, SITE_MANAGER | Chỉ xem site thuộc quyền quản lý. |
| Kéo thả điều chuyển | HR Admin | Chỉ HR có quyền thay đổi cấu trúc. |
| Tìm kiếm NV | HR, Quản lý | Manager chỉ tìm NV thuộc team/phòng ban. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị cây tổ chức**

- Cấu trúc: Organization → Site → Department → Team → Employee.
- Mỗi node hiển thị: Tên, Số lượng NV con, Icon loại (Site/Dept/Team/Person).
- Mặc định: Expand đến cấp Department, collapse Team/Employee.

#### **AC2. Expand/Collapse**

- Nhấn icon "+" mở rộng; "-" thu gọn.
- Hiệu ứng animation mượt mà (< 300ms).
- Trạng thái expand/collapse được lưu trong session (không reset khi navigate).

#### **AC3. Tìm kiếm nhân viên**

- Input search không phân biệt hoa/thường/dấu (VD: "nguyen" tìm được "Nguyễn").
- Kết quả: Highlight node trên cây + tự động expand path đến node đó.
- Hỗ trợ tìm theo: Tên NV, Mã NV, Tên phòng ban.

#### **AC4. Kéo thả điều chuyển**

- Cho phép kéo phòng ban/nhóm sang cấp cha khác trong cùng site.
- Trước khi lưu: Hiển thị confirm "Bạn có chắc muốn chuyển [X] sang [Y]?".
- Sau khi lưu: Ghi audit log (ai, thời điểm, thay đổi gì).
- Chặn: Không cho kéo phòng ban có NV sang site khác (phải transfer NV trước).

---

### **4. DEFINITION OF DONE (DOD)**

1. **Hiệu năng:** Render cây ≤ 2 giây cho 5,000+ NV.
2. **Tìm kiếm:** Kết quả trả về ≤ 0.5 giây.
3. **Audit:** Mọi thay đổi cấu trúc được ghi log đầy đủ.
4. **QA:** Kiểm thử cây sâu 5 cấp; kéo thả cross-department; tìm kiếm unicode.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM01-E1 | **Sơ đồ > 1000 node** — Tổ chức lớn | MEDIUM | Lazy-load: chỉ render 3 cấp đầu tiên. Expand on-demand. Virtual rendering cho performance. |
| EM01-E2 | **NV thuộc nhiều phòng ban** — IT support multi-site | MEDIUM | Hiển thị tại Primary department. Icon link "→ Xem thêm" dẫn đến các department phụ. |
| EM01-E3 | **Drag-drop vào chính nó** — Kéo phòng ban vào chính nó hoặc child | HIGH | Chặn: "Không thể chuyển đơn vị vào chính nó hoặc đơn vị con." |
