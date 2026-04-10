# US-REG-03: Đăng ký tăng ca (OT)

---

**AS A** Nhân viên,  
**I WANT TO** đăng ký làm tăng ca (OT) trước hoặc sau khi đã làm thêm giờ, kèm mốc thời gian cụ thể,  
**SO THAT** giờ OT của tôi được ghi nhận chính thức, tính đúng hệ số lương và không vượt giới hạn pháp luật.

---

### **1. BUSINESS FLOW**

1. **Khởi tạo:** NV chọn "Đăng ký tăng ca" tại Trung tâm đăng ký.
2. **Chọn loại đăng ký:**
   - **Trước (PRE_APPROVED):** Đăng ký trước ngày làm OT.
   - **Sau (POST_APPROVED):** Đăng ký sau khi đã OT (trong vòng 3 ngày).
3. **Nhập thông tin:** Chọn ngày, giờ bắt đầu OT, giờ kết thúc OT, lý do.
4. **Validate:**
   - Kiểm tra giới hạn OT: ngày (≤ 4h), tuần (≤ 12h), tháng (≤ 40h), năm (≤ 200h/300h).
   - Kiểm tra trùng: chỉ 1 OT request ACTIVE (PENDING/APPROVED) cho mỗi NV mỗi ngày.
   - Tính hệ số: weekday=1.5x, weekend=2.0x, holiday=3.0x.
5. **Gửi đơn:** Tạo OvertimeRequest (status: PENDING) → Chuyển phê duyệt.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Form đăng ký OT | Nhân viên, HR, Quản lý | Mọi role đều có thể tạo đơn OT cho chính mình. |
| Giờ OT lũy kế (ngày/tuần/tháng/năm) | Nhân viên | ABAC: Chỉ xem dữ liệu của chính mình. |
| Hệ số OT áp dụng | Nhân viên | Hiển thị read-only, tự động tính theo loại ngày. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị thông tin OT hiện tại**

- Trước khi nhập form, hiển thị tóm tắt OT lũy kế:
  - Tuần này: X/12 giờ
  - Tháng này: X/40 giờ
  - Năm nay: X/200 giờ
- Hiển thị cảnh báo vàng khi đạt ≥ 80% giới hạn; đỏ khi đạt 100%.

#### **AC2. Nhập mốc thời gian OT**

- Giờ bắt đầu OT: mặc định = Giờ tan ca + 1 phút.
- Giờ kết thúc OT: NV tự nhập.
- Hệ thống tự tính: Số giờ OT = Kết thúc - Bắt đầu.
- Hiển thị hệ số: "Ngày thường × 1.5" hoặc "Cuối tuần × 2.0" hoặc "Ngày lễ × 3.0".

#### **AC3. Kiểm tra giới hạn OT**

- **Case 1 (Vượt giới hạn ngày):** Đăng ký > 4h/ngày → Chặn gửi + hiển thị: "Vượt giới hạn OT ngày (tối đa 4 giờ)".
- **Case 2 (Vượt giới hạn tháng):** OT lũy kế + đơn mới > 40h → Chặn gửi.
- **Case 3 (Vượt giới hạn năm):** OT lũy kế + đơn mới > 200h → Chặn gửi (trừ khi có phê duyệt 300h đặc biệt).
- **Case 4 (Trùng đơn):** Đã có đơn OT PENDING/APPROVED cho ngày đó → Chặn tạo đơn mới.

#### **AC4. Đăng ký sau (POST_APPROVED)**

- Chỉ cho phép đăng ký OT cho ngày đã qua trong vòng 3 ngày.
- Hệ thống cross-check với dữ liệu chấm công thực tế: NV phải có mốc check-out sau giờ tan ca.

---

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| R03-E1 | **OT thực tế khác đăng ký** — Đăng ký 18:00-20:00 nhưng check-out 21:00 | HIGH | Giờ OT tính theo MIN(đăng ký, thực tế). Phần dư (20:00-21:00) → tạo auto-detected OT request riêng cần duyệt thêm. Không tự động ghi nhận phần chênh. |
| R03-E2 | **OT ngày lễ trùng cuối tuần** — 01/05 rơi vào Chủ nhật | CRITICAL | **Theo Luật Lao động VN:** áp dụng hệ số cao nhất. Holiday (3.0x) > Weekend (2.0x) → tính 3.0x. Logic: check holiday calendar trước, nếu là ngày lễ → luôn dùng 3.0x bất kể thứ trong tuần. |
| R03-E3 | **OT liên tiếp nhiều ngày** — NV đăng ký OT 7 ngày liên tiếp (mỗi ngày 2h = 14h/tuần) | MEDIUM | Validate tổng tuần: SUM(approved + pending OT trong tuần) + đơn mới > 12h → chặn. Hiển thị: "Vượt giới hạn OT tuần (tối đa 12 giờ). Đã sử dụng Xh, còn lại Yh." |
| R03-E4 | **Auto-detected OT không có đơn** — NV làm thêm 2h nhưng quên đăng ký | HIGH | Hệ thống phát hiện check-out sau giờ tan ca > 30 phút → tạo OT record (status: AUTO_DETECTED, PENDING). Push cho NV: "Phát hiện OT Xh ngày dd/MM. Xác nhận để gửi duyệt?" NV confirm → chuyển PENDING approval. NV bỏ qua 3 ngày → auto-expire. |

---

### **4. DEFINITION OF DONE (DOD)**

1. **Giới hạn OT:** Kiểm thử tất cả ngưỡng (ngày/tuần/tháng/năm) → Đảm bảo chặn chính xác.
2. **Partial unique index:** DB chỉ cho phép 1 request OT ACTIVE (PENDING/APPROVED) per NV per ngày.
3. **Hệ số:** Kiểm thử OT vào ngày thường, cuối tuần, ngày lễ → Hệ số đúng. **Đặc biệt: ngày lễ trùng weekend phải là 3.0x.**
4. **QA:** Kiểm thử PRE và POST approval flow; case OT xuyên đêm; **auto-detected OT; OT actual > registered; weekly cumulative limit**.
