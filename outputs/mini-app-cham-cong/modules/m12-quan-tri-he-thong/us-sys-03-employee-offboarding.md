# US-SYS-03: Employee Offboarding Workflow

---

**AS A** HR Admin,  
**I WANT TO** trigger quy trình offboarding tự động khi nhân viên nghỉ việc để hệ thống tự hủy đơn từ, freeze phép, deactivate C-Vision mapping, và re-route approval chain,  
**SO THAT** không có bước nào bị bỏ sót, dữ liệu được xử lý nhất quán, và quyền lợi NV (quyết toán phép, lương) được tính đúng.

---

### **1. BUSINESS FLOW**

1. **Trigger**: HR vào hồ sơ NV → Nhấn "Offboarding" → Nhập ngày hiệu lực (terminationDate) + lý do.
2. **Xác nhận**: Hệ thống hiển thị impact report: số đơn PENDING, phép còn lại, ca đang gán, mapping camera.
3. **Execute**: HR xác nhận → Hệ thống chạy workflow tự động (EAMS §12.1):

```
Offboarding Workflow (auto, ≤ 5 phút):
├── 1. Đơn PENDING (Leave/OT/Correction) → AUTO_CANCEL
│     Push NV: "Đơn [X] đã tự động hủy."
├── 2. Leave Balance → FREEZE
│     Tính phép chưa dùng → ghi vào payroll quyết toán
├── 3. Shift Assignment → REMOVE (từ terminationDate + 1)
├── 4. C-Vision Mapping → DEACTIVATE (soft-delete)
│     Webhook với personId cũ → ignored
├── 5. Approval Chain → RE-ROUTE
│     Đơn NV khác đang chờ NV này duyệt → fallback chain
│     Remove NV khỏi approver pool
├── 6. Notification → DEACTIVATE Push token
│     Gửi email cuối: "Tài khoản đã bị vô hiệu hóa"
└── 7. Employee Status → TERMINATED
```

4. **Report**: Hiển thị kết quả: "Offboarding hoàn tất. [N] hành động đã thực hiện."

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin | Role | Ghi chú |
| --- | --- | --- |
| Trigger Offboarding | SITE_HR_ADMIN (NV cùng site), GLOBAL_HR_ADMIN | Chỉ HR có quyền. |
| Xem Impact Report | HR Admin (trigger) | Preview trước khi execute. |
| Revert Offboarding | GLOBAL_HR_ADMIN, SUPER_ADMIN | Trong 48h. Sau 48h: không thể revert. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Impact Report (Preview)**

| Mục | Hiển thị |
| --- | --- |
| Đơn PENDING | Số lượng + danh sách (Leave: 2, OT: 1, Correction: 0) |
| Leave Balance | Phép còn lại: [X] ngày (sẽ quyết toán) |
| Shift Assignment | Ca đang gán: [Tên ca] (từ [DD/MM] — sẽ bị xóa) |
| C-Vision Mapping | [N] mapping active (sẽ deactivate) |
| Approval pending | [N] đơn NV khác đang chờ NV này duyệt (sẽ re-route) |

#### **AC2. Workflow Execution**

- Tất cả 7 bước chạy tuần tự trong 1 transaction.
- Nếu bước nào lỗi: rollback toàn bộ. Hiển thị lỗi cụ thể.
- Progress indicator: "Đang xử lý... [3/7] Xóa ca làm việc..."

#### **AC3. Revert (Undo)**

