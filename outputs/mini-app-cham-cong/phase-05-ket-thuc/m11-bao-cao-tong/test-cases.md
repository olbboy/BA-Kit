# Test Suite — M11: Báo cáo tổng & Xuất

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen

---

## Coverage Summary

| US | Happy | Edge | Error | Security | Concurrency | Data | Perf | Total |
|----|-------|------|-------|----------|-------------|------|------|-------|
| US-RPT-01 Dashboard quản lý | 2 | 3 | 2 | 2 | 0 | 1 | 1 | **11** |
| US-RPT-02 Xuất báo cáo/payroll | 2 | 3 | 2 | 1 | 1 | 1 | 1 | **11** |
| US-RPT-03 Báo cáo tuân thủ | 2 | 2 | 1 | 1 | 0 | 1 | 0 | **7** |
| US-RPT-04 Khóa kỳ lương | 2 | 3 | 2 | 2 | 1 | 1 | 0 | **11** |
| **Total** | **8** | **11** | **7** | **6** | **2** | **4** | **2** | **40** |

---

| TC-ID | US | Category | Steps | Expected Result | Priority |
|-------|-----|----------|-------|-----------------|----------|
| TC-RT01-HP-01 | RPT-01 | Happy | Manager mở dashboard | 6 counters + biểu đồ + top vi phạm. Data scope = team. | P1 |
| TC-RT01-HP-02 | RPT-01 | Happy | Drill-down counter "Đi trễ" | Danh sách NV đi trễ hôm nay. | P1 |
| TC-RT01-EC-01 | RPT-01 | Edge | Phòng ban không có NV | "Chưa có dữ liệu". Không tính vào average. | P2 |
| TC-RT01-EC-02 | RPT-01 | Edge | Dữ liệu chưa chốt | Badge cam: "Dữ liệu tạm tính." Live update. | P2 |
| TC-RT01-EC-03 | RPT-01 | Edge | Tổng = Có mặt + Trễ + Vắng + Nghỉ | Verify counters sum. Mismatch = BUG. | P1 |
| TC-RT01-ER-01 | RPT-01 | Error | Biểu đồ render fail | Fallback: table view. Error message. | P3 |
| TC-RT01-ER-02 | RPT-01 | Error | 0 NV active (phòng ban deactivated) | Empty state. "Phòng ban không có NV." | P3 |
| TC-RT01-SEC-01 | RPT-01 | Security | Manager xem data site khác | Chặn. RBAC scope = team/dept. | P1 |
| TC-RT01-SEC-02 | RPT-01 | Security | GLOBAL_HR xem tất cả sites | 200 OK. All sites accessible. | P1 |
| TC-RT01-DI-01 | RPT-01 | Data | Counters khớp DB aggregation | Tổng NV = COUNT employees active. Có mặt = SUM present today. | P1 |
| TC-RT01-PERF-01 | RPT-01 | Perf | Dashboard 5000 NV | ≤ 3 giây. Cached aggregation. | P1 |
| TC-RT02-HP-01 | RPT-02 | Happy | HR xuất payroll Excel tháng 4 | File .xlsx 13 cột. 500 NV rows. | P1 |
| TC-RT02-HP-02 | RPT-02 | Happy | HR xuất CSV | File .csv tương tự Excel. UTF-8 BOM for VN chars. | P1 |
| TC-RT02-EC-01 | RPT-02 | Edge | NV mới giữa tháng | Pro-rata ngày công. Ghi chú dòng "NV mới từ dd/MM". | P2 |
| TC-RT02-EC-02 | RPT-02 | Edge | NV nghỉ việc giữa tháng | Ngày công tính đến lastWorkingDate. Ghi chú. | P2 |
| TC-RT02-EC-03 | RPT-02 | Edge | Payroll tháng có OT > 200h/năm | Cảnh báo compliance: "NV [X] vượt giới hạn OT năm." | P1 |
| TC-RT02-ER-01 | RPT-02 | Error | Export 10000 NV | Queue job. Download link khi ready. Timeout 5 phút max. | P2 |
| TC-RT02-ER-02 | RPT-02 | Error | Export kỳ chưa chốt | Cảnh báo: "Dữ liệu chưa chốt. Số liệu tạm tính." Cho phép export. | P2 |
| TC-RT02-SEC-01 | RPT-02 | Security | Manager xuất payroll (không phải HR) | 403: Chỉ SITE_HR hoặc GLOBAL_HR. | P1 |
| TC-RT02-CON-01 | RPT-02 | Concurrency | 2 HR export cùng lúc | Parallel OK. Separate file generations. | P3 |
| TC-RT02-DI-01 | RPT-02 | Data | Excel data khớp DB | Random sample 10 NV: verify ngày công, OT, phép against DB. | P1 |
| TC-RT02-PERF-01 | RPT-02 | Perf | Export 5000 NV | ≤ 30 giây generation. File ≤ 5MB. | P2 |
| TC-RT03-HP-01 | RPT-03 | Happy | HR xem báo cáo tuân thủ luật lao động | Checklist: OT ≤200h/năm, phép ≥12 ngày, ... | P1 |
| TC-RT03-HP-02 | RPT-03 | Happy | Violation alert: NV vượt OT | Red flag per NV. Summary count. | P1 |
| TC-RT03-EC-01 | RPT-03 | Edge | OT limit đặc biệt 300h (đã approved) | Hiển thị "Mở rộng đã duyệt" thay vì violation. | P2 |
| TC-RT03-EC-02 | RPT-03 | Edge | NV thâm niên 7 năm → 13 ngày phép | Báo cáo tính đúng entitlement theo seniority. | P2 |
| TC-RT03-ER-01 | RPT-03 | Error | Missing employment data | Skip NV + flag: "Thiếu ngày bắt đầu làm." | P3 |
| TC-RT03-SEC-01 | RPT-03 | Security | NV xem compliance report | 403. Chỉ HR/SYS_ADMIN. | P1 |
| TC-RT03-DI-01 | RPT-03 | Data | Compliance rules khớp Luật LĐ VN | Verify OT limits, leave entitlements vs Nghị định 13/2023. | P1 |
| TC-RT04-HP-01 | RPT-04 | Happy | HR khóa kỳ lương tháng 4 | POST lock. Status LOCKED. No more changes. | P1 |
| TC-RT04-HP-02 | RPT-04 | Happy | HR re-export (new version) | New version created. Old version preserved in history. | P1 |
| TC-RT04-EC-01 | RPT-04 | Edge | Correction sau lock | Cảnh báo: "Kỳ lương tháng X đã xuất." Ghi nhận kỳ bổ sung. | P1 |
| TC-RT04-EC-02 | RPT-04 | Edge | Lock khi chưa chốt công | Chặn: "Chốt công chưa hoàn tất. Vui lòng chốt trước." | P1 |
| TC-RT04-EC-03 | RPT-04 | Edge | Supplementary payroll | Thay đổi sau lock → kỳ bổ sung riêng biệt. | P2 |
| TC-RT04-ER-01 | RPT-04 | Error | Lock khi có draft corrections | Cảnh báo: "[N] corrections chưa xử lý. Xác nhận lock?" | P2 |
| TC-RT04-ER-02 | RPT-04 | Error | Unlock kỳ đã lock >30 ngày | Chặn: "Không thể unlock sau 30 ngày." | P2 |
| TC-RT04-SEC-01 | RPT-04 | Security | Manager lock kỳ lương | 403: Chỉ SITE_HR/GLOBAL_HR. | P1 |
| TC-RT04-SEC-02 | RPT-04 | Security | Unlock không có audit trail | Enforce: audit log bắt buộc. Block nếu reason rỗng. | P1 |
| TC-RT04-CON-01 | RPT-04 | Concurrency | 2 HR lock cùng kỳ | Idempotent: lần 2 → "Kỳ đã được khóa." | P2 |
| TC-RT04-DI-01 | RPT-04 | Data | Lock → read-only constraint | Verify: INSERT/UPDATE attendance cho tháng locked → 423 error. | P1 |
