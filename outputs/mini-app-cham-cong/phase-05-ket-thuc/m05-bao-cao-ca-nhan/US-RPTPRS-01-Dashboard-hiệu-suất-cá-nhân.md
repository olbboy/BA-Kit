# US-RPTPRS-01: Dashboard hiệu suất cá nhân

---

**AS A** Nhân viên,  
**I WANT TO** xem dashboard tổng hợp hiệu suất chuyên cần cá nhân gồm Score, tổng giờ làm, ngày nghỉ và giờ OT trong tháng,  
**SO THAT** tôi có thể tự đánh giá và chủ động cải thiện hiệu suất làm việc mà không cần hỏi HR.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** NV mở mục "Báo cáo cá nhân" trên Mini App.
2. **Khởi tạo dữ liệu:** Backend tổng hợp DailyAttendanceSummary, LeaveRequest, OvertimeRequest từ ngày 01 đến ngày hiện tại trong tháng.
3. **Hiển thị:** Dashboard gồm 4 widget chính + biểu đồ trend 4 tuần.
4. **Cập nhật:** Dữ liệu tự động refresh khi có sự kiện chấm công hoặc đơn từ được duyệt.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Score chuyên cần | Nhân viên, HR, Quản lý | ABAC: NV chỉ xem của mình. |
| Tổng giờ làm tháng | Nhân viên | Lấy từ DailyAttendanceSummary. |
| Biểu đồ trend | Nhân viên | Hiển thị dữ liệu 4 tuần gần nhất. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Widget Score chuyên cần**

- Công thức: Score = (Ngày đúng giờ / Tổng ngày làm việc thực tế) × 100.
- Hiển thị: Số tròn (VD: 92), dạng circular progress (Xanh ≥ 90, Vàng 70-89, Đỏ < 70).
- Không tính ngày lễ, ngày nghỉ phép vào mẫu số.

#### **AC2. Widget Tổng giờ làm**

- Công thức: SUM(netHours) từ ngày 01 đến hiện tại.
- Hiển thị: dạng "168.5h / 176h" (thực tế / quy định).
- Progress bar thể hiện % hoàn thành.

#### **AC3. Widget Ngày nghỉ & OT**

- Ngày nghỉ: COUNT đơn nghỉ APPROVED trong tháng. Hỗ trợ 0.5 ngày.
- Giờ OT: SUM giờ OT APPROVED trong tháng. Hiển thị dạng "12.5h".

#### **AC4. Biểu đồ Trend 4 tuần**

- Biểu đồ đường (line chart) hiển thị Score chuyên cần theo tuần (4 điểm dữ liệu).
- Mỗi điểm hiển thị tooltip: Tuần X, Score Y%, Số ngày trễ.
- Cho phép chuyển sang view tháng (12 điểm dữ liệu).

#### **AC5. Chọn kỳ báo cáo**

- Dropdown chọn tháng/năm. Mặc định: tháng hiện tại.
- Khi đổi tháng → Dashboard tải lại dữ liệu tương ứng.

---

### **4. DEFINITION OF DONE (DOD)**

1. **Độ chính xác:** Score phải khớp 100% với dữ liệu nhật ký chấm công (US-ATTEN-03).
2. **Hiệu năng:** Dashboard tải ≤ 2 giây.
3. **Responsive:** Hiển thị tốt trên mobile (single column) và web (grid layout).
4. **QA:** Kiểm thử với NV có 0 ngày chấm công, NV mới (< 1 tháng), NV có OT xuyên đêm.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RP01-E1 | **NV mới < 1 tháng** — Chưa đủ dữ liệu tính score | LOW | Dashboard hiển thị: "Chưa đủ dữ liệu (cần ≥ 1 tháng)." Ẩn biểu đồ trend. Hiển thị dữ liệu raw có sẵn. |
| RP01-E2 | **NV chuyển site giữa tháng** — Dữ liệu thuộc 2 site | MEDIUM | Gộp dữ liệu cả 2 site cho tháng hiện tại. Ghi chú: "Bao gồm dữ liệu từ [Site A] (01-15) và [Site B] (16-30)." |
| RP01-E3 | **Ca đêm ảnh hưởng tính toán ngày công** | MEDIUM | Ngày công tính theo ngày bắt đầu ca (VD: ca 22:00 T → 06:00 T+1 = ngày công T). |
