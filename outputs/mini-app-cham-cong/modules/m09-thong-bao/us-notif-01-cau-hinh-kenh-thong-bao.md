# US-NOTIF-01: Cấu hình kênh thông báo

---

**AS A** HR Admin,  
**I WANT TO** cấu hình các kênh gửi thông báo (Push, Email, Popup) và thiết lập kênh ưu tiên cho từng loại sự kiện,  
**SO THAT** nhân viên nhận được thông báo qua kênh ưu tiên theo cấu hình (Push > Email > In-App), đảm bảo không bỏ sót thông tin quan trọng.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** Admin mở "Cấu hình thông báo" → Tab "Kênh thông báo".
2. **Xem danh sách kênh:** Hiển thị 3 kênh: App Push Notification, Email, Popup Dashboard.
3. **Cấu hình kênh:** Bật/tắt từng kênh; thiết lập kênh mặc định cho từng nhóm sự kiện.
4. **Fallback:** Nếu kênh ưu tiên thất bại → Tự động chuyển sang kênh dự phòng.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Cấu hình kênh | HR Admin, SYS_ADMIN | Chỉ Admin cấu hình hệ thống. |
| Xem cấu hình hiện tại | HR, IT Admin | Read-only. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Danh sách kênh**

| Kênh | Mô tả | Use case chính |
| --- | --- | --- |
| App Push | Thông báo đẩy trên điện thoại | Chấm công, nhắc nhở |
| Email | Gửi qua SMTP | Đơn từ, báo cáo |
| Popup Dashboard | Hiển thị trên giao diện web | Cảnh báo real-time |

- Mỗi kênh có Toggle Bật/Tắt.
- Hiển thị trạng thái kết nối: Connected (Xanh), Disconnected (Đỏ).

#### **AC2. Mapping kênh theo nhóm sự kiện**

- Bảng matrix: Hàng = Nhóm sự kiện, Cột = Kênh (Push/Email/Popup).
- Checkbox cho phép chọn nhiều kênh cho mỗi nhóm.
- Kênh ưu tiên: Drag-and-drop sắp xếp thứ tự ưu tiên.

#### **AC3. Fallback logic**

- Nếu Push thất bại (NV tắt notification) → Gửi Email.
- Nếu Email thất bại (bounce) → Ghi log + hiển thị Popup.
- Admin có thể cấu hình chuỗi fallback cho từng nhóm.

---

---

### **GHERKIN SCENARIOS**

```gherkin
Feature: US-NOTIF-01
  As a HR Admin
  I want to cấu hình các kênh gửi thông báo (Push, Email, Popup) và thiết lập kênh ưu tiên cho từng loại sự kiện
  So that nhân viên nhận được thông báo qua kênh ưu tiên theo cấu hình (Push > Email > In-App), đảm bảo không bỏ sót thông tin quan trọng.

  # --- AC1: Danh sách kênh ---
  Scenario: AC1.1 — Danh sách kênh
    Given HR Admin truy cập module
    When thực hiện "Danh sách kênh"
    Then hiển thị kết quả chính xác. Dữ liệu phân quyền đúng RBAC.

  # --- AC2: Mapping kênh theo nhóm sự kiện ---
  Scenario: AC2.1 — Mapping kênh theo nhóm sự kiện
    Given HR Admin truy cập module
    When thực hiện "Mapping kênh theo nhóm sự kiện"
    Then hiển thị kết quả chính xác. Dữ liệu phân quyền đúng RBAC.

  # --- AC3: Fallback logic ---
  Scenario: AC3.1 — Fallback logic
    Given HR Admin truy cập module
    When thực hiện "Fallback logic"
    Then hiển thị kết quả chính xác. Dữ liệu phân quyền đúng RBAC.

  # --- Edge Case ---
  Scenario: Edge1 — NV tắt Push Permission
    Given iOS/Android block notification
    When hệ thống kiểm tra
    Then Fallback sang Email. Dashboard hiển thị: "Push bị tắt — đang dùng Email." Nhắc NV bật Push khi mở app.

  # --- Edge Case ---
  Scenario: Edge2 — Email bounce
    Given Email NV không hợp lệ
    When hệ thống kiểm tra
    Then Mark as FAILED. Retry 1 lần. Log vào dead letter queue. HR dashboard: "[N] NV có email lỗi."

  # --- Edge Case ---
  Scenario: Edge3 — Kênh bị disable toàn hệ thống
    Given Admin tắt kênh Push
    When hệ thống kiểm tra
    Then Cảnh báo admin: "Tắt kênh Push sẽ ảnh hưởng [N] loại thông báo. Thông báo bắt buộc sẽ chuyển sang Email."
```

### **4. DEFINITION OF DONE (DOD)**

1. **Kết nối:** Toggle bật kênh → Hệ thống kiểm tra kết nối (Push/SMTP) → Hiển thị trạng thái.
2. **Fallback:** Kiểm thử Push fail → Email được gửi tự động.
3. **Giao diện:** Matrix kênh × sự kiện hiển thị rõ ràng, dễ cấu hình.
4. **QA:** Kiểm thử bật/tắt từng kênh; gửi thông báo qua tất cả kênh.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| NF01-E1 | **NV tắt Push Permission** — iOS/Android block notification | MEDIUM | Fallback sang Email. Dashboard hiển thị: "Push bị tắt — đang dùng Email." Nhắc NV bật Push khi mở app. |
| NF01-E2 | **Email bounce** — Email NV không hợp lệ | MEDIUM | Mark as FAILED. Retry 1 lần. Log vào dead letter queue. HR dashboard: "[N] NV có email lỗi." |
| NF01-E3 | **Kênh bị disable toàn hệ thống** — Admin tắt kênh Push | HIGH | Cảnh báo admin: "Tắt kênh Push sẽ ảnh hưởng [N] loại thông báo. Thông báo bắt buộc sẽ chuyển sang Email." |
