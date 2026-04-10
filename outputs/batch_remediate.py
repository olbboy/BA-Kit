#!/usr/bin/env python3
"""
Batch remediation: Add EDGE CASES & ERROR HANDLING sections
to all US files that are missing them.
Also fixes ambiguous SO THAT phrases (Phase 2).
"""

import os
import re
from pathlib import Path

BASE = Path('/Users/dmdat/Workspaces/Projects/ba-kit-antigravity/outputs/mini-app-cham-cong/2.11-Mini-app')

# ────────────────────────────────────────────────────────────
# Edge Cases per US file (manually curated per domain context)
# ────────────────────────────────────────────────────────────

EDGE_CASES = {
    # ── Module 2.11.2: Ca làm việc ──
    'US-SHIFT-01': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SH01-E1 | **Ca không có nhân viên** — Ca mới tạo chưa gán NV | LOW | Thẻ ca hiển thị "0 nhân viên", avatar section trống. Không ẩn thẻ. |
| SH01-E2 | **Số lượng ca > 50** — Doanh nghiệp lớn có nhiều ca | MEDIUM | Danh sách hỗ trợ virtual scroll, lazy load mỗi batch 20 thẻ. Search bar cho phép tìm theo tên ca. |
| SH01-E3 | **Ca bị xóa khi đang có NV** — HR xóa ca có 100 NV đang active | HIGH | Chặn xóa. Hiển thị: "Không thể xóa ca đang có [N] nhân viên. Vui lòng chuyển NV sang ca khác trước." |
| SH01-E4 | **Concurrent edit** — 2 HR cùng sửa 1 ca | MEDIUM | Optimistic locking: HR sửa sau nhận cảnh báo "Ca đã được cập nhật bởi [Tên HR]. Vui lòng tải lại." |
""",

    'US-SHIFT-02': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SH02-E1 | **Giờ kết thúc < Giờ bắt đầu** — VD: 22:00 - 06:00 (Ca đêm) | HIGH | Hệ thống nhận diện ca đêm (cross-midnight). Tự động set endDate = startDate + 1. Hiển thị badge "Ca đêm". |
| SH02-E2 | **Giờ trùng với ca khác** — 2 ca có overlapping time window | MEDIUM | Cảnh báo (không chặn): "Khung giờ trùng với ca [Tên ca]. NV không thể thuộc cả 2 ca cùng ngày." |
| SH02-E3 | **Ca có 0h working** — Giờ bắt đầu = Giờ kết thúc | HIGH | Validation chặn: "Tổng giờ làm phải > 0. Vui lòng kiểm tra lại khung giờ." |
| SH02-E4 | **Ngày áp dụng trong quá khứ** — HR set effective date đã qua | MEDIUM | Cảnh báo: "Ngày hiệu lực trong quá khứ. Dữ liệu chấm công lịch sử sẽ KHÔNG bị tính lại." Cho phép tiếp tục. |
""",

    'US-SHIFT-03': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SH03-E1 | **Punch limit = 0** — HR set giờ giới hạn = 0 phút | HIGH | Validation: "Giới hạn chấm công phải ≥ 30 phút." Chặn lưu. |
| SH03-E2 | **Punch limit > 24h** — Nhập giá trị vô lý | HIGH | Validation: "Giới hạn chấm công không được vượt quá 24 giờ." |
| SH03-E3 | **NV quẹt ngoài punch limit** — Quẹt trước giờ cho phép | MEDIUM | Mốc quẹt bị reject với status OUTSIDE_PUNCH_LIMIT. NV nhận thông báo: "Chấm công ngoài giới hạn thời gian cho phép." |
| SH03-E4 | **Ca đêm cross-midnight punch** — Punch limit ca 22:00-06:00 bao gồm 2 ngày | MEDIUM | Giới hạn tính liên tục qua 00:00 (VD: từ 21:00 T đến 07:00 T+1). Không bị cắt tại nửa đêm. |
""",

    'US-SHIFT-04': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SH04-E1 | **Giờ nghỉ lớn hơn giờ làm** — Nghỉ trưa 5h trong ca 8h | HIGH | Validation: "Tổng giờ nghỉ ([N]h) không được ≥ tổng giờ làm ([M]h)." Chặn lưu. |
| SH04-E2 | **Giờ nghỉ ngoài khung ca** — Nghỉ 18:00-19:00 nhưng ca kết thúc 17:00 | MEDIUM | Validation: "Giờ nghỉ phải nằm trong khung ca làm việc [HH:MM - HH:MM]." |
| SH04-E3 | **Nhiều khoảng nghỉ overlap** — Nghỉ 12:00-13:00 và 12:30-13:30 | MEDIUM | Validation: "Khoảng nghỉ bị trùng lắp. Vui lòng điều chỉnh." |
| SH04-E4 | **Ca không có giờ nghỉ** — Ca 4h không set break | LOW | Cho phép. Working hours = Full shift duration. Hiển thị note: "Ca này chưa cấu hình giờ nghỉ." |
""",

    'US-SHIFT-05': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SH05-E1 | **File Excel lỗi format** — Cột thiếu, data type sai | HIGH | Trả file lỗi kèm cột "Lý do lỗi" cho mỗi dòng. Không import dòng lỗi. Hiển thị: "X/Y bản ghi thành công, Z lỗi." |
| SH05-E2 | **NV đã thuộc ca khác** — Import NV đang active ở ca cũ | MEDIUM | Cảnh báo: "[N] NV đang thuộc ca khác. Chọn: (A) Chuyển sang ca mới, (B) Bỏ qua, (C) Thêm ca phụ." |
| SH05-E3 | **Mã NV không tồn tại** — File chứa mã NV không có trong hệ thống | HIGH | Mark as ERROR. Ghi nhận vào file kết quả: "Mã NV [X] không tồn tại trong hệ thống." |
| SH05-E4 | **Import file > 5000 dòng** — Vượt giới hạn batch | MEDIUM | Hiển thị: "File vượt quá 5,000 bản ghi. Vui lòng chia nhỏ file." Chặn upload. |
| SH05-E5 | **Duplicate trong file** — Cùng 1 mã NV xuất hiện 2 lần | MEDIUM | Lấy dòng cuối cùng (last-write-wins). Log warning: "Mã NV [X] bị trùng tại dòng [A] và [B], lấy dòng [B]." |
""",

    # ── Module 2.11.5: Báo cáo cá nhân ──
    'US-RPTPRS-01': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RP01-E1 | **NV mới < 1 tháng** — Chưa đủ dữ liệu tính score | LOW | Dashboard hiển thị: "Chưa đủ dữ liệu (cần ≥ 1 tháng)." Ẩn biểu đồ trend. Hiển thị dữ liệu raw có sẵn. |
| RP01-E2 | **NV chuyển site giữa tháng** — Dữ liệu thuộc 2 site | MEDIUM | Gộp dữ liệu cả 2 site cho tháng hiện tại. Ghi chú: "Bao gồm dữ liệu từ [Site A] (01-15) và [Site B] (16-30)." |
| RP01-E3 | **Ca đêm ảnh hưởng tính toán ngày công** | MEDIUM | Ngày công tính theo ngày bắt đầu ca (VD: ca 22:00 T → 06:00 T+1 = ngày công T). |
""",

    'US-RPTPRS-02': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RP02-E1 | **KPI target chưa được cấu hình** — HR chưa set target cho site | MEDIUM | Hiển thị actual values, cột target hiển thị "N/A". Badge: "Target chưa được thiết lập — liên hệ HR." |
| RP02-E2 | **Dữ liệu OT bị điều chỉnh sau chốt công** — Review lại số liệu sau correction | LOW | Hiển thị giá trị sau correction kèm icon "Đã điều chỉnh". Tooltip: "Giá trị gốc: X, Sau điều chỉnh: Y." |
""",

    # ── Module 2.11.6: Quản lý nhân sự ──
    'US-EMP-01': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM01-E1 | **Sơ đồ > 1000 node** — Tổ chức lớn | MEDIUM | Lazy-load: chỉ render 3 cấp đầu tiên. Expand on-demand. Virtual rendering cho performance. |
| EM01-E2 | **NV thuộc nhiều phòng ban** — IT support multi-site | MEDIUM | Hiển thị tại Primary department. Icon link "→ Xem thêm" dẫn đến các department phụ. |
| EM01-E3 | **Drag-drop vào chính nó** — Kéo phòng ban vào chính nó hoặc child | HIGH | Chặn: "Không thể chuyển đơn vị vào chính nó hoặc đơn vị con." |
""",

    'US-EMP-02': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM02-E1 | **Xóa phòng ban có NV** — Phòng ban còn 50 NV active | HIGH | Chặn xóa. Hiển thị: "Phòng ban còn [50] nhân viên. Chuyển NV trước khi xóa." |
| EM02-E2 | **Tên phòng ban trùng** — Tạo 2 phòng ban cùng tên tại 1 site | MEDIUM | Cho phép nhưng cảnh báo: "Đã tồn tại phòng ban '[Tên]' tại chi nhánh này." |
| EM02-E3 | **Xóa phòng ban cha** — Phòng ban có sub-departments | HIGH | Chặn: "Phòng ban có [N] đơn vị con. Xóa hoặc chuyển đơn vị con trước." |
""",

    'US-EMP-03': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM03-E1 | **Tìm kiếm không dấu** — VD: "Nguyen" tìm "Nguyễn" | MEDIUM | Full-text search không phân biệt dấu, hoa/thường. Sử dụng unaccent + ILIKE. |
| EM03-E2 | **Danh sách > 5000 NV** — Load time | MEDIUM | Phân trang server-side (50 NV/trang). Virtual scroll cho smooth UX. |
| EM03-E3 | **NV status TRANSFERRED** — Đang chuyển chi nhánh | LOW | Hiển thị badge "Đang chuyển" màu vàng. Cho phép xem nhưng không chỉnh sửa. |
""",

    'US-EMP-04': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM04-E1 | **Email trùng** — Import 2 NV cùng email | HIGH | Mark lỗi: "Email [X] đã tồn tại (NV: [Mã NV cũ])." Không import dòng trùng. |
| EM04-E2 | **Phòng ban không tồn tại** — File Excel chứa tên phòng ban sai | HIGH | Mark lỗi: "Phòng ban '[X]' không tồn tại. Tạo phòng ban trước hoặc sửa file." |
| EM04-E3 | **File > 5000 dòng** | MEDIUM | Chặn: "File vượt 5,000 bản ghi. Vui lòng chia nhỏ." |
| EM04-E4 | **Upload giữa chừng mất mạng** — Processed 2000/5000 dòng | HIGH | Transaction toàn file: rollback toàn bộ nếu lỗi giữa chừng. Hoặc: partial commit kèm report "2000 thành công, 3000 chưa xử lý." |
""",

    'US-EMP-05': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM05-E1 | **Camera offline** — Không có dữ liệu real-time từ site | MEDIUM | Badge "Offline" trên site card. Hiển thị dữ liệu cuối cùng kèm timestamp "Cập nhật lúc [HH:MM]." |
| EM05-E2 | **Toàn bộ NV WFH** — On-site = 0 | LOW | Hiển thị đúng "0 on-site". Không ẩn dashboard. Hiển thị chi tiết WFH breakdown. |
| EM05-E3 | **Timezone khác nhau** — Site ở HCM (UTC+7) vs Site ở HN (UTC+7) nhưng server UTC | LOW | Tất cả giờ hiển thị theo timezone site. Server store UTC, client convert theo site timezone. |
""",

    'US-EMP-06': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EM06-E1 | **Xóa cấp bậc đang được sử dụng** — 200 NV có cấp bậc "Nhân viên" | HIGH | Chặn xóa: "Cấp bậc đang được gán cho [200] NV. Chuyển NV sang cấp bậc khác trước." |
| EM06-E2 | **Tên cấp bậc trùng** | MEDIUM | Chặn: "Cấp bậc '[X]' đã tồn tại." |
""",

    # ── Module 2.11.7: Lịch nghỉ ──
    'US-HOL-01': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| HL01-E1 | **Ngày nghỉ trùng cuối tuần** — VD: 30/4 rơi vào Chủ nhật | MEDIUM | HR quyết định: (A) Nghỉ bù T2, (B) Không nghỉ bù. Hệ thống hiển thị cảnh báo khi tạo. |
| HL01-E2 | **Xóa ngày nghỉ đã có đơn nghỉ phép** — NV đã approved leave trùng ngày | HIGH | Chặn xóa. Hiển thị: "[N] đơn nghỉ phép đã approved trùng ngày này. Hủy đơn trước khi xóa." |
| HL01-E3 | **Ngày nghỉ thiên tai — scope vùng** — Chỉ áp dụng 1 số tỉnh | MEDIUM | Chọn scope: Toàn quốc / Tỉnh cụ thể. Chỉ NV có Primary Site tại tỉnh đó mới bị ảnh hưởng. |
""",

    'US-HOL-02': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| HL02-E1 | **Policy trùng date range** — 2 policy nghỉ lễ cùng ngày cho cùng site | HIGH | Chặn: "Đã tồn tại policy nghỉ cho ngày [DD/MM] tại [Site]. Vui lòng chỉnh sửa policy hiện có." |
| HL02-E2 | **Rule nghỉ circular** — Rule A tham chiếu Rule B, Rule B tham chiếu Rule A | HIGH | Validation: phát hiện circular reference. Chặn lưu kèm message rõ ràng. |
| HL02-E3 | **Policy áp dụng retroactive** — Tạo policy cho ngày đã qua | MEDIUM | Cảnh báo: "Policy áp dụng cho ngày trong quá khứ. Dữ liệu chấm công lịch sử sẽ được tính lại." Yêu cầu xác nhận. |
""",

    'US-HOL-03': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| HL03-E1 | **Batch job fail giữa chừng** — Sync 1000 NV, lỗi tại NV thứ 500 | HIGH | Ghi log chi tiết. Đánh dấu NV lỗi. Tiếp tục xử lý NV còn lại. Retry failed batch sau 15 phút. |
| HL03-E2 | **Duplicate sync event** — 2 instance job chạy đồng thời | MEDIUM | Distributed lock (Redis). Instance thứ 2 skip nếu lock đã active. Log: "Sync already running, skipped." |
| HL03-E3 | **Config thay đổi giữa batch** — HR thay đổi policy khi batch đang chạy | LOW | Batch dùng snapshot config tại thời điểm bắt đầu. Thay đổi áp dụng cho batch tiếp theo. |
""",

    'US-HOL-04': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| HL04-E1 | **API query year = null** — Client không gửi year param | LOW | Default: năm hiện tại. Response header: `X-Default-Year: 2026`. |
| HL04-E2 | **API rate limit** — Client gọi > 100 req/phút | MEDIUM | 429 Too Many Requests. Header: `Retry-After: 60`. |
| HL04-E3 | **Không có dữ liệu cho năm** — Query năm chưa có policy | LOW | Trả array rỗng `[]` với HTTP 200 (không phải 404). |
""",

    # ── Module 2.11.8: Camera AI ──
    'US-CAM-01': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| CM01-E1 | **Device ID trùng** — Đăng ký camera đã có trong hệ thống | HIGH | Chặn: "Device ID [X] đã được đăng ký tại [Site Y]." |
| CM01-E2 | **Xóa camera đang active** — Camera đang có NV check-in hằng ngày | HIGH | Soft-delete: set status INACTIVE. Dữ liệu lịch sử giữ nguyên. Cần confirm: "Camera sẽ ngừng nhận dữ liệu chấm công." |
| CM01-E3 | **Camera chưa có trên C-Vision** — DeviceId không match C-Vision API | MEDIUM | Cảnh báo: "Thiết bị chưa được đăng ký trên C-Vision. Webhook sẽ bị reject." Cho phép lưu draft. |
""",

    'US-CAM-02': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| CM02-E1 | **NV chưa có ảnh khuôn mặt** — Mapping NV mới chưa enroll face | MEDIUM | Trạng thái mapping: PENDING_ENROLLMENT. Alert: "NV [Tên] cần chụp ảnh khuôn mặt tại bộ phận IT." |
| CM02-E2 | **1 NV map nhiều C-Vision ID** — NV enroll trên 2 device khác nhau | MEDIUM | Cho phép (multi-device). Bảng mapping hiển thị tất cả. De-dup attendance dựa trên employeeId. |
| CM02-E3 | **Bulk mapping file lỗi** — CSV chứa employeeCode không tồn tại | HIGH | Trả file lỗi kèm cột ghi chú. Không tạo mapping cho dòng lỗi. |
""",

    'US-CAM-03': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| CM03-E1 | **Camera offline > 1 giờ** — Health check fail liên tục | HIGH | Escalate: Email IT Manager + Push notification. Dashboard badge đỏ. Log incident. |
| CM03-E2 | **False offline** — Network hiccup 30 giây | LOW | Grace period: 3 consecutive fails (15 phút) mới đánh dấu offline. Tránh alert spam. |
| CM03-E3 | **Tất cả camera cùng site offline** — Mất mạng toàn site | CRITICAL | Alert đặc biệt cho SITE_MANAGER + IT. Fallback: cho phép manual check-in. Banner toàn app: "Hệ thống camera tại [Site] đang bảo trì." |
""",

    # ── Module 2.11.9: Thông báo ──
    'US-NOTIF-01': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| NF01-E1 | **NV tắt Push Permission** — iOS/Android block notification | MEDIUM | Fallback sang Email. Dashboard hiển thị: "Push bị tắt — đang dùng Email." Nhắc NV bật Push khi mở app. |
| NF01-E2 | **Email bounce** — Email NV không hợp lệ | MEDIUM | Mark as FAILED. Retry 1 lần. Log vào dead letter queue. HR dashboard: "[N] NV có email lỗi." |
| NF01-E3 | **Kênh bị disable toàn hệ thống** — Admin tắt kênh Push | HIGH | Cảnh báo admin: "Tắt kênh Push sẽ ảnh hưởng [N] loại thông báo. Thông báo bắt buộc sẽ chuyển sang Email." |
""",

    'US-NOTIF-02': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| NF02-E1 | **Trigger event spike** — 5000 NV check-in cùng lúc (đầu ca) | HIGH | Queue-based processing (BullMQ). Rate limit: 100 notification/giây. NV nhận trong ≤ 60s. |
| NF02-E2 | **Trigger cho NV đã nghỉ việc** — Event cho NV status INACTIVE | LOW | Skip notification. Log: "Skipped notification for inactive employee [ID]." |
| NF02-E3 | **Duplicate trigger** — Cùng 1 event gửi 2 lần (webhook retry) | MEDIUM | Idempotency key per event. Lần 2 skip, log: "Duplicate event [key], ignored." |
""",

    'US-NOTIF-03': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| NF03-E1 | **NV tắt thông báo bắt buộc** — Cố tắt notification phê duyệt | HIGH | UI disable toggle cho thông báo bắt buộc. Backend ignore "mute" request cho mandatory events. |
| NF03-E2 | **Quiet hours conflict với ca đêm** — Quiet hours 22:00-07:00, NV ca đêm cần check-in reminder | MEDIUM | Ca đêm NV: quiet hours auto-adjusted theo shift schedule. Chỉ mute khi NV KHÔNG có ca. |
| NF03-E3 | **Batch digest quá lớn** — Daily digest chứa > 50 items | LOW | Truncate tại 20 items + link "Xem thêm [N] thông báo khác trên App." |
""",

    # ── Module 2.11.10: Phê duyệt ──
    'US-APPR-01': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| AP01-E1 | **Approver bị terminated** — Manager nghỉ việc khi có đơn PENDING | CRITICAL | Auto-reassign sang fallback chain (SITE_MANAGER → SITE_HR → GLOBAL_HR). Push NV: "Đơn đã chuyển đến [Approver mới]." Audit: "Auto-reassigned." |
| AP01-E2 | **Self-approve** — Manager gửi đơn nghỉ cho chính mình duyệt | HIGH | Chặn self-approve. Auto-route lên DEPT_HEAD hoặc SITE_HR. |
| AP01-E3 | **Approver offline > 7 ngày** — Không duyệt đơn nào trong 7 ngày | MEDIUM | Auto-escalate lên level tiếp. Alert HR: "[Tên] có [N] đơn quá hạn." Không auto-approve. |
| AP01-E4 | **Đơn tạo sát ngày chốt công** — Đơn tạo ngày 24, chốt công ngày 25 | MEDIUM | Cảnh báo approver: "Đơn này cần duyệt trước [DD/MM] (ngày chốt công)." Push reminder 24h trước. |
""",

    'US-APPR-02': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| AP02-E1 | **Tổ chức thay đổi giữa approval** — NV chuyển phòng khi đơn đang xử lý | MEDIUM | Snapshot approver chain tại thời điểm tạo đơn. Thay đổi tổ chức KHÔNG ảnh hưởng đơn đang pending. |
| AP02-E2 | **Config approval chain rỗng** — Site mới chưa cấu hình | HIGH | Chặn NV tạo đơn. Hiển thị: "Chưa cấu hình quy trình phê duyệt. Liên hệ HR chi nhánh." |
| AP02-E3 | **Circular approval** — Manager A approve cho Manager B và ngược lại | HIGH | Validate chain: không cho phép circular. Chặn lưu config nếu phát hiện loop. |
""",

    'US-APPR-03': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| AP03-E1 | **Batch approve lỗi giữa chừng** — Đơn thứ 25/50 bị lỗi | MEDIUM | Xử lý tuần tự, không rollback đã duyệt. Kết quả: "24 ✓, 1 ✗, 25 ○". Retry riêng đơn lỗi. |
| AP03-E2 | **Batch quá lớn** — Chọn > 50 đơn | LOW | Chặn: "Tối đa 50 đơn/lần. Đã chọn [N]." |
| AP03-E3 | **Đơn bị cancel khi đang trong batch** — NV hủy đơn ngay lúc manager batch approve | MEDIUM | Check status trước khi approve. Đơn CANCELLED → skip, ghi nhận "Đã bị hủy bởi NV." |
""",

    # ── Module 2.11.11: Báo cáo tổng ──
    'US-RPT-01': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RT01-E1 | **Phòng ban không có dữ liệu** — Phòng ban mới tạo, chưa có NV chấm công | LOW | Hiển thị "Chưa có dữ liệu" thay vì 0%. Không tính vào average. |
| RT01-E2 | **Dữ liệu chưa chốt** — Xem dashboard tháng chưa đến ngày chốt | MEDIUM | Badge: "Dữ liệu tạm tính (chưa chốt công)." Màu cam thay vì xanh. Số liệu live update. |
| RT01-E3 | **RBAC filter** — Manager xem báo cáo phòng ban khác | HIGH | Chặn: chỉ hiển thị phòng ban mà user có quyền. SITE_HR xem toàn site. GLOBAL_HR xem toàn bộ. |
""",

    'US-RPT-02': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RT02-E1 | **Export file > 10MB** — 5000 NV × 12 tháng | MEDIUM | Async export: "File đang được tạo. Bạn sẽ nhận email khi hoàn tất." Không block UI. |
| RT02-E2 | **Template payroll không khớp** — MISA format khác SAP format | MEDIUM | Dropdown chọn template: MISA / SAP / Oracle / Custom. Preview 5 dòng đầu trước khi export. |
| RT02-E3 | **Export dữ liệu chưa chốt công** — Tháng chưa complete | HIGH | Cảnh báo: "Dữ liệu tháng [MM] chưa chốt công. File export có thể thay đổi." Yêu cầu confirm. |
| RT02-E4 | **NV có OT qua 2 tháng** — OT ca đêm T cuối tháng → T+1 đầu tháng kế | MEDIUM | Split: giờ trước 00:00 tính tháng M, giờ sau 00:00 tính tháng M+1. Ghi chú trong file export. |
""",

    'US-RPT-03': """
### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RT03-E1 | **OT vượt giới hạn pháp luật** — NV > 200h/năm | CRITICAL | Highlight đỏ trong báo cáo. Alert HR + Ban Giám đốc. Ghi nhận risk: "Vi phạm ND 13/2023 Điều [X]." |
| RT03-E2 | **Nghỉ phép vượt quota** — NV nghỉ > số phép cho phép (do approved nhầm) | HIGH | Flag trong báo cáo: "Vượt hạn mức [N] ngày." Gợi ý: trừ lương hoặc chuyển sang nghỉ không lương. |
| RT03-E3 | **Data discrepancy** — Tổng ngày công dashboard ≠ file export | HIGH | Checksum validation trước khi export. Nếu khác biệt > 0.5 ngày → alert: "Dữ liệu không nhất quán. Liên hệ IT." |
""",
}

