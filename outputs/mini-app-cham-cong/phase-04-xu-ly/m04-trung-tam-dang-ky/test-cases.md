# Test Suite — M04: Trung tâm Đăng ký

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen

---

## Coverage Summary

| US | Happy | Edge | Error | Security | Concurrency | Data | Perf | Total |
|----|-------|------|-------|----------|-------------|------|------|-------|
| US-REG-01 Nghỉ phép | 3 | 5 | 3 | 2 | 1 | 1 | 0 | **15** |
| US-REG-02 Đổi ca | 2 | 3 | 2 | 1 | 1 | 1 | 0 | **10** |
| US-REG-03 Tăng ca | 2 | 4 | 3 | 1 | 0 | 1 | 0 | **11** |
| US-REG-04 Theo dõi đơn | 2 | 2 | 1 | 1 | 0 | 0 | 1 | **7** |
| US-REG-05 Policy phép | 2 | 3 | 2 | 1 | 0 | 1 | 0 | **9** |
| US-REG-06 Công tác/WFH | 2 | 3 | 2 | 1 | 0 | 1 | 0 | **9** |
| **Total** | **13** | **20** | **13** | **7** | **2** | **5** | **1** | **61** |

---

## US-REG-01: Đăng ký nghỉ phép

| TC-ID | Category | Precondition | Steps | Expected Result | Priority |
|-------|----------|-------------|-------|-----------------|----------|
| TC-R01-HP-01 | Happy | NV có 9 ngày phép còn lại | Tạo đơn phép năm 3 ngày | 201 Created. Status PENDING. Balance pending +=3. | P1 |
| TC-R01-HP-02 | Happy | Đơn phép nửa ngày | Chọn halfDay=AM, 1 ngày | workingDays=0.5. Hiển thị "Bạn sẽ nghỉ 0.5 ngày". | P1 |
| TC-R01-HP-03 | Happy | Phép ốm có đính kèm | Tạo đơn SICK + upload giấy khám bệnh | Accepted. File attached. | P1 |
| TC-R01-EC-01 | Edge | Nghỉ xuyên 2 tháng (28/03-02/04) | Tạo đơn phép cross-month | Balance split: tháng 3: -2 ngày, tháng 4: -1 ngày. Hiển thị phân chia. | P2 |
| TC-R01-EC-02 | Edge | Carryover hết hạn 31/03, đăng ký nghỉ 01/04 | Tạo đơn | Trừ vào phép năm mới (không dùng carryover). | P1 |
| TC-R01-EC-03 | Edge | NV thử việc < 12 tháng, vào tháng 7 | Tạo đơn phép năm | Phép = (12×6)/12 = 6 ngày. Công thức hiển thị trên form. | P2 |
| TC-R01-EC-04 | Edge | Nghỉ phép trùng OT đã duyệt ngày 20/05 | Tạo đơn nghỉ ngày 20/05 | Cảnh báo xung đột OT. Confirm → auto-cancel OT + tạo đơn nghỉ. | P1 |
| TC-R01-EC-05 | Edge | Hủy đơn đã APPROVED | Nhấn hủy đơn approved | Không cho hủy trực tiếp. Tạo workflow "Yêu cầu hủy" → HR duyệt. | P2 |
| TC-R01-ER-01 | Error | Trùng ngày nghỉ (PENDING/APPROVED đã tồn tại) | POST leave trùng ngày | 400: DUPLICATE_LEAVE. Hiển thị "Đã có đơn nghỉ ngày X". | P1 |
| TC-R01-ER-02 | Error | Hết phép | POST leave khi balance=0 | 400: INSUFFICIENT_BALANCE. "Không đủ số ngày phép." | P1 |
| TC-R01-ER-03 | Error | Thiếu đính kèm bắt buộc (Ốm) | POST SICK leave without attachment | 400: ATTACHMENT_REQUIRED. | P2 |
| TC-R01-SEC-01 | Security | NV xem balance NV khác | API empId=other | 403 Forbidden. | P1 |
| TC-R01-SEC-02 | Security | HR tạo đơn thay NV (hợp lệ) | HR POST leave cho NV | 201. createdBy=HR. Ghi chú "Tạo bởi HR". | P2 |
| TC-R01-CON-01 | Concurrency | 2 request đồng thời cùng NV trừ phép | Concurrent POST | Chỉ 1 thành công. Pessimistic lock. | P1 |
| TC-R01-DI-01 | Data | Đơn APPROVED → balance update | Approve đơn 3 ngày | balance.used +=3, balance.pending -=3. DB consistent. | P1 |

## US-REG-02: Đăng ký đổi ca

