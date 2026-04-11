# Test Suite — M06: Ca làm việc & Phân ca

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen

---

## Coverage Summary

| US | Happy | Edge | Error | Security | Concurrency | Data | Perf | Total |
|----|-------|------|-------|----------|-------------|------|------|-------|
| US-SHIFT-01 Danh sách ca | 2 | 3 | 2 | 1 | 1 | 1 | 1 | **11** |
| US-SHIFT-02 Cấu hình giờ | 2 | 3 | 2 | 1 | 0 | 1 | 0 | **9** |
| US-SHIFT-03 Punch limit | 2 | 3 | 2 | 1 | 0 | 1 | 0 | **9** |
| US-SHIFT-04 Giờ nghỉ | 2 | 2 | 2 | 1 | 0 | 1 | 0 | **8** |
| US-SHIFT-05 Import NV ca | 2 | 3 | 2 | 1 | 0 | 1 | 1 | **10** |
| US-SHIFT-06 Phân ca pattern | 2 | 3 | 2 | 1 | 1 | 1 | 0 | **10** |
| US-SHIFT-07 Lịch ca team (MGR) | 2 | 3 | 2 | 2 | 0 | 1 | 1 | **11** |
| **Total** | **14** | **20** | **14** | **8** | **2** | **7** | **3** | **68** |

---

## US-SHIFT-01: Danh sách ca làm việc

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-SH01-HP-01 | Happy | HR mở danh sách ca | Thẻ ca hiển thị: tên, badge Active/Inactive, giờ, NV count (+24). | P1 |
| TC-SH01-HP-02 | Happy | HR nhấn vào thẻ ca | Chi tiết ca load bên phải. Viền xanh highlight. | P1 |
| TC-SH01-EC-01 | Edge | Ca không có NV | Thẻ "0 nhân viên", avatar section trống. Không ẩn. | P2 |
| TC-SH01-EC-02 | Edge | >50 ca | Virtual scroll, lazy load 20 batch. Search. | P2 |
| TC-SH01-EC-03 | Edge | Xóa ca có 100 NV active | Chặn: "Không thể xóa ca đang có [N] NV." | P1 |
| TC-SH01-ER-01 | Error | Ca trùng tên (cùng site) | Cảnh báo (cho phép tạo, tên không unique). | P3 |
| TC-SH01-ER-02 | Error | Toggle Inactive ca đang phân | Confirm: "Ca có NV đang phân lịch tuần tới. Xác nhận tắt?" | P2 |
| TC-SH01-SEC-01 | Security | NV truy cập cấu hình ca | 403: Chỉ HR/Admin. | P1 |
| TC-SH01-CON-01 | Concurrency | 2 HR sửa 1 ca | Optimistic lock. "Đã cập nhật bởi [X]." | P2 |
| TC-SH01-DI-01 | Data | NV count khớp | Card "+24" = COUNT(employee_shifts WHERE shift_id=X AND active=true). | P2 |
| TC-SH01-PERF-01 | Perf | Load 50 ca | ≤ 1.5 giây. | P2 |

