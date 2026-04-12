# Test Suite — M10: Trung tâm Phê duyệt

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen

---

## Coverage Summary

| US | Happy | Edge | Error | Security | Concurrency | Data | Perf | Total |
|----|-------|------|-------|----------|-------------|------|------|-------|
| US-APPR-01 Inbox | 3 | 4 | 3 | 2 | 1 | 1 | 1 | **15** |
| US-APPR-02 Chuỗi phê duyệt | 2 | 3 | 2 | 1 | 0 | 1 | 0 | **9** |
| US-APPR-03 Phê duyệt hàng loạt | 2 | 3 | 3 | 1 | 1 | 1 | 1 | **12** |
| **Total** | **7** | **10** | **8** | **4** | **2** | **3** | **2** | **36** |

---

## US-APPR-01: Inbox phê duyệt

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-AP01-HP-01 | Happy | Manager đã đăng nhập, có team members | Manager mở Inbox | — | Danh sách đơn PENDING thuộc team hiển thị. Badge =[N]. | P1 |
| TC-AP01-HP-02 | Happy | Manager đã đăng nhập, có team members | Manager duyệt đơn nghỉ phép | — | 1-tap approve → confirm. Status → APPROVED (hoặc next level). NV nhận push. | P1 |
| TC-AP01-HP-03 | Happy | Manager đã đăng nhập, có team members | Manager từ chối đơn + lý do | — | Nhập lý do ≥10 ký tự → confirm. Status → REJECTED. NV nhận push + lý do. | P1 |
| TC-AP01-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Approver bị terminated | — | Auto-reassign qua fallback chain. Push NV: "Đơn chuyển đến [Approver mới]." | P1 |
| TC-AP01-EC-02 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Self-approve (Manager tự duyệt đơn mình) | — | Chặn. Auto-route lên DEPT_HEAD hoặc SITE_HR. | P1 |
| TC-AP01-EC-03 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Approver offline >7 ngày | 7 | Auto-escalate lên level tiếp. Alert HR. Không auto-approve. | P2 |
| TC-AP01-EC-04 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Đơn tạo sát ngày chốt công | — | Cảnh báo: "Đơn cần duyệt trước [DD/MM]." Push reminder 24h. | P2 |
| TC-AP01-ER-01 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Từ chối không nhập lý do | 400 | 400: REJECT_REASON_REQUIRED. "Tối thiểu 10 ký tự." | P1 |
| TC-AP01-ER-02 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Duyệt đơn đã xử lý (race condition) | 409 | 409: ALREADY_PROCESSED. "Đơn đã được xử lý bởi [Tên]." | P2 |
| TC-AP01-ER-03 | Error | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Duyệt khi kỳ đã chốt | 423 | 423: PERIOD_LOCKED. | P1 |
| TC-AP01-SEC-01 | Security | Hệ thống ở trạng thái biên / đặc biệt | Manager xem đơn team khác | 403 | 403: Forbidden. RBAC filter. | P1 |
| TC-AP01-SEC-02 | Security | Hệ thống ở trạng thái biên / đặc biệt | NV truy cập endpoint approve | 403 | 403: NOT_CURRENT_APPROVER. | P1 |
| TC-AP01-CON-01 | Concurrency | 2+ users thao tác đồng thời trên cùng resource | 2 approver cùng duyệt 1 đơn | — | Optimistic lock. Người thứ 2: "Đơn đã được xử lý." | P2 |
| TC-AP01-DI-01 | Data | Dữ liệu đã tồn tại trong DB, cần cross-verify | Approve leave → balance update | — | balance.used += days. balance.pending -= days. | P1 |
| TC-AP01-PERF-01 | Perf | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Load inbox 500 đơn | 2, 500, ≤ 2 | Tải ≤ 2 giây. Phân trang 20/trang. | P2 |

