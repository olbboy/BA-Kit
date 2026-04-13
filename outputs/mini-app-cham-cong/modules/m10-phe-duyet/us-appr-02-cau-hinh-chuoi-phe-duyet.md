# US-APPR-02: Cấu hình chuỗi phê duyệt

---

**AS A** HR Admin,  
**I WANT TO** thiết lập chuỗi phê duyệt (Approval Chain) cho từng loại đơn tại mỗi chi nhánh,  
**SO THAT** đơn từ được duyệt đúng cấp, đúng quy trình theo chính sách riêng của từng site.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** HR Admin mở "Trung tâm phê duyệt" → Tab "Cấu hình".
2. **Chọn site:** Dropdown chọn chi nhánh cần cấu hình.
3. **Chọn loại đơn:** LEAVE, OT_REQUEST, CORRECTION, MANUAL_ATTENDANCE, SHIFT_CHANGE.
4. **Thiết lập chain:**
   - Thêm level: Chọn loại approver (DIRECT_MANAGER, DEPT_HEAD, SITE_HR, GLOBAL_HR).
   - Điều kiện kích hoạt: VD "Level 2 chỉ kích hoạt nếu nghỉ > 3 ngày".
   - Sắp xếp thứ tự level.
5. **Cấu hình fallback:** Nếu approver chính không có quyền tại site → Chỉ định fallback.
6. **Lưu:** Áp dụng cho tất cả đơn mới tại site đó.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Cấu hình chain | HR Admin, GLOBAL_HR | SITE_HR chỉ cấu hình site mình. |
| Xem cấu hình | HR, Quản lý | Read-only. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Thiết lập Approval Chain**

- Giao diện dạng danh sách level (drag-and-drop sắp xếp thứ tự).
- Mỗi level gồm:
  - **Loại approver:** DIRECT_MANAGER, DEPT_HEAD, SITE_MANAGER, SITE_HR, GLOBAL_HR.
  - **Điều kiện (optional):** > N ngày, > N giờ, loại phép nhạy cảm.
  - **Bắt buộc/Tùy chọn:** Level bắt buộc luôn kích hoạt; level tùy chọn chỉ khi điều kiện thỏa.
- Tối thiểu 1 level; tối đa 5 levels.

#### **AC2. Xác định Approver (Approver Resolution)**

Hệ thống tự động xác định người duyệt:

| Loại | Cách xác định |
| --- | --- |
| DIRECT_MANAGER | Employee.managerId |
| DEPT_HEAD | Trưởng phòng ban của NV |
| SITE_MANAGER | User có role SITE_MANAGER tại site |
| SITE_HR | User có role SITE_HR_ADMIN tại site |
| GLOBAL_HR | User có role GLOBAL_HR_ADMIN, scope ALL_SITES |

#### **AC3. Chuỗi Fallback**

- Nếu approver chính không có quyền tại site:
  - DIRECT_MANAGER → SITE_MANAGER → SITE_HR → GLOBAL_HR.
- Admin có thể tùy chỉnh chuỗi fallback.
- Hiển thị cảnh báo: "Approver [Tên] không có quyền tại site [X]. Fallback: [Y]".

#### **AC4. Cấu hình ngày chốt công**

- Thiết lập ngày chốt công hàng tháng (VD: ngày 25).
- Sau ngày chốt: Đơn thuộc tháng cũ KHÔNG thể duyệt (trừ Exception Approval).
- Exception Approval: Chỉ GLOBAL_HR hoặc SYS_ADMIN có quyền.

---

---

### **GHERKIN SCENARIOS**

```gherkin
Feature: US-APPR-02
  As a HR Admin
  I want to thiết lập chuỗi phê duyệt (Approval Chain) cho từng loại đơn tại mỗi chi nhánh
  So that đơn từ được duyệt đúng cấp, đúng quy trình theo chính sách riêng của từng site.

  # --- AC1: Thiết lập Approval Chain ---
  Scenario: AC1.1 — Thiết lập Approval Chain
    Given HR Admin truy cập module
    When thực hiện "Thiết lập Approval Chain"
    Then hiển thị kết quả chính xác. Dữ liệu phân quyền đúng RBAC.

  # --- AC2: Xác định Approver (Approver Resolution) ---
  Scenario: AC2.1 — Xác định Approver (Approver Resolution)
    Given HR Admin truy cập module
    When thực hiện "Xác định Approver (Approver Resolution)"
    Then hiển thị kết quả chính xác. Dữ liệu phân quyền đúng RBAC.

  # --- AC3: Chuỗi Fallback ---
  Scenario: AC3.1 — Chuỗi Fallback
    Given HR Admin truy cập module
    When thực hiện "Chuỗi Fallback"
    Then hiển thị kết quả chính xác. Dữ liệu phân quyền đúng RBAC.

  # --- AC4: Cấu hình ngày chốt công ---
  Scenario: AC4.1 — Cấu hình ngày chốt công
    Given HR Admin truy cập module
    When thực hiện "Cấu hình ngày chốt công"
    Then hiển thị kết quả chính xác. Dữ liệu phân quyền đúng RBAC.

  # --- Edge Case ---
  Scenario: Edge1 — Tổ chức thay đổi giữa approval
    Given NV chuyển phòng khi đơn đang xử lý
    When hệ thống kiểm tra
    Then Snapshot approver chain tại thời điểm tạo đơn. Thay đổi tổ chức KHÔNG ảnh hưởng đơn đang pending.

  # --- Edge Case ---
  Scenario: Edge2 — Config approval chain rỗng
    Given Site mới chưa cấu hình
    When hệ thống kiểm tra
    Then Chặn NV tạo đơn. Hiển thị: "Chưa cấu hình quy trình phê duyệt. Liên hệ HR chi nhánh."

  # --- Edge Case ---
  Scenario: Edge3 — Circular approval
    Given Manager A approve cho Manager B và ngược lại
    When hệ thống kiểm tra
    Then Validate chain: không cho phép circular. Chặn lưu config nếu phát hiện loop.
```

### **4. DEFINITION OF DONE (DOD)**

1. **Chain hoạt động:** Tạo đơn → Đúng approver nhận đơn theo chain.
2. **Điều kiện:** Đơn 2 ngày → Chỉ level 1; Đơn 5 ngày → Level 1 + 2 + 3.
3. **Fallback:** Manager nghỉ phép → Đơn tự chuyển sang SITE_MANAGER.
4. **QA:** Kiểm thử chain 3 level; fallback; ngày chốt công; exception approval.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| AP02-E1 | **Tổ chức thay đổi giữa approval** — NV chuyển phòng khi đơn đang xử lý | MEDIUM | Snapshot approver chain tại thời điểm tạo đơn. Thay đổi tổ chức KHÔNG ảnh hưởng đơn đang pending. |
| AP02-E2 | **Config approval chain rỗng** — Site mới chưa cấu hình | HIGH | Chặn NV tạo đơn. Hiển thị: "Chưa cấu hình quy trình phê duyệt. Liên hệ HR chi nhánh." |
| AP02-E3 | **Circular approval** — Manager A approve cho Manager B và ngược lại | HIGH | Validate chain: không cho phép circular. Chặn lưu config nếu phát hiện loop. |