# ────────────────────────────────────────────────────────────
# Ambiguity fixes (Phase 2)
# ────────────────────────────────────────────────────────────

AMBIGUITY_FIXES = {
    'US-NOTIF-03': (
        '**SO THAT** hệ thống gửi thông báo hiệu quả, không spam',
        '**SO THAT** hệ thống gửi ≤ 3 thông báo/giờ cho mỗi NV, không spam'
    ),
    'US-EMP-03': (
        '**SO THAT** tôi có thể tra cứu, quản lý thông tin nhân viên hiệu quả.',
        '**SO THAT** tôi có thể tra cứu nhân viên trong ≤ 3 thao tác và quản lý thông tin chính xác.'
    ),
    'US-NOTIF-01': (
        '**SO THAT** nhân viên nhận được thông báo qua kênh phù hợp nhất',
        '**SO THAT** nhân viên nhận được thông báo qua kênh ưu tiên theo cấu hình (Push > Email > In-App)'
    ),
    'US-SHIFT-05': (
        'một cách nhanh chóng và chính xác',
        'trong ≤ 30 giây cho 500 bản ghi và chính xác (0 sai sót format)'
    ),
    'US-SHIFT-01': (
        'nắm bắt nhanh chóng hiện trạng',
        'nắm bắt hiện trạng trong ≤ 2 giây tải trang'
    ),
    'US-EMP-01': (
        'thực hiện điều chuyển tổ chức nhanh chóng.',
        'thực hiện điều chuyển tổ chức bằng drag-and-drop trực quan.'
    ),
    'US-APPR-01': (
        'duyệt hoặc từ chối nhanh kèm lý do',
        'duyệt hoặc từ chối trong ≤ 2 tap trên mobile kèm lý do'
    ),
    'US-APPR-03': (
        '**SO THAT** tôi có thể xử lý nhanh khi có nhiều đơn tồn đọng',
        '**SO THAT** tôi có thể xử lý ≤ 50 đơn/lần trong ≤ 3 giây khi có nhiều đơn tồn đọng'
    ),
}


