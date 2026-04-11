# US-SHIFT-06: Phân ca theo Pattern (Ca xoay/luân phiên)

---

**AS A** HR Admin,  
**I WANT TO** thiết lập lịch phân ca xoay tự động theo pattern (VD: Sáng → Chiều → Đêm → Nghỉ) lặp lại trong khoảng thời gian xác định,  
**SO THAT** tôi không phải gán ca thủ công từng ngày cho nhân viên làm ca luân phiên, giảm lỗi phân ca và tiết kiệm thời gian quản lý.

---

### **1. BUSINESS FLOW**

1. **Tạo Pattern**: HR vào "Phân ca theo Pattern" → Đặt tên (VD: "Ca xoay 4 ngày") → Kéo thả các ca vào slot.
2. **Cấu hình chu kỳ**: Pattern = [CA_SANG, CA_CHIEU, CA_DEM, OFF] → Hệ thống tự lặp lại.
3. **Gán NV**: Chọn NV/nhóm NV → Chọn ngày bắt đầu → Chọn ngày kết thúc (hoặc "Không giới hạn").
4. **Preview**: Hệ thống hiển thị lịch ca 30 ngày tới dạng calendar grid để HR xác nhận.
5. **Generate**: Hệ thống tạo `ShiftAssignment` cho từng ngày × NV (unique constraint: tenant + employee + date).
6. **Xử lý conflict**: Nếu NV đã có ca tại ngày X → Hiển thị conflict list → HR chọn: Ghi đè / Bỏ qua / Hủy.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin | Role | Ghi chú |
| --- | --- | --- |
| Tạo/Sửa/Xóa Pattern | HR Admin | GLOBAL_HR: toàn hệ thống. SITE_HR: ca thuộc site mình. |
| Gán Pattern cho NV | HR Admin | ABAC: chỉ gán cho NV thuộc site mình (trừ GLOBAL_HR). |
| Xem Pattern hiện tại | HR, Manager | Manager xem read-only lịch ca team. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Pattern Builder**

- Drag-and-drop ca vào slot (mỗi slot = 1 ngày trong chu kỳ).
- Slot đặc biệt: `OFF` (nghỉ), `FLEX` (NV tự chọn).
- Chu kỳ tối thiểu: 2 ngày. Tối đa: 31 ngày.
- Hiển thị tổng giờ làm/tuần trung bình dựa trên pattern.

#### **AC2. Preview Calendar**

- Hiển thị lịch ca 30 ngày tới cho mỗi NV dạng grid (cột = ngày, hàng = NV).
- Highlight conflict: ô màu đỏ nếu NV đã có ca khác.
- Hiển thị ngày lễ/nghỉ (Module 07) trên calendar — ca trùng ngày lễ được đánh dấu.

#### **AC3. Conflict Resolution**

- Khi gán pattern gặp conflict:
  - **Ghi đè**: Xóa ca cũ, gán ca mới. Log: "Ca [Tên ca cũ] bị thay thế bởi pattern [Tên pattern]."
  - **Bỏ qua**: Giữ ca cũ, không gán ca mới cho ngày đó.
  - **Hủy**: Dừng toàn bộ gán pattern.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SH06-E1 | **Pattern vượt ngày chốt công** — Gán pattern từ ngày 20 (tháng N) qua ngày 25 (chốt) | MEDIUM | Cảnh báo: "Pattern bao gồm ngày sau chốt công [DD/MM]. Ca sau ngày chốt thuộc kỳ lương tháng sau." |
| SH06-E2 | **NV nghỉ việc giữa pattern** — NV terminate ngày 15, pattern đến ngày 30 | MEDIUM | Hệ thống auto-delete ShiftAssignment từ terminationDate + 1. Log: "Đã hủy ca từ [DD/MM] do NV nghỉ việc." |
| SH06-E3 | **Xóa pattern đang active** — 200 NV đang dùng pattern này | HIGH | Confirm: "Pattern đang gán cho [200] NV. Xóa sẽ hủy tất cả ca tương lai (không ảnh hưởng quá khứ). Tiếp tục?" |
| SH06-E4 | **Ca trong pattern bị deactivate** — VD: "Ca Đêm" bị tắt nhưng pattern vẫn dùng | HIGH | Validation khi generate: "Ca [Tên] đã bị deactivate. Không thể tạo lịch. Cập nhật pattern trước." |

---

### **DEFINITION OF DONE (DOD)**

1. **AC Verified**: Pattern Builder, Preview Calendar, Conflict Resolution hoạt động đúng.
2. **Performance**: Generate lịch 30 ngày cho 500 NV ≤ 10 giây.
3. **Constraint**: Unique constraint (tenant + employee + date) không bị vi phạm.
4. **Edge Cases Tested**: Cross-payroll, NV nghỉ việc, ca deactivate.
5. **Integration**: Ca từ pattern hiển thị đúng trên US-ATTEN-01 (Hub chấm công).
