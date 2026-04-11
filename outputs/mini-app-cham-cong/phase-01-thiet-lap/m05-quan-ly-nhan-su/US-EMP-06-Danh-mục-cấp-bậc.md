# US-EMP-06: Danh mục cấp bậc

---

**AS A** HR Admin,  
**I WANT TO** quản lý danh mục cấp bậc nhân sự (Nhân viên, Trưởng nhóm, Trưởng phòng...),  
**SO THAT** hệ thống có căn cứ phân quyền chính xác cho các luồng phê duyệt và báo cáo.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** HR mở "Quản lý nhân sự" → Tab "Danh mục cấp bậc".
2. **Xem danh sách:** Hiển thị các cấp bậc hiện có theo thứ tự phân cấp.
3. **CRUD:** Thêm/Sửa/Xóa cấp bậc. Gán cấp bậc cho NV.
4. **Áp dụng:** Cấp bậc được dùng trong phân quyền (Module 10) và báo cáo (Module 11).

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| CRUD danh mục cấp bậc | HR Admin, GLOBAL_HR | Chỉ HR cấp cao mới được thay đổi. |
| Xem danh mục | HR, Quản lý | Read-only. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Danh sách cấp bậc mặc định**

Hệ thống seed sẵn:
- EMPLOYEE (Nhân viên)
- TEAM_LEAD (Trưởng nhóm)
- MANAGER (Quản lý)
- DEPT_HEAD (Trưởng phòng)
- SITE_MANAGER (Quản lý chi nhánh)

#### **AC2. CRUD cấp bậc**

- **Thêm:** Tên (*), Mã (*), Mô tả, Thứ tự phân cấp (level).
- **Sửa:** Cho phép đổi tên, mô tả. Chặn đổi mã nếu đã có NV sử dụng.
- **Xóa:** Chặn nếu còn NV đang gán cấp bậc này.

#### **AC3. Mapping với phân quyền**

- Cấp bậc quyết định: ai là approver của ai (Module 10).
- Level cao hơn có thể xem báo cáo của level thấp hơn.
- Hiển thị mapping: Cấp bậc → Role EAMS (VD: DEPT_HEAD → quyền phê duyệt cấp 2).

---

### **4. DEFINITION OF DONE (DOD)**

1. **Chặn xóa:** Xóa cấp bậc đang có NV → Phải bị chặn.
2. **Seed data:** Hệ thống mới phải có 5 cấp bậc mặc định sẵn.
3. **Phân quyền:** Thay đổi cấp bậc NV → Quyền phê duyệt cập nhật tương ứng.
4. **QA:** Kiểm thử thêm cấp bậc mới → Gán cho NV → Kiểm tra phân quyền.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM06-E1 | **Xóa cấp bậc đang được sử dụng** — 200 NV có cấp bậc "Nhân viên" | HIGH | Chặn xóa: "Cấp bậc đang được gán cho [200] NV. Chuyển NV sang cấp bậc khác trước." |
| EM06-E2 | **Tên cấp bậc trùng** | MEDIUM | Chặn: "Cấp bậc '[X]' đã tồn tại." |
