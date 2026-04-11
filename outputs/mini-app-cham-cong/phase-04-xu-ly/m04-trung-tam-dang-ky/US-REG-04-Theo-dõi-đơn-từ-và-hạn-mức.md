# US-REG-04: Theo dõi đơn từ và hạn mức

---

**AS A** Nhân viên,  
**I WANT TO** xem danh sách tất cả đơn đã gửi (nghỉ phép, đổi ca, OT) kèm trạng thái và hạn mức phép/OT còn lại,  
**SO THAT** tôi có thể theo dõi tiến độ phê duyệt và chủ động quản lý quyền lợi cá nhân.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** NV mở tab "Đơn từ của tôi" trong Trung tâm đăng ký.
2. **Xem danh sách:** Hệ thống hiển thị toàn bộ đơn đã gửi, sắp xếp mới nhất trước.
3. **Lọc:** NV có thể lọc theo: Loại đơn (Nghỉ phép/Đổi ca/OT), Trạng thái (Pending/Approved/Rejected), Khoảng thời gian.
4. **Xem chi tiết:** Nhấn vào đơn → Xem thông tin đầy đủ + lịch sử phê duyệt + lý do từ chối (nếu có).
5. **Hủy đơn:** NV có thể hủy đơn đang ở trạng thái PENDING.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Danh sách đơn cá nhân | Nhân viên | ABAC: Chỉ xem đơn của chính mình. |
| Hạn mức phép/OT | Nhân viên | ABAC: Chỉ xem hạn mức cá nhân. |
| Hủy đơn Pending | Nhân viên | Chỉ hủy đơn do chính mình tạo, chỉ khi PENDING. |
| Danh sách đơn team | Quản lý | Manager xem đơn team tại Module 10. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị danh sách đơn**

- Mỗi đơn hiển thị: Loại đơn (icon), Ngày/khoảng ngày, Badge trạng thái (Pending=Vàng, Approved=Xanh, Rejected=Đỏ, Cancelled=Xám).
- Sắp xếp: Mới nhất trên cùng.
- Phân trang: Tải 20 đơn/lần, infinite scroll.

#### **AC2. Xem chi tiết đơn**

- Hiển thị toàn bộ thông tin đơn: loại, ngày, lý do, file đính kèm.
- **Lịch sử phê duyệt:** Timeline hiển thị: Ai duyệt → Thời điểm → Kết quả (Approved/Rejected).
- **Lý do từ chối:** Nếu đơn bị Rejected, hiển thị rõ lý do từ approver.

#### **AC3. Hủy đơn**

- Nút "Hủy đơn" chỉ hiển thị khi đơn ở trạng thái PENDING.
- Khi hủy: Hệ thống confirm "Bạn có chắc muốn hủy đơn này?" → Nếu xác nhận → Status = CANCELLED.
- Nghỉ phép bị hủy: balance.pending -= workingDays (hoàn lại pending balance).
- Đơn đã APPROVED: KHÔNG cho phép hủy (chặn nút).

#### **AC4. Widget hạn mức**

- Hiển thị tại đầu trang:
  - **Phép năm:** Đã dùng / Tổng (VD: 5/12 ngày). Progress bar.
  - **Phép chuyển tiếp:** Còn lại / Đã dùng. Ngày hết hạn.
  - **OT tháng:** X/40 giờ.
  - **OT năm:** X/200 giờ.

---

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| R04-E1 | **Self-approval** — NV đồng thời là Manager, gửi đơn và tự duyệt cho chính mình | CRITICAL | **Chặn tuyệt đối.** Backend validate: requestor.id !== approver.id. Nếu NV là Manager → đơn tự động skip level 1, chuyển lên DEPT_HEAD hoặc SITE_HR. Ghi audit: "Self-approval blocked — escalated to [approver]". |
| R04-E2 | **Approver đi nghỉ** — Manager nghỉ phép 2 tuần, đơn team bị treo | HIGH | Auto-delegation: nếu approver có đơn nghỉ APPROVED trùng ngày → fallback chain tự động kích hoạt (EAMS §7.3): DIRECT_MANAGER → SITE_MANAGER → SITE_HR → GLOBAL_HR. Push cho NV: "Đơn đã chuyển đến [Tên approver mới] do quản lý đang nghỉ phép". |

---

### **4. DEFINITION OF DONE (DOD)**

1. **Hủy đơn:** Kiểm thử hủy đơn PENDING → Balance phải hoàn lại đúng. Hủy đơn APPROVED → Phải bị chặn.
2. **Lý do từ chối:** Kiểm thử đơn bị reject → Lý do hiển thị đúng từ approver.
3. **Hiệu năng:** Tải danh sách 100+ đơn ≤ 2 giây.
4. **QA:** Kiểm thử lọc kết hợp nhiều điều kiện; pagination; **self-approval blocked; approver delegation**.
