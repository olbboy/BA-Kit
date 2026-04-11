# Test Suite — M03: Giải trình công

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen

---

## Coverage Summary

| US | Happy | Edge | Error | Security | Concurrency | Data | Perf | Total |
|----|-------|------|-------|----------|-------------|------|------|-------|
| US-EXPL-01 Danh sách lỗi | 2 | 3 | 2 | 1 | 0 | 1 | 1 | **10** |
| US-EXPL-02 Yêu cầu sửa | 2 | 3 | 3 | 2 | 1 | 1 | 0 | **12** |
| **Total** | **4** | **6** | **5** | **3** | **1** | **2** | **1** | **22** |

---

| TC-ID | US | Category | Steps | Expected Result | Priority |
|-------|-----|----------|-------|-----------------|----------|
| TC-EX01-HP-01 | EXPL-01 | Happy | NV mở danh sách violations | Đi muộn, về sớm, vắng — hiển thị badge + severity. | P1 |
| TC-EX01-HP-02 | EXPL-01 | Happy | NV nhấn "Giải trình ngay" | Chuyển sang form giải trình, ngày tự điền. | P1 |
| TC-EX01-EC-01 | EXPL-01 | Edge | Violations sau chốt công | Nút giải trình disabled. "Kỳ đã chốt." | P1 |
| TC-EX01-EC-02 | EXPL-01 | Edge | NV không có violations | "Không có lỗi cần giải trình. 🎉" | P3 |
| TC-EX01-EC-03 | EXPL-01 | Edge | Violations + đơn PENDING | Badge "Đang giải trình" (Vàng). Ẩn nút submit mới. | P2 |
| TC-EX01-ER-01 | EXPL-01 | Error | API violations timeout | Skeleton +retry. "Không tải được." | P3 |
| TC-EX01-ER-02 | EXPL-01 | Error | Violation cho ngày chưa chấm công | Loại ABSENT hiển thị. Giải trình as "Lý do vắng mặt". | P2 |
| TC-EX01-SEC-01 | EXPL-01 | Security | NV xem violations NV khác | 403 Forbidden. ABAC. | P1 |
| TC-EX01-DI-01 | EXPL-01 | Data | Violations khớp attendance_anomalies | COUNT UI = COUNT DB WHERE resolved=false. | P1 |
| TC-EX01-PERF-01 | EXPL-01 | Perf | Load 30 violations | ≤ 2 giây. Pagination 10/trang. | P2 |
| TC-EX02-HP-01 | EXPL-02 | Happy | NV gửi sửa chấm công (MODIFY) | POST correction: old time → new time + reason. PENDING. | P1 |
| TC-EX02-HP-02 | EXPL-02 | Happy | Correction approved | Record gốc updated. Daily summary recalculated. | P1 |
| TC-EX02-EC-01 | EXPL-02 | Edge | Correction ADD (quên check-out) | NV thêm mốc check-out. Approval required. | P1 |
| TC-EX02-EC-02 | EXPL-02 | Edge | Correction DELETE (check-in nhầm) | NV yêu cầu xóa record. HR review bắt buộc. | P2 |
| TC-EX02-EC-03 | EXPL-02 | Edge | Correction cho ngày đã chốt | 423: PERIOD_LOCKED. Exception unlock cần GLOBAL_HR. | P1 |
| TC-EX02-ER-01 | EXPL-02 | Error | Reason < 20 ký tự | 400: "Lý do cần ít nhất 20 ký tự." | P2 |
| TC-EX02-ER-02 | EXPL-02 | Error | File evidence > 5MB | 400: "File quá lớn." | P3 |
| TC-EX02-ER-03 | EXPL-02 | Error | Correction trùng (cùng NV cùng ngày PENDING) | 409: "Đã có yêu cầu sửa ngày [X]." | P2 |
| TC-EX02-SEC-01 | EXPL-02 | Security | NV sửa chấm công NV khác | 403, ABAC chặn. | P1 |
| TC-EX02-SEC-02 | EXPL-02 | Security | NV tự approve correction | 403: SELF_APPROVE_FORBIDDEN. | P1 |
| TC-EX02-CON-01 | EXPL-02 | Concurrency | Approve correction khi daily summary đang recalculate | DB transaction. Recalculate trong transaction. No partial state. | P2 |
| TC-EX02-DI-01 | EXPL-02 | Data | Correction → attendance_corrections + summary | correction entry + daily_summary updated atomically. | P1 |
