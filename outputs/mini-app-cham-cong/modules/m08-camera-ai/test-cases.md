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

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-CM01-HP-01 | Happy | IT Admin đã đăng nhập, có quyền SYS_ADMIN | IT đăng ký camera mới | — | POST /cameras → 201. deviceId, name, siteId, direction=IN_ONLY. | P1 |
| TC-CM01-HP-02 | Happy | IT Admin đã đăng nhập, có quyền SYS_ADMIN | IT toggle camera Inactive | — | PATCH /cameras/{id}/status → Inactive. Webhook drop + ghi log. | P1 |
| TC-CM01-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Device ID trùng | 409 | 409: "Device ID [X] đã đăng ký tại [Site Y]." | P1 |
| TC-CM01-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Xóa camera đang active (NV check-in hàng ngày) | — | Soft-delete. Cần confirm. Attendance history giữ nguyên. | P1 |
| TC-CM01-EC-03 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Camera chưa đăng ký trên C-Vision | — | Cảnh báo: "Webhook sẽ bị reject." Cho phép lưu draft. | P2 |
| TC-CM01-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | confidenceThreshold=0.69 (out of range) | 422 | 422: "Phải trong 0.70–0.99." | P2 |
| TC-CM01-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Thiếu required fields (deviceId) | 400 | 400: VALIDATION_ERROR. | P2 |
| TC-CM01-ER-03 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | PUT camera đổi deviceId | 400 | 400: IMMUTABLE_FIELD. deviceId không được sửa sau tạo. | P2 |
| TC-CM01-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | HR read-only cameras | — | 200 GET. Không thể POST/PUT/DELETE. | P1 |
| TC-CM01-SEC-02 | Security | Hệ thống ở trạng thái biên / đặc biệt | NV truy cập /cameras | 403 | 403 Forbidden. | P1 |
| TC-CM01-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Camera Active → webhook accepted | — | Webhook từ camera Active → attendance record created. | P1 |

## US-CAM-02: Mapping nhân viên

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-CM02-HP-01 | Happy | NV đã đăng nhập, có ca làm việc active | HR tạo mapping NV ↔ C-Vision person | — | POST /camera-mappings → 201. cvisionPersonId ↔ employeeId. | P1 |
| TC-CM02-HP-02 | Happy | HR Admin đã đăng nhập, có quyền quản trị | HR bulk-create mappings | CSV/Excel file | Bulk POST → N mappings created. | P1 |
| TC-CM02-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Mapping trùng (cùng personId) | 409 | 409: "personId [X] đã được map với NV [Y]." | P1 |
| TC-CM02-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | NV chuyển chi nhánh → mapping cần update | — | HR xóa mapping cũ → tạo mapping mới tại site mới. | P2 |
| TC-CM02-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | employeeId không tồn tại | 404 | 404: EMPLOYEE_NOT_FOUND. | P2 |
| TC-CM02-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Xóa mapping NV đang active | — | Cảnh báo: "NV sẽ không check-in được. Xác nhận?" | P2 |
| TC-CM02-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | NV tạo mapping | 403 | 403: Chỉ HR_ADMIN. | P1 |
| TC-CM02-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Mapping → webhook routing | — | Webhook personId=X → lookup mapping → employeeId=Y → attendance record. | P1 |
| TC-CM02-PERF-01 | Perf | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Bulk 500 mappings | 10, 500, ≤ 10 | ≤ 10 giây. Progress indicator. | P2 |

## US-CAM-03: Health check và monitoring

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-CM03-HP-01 | Happy | IT Admin đã đăng nhập, có quyền SYS_ADMIN | IT xem health dashboard | — | Tổng camera, Active, Offline, Inactive counts. | P1 |
| TC-CM03-HP-02 | Happy | User đã đăng nhập thành công | Camera offline >5 phút | 5 | Badge Offline (Đỏ). Alert IT admin. | P1 |
| TC-CM03-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Camera baru đăng ký (chưa heartbeat) | — | Status "Chờ kết nối" (Vàng). lastHeartbeatAt=null. | P2 |
| TC-CM03-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | 100% cameras offline | 100 | Alert CRITICAL. Push SYS_ADMIN. Dashboard đỏ toàn bộ. | P1 |
| TC-CM03-EC-03 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Heartbeat flapping (online/offline mỗi 30s) | 3 | Debounce: chỉ alert sau 3 lần offline liên tiếp. | P2 |
| TC-CM03-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Health API timeout | 3 | Retry 3 lần. Fallback cached data + "Dữ liệu có thể cũ." | P2 |
| TC-CM03-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Camera gửi heartbeat nhưng không gửi event | — | Cảnh báo "Camera hoạt động nhưng không có sự kiện nhận dạng. Kiểm tra đặt vị trí." | P2 |
| TC-CM03-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | HR xem health dashboard | — | 200 OK (read-only). Chỉ cameras thuộc site. | P1 |
| TC-CM03-PERF-01 | Perf | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Dashboard 200 cameras | 3, ≤ 3 | ≤ 3 giây load. Auto-refresh 30s. | P2 |