| TC-ID | Category | Precondition | Steps | Expected Result | Priority |
|-------|----------|-------------|-------|-----------------|----------|
| TC-R02-HP-01 | Happy | NV có ca Sáng, đổi sang ca Chiều | POST shift-change | 201. Status PENDING. Hiển thị ca cũ → ca mới. | P1 |
| TC-R02-HP-02 | Happy | Đơn đổi ca được duyệt | Approve shift-change | Ca mới áp dụng vào employee_shifts. Lịch phân ca cập nhật. | P1 |
| TC-R02-EC-01 | Edge | Đổi ca vào ngày đã có OT approved | POST shift-change | Cảnh báo xung đột. Xác nhận trước khi tiếp tục. | P2 |
| TC-R02-EC-02 | Edge | Đổi ca khi NV có đơn nghỉ cùng ngày | POST shift-change | Chặn: "Bạn có đơn nghỉ ngày X. Hủy nghỉ trước khi đổi ca." | P2 |
| TC-R02-EC-03 | Edge | Đổi sang ca đêm (cross-day) | POST shift-change night | Validate: ca đêm cần xử lý logic xuyên ngày. Approval kèm note. | P2 |
| TC-R02-ER-01 | Error | Ca đích không tồn tại/Inactive | POST targetShift=inactive | 400: "Ca [X] không khả dụng". | P2 |
| TC-R02-ER-02 | Error | Đổi ca ngày đã chốt | POST date=locked | 423: PERIOD_LOCKED. | P1 |
| TC-R02-SEC-01 | Security | NV đổi ca cho NV khác | POST empId=other | 403 Forbidden. | P1 |
| TC-R02-CON-01 | Concurrency | 2 NV cùng đổi vào 1 ca đầy | Concurrent POST | Nếu ca có quota → chỉ 1 thành công. Nếu không có quota → cả 2 OK. | P2 |
| TC-R02-DI-01 | Data | Đổi ca → employee_shifts update | After approve | employee_shifts row updated. Daily summary recalculate. | P2 |

## US-REG-03: Đăng ký tăng ca

| TC-ID | Category | Precondition | Steps | Expected Result | Priority |
|-------|----------|-------------|-------|-----------------|----------|
| TC-R03-HP-01 | Happy | NV OT weekday 18:00-21:00 | POST OT request | 201. hours=3, multiplier=1.5x. Status PENDING. | P1 |
| TC-R03-HP-02 | Happy | OT holiday được duyệt | Approve OT ngày lễ | multiplier=3.0x. Summary cập nhật overtime_hours. | P1 |
| TC-R03-EC-01 | Edge-BVA | OT = 4h (giới hạn ngày) | POST OT 4h | Accept (đúng limit). | P1 |
| TC-R03-EC-02 | Edge-BVA | OT = 4h01m (vượt giới hạn ngày) | POST OT 4h01m | 400: "Vượt giới hạn OT ngày (4h)". | P1 |
| TC-R03-EC-03 | Edge | OT lũy kế tháng = 39h, yêu cầu thêm 2h | POST OT 2h | Accept nhưng cảnh báo: "Bạn sẽ vượt 40h/tháng (41h). Cần phê duyệt đặc biệt." | P2 |
| TC-R03-EC-04 | Edge | OT lũy kế năm = 199h | POST OT 2h | Accept. Cảnh báo HR: "NV sắp đạt giới hạn 200h/năm." | P2 |
| TC-R03-ER-01 | Error | Trùng OT cùng ngày (đã có PENDING/APPROVED) | POST OT duplicate | 409: "Đã có đơn OT ngày X." Partial unique index. | P1 |
| TC-R03-ER-02 | Error | OT startTime > endTime | POST startTime=21:00 endTime=18:00 | 400: VALIDATION_ERROR. | P2 |
| TC-R03-ER-03 | Error | OT ngày không phải ngày làm việc/chưa có ca | POST OT no-shift | Cảnh báo: "Bạn không có ca ngày X. Chấp nhận đăng ký OT?" | P2 |
| TC-R03-SEC-01 | Security | NV xem OT lũy kế NV khác | API empId=other | 403 Forbidden. | P1 |
| TC-R03-DI-01 | Data | OT approved → daily_summary.overtime_hours | After approve | daily_attendance_summaries.overtime_hours += approved_hours. | P2 |

## US-REG-04: Theo dõi đơn từ và hạn mức

