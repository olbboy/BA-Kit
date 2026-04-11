# Test Suite — M07: Cấu hình Lịch nghỉ & Ngày lễ

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen

---

## Coverage Summary

| US | Happy | Edge | Error | Security | Concurrency | Data | Perf | Total |
|----|-------|------|-------|----------|-------------|------|------|-------|
| US-HOL-01 Danh sách ngày nghỉ | 2 | 3 | 2 | 1 | 0 | 1 | 0 | **9** |
| US-HOL-02 Policy & rules | 2 | 3 | 2 | 1 | 0 | 1 | 0 | **9** |
| US-HOL-03 Sync & batch job | 2 | 2 | 2 | 1 | 1 | 1 | 1 | **10** |
| US-HOL-04 API hiển thị | 2 | 2 | 1 | 1 | 0 | 1 | 1 | **8** |
| **Total** | **8** | **10** | **7** | **4** | **1** | **4** | **2** | **36** |

---

| TC-ID | US | Category | Steps | Expected Result | Priority |
|-------|-----|----------|-------|-----------------|----------|
| TC-H01-HP-01 | HOL-01 | Happy | HR tạo ngày lễ Tết Dương lịch 01/01 | Holiday created. Type=NATIONAL. Recurring=yearly. | P1 |
| TC-H01-HP-02 | HOL-01 | Happy | HR xem danh sách 2026 | 10+ ngày lễ quốc gia + custom. Calendar view. | P1 |
| TC-H01-EC-01 | HOL-01 | Edge | Tết Nguyên Đán (Âm lịch → Dương lịch) | Auto-convert lunar date. Hiển thị cả Âm/Dương. | P1 |
| TC-H01-EC-02 | HOL-01 | Edge | Ngày nghỉ bù (Giỗ Tổ rơi T7 → nghỉ Thứ 2) | Compensatory holiday auto-added. Config rule. | P2 |
| TC-H01-EC-03 | HOL-01 | Edge | Multi-tenant: Tenant A có custom holiday, B không | Per-tenant isolation. B không thấy holiday riêng của A. | P2 |
| TC-H01-ER-01 | HOL-01 | Error | Thêm holiday trùng ngày | 409: "Ngày [X] đã có ngày nghỉ." | P2 |
| TC-H01-ER-02 | HOL-01 | Error | Xóa holiday quốc gia | Chặn: "Ngày lễ quốc gia không thể xóa." Custom OK. | P2 |
| TC-H01-SEC-01 | HOL-01 | Security | NV tạo ngày lễ | 403: Chỉ HR/Admin. | P1 |
| TC-H01-DI-01 | HOL-01 | Data | Holiday → leave/OT calculation | Ngày lễ: nghỉ có lương. OT = 3.0x. Attendance = HOLIDAY. | P1 |
| TC-H02-HP-01 | HOL-02 | Happy | HR cấu hình policy annual=12, carryover=5 | Policy saved per-site. | P1 |
| TC-H02-HP-02 | HOL-02 | Happy | HR tạo rule: SICK cần attachment | Rule applied: SICK leave requires file upload. | P1 |
| TC-H02-EC-01 | HOL-02 | Edge | Policy khác nhau per-site | Site A: 12 ngày. Site B: 15 ngày. Correct per NV. | P1 |
| TC-H02-EC-02 | HOL-02 | Edge | Sửa policy mid-year | Pro-rata recalculate. Preview impact. | P2 |
| TC-H02-EC-03 | HOL-02 | Edge | Rule: advance notice = 30 ngày cho MATERNITY | Validate đơn MATERNITY: startDate >= now + 30 days. | P2 |
| TC-H02-ER-01 | HOL-02 | Error | Xóa policy đang active | Chặn: "Policy đang áp dụng cho [N] NV." | P1 |
| TC-H02-ER-02 | HOL-02 | Error | carryoverMax > baseEntitlement | Cảnh báo: "Carryover max > phép cơ bản." | P3 |
| TC-H02-SEC-01 | HOL-02 | Security | Manager sửa policy | 403: Chỉ SITE_HR hoặc GLOBAL_HR. | P1 |
| TC-H02-DI-01 | HOL-02 | Data | Policy → balance calculation | Balance = baseEntitlement + seniority + carryover. Correct. | P1 |
| TC-H03-HP-01 | HOL-03 | Happy | Auto-seed ngày lễ VN đầu năm | Cron job 01/01: seed 10 ngày lễ cho năm mới. | P1 |
| TC-H03-HP-02 | HOL-03 | Happy | Batch recalculate balance | HR trigger → tất cả NV balance tính lại. Audit log. | P1 |
| TC-H03-EC-01 | HOL-03 | Edge | Seed trùng (chạy cron 2 lần) | Idempotent: không tạo duplicate. Skip existing. | P1 |
| TC-H03-EC-02 | HOL-03 | Edge | Tết Âm lịch thay đổi hàng năm | Tính lịch Âm lịch dynamic. Verify 29 tháng Chạp vs 30. | P2 |
| TC-H03-ER-01 | HOL-03 | Error | Batch job fail mid-way | Resume mechanism. Partial progress saved. Alert admin. | P2 |
| TC-H03-ER-02 | HOL-03 | Error | Cron job missed | Retry mechanism. Admin alert. Manual trigger option. | P2 |
| TC-H03-SEC-01 | HOL-03 | Security | Manual trigger cron job | Chỉ SYS_ADMIN. Audit log. | P1 |
| TC-H03-CON-01 | HOL-03 | Concurrency | 2 HR trigger recalculate | Lock: "Batch đang chạy. Vui lòng đợi." | P2 |
| TC-H03-DI-01 | HOL-03 | Data | Seed → holidays table | COUNT(holidays WHERE year=2026) >= 10. Correct dates. | P1 |
| TC-H03-PERF-01 | HOL-03 | Perf | Recalculate 5000 NV | ≤ 60 giây. Background job. Progress. | P2 |
| TC-H04-HP-01 | HOL-04 | Happy | Calendar API: GET /holidays?year=2026 | Return 10+ holidays. Format: date, name, type, dayOfWeek. | P1 |
| TC-H04-HP-02 | HOL-04 | Happy | NV xem lịch nghỉ trên Mini App | Calendar view highlight ngày lễ. Tooltip: tên ngày lễ. | P1 |
| TC-H04-EC-01 | HOL-04 | Edge | Năm nhuận (29/02) | Calendar hiển thị 29/02 đúng. Nếu là holiday → highlight. | P3 |
| TC-H04-EC-02 | HOL-04 | Edge | Holiday trùng cuối tuần (T7/CN) | Calendar hiển thị doubly-marked. Nghỉ bù nếu có rule. | P2 |
| TC-H04-ER-01 | HOL-04 | Error | API year=9999 | 400: "Năm phải trong khoảng 2020-2030." | P3 |
| TC-H04-SEC-01 | HOL-04 | Security | Cross-tenant xem holidays | 403: Chỉ holidays thuộc tenant. National shared. | P1 |
| TC-H04-DI-01 | HOL-04 | Data | API response khớp DB | JSON fields match holidays table columns. | P2 |
| TC-H04-PERF-01 | HOL-04 | Perf | Load calendar + 50 holidays | ≤ 1 giây. Cached. | P2 |
