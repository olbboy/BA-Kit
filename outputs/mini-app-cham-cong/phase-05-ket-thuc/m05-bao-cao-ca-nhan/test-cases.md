# Test Suite — M05-RPT: Báo cáo cá nhân

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen

---

## Coverage Summary

| US | Happy | Edge | Error | Security | Data | Perf | Total |
|----|-------|------|-------|----------|------|------|-------|
| US-RPTPRS-01 Dashboard hiệu suất | 2 | 3 | 1 | 1 | 1 | 1 | **9** |
| US-RPTPRS-02 KPI & highlights | 2 | 2 | 1 | 1 | 1 | 1 | **8** |
| **Total** | **4** | **5** | **2** | **2** | **2** | **2** | **17** |

---

| TC-ID | US | Category | Steps | Expected Result | Priority |
|-------|-----|----------|-------|-----------------|----------|
| TC-RP01-HP-01 | RPTPRS-01 | Happy | NV mở dashboard hiệu suất | Score chuyên cần (%), tổng giờ làm, tổng nghỉ, OT lũy kế. | P1 |
| TC-RP01-HP-02 | RPTPRS-01 | Happy | Biểu đồ trend 4 tuần | Line chart: score theo tuần (4 điểm). Responsive. | P1 |
| TC-RP01-EC-01 | RPTPRS-01 | Edge | NV mới (<4 tuần) | Biểu đồ thiếu điểm dữ liệu. Hiển thị: "Dữ liệu từ [joinDate]." | P2 |
| TC-RP01-EC-02 | RPTPRS-01 | Edge | Trung bình phòng ban (ẩn danh) | Hiển thị avg score phòng ban. Không hiện tên NV khác. | P1 |
| TC-RP01-EC-03 | RPTPRS-01 | Edge | Score = 100% (hoàn hảo) | Badge "Xuất sắc 🏆". Animate. | P3 |
| TC-RP01-ER-01 | RPTPRS-01 | Error | API timeout | Skeleton → "Thử lại." | P3 |
| TC-RP01-SEC-01 | RPTPRS-01 | Security | NV xem dashboard NV khác | 403. ABAC User_ID. | P1 |
| TC-RP01-DI-01 | RPTPRS-01 | Data | Score khớp tính toán | (Ngày đúng giờ / Ngày làm) × 100 = score%. Verify. | P1 |
| TC-RP01-PERF-01 | RPTPRS-01 | Perf | Load dashboard | ≤ 2 giây. | P2 |
| TC-RP02-HP-01 | RPTPRS-02 | Happy | NV xem KPI highlights quý | So sánh Q hiện tại vs Q trước. Arrow up/down. | P1 |
| TC-RP02-HP-02 | RPTPRS-02 | Happy | KPI badges | Achievement badges: "Đúng giờ 30 ngày liên tiếp". | P2 |
| TC-RP02-EC-01 | RPTPRS-02 | Edge | Quý đầu tiên (Q trước không có data) | Không hiển thị comparison. "Chưa đủ dữ liệu so sánh." | P2 |
| TC-RP02-EC-02 | RPTPRS-02 | Edge | NV nghỉ nửa quý | KPI tính pro-rata: chỉ ngày active. | P2 |
| TC-RP02-ER-01 | RPTPRS-02 | Error | KPI calculation division by zero | Protected: mẫu số=0 → "Chưa có dữ liệu." | P2 |
| TC-RP02-SEC-01 | RPTPRS-02 | Security | NV xem KPI NV khác | 403. ABAC. | P1 |
| TC-RP02-DI-01 | RPTPRS-02 | Data | KPI khớp attendance data | Cross-verify score với daily_attendance_summaries. | P1 |
| TC-RP02-PERF-01 | RPTPRS-02 | Perf | Load KPI Q1 (90 ngày) | ≤ 3 giây. | P2 |