- Trong 48h: nút "Hoàn tác Offboarding" khả dụng.
- Revert: Restore status, re-create shift, re-activate mapping, refund phép.
- Sau 48h: nút disabled. Log: "Hết thời hạn hoàn tác."

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SY03-E1 | **NV là Manager đang approve đơn** — NV nghỉ việc có 15 đơn team đang PENDING | CRITICAL | Step 5: Auto-reassign tất cả đơn PENDING sang fallback (SITE_MANAGER → SITE_HR → GLOBAL_HR). Push cho NV bị ảnh hưởng: "Đơn đã chuyển đến [Approver mới]." |
| SY03-E2 | **NV có leave approved tuần sau** — Đã approved nhưng chưa diễn ra | HIGH | Auto-cancel. Hoàn phép: `balance.used -= days`. Log: "Leave request [ID] auto-cancelled due to offboarding." |
| SY03-E3 | **Offboarding NV đang trong ca đêm** — NV check-in lúc 22:00, offboarding trigger lúc 23:00 | MEDIUM | Cho phép ca hiện tại hoàn thành. Offboarding effective = ngày tiếp theo. Mốc check-out vẫn được ghi nhận. |
| SY03-E4 | **Revert sau khi NV đã bị xóa C-Vision mapping** — Mapping đã bị partner C-Vision xóa bên phía họ | MEDIUM | Revert tạo lại mapping trong EAMS nhưng cảnh báo: "Cần liên hệ C-Vision để re-enroll khuôn mặt NV." |
| SY03-E5 | **Double offboarding** — HR trigger 2 lần cho cùng NV | LOW | Lần 2 chặn: "NV [Tên] đã được offboarding ngày [DD/MM]." |

---

### **DEFINITION OF DONE (DOD)**

1. **AC Verified**: Impact report, 7-step workflow, revert hoạt động đúng.
2. **Transaction**: Workflow atomic — rollback nếu có bước lỗi.
3. **SLA**: Toàn bộ workflow ≤ 5 phút cho NV có 100 records.
4. **Audit Trail**: Log chi tiết mỗi bước (action, timestamp, result).
5. **Edge Cases Tested**: Manager offboarding, ca đêm, revert.
6. **Integration**: Tích hợp đúng với Module 01 (Chấm công), 07 (Lịch nghỉ), 08 (Camera), 10 (Phê duyệt).

---

### **GHERKIN SCENARIOS**

```gherkin
Feature: US-SYS-03 — Employee Offboarding
  As a HR Admin
  I want to trigger offboarding tự động (7 bước) khi NV nghỉ việc
  So that không bỏ sót bước, dữ liệu xử lý nhất quán.

  # --- AC1: Impact Report ---
  Scenario: AC1.1 — Preview trước execute
    Given NV emp-001: 2 đơn Leave PENDING, 5 ngày phép còn, ca Sáng, 1 mapping camera
    When HR nhấn "Offboarding"
    Then impact: Đơn PENDING=2, Leave Balance=5, Shift=Ca Sáng, Mapping=1, Approval queue=0

  # --- AC2: Workflow ---
  Scenario: AC2.1 — 7 bước tuần tự
    Given HR xác nhận offboarding emp-001
    When workflow chạy
    Then 1.Cancel đơn → 2.Freeze phép → 3.Remove shift → 4.Deactivate mapping → 5.Re-route approval → 6.Deactivate push → 7.Status=TERMINATED
    And hoàn tất ≤ 5 phút. Progress: "3/7 Xóa ca làm việc..."

  # --- AC3: Revert ---
  Scenario: AC3.1 — Hoàn tác trong 48h
    Given offboarding emp-001 thực hiện 10h trước
    When GLOBAL_HR nhấn "Hoàn tác"
    Then restore: ACTIVE, re-create shift, re-activate mapping, refund phép

  Scenario: AC3.2 — Quá 48h → disabled
    Given offboarding 50h trước
    When HR xem
    Then nút "Hoàn tác" disabled. Tooltip: "Hết thời hạn hoàn tác."

  # --- Edge Cases ---
  Scenario: Edge1 — NV là Manager có 15 đơn PENDING
    Given emp-001 là manager, 15 đơn team PENDING
    When offboarding step 5
    Then auto-reassign 15 đơn → fallback chain. Push NV bị ảnh hưởng.

  Scenario: Edge2 — Offboarding khi NV đang trong ca đêm
    Given NV check-in 22:00, HR trigger offboarding 23:00
    When hệ thống xử lý
    Then cho phép ca hoàn thành. Offboarding effective = ngày tiếp theo.

  Scenario: Edge3 — Double offboarding → chặn
    Given emp-001 đã offboarding
    When HR trigger lần 2
    Then chặn: "NV emp-001 đã được offboarding ngày [DD/MM]."
```
