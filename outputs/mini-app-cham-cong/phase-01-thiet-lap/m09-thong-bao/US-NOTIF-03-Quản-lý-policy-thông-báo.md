# US-NOTIF-03: Quản lý policy thông báo

---

**AS A** HR Admin,  
**I WANT TO** cấu hình policy gửi thông báo (Batching, Throttle, Schedule) và cho phép nhân viên tùy chỉnh preference cá nhân,  
**SO THAT** hệ thống gửi ≤ 3 thông báo/giờ cho mỗi NV, không spam, và nhân viên có thể tắt thông báo nhắc nhở nhưng vẫn nhận thông báo bắt buộc.

---

### **1. BUSINESS FLOW**

1. **Cấu hình policy (Admin):**
   - **Batching:** Gom nhiều event cùng loại → Gửi 1 thông báo tổng hợp (VD: gom 5 đơn cần duyệt → 1 email).
   - **Throttle:** Giới hạn số thông báo tối đa/giờ cho mỗi NV (VD: max 10 push/giờ).
   - **Schedule:** Chỉ gửi thông báo trong khung giờ (VD: 07:00-22:00, không gửi ban đêm).
2. **Preference cá nhân (NV):**
   - NV mở Settings → Thông báo → Bật/tắt từng nhóm thông báo.
   - Thông báo bắt buộc (kết quả phê duyệt, kỷ luật) KHÔNG cho phép tắt.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Cấu hình Batching/Throttle/Schedule | HR Admin, SYS_ADMIN | Áp dụng toàn hệ thống. |
| Preference cá nhân | Nhân viên | Chỉ tùy chỉnh cho chính mình. |
| Xem policy hiện tại | HR, Quản lý | Read-only. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Cấu hình Batching**

- Toggle Bật/Tắt batching cho từng nhóm sự kiện.
- Khi Bật: Thiết lập khoảng thời gian gom (VD: 15 phút, 30 phút, 1 giờ).
- Thông báo gom hiển thị: "Bạn có X đơn mới cần duyệt" thay vì X thông báo riêng lẻ.

#### **AC2. Cấu hình Throttle**

- Thiết lập: Max N thông báo/giờ/NV. Mặc định: 20.
- Khi vượt ngưỡng: Thông báo mới được queue, gửi khi slot khả dụng.
- Thông báo bắt buộc KHÔNG bị throttle.

#### **AC3. Cấu hình Schedule**

- Khung giờ gửi: Giờ bắt đầu — Giờ kết thúc (VD: 07:00-22:00).
- Ngoài khung giờ: Thông báo được queue → Gửi đầu khung giờ tiếp theo.
- Ngoại lệ: Thông báo khẩn cấp (camera offline, security event) gửi ngay bất kể schedule.

#### **AC4. Preference cá nhân NV**

- Giao diện: Danh sách nhóm thông báo + Toggle cho mỗi nhóm.
- **Cho phép tắt:** Nhắc nhở chấm công, Thông báo check-in/out, Lịch nghỉ lễ.
- **KHÔNG cho phép tắt (bắt buộc):** Kết quả phê duyệt đơn, Cảnh báo vi phạm, Kỷ luật lao động.
- Toggle bắt buộc hiển thị: Xám + icon khóa + tooltip "Thông báo bắt buộc — không thể tắt".

---

### **4. DEFINITION OF DONE (DOD)**

1. **Batching:** 5 event trong 15 phút → NV nhận 1 thông báo tổng hợp (không phải 5).
2. **Throttle:** Gửi 25 thông báo liên tiếp (limit 20) → 5 thông báo bị queue.
3. **Bắt buộc:** NV cố tắt thông báo bắt buộc → UI disabled + backend reject.
4. **QA:** Kiểm thử batching + throttle + schedule kết hợp; thông báo khẩn cấp bypass schedule.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| NF03-E1 | **NV tắt thông báo bắt buộc** — Cố tắt notification phê duyệt | HIGH | UI disable toggle cho thông báo bắt buộc. Backend ignore "mute" request cho mandatory events. |
| NF03-E2 | **Quiet hours conflict với ca đêm** — Quiet hours 22:00-07:00, NV ca đêm cần check-in reminder | MEDIUM | Ca đêm NV: quiet hours auto-adjusted theo shift schedule. Chỉ mute khi NV KHÔNG có ca. |
| NF03-E3 | **Batch digest quá lớn** — Daily digest chứa > 50 items | LOW | Truncate tại 20 items + link "Xem thêm [N] thông báo khác trên App." |
