# Test Suite — M08: Cấu hình Camera AI

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen

---

## Coverage Summary

| US | Happy | Edge | Error | Security | Concurrency | Data | Perf | Total |
|----|-------|------|-------|----------|-------------|------|------|-------|
| US-CAM-01 Quản lý thiết bị | 2 | 3 | 3 | 2 | 0 | 1 | 0 | **11** |
| US-CAM-02 Mapping NV | 2 | 2 | 2 | 1 | 0 | 1 | 1 | **9** |
| US-CAM-03 Health check | 2 | 3 | 2 | 1 | 0 | 0 | 1 | **9** |
| US-CAM-04 Face ID enrollment | 2 | 3 | 3 | 2 | 1 | 1 | 0 | **12** |
| **Total** | **8** | **11** | **10** | **6** | **1** | **3** | **2** | **41** |

---

## US-CAM-01: Quản lý danh sách thiết bị Camera

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-CM01-HP-01 | Happy | IT đăng ký camera mới | POST /cameras → 201. deviceId, name, siteId, direction=IN_ONLY. | P1 |
| TC-CM01-HP-02 | Happy | IT toggle camera Inactive | PATCH /cameras/{id}/status → Inactive. Webhook drop + ghi log. | P1 |
| TC-CM01-EC-01 | Edge | Device ID trùng | 409: "Device ID [X] đã đăng ký tại [Site Y]." | P1 |
| TC-CM01-EC-02 | Edge | Xóa camera đang active (NV check-in hàng ngày) | Soft-delete. Cần confirm. Attendance history giữ nguyên. | P1 |
| TC-CM01-EC-03 | Edge | Camera chưa đăng ký trên C-Vision | Cảnh báo: "Webhook sẽ bị reject." Cho phép lưu draft. | P2 |
| TC-CM01-ER-01 | Error | confidenceThreshold=0.69 (out of range) | 422: "Phải trong 0.70–0.99." | P2 |
| TC-CM01-ER-02 | Error | Thiếu required fields (deviceId) | 400: VALIDATION_ERROR. | P2 |
| TC-CM01-ER-03 | Error | PUT camera đổi deviceId | 400: IMMUTABLE_FIELD. deviceId không được sửa sau tạo. | P2 |
| TC-CM01-SEC-01 | Security | HR read-only cameras | 200 GET. Không thể POST/PUT/DELETE. | P1 |
| TC-CM01-SEC-02 | Security | NV truy cập /cameras | 403 Forbidden. | P1 |
| TC-CM01-DI-01 | Data | Camera Active → webhook accepted | Webhook từ camera Active → attendance record created. | P1 |

## US-CAM-02: Mapping nhân viên

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-CM02-HP-01 | Happy | HR tạo mapping NV ↔ C-Vision person | POST /camera-mappings → 201. cvisionPersonId ↔ employeeId. | P1 |
| TC-CM02-HP-02 | Happy | HR bulk-create mappings | Bulk POST → N mappings created. | P1 |
| TC-CM02-EC-01 | Edge | Mapping trùng (cùng personId) | 409: "personId [X] đã được map với NV [Y]." | P1 |
| TC-CM02-EC-02 | Edge | NV chuyển chi nhánh → mapping cần update | HR xóa mapping cũ → tạo mapping mới tại site mới. | P2 |
| TC-CM02-ER-01 | Error | employeeId không tồn tại | 404: EMPLOYEE_NOT_FOUND. | P2 |
| TC-CM02-ER-02 | Error | Xóa mapping NV đang active | Cảnh báo: "NV sẽ không check-in được. Xác nhận?" | P2 |
| TC-CM02-SEC-01 | Security | NV tạo mapping | 403: Chỉ HR_ADMIN. | P1 |
| TC-CM02-DI-01 | Data | Mapping → webhook routing | Webhook personId=X → lookup mapping → employeeId=Y → attendance record. | P1 |
| TC-CM02-PERF-01 | Perf | Bulk 500 mappings | ≤ 10 giây. Progress indicator. | P2 |

