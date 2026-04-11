# US-REG-02: Đăng ký đổi ca

---

**AS A** Nhân viên,  
**I WANT TO** gửi yêu cầu đổi ca làm việc cho một ngày cụ thể trên Mini App,  
**SO THAT** tôi có thể chủ động sắp xếp lịch ca khi có việc đột xuất mà không cần liên hệ HR trực tiếp.

---

### **1. BUSINESS FLOW**

1. **Khởi tạo:** NV chọn "Đổi ca" tại Trung tâm đăng ký.
2. **Chọn ngày:** NV chọn ngày cần đổi ca → Hệ thống hiển thị ca hiện tại đang được phân (tự điền).
3. **Chọn ca mới:** Hệ thống hiển thị danh sách ca Active khả dụng (loại trừ ca trùng giờ với đơn khác).
4. **Nhập lý do:** NV nhập lý do đổi ca.
5. **Validate:**
   - Kiểm tra xung đột: ca mới không trùng khung giờ với ca/đơn khác trong ngày.
   - Kiểm tra ca mới còn slot (nếu có giới hạn số NV/ca).
6. **Gửi đơn:** Tạo ShiftChangeRequest (status: PENDING) → Chuyển phê duyệt.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Form đổi ca | Nhân viên | NV chỉ đổi ca cho chính mình. |
| Ca hiện tại của NV | Nhân viên, HR, Quản lý | ABAC: NV xem ca mình; Manager xem ca team. |
| Danh sách ca khả dụng | Nhân viên | Chỉ hiển thị ca Active thuộc site của NV. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Hiển thị ca hiện tại**

- Khi NV chọn ngày, hệ thống tự động hiển thị: Tên ca hiện tại, Giờ In/Out, Ngày áp dụng.
- Nếu ngày chọn chưa được phân ca → Hiển thị "Chưa có ca" và chặn gửi đơn.

#### **AC2. Danh sách ca khả dụng**

- Hiển thị các ca Active thuộc site NV, loại trừ: ca hiện tại, ca trùng khung giờ với đơn đã gửi trong ngày.
- Mỗi ca hiển thị: Tên, Giờ In/Out, Số phút nghỉ.

#### **AC3. Kiểm tra xung đột**

- **Case 1 (Trùng giờ):** Ca mới có khung giờ chồng lấn với ca/đơn OT/đơn đổi ca khác trong ngày → Hiển thị lỗi.
- **Case 2 (Đã có đơn đổi ca Pending):** NV đã có đơn đổi ca Pending cho ngày đó → Chặn tạo đơn mới.

#### **AC4. Phản hồi sau gửi**

- Hiển thị thông báo: "Yêu cầu đổi ca đã gửi. Ca mới sẽ áp dụng sau khi được duyệt."
- Ca hiện tại KHÔNG thay đổi cho đến khi đơn được APPROVED.

---

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| R02-E1 | **Đổi ca sau khi đã check-in** — NV check-in 8:00 (ca Sáng), đơn đổi sang ca Chiều được duyệt | HIGH | Chặn đổi ca cho ngày đã có dữ liệu chấm công. Hiển thị lỗi: "Không thể đổi ca — đã có mốc chấm công ngày [dd/MM]. Vui lòng giải trình thay vì đổi ca." |
| R02-E2 | **Đổi ca tương hỗ (swap)** — NV A muốn đổi ca với NV B | MEDIUM | Phase 1: chưa hỗ trợ swap. Hiển thị note: "Để đổi ca với đồng nghiệp, cả 2 cần gửi đơn đổi ca riêng". Phase 2 (future): form Swap Request linking 2 NV. |

---

### **4. DEFINITION OF DONE (DOD)**

1. **Dữ liệu:** Sau khi đơn APPROVED, ca của NV trong ngày đó phải thay đổi trong Database và hiển thị đúng trên Dashboard (Module 01).
2. **Thông báo:** NV nhận Push notification khi đơn được duyệt/từ chối.
3. **UI:** Form hiển thị trực quan ca cũ → ca mới dạng so sánh.
4. **QA:** Kiểm thử case đổi ca đêm, ca xoay, xung đột nhiều đơn cùng ngày, **đổi ca ngày đã check-in**.
