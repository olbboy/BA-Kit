# Test Suite — M05: Quản lý Nhân sự & CCTC

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen

---

## Coverage Summary

| US | Happy | Edge | Error | Security | Concurrency | Data | Perf | Total |
|----|-------|------|-------|----------|-------------|------|------|-------|
| US-EMP-01 Sơ đồ CCTC | 2 | 2 | 1 | 1 | 0 | 1 | 1 | **8** |
| US-EMP-02 CRUD Phòng ban | 2 | 2 | 2 | 1 | 1 | 1 | 0 | **9** |
| US-EMP-03 Danh sách NV | 2 | 2 | 1 | 1 | 0 | 0 | 1 | **7** |
| US-EMP-04 Bulk Import | 2 | 3 | 3 | 1 | 0 | 1 | 1 | **11** |
| US-EMP-05 Dashboard | 2 | 3 | 1 | 1 | 0 | 1 | 1 | **9** |
| US-EMP-06 Cấp bậc | 2 | 1 | 1 | 1 | 0 | 1 | 0 | **6** |
| **Total** | **12** | **13** | **9** | **6** | **1** | **5** | **4** | **50** |

---

## US-EMP-01: Sơ đồ cơ cấu tổ chức

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-E01-HP-01 | Happy | HR Admin đã đăng nhập, có quyền quản trị | HR mở sơ đồ CCTC | — | Cây tổ chức hiển thị: Org → Sites → Depts → Teams → NV. Expand/Collapse OK. | P1 |
| TC-E01-HP-02 | Happy | NV đã đăng nhập, có ca làm việc active | HR kéo thả NV sang phòng ban khác | — | Drag & drop thành công. Confirm dialog. DB cập nhật dept_id. | P1 |
| TC-E01-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Circular reference (Dept A → B → A) | — | Validate DAG. Chặn: "Không thể tạo vòng lặp trong CCTC". | P1 |
| TC-E01-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Org có 50+ phòng ban | — | Virtual scroll. Lazy load children. Search bar. | P2 |
| TC-E01-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Kéo thả NV sang site khác (cross-site) | — | Chặn nếu HR chi nhánh. GLOBAL_HR cho phép. | P2 |
| TC-E01-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | HR chi nhánh A xem CCTC chi nhánh B | — | Chỉ hiển thị site thuộc ABAC scope. | P1 |
| TC-E01-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Kéo thả → dept_id update | — | Verify DB: employee.department_id = new_dept_id. | P2 |
| TC-E01-PERF-01 | Perf | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Load CCTC 5000 NV | 3, 500, ≤ 3 | Tải ≤ 3 giây. Chỉ load root + L1 ban đầu. | P2 |

## US-EMP-02: Quản lý phòng ban

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-E02-HP-01 | Happy | HR Admin đã đăng nhập, có quyền quản trị | HR tạo phòng ban mới | — | POST /departments → 201. Hiển thị trên cây. | P1 |
| TC-E02-HP-02 | Happy | HR Admin đã đăng nhập, có quyền quản trị | HR sửa tên phòng ban | — | PUT /departments/{id} → 200. Tên cập nhật real-time. | P1 |
| TC-E02-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Xóa phòng ban còn NV | — | Chặn: "Phòng ban có [N] NV. Chuyển NV trước khi xóa." | P1 |
| TC-E02-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Tạo phòng ban cùng tên | — | Cho phép (tên không unique). Nhưng hiển thị warning. | P3 |
| TC-E02-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Xóa phòng ban gốc (root) | — | Chặn: "Không thể xóa phòng ban gốc." | P2 |
| TC-E02-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Tạo phòng ban parentId không tồn tại | 404 | 404: "Phòng ban cha không tồn tại." | P2 |
| TC-E02-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | Manager tạo phòng ban | 403 | 403: Chỉ HR mới có quyền. | P1 |
| TC-E02-CON-01 | Concurrency | 2+ users thao tác đồng thời trên cùng resource | 2 HR cùng sửa 1 phòng ban | — | Optimistic lock: "Đã được cập nhật bởi [Tên]. Tải lại." | P2 |
| TC-E02-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Delete dept → NV dept_id NULL? | — | NV dept_id giữ nguyên (soft-delete dept). Dept status = INACTIVE. | P2 |

