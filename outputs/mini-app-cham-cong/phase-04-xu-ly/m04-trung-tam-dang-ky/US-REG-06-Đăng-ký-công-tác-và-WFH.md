# US-REG-06: Đăng ký công tác & WFH (Business Travel / Work From Home)

---

**AS A** Nhân viên,  
**I WANT TO** gửi yêu cầu đăng ký Công tác (Business Travel) hoặc Làm việc tại nhà (WFH) trên Mini App,  
**SO THAT** tôi được ghi nhận "Có mặt hợp lệ" mà không cần chấm công tại văn phòng, và quản lý nắm được vị trí làm việc thực tế của tôi.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** NV mở Trung tâm đăng ký → chọn "Đăng ký Công tác" hoặc "Đăng ký WFH".
2. **Chọn loại:**
   - **Công tác (BUSINESS_TRAVEL):** Nhập địa điểm, ngày bắt đầu-kết thúc, mục đích, người liên hệ (nếu có).
   - **WFH (WORK_FROM_HOME):** Chọn ngày (hỗ trợ multi-select), lý do.
3. **Kiểm tra ràng buộc:**
   - WFH: Hạn mức WFH tuần/tháng (cấu hình bởi US-HOL-02). Nếu vượt → cảnh báo.
   - Công tác: Không giới hạn ngày nhưng chặn trùng ngày nghỉ phép/OT đã duyệt.
4. **Approval:** Đơn gửi Manager → duyệt/từ chối qua Module 10.
5. **Sau khi duyệt:**
   - Hệ thống đánh dấu ngày công tác/WFH = `PRESENT` (hợp lệ, không cần check-in camera).
   - Dashboard hiện diện (US-EMP-05) cập nhật: NV hiển thị ở nhóm "Công tác" hoặc "WFH" thay vì "Vắng mặt".
6. **Thông báo:** Push cho Manager khi có đơn mới; Push cho NV khi đơn được duyệt/từ chối.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Tạo đơn Công tác / WFH | Nhân viên | Chỉ tạo cho chính mình. |
| Duyệt đơn | Manager, HR Admin | Manager duyệt team. HR duyệt toàn site. |
| Xem team WFH calendar | Manager | Xem lịch WFH team để kiểm tra tỷ lệ on-site. |
| Cấu hình hạn mức WFH | HR Admin | Qua US-HOL-02. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Form Đăng ký Công tác**

- Fields: Loại (Công tác), Ngày bắt đầu, Ngày kết thúc, Địa điểm, Mô tả/Mục đích, Đính kèm (tùy chọn).
- Hỗ trợ công tác liên tục nhiều ngày (date range picker).
- Validation: Ngày bắt đầu ≥ ngày hiện tại (không tạo công tác quá khứ, chỉ CURRENT hoặc FUTURE).
- Chặn trùng ngày đã có đơn nghỉ phép/OT APPROVED.

#### **AC2. Form Đăng ký WFH**

- Fields: Loại (WFH), Ngày (multi-select calendar), Lý do.
- Hiển thị hạn mức: "Đã dùng X/Y ngày WFH tuần này" (từ US-HOL-02 config).
- Nếu vượt hạn mức → cảnh báo vàng: "Bạn đã vượt hạn mức WFH tuần (Y ngày). Đơn vẫn gửi nhưng cần phê duyệt đặc biệt." → đơn route đến HR thay vì Manager.
- Chặn WFH vào ngày lễ hoặc ngày NV đã đăng ký nghỉ phép.

#### **AC3. Tích hợp Dashboard Hiện diện (US-EMP-05)**

- NV có đơn APPROVED:
  - Công tác → counter "Công tác" trong dashboard.
  - WFH → counter "WFH" trong dashboard.
- NV KHÔNG hiển thị ở "Vắng mặt" nếu có đơn Công tác/WFH active.
- Click vào counter → xem danh sách NV kèm địa điểm (Công tác) hoặc "WFH" tag.

#### **AC4. Auto-marking attendance**

- Khi đơn WFH/Công tác APPROVED cho ngày T:
  - Hệ thống tự tạo `AttendanceRecord` với `source = WFH` hoặc `source = BUSINESS_TRAVEL`.
  - Status = `PRESENT`, netHours = ca đang gán (tính đủ giờ).
  - Dashboard NV hiển thị: "WFH ✅" hoặc "Công tác ✅" thay vì badge "Chưa chấm công".

---

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RG06-E1 | **WFH vượt hạn mức** — NV đăng ký ngày thứ 3 trong tuần khi limit = 2 | MEDIUM | Cảnh báo: "Vượt hạn mức (2/tuần)". Đơn vẫn submit nhưng route đến HR thay vì Manager. HR duyệt = exception. |
| RG06-E2 | **Công tác trùng ngày nghỉ phép** — NV đã có APPROVED leave ngày 15-17, đăng ký công tác 16-20 | HIGH | Chặn ngày trùng: "Ngày 16-17 đã có đơn nghỉ phép. Vui lòng hủy nghỉ phép trước hoặc chọn ngày khác." Cho phép đăng ký 18-20. |
| RG06-E3 | **Toàn team WFH cùng ngày** — 100% team đăng ký WFH thứ 6 | MEDIUM | Cảnh báo Manager khi duyệt: "Nếu duyệt, 100% team sẽ WFH ngày này. On-site = 0." Manager vẫn có thể duyệt (tùy chính sách). |
| RG06-E4 | **NV công tác nhưng quẹt camera tại site khác** — NV đi công tác HCM, quẹt face ở VP HCM | LOW | Camera HCM vẫn ghi nhận mốc quẹt (site khác). Dashboard hiển thị cả 2: Công tác (theo đơn) + mốc quẹt (theo camera). Không xung đột. |

---

### **4. DEFINITION OF DONE (DOD)**

1. **End-to-end WFH:** NV đăng ký WFH → Manager duyệt → ngày WFH hiển thị "PRESENT" trên dashboard.
2. **End-to-end Công tác:** NV đăng ký công tác 3 ngày → attendance = PRESENT cả 3 ngày → payroll tính đủ công.
3. **Hạn mức:** Vượt WFH limit → route HR → duyệt/từ chối đúng flow.
4. **Dashboard:** US-EMP-05 hiển thị counter Công tác + WFH chính xác.
5. **QA:** Test trùng lịch, vượt hạn mức, multi-day, toàn team WFH, camera cross-site.