## US-SHIFT-02 đến US-SHIFT-06

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-SH02-HP-01 | Happy | Cấu hình ca FIXED 08:00-17:00 | startTime/endTime/workingHours=8h saved. | P1 |
| TC-SH02-HP-02 | Happy | Cấu hình ca FLEXIBLE core 10:00-15:00 | flexibleWindow ±2h. Core hours enforced. | P1 |
| TC-SH02-EC-01 | Edge | Ca đêm 20:00-06:00 (cross-day) | isNightShift=true. Logic ngày xuyên midnight. | P1 |
| TC-SH02-EC-02 | Edge | Ca SPLIT 08-12, 14-18 (2 buổi) | breaks=[{unpaid, 12-14}]. 8h working. 2h break. | P2 |
| TC-SH02-EC-03 | Edge | workingHours > 12h | Cảnh báo luật lao động. Confirm. | P2 |
| TC-SH02-ER-01 | Error | startTime > endTime (not night) | 400: "Giờ bắt đầu phải trước giờ kết thúc." | P2 |
| TC-SH02-ER-02 | Error | workingHours = 0 | 400: "Số giờ làm phải > 0." | P2 |
| TC-SH03-HP-01 | Happy | Cấu hình punch limit: early=30min, late=120min | earlyCheckInMinutes=30, lateCheckOutMinutes=120. | P1 |
| TC-SH03-HP-02 | Happy | NV quẹt 35 phút trước ca | Check-in rejected: "Ngoài khung punch limit." | P1 |
| TC-SH03-EC-01 | Edge | early=0 (không cho check-in sớm) | NV phải quẹt đúng giờ ca. | P2 |
| TC-SH03-EC-02 | Edge | late=0 (check-out đúng giờ) | Check-out sau giờ ca → ghi nhận OT candidate. | P2 |
| TC-SH03-EC-03 | Edge | NV punch ngoài limit → nút giải trình | Thông báo: "Check-in ngoài khung giờ. Liên hệ HR." | P2 |
| TC-SH04-HP-01 | Happy | Thêm break 12:00-13:00 isPaid=false | Break saved. Net hours = gross - 1h. | P1 |
| TC-SH04-HP-02 | Happy | Break isPaid=true (nghỉ giải lao 15p) | Net hours không trừ. Vẫn tính lương. | P1 |
| TC-SH04-EC-01 | Edge | Break overlap giờ làm | Validate: break phải nằm trong startTime-endTime. | P2 |
| TC-SH04-EC-02 | Edge | Nhiều breaks tổng > 3h | Cảnh báo: "Tổng giờ nghỉ chiếm >37% ca." | P2 |
| TC-SH05-HP-01 | Happy | Import 50 NV vào ca Sáng từ Excel | 50 employee_shift records created. | P1 |
| TC-SH05-HP-02 | Happy | NV đã có ca → cập nhật | Replace old shift assignment. Audit log. | P1 |
| TC-SH05-EC-01 | Edge | Import NV site khác | Chặn (SITE_HR). GLOBAL_HR cho phép. | P2 |
| TC-SH05-EC-02 | Edge | Import NV Inactive | Skip + ghi vào file lỗi. | P2 |
| TC-SH05-EC-03 | Edge | Rollback import ca | Undo 30 phút. employee_shifts rollback. | P2 |
| TC-SH06-HP-01 | Happy | Phân ca xoay [Sáng, Chiều, Đêm, OFF] 4 NV | 4 NV x 30 ngày = 120 records theo pattern. | P1 |
| TC-SH06-HP-02 | Happy | Preview trước khi áp dụng | Calendar view hiển thị pattern. Confirm. | P1 |
| TC-SH06-EC-01 | Edge | Pattern kéo dài 90 ngày (3 tháng) | Tối đa cho phép. Performance OK. | P2 |
| TC-SH06-EC-02 | Edge | NV đã có ca cá nhân (override) | Cảnh báo: "NV [X] đã có ca riêng ngày [Y]. Ghi đè?" | P2 |
| TC-SH06-EC-03 | Edge | Pattern có OFF trùng ngày lễ | Gộp: ngày đó = Holiday (ưu tiên hơn OFF). | P3 |
| TC-SH06-SEC-01 | Security | NV tạo pattern phân ca | 403: Chỉ HR. | P1 |
| TC-SH06-ER-01 | Error | Pattern rỗng | 400: "Pattern cần ít nhất 1 ca." | P2 |
| TC-SH06-ER-02 | Error | Ca trong pattern Inactive | 400: "Ca [X] đang Inactive. Kích hoạt trước." | P2 |
| TC-SH06-CON-01 | Concurrency | 2 HR phân ca pattern cho cùng NV | Conflict detection. "NV [X] đang được phân ca bởi [HR2]." | P2 |
| TC-SH06-DI-01 | Data | Pattern → employee_shifts | record_count = NV × days. Unique constraint (employee+date). | P1 |
| TC-SH-ALL-SEC | Security | ALL — RBAC HR chi nhánh | HR chỉ quản lý ca thuộc site mình. | P1 |
| TC-SH-ALL-DI | Data | ALL — workingHours = startTime-endTime-breaks | Công thức tính đúng cho mọi ca type. | P1 |
| TC-SH-ALL-ER | Error | ALL — Validation sâu | startTime, endTime bắt buộc. workingHours auto-calc hoặc manual. | P2 |

## US-SHIFT-07: Xem lịch phân ca team (Manager View)

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-SH07-HP-01 | Happy | Manager mở "Lịch phân ca team" → Tuần view | Calendar grid: 7 cột (ngày) × N hàng (NV). Mỗi ô: tên ca + giờ + color code. | P1 |
| TC-SH07-HP-02 | Happy | Manager chuyển sang Tháng view | Calendar compact: 30 cột. Ô hiện tên ca abbreviated. Color coding đúng. | P1 |
| TC-SH07-EC-01 | Edge | NV chưa được gán ca | Ô trống (không màu). Tooltip: "Chưa phân ca." | P2 |
| TC-SH07-EC-02 | Edge | Team > 50 NV (DEPT_HEAD) | Virtual scroll hàng NV. Lazy load. Search NV by name. | P2 |
| TC-SH07-EC-03 | Edge | NV có 2 ca cùng ngày (conflict) | Ô đỏ + badge "⚠️ Xung đột". Link: "Báo HR xử lý." | P2 |
| TC-SH07-ER-01 | Error | Gap detected: Ca sáng có 3/5 NV (< threshold) | Ô highlight đỏ. Tooltip: "Ca Sáng ngày 15/04: 3/5 NV (Thiếu 2)." Nút "Đề xuất bổ sung." | P1 |
| TC-SH07-ER-02 | Error | Manager gửi "Đề xuất đổi ca" thiếu lý do | 400: "Lý do bắt buộc (≥10 ký tự)." | P2 |
| TC-SH07-SEC-01 | Security | Manager xem lịch ca NV team khác | Chặn: chỉ NV có managerId = self. DEPT_HEAD: toàn phòng. | P1 |
| TC-SH07-SEC-02 | Security | Manager cố sửa trực tiếp lịch ca | Không có endpoint. Chỉ "Đề xuất" gửi HR. Read-only calendar. | P1 |
| TC-SH07-DI-01 | Data | Calendar khớp employee_shifts | Verify: mỗi ô = employee_shifts record (employee_id + date + shift_id). | P2 |
| TC-SH07-PERF-01 | Perf | Load tuần 50 NV | ≤ 2 giây. | P2 |