def find_us_file(us_id: str) -> Path:
    """Find the markdown file for a US ID."""
    for f in BASE.rglob(f'{us_id}-*.md'):
        return f
    for f in BASE.rglob(f'{us_id}*.md'):
        return f
    return None


def process_file(us_id: str, edge_case_text: str):
    """Add edge cases to a file and fix ambiguities if applicable."""
    filepath = find_us_file(us_id)
    if not filepath:
        print(f"  ❌ File not found: {us_id}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # Check if already has edge cases
    if 'EDGE CASE' in content or 'ERROR HANDLING' in content:
        print(f"  ⏩ Already has edge cases: {us_id}")
    else:
        # Check if has DoD — insert before DoD, or append to end
        if 'DEFINITION OF DONE' in content:
            content = content.rstrip() + '\n\n---\n' + edge_case_text
        else:
            # Add both edge cases and DoD
            dod_section = f"""
---

### **DEFINITION OF DONE (DOD)**

1. **AC Verified**: Tất cả Acceptance Criteria pass QA testing.
2. **RBAC Enforced**: Phân quyền đúng theo role matrix.
3. **Edge Cases Tested**: Tất cả edge cases trong bảng trên được test.
4. **Responsive**: UI hoạt động trên mobile (375px+) và desktop.
5. **API Error Handling**: Tất cả API trả error code + message rõ ràng.
"""
            content = content.rstrip() + '\n\n---\n' + edge_case_text + dod_section
        modified = True
        print(f"  ✅ Added edge cases: {us_id}")

    # Apply ambiguity fixes
    if us_id in AMBIGUITY_FIXES:
        old_text, new_text = AMBIGUITY_FIXES[us_id]
        if old_text in content:
            content = content.replace(old_text, new_text, 1)
            modified = True
            print(f"  ✅ Fixed ambiguity: {us_id}")

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def add_rbac_to_shift_files():
    """Add RBAC section to US-SHIFT-03 and US-SHIFT-04."""
    rbac_section = """
### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin | Role | Ghi chú |
| --- | --- | --- |
| Cấu hình punch limit | HR Admin | Chỉ HR mới được thay đổi giới hạn. |
| Xem cấu hình hiện tại | HR, Quản lý | Read-only cho Quản lý. |
"""
    for us_id in ['US-SHIFT-03', 'US-SHIFT-04']:
        filepath = find_us_file(us_id)
        if not filepath:
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'RBAC' in content or 'ACCESS CONTROL' in content:
            print(f"  ⏩ Already has RBAC: {us_id}")
            continue
        # Insert after BUSINESS FLOW section
        insertion_point = content.find('### **3.')
        if insertion_point == -1:
            insertion_point = content.find('### **2.')
        if insertion_point > 0:
            # Find the --- before section 3
            prev_hr = content.rfind('---', 0, insertion_point)
            if prev_hr > 0:
                content = content[:prev_hr] + '---\n' + rbac_section + '\n---\n\n' + content[insertion_point:]
            else:
                content = content[:insertion_point] + rbac_section + '\n---\n\n' + content[insertion_point:]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Added RBAC: {us_id}")


def main():
    print("=" * 60)
    print("Batch Remediation: Edge Cases + DoD + Ambiguity Fixes")
    print("=" * 60)

    total = 0
    updated = 0

    for us_id, edge_text in EDGE_CASES.items():
        total += 1
        if process_file(us_id, edge_text):
            updated += 1
        
    print(f"\n--- Phase 2: RBAC fixes ---")
    add_rbac_to_shift_files()

    print(f"\n{'=' * 60}")
    print(f"DONE! Processed: {total} | Updated: {updated}")
    print("=" * 60)


if __name__ == '__main__':
    main()
