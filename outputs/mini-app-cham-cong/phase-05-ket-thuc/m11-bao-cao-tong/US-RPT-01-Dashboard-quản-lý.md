# US-RPT-01: Dashboard quản lý

---

**AS A** Quản lý / HR Admin,  
**I WANT TO** xem dashboard tổng hợp chuyên cần toàn phòng ban/chi nhánh với biểu đồ trực quan,  
**SO THAT** tôi có thể nắm bắt tình hình nhân sự, phát hiện vấn đề sớm và ra quyết định quản trị dựa trên dữ liệu.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** Manager/HR mở "Báo cáo tổng" → Dashboard.
2. **Hiển thị:** 6 counter cards + Biểu đồ chuyên cần + Top NV vi phạm + Xu hướng.
3. **Lọc:** Theo phòng ban, chi nhánh, khoảng thời gian.
4. **Drill-down:** Nhấn vào metric → Xem danh sách NV chi tiết.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Dashboard team | MANAGER, DEPT_HEAD | Chỉ xem NV thuộc team/phòng ban. |
| Dashboard site | SITE_HR, SITE_MANAGER | Xem toàn bộ NV site. |
| Dashboard toàn hệ thống | GLOBAL_HR, SYS_ADMIN | Xem tất cả site. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Counter Cards (6 metrics)**

| Metric | Nguồn | Mô tả |
| --- | --- | --- |
| Tổng NV | EmployeeAggregator | Số NV active thuộc scope |
| Có mặt | AttendanceAggregator | PRESENT + EARLY_LEAVE hôm nay |
| Đi trễ | AttendanceAggregator | LATE + LATE_AND_EARLY hôm nay |
| Vắng mặt | Tính toán | Tổng - Có mặt - Nghỉ phép - Chưa check-in |
| Nghỉ phép | LeaveAggregator | Đơn APPROVED trùng hôm nay |
| Chờ phê duyệt | ApprovalAggregator | PENDING của approver hiện tại |

#### **AC2. Biểu đồ chuyên cần theo phòng ban**

- Dạng: Bar chart hoặc Donut chart.
- Mỗi phòng ban: % Đúng giờ, % Trễ, % Vắng.
- Cho phép chuyển view: Hôm nay / Tuần này / Tháng này.

#### **AC3. Top NV vi phạm**

- Danh sách top 10 NV đi muộn/về sớm nhiều nhất trong tháng.
- Mỗi dòng: Ảnh, Tên, Phòng ban, Số lần trễ, Tổng phút trễ.
- Sắp xếp: Nhiều vi phạm nhất ở trên.

#### **AC4. Xu hướng 7/30 ngày**

- Biểu đồ đường: Trục X = ngày, Trục Y = % có mặt.
- Toggle: 7 ngày / 30 ngày.
- Hiển thị đường trung bình (average line) để so sánh.

#### **AC5. Drill-down**

- Nhấn vào counter card "Đi trễ" → Hiển thị danh sách NV đi trễ hôm nay.
- Nhấn vào phòng ban trên biểu đồ → Drill-down xem NV phòng đó.

---

### **4. DEFINITION OF DONE (DOD)**

1. **Dữ liệu:** Counter phải khớp: Tổng = Có mặt + Trễ + Vắng + Nghỉ phép.
2. **RBAC:** Manager chỉ thấy data team mình; GLOBAL_HR thấy tất cả.
3. **Hiệu năng:** Dashboard tải ≤ 3 giây cho 5,000+ NV.
4. **QA:** Kiểm thử drill-down; chuyển view thời gian; biểu đồ với 0 NV.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RT01-E1 | **Phòng ban không có dữ liệu** — Phòng ban mới tạo, chưa có NV chấm công | LOW | Hiển thị "Chưa có dữ liệu" thay vì 0%. Không tính vào average. |
| RT01-E2 | **Dữ liệu chưa chốt** — Xem dashboard tháng chưa đến ngày chốt | MEDIUM | Badge: "Dữ liệu tạm tính (chưa chốt công)." Màu cam thay vì xanh. Số liệu live update. |
| RT01-E3 | **RBAC filter** — Manager xem báo cáo phòng ban khác | HIGH | Chặn: chỉ hiển thị phòng ban mà user có quyền. SITE_HR xem toàn site. GLOBAL_HR xem toàn bộ. |
