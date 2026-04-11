# Test Suite — M12: Quản trị hệ thống

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen

---

## Coverage Summary

| US | Happy | Edge | Error | Security | Concurrency | Data | Perf | Total |
|----|-------|------|-------|----------|-------------|------|------|-------|
| US-SYS-01 Quản lý chi nhánh | 2 | 2 | 2 | 2 | 0 | 1 | 0 | **9** |
| US-SYS-02 Audit log viewer | 2 | 3 | 2 | 1 | 0 | 1 | 1 | **10** |
| US-SYS-03 Employee offboarding | 2 | 3 | 3 | 2 | 1 | 1 | 1 | **13** |
| US-SYS-04 Chốt công tháng | 2 | 4 | 3 | 2 | 1 | 1 | 0 | **13** |
| US-SYS-05 Employee onboarding | 2 | 3 | 2 | 1 | 1 | 1 | 0 | **10** |
| US-SYS-06 Data retention policy | 2 | 3 | 3 | 2 | 1 | 1 | 0 | **12** |
| **Total** | **12** | **18** | **15** | **10** | **4** | **6** | **2** | **67** |

---

## US-SYS-01: Quản lý chi nhánh

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-SY01-HP-01 | Happy | Admin tạo site mới | POST /admin/sites → 201. Name, code, timezone, closingDay. | P1 |
| TC-SY01-HP-02 | Happy | Admin deactivate site | DELETE /admin/sites/{id} → Soft delete. Status=INACTIVE. | P1 |
| TC-SY01-EC-01 | Edge | Xóa site có NV active | 409: "Site có [N] NV active. Chuyển NV trước." | P1 |
| TC-SY01-EC-02 | Edge | Code duplicate | 400: DUPLICATE_SITE_CODE. | P1 |
| TC-SY01-ER-01 | Error | Sửa code sau khi có data | 400: IMMUTABLE_FIELD. "Không sửa mã sau khi có dữ liệu." | P2 |
| TC-SY01-ER-02 | Error | Timezone invalid | 400: "Timezone không hợp lệ." | P3 |
| TC-SY01-SEC-01 | Security | HR tạo site | 403: Chỉ SYS_ADMIN/SUPER_ADMIN. | P1 |
| TC-SY01-SEC-02 | Security | SITE_HR deactivate site | 403: Cross-role chặn. | P1 |
| TC-SY01-DI-01 | Data | Create site → sites table | Verify all fields persisted. audit_log entry created. | P2 |

## US-SYS-02: Audit log viewer

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-SY02-HP-01 | Happy | Admin xem audit log | GET /admin/audit-logs + filters → Paginated list. | P1 |
| TC-SY02-HP-02 | Happy | Export CSV | POST /admin/audit-logs/export → File download. | P1 |
| TC-SY02-EC-01 | Edge | >1M records | Server-side pagination 100/trang. Indexed search. | P2 |
| TC-SY02-EC-02 | Edge | Filter time range >90 ngày | Chặn: "Giới hạn 90 ngày/lần. Chọn khoảng nhỏ hơn." | P2 |
| TC-SY02-EC-03 | Edge | Audit log immutable | No UPDATE/DELETE endpoint. Append-only. | P1 |
| TC-SY02-ER-01 | Error | Export quá lớn (10GB) | Queue job. Download link + email. Timeout 10 phút. | P3 |
| TC-SY02-ER-02 | Error | Filter không có kết quả | "Không tìm thấy log phù hợp." Empty state. | P3 |
| TC-SY02-SEC-01 | Security | Manager xem audit log | 403: Chỉ GLOBAL_HR/SYS_ADMIN. | P1 |
| TC-SY02-DI-01 | Data | Log retention 3 năm | Verify: logs >3 năm auto-archived/deleted theo policy. | P2 |
| TC-SY02-PERF-01 | Perf | Query 1M logs with filters | ≤ 3 giây (indexed). | P2 |

