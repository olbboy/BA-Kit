# Test Suite — M09: Cấu hình Thông báo

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen

---

## Coverage Summary

| US | Happy | Edge | Error | Security | Concurrency | Data | Perf | Total |
|----|-------|------|-------|----------|-------------|------|------|-------|
| US-NOTIF-01 Kênh thông báo | 2 | 2 | 2 | 1 | 0 | 1 | 1 | **9** |
| US-NOTIF-02 Sự kiện kích hoạt | 2 | 3 | 2 | 1 | 0 | 1 | 0 | **9** |
| US-NOTIF-03 Policy | 2 | 2 | 2 | 1 | 0 | 0 | 1 | **8** |
| US-NOTIF-04 Email template | 2 | 3 | 2 | 2 | 0 | 1 | 0 | **10** |
| **Total** | **8** | **10** | **8** | **5** | **0** | **3** | **2** | **36** |

---

| TC-ID | US | Category | Steps | Expected Result | Priority |
|-------|-----|----------|-------|-----------------|----------|
| TC-N01-HP-01 | NOTIF-01 | Happy | Admin cấu hình Push + Email channels | Channels saved. Push=Primary, Email=Fallback. | P1 |
| TC-N01-HP-02 | NOTIF-01 | Happy | Push fail → fallback Email | Push delivery fail → auto-send Email. Dead letter if both fail. | P1 |
| TC-N01-EC-01 | NOTIF-01 | Edge | Thông báo bắt buộc (phê duyệt) | NV không thể tắt. Luôn nhận push. | P1 |
| TC-N01-EC-02 | NOTIF-01 | Edge | NV ca đêm (22:00-06:00) | Night shift exempt từ schedule restriction. Nhận push bất kỳ giờ nào. | P2 |
| TC-N01-ER-01 | NOTIF-01 | Error | Firebase token expired | Auto-refresh token. Nếu fail → fallback Email. | P2 |
| TC-N01-ER-02 | NOTIF-01 | Error | Email SMTP down | Queue retry 3 lần, 5 phút interval. Dead letter queue + Admin alert. | P2 |
| TC-N01-SEC-01 | NOTIF-01 | Security | NV sửa notification config | 403: Chỉ Admin. NV chỉ toggle non-mandatory. | P1 |
| TC-N01-DI-01 | NOTIF-01 | Data | Notification delivery log | notification_logs table: channel, status, retryCount, timestamp. | P2 |
| TC-N01-PERF-01 | NOTIF-01 | Perf | Push 5000 NV cùng lúc | Batch send ≤ 60 giây. No dropped messages. | P2 |
| TC-N02-HP-01 | NOTIF-02 | Happy | Admin bật event "Đơn được duyệt" | Event registered. NV nhận push khi đơn approved. | P1 |
| TC-N02-HP-02 | NOTIF-02 | Happy | 36 event types đăng ký | All 36 events configurable. Default ON/OFF per event. | P1 |
| TC-N02-EC-01 | NOTIF-02 | Edge | Batching: 5 check-in events trong 15 phút | Gộp → 1 thông báo tổng hợp: "5 nhân viên vừa check-in." | P2 |
| TC-N02-EC-02 | NOTIF-02 | Edge | Throttle: >20 push/giờ/NV | Throttle. Queue excess. Deliver in next hour window. | P2 |
| TC-N02-EC-03 | NOTIF-02 | Edge | Schedule: event lúc 23:00 (ngoải giờ 07-22) | Queue until 07:00 sáng hôm sau. Trừ khẩn cấp. | P2 |
| TC-N02-ER-01 | NOTIF-02 | Error | Event handler crash | Retry queue. DLQ after 3 fails. No data loss. | P2 |
| TC-N02-ER-02 | NOTIF-02 | Error | Event type unknown | Log error. Skip. No crash. | P3 |
| TC-N02-SEC-01 | NOTIF-02 | Security | NV chỉnh event mandatory | 403: Mandatory events always ON. | P1 |
| TC-N02-DI-01 | NOTIF-02 | Data | Event → notification_events table | event_type, triggered_at, target_user_ids. | P2 |
| TC-N03-HP-01 | NOTIF-03 | Happy | Admin cấu hình batching=15min, throttle=20/hr | Policy saved per-site. | P1 |
| TC-N03-HP-02 | NOTIF-03 | Happy | Admin cấu hình schedule=07:00-22:00 | Non-urgent ngoài giờ → queued. | P1 |
| TC-N03-EC-01 | NOTIF-03 | Edge | Policy khác nhau per-site | Site A: throttle=20. Site B: throttle=30. Correct per NV's site. | P2 |
| TC-N03-EC-02 | NOTIF-03 | Edge | Policy change mid-batch | New policy áp dụng cho batch tiếp theo, không batch đang chạy. | P2 |
| TC-N03-ER-01 | NOTIF-03 | Error | Batching window = 0 (instant) | No batching. Each event = 1 notification. High load warning. | P2 |
| TC-N03-ER-02 | NOTIF-03 | Error | Schedule start > end (07:00-06:00) | 400: "Giờ bắt đầu phải trước giờ kết thúc." | P3 |
| TC-N03-SEC-01 | NOTIF-03 | Security | Manager sửa notification policy | 403: Chỉ Admin/SYS_ADMIN. | P1 |
| TC-N03-PERF-01 | NOTIF-03 | Perf | Batching 1000 events trong 15 phút | Gộp thành ≤ 50 notifications. Processing ≤ 5 giây. | P2 |
| TC-N04-HP-01 | NOTIF-04 | Happy | HR sửa template "Đơn được duyệt" via WYSIWYG | Save OK. Version mới active. Version cũ archived. Logo + branding áp dụng. | P1 |
| TC-N04-HP-02 | NOTIF-04 | Happy | HR preview → test send → nhận email | Email đúng format. Biến `{{employee_name}}` replaced. Desktop+Mobile layout OK. | P1 |
| TC-N04-EC-01 | NOTIF-04 | Edge | Template body > 100KB (nhiều hình) | Cảnh báo: "Template quá lớn. Gmail có thể cắt bớt nội dung." | P2 |
| TC-N04-EC-02 | NOTIF-04 | Edge | Rollback về version cũ | Chọn version 3/10 → Active lại. Version hiện tại → archived. | P2 |
| TC-N04-EC-03 | NOTIF-04 | Edge | Logo URL broken (CDN expire) | Fallback text: `{{company_name}}`. Email vẫn gửi. Cảnh báo admin. | P2 |
| TC-N04-ER-01 | NOTIF-04 | Error | Biến `{{salary}}` không hợp lệ | Validation: "Biến `{{salary}}` không được hỗ trợ." Chặn save. | P2 |
| TC-N04-ER-02 | NOTIF-04 | Error | Test send > 5 lần/ngày | 429: "Đã vượt giới hạn test send (5/ngày). Thử lại ngày mai." | P3 |
| TC-N04-SEC-01 | NOTIF-04 | Security | HTML injection `<script>` | Sanitize: strip `<script>`, `<iframe>`, `onclick`. Chỉ safe HTML tags. | P1 |
| TC-N04-SEC-02 | NOTIF-04 | Security | NV truy cập template editor | 403: Chỉ HR_ADMIN. | P1 |
| TC-N04-DI-01 | NOTIF-04 | Data | Template version history ≤ 10 | Max 10 versions. Version 11 → purge oldest. Audit log. | P2 |