## US-CAM-03: Health check và monitoring

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-CM03-HP-01 | Happy | IT xem health dashboard | Tổng camera, Active, Offline, Inactive counts. | P1 |
| TC-CM03-HP-02 | Happy | Camera offline >5 phút | Badge Offline (Đỏ). Alert IT admin. | P1 |
| TC-CM03-EC-01 | Edge | Camera baru đăng ký (chưa heartbeat) | Status "Chờ kết nối" (Vàng). lastHeartbeatAt=null. | P2 |
| TC-CM03-EC-02 | Edge | 100% cameras offline | Alert CRITICAL. Push SYS_ADMIN. Dashboard đỏ toàn bộ. | P1 |
| TC-CM03-EC-03 | Edge | Heartbeat flapping (online/offline mỗi 30s) | Debounce: chỉ alert sau 3 lần offline liên tiếp. | P2 |
| TC-CM03-ER-01 | Error | Health API timeout | Retry 3 lần. Fallback cached data + "Dữ liệu có thể cũ." | P2 |
| TC-CM03-ER-02 | Error | Camera gửi heartbeat nhưng không gửi event | Cảnh báo "Camera hoạt động nhưng không có sự kiện nhận dạng. Kiểm tra đặt vị trí." | P2 |
| TC-CM03-SEC-01 | Security | HR xem health dashboard | 200 OK (read-only). Chỉ cameras thuộc site. | P1 |
| TC-CM03-PERF-01 | Perf | Dashboard 200 cameras | ≤ 3 giây load. Auto-refresh 30s. | P2 |

## US-CAM-04: Đăng ký khuôn mặt (Face ID Enrollment)

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-CM04-HP-01 | Happy | NV đăng ký Face ID 3 bước | Step 1: xác nhận info → Step 2: chụp ảnh → Step 3: sync C-Vision. Status=ENROLLED. | P1 |
| TC-CM04-HP-02 | Happy | NV chấm công sau enrollment | Webhook match personId → attendance record. OK. | P1 |
| TC-CM04-EC-01 | Edge | Ảnh chất lượng thấp (ánh sáng yếu) | Step 2: "Ánh sáng không đủ. Chụp lại." Max 5 lần. | P1 |
| TC-CM04-EC-02 | Edge | Enrollment session expired (>1h) | 409: SESSION_EXPIRED. "Bắt đầu lại." | P2 |
| TC-CM04-EC-03 | Edge | NV đã enrolled → HR yêu cầu RE_ENROLLMENT | Status RE_ENROLLMENT → xóa ảnh cũ C-Vision → NV chụp lại. | P2 |
| TC-CM04-ER-01 | Error | C-Vision API down khi sync | Step 3: "Đồng bộ thất bại. Thử lại sau." Status=FAILED. Retry button. | P1 |
| TC-CM04-ER-02 | Error | C-Vision trả duplicate personId | 409: "Khuôn mặt đã khớp với NV [X]. Kiểm tra lại." | P2 |
| TC-CM04-ER-03 | Error | Ảnh bị che mặt (mask/sunglasses) | Step 2: face detection fail. "Không phát hiện khuôn mặt. Bỏ khẩu trang." | P1 |
| TC-CM04-SEC-01 | Security | Ảnh truyền qua kênh không HTTPS | Enforce HTTPS. Certificate validation. | P1 |
| TC-CM04-SEC-02 | Security | Ảnh retention > 90 ngày | Auto-delete after 90 days. Data Retention Policy compliance. | P2 |
| TC-CM04-CON-01 | Concurrency | 2 HR cùng enroll 1 NV | Session lock: "NV đang được đăng ký bởi [HR2]." | P2 |
| TC-CM04-DI-01 | Data | Enrollment → CVisionPersonMapping | Mapping auto-created. personId ↔ employeeId. | P1 |