## US-SYS-03: Employee offboarding

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-SY03-HP-01 | Happy | HR trigger offboarding | POST /admin/offboarding → 202. Workflow initiated (7 steps). | P1 |
| TC-SY03-HP-02 | Happy | Workflow hoàn tất | All 7 steps OK: deactivate biometric, close requests, transfer approvals. | P1 |
| TC-SY03-EC-01 | Edge | NV có đơn APPROVED tương lai | Auto-cancel leave. Hoàn phép balance. Push NV. | P1 |
| TC-SY03-EC-02 | Edge | NV là approver cho NV khác | Auto-reassign approvals qua fallback chain. | P1 |
| TC-SY03-EC-03 | Edge | NV có OT chưa duyệt | Cancel OT requests. Push: "Đơn OT đã hủy do nghỉ việc." | P2 |
| TC-SY03-ER-01 | Error | Step 3/7 fails (C-Vision API down) | Retry step. Mark partial. Alert admin. Resume when fix. | P1 |
| TC-SY03-ER-02 | Error | Offboarding NV đã offboarded | 422: OFFBOARDING_IN_PROGRESS. Hoặc "NV đã được offboard." | P2 |
| TC-SY03-ER-03 | Error | Rollback offboarding (undo) | Không hỗ trợ auto-rollback. Manual reactivate bởi SYS_ADMIN. Audit log. | P2 |
| TC-SY03-SEC-01 | Security | Manager trigger offboarding | 403: Chỉ HR_ADMIN/SYS_ADMIN. | P1 |
| TC-SY03-SEC-02 | Security | Offboarding SUPER_ADMIN | Chặn: "Không thể offboard Super Admin." | P1 |
| TC-SY03-CON-01 | Concurrency | 2 HR trigger offboarding cùng NV | 422: OFFBOARDING_IN_PROGRESS. | P2 |
| TC-SY03-DI-01 | Data | Post-offboarding state | employee.status=INACTIVE. All mappings deactivated. Balance frozen. | P1 |
| TC-SY03-PERF-01 | Perf | Offboarding SLA | Toàn bộ workflow ≤ 5 phút. | P1 |

## US-SYS-04: Chốt công tháng

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-SY04-HP-01 | Happy | Cấu hình closingDay=25 | PUT config → saved per-site. | P1 |
| TC-SY04-HP-02 | Happy | Auto-close trigger | Cron 00:00 ngày 25 → OPEN→GRACE→LOCKED. | P1 |
| TC-SY04-EC-01 | Edge | Closing day = Chủ nhật | weekendRule=PREV_WORKDAY → chốt Thứ 6. Display adjusted. | P1 |
| TC-SY04-EC-02 | Edge | NV submit 23:59, chốt 00:00 | Accept if timestamp < closing. Transaction isolation. | P1 |
| TC-SY04-EC-03 | Edge | Cron job failed | Retry mechanism. Monitor mỗi giờ. Auto-trigger. Admin alert. | P1 |
| TC-SY04-EC-04 | Edge | 200 NV có lỗi tồn đọng trước lock | Cảnh báo đỏ. HR confirm hoặc extend grace +1-3 ngày (max 1 lần). | P2 |
| TC-SY04-ER-01 | Error | closingDay = 30 | 400: "closingDay phải 1-28." | P2 |
| TC-SY04-ER-02 | Error | Exception unlock > 30 ngày sau chốt | Chặn: "Hết hạn exception unlock." | P2 |
| TC-SY04-ER-03 | Error | graceDays = -1 | 400: "graceDays phải 0-7." | P3 |
| TC-SY04-SEC-01 | Security | Manager cấu hình chốt | 403: Chỉ SYS_ADMIN. | P1 |
| TC-SY04-SEC-02 | Security | Exception unlock audit trail | Verify immutable log: actor, employee, date, reason, timestamp. | P1 |
| TC-SY04-CON-01 | Concurrency | 2 admin trigger lock cùng kỳ | Idempotent. Lần 2: "Kỳ đã chốt." | P2 |
| TC-SY04-DI-01 | Data | LOCKED → no changes | INSERT/UPDATE attendance cho tháng locked → 423. | P1 |