## US-APPR-02: Cấu hình chuỗi phê duyệt

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-AP02-HP-01 | Happy | HR Admin đã đăng nhập, có quyền quản trị | HR tạo chuỗi Leave: 2-level | — | POST approval-chain: Level 1=MANAGER, Level 2=SITE_HR. | P1 |
| TC-AP02-HP-02 | Happy | HR Admin đã đăng nhập, có quyền quản trị | HR sửa chuỗi thêm Level 3 | 5 | PUT: thêm Level 3=GLOBAL_HR khi >5 ngày. | P1 |
| TC-AP02-EC-01 | Edge | Hệ thống ở trạng thái biên / đặc biệt | Xóa chuỗi đang có đơn PENDING | — | Chặn: "Có [N] đơn đang sử dụng chuỗi này." | P2 |
| TC-AP02-EC-02 | Edge | Cấu hình chuỗi cho requestType chưa có | User đã đăng nhập | POST OT_REQUEST chain lần đầu | API request body/params | Thành công. Đơn OT mới sẽ dùng chuỗi. | P2 |
| TC-AP02-EC-03 | Edge | Condition phức tạp: >3 days AND department=Engineering | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | POST conditional chain | API request body/params | Chỉ áp dụng khi cả 2 điều kiện thỏa. | P2 |
| TC-AP02-ER-01 | Error | Tạo chuỗi không có level nào | User đã đăng nhập | POST levels=[] | 400 | 400: "Chuỗi cần ít nhất 1 level." | P2 |
| TC-AP02-ER-02 | Error | Level duplicate (2 lần MANAGER) | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | POST duplicate levels | 400 | 400: "Không được trùng approver type." | P3 |
| TC-AP02-SEC-01 | Security | Manager (không phải HR) sửa chuỗi | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | PUT role=MANAGER | 403 | 403: Forbidden. | P1 |
| TC-AP02-DI-01 | Data | Sửa chuỗi → đơn mới dùng chuỗi mới | User đã đăng nhập | Create leave after chain update | — | Đơn mới dùng chuỗi mới. Đơn cũ giữ chuỗi cũ. | P1 |

## US-APPR-03: Phê duyệt hàng loạt

| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |
|--------|----------|--------------|-------|-------|-----------------|----------|
| TC-AP03-HP-01 | Happy | HR chọn 5 đơn → Batch approve | User đã đăng nhập | POST /approvals/batch action=APPROVE | API request body/params | approved=5, failed=0. NV nhận push. | P1 |
| TC-AP03-HP-02 | Happy | HR batch reject 3 đơn + lý do | Hệ thống ở trạng thái biên / đặc biệt | POST batch action=REJECT + note | API request body/params | rejected=3. Lý do chung gửi cho tất cả NV. | P1 |
| TC-AP03-EC-01 | Edge | Batch 50 đơn (max limit) | User đã đăng nhập | POST 50 items | API request body/params | Xử lý tuần tự. Timeout đủ lớn. Kết quả per-item. | P2 |
| TC-AP03-EC-02 | Edge | Batch 51 đơn (>max) | User đã đăng nhập | POST 51 items | 400 | 400: "Tối đa 50 đơn/batch." | P2 |
| TC-AP03-EC-03 | Edge | 3/5 đơn thành công, 2 fail (đã xử lý) | User đã đăng nhập | Batch 5/mixed | — | approved=3, failed=2. Không rollback đơn thành công. | P1 |
| TC-AP03-ER-01 | Error | Batch reject không có lý do | Hệ thống ở trạng thái biên / đặc biệt | POST REJECT note="" | 400 | 400: REJECT_REASON_REQUIRED. Chặn toàn batch. | P1 |
| TC-AP03-ER-02 | Error | Batch chứa đơn khác requestType | User đã đăng nhập | POST mixed Leave+OT | API request body/params | Cho phép nếu approver có quyền cho cả 2 type. | P2 |
| TC-AP03-ER-03 | Error | Batch timeout (server quá tải) | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | POST khi load cao | API request body/params | 202: Accepted. Job ID trả về. Poll status endpoint. | P3 |
| TC-AP03-SEC-01 | Security | Batch approve đơn team khác | User đã đăng nhập | POST ids=other_team | API request body/params | Chỉ approve đơn thuộc quyền. Đơn ngoài quyền: failed=true. | P1 |
| TC-AP03-CON-01 | Concurrency | 2 HR cùng batch approve overlapping set | Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi | Concurrent batch | — | Đơn đã processed: skip (ALREADY_PROCESSED). Không duplicate approve. | P2 |
| TC-AP03-DI-01 | Data | Batch 5 leave approve → 5 balance updates | User đã đăng nhập | After batch | — | Mỗi NV balance update đúng. No partial state. | P1 |
| TC-AP03-PERF-01 | Perf | Batch 50 đơn | User đã đăng nhập | POST 50 items | 30, ≤ 30 | Xử lý ≤ 30 giây. Progress indicator trên UI. | P2 |

