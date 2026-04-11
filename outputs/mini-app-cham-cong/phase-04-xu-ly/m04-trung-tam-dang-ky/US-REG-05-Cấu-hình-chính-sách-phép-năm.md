# US-REG-05: Cấu hình chính sách phép năm (Leave Policy Admin)

---

**AS A** HR Admin,  
**I WANT TO** cấu hình chính sách phép năm bao gồm số ngày cơ bản, thâm niên, carryover và pro-rata cho nhân viên mới,  
**SO THAT** hệ thống tự động tính đúng số dư phép cho từng nhân viên theo quy định công ty và Luật Lao động Việt Nam.

---

### **1. BUSINESS FLOW**

1. **Truy cập**: HR vào "Cấu hình chính sách phép" → Xem danh sách policy hiện tại.
2. **Tạo/Sửa policy**: Nhập các thông số: phép cơ bản, thâm niên, carryover, pro-rata.
3. **Gán policy**: Gán policy cho Site / Phòng ban / Nhóm NV cụ thể.
4. **Effective date**: Set ngày hiệu lực (thường 01/01 hàng năm).
5. **Batch recalculate**: Hệ thống tính lại `LeaveBalance` cho tất cả NV thuộc policy.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin | Role | Ghi chú |
| --- | --- | --- |
| Tạo/Sửa/Xóa Leave Policy | GLOBAL_HR_ADMIN | Policy áp dụng toàn hệ thống. |
| Gán policy cho Site | SITE_HR_ADMIN, GLOBAL_HR | SITE_HR chỉ gán cho site mình. |
| Xem policy hiện tại | HR, Manager | Read-only. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Cấu hình phép cơ bản**

| Thông số | Mô tả | Mặc định | Ràng buộc |
| --- | --- | --- | --- |
| `annualEntitlement` | Số ngày phép/năm | 12 | ≥ 12 (theo Luật LĐ VN) |
| `seniorityBonusDays` | Ngày phép thưởng thâm niên | 1 | ≥ 0 |
| `seniorityYears` | Mỗi N năm được thưởng | 5 | ≥ 1 |
| `maxCarryoverDays` | Số ngày phép chuyển tiếp tối đa | 5 | ≥ 0 |
| `carryoverExpiryDate` | Hạn sử dụng phép chuyển tiếp | 31/03 | DD/MM |
| `proRataEnabled` | Tính phép pro-rata cho NV mới | true | boolean |

#### **AC2. Công thức tính**

- **Phép năm**: `annualEntitlement + FLOOR(years_of_service / seniorityYears) × seniorityBonusDays`
  - VD: NV 7 năm → 12 + FLOOR(7/5) × 1 = 13 ngày.
- **Pro-rata (NV mới)**: `(entitlement × months_worked) / 12` (làm tròn 0.5 ngày)
  - VD: Vào tháng 7 → (12 × 6) / 12 = 6 ngày.
- **Carryover**: `MIN(unused_days, maxCarryoverDays)` → hết hạn sau `carryoverExpiryDate`.
  - VD: Năm 2025 dư 8 ngày → carryover 5 ngày → hết hạn 31/03/2026.

#### **AC3. Batch Recalculate**

- Khi policy thay đổi hoặc đầu năm mới: nút "Tính lại phép cho tất cả NV".
- Progress bar: "Đang tính... [N/M] nhân viên".
- Kết quả: "Đã cập nhật [M] NV. [X] NV có thay đổi phép."

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RG05-E1 | **Giảm phép khi NV đã dùng hết** — Policy cũ: 15 ngày, NV đã dùng 14. Policy mới: 12 ngày → Balance = -2 | HIGH | Cảnh báo HR: "[N] NV có balance âm sau thay đổi." Cho phép: balance âm → trừ lương kỳ tới. |
| RG05-E2 | **Carryover đã hết hạn** — Ngày 01/04, carryover chưa bị xóa | MEDIUM | Batch job 01/04 00:01: auto-expire carryover. NV nhận thông báo: "Phép chuyển tiếp [N ngày] đã hết hạn." |
| RG05-E3 | **NV chuyển site có policy khác** — NV chuyển từ Site A (15 ngày) sang Site B (12 ngày) | MEDIUM | Áp dụng policy Site B từ ngày chuyển. Phép đã dùng tính cộng dồn. Pro-rata cho số tháng còn lại. |
| RG05-E4 | **2 policy áp dụng cùng NV** — NV thuộc phòng ban có policy riêng + site có policy khác | HIGH | Ưu tiên: Policy cụ thể hơn wins (Phòng ban > Site > Global). Hiển thị: "Policy: [Tên] (nguồn: Phòng ban [X])." |

---

### **DEFINITION OF DONE (DOD)**

1. **AC Verified**: Công thức tính phép đúng theo Luật LĐ VN (≥ 12 ngày, thâm niên, pro-rata).
2. **Batch Performance**: Tính lại phép cho 5000 NV ≤ 30 giây.
3. **Carryover Logic**: Hết hạn tự động theo cấu hình.
4. **Edge Cases Tested**: Balance âm, NV chuyển site, policy conflict.
5. **Audit Trail**: Log thay đổi policy (old_value → new_value, changed_by).
