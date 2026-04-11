# 2.11.8. Cấu hình Camera AI

---

| Thông tin | Nội dung |
| --- | --- |
| Target release | Version 1.0 (Sprint 8) |
| Epic | STRATOS-ADMIN: Hệ thống Quản trị & Cấu hình tập trung |
| Document owner | BA Team |
| Stakeholder | IT Admin, HR Admin |
| Status | Draft |
| Tham chiếu | EAMS v2.0 §8 (Tích hợp C-Vision) |

---

### **1. MỤC TIÊU**

- **Lý do tồn tại:** Camera AI (C-Vision) là nguồn dữ liệu chấm công chính. Cần giao diện quản lý thiết bị, mapping nhân viên và giám sát sức khỏe hệ thống.
- **Bài toán:** Đăng ký thiết bị camera, gán hướng In/Out, mapping personId↔employeeId, và phát hiện sớm camera mất kết nối.
- **Giá trị mang lại:** Giảm 95% lỗi chấm công do thiết bị; phát hiện camera offline trong < 5 phút.

---

### **2. MÔ TẢ QUY TRÌNH NGHIỆP VỤ**

```
IT Admin truy cập "Cấu hình Camera AI"
        ↓
  ├─ Quản lý thiết bị:
  │   ├─ Thêm camera mới: deviceId, siteId, directionType, threshold
  │   ├─ Sửa cấu hình: ngưỡng confidence, hướng In/Out
  │   └─ Vô hiệu hóa camera hỏng
  │
  ├─ Mapping nhân viên:
  │   ├─ Bulk-create mapping từ danh sách NV
  │   └─ Xử lý mapping thất bại (personId không khớp)
  │
  └─ Health Check:
      ├─ Dashboard trạng thái: Online/Offline/Warning
      └─ Cảnh báo khi camera mất heartbeat > 5 phút
```

---

### **3. NHU CẦU NGƯỜI DÙNG**

| Persona | Nhu cầu cụ thể | Tài liệu / Căn cứ |
| --- | --- | --- |
| IT Admin | Muốn đăng ký camera mới khi lắp đặt tại cổng ra vào chi nhánh. | Device Management |
| IT Admin | Muốn biết ngay khi camera mất kết nối để sửa chữa kịp thời. | Health Check |
| HR Admin | Muốn mapping nhân viên mới với C-Vision để họ có thể chấm công Face ID. | Employee Mapping |

---

### **4. PHẠM VI CHỨC NĂNG**

| Mã | Chức năng | Mô tả chi tiết | User Story |
| --- | --- | --- | --- |
| F08.1 | Quản lý danh sách thiết bị | CRUD thiết bị camera: deviceId, tên, siteId, directionType (IN_ONLY/OUT_ONLY/BIDIRECTIONAL), confidenceThreshold, status (Active/Inactive). Lọc theo site. | [US-CAM-01](./US-CAM-01-Quản-lý-danh-sách-thiết-bị.md) |
| F08.2 | Mapping nhân viên - Camera | Quản lý bảng CVisionPersonMapping: cvisionPersonId ↔ employeeId. Hỗ trợ bulk-create từ danh sách NV. Xử lý mapping lỗi. | [US-CAM-02](./US-CAM-02-Mapping-nhân-viên.md) |
| F08.3 | Health check & Monitoring | Dashboard trạng thái camera real-time. Heartbeat mỗi 5 phút. Cảnh báo IT/Admin khi mất tín hiệu. Lịch sử uptime. | [US-CAM-03](./US-CAM-03-Health-check-và-monitoring.md) |
| F08.4 | Đăng ký khuôn mặt NV (Face ID Enrollment) | Quy trình 3 bước: Xác nhận thông tin → Chụp ảnh khuôn mặt → Đồng bộ C-Vision. NV tự đăng ký trên Mini App. Kiểm tra chất lượng ảnh tự động. | [US-CAM-04](./US-CAM-04-Đăng-ký-khuôn-mặt-nhân-viên.md) |

