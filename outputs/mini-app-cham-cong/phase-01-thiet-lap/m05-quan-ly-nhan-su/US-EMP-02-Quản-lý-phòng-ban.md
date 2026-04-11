# US-EMP-02: Quản lý phòng ban (CRUD)

---

**AS A** HR Admin,  
**I WANT TO** thêm, sửa, xóa các đơn vị tổ chức (Khối/Phòng ban/Đội nhóm),  
**SO THAT** cơ cấu tổ chức luôn cập nhật khi công ty có thay đổi bộ máy.

---

### **1. BUSINESS FLOW**

1. **Thêm mới:** HR nhấn "Tạo mới" → Chọn loại (Khối/Phòng/Nhóm) → Nhập tên, mã, cấp cha → Lưu.
2. **Chỉnh sửa:** HR chọn đơn vị → Sửa tên, mã, cấp cha → Lưu.
3. **Xóa:** HR chọn đơn vị → Hệ thống kiểm tra còn NV không → Nếu còn: chặn xóa; Nếu trống: confirm xóa.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Thêm/Sửa/Xóa phòng ban | HR Admin, GLOBAL_HR | SITE_HR chỉ CRUD trong site mình. |
| Xem danh sách phòng ban | HR, Quản lý | Manager chỉ xem phòng ban liên quan. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Tạo mới đơn vị**

- Trường bắt buộc: Tên (max 100 ký tự), Loại (Khối/Phòng/Nhóm), Cấp cha.
- Trường tùy chọn: Mã đơn vị, Mô tả, Quản lý phụ trách (DEPT_HEAD).
- Mã đơn vị phải unique trong cùng tenant.

#### **AC2. Cơ chế chặn xóa**

- **Có NV:** Hiển thị "Không thể xóa — còn X nhân viên thuộc đơn vị này. Vui lòng chuyển NV trước."
- **Có đơn vị con:** Hiển thị "Không thể xóa — còn Y đơn vị con. Vui lòng xóa hoặc chuyển đơn vị con trước."
- **Trống hoàn toàn:** Cho phép xóa sau confirm.

#### **AC3. Chỉnh sửa & Di chuyển**

- Cho phép đổi cấp cha (di chuyển trong cây tổ chức).
- Khi di chuyển: Tất cả NV và đơn vị con di chuyển theo.
- Ghi audit log cho mọi thay đổi.

---

### **4. DEFINITION OF DONE (DOD)**

1. **Chặn xóa:** Kiểm thử xóa phòng ban có NV → Phải bị chặn.
2. **Unique constraint:** Tạo 2 phòng ban cùng mã → Phải báo lỗi.
3. **Audit:** Mọi CRUD đều ghi log (ai, thời điểm, hành động).
4. **QA:** Kiểm thử tạo/sửa/xóa ở tất cả cấp; di chuyển cross-level.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM02-E1 | **Xóa phòng ban có NV** — Phòng ban còn 50 NV active | HIGH | Chặn xóa. Hiển thị: "Phòng ban còn [50] nhân viên. Chuyển NV trước khi xóa." |
| EM02-E2 | **Tên phòng ban trùng** — Tạo 2 phòng ban cùng tên tại 1 site | MEDIUM | Cho phép nhưng cảnh báo: "Đã tồn tại phòng ban '[Tên]' tại chi nhánh này." |
| EM02-E3 | **Xóa phòng ban cha** — Phòng ban có sub-departments | HIGH | Chặn: "Phòng ban có [N] đơn vị con. Xóa hoặc chuyển đơn vị con trước." |
