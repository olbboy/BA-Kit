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

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-SY01-HP-01 | Happy | HR Admin đã đăng nhập, có quyền quản trị | Admin tạo site mới | — | POST /admin/sites → 201. Name, code, timezone, closingDay. | P1 |
| TC-SY01-HP-02 | Happy | HR Admin đã đăng nhập, có quyền quản trị | Admin deactivate site | — | DELETE /admin/sites/{id} → Soft delete. Status=INACTIVE. | P1 |
| TC-SY01-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Xóa site có NV active | 409 | 409: "Site có [N] NV active. Chuyển NV trước." | P1 |
| TC-SY01-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Code duplicate | 400 | 400: DUPLICATE_SITE_CODE. | P1 |
| TC-SY01-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Sửa code sau khi có data | 400 | 400: IMMUTABLE_FIELD. "Không sửa mã sau khi có dữ liệu." | P2 |
| TC-SY01-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Timezone invalid | 400 | 400: "Timezone không hợp lệ." | P3 |
| TC-SY01-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | HR tạo site | 403 | 403: Chỉ SYS_ADMIN/SUPER_ADMIN. | P1 |
| TC-SY01-SEC-02 | Security | Hệ thống ở trạng thái biên / đặc biệt | SITE_HR deactivate site | 403 | 403: Cross-role chặn. | P1 |
| TC-SY01-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Create site → sites table | — | Verify all fields persisted. audit_log entry created. | P2 |

## US-SYS-02: Audit log viewer

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-SY02-HP-01 | Happy | HR Admin đã đăng nhập, có quyền quản trị | Admin xem audit log | — | GET /admin/audit-logs + filters → Paginated list. | P1 |
| TC-SY02-HP-02 | Happy | User đã đăng nhập thành công | Export CSV | — | POST /admin/audit-logs/export → File download. | P1 |
| TC-SY02-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | >1M records | — | Server-side pagination 100/trang. Indexed search. | P2 |
| TC-SY02-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Filter time range >90 ngày | 90, 90 | Chặn: "Giới hạn 90 ngày/lần. Chọn khoảng nhỏ hơn." | P2 |
| TC-SY02-EC-03 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Audit log immutable | — | No UPDATE/DELETE endpoint. Append-only. | P1 |
| TC-SY02-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Export quá lớn (10GB) | 10 | Queue job. Download link + email. Timeout 10 phút. | P3 |
| TC-SY02-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Filter không có kết quả | — | "Không tìm thấy log phù hợp." Empty state. | P3 |
| TC-SY02-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | Manager xem audit log | 403 | 403: Chỉ GLOBAL_HR/SYS_ADMIN. | P1 |
| TC-SY02-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Log retention 3 năm | — | Verify: logs >3 năm auto-archived/deleted theo policy. | P2 |
| TC-SY02-PERF-01 | Perf | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Query 1M logs with filters | 3, ≤ 3 | ≤ 3 giây (indexed). | P2 |

## US-SYS-03: Employee offboarding

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-SY03-HP-01 | Happy | HR Admin đã đăng nhập, có quyền quản trị | HR trigger offboarding | — | POST /admin/offboarding → 202. Workflow initiated (7 steps). | P1 |
| TC-SY03-HP-02 | Happy | User đã đăng nhập thành công | Workflow hoàn tất | — | All 7 steps OK: deactivate biometric, close requests, transfer approvals. | P1 |
| TC-SY03-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | NV có đơn APPROVED tương lai | — | Auto-cancel leave. Hoàn phép balance. Push NV. | P1 |
| TC-SY03-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | NV là approver cho NV khác | — | Auto-reassign approvals qua fallback chain. | P1 |
| TC-SY03-EC-03 | Edge | Hệ thống ở trạng thái biên / đặc biệt | NV có OT chưa duyệt | — | Cancel OT requests. Push: "Đơn OT đã hủy do nghỉ việc." | P2 |
| TC-SY03-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Step 3/7 fails (C-Vision API down) | API request body/params | Retry step. Mark partial. Alert admin. Resume when fix. | P1 |
| TC-SY03-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Offboarding NV đã offboarded | 422 | 422: OFFBOARDING_IN_PROGRESS. Hoặc "NV đã được offboard." | P2 |
| TC-SY03-ER-03 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Rollback offboarding (undo) | — | Không hỗ trợ auto-rollback. Manual reactivate bởi SYS_ADMIN. Audit log. | P2 |
| TC-SY03-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | Manager trigger offboarding | 403 | 403: Chỉ HR_ADMIN/SYS_ADMIN. | P1 |
| TC-SY03-SEC-02 | Security | Hệ thống ở trạng thái biên / đặc biệt | Offboarding SUPER_ADMIN | — | Chặn: "Không thể offboard Super Admin." | P1 |
| TC-SY03-CON-01 | Concurrency | 2+ users thao tác đồng thời trên cùng resource | 2 HR trigger offboarding cùng NV | 422 | 422: OFFBOARDING_IN_PROGRESS. | P2 |
| TC-SY03-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Post-offboarding state | API request body/params | employee.status=INACTIVE. All mappings deactivated. Balance frozen. | P1 |
| TC-SY03-PERF-01 | Perf | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Offboarding SLA | 5, ≤ 5 | Toàn bộ workflow ≤ 5 phút. | P1 |