---

### **5. PIPELINE XỬ LÝ WEBHOOK** *(Nguồn: EAMS v2.0 §8.3)*

| Bước | Hành động | Xử lý lỗi |
| --- | --- | --- |
| 1 | Xác thực signature HMAC-SHA256 | Reject webhook |
| 2 | Kiểm tra idempotency (Redis) | Skip nếu đã xử lý |
| 3 | Tìm tenant từ deviceId | Failed: device chưa đăng ký |
| 4 | Tải cấu hình device (site, threshold) | Failed: device không tồn tại |
| 5 | Kiểm tra confidence ≥ threshold | Failed: cần HR review |
| 6 | Mapping personId → employeeId | Failed: cần tạo mapping |
| 7 | Xác định CHECK_IN/CHECK_OUT | Dùng thuật toán xen kẽ |
| 8 | Tạo attendance record | Circuit breaker + retry |

---

### **6. YÊU CẦU PHI CHỨC NĂNG**

- **De-duplication:** Nếu NV bị quét nhiều lần trong < 30 giây, chỉ lấy mốc sớm nhất.
- **Độ trễ:** Dữ liệu từ Camera đến App ≤ 60 giây.
- **Health Check:** Heartbeat mỗi 5 phút; cảnh báo ngay khi mất tín hiệu.
- **Bảo mật:** Webhook xác thực HMAC-SHA256; ảnh Face ID chỉ dùng cho chấm công.

---

### **EDGE CASES & ERROR HANDLING (toàn module)**

| # | US | Case | Severity | Expected Behavior |
|---|-----|------|----------|-------------------|
| C01-E1 | CAM-01 | **Camera đổi site** — Camera chuyển từ Site A sang Site B | MEDIUM | Cho phép update siteId. Dữ liệu lịch sử giữ nguyên (gán theo siteId tại thời điểm ghi nhận). Audit log: "Camera [X] chuyển từ Site A → Site B bởi [Admin]". |
| C01-E2 | CAM-01 | **Clock sync** — Camera clock lệch 5 phút so với server | HIGH | **Bắt buộc** dùng server timestamp (receivedAt) thay vì device timestamp (recognitionTime) cho mục đích tính công. recognitionTime chỉ dùng tham khảo. Cảnh báo IT nếu abs(serverTime - deviceTime) > 2 phút. |
| C02-E1 | CAM-02 | **Duplicate personId** — 1 NV có 2 personId trong C-Vision | CRITICAL | Detect: nếu 2 mapping khác nhau match cùng employeeId → cảnh báo HR "NV [Tên] có 2 personId: [A], [B]". Cho phép merge: chọn personId chính, deactivate personId phụ. Tất cả records cũ với personId phụ → re-map sang personId chính. |
| C02-E2 | CAM-02 | **NV nghỉ việc — mapping cleanup** — Mapping vẫn active sau khi NV terminated | MEDIUM | Khi NV status → INACTIVE/TERMINATED: auto-deactivate mapping (soft delete). Webhook với personId cũ → log "PersonId [X] mapped to terminated employee — ignored". Không tạo attendance record. |
| C03-E1 | CAM-03 | **Camera offline + NV quét mặt** — Camera offline, NV quét nhưng không có webhook | HIGH | Push cho toàn bộ NV thuộc site có camera offline: "Camera tại [Tên sảnh] đang bảo trì. Vui lòng sử dụng cổng [Y] hoặc liên hệ HR nhập thủ công." Hiển thị banner đỏ trên Dashboard NV: "Camera tạm ngưng — dữ liệu chấm công có thể chậm". |

---

### **7. ĐIỀU KIỆN GIẢ ĐỊNH**

1. Camera AI (C-Vision) đã được lắp đặt và kết nối internet ổn định.
2. Đối tác C-Vision đã cung cấp deviceId và cấu hình webhook.
3. Danh sách nhân viên đã được import vào hệ thống (Module 05).
