# US-SHIFT-07: Xem lịch phân ca team (Manager View)

---

**AS A** Quản lý / Trưởng phòng (MANAGER, DEPT_HEAD),  
**I WANT TO** xem lịch phân ca của tất cả nhân viên thuộc team/phòng ban trên giao diện calendar trực quan,  
**SO THAT** tôi có thể nắm bắt lịch làm việc team trong tuần/tháng, phát hiện thiếu hụt nhân lực sớm, và phối hợp với HR khi cần điều chỉnh phân ca.

---

### **1. BUSINESS FLOW**

1. **Truy cập**: Manager mở "Lịch phân ca team" → Tab "Team Schedule".
2. **Hiển thị**: Hệ thống tải lịch ca của tất cả NV thuộc `employee.managerId = currentUser` (MANAGER) hoặc `employee.departmentId` (DEPT_HEAD).
3. **View modes**: Manager chọn view: **Tuần** (mặc định) hoặc **Tháng**.
4. **Lọc**: Filter theo NV cụ thể, ca cụ thể, hoặc trạng thái (Đang làm / Nghỉ / OFF).
5. **Phát hiện gap**: Hệ thống highlight ô nếu ngày nào có < `minStaffThreshold` NV (cấu hình per-site bởi HR).
6. **Yêu cầu điều chỉnh**: Manager nhấn "Đề xuất đổi ca" → Hệ thống tạo request gửi HR → HR xử lý tại US-SHIFT-06.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Lịch ca team trực thuộc | MANAGER | Chỉ NV có `managerId = self`. Read-only. |
| Lịch ca toàn phòng ban | DEPT_HEAD | Tất cả NV trong `departmentId`. Read-only. |
| Lịch ca toàn site | SITE_MANAGER | Tất cả NV thuộc site. Read-only. |
| Nút "Đề xuất đổi ca" | MANAGER, DEPT_HEAD | Tạo request gửi HR — KHÔNG trực tiếp sửa ca. |
| Sửa lịch ca | (Không có) | Manager KHÔNG được sửa trực tiếp. Chỉ HR có quyền qua US-SHIFT-05/06. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Calendar Grid**

- **Tuần view**: Cột = 7 ngày (Thứ 2 → Chủ nhật). Hàng = NV. Mỗi ô hiển thị: Tên ca + giờ (VD: "Sáng 08:00-17:00").
- **Tháng view**: Cột = 30/31 ngày. Ô compact (chỉ hiện tên ca abbreviated + color code).
- **Color coding**: Ca sáng (Xanh), Ca chiều (Cam), Ca đêm (Tím), OFF (Xám nhạt), Nghỉ phép (Đỏ nhạt), Ngày lễ (Vàng).
- **Số lượng NV**: Footer bar hiển thị SUM NV có mặt per ngày — highlight nếu < threshold.

#### **AC2. Nhân sự summary per ngày**

- Khi nhấn vào cột ngày → Popup: Danh sách NV + Ca + Trạng thái (Đã check-in / Chưa check-in / Nghỉ phép / OFF).
- Badge summary: "X đang làm | Y nghỉ phép | Z OFF".
- Link drill-down: Nhấn vào NV → Xem nhật ký chấm công (US-ATTEN-03) với quyền RBAC Manager.

#### **AC3. Gap Detection (Understaffing Alert)**

- HR cấu hình `minStaffThreshold` per site per ca (VD: Ca sáng cần ≥ 5 NV).
- Ô calendar highlight đỏ nếu ngày đó có NV working < threshold.
- Tooltip: "Ca Sáng ngày 15/04: 3/5 NV (Thiếu 2 người)."
- Nút "Đề xuất bổ sung" → Form gửi HR: "Ngày X, Ca Y, Thiếu Z NV."

#### **AC4. Đề xuất đổi ca (Request)**

- Manager chọn NV + ngày + ca mới → Form "Đề xuất đổi ca" → Request gửi HR.
- Lý do bắt buộc (≥ 10 ký tự).
- Ghi chú: Manager KHÔNG trực tiếp sửa lịch ca. Chỉ đề xuất.
- HR nhận request tại M06 → Approve/Reject → Manager nhận thông báo kết quả.

---

### **4. DEFINITION OF DONE (DOD)**

1. **RBAC**: Manager chỉ thấy NV team mình. DEPT_HEAD thấy toàn phòng. Không sửa trực tiếp.
2. **Gap detection**: Threshold đúng. Highlight khi < min. Tooltip chính xác.
3. **Integration**: Lịch ca khớp với data từ US-SHIFT-05/06 (employee_shifts table).
4. **Hiệu năng**: Calendar load ≤ 2 giây cho team 50 NV × 30 ngày.
5. **QA**: Kiểm thử chuyển view tuần/tháng, filter, gap detection, đề xuất đổi ca.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SH07-E1 | **NV chưa được gán ca** — NV mới chưa có lịch | LOW | Ô trống (không màu). Tooltip: "Chưa phân ca." Đề xuất HR gán. |
| SH07-E2 | **Team > 50 NV** — DEPT_HEAD có 80 NV | MEDIUM | Virtual scroll hàng NV. Lazy load. Search NV by name. |
| SH07-E3 | **NV thuộc 2 ca cùng ngày** — Conflict chưa được xử lý | MEDIUM | Ô hiển thị 2 ca chồng + badge "⚠️ Xung đột" (Đỏ). Link HR: "Báo HR xử lý." |
| SH07-E4 | **Ngày lễ trùng ngày làm** — Ca đêm xuyên qua ngày lễ | LOW | Calendar hiển thị stripe: nửa ô = ca đêm (Tím), nửa ô = ngày lễ (Vàng). |
| SH07-E5 | **Manager nghỉ phép xem lịch team** — Delegate? | LOW | Vẫn cho phép xem read-only. Không ảnh hưởng approval flow. |
