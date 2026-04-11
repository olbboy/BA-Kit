# US-CAM-03: Health check và Monitoring

---

**AS A** IT Admin,  
**I WANT TO** giám sát trạng thái hoạt động (Online/Offline) của tất cả camera AI trong thời gian thực,  
**SO THAT** tôi có thể phát hiện và xử lý camera mất kết nối trước khi ảnh hưởng đến chấm công của nhân viên.

---

### **1. BUSINESS FLOW**

1. **Heartbeat:** Hệ thống kiểm tra tín hiệu camera mỗi 5 phút (dựa trên lastEventTime từ webhook).
2. **Dashboard:** Hiển thị trạng thái: Online (< 5 phút từ event cuối), Warning (5-15 phút), Offline (> 15 phút).
3. **Cảnh báo:** Khi camera chuyển Offline → Gửi alert cho IT Admin qua Push + Email.
4. **Lịch sử:** Ghi log uptime/downtime để phân tích.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Dashboard monitoring | IT Admin, SYS_ADMIN | Xem trạng thái toàn bộ camera. |
| Cảnh báo Offline | IT Admin | Nhận alert tự động. |
| Lịch sử uptime | IT Admin, HR Admin | HR xem để biết camera nào hay lỗi. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Dashboard trạng thái**

- Hiển thị grid các camera card:
  - **Online (Xanh):** lastEventTime < 5 phút trước.
  - **Warning (Vàng):** lastEventTime 5-15 phút trước.
  - **Offline (Đỏ):** lastEventTime > 15 phút trước.
- Mỗi card: Tên camera, Site, Hướng, Thời gian event cuối, Uptime % (24h gần nhất).
- Tổng hợp: X Online / Y Warning / Z Offline.

#### **AC2. Cảnh báo tự động**

- Khi camera chuyển từ Online → Offline:
  - Push notification cho IT Admin: "Camera [Tên] tại [Site] đã mất kết nối lúc [HH:MM]".
  - Email cho IT Team nếu offline > 30 phút.
- Khi camera khôi phục (Offline → Online):
  - Thông báo: "Camera [Tên] đã hoạt động trở lại".

#### **AC3. Lịch sử Uptime**

- Biểu đồ timeline (24h/7 ngày/30 ngày) cho từng camera.
- Hiển thị: Thời gian Online (Xanh), Offline (Đỏ).
- Tính: Uptime % = (Tổng phút Online / Tổng phút) × 100.

#### **AC4. De-duplication**

- Nếu NV bị quét nhiều lần trong < 30 giây → Chỉ lấy mốc sớm nhất.
- Log các mốc bị de-duplicate để IT debug.

---

### **4. DEFINITION OF DONE (DOD)**

1. **Độ trễ:** Trạng thái camera cập nhật trên dashboard ≤ 1 phút.
2. **Cảnh báo:** Camera offline → IT nhận alert ≤ 5 phút.
3. **Uptime:** Biểu đồ hiển thị chính xác so với log thực tế.
4. **QA:** Kiểm thử: camera ngắt kết nối, camera khôi phục, nhiều camera offline đồng thời.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| CM03-E1 | **Camera offline > 1 giờ** — Health check fail liên tục | HIGH | Escalate: Email IT Manager + Push notification. Dashboard badge đỏ. Log incident. |
| CM03-E2 | **False offline** — Network hiccup 30 giây | LOW | Grace period: 3 consecutive fails (15 phút) mới đánh dấu offline. Tránh alert spam. |
| CM03-E3 | **Tất cả camera cùng site offline** — Mất mạng toàn site | CRITICAL | Alert đặc biệt cho SITE_MANAGER + IT. Fallback: cho phép manual check-in. Banner toàn app: "Hệ thống camera tại [Site] đang bảo trì." |