## US-SYS-04: Chốt công tháng

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-SY04-HP-01 | Happy | User đã đăng nhập thành công | Cấu hình closingDay=25 | — | PUT config → saved per-site. | P1 |
| TC-SY04-HP-02 | Happy | User đã đăng nhập thành công | Auto-close trigger | 00, 00:00 | Cron 00:00 ngày 25 → OPEN→GRACE→LOCKED. | P1 |
| TC-SY04-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Closing day = Chủ nhật | — | weekendRule=PREV_WORKDAY → chốt Thứ 6. Display adjusted. | P1 |
| TC-SY04-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | NV submit 23:59, chốt 00:00 | 23:59, 00:00 | Accept if timestamp < closing. Transaction isolation. | P1 |
| TC-SY04-EC-03 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Cron job failed | — | Retry mechanism. Monitor mỗi giờ. Auto-trigger. Admin alert. | P1 |
| TC-SY04-EC-04 | Edge | Hệ thống ở trạng thái biên / đặc biệt | 200 NV có lỗi tồn đọng trước lock | 3, 1 | Cảnh báo đỏ. HR confirm hoặc extend grace +1-3 ngày (max 1 lần). | P2 |
| TC-SY04-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | closingDay = 30 | 400 | 400: "closingDay phải 1-28." | P2 |
| TC-SY04-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Exception unlock > 30 ngày sau chốt | 30 | Chặn: "Hết hạn exception unlock." | P2 |
| TC-SY04-ER-03 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | graceDays = -1 | 400 | 400: "graceDays phải 0-7." | P3 |
| TC-SY04-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | Manager cấu hình chốt | 403 | 403: Chỉ SYS_ADMIN. | P1 |
| TC-SY04-SEC-02 | Security | Hệ thống ở trạng thái biên / đặc biệt | Exception unlock audit trail | — | Verify immutable log: actor, employee, date, reason, timestamp. | P1 |
| TC-SY04-CON-01 | Concurrency | 2+ users thao tác đồng thời trên cùng resource | 2 admin trigger lock cùng kỳ | — | Idempotent. Lần 2: "Kỳ đã chốt." | P2 |
| TC-SY04-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | LOCKED → no changes | 423 | INSERT/UPDATE attendance cho tháng locked → 423. | P1 |

## US-SYS-05: Employee onboarding wizard

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-SY05-HP-01 | Happy | NV đã đăng nhập, có ca làm việc active | HR onboard NV mới 7 bước | — | 1.Profile→2.Site→3.Shift→4.FaceID→5.Leave→6.Approval→7.Welcome. | P1 |
| TC-SY05-HP-02 | Happy | NV đã đăng nhập, có ca làm việc active | Bulk onboarding 10 NV | CSV/Excel file | POST /admin/onboarding/batch → 10 parallels. Progress. | P1 |
| TC-SY05-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Skip optional step (FaceID) | — | Mark step "Skipped". NV nhắc "Đăng ký Face ID sau." | P2 |
| TC-SY05-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | NV thuộc 2 sites | — | Step 2: assign primary + secondary site. | P2 |
| TC-SY05-EC-03 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Resume wizard (HR đóng giữa chừng) | — | Save progress. Resume from last step. | P2 |
| TC-SY05-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Email NV trùng | 409 | 409: "Email đã tồn tại." | P1 |
| TC-SY05-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Shift không có tại site selected | — | Cảnh báo: "Ca [X] không thuộc site [Y]." | P2 |
| TC-SY05-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | Manager chạy onboarding | 403 | 403: Chỉ HR_ADMIN/SYS_ADMIN. | P1 |
| TC-SY05-CON-01 | Concurrency | 2+ users thao tác đồng thời trên cùng resource | 2 HR onboard cùng NV (email) | 409 | Unique constraint. Người thứ 2: 409. | P2 |
| TC-SY05-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Post-onboarding state | API request body/params | employee created + shift assigned + balance initialized + mapping ready. | P1 |