## US-SYS-05: Employee onboarding wizard

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-SY05-HP-01 | Happy | HR onboard NV mới 7 bước | 1.Profile→2.Site→3.Shift→4.FaceID→5.Leave→6.Approval→7.Welcome. | P1 |
| TC-SY05-HP-02 | Happy | Bulk onboarding 10 NV | POST /admin/onboarding/batch → 10 parallels. Progress. | P1 |
| TC-SY05-EC-01 | Edge | Skip optional step (FaceID) | Mark step "Skipped". NV nhắc "Đăng ký Face ID sau." | P2 |
| TC-SY05-EC-02 | Edge | NV thuộc 2 sites | Step 2: assign primary + secondary site. | P2 |
| TC-SY05-EC-03 | Edge | Resume wizard (HR đóng giữa chừng) | Save progress. Resume from last step. | P2 |
| TC-SY05-ER-01 | Error | Email NV trùng | 409: "Email đã tồn tại." | P1 |
| TC-SY05-ER-02 | Error | Shift không có tại site selected | Cảnh báo: "Ca [X] không thuộc site [Y]." | P2 |
| TC-SY05-SEC-01 | Security | Manager chạy onboarding | 403: Chỉ HR_ADMIN/SYS_ADMIN. | P1 |
| TC-SY05-CON-01 | Concurrency | 2 HR onboard cùng NV (email) | Unique constraint. Người thứ 2: 409. | P2 |
| TC-SY05-DI-01 | Data | Post-onboarding state | employee created + shift assigned + balance initialized + mapping ready. | P1 |

## US-SYS-06: Cấu hình Data Retention Policy

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-SY06-HP-01 | Happy | Admin cấu hình retention Face ID = 90 ngày | Policy saved. Cron job enforce nightly. | P1 |
| TC-SY06-HP-02 | Happy | Cron job chạy → archive attendance > 5 năm | X records archived to cold storage. Report email sent. | P1 |
| TC-SY06-EC-01 | Edge | Purge > 10,000 records/ngày | Dừng auto-purge. Alert SYS_ADMIN. Confirm thủ công. | P1 |
| TC-SY06-EC-02 | Edge | Soft-delete → hard-delete sau 7 ngày | Safety window: 7 ngày rollback trước khi hard-delete. | P1 |
| TC-SY06-EC-03 | Edge | Data subject erasure request (NĐ 13/2023) | Per-employee purge: Face ID + attendance + logs. Giữ aggregated anonymous. | P1 |
| TC-SY06-ER-01 | Error | Retention = 0 ngày | Chặn: "Retention tối thiểu 1 ngày." | P2 |
| TC-SY06-ER-02 | Error | Cron job fail mid-batch | Resume mechanism. Partial progress saved. Alert admin. | P2 |
| TC-SY06-ER-03 | Error | Archive khi cold storage full | Alert: "Cold storage gần đầy (90%). Mở rộng dung lượng." Pause archive. | P2 |
| TC-SY06-SEC-01 | Security | HR cấu hình retention | 403: Chỉ SYS_ADMIN/SUPER_ADMIN. | P1 |
| TC-SY06-SEC-02 | Security | Purge thủ công cần confirm 2 lần | Double confirm + reason bắt buộc. Audit log immutable. | P1 |
| TC-SY06-CON-01 | Concurrency | 2 admin trigger purge cùng lúc | Lock: "Batch đang chạy. Vui lòng đợi." | P2 |
| TC-SY06-DI-01 | Data | Compliance dashboard accurate | ☑️ Face ID < 90 days post-offboard. ☑️ Attendance ≥ 5 years. ☑️ Payroll ≥ 10 years. | P1 |
