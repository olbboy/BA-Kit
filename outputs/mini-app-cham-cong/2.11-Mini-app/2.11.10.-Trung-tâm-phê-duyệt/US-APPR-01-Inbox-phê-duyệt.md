# US-APPR-01: Inbox phê duyệt

---

**AS A** Quản lý / HR Admin,  
**I WANT TO** xem danh sách tất cả đơn chờ phê duyệt tại một giao diện tập trung, duyệt hoặc từ chối trong ≤ 2 tap trên mobile kèm lý do,  
**SO THAT** tôi không bỏ sót đơn từ của nhân viên và xử lý kịp thời để không ảnh hưởng đến quyền lợi của họ.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** Approver mở "Trung tâm phê duyệt" → Tab "Inbox".
2. **Xem danh sách:** Hiển thị đơn chờ duyệt thuộc quyền của approver hiện tại.
3. **Lọc:** Theo loại (Leave/OT/Correction/ShiftChange), theo NV, theo ngày gửi.
4. **Xem chi tiết:** Nhấn đơn → Hiển thị thông tin đầy đủ + file đính kèm.
5. **Duyệt/Từ chối:**
   - Duyệt: Nhấn "Phê duyệt" → Đơn chuyển sang level tiếp (nếu multi-level) hoặc Final APPROVED.
   - Từ chối: Nhấn "Từ chối" → Nhập lý do bắt buộc → Đơn chuyển REJECTED.
6. **Thông báo:** NV nhận Push notification với kết quả.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Đơn chờ duyệt | MANAGER, DEPT_HEAD, SITE_HR, GLOBAL_HR | Chỉ xem đơn thuộc quyền duyệt. |
| Duyệt/Từ chối | Approver tại level hiện tại | Chỉ approver được assign mới có quyền. |
| Lý do từ chối | Approver | Bắt buộc nhập khi từ chối. |
| File đính kèm | Approver | Xem file NV đính kèm (ảnh, PDF). |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị Inbox**

- Badge số đơn chưa duyệt trên icon Trung tâm phê duyệt.
- Danh sách hiển thị: Tên NV, Ảnh, Loại đơn (icon), Ngày gửi, Khoảng ngày/giờ yêu cầu, Mức ưu tiên.
- Sắp xếp: Đơn gần ngày chốt công ở trên cùng → Đơn cũ nhất → Đơn mới nhất.
- Phân trang: 20 đơn/trang.

#### **AC2. Chi tiết đơn**

- Hiển thị đầy đủ: Loại, ngày, lý do, file đính kèm (preview ảnh/PDF inline).
- **Leave:** Loại phép, khoảng ngày, số ngày, hạn mức phép còn lại của NV.
- **OT:** Mốc giờ, hệ số, giờ OT lũy kế tháng/năm của NV.
- **Correction:** Mốc giờ gốc → Mốc giờ yêu cầu sửa, lý do, ảnh minh chứng.
- **ShiftChange:** Ca cũ → Ca mới, lý do.

#### **AC3. Duyệt / Từ chối**

- **Duyệt:** 1 nhấn → Confirm → Đơn chuyển trạng thái.
- **Từ chối:** Nhấn → Modal nhập lý do (bắt buộc, ≥ 10 ký tự) → Confirm.
- Sau xử lý: Đơn biến mất khỏi inbox; NV nhận thông báo kèm lý do (nếu từ chối).

#### **AC4. Multi-level approval**

- Khi đơn cần nhiều level:
  - Level 1 APPROVED → Đơn chuyển sang inbox Level 2.
  - Tất cả levels APPROVED → Final APPROVED → Áp dụng.
  - Bất kỳ level REJECTED → Final REJECTED.
- Hiển thị progress: "Level 1/3 — Đã duyệt bởi [Tên Manager]".

---

### **4. DEFINITION OF DONE (DOD)**

1. **Đúng quyền:** Manager chỉ thấy đơn team mình; SITE_HR thấy đơn toàn site.
2. **Lý do từ chối:** Kiểm thử từ chối không nhập lý do → Phải bị chặn.
3. **Multi-level:** Kiểm thử luồng 3 level → Đơn chuyển đúng thứ tự.
4. **QA:** Kiểm thử: approver fallback (manager nghỉ phép), duyệt sau ngày chốt (phải bị chặn).

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| AP01-E1 | **Approver bị terminated** — Manager nghỉ việc khi có đơn PENDING | CRITICAL | Auto-reassign sang fallback chain (SITE_MANAGER → SITE_HR → GLOBAL_HR). Push NV: "Đơn đã chuyển đến [Approver mới]." Audit: "Auto-reassigned." |
| AP01-E2 | **Self-approve** — Manager gửi đơn nghỉ cho chính mình duyệt | HIGH | Chặn self-approve. Auto-route lên DEPT_HEAD hoặc SITE_HR. |
| AP01-E3 | **Approver offline > 7 ngày** — Không duyệt đơn nào trong 7 ngày | MEDIUM | Auto-escalate lên level tiếp. Alert HR: "[Tên] có [N] đơn quá hạn." Không auto-approve. |
| AP01-E4 | **Đơn tạo sát ngày chốt công** — Đơn tạo ngày 24, chốt công ngày 25 | MEDIUM | Cảnh báo approver: "Đơn này cần duyệt trước [DD/MM] (ngày chốt công)." Push reminder 24h trước. |