| TC-ID | Category | Precondition | Steps | Expected Result | Priority |
|-------|----------|-------------|-------|-----------------|----------|
| TC-R04-HP-01 | Happy | NV có 3 đơn: 1 PENDING, 1 APPROVED, 1 REJECTED | Xem danh sách | 3 đơn hiển thị đúng status, filter hoạt động. | P1 |
| TC-R04-HP-02 | Happy | NV xem hạn mức phép | Xem balance | Phép năm: 9/12, Carryover: 2 (hết hạn 31/03). | P1 |
| TC-R04-EC-01 | Edge | Không có đơn nào | Xem danh sách | "Chưa có đơn từ nào". Empty state. | P3 |
| TC-R04-EC-02 | Edge | Đơn > 100 | Xem danh sách | Phân trang 20/trang. Filter theo type + status. | P2 |
| TC-R04-ER-01 | Error | API balance timeout | Xem hạn mức | Skeleton loading → "Không tải được. Thử lại." | P3 |
| TC-R04-SEC-01 | Security | NV xem đơn NV khác | API empId=other | 403 Forbidden. | P1 |
| TC-R04-PERF-01 | Perf | Load danh sách đơn | Mở trang | Tải ≤ 2 giây. | P2 |

## US-REG-05: Cấu hình chính sách phép năm

| TC-ID | Category | Precondition | Steps | Expected Result | Priority |
|-------|----------|-------------|-------|-----------------|----------|
| TC-R05-HP-01 | Happy | HR cập nhật baseEntitlement 12→14 | PUT /leave-policies | Policy cập nhật. Preview: "Ảnh hưởng X NV." | P1 |
| TC-R05-HP-02 | Happy | Batch recalculate sau đổi policy | Confirm recalculate | Balance toàn bộ NV được tính lại. Audit log: old → new. | P1 |
| TC-R05-EC-01 | Edge | carryoverMax = 0 (không cho phép) | PUT carryoverMax=0 | Hệ thống reset carryover balance toàn bộ NV về 0. Cảnh báo trước. | P2 |
| TC-R05-EC-02 | Edge | Sửa policy giữa năm | PUT mid-year | Pro-rata tính lại: NV đã dùng nhiều hơn entitlement mới → cảnh báo. | P2 |
| TC-R05-EC-03 | Edge | halfDayAllowed = false | PUT halfDayAllowed=false | Đơn nghỉ nửa ngày bị chặn. Existing PENDING half-day → cảnh báo. | P2 |
| TC-R05-ER-01 | Error | baseEntitlement < days already used | PUT entitlement < used | Cảnh báo: "X NV đã sử dụng hơn entitlement mới. Xác nhận?" | P1 |
| TC-R05-ER-02 | Error | carryoverExpiry in the past | PUT expiryDate=past | 400: "Ngày hết hạn phải trong tương lai." | P2 |
| TC-R05-SEC-01 | Security | NV (không phải HR) sửa policy | PUT role=EMPLOYEE | 403 Forbidden. | P1 |
| TC-R05-DI-01 | Data | Recalculate consistency | After recalculate | SUM(used + pending + remaining) = total entitlement. | P1 |

## US-REG-06: Đăng ký công tác và WFH

| TC-ID | Category | Precondition | Steps | Expected Result | Priority |
|-------|----------|-------------|-------|-----------------|----------|
| TC-R06-HP-01 | Happy | NV đăng ký WFH 1 ngày | POST WFH request | 201. Status PENDING. Ngày WFH hiển thị trên dashboard. | P1 |
| TC-R06-HP-02 | Happy | NV đăng ký công tác 3 ngày | POST business-trip | 201. Có khoảng ngày, địa điểm công tác. | P1 |
| TC-R06-EC-01 | Edge | WFH trùng ngày có ca tại site | POST WFH ngày có ca | Cảnh báo: "Bạn có ca tại [Site]. WFH sẽ thay thế chấm công camera." | P2 |
| TC-R06-EC-02 | Edge | Công tác dài > 30 ngày | POST trip 31 ngày | Cần phê duyệt GLOBAL_HR thay vì Manager. | P2 |
| TC-R06-EC-03 | Edge | WFH NV ca đêm | POST WFH cho ca đêm | Cảnh báo: "Ca đêm không hỗ trợ WFH. Vui lòng liên hệ HR." | P2 |
| TC-R06-ER-01 | Error | WFH trùng ngày nghỉ phép | POST WFH ngày có leave | 400: "Đã có đơn nghỉ phép ngày X." | P1 |
| TC-R06-ER-02 | Error | Công tác thiếu địa điểm | POST trip no location | 400: VALIDATION_ERROR. "Địa điểm công tác là bắt buộc." | P2 |
| TC-R06-SEC-01 | Security | NV đăng ký WFH cho NV khác | POST empId=other | 403 Forbidden. | P1 |
| TC-R06-DI-01 | Data | WFH approved → dashboard presence | After approve | EMP-05 dashboard hiện "WFH" thay vì "Vắng mặt". | P2 |
