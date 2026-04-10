# US-ATTEN-04: Trung tâm cảnh báo và thông báo

---

**AS A** Nhân viên ,  
**I WANT TO** thấy danh sách các vi phạm quy chế (đi muộn, về sớm, thiếu mốc quẹt, vắng mặt chưa xin phép) ngay tại màn hình chính,  
**SO THAT** tôi có thể thực hiện "Giải trình ngay" để đảm bảo quyền lợi giờ công của mình được cập nhật kịp thời.

---

### **1. BUSINESS FLOW**

1. **Hệ thống quét**: Cuối mỗi ngày làm việc, hệ thống Backend tự động so khớp dữ liệu quét AI với Lịch phân ca.
2. **Phát hiện sai lệch**: Nếu phát hiện các case:    - Giờ vào muộn (LATE).
    - Giờ ra sớm (EARLY).
    - Thiếu mốc quẹt (MISSING PUNCH).
    - Vắng mặt không phép (UNAUTHORIZED ABSENCE).

3. **Đẩy cảnh báo**: Hệ thống tự động điền danh sách vi phạm vào khung **"Cảnh báo vi phạm"** trên Web App của nhân viên đó.
4. **Tương tác giải trình**: Nhân viên nhấn nút **"Giải trình ngay"** ➔ Chuyển hướng đến màn hình **Module Giải trình công** kèm thông tin ngày vi phạm đã được điền sẵn (Prefill).
5. **Hoàn tất**: Sau khi đơn giải trình được gửi (Pending), cảnh báo đó sẽ tạm thời ẩn đi trong danh sách chờ.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Danh sách vi phạm cá nhân | Nhân viên , HR, Quản lý | ABAC: Chỉ hiển thị cảnh báo thuộc về User_ID đang đăng nhập. |
| Button "Giải trình ngay" | Nhân viên | Chỉ nhân viên mới có quyền tự giải trình cho chính họ. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **3.1. Hiển thị Widget Cảnh báo**

- **Tiêu đề**: "Cảnh báo vi phạm quy chế".
- **Danh sách hiển thị**: Hiển thị tối đa 03 cảnh báo mới nhất chưa xử lý.
- **Thông tin trên mỗi dòng**:    - Badge phân loại: Đi muộn / Về sớm / Thiếu giờ / Vắng mặt (Màu đỏ/Icon cảnh báo).
    - Ngày vi phạm: (VD: Thứ Sáu, 29/11).
    - Nút thao tác: [Giải trình ngay].

#### **3.2. Logic Hiển thị Cảnh báo**

- **Case 1 (Muộn/Sớm)**: Chỉ hiển thị nếu NV chưa có đơn Giải trình hoặc đơn Xin nghỉ phép tương ứng cho ngày đó.
- **Case 2 (Thiếu quẹt)**: Hiển thị nếu chỉ có giờ Vào mà không có giờ Ra sau 24h hàng ngày (Không bao gồm ca đêm).
- **Case 3 (Vắng mặt)**: Hiển thị nếu ngày làm việc đã qua mà không có bất kỳ mốc dữ liệu chấm công nào + không có đơn phép.

#### **3.3. Phản hồi Web App**

- Khi nhân viên nhấn nút "Giải trình ngay" ➔ Web App phải ghi nhớ ngày vi phạm để khi chuyển sang màn Giải trình, người dùng không cần chọn lại ngày (Autofill).
- Cảnh báo phải biến mất khỏi danh sách ngay khi đơn giải trình ở trạng thái Pending (Đang chờ duyệt).

---

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| A04-E1 | **Nhiều loại vi phạm cùng ngày** — NV vừa "Đi muộn" vừa "Thiếu quẹt" | MEDIUM | Hiển thị tất cả vi phạm (mỗi loại 1 dòng). Ưu tiên hiển thị: Vắng mặt > Thiếu quẹt > Đi muộn > Về sớm. Giới hạn 3 cảnh báo mới nhất → "Xem tất cả" cho phần còn lại. |
| A04-E2 | **Ca thay đổi retroactively** — HR đổi ca cho NV sau khi cảnh báo đã tạo | HIGH | Khi ca thay đổi → batch job re-evaluate toàn bộ anomalies của NV trong ngày. Cảnh báo cũ bị xóa/cập nhật nếu không còn vi phạm với ca mới. Ghi audit log "Cảnh báo tự động xóa do thay đổi ca". |
| A04-E3 | **NV nghỉ phép nửa ngày + cảnh báo** — NV nghỉ AM, làm PM. Hệ thống báo "Vắng mặt" sáng | MEDIUM | Cross-check đơn nghỉ phép APPROVED trước khi tạo cảnh báo. Nếu có đơn nghỉ AM/PM → chỉ quét buổi còn lại. Nếu có đơn cả ngày → không tạo cảnh báo. |

---

### **4. DEFINITION OF DONE (DOD)**

1. **Dữ liệu thực**: Danh sách cảnh báo phải khớp hoàn toàn với Badge trạng thái trong Nhật ký (Module 01).
2. **Thông báo (Push)**: Đi kèm với hiển thị trên App, hệ thống nên gửi 1 Push Notification nhắc nhở vào 08:00 AM sáng hôm sau nếu vi phạm chưa được xử lý.
3. **Giao diện**: Layout Web phải nổi bật màu sắc cảnh báo (Tone màu Cam/Đỏ) để gây chú ý cho người dùng.
4. **QA**: Kiểm thử logic quét dữ liệu sau 24h đối với 4 loại vi phạm — **thêm case: nhiều vi phạm/ngày, thay đổi ca retroactively, nghỉ phép nửa ngày**.
