# US-SYS-05: Employee Onboarding Wizard

---

**AS A** HR Admin,  
**I WANT TO** thực hiện quy trình onboarding tập trung qua wizard 7 bước khi nhân viên mới gia nhập,  
**SO THAT** mọi cài đặt cần thiết (profile, site, shift, Face ID, phép, approval chain, thông báo) được hoàn thành nhanh, đồng bộ, tránh bỏ sót bước khi onboard hàng loạt.

---

### **1. BUSINESS FLOW**

1. **Bước 1 — Tạo/Xác nhận Profile**: HR tạo mới hoặc xác nhận NV từ Bulk Import (US-EMP-04). Verify: Mã NV, Họ tên, Email, Phòng ban, Chức vụ, joinDate.
2. **Bước 2 — Gán Site**: Chọn Primary Site cho NV. Nếu NV thuộc nhiều site → chọn primary + secondary sites.
3. **Bước 3 — Gán ca làm việc**: Chọn ca từ thư viện (US-SHIFT-01). Nếu ca xoay → chọn pattern (US-SHIFT-06). Preview lịch ca 30 ngày đầu.
4. **Bước 4 — Trigger Face ID Enrollment**: Gửi invitation Push/Email cho NV để tự đăng ký Face ID (US-CAM-04). Trạng thái: INVITATION_SENT.
5. **Bước 5 — Tính phép năm**: Tự động tính phép pro-rata dựa trên joinDate + policy công ty (US-REG-05). Hiển thị: "Phép năm = X ngày (pro-rata từ dd/MM)".
6. **Bước 6 — Thêm vào Approval Chain**: Tự động gán NV vào chain phê duyệt của phòng ban (US-APPR-02). HR confirm Manager trực tiếp.
7. **Bước 7 — Gửi Welcome Notification**: Push + Email: "Chào mừng [Tên] gia nhập [Site]. Ca: [Tên ca]. Phép: X ngày."
8. **Hoàn tất**: Checklist hiển thị 7/7 ✅. NV status = `ACTIVE`. NV có thể chấm công từ ngày làm việc đầu tiên.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Khởi tạo Onboarding Wizard | HR Admin | SITE_HR tạo cho NV thuộc site. GLOBAL_HR tạo cho mọi NV. |
| Gán site | HR Admin | Phải là site mà HR có quyền. |
| Gán ca làm việc | HR Admin | Chỉ ca thuộc site đã gán. |
| Xem Onboarding Dashboard | HR Admin, Manager | Trạng thái onboarding từng NV. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Wizard UI 7 bước**

- Stepper navigation: 7 bước, cho phép quay lại sửa bước trước.
- Mỗi bước có validation riêng. Không cho skip bước bắt buộc (1, 2, 3).
- Bước 4, 5, 6 có thể auto-fill (HR chỉ cần confirm).
- Progress bar hiển thị: "Bước 3/7 — Gán ca làm việc".

#### **AC2. Bulk Onboarding**

- Hỗ trợ chọn nhiều NV từ Bulk Import (US-EMP-04) → apply cùng 1 wizard.
- Bước 2-3: apply cùng site + shift cho toàn batch.
- Bước 4: invitation gửi hàng loạt (queue-based, 10 push/giây).
- Bước 5: tính phép pro-rata cho từng NV riêng (joinDate khác nhau).
- Progress: "Đang onboard: 45/200 NV..."

#### **AC3. Onboarding Dashboard**

- Tab mới trong Module 12: "Onboarding Tracker".
- Bảng: Mã NV, Tên, Bước hiện tại (1-7), Status (In Progress/Completed/Stuck), Ngày bắt đầu onboard.
- Filter: Phòng ban, Site, Status.
- NV stuck > 3 ngày → badge đỏ, push HR nhắc nhở.

#### **AC4. Integration với các module**

- Bước 2: tạo `SiteAssignment` → Module 12 (US-SYS-01).
- Bước 3: tạo `ShiftAssignment` → Module 02 (US-SHIFT-05/06).
- Bước 4: tạo `FaceEnrollmentInvitation` → Module 08 (US-CAM-04).
- Bước 5: tạo `LeaveBalance` → Module 04 (US-REG-05).
- Bước 6: tạo `ApprovalChainMembership` → Module 10 (US-APPR-02).
- Bước 7: trigger `WelcomeNotification` → Module 09 (US-NOTIF-02).

---

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SY05-E1 | **Bulk onboard 500 NV** — Factory opening, toàn bộ NV mới cùng ngày | HIGH | Queue-based processing. UI hiển thị progress real-time. NV không cần đợi — nhận push khi hoàn tất. Timeout: 30 phút max cho batch 500. |
| SY05-E2 | **NV thuộc 2 site** — NV IT hỗ trợ 2 chi nhánh | MEDIUM | Wizard cho phép chọn primary + secondary site. Ca gán theo primary site. Face ID enrollment gửi 1 lần (mapping áp dụng cho tất cả camera). |
| SY05-E3 | **Face ID enrollment fail** — NV không có smartphone hoặc từ chối | MEDIUM | Wizard vẫn hoàn tất (bước 4 = SKIPPED). Dashboard ghi chú: "Face ID chưa đăng ký". NV có thể đăng ký sau qua US-CAM-04. Attendance fallback = Manual Entry (US-ATTEN-05). |
| SY05-E4 | **Wizard bị gián đoạn** — HR đóng browser giữa chừng bước 4 | MEDIUM | Auto-save sau mỗi bước hoàn thành. HR mở lại → resume từ bước cuối. Draft tồn tại 7 ngày, sau đó tự xóa + alert HR. |

---

### **4. DEFINITION OF DONE (DOD)**

1. **End-to-end:** NV mới onboard qua wizard → chấm công Face ID ngày đầu → record đúng ca + site.
2. **Bulk:** Import 100 NV → wizard batch → tất cả ACTIVE trong ≤ 15 phút.
3. **Rollback:** Nếu wizard fail ở bước 5 → các bước 1-4 vẫn giữ. HR resume hoặc reset.
4. **Dashboard:** Onboarding tracker hiển thị chính xác status từng NV.
5. **QA:** Test single + bulk, resume after interruption, multi-site NV, Face ID skip.
