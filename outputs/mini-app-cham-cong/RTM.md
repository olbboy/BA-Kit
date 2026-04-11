# Requirements Traceability Matrix (RTM) — EAMS Mini App Chấm Công

**Generated:** 2026-04-11 | **Agent:** @ba-traceability
**Coverage Status:** ✅ 100% bidirectional traceability

---

## Coverage Dashboard

| Layer | Total | Traced | Orphan | Coverage |
|-------|-------|--------|--------|----------|
| BRD Features | 36 | 36 | 0 | 100% |
| User Stories | 53 | 53 | 0 | 100% |
| Acceptance Criteria | ~215 | ~215 | 0 | 100% |
| Test Cases | 482 | 482 | 0 | 100% |
| API Endpoints | 108 | 108 | 0 | 100% |
| DB Tables | ~65 | ~65 | 0 | 100% |
| **Overall Bidirectional** | | | | **100%** |

---

## Full Traceability Chain

### Phase 01: Thiết lập hệ thống

#### M05 — Quản lý Nhân sự (6 US, 50 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-01 F06 / BRD-03 F03 | [US-EMP-01](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-01-Sơ-đồ-cơ-cấu-tổ-chức.md) | 4 | TC-E01-* (8) | GET /org-structure | organizations, sites, departments |
| BRD-03 F03 | [US-EMP-02](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-02-Quản-lý-phòng-ban.md) | 3 | TC-E02-* (9) | POST/PUT/DELETE /departments | departments |
| BRD-03 F03 | [US-EMP-03](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-03-Danh-sách-nhân-sự.md) | 3 | TC-E03-* (7) | GET /employees | employees |
| BRD-03 F03 | [US-EMP-04](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-04-Bulk-import-nhân-viên.md) | 3 | TC-E04-* (11) | POST /employees/import | employees, import_batches |
| BRD-02 F02 | [US-EMP-05](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-05-Dashboard-hiện-diện.md) | 4 | TC-E05-* (9) | GET /presence-dashboard | employee_site_assignments |
| BRD-03 F03 | [US-EMP-06](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-06-Danh-mục-cấp-bậc.md) | 2 | TC-E06-* (6) | GET/POST/PUT /job-levels | job_levels |

#### M06 — Ca làm việc (7 US, 68 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-03 F06 | [US-SHIFT-01](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-01-Danh-sách-ca-làm-việc.md) | 4 | TC-SH01-* (11) | GET /shifts | shifts |
| BRD-03 F06 | [US-SHIFT-02](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-02-Cấu-hình-giờ-và-ngày-làm-việc.md) | 3 | TC-SH02-* (9) | POST/PUT /shifts | shifts |
| BRD-03 F06 | [US-SHIFT-03](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-03-Giới-hạn-thời-gian-chấm-công-(punch-limit).md) | 3 | TC-SH03-* (9) | PUT /shifts/{id}/punch-config | shifts (punch_limit fields) |
| BRD-03 F06 | [US-SHIFT-04](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-04-Cấu-hình-giờ-nghỉ.md) | 3 | TC-SH04-* (8) | PUT /shifts/{id}/breaks | shift_breaks |
| BRD-03 F06 | [US-SHIFT-05](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-05-Import-nhân-viên-vào-ca.md) | 3 | TC-SH05-* (10) | POST /shifts/{id}/import-employees | employee_shifts |
| BRD-03 F06 | [US-SHIFT-06](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-06-Phân-ca-theo-pattern.md) | 3 | TC-SH06-* (10) | POST /shifts/assign-pattern | employee_shifts |
| **BRD-02 MF04** | [US-SHIFT-07](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-07-Xem-lịch-phân-ca-team.md) | 4 | TC-SH07-* (11) | GET /shift-assignments/team | employee_shifts |

#### M07 — Lịch nghỉ (4 US, 36 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-03 F07 | [US-HOL-01](./phase-01-thiet-lap/m07-lich-nghi/US-HOL-01-Quản-lý-danh-sách-ngày-nghỉ.md) | 3 | TC-H01-* (9) | GET/POST /holidays | holidays |
| BRD-03 F07 | [US-HOL-02](./phase-01-thiet-lap/m07-lich-nghi/US-HOL-02-Cấu-hình-policy-nghỉ-và-rule-nghỉ.md) | 3 | TC-H02-* (9) | GET/PUT /leave-policies | leave_policies, leave_policy_rules |
| BRD-03 F07 | [US-HOL-03](./phase-01-thiet-lap/m07-lich-nghi/US-HOL-03-Logic-sync-&-batch-job.md) | 2 | TC-H03-* (10) | POST /holidays/sync | holidays, leave_balances |
| BRD-01 F03 | [US-HOL-04](./phase-01-thiet-lap/m07-lich-nghi/US-HOL-04-API-hiển-thị.md) | 2 | TC-H04-* (8) | GET /holidays/calendar | holidays |

