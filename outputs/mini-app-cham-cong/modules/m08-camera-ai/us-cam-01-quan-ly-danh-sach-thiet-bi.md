# US-CAM-01: Quản lý danh sách thiết bị Camera

---

**AS A** IT Admin,  
**I WANT TO** đăng ký, cấu hình và quản lý danh sách camera AI (C-Vision) trong hệ thống,  
**SO THAT** mỗi camera được gán đúng chi nhánh, hướng In/Out và ngưỡng confidence để dữ liệu chấm công chính xác.

---

### **1. BUSINESS FLOW**

1. **Xem danh sách:** IT Admin truy cập "Cấu hình Camera AI" → Hiển thị bảng danh sách camera.
2. **Thêm camera:** Nhập deviceId (từ C-Vision), chọn site, đặt tên, chọn directionType, thiết lập threshold.
3. **Sửa cấu hình:** Thay đổi hướng In/Out, ngưỡng confidence, trạng thái Active/Inactive.
4. **Vô hiệu hóa:** Chuyển camera sang Inactive khi hỏng/bảo trì → Hệ thống bỏ qua webhook từ camera này.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| CRUD camera | IT Admin, SYS_ADMIN | Chỉ IT/Admin mới quản lý thiết bị. |
| Xem danh sách camera | HR Admin | Read-only, để biết camera nào đang hoạt động. |
| Camera thuộc site | SITE_HR | Chỉ xem camera thuộc site mình. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị danh sách camera**

- Các cột: Tên camera, Device ID, Chi nhánh, Hướng (IN/OUT/BIDIRECTIONAL), Ngưỡng confidence, Trạng thái, Lần hoạt động cuối.
- Badge trạng thái: Active (Xanh), Inactive (Xám), Offline (Đỏ — mất heartbeat > 5 phút).
- Lọc theo: Chi nhánh, Trạng thái, Hướng.

#### **AC2. Thêm/Sửa camera**

- **Trường bắt buộc:** deviceId (*), Tên (*), Site (*), directionType (*).
- **directionType:** IN_ONLY (cổng vào), OUT_ONLY (cổng ra), BIDIRECTIONAL (2 chiều).
- **confidenceThreshold:** Mặc định 0.85. Cho phép chỉnh từ 0.70 đến 0.99.
- **deviceId unique:** Không cho phép 2 camera cùng deviceId trong hệ thống.

#### **AC3. Vô hiệu hóa camera**

- Toggle Active/Inactive.
- Khi Inactive: Webhook từ camera này vẫn được nhận nhưng bị drop (ghi log).
- Hiển thị cảnh báo trước khi vô hiệu hóa: "Camera [X] sẽ ngừng ghi nhận chấm công. Xác nhận?"

#### **AC4. Xác định hướng chấm công**

Hệ thống xác định CHECK_IN/CHECK_OUT theo thứ tự ưu tiên:
1. **Cấu hình thiết bị:** IN_ONLY = luôn CHECK_IN; OUT_ONLY = luôn CHECK_OUT.
2. **Tên thiết bị:** Chứa "entrance/vào/checkin" = IN; "exit/ra/checkout" = OUT.
3. **Xen kẽ:** Lần cuối là CHECK_IN → lần này CHECK_OUT, và ngược lại.

---

---

### **GHERKIN SCENARIOS**

```gherkin
Feature: US-CAM-01
  As a IT Admin
  I want to đăng ký, cấu hình và quản lý danh sách camera AI (C-Vision) trong hệ thống
  So that mỗi camera được gán đúng chi nhánh, hướng In/Out và ngưỡng confidence để dữ liệu chấm công chính xác.

  Scenario: AC1 — Hiển thị danh sách camera
    Given IT Admin đã đăng nhập vào hệ thống
    And dữ liệu đã tồn tại trong hệ thống
    When IT Admin truy cập màn hình "Hiển thị danh sách camera"
    Then hệ thống hiển thị đúng dữ liệu theo quyền truy cập

  Scenario: AC2 — Thêm/Sửa camera
    Given IT Admin đã đăng nhập vào hệ thống
    When IT Admin thực hiện "Thêm/Sửa camera" với dữ liệu hợp lệ
    Then hệ thống lưu thành công và trả về xác nhận
    And thông báo được gửi đến người phê duyệt

  Scenario: AC3 — Vô hiệu hóa camera
    Given IT Admin đã đăng nhập vào hệ thống
    When IT Admin thực hiện "Vô hiệu hóa camera"
    Then hệ thống xử lý đúng theo yêu cầu

  Scenario: AC4 — Xác định hướng chấm công
    Given IT Admin đã đăng nhập vào hệ thống
    When IT Admin thực hiện "Xác định hướng chấm công"
    Then hệ thống xử lý đúng theo yêu cầu

  Scenario: Error1 — Device ID trùng
    Given IT Admin đã đăng nhập
    When xảy ra điều kiện "Device ID trùng"
    Then hệ thống hiển thị thông báo lỗi phù hợp
    And không có dữ liệu bị mất hoặc sai lệch

  Scenario: Error2 — Xóa camera đang active
    Given IT Admin đã đăng nhập
    When xảy ra điều kiện "Xóa camera đang active"
    Then hệ thống hiển thị thông báo lỗi phù hợp
    And không có dữ liệu bị mất hoặc sai lệch

  Scenario: Error3 — Camera chưa có trên C-Vision
    Given IT Admin đã đăng nhập
    When xảy ra điều kiện "Camera chưa có trên C-Vision"
    Then hệ thống hiển thị thông báo lỗi phù hợp
    And không có dữ liệu bị mất hoặc sai lệch
```

### **4. DEFINITION OF DONE (DOD)**

1. **Webhook:** Sau khi thêm camera, webhook từ C-Vision phải được xử lý đúng.
2. **Inactive:** Camera Inactive → Không tạo attendance record.
3. **Unique:** Thêm camera trùng deviceId → Báo lỗi.
4. **QA:** Kiểm thử thêm/sửa/vô hiệu hóa; kiểm tra direction detection logic.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| CM01-E1 | **Device ID trùng** — Đăng ký camera đã có trong hệ thống | HIGH | Chặn: "Device ID [X] đã được đăng ký tại [Site Y]." |
| CM01-E2 | **Xóa camera đang active** — Camera đang có NV check-in hằng ngày | HIGH | Soft-delete: set status INACTIVE. Dữ liệu lịch sử giữ nguyên. Cần confirm: "Camera sẽ ngừng nhận dữ liệu chấm công." |
| CM01-E3 | **Camera chưa có trên C-Vision** — DeviceId không match C-Vision API | MEDIUM | Cảnh báo: "Thiết bị chưa được đăng ký trên C-Vision. Webhook sẽ bị reject." Cho phép lưu draft. |
