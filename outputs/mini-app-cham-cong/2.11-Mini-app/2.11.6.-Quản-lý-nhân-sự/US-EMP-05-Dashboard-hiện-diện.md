# US-EMP-05: Dashboard hiện diện real-time

---

**AS A** Quản lý,  
**I WANT TO** xem dashboard hiển thị số lượng nhân viên On-site, WFH, Vắng mặt và Nghỉ phép trong thời gian thực,  
**SO THAT** tôi có thể nắm bắt ngay tình hình nhân lực hiện tại để điều phối công việc.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** Manager/HR mở "Quản lý nhân sự" → Tab "Hiện diện".
2. **Khởi tạo:** Hệ thống tổng hợp trạng thái hiện diện từ AttendanceAggregator và LeaveAggregator.
3. **Hiển thị:** 4 counter cards + danh sách chi tiết NV theo từng trạng thái.
4. **Cập nhật:** Real-time khi có mốc chấm công mới hoặc đơn nghỉ được duyệt.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Dashboard hiện diện toàn site | SITE_HR, SITE_MANAGER | Xem toàn bộ NV thuộc site. |
| Dashboard hiện diện team | MANAGER, DEPT_HEAD | Chỉ xem NV thuộc team/phòng ban. |
| Dashboard toàn hệ thống | GLOBAL_HR | Xem tất cả site. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Counter Cards**

- **On-site:** NV có mốc check-in hôm nay và chưa check-out (hoặc đang trong ca).
- **WFH:** NV có đơn WFH APPROVED cho hôm nay.
- **Vắng mặt:** NV không có mốc check-in, không có đơn nghỉ/WFH, và đã qua giờ bắt đầu ca + grace period.
- **Nghỉ phép:** NV có đơn nghỉ APPROVED trùng hôm nay.
- Mỗi card hiển thị: Số lượng + % so với tổng NV.

#### **AC2. Danh sách chi tiết**

- Nhấn vào card → Hiển thị danh sách NV thuộc trạng thái đó.
- Mỗi dòng: Ảnh, Tên, Phòng ban, Giờ check-in (nếu có), Trạng thái chi tiết.
- Hỗ trợ tìm kiếm trong danh sách.

#### **AC3. Real-time update**

- Khi NV check-in → Counter On-site tăng, Vắng mặt giảm (trong vòng 60 giây).
- Sử dụng WebSocket hoặc polling (interval ≤ 30 giây).

---

### **4. DEFINITION OF DONE (DOD)**

1. **Dữ liệu:** Counter phải khớp với tổng NV active trong hệ thống.
2. **Real-time:** Kiểm thử NV check-in → Dashboard cập nhật ≤ 60 giây.
3. **RBAC:** Manager chỉ thấy NV team mình; SITE_HR thấy toàn site.
4. **QA:** Kiểm thử các edge case: NV multi-site, NV chuyển phòng ban, NV ca đêm.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM05-E1 | **Camera offline** — Không có dữ liệu real-time từ site | MEDIUM | Badge "Offline" trên site card. Hiển thị dữ liệu cuối cùng kèm timestamp "Cập nhật lúc [HH:MM]." |
| EM05-E2 | **Toàn bộ NV WFH** — On-site = 0 | LOW | Hiển thị đúng "0 on-site". Không ẩn dashboard. Hiển thị chi tiết WFH breakdown. |
| EM05-E3 | **Timezone khác nhau** — Site ở HCM (UTC+7) vs Site ở HN (UTC+7) nhưng server UTC | LOW | Tất cả giờ hiển thị theo timezone site. Server store UTC, client convert theo site timezone. |