## US-CAM-04: Đăng ký khuôn mặt (Face ID Enrollment)

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-CM04-HP-01 | Happy | NV đã đăng nhập, có ca làm việc active | NV đăng ký Face ID 3 bước | — | Step 1: xác nhận info → Step 2: chụp ảnh → Step 3: sync C-Vision. Status=ENROLLED. | P1 |
| TC-CM04-HP-02 | Happy | NV đã đăng nhập, có ca làm việc active | NV chấm công sau enrollment | — | Webhook match personId → attendance record. OK. | P1 |
| TC-CM04-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Ảnh chất lượng thấp (ánh sáng yếu) | 5 | Step 2: "Ánh sáng không đủ. Chụp lại." Max 5 lần. | P1 |
| TC-CM04-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Enrollment session expired (>1h) | 409 | 409: SESSION_EXPIRED. "Bắt đầu lại." | P2 |
| TC-CM04-EC-03 | Edge | Hệ thống ở trạng thái biên / đặc biệt | NV đã enrolled → HR yêu cầu RE_ENROLLMENT | — | Status RE_ENROLLMENT → xóa ảnh cũ C-Vision → NV chụp lại. | P2 |
| TC-CM04-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | C-Vision API down khi sync | API request body/params | Step 3: "Đồng bộ thất bại. Thử lại sau." Status=FAILED. Retry button. | P1 |
| TC-CM04-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | C-Vision trả duplicate personId | 409 | 409: "Khuôn mặt đã khớp với NV [X]. Kiểm tra lại." | P2 |
| TC-CM04-ER-03 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Ảnh bị che mặt (mask/sunglasses) | — | Step 2: face detection fail. "Không phát hiện khuôn mặt. Bỏ khẩu trang." | P1 |
| TC-CM04-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | Ảnh truyền qua kênh không HTTPS | — | Enforce HTTPS. Certificate validation. | P1 |
| TC-CM04-SEC-02 | Security | Hệ thống ở trạng thái biên / đặc biệt | Ảnh retention > 90 ngày | 90 | Auto-delete after 90 days. Data Retention Policy compliance. | P2 |
| TC-CM04-CON-01 | Concurrency | 2+ users thao tác đồng thời trên cùng resource | 2 HR cùng enroll 1 NV | — | Session lock: "NV đang được đăng ký bởi [HR2]." | P2 |
| TC-CM04-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Enrollment → CVisionPersonMapping | — | Mapping auto-created. personId ↔ employeeId. | P1 |

---

## Boundary Value Analysis (BVA)


### Ngưỡng confidence nhận diện (`confidenceThreshold`)

| TC-BVA | Value | Type | Expected |
|--------|-------|------|----------|
| BVA-CONFID-01 | 0.7 | MIN | ✅ Accept (minimum) |
| BVA-CONFID-02 | 0.69 | BELOW_MIN | ❌ Reject: dưới giới hạn |
| BVA-CONFID-03 | 0.84 | JUST_BELOW | ✅/⚠️ Accept nhưng gần ngưỡng |
| BVA-CONFID-04 | 0.85 | BOUNDARY | ✅ Accept (ngưỡng chính xác) |
| BVA-CONFID-05 | 0.86 | JUST_ABOVE | ✅ Accept (vượt ngưỡng 1 đơn vị) |
| BVA-CONFID-06 | 0.99 | MAX | ✅ Accept (maximum) |
| BVA-CONFID-07 | 1.0 | ABOVE_MAX | ❌ Reject: vượt giới hạn |

### Tần suất heartbeat (`heartbeatInterval`)

| TC-BVA | Value | Type | Expected |
|--------|-------|------|----------|
| BVA-HEARTB-01 | 10 giây | MIN | ✅ Accept (minimum) |
| BVA-HEARTB-02 | 9 giây | BELOW_MIN | ❌ Reject: dưới giới hạn |
| BVA-HEARTB-03 | 59 giây | JUST_BELOW | ✅/⚠️ Accept nhưng gần ngưỡng |
| BVA-HEARTB-04 | 60 giây | BOUNDARY | ✅ Accept (ngưỡng chính xác) |
| BVA-HEARTB-05 | 61 giây | JUST_ABOVE | ✅ Accept (vượt ngưỡng 1 đơn vị) |
| BVA-HEARTB-06 | 300 giây | MAX | ✅ Accept (maximum) |
| BVA-HEARTB-07 | 301 giây | ABOVE_MAX | ❌ Reject: vượt giới hạn |

### Số ảnh đăng ký khuôn mặt (`enrollmentPhotos`)

| TC-BVA | Value | Type | Expected |
|--------|-------|------|----------|
| BVA-ENROLL-01 | 1 ảnh | MIN | ✅ Accept (minimum) |
| BVA-ENROLL-02 | 0 ảnh | BELOW_MIN | ❌ Reject: dưới giới hạn |
| BVA-ENROLL-03 | 2 ảnh | JUST_BELOW | ✅/⚠️ Accept nhưng gần ngưỡng |
| BVA-ENROLL-04 | 3 ảnh | BOUNDARY | ✅ Accept (ngưỡng chính xác) |
| BVA-ENROLL-05 | 4 ảnh | JUST_ABOVE | ✅ Accept (vượt ngưỡng 1 đơn vị) |
| BVA-ENROLL-06 | 5 ảnh | MAX | ✅ Accept (maximum) |
| BVA-ENROLL-07 | 6 ảnh | ABOVE_MAX | ❌ Reject: vượt giới hạn |
