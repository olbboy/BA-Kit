# US-EXPL-01: Danh sách lỗi cần giải trình

---

**AS A** Nhân viên,  
**I WANT TO** xem danh sách các lỗi chấm công (quên check-out, vào muộn, về sớm) kèm theo thông tin hạn định giải trình trước ngày chốt công,  
**SO THAT** tôi nắm được ngày công nào đang bị lỗi và xử lý kịp thời trước khi hệ thống tự động khóa và ghi nhận vi phạm quy chế vĩnh viễn.

---

### **1. BUSINESS FLOW**

1. **Phát hiện lỗi (Real-time Detection)**: Hệ thống AI quét và đẩy các mốc sai lệch công (Anomaly) vào danh sách.
2. **Thời gian ân hạn (Grace Period)**: Nhân viên thấy nút **"CHỜ GIẢI TRÌNH"** màu đỏ, cho phép thực hiện sửa đổi dữ liệu.
3. **Ngày chốt công (Closing Date Trigger)**: Khi đến ngày chốt công (VD: Ngày 25 hàng tháng), hệ thống tự động quét toàn bộ đơn đang ở trạng thái "Chờ giải trình" của tháng cũ.
4. **Khóa & Ghi nhận vi phạm (Enforcement)**:    - Hệ thống **ẩn/vô hiệu hóa** nút giải trình cho các ngày công tháng cũ.
    - Trạng thái của thẻ lỗi chuyển thành **"VI PHẠM QUY CHẾ"** (Màu đỏ sẫm).
    - Ghi mốc "Vi phạm tuân thủ" vào hồ sơ chuyên cần của nhân viên.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Danh sách lỗi/vi phạm | Nhân viên, HR, Quản lý | ABAC: NV xem của mình; Quản lý xem của Team. |
| Thao tác giải trình | Nhân viên | Chỉ được thực hiện trước ngày chốt công. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị Trạng thái theo Thời gian (Timeline Status Logic)**

- **Case 1 (Còn hạn - Actionable)**: `Ngày hiện tại <= Ngày chốt công hằng tháng`.    - Nút hiển thị màu đỏ cam: **"CHỜ GIẢI TRÌNH"**.
    - Cho phép nhấn để mở Form giải trình.

- **Case 2 (Quá hạn - Violation Record)**: `Ngày hiện tại > Ngày chốt công hằng tháng`. (Đối với các ngày công thuộc tháng cũ).    - Nút chuyển sang màu đỏ sẫm: **"VI PHẠM QUY CHẾ"**.
    - Vô hiệu hóa (Disable) tính năng nhấn/mở form.
    - Hiển thị dòng thông báo nhỏ: *"Đã quá hạn giải trình cho ngày công này"*.

#### **AC2. Logic Hiển thị Widget Cảnh báo (Compliance Summary)**

- Hiển thị Badge số lượng lỗi tồn tại: `[X] lỗi mới cần giải trình`.
- Nếu có lỗi sắp đến ngày chốt (VD: còn 1 ngày), hệ thống hiển thị Badge **"Khẩn cấp"** (Màu đỏ nháy nhẹ) để hối thúc nhân viên.

#### **AC3. Ghi nhận vi phạm vĩnh viễn (Audit Log)**

- Sau mốc chốt công, trạng thái "Vi phạm quy chế" được lưu vĩnh viễn vào hệ thống (Immutable).
- Mọi yêu cầu sửa đổi sau ngày chốt phải thông qua quy trình **"Duyệt ngoại lệ (Exception Approval)"** của HR Admin trên hệ thống Quản trị (Admin Portal).

---

### **4. DEFINITION OF DONE (DOD)**

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| E01-E1 | **Ngày chốt công vào T7/CN/Lễ** — Ngày 25 là Chủ nhật | MEDIUM | Quy tắc: đẩy về ngày làm việc gần nhất TRƯỚC ngày chốt (tức thứ 6 ngày 24). Cấu hình tại Module 10 (Phê duyệt). |
| E01-E2 | **HR đã sửa công trước khi NV giải trình** — HR nhập thủ công (Manual Entry) cho ngày X, NV vẫn thấy lỗi ngày X | HIGH | Cross-check: nếu ngày X đã có Manual Entry APPROVED → ẩn lỗi, hiển thị "Đã được HR điều chỉnh". Nếu NV đã tạo đơn giải trình → thông báo "Ngày công này đã được HR xử lý — đơn giải trình sẽ tự động hủy". |
| E01-E3 | **Giải trình cho ngày chưa kết thúc** — NV thấy "Thiếu check-out" lúc 15:00 nhưng ca kết thúc 17:30 | MEDIUM | Hệ thống chỉ tạo anomaly "Thiếu check-out" sau khi: ca kết thúc + lateCheckOutMinutes (punch limit) + 1 giờ buffer. Trước mốc đó → không hiển thị lỗi thiếu quẹt. |
| E01-E4 | **Exception Approval sau chốt công** — Cần workflow duyệt ngoại lệ cho đơn tháng cũ | CRITICAL | **Workflow bổ sung:** Chỉ GLOBAL_HR hoặc SYS_ADMIN có quyền mở khóa (Unlock) đơn giải trình sau chốt. Form "Yêu cầu mở khóa": chọn NV + ngày + lý do ngoại lệ. Mọi Unlock được ghi audit log immutable. Giới hạn: tối đa 30 ngày sau chốt công. |

---

### **4. DEFINITION OF DONE (DOD)**

1. **Logic Locking**: Kiểm thử chuyển ngày hệ thống sang ngày 26 (sau ngày chốt 25) ➔ Đảm bảo tất cả đơn tháng cũ bị khóa nút "Giải trình".
2. **Thông báo**: Hệ thống tự động gửi Push cảnh báo trước 24h khi đến ngày chốt công cho các nhân viên có lỗi tồn đọng.
3. **UI/UX**: Trạng thái "Vi phạm quy chế" phải trông khác biệt rõ rệt so với "Chờ giải trình" để người dùng nhận thức được mức độ nghiêm trọng.
4. **Data Persistence**: Vi phạm không bị mất đi kể cả khi nhân viên cài lại App hoặc chuyển thiết bị.
5. **Exception Approval**: Kiểm thử GLOBAL_HR mở khóa đơn sau chốt → đơn được xử lý + audit log ghi đầy đủ.