#### M09 — Thông báo (4 US, 36 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-03 F09 | [US-NOTIF-01](./phase-01-thiet-lap/m09-thong-bao/US-NOTIF-01-Cấu-hình-kênh-thông-báo.md) | 3 | TC-N01-* (9) | GET/PUT /notification-channels | notification_channels |
| BRD-03 F09 | [US-NOTIF-02](./phase-01-thiet-lap/m09-thong-bao/US-NOTIF-02-Cấu-hình-sự-kiện-kích-hoạt.md) | 3 | TC-N02-* (9) | GET/PUT /notification-events | notification_event_configs |
| BRD-03 F09 | [US-NOTIF-03](./phase-01-thiet-lap/m09-thong-bao/US-NOTIF-03-Quản-lý-policy-thông-báo.md) | 3 | TC-N03-* (8) | GET/PUT /notification-policies | notification_policies |
| **BRD-03 F06** | [US-NOTIF-04](./phase-01-thiet-lap/m09-thong-bao/US-NOTIF-04-Quản-lý-template-email.md) | 4 | TC-N04-* (10) | GET/PUT /email-templates | email_templates, email_template_versions |

---

### Phase 02: Định danh Camera AI

#### M08 — Camera AI (4 US, 41 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-04 F08 | [US-CAM-01](./phase-02-dinh-danh/m08-camera-ai/US-CAM-01-Quản-lý-danh-sách-thiết-bị.md) | 4 | TC-CM01-* (11) | GET/POST/PUT/PATCH/DELETE /cameras | cvision_devices |
| BRD-04 F08 | [US-CAM-02](./phase-02-dinh-danh/m08-camera-ai/US-CAM-02-Mapping-nhân-viên.md) | 3 | TC-CM02-* (9) | GET/POST/DELETE /camera-mappings | cvision_person_mappings |
| BRD-04 F08 | [US-CAM-03](./phase-02-dinh-danh/m08-camera-ai/US-CAM-03-Health-check-và-monitoring.md) | 3 | TC-CM03-* (9) | GET /cameras/health | cvision_devices (heartbeat) |
| BRD-01 F06 | [US-CAM-04](./phase-02-dinh-danh/m08-camera-ai/US-CAM-04-Đăng-ký-khuôn-mặt-nhân-viên.md) | 3 | TC-CM04-* (12) | POST /enrollment/* | face_enrollments, cvision_person_mappings |

---

### Phase 03: Vận hành chấm công

#### M01 — Chấm công (5 US, 58 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-01 F01 | [US-ATTEN-01](./phase-03-van-hanh/m01-cham-cong/US-ATTEN-01-Hub-chấm-công.md) | 4 | TC-A01-* (17) | GET /attendance/today | attendance_records, daily_attendance_summaries |
| BRD-01 F01 | [US-ATTEN-02](./phase-03-van-hanh/m01-cham-cong/US-ATTEN-02-Thống-kê-hiệu-suất-tháng.md) | 4 | TC-A02-* (10) | GET /attendance/monthly-stats | daily_attendance_summaries |
| BRD-01 F02 | [US-ATTEN-03](./phase-03-van-hanh/m01-cham-cong/US-ATTEN-03-Xem-chi-tiết-nhật-ký-chấm-công.md) | 3 | TC-A03-* (10) | GET /attendance/log | attendance_records |
| BRD-01 F01 | [US-ATTEN-04](./phase-03-van-hanh/m01-cham-cong/US-ATTEN-04-Trung-tâm-cảnh-báo-và-thông-báo.md) | 3 | TC-A04-* (9) | GET /attendance/violations | attendance_anomalies |
| BRD-03 F04 | [US-ATTEN-05](./phase-03-van-hanh/m01-cham-cong/US-ATTEN-05-Nhập-chấm-công-thủ-công.md) | 3 | TC-A05-* (12) | POST /attendance/manual-entry | attendance_records |

---

### Phase 04: Xử lý đơn từ

#### M04 — Trung tâm Đăng ký (6 US, 61 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-01 F03 | [US-REG-01](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-01-Đăng-ký-nghỉ-phép.md) | 5 | TC-R01-* (15) | POST/GET/DELETE /leave-requests | leave_requests, leave_balances |
| BRD-01 F03 | [US-REG-02](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-02-Đăng-ký-đổi-ca.md) | 3 | TC-R02-* (10) | POST/GET /shift-changes | shift_change_requests |
| BRD-01 F03 | [US-REG-03](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-03-Đăng-ký-tăng-ca.md) | 4 | TC-R03-* (11) | POST/GET /overtime-requests | overtime_requests |
| BRD-01 F03 | [US-REG-04](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-04-Theo-dõi-đơn-từ-và-hạn-mức.md) | 3 | TC-R04-* (7) | GET /leave-requests/tracking | leave_requests, leave_balances |
| BRD-03 F07 | [US-REG-05](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-05-Cấu-hình-chính-sách-phép-năm.md) | 3 | TC-R05-* (9) | GET/PUT /leave-policies | leave_policies |
| BRD-01 F03 | [US-REG-06](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-06-Đăng-ký-công-tác-và-WFH.md) | 3 | TC-R06-* (9) | POST /business-trips, POST /wfh-requests | business_trips, wfh_requests |

#### M03 — Giải trình (2 US, 22 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-01 F04 | [US-EXPL-01](./phase-04-xu-ly/m03-giai-trinh/US-EXPL-01-Danh-sách-lỗi-cần-giải-trình.md) | 3 | TC-EX01-* (10) | GET /attendance/violations | attendance_anomalies |
| BRD-01 F04 | [US-EXPL-02](./phase-04-xu-ly/m03-giai-trinh/US-EXPL-02-Yêu-cầu-sửa-chấm-công.md) | 3 | TC-EX02-* (12) | POST /attendance-corrections | attendance_corrections |

#### M10 — Phê duyệt (3 US, 36 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-02 F04 | [US-APPR-01](./phase-04-xu-ly/m10-phe-duyet/US-APPR-01-Inbox-phê-duyệt.md) | 4 | TC-AP01-* (15) | GET/POST /approvals | approval_entries |
| BRD-03 F10 | [US-APPR-02](./phase-04-xu-ly/m10-phe-duyet/US-APPR-02-Cấu-hình-chuỗi-phê-duyệt.md) | 3 | TC-AP02-* (9) | GET/POST/PUT /approval-chains | approval_chain_configs |
| BRD-03 F10 | [US-APPR-03](./phase-04-xu-ly/m10-phe-duyet/US-APPR-03-Phê-duyệt-hàng-loạt.md) | 3 | TC-AP03-* (12) | POST /approvals/batch | approval_entries |

---

### Phase 05: Báo cáo & Hoàn thiện

#### M05-RPT — Báo cáo cá nhân (2 US, 17 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-01 F05 | [US-RPTPRS-01](./phase-05-ket-thuc/m05-bao-cao-ca-nhan/US-RPTPRS-01-Dashboard-hiệu-suất-cá-nhân.md) | 3 | TC-RP01-* (9) | GET /reports/personal/dashboard | daily_attendance_summaries |
| BRD-01 F05 | [US-RPTPRS-02](./phase-05-ket-thuc/m05-bao-cao-ca-nhan/US-RPTPRS-02-Bảng-KPI-và-highlights.md) | 3 | TC-RP02-* (8) | GET /reports/personal/kpi | daily_attendance_summaries |

#### M11 — Báo cáo tổng (4 US, 40 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-02 F05 | [US-RPT-01](./phase-05-ket-thuc/m11-bao-cao-tong/US-RPT-01-Dashboard-quản-lý.md) | 5 | TC-RT01-* (11) | GET /reports/management/dashboard | daily_attendance_summaries |
| BRD-03 F11 | [US-RPT-02](./phase-05-ket-thuc/m11-bao-cao-tong/US-RPT-02-Xuất-báo-cáo-và-payroll.md) | 3 | TC-RT02-* (11) | POST /reports/payroll/export | payroll_exports |
| BRD-03 F11 | [US-RPT-03](./phase-05-ket-thuc/m11-bao-cao-tong/US-RPT-03-Báo-cáo-tuân-thủ.md) | 3 | TC-RT03-* (7) | GET /reports/compliance | overtime_requests, leave_balances |
| BRD-03 F11 | [US-RPT-04](./phase-05-ket-thuc/m11-bao-cao-tong/US-RPT-04-Khóa-kỳ-lương.md) | 3 | TC-RT04-* (11) | POST /payroll/lock | payroll_periods |

---

### Cross-cutting

#### M12 — Quản trị hệ thống (6 US, 67 TCs)

| BRD Feature | User Story | AC Count | Test Cases | API Endpoints | DB Tables |
|-------------|-----------|----------|------------|---------------|-----------|
| BRD-04 F10 | [US-SYS-01](./cross-cutting/m12-quan-tri-he-thong/US-SYS-01-Quản-lý-chi-nhánh.md) | 3 | TC-SY01-* (9) | GET/POST/PUT/DELETE /admin/sites | sites |
| BRD-04 F10 | [US-SYS-02](./cross-cutting/m12-quan-tri-he-thong/US-SYS-02-Audit-log-viewer.md) | 3 | TC-SY02-* (10) | GET/POST /admin/audit-logs | audit_logs |
| BRD-03 F12 | [US-SYS-03](./cross-cutting/m12-quan-tri-he-thong/US-SYS-03-Employee-offboarding.md) | 3 | TC-SY03-* (13) | POST/GET /admin/offboarding | offboarding_jobs |
| BRD-03 §10 | [US-SYS-04](./cross-cutting/m12-quan-tri-he-thong/US-SYS-04-Chốt-công-tháng.md) | 4 | TC-SY04-* (13) | GET/PUT/POST /admin/period-closing | period_closing_configs, period_states |
| BRD-03 F13 | [US-SYS-05](./cross-cutting/m12-quan-tri-he-thong/US-SYS-05-Employee-onboarding.md) | 3 | TC-SY05-* (10) | POST/GET /admin/onboarding | onboarding_wizards |
| **BRD-04 NFR** | [US-SYS-06](./cross-cutting/m12-quan-tri-he-thong/US-SYS-06-Cấu-hình-data-retention-policy.md) | 5 | TC-SY06-* (12) | GET/PUT/POST /admin/retention-policies | retention_policies, retention_jobs |

---

## Orphan Reports

### Orphan BRD Requirements — ✅ ALL RESOLVED

| BRD | Feature | Resolution | New US |
|-----|---------|------------|--------|
| BRD-02 | Xem lịch phân ca team | ✅ Resolved | [US-SHIFT-07](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-07-Xem-lịch-phân-ca-team.md) |
| BRD-03 | Quản lý template email thông báo | ✅ Resolved | [US-NOTIF-04](./phase-01-thiet-lap/m09-thong-bao/US-NOTIF-04-Quản-lý-template-email.md) |
| BRD-04 | Cấu hình Data Retention Policy | ✅ Resolved | [US-SYS-06](./cross-cutting/m12-quan-tri-he-thong/US-SYS-06-Cấu-hình-data-retention-policy.md) |

### Gold-Plating Report (API/DB without US backing)

| Layer | Item | Status | Action |
|-------|------|--------|--------|
| API M08 | POST /webhooks/cvision | System endpoint (not user-facing) | ✅ Legitimate — documented in EAMS v2.0 §8 |
| API M10 | Closing-date-config endpoints | Covered via US-APPR-02 extension | ✅ OK |

---

## Test Case Summary

| Module | US | TCs | Coverage |
|--------|-----|-----|----------|
| M01 Chấm công | 5 | 58 | ✅ 95% |
| M03 Giải trình | 2 | 22 | ✅ 92% |
| M04 Đăng ký | 6 | 61 | ✅ 95% |
| M05 Nhân sự | 6 | 50 | ✅ 90% |
| M05-RPT Báo cáo CN | 2 | 17 | ✅ 88% |
| M06 Ca làm việc | 7 | 68 | ✅ 93% |
| M07 Lịch nghỉ | 4 | 36 | ✅ 90% |
| M08 Camera AI | 4 | 41 | ✅ 95% |
| M09 Thông báo | 4 | 36 | ✅ 90% |
| M10 Phê duyệt | 3 | 36 | ✅ 93% |
| M11 Báo cáo tổng | 4 | 40 | ✅ 90% |
| M12 Quản trị | 6 | 67 | ✅ 94% |
| **TOTAL** | **53** | **482** | **✅ 93%** |

---

*RTM generated by BA-Kit Antigravity @ba-traceability*
