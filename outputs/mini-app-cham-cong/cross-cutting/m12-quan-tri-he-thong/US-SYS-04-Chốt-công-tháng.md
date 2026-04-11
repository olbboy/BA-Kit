# US-SYS-04: Chốt công tháng (Period Closing)

---

**AS A** HR Admin,  
**I WANT TO** cấu hình và thực hiện chốt công hàng tháng để khóa dữ liệu chấm công sau ngày chốt,  
**SO THAT** dữ liệu payroll không bị thay đổi ngoài kiểm soát, và mọi điều chỉnh sau chốt phải qua quy trình Exception Approval có audit trail.

---

### **1. BUSINESS FLOW**

1. **Cấu hình**: SYS_ADMIN thiết lập tham số chốt công cho từng site: `closingDay` (1-28), `graceDays`, `weekendRule`.
2. **Auto-trigger**: Hệ thống tự động chốt vào `closingDay` hàng tháng (cron job 00:00). Nếu ngày chốt rơi vào T7/CN → áp dụng `weekendRule` (PREV_WORKDAY hoặc NEXT_WORKDAY).
3. **Grace period**: Trong `graceDays` ngày sau chốt, NV vẫn được gửi giải trình correction cuối cùng.
4. **Lock**: Sau grace period → toàn bộ dữ liệu tháng chuyển `LOCKED`. Đơn giải trình bị disable. Vi phạm chưa xử lý → "VI PHẠM QUY CHẾ" vĩnh viễn.
5. **Exception unlock**: Chỉ GLOBAL_HR / SYS_ADMIN có thể mở khóa cho từng NV + ngày cụ thể, kèm lý do. Giới hạn: ≤ 30 ngày sau chốt.
6. **Thông báo**: Push notification toàn site trước 3 ngày: "Còn X ngày đến hạn chốt công. Vui lòng giải trình các lỗi tồn đọng."

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Cấu hình closingDay, graceDays | SYS_ADMIN | Cấu hình per-site. |
| Xem trạng thái chốt (OPEN/LOCKED) | HR Admin, Manager | HR xem toàn site; Manager xem team. |
| Exception Unlock | GLOBAL_HR, SYS_ADMIN | Unlock từng NV + ngày. Audit log bắt buộc. |
| Xem lịch sử chốt | HR Admin | Danh sách các kỳ chốt kèm timestamp, người thực hiện. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Cấu hình chốt công per-site**

- Form: dropdown `closingDay` (1-28), input `graceDays` (0-7, default: 3), dropdown `weekendRule` (PREV_WORKDAY / NEXT_WORKDAY).
- Scope: mỗi site cấu hình riêng (`closingScope = PER_SITE`).
- Validation: `closingDay` phải nằm trong 1-28 (tránh ngày 29-31 không tồn tại ở một số tháng).

#### **AC2. Auto-closing trigger**

- Cron job chạy 00:00 vào `closingDay` (hoặc ngày điều chỉnh theo `weekendRule`).
- Trạng thái kỳ: `OPEN` → `GRACE` → `LOCKED`.
- Trong GRACE: NV vẫn gửi được giải trình nhưng không tạo đơn mới (nghỉ phép, OT cho tháng cũ).
- Sau GRACE → LOCKED: nút "Giải trình" cho ngày thuộc tháng cũ bị disabled. Tooltip: "Kỳ đã chốt. Liên hệ HR để mở khóa."

#### **AC3. Exception Unlock**

- Form: chọn NV + chọn ngày + nhập lý do ngoại lệ.
- Constraint: ngày phải thuộc kỳ LOCKED và ≤ 30 ngày kể từ closing date.
- Sau unlock: NV có 24h để gửi giải trình. Hết 24h → tự re-lock.
- Mỗi unlock tạo 1 audit log entry: `{actor, employee, date, reason, timestamp}` — immutable, append-only.

#### **AC4. Dashboard trạng thái chốt**

- HR Dashboard hiển thị: Kỳ hiện tại (OPEN/GRACE/LOCKED), ngày chốt kế tiếp, countdown.
- Danh sách NV có lỗi tồn đọng chưa giải trình (highlight đỏ).
- Badge summary: X lỗi đã xử lý / Y lỗi tồn đọng / Z sẽ thành "Vi phạm quy chế" nếu không xử lý.

---

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SY04-E1 | **Closing day = T7/CN** — Ngày 25 rơi vào Chủ nhật | MEDIUM | `weekendRule = PREV_WORKDAY`: chốt Thứ 6 (24). Hiển thị ngày chốt thực tế trên dashboard. Push notification điều chỉnh. |
| SY04-E2 | **NV gửi giải trình sát giờ chốt** — NV submit lúc 23:59, chốt lúc 00:00 | HIGH | Accept nếu submit timestamp < closing timestamp (server time). Race condition: dùng DB transaction isolation. |
| SY04-E3 | **Cron job fail** — Server down vào ngày chốt | CRITICAL | Retry mechanism: job monitor kiểm tra mỗi giờ. Nếu chốt chưa chạy → auto-trigger. Alert SYS_ADMIN. Không bao giờ skip chốt. |
| SY04-E4 | **200 NV có lỗi tồn đọng** — Chốt sẽ khiến 200 NV bị "Vi phạm quy chế" | HIGH | Trước khi GRACE → LOCKED: dashboard cảnh báo đỏ "200 NV sẽ bị ghi nhận vi phạm quy chế". HR phải confirm hoặc extend grace period (+1-3 ngày, max 1 lần). |

---

### **4. DEFINITION OF DONE (DOD)**

1. **End-to-end:** Kỳ chuyển OPEN → GRACE → LOCKED đúng timeline. Giải trình bị disabled sau LOCKED.
2. **Exception:** GLOBAL_HR unlock → NV giải trình thành công → re-lock tự động sau 24h.
3. **Audit:** Mọi unlock/re-lock được ghi audit log immutable. Không thể xóa/sửa log.
4. **Notification:** Push trước 3 ngày + push khi chốt + push cho NV có lỗi tồn đọng.
5. **QA:** Test cron job, weekend rule, race condition, exception unlock.