## US-EMP-03: Danh sách nhân sự

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-E03-HP-01 | Happy | HR tìm NV theo tên | User đã đăng nhập | GET /employees?search=Nguyễn | API request body/params | Kết quả không phân biệt hoa/thường/dấu. | P1 |
| TC-E03-HP-02 | Happy | HR lọc theo status=ACTIVE + dept | User đã đăng nhập | Filter 2 điều kiện | — | Chỉ NV active thuộc phòng ban chọn. | P1 |
| TC-E03-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Search "nguyen" (không dấu) | — | Fuzzy match: trả về "Nguyễn" results. | P2 |
| TC-E03-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Danh sách 5000+ NV | 500 | Server-side pagination 20/page. Total count header. | P2 |
| TC-E03-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Search query injection | — | Search input sanitized. No SQL injection. | P1 |
| TC-E03-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | HR chi nhánh A xem NV chi nhánh B | — | Chỉ hiển thị NV thuộc site. GLOBAL_HR thấy tất cả. | P1 |
| TC-E03-PERF-01 | Perf | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Load 5000 NV list | 2, 500, ≤ 2 | ≤ 2 giây. Server-side search. | P2 |

## US-EMP-04: Bulk import nhân viên

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-E04-HP-01 | Happy | NV đã đăng nhập, có ca làm việc active | Import 500 NV từ Excel | 500 | Upload .xlsx → Validate → Import thành công. | P1 |
| TC-E04-HP-02 | Happy | User đã đăng nhập thành công | Download file lỗi | 500 | Import 500, 10 lỗi → Trả file Excel kèm cột lỗi. | P1 |
| TC-E04-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Import idempotency (cùng file 2 lần) | 2 | Lần 2: "X bản ghi đã tồn tại — bỏ qua." Không duplicate. | P1 |
| TC-E04-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Rollback import trong 30 phút | 30 | HR nhấn "Hủy import" → Xóa toàn bộ NV batch. Audit log. | P1 |
| TC-E04-EC-03 | Edge | Hệ thống ở trạng thái biên / đặc biệt | File > 5000 bản ghi | 500, 400, 500 | 400: "Tối đa 5000 bản ghi/lần." | P2 |
| TC-E04-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Email trùng | — | Validate: email unique. Ghi lỗi cụ thể "Email [X] đã tồn tại dòng [N]." | P1 |
| TC-E04-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Phòng ban không tồn tại | — | Validate: dept_code. Ghi lỗi "Phòng ban [X] không tồn tại dòng [N]." | P1 |
| TC-E04-ER-03 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | File format sai (.csv thay vì .xlsx) | 400 | 400: "Chỉ hỗ trợ file .xlsx." | P2 |
| TC-E04-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | NV upload file import | 403 | 403: Chỉ HR có quyền. | P1 |
| TC-E04-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Import → employees table consistent | 500 | 500 records in DB. batchId ghi nhận. | P1 |
| TC-E04-PERF-01 | Perf | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Import 5000 NV | 30, 500, ≤ 30 | ≤ 30 giây xử lý. Progress bar hiển thị. | P2 |