## US-SYS-06: Cấu hình Data Retention Policy

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-SY06-HP-01 | Happy | HR Admin đã đăng nhập, có quyền quản trị | Admin cấu hình retention Face ID = 90 ngày | 90 | Policy saved. Cron job enforce nightly. | P1 |
| TC-SY06-HP-02 | Happy | User đã đăng nhập thành công | Cron job chạy → archive attendance > 5 năm | — | X records archived to cold storage. Report email sent. | P1 |
| TC-SY06-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Purge > 10,000 records/ngày | — | Dừng auto-purge. Alert SYS_ADMIN. Confirm thủ công. | P1 |
| TC-SY06-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Soft-delete → hard-delete sau 7 ngày | 7, 7 | Safety window: 7 ngày rollback trước khi hard-delete. | P1 |
| TC-SY06-EC-03 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Data subject erasure request (NĐ 13/2023) | — | Per-employee purge: Face ID + attendance + logs. Giữ aggregated anonymous. | P1 |
| TC-SY06-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Retention = 0 ngày | 0, 1 | Chặn: "Retention tối thiểu 1 ngày." | P2 |
| TC-SY06-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Cron job fail mid-batch | — | Resume mechanism. Partial progress saved. Alert admin. | P2 |
| TC-SY06-ER-03 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Archive khi cold storage full | 90 | Alert: "Cold storage gần đầy (90%). Mở rộng dung lượng." Pause archive. | P2 |
| TC-SY06-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | HR cấu hình retention | 403 | 403: Chỉ SYS_ADMIN/SUPER_ADMIN. | P1 |
| TC-SY06-SEC-02 | Security | Hệ thống ở trạng thái biên / đặc biệt | Purge thủ công cần confirm 2 lần | 2 | Double confirm + reason bắt buộc. Audit log immutable. | P1 |
| TC-SY06-CON-01 | Concurrency | 2+ users thao tác đồng thời trên cùng resource | 2 admin trigger purge cùng lúc | — | Lock: "Batch đang chạy. Vui lòng đợi." | P2 |
| TC-SY06-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Compliance dashboard accurate | — | ☑️ Face ID < 90 days post-offboard. ☑️ Attendance ≥ 5 years. ☑️ Payroll ≥ 10 years. | P1 |

---

## Boundary Value Analysis (BVA)


### Data retention period (`retentionDays`)

| TC-BVA | Value | Type | Expected |
|--------|-------|------|----------|
| BVA-RETENT-01 | 30 ngày | MIN | ✅ Accept (minimum) |
| BVA-RETENT-02 | 29 ngày | BELOW_MIN | ❌ Reject: dưới giới hạn |
| BVA-RETENT-03 | 364 ngày | JUST_BELOW | ✅/⚠️ Accept nhưng gần ngưỡng |
| BVA-RETENT-04 | 365 ngày | BOUNDARY | ✅ Accept (ngưỡng chính xác) |
| BVA-RETENT-05 | 366 ngày | JUST_ABOVE | ✅ Accept (vượt ngưỡng 1 đơn vị) |
| BVA-RETENT-06 | 3650 ngày | MAX | ✅ Accept (maximum) |
| BVA-RETENT-07 | 3651 ngày | ABOVE_MAX | ❌ Reject: vượt giới hạn |

### Lọc audit log theo ngày (`auditLogDays`)

| TC-BVA | Value | Type | Expected |
|--------|-------|------|----------|
| BVA-AUDITL-01 | 1 ngày | MIN | ✅ Accept (minimum) |
| BVA-AUDITL-02 | 0 ngày | BELOW_MIN | ❌ Reject: dưới giới hạn |
| BVA-AUDITL-03 | 29 ngày | JUST_BELOW | ✅/⚠️ Accept nhưng gần ngưỡng |
| BVA-AUDITL-04 | 30 ngày | BOUNDARY | ✅ Accept (ngưỡng chính xác) |
| BVA-AUDITL-05 | 31 ngày | JUST_ABOVE | ✅ Accept (vượt ngưỡng 1 đơn vị) |
| BVA-AUDITL-06 | 90 ngày | MAX | ✅ Accept (maximum) |
| BVA-AUDITL-07 | 91 ngày | ABOVE_MAX | ❌ Reject: vượt giới hạn |

### Số bước onboarding wizard (`onboardingSteps`)

| TC-BVA | Value | Type | Expected |
|--------|-------|------|----------|
| BVA-ONBOAR-01 | 1 bước | MIN | ✅ Accept (minimum) |
| BVA-ONBOAR-02 | 0 bước | BELOW_MIN | ❌ Reject: dưới giới hạn |
| BVA-ONBOAR-03 | 6 bước | JUST_BELOW | ✅/⚠️ Accept nhưng gần ngưỡng |
| BVA-ONBOAR-04 | 7 bước | BOUNDARY | ✅ Accept (ngưỡng chính xác) |
| BVA-ONBOAR-05 | 8 bước | JUST_ABOVE | ✅ Accept (vượt ngưỡng 1 đơn vị) |
| BVA-ONBOAR-06 | 7 bước | MAX | ✅ Accept (maximum) |
| BVA-ONBOAR-07 | 8 bước | ABOVE_MAX | ❌ Reject: vượt giới hạn |