---

## Boundary Value Analysis (BVA)


### Số cấp phê duyệt (`approvalLevels`)

| TC-BVA | Value | Type | Expected |
|--------|-------|------|----------|
| BVA-APPROV-01 | 1 cấp | MIN | ✅ Accept (minimum) |
| BVA-APPROV-02 | 0 cấp | BELOW_MIN | ❌ Reject: dưới giới hạn |
| BVA-APPROV-03 | 1 cấp | JUST_BELOW | ✅/⚠️ Accept nhưng gần ngưỡng |
| BVA-APPROV-04 | 2 cấp | BOUNDARY | ✅ Accept (ngưỡng chính xác) |
| BVA-APPROV-05 | 3 cấp | JUST_ABOVE | ✅ Accept (vượt ngưỡng 1 đơn vị) |
| BVA-APPROV-06 | 5 cấp | MAX | ✅ Accept (maximum) |
| BVA-APPROV-07 | 6 cấp | ABOVE_MAX | ❌ Reject: vượt giới hạn |

### Số đơn duyệt hàng loạt (`bulkApproveLimit`)

| TC-BVA | Value | Type | Expected |
|--------|-------|------|----------|
| BVA-BULKAP-01 | 1 đơn | MIN | ✅ Accept (minimum) |
| BVA-BULKAP-02 | 0 đơn | BELOW_MIN | ❌ Reject: dưới giới hạn |
| BVA-BULKAP-03 | 19 đơn | JUST_BELOW | ✅/⚠️ Accept nhưng gần ngưỡng |
| BVA-BULKAP-04 | 20 đơn | BOUNDARY | ✅ Accept (ngưỡng chính xác) |
| BVA-BULKAP-05 | 21 đơn | JUST_ABOVE | ✅ Accept (vượt ngưỡng 1 đơn vị) |
| BVA-BULKAP-06 | 50 đơn | MAX | ✅ Accept (maximum) |
| BVA-BULKAP-07 | 51 đơn | ABOVE_MAX | ❌ Reject: vượt giới hạn |

---

## State Transition Testing — Approval Chain Lifecycle

**States:** `PENDING_L1` → `PENDING_L2` → `APPROVED` → `REJECTED` → `DELEGATED` → `ESCALATED`

| TC-STATE | From | To | Trigger | Validity | Expected |
|----------|------|----|---------|----------|----------|
| TC-STATE-01 | `PENDING_L1` | `PENDING_L2` | L1 approve (multi-level) | **Valid** | ✅ Transition OK |
| TC-STATE-02 | `PENDING_L1` | `APPROVED` | L1 approve (single-level) | **Valid** | ✅ Transition OK |
| TC-STATE-03 | `PENDING_L1` | `REJECTED` | L1 reject | **Valid** | ✅ Transition OK |
| TC-STATE-04 | `PENDING_L1` | `DELEGATED` | L1 delegate | **Valid** | ✅ Transition OK |
| TC-STATE-05 | `PENDING_L2` | `APPROVED` | L2 final approve | **Valid** | ✅ Transition OK |
| TC-STATE-06 | `PENDING_L2` | `REJECTED` | L2 reject | **Valid** | ✅ Transition OK |
| TC-STATE-07 | `APPROVED` | `PENDING_L1` | Re-open approved | **INVALID** | ❌ 400/403 — Transition không hợp lệ |