## US-EMP-05: Dashboard hiện diện

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-E05-HP-01 | Happy | Manager đã đăng nhập, có team members | Manager mở dashboard | — | 4 counters: On-site / WFH / Vắng / Nghỉ phép. Real-time. | P1 |
| TC-E05-HP-02 | Happy | NV đã đăng nhập, có ca làm việc active | NV quẹt mặt → counter cập nhật | — | Counter "Có mặt" += 1. Real-time update (WebSocket/polling). | P1 |
| TC-E05-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | NV công tác (Business Travel) | — | Counter thứ 5: "Công tác". NV có đơn công tác APPROVED. | P2 |
| TC-E05-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | NV ca FREE — chưa check-in | — | Status "Chưa check-in" (Xám) thay vì "Vắng mặt" (Đỏ). | P2 |
| TC-E05-EC-03 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Tất cả NV vắng (ngày lễ) | — | Counter: 0 on-site. Hiển thị "Hôm nay là ngày nghỉ lễ". | P3 |
| TC-E05-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | WebSocket disconnect | — | Fallback polling 30s. Badge "Dữ liệu có thể chưa cập nhật." | P2 |
| TC-E05-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | Manager xem dashboard phòng ban khác | — | Chặn: chỉ hiển thị NV team. SITE_HR xem toàn site. | P1 |
| TC-E05-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Counters khớp | — | On-site + WFH + Vắng + Nghỉ + Công tác = Tổng NV active. | P1 |
| TC-E05-PERF-01 | Perf | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Dashboard 500 NV | 2, 500, ≤ 2 | Tải ≤ 2 giây. Counter animate on update. | P2 |

## US-EMP-06: Danh mục cấp bậc

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-E06-HP-01 | Happy | HR Admin đã đăng nhập, có quyền quản trị | HR tạo cấp bậc mới "Trưởng dự án" | — | POST /job-levels → 201. Hiển thị trong dropdown. | P1 |
| TC-E06-HP-02 | Happy | HR Admin đã đăng nhập, có quyền quản trị | HR sửa tên cấp bậc | — | PUT /job-levels/{id} → 200. Cập nhật cascading ở NV profiles. | P1 |
| TC-E06-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Xóa cấp bậc đang gán NV | — | Chặn: "Có [N] NV thuộc cấp bậc này." | P2 |
| TC-E06-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Tạo trùng tên | 409 | 409: "Cấp bậc [X] đã tồn tại." | P2 |
| TC-E06-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | NV tạo cấp bậc | 403 | 403: Chỉ HR. | P1 |
| TC-E06-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Cấp bậc → role mapping | — | job_level_id linked to RBAC permission config. Verify cascade. | P2 |

---

## Boundary Value Analysis (BVA)


### Số dòng bulk import (`bulkImportRows`)

| TC-BVA | Value | Type | Expected |
|--------|-------|------|----------|
| BVA-BULKIM-01 | 1 dòng | MIN | ✅ Accept (minimum) |
| BVA-BULKIM-02 | 0 dòng | BELOW_MIN | ❌ Reject: dưới giới hạn |
| BVA-BULKIM-03 | 499 dòng | JUST_BELOW | ✅/⚠️ Accept nhưng gần ngưỡng |
| BVA-BULKIM-04 | 500 dòng | BOUNDARY | ✅ Accept (ngưỡng chính xác) |
| BVA-BULKIM-05 | 501 dòng | JUST_ABOVE | ✅ Accept (vượt ngưỡng 1 đơn vị) |
| BVA-BULKIM-06 | 5000 dòng | MAX | ✅ Accept (maximum) |
| BVA-BULKIM-07 | 5001 dòng | ABOVE_MAX | ❌ Reject: vượt giới hạn |

### Cấp tổ chức (`departmentDepth`)

| TC-BVA | Value | Type | Expected |
|--------|-------|------|----------|
| BVA-DEPART-01 | 1 cấp | MIN | ✅ Accept (minimum) |
| BVA-DEPART-02 | 0 cấp | BELOW_MIN | ❌ Reject: dưới giới hạn |
| BVA-DEPART-03 | 2 cấp | JUST_BELOW | ✅/⚠️ Accept nhưng gần ngưỡng |
| BVA-DEPART-04 | 3 cấp | BOUNDARY | ✅ Accept (ngưỡng chính xác) |
| BVA-DEPART-05 | 4 cấp | JUST_ABOVE | ✅ Accept (vượt ngưỡng 1 đơn vị) |
| BVA-DEPART-06 | 5 cấp | MAX | ✅ Accept (maximum) |
| BVA-DEPART-07 | 6 cấp | ABOVE_MAX | ❌ Reject: vượt giới hạn |
