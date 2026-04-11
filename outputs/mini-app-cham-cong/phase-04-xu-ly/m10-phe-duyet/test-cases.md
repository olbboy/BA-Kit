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

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-AP01-HP-01 | Happy | Manager mở Inbox | Danh sách đơn PENDING thuộc team hiển thị. Badge =[N]. | P1 |
| TC-AP01-HP-02 | Happy | Manager duyệt đơn nghỉ phép | 1-tap approve → confirm. Status → APPROVED (hoặc next level). NV nhận push. | P1 |
| TC-AP01-HP-03 | Happy | Manager từ chối đơn + lý do | Nhập lý do ≥10 ký tự → confirm. Status → REJECTED. NV nhận push + lý do. | P1 |
| TC-AP01-EC-01 | Edge | Approver bị terminated | Auto-reassign qua fallback chain. Push NV: "Đơn chuyển đến [Approver mới]." | P1 |
| TC-AP01-EC-02 | Edge | Self-approve (Manager tự duyệt đơn mình) | Chặn. Auto-route lên DEPT_HEAD hoặc SITE_HR. | P1 |
| TC-AP01-EC-03 | Edge | Approver offline >7 ngày | Auto-escalate lên level tiếp. Alert HR. Không auto-approve. | P2 |
| TC-AP01-EC-04 | Edge | Đơn tạo sát ngày chốt công | Cảnh báo: "Đơn cần duyệt trước [DD/MM]." Push reminder 24h. | P2 |
| TC-AP01-ER-01 | Error | Từ chối không nhập lý do | 400: REJECT_REASON_REQUIRED. "Tối thiểu 10 ký tự." | P1 |
| TC-AP01-ER-02 | Error | Duyệt đơn đã xử lý (race condition) | 409: ALREADY_PROCESSED. "Đơn đã được xử lý bởi [Tên]." | P2 |
| TC-AP01-ER-03 | Error | Duyệt khi kỳ đã chốt | 423: PERIOD_LOCKED. | P1 |
| TC-AP01-SEC-01 | Security | Manager xem đơn team khác | 403: Forbidden. RBAC filter. | P1 |
| TC-AP01-SEC-02 | Security | NV truy cập endpoint approve | 403: NOT_CURRENT_APPROVER. | P1 |
| TC-AP01-CON-01 | Concurrency | 2 approver cùng duyệt 1 đơn | Optimistic lock. Người thứ 2: "Đơn đã được xử lý." | P2 |
| TC-AP01-DI-01 | Data | Approve leave → balance update | balance.used += days. balance.pending -= days. | P1 |
| TC-AP01-PERF-01 | Perf | Load inbox 500 đơn | Tải ≤ 2 giây. Phân trang 20/trang. | P2 |

## US-APPR-02: Cấu hình chuỗi phê duyệt

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-AP02-HP-01 | Happy | HR tạo chuỗi Leave: 2-level | POST approval-chain: Level 1=MANAGER, Level 2=SITE_HR. | P1 |
| TC-AP02-HP-02 | Happy | HR sửa chuỗi thêm Level 3 | PUT: thêm Level 3=GLOBAL_HR khi >5 ngày. | P1 |
| TC-AP02-EC-01 | Edge | Xóa chuỗi đang có đơn PENDING | Chặn: "Có [N] đơn đang sử dụng chuỗi này." | P2 |
| TC-AP02-EC-02 | Edge | Cấu hình chuỗi cho requestType chưa có | POST OT_REQUEST chain lần đầu | Thành công. Đơn OT mới sẽ dùng chuỗi. | P2 |
| TC-AP02-EC-03 | Edge | Condition phức tạp: >3 days AND department=Engineering | POST conditional chain | Chỉ áp dụng khi cả 2 điều kiện thỏa. | P2 |
| TC-AP02-ER-01 | Error | Tạo chuỗi không có level nào | POST levels=[] | 400: "Chuỗi cần ít nhất 1 level." | P2 |
| TC-AP02-ER-02 | Error | Level duplicate (2 lần MANAGER) | POST duplicate levels | 400: "Không được trùng approver type." | P3 |
| TC-AP02-SEC-01 | Security | Manager (không phải HR) sửa chuỗi | PUT role=MANAGER | 403: Forbidden. | P1 |
| TC-AP02-DI-01 | Data | Sửa chuỗi → đơn mới dùng chuỗi mới | Create leave after chain update | Đơn mới dùng chuỗi mới. Đơn cũ giữ chuỗi cũ. | P1 |

## US-APPR-03: Phê duyệt hàng loạt

| TC-ID | Category | Steps | Expected Result | Priority |
|-------|----------|-------|-----------------|----------|
| TC-AP03-HP-01 | Happy | HR chọn 5 đơn → Batch approve | POST /approvals/batch action=APPROVE | approved=5, failed=0. NV nhận push. | P1 |
| TC-AP03-HP-02 | Happy | HR batch reject 3 đơn + lý do | POST batch action=REJECT + note | rejected=3. Lý do chung gửi cho tất cả NV. | P1 |
| TC-AP03-EC-01 | Edge | Batch 50 đơn (max limit) | POST 50 items | Xử lý tuần tự. Timeout đủ lớn. Kết quả per-item. | P2 |
| TC-AP03-EC-02 | Edge | Batch 51 đơn (>max) | POST 51 items | 400: "Tối đa 50 đơn/batch." | P2 |
| TC-AP03-EC-03 | Edge | 3/5 đơn thành công, 2 fail (đã xử lý) | Batch 5/mixed | approved=3, failed=2. Không rollback đơn thành công. | P1 |
| TC-AP03-ER-01 | Error | Batch reject không có lý do | POST REJECT note="" | 400: REJECT_REASON_REQUIRED. Chặn toàn batch. | P1 |
| TC-AP03-ER-02 | Error | Batch chứa đơn khác requestType | POST mixed Leave+OT | Cho phép nếu approver có quyền cho cả 2 type. | P2 |
| TC-AP03-ER-03 | Error | Batch timeout (server quá tải) | POST khi load cao | 202: Accepted. Job ID trả về. Poll status endpoint. | P3 |
| TC-AP03-SEC-01 | Security | Batch approve đơn team khác | POST ids=other_team | Chỉ approve đơn thuộc quyền. Đơn ngoài quyền: failed=true. | P1 |
| TC-AP03-CON-01 | Concurrency | 2 HR cùng batch approve overlapping set | Concurrent batch | Đơn đã processed: skip (ALREADY_PROCESSED). Không duplicate approve. | P2 |
| TC-AP03-DI-01 | Data | Batch 5 leave approve → 5 balance updates | After batch | Mỗi NV balance update đúng. No partial state. | P1 |
| TC-AP03-PERF-01 | Perf | Batch 50 đơn | POST 50 items | Xử lý ≤ 30 giây. Progress indicator trên UI. | P2 |
