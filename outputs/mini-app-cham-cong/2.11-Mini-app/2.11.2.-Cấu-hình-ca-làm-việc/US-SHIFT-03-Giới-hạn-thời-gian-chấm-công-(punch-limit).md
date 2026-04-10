# US-SHIFT-03: Giới hạn thời gian chấm công (punch limit)

---

**AS A** HR,  
**I WANT TO** giới hạn khung giờ cho phép Check-in sớm và Check-out muộn so với giờ ca chính thức,  
**SO THAT** hệ thống không ghi nhận dữ liệu "ngoại lai" (quẹt thẻ quá sớm hoặc quá muộn vô ích), giúp bảo vệ tính chính xác của dữ liệu báo cáo chuyên cần.

---

### **1. BUSINESS FLOW**

1. Thiết lập: HR nhập tham số số giờ giới hạn (vd: 3 giờ).
2. Giới hạn In: Hệ thống chỉ chấp nhận mốc quẹt nếu Check_in >= (Giờ Vào Ca - 3h).
3. Giới hạn Out: Hệ thống chỉ cập nhật mốc quẹt cuối cùng nếu Check_out <= (Giờ Tan Ca + 3h).

---

### **2. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Cấu hình Tham số Giới hạn**

- Tham số 1: "Cho phép Check-In sớm tối đa (giờ)".
- Tham số 2: "Cho phép Check-out muộn tối đa (giờ)".
- Kiểu dữ liệu: Số nguyên (vd: 2, 3, 5...).
- Check validate

#### **AC2. Logic xác thực mốc quẹt (Validation Logic)**

- **Trường hợp quẹt sớm quá mức**: NV quẹt lúc 04:00 AM cho ca làm 08:00 AM (Giới hạn là 3h) ➔ Backend bỏ qua mốc quẹt này, không hiển thị Badge "Đã chấm công".
- **Trường hợp làm thêm giờ (OT)**: Nếu ca làm việc kết thúc lúc 17:30 (Giới hạn ra 3h là đến 20:30), nhưng nhân viên có **Đơn OT** được duyệt đến 22:00 ➔ Hệ thống tự động mở khung giới hạn Check-out ra đến 22:30 để ghi nhận dữ liệu.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin | Role | Ghi chú |
| --- | --- | --- |
| Cấu hình punch limit | HR Admin | Chỉ HR mới được thay đổi giới hạn. |
| Xem cấu hình hiện tại | HR, Quản lý | Read-only cho Quản lý. |

---

### **3. DEFINITION OF DONE (DOD)**

1. **Dữ liệu rác**: Kiểm thử với mốc quẹt nằm ngoài khung giới hạn ➔ Đảm bảo không làm sai lệch mốc giờ "Vào/Ra" trên Dashboard của nhân viên.
2. **Thông báo**: Khi NV quẹt ngoài khung, Camera vẫn báo thành công, nhưng App sẽ không hiển thị cập nhật trạng thái làm việc.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SH03-E1 | **Punch limit = 0** — HR set giờ giới hạn = 0 phút | HIGH | Validation: "Giới hạn chấm công phải ≥ 30 phút." Chặn lưu. |
| SH03-E2 | **Punch limit > 24h** — Nhập giá trị vô lý | HIGH | Validation: "Giới hạn chấm công không được vượt quá 24 giờ." |
| SH03-E3 | **NV quẹt ngoài punch limit** — Quẹt trước giờ cho phép | MEDIUM | Mốc quẹt bị reject với status OUTSIDE_PUNCH_LIMIT. NV nhận thông báo: "Chấm công ngoài giới hạn thời gian cho phép." |
| SH03-E4 | **Ca đêm cross-midnight punch** — Punch limit ca 22:00-06:00 bao gồm 2 ngày | MEDIUM | Giới hạn tính liên tục qua 00:00 (VD: từ 21:00 T đến 07:00 T+1). Không bị cắt tại nửa đêm. |
