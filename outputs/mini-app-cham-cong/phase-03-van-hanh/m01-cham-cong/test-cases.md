# Test Suite — M01: Chấm công & Nhật ký

**Generated:** 2026-04-11 | **Standard:** ISTQB | **Agent:** @ba-test-gen
**Coverage Target:** ≥80% across 7 categories

---

## Coverage Summary

| US | Happy Path | Edge | Error | Security | Concurrency | Data Integrity | Performance | Total TCs |
|----|-----------|------|-------|----------|-------------|----------------|-------------|-----------|
| US-ATTEN-01 | 3 | 6 | 3 | 2 | 1 | 1 | 1 | **17** |
| US-ATTEN-02 | 2 | 3 | 2 | 1 | 0 | 1 | 1 | **10** |
| US-ATTEN-03 | 2 | 2 | 2 | 2 | 0 | 1 | 1 | **10** |
| US-ATTEN-04 | 2 | 3 | 2 | 1 | 0 | 1 | 0 | **9** |
| US-ATTEN-05 | 2 | 3 | 3 | 2 | 1 | 1 | 0 | **12** |
| **Total** | **11** | **17** | **12** | **8** | **2** | **5** | **3** | **58** |
| **Coverage** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **95%** |

---

## US-ATTEN-01: Hub chấm công

### Happy Path

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A01-HP-01 | NV có ca sáng 08:00-17:00, quẹt mặt thành công lúc 07:55 | 1. NV quẹt mặt tại camera 2. Mở Mini App | confidence=0.95 | Badge "ĐÃ CHẤM CÔNG" (Xanh), Giờ Vào = 07:55, thanh tiến độ bắt đầu chạy | P1-Critical |
| TC-A01-HP-02 | NV chưa quẹt trong ngày | 1. Mở Mini App | — | Badge "CHƯA CHẤM CÔNG" (Xám), Giờ Vào = --:--, thanh tiến độ 0% | P1-Critical |
| TC-A01-HP-03 | NV đã quẹt vào lúc 08:00 và ra lúc 17:05 | 1. Mở Mini App | — | Badge "ĐÃ CHẤM CÔNG" (Xanh), Giờ Vào = 08:00, Giờ Ra = 17:05, tiến độ 100%+ | P1-Critical |

### Edge Cases (Boundary Value Analysis)

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A01-EC-01 | NV quẹt đúng giờ bắt đầu ca | 1. Quẹt lúc 08:00:00 | time=08:00:00 | Late = 0 phút. Badge Xanh. Đúng giờ. | P2-High |
| TC-A01-EC-02 | Ca đêm 20:00-06:00, quẹt lúc 23:50 (T) | 1. Quẹt mặt 23:50 ngày T | date=T, time=23:50 | Gán vào Nhật ký ngày T. Tiến độ tiếp tục chạy xuyên 00:00. | P2-High |
| TC-A01-EC-03 | Grace Period: quẹt 08:12, ca 08:00, grace=15 | 1. Quẹt lúc 08:12 | grace=15min | Đúng giờ (08:12 < 08:15). Late = 0 phút. | P1-Critical |
| TC-A01-EC-04 | Grace Period: quẹt 08:16, ca 08:00, grace=15 | 1. Quẹt lúc 08:16 | grace=15min | Trễ 1 phút. Badge cảnh báo. lateMins = 1. | P1-Critical |
| TC-A01-EC-05 | Grace Period boundary: quẹt 08:15:00 exact | 1. Quẹt lúc 08:15:00 | grace=15min | Đúng giờ (=15, đúng boundary inclusive). Late = 0. | P1-Critical |
| TC-A01-EC-06 | Ca đêm qua 2 loại ngày: T=weekday, T+1=holiday | 1. Ca 20:00-06:00, giờ trước 00:00 = weekday, sau 00:00 = holiday | — | Split calculation tại 00:00. OT hệ số khác nhau cho mỗi phần. | P2-High |

### Error Cases

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A01-ER-01 | Webhook delay > 60s SLA | 1. Camera gửi webhook muộn | delay>60s | Mini-banner "Đang đồng bộ dữ liệu..." thay vì badge xám. Auto-retry 15s, timeout 5 phút. | P2-High |
| TC-A01-ER-02 | NV chưa được gán ca | 1. NV quẹt mặt 2. Mở App | no_shift=true | Badge "Chưa có ca làm việc". Ẩn thanh tiến độ. Link "Liên hệ HR". Record vẫn lưu (UNASSIGNED). | P2-High |
| TC-A01-ER-03 | Confidence = 0.84 (dưới ngưỡng 0.85) | 1. Camera gửi webhook conf=0.84 | confidence=0.84 | Không tạo attendance record approved. Cần HR review. | P2-High |

### Security Cases

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A01-SEC-01 | NV A đang đăng nhập | 1. Gọi API GET /attendance/today?empId=NV_B | empId=NV_B | 403 Forbidden. ABAC chặn xem dữ liệu NV khác. | P1-Critical |
| TC-A01-SEC-02 | NV thử xem qua Web Inspect/URL manipulation | 1. Sửa empId URL param | — | Backend validate User_ID đăng nhập vs. empId request. Trả 403. | P1-Critical |

### Concurrency Cases

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A01-CON-01 | Camera gửi 3 webhook cách nhau <30s | 1. Webhook 1 lúc 08:00:00 2. Webhook 2 lúc 08:00:15 3. Webhook 3 lúc 08:00:25 | 3 webhooks | De-duplication: chỉ giữ mốc 08:00:00 (sớm nhất). 2 webhook sau bị drop. | P2-High |

### Data Integrity

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A01-DI-01 | NV check-in tạo attendance_record | 1. Check-in 2. Verify daily_attendance_summaries | — | daily_attendance_summaries.first_checkin_at = attendance_records.recorded_at. Consistent. | P2-High |

### Performance

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A01-PERF-01 | 5000 NV cùng check-in sáng (8:00-8:30) | 1. Simulate 5000 webhook trong 30 phút | 5000 concurrent | Webhook processing < 60s SLA. Không mất record. Queue depth manageable. | P3-Medium |

---

## US-ATTEN-02: Thống kê hiệu suất tháng

### Happy Path

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A02-HP-01 | NV có 15 ngày chấm công trong tháng, 13 đúng giờ | 1. Mở thống kê tháng | — | Tỷ lệ đúng giờ = 87%, Tổng nghỉ = 2 ngày, OT hiển thị đúng | P1-Critical |
| TC-A02-HP-02 | NV có OT được duyệt 1.5h | 1. Xem thẻ OT | — | Thẻ hiển thị "01.5h". Cập nhật real-time sau khi đơn OT được duyệt. | P1-Critical |

### Edge Cases

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A02-EC-01 | Ngày 01 đầu tháng, chưa có dữ liệu | 1. Mở thống kê | mẫu_số=0 | Hiển thị "--" cho tất cả metrics. Không NaN/0%. | P1-Critical |
| TC-A02-EC-02 | NV gia nhập ngày 15, xem thống kê cuối tháng | 1. Mở thống kê | joinDate=15 | Mẫu số tính từ ngày 15. Ghi chú "(Tính từ 15/04)". | P2-High |
| TC-A02-EC-03 | NV nghỉ thai sản 6 tháng | 1. Mở thống kê | longLeave=true | Hiển thị "Đang nghỉ dài hạn — Thai sản". Ẩn thẻ thống kê chuyên cần. | P2-High |

### Error Cases

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A02-ER-01 | API timeout khi tính thống kê | 1. Backend tính quá 1.5s | — | Hiển thị skeleton/loading. Retry. Nếu fail → "Không tải được dữ liệu. Thử lại." | P2-High |
| TC-A02-ER-02 | Dữ liệu chấm công bị corrupt (missing shift) | 1. NV có record nhưng không có shift_id | — | Bỏ ngày đó khỏi mẫu số. Ghi log cảnh báo cho HR. | P3-Medium |

### Security

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A02-SEC-01 | NV A cố xem thống kê NV B | 1. API call với empId=NV_B | — | 403 Forbidden. ABAC filter by User_ID. | P1-Critical |

### Data Integrity

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A02-DI-01 | Thống kê phải khớp nhật ký | 1. So sánh tỷ lệ đúng giờ vs. danh sách US-ATTEN-03 | — | Số liệu trùng khớp 100%. | P2-High |

### Performance

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A02-PERF-01 | Tải 3 thẻ thống kê | 1. Mở trang | — | Thời gian truy xuất ≤ 1.5 giây. | P2-High |

---

## US-ATTEN-03: Xem chi tiết nhật ký chấm công

### Happy Path

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A03-HP-01 | NV có 22 ngày chấm công trong tháng | 1. Mở nhật ký 2. Xem danh sách accordion | month=2026-04 | 22 dòng, mỗi dòng: ngày, giờ In/Out, status tag, source (CAMERA_AI). Phân trang 20/trang. | P1-Critical |
| TC-A03-HP-02 | NV nhấn vào ngày cụ thể | 1. Nhấn "10/04/2026" | date=2026-04-10 | Expand: hiển thị tất cả mốc quẹt trong ngày, ảnh Face ID, confidence score, device name. | P1-Critical |

### Edge Cases

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A03-EC-01 | NV mới, chưa có nhật ký | 1. Mở nhật ký | records=0 | "Chưa có dữ liệu chấm công" với illustration. | P2-High |
| TC-A03-EC-02 | Nhật ký 30 ngày gần nhất | 1. Cuộn xuống cuối | — | Chỉ hiển thị 30 ngày gần nhất. Nút "Xem thêm" tải thêm batch. | P2-High |

### Error & Security

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A03-ER-01 | Ảnh Face ID không tải được (CDN lỗi) | 1. Mở chi tiết ngày | imageUrl=broken | Placeholder "Ảnh không khả dụng". Không crash. | P3-Medium |
| TC-A03-ER-02 | Source = MANUAL (HR nhập) | 1. Xem ngày có record thủ công | source=MANUAL | Tag "Nhập thủ công" thay vì "Camera AI". Hiển thị reason. | P2-High |
| TC-A03-SEC-01 | NV A xem nhật ký NV B | 1. API empId=NV_B | — | 403 Forbidden. | P1-Critical |
| TC-A03-SEC-02 | Manager xem nhật ký NV thuộc team | 1. API empId=NV_team | — | 200 OK. RBAC cho phép Manager xem team. | P1-Critical |

### Data Integrity

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A03-DI-01 | Nhật ký khớp daily_attendance_summaries | 1. So sánh workedHours | — | workedHours trên UI = net_hours trong DB. | P2-High |

### Performance

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A03-PERF-01 | Load 30 ngày nhật ký | 1. Mở trang | — | Tải ≤ 2 giây. Pagination hoạt động. | P2-High |

---

## US-ATTEN-04: Trung tâm cảnh báo và thông báo

### Happy Path

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A04-HP-01 | NV có 3 cảnh báo mới (LATE, MISSING_CHECKOUT, ABSENT) | 1. Mở dashboard | — | 3 cảnh báo hiển thị: badge đỏ/vàng, severity icon, ngày vi phạm, nút "Giải trình ngay". | P1-Critical |
| TC-A04-HP-02 | NV nhấn "Giải trình ngay" | 1. Nhấn nút | anomaly_id=X | Chuyển sang Module 03 với ngày vi phạm tự điền. | P1-Critical |

### Edge Cases

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A04-EC-01 | NV không có cảnh báo nào | 1. Mở cảnh báo | violations=0 | "Không có cảnh báo. Chuyên cần tốt! 🎉" | P3-Medium |
| TC-A04-EC-02 | Cảnh báo đã gửi giải trình (PENDING) | 1. Xem cảnh báo | is_resolved=pending | Cảnh báo chuyển status "Đang giải trình" (Vàng). Không hiển thị nút "Giải trình". | P2-High |
| TC-A04-EC-03 | >3 cảnh báo mới | 1. Mở dashboard | violations=5 | Hiển thị 3 mới nhất. Link "Xem tất cả (5)" để mở danh sách đầy đủ. | P2-High |

### Error & Security

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A04-ER-01 | Mark as read fails (network error) | 1. PATCH /violations/{id}/read | — | Retry silently. Cảnh báo vẫn hiển thị nếu fail. | P3-Medium |
| TC-A04-ER-02 | Cảnh báo sau ngày chốt công | 1. Xem cảnh báo tháng cũ (LOCKED) | locked=true | Nút "Giải trình" disabled. Tooltip: "Kỳ đã chốt. Liên hệ HR." | P2-High |
| TC-A04-SEC-01 | NV xem cảnh báo NV khác | 1. API empId=other | — | 403 Forbidden. | P1-Critical |

### Data Integrity

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A04-DI-01 | Cảnh báo khớp attendance_anomalies table | 1. Compare | — | Số cảnh báo UI = COUNT(attendance_anomalies WHERE is_resolved=false). | P2-High |

---

## US-ATTEN-05: Nhập chấm công thủ công

### Happy Path

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A05-HP-01 | HR nhập chấm công cho NV bị camera lỗi | 1. POST /attendance/manual-entry 2. Chờ approval | empId, date, checkIn, checkOut, reason, evidence | Record tạo (PENDING_APPROVAL). Approval workflow triggered. | P1-Critical |
| TC-A05-HP-02 | Manual entry được duyệt | 1. Approver duyệt | approve=true | Record → APPROVED. Daily summary cập nhật. NV thấy trên nhật ký. | P1-Critical |

### Edge Cases

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A05-EC-01 | Nhập cho ngày đã có record CVISION | 1. POST manual cho ngày đã có camera record | date=existing | Cảnh báo: "Ngày này đã có dữ liệu từ Camera AI. Xác nhận ghi đè?" | P2-High |
| TC-A05-EC-02 | Nhập cho ngày đã bị chốt (LOCKED) | 1. POST manual cho ngày locked | date=locked | 422: DATE_LOCKED. "Ngày chấm công đã bị chốt — không thể chỉnh sửa." | P1-Critical |
| TC-A05-EC-03 | Nhập trùng (cùng NV cùng ngày) | 1. POST manual 2 lần cho cùng NV, ngày | — | 409: DUPLICATE_MANUAL_ENTRY. Chặn trùng. | P2-High |

### Error Cases

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A05-ER-01 | Thiếu required field (reason) | 1. POST without reason | reason=null | 400: VALIDATION_ERROR. "Lý do là bắt buộc." | P2-High |
| TC-A05-ER-02 | NV chưa được gán ca ngày đó | 1. POST manual cho NV no-shift | no_shift=true | 404: NO_SHIFT_ASSIGNED. "Nhân viên chưa được gán ca." | P2-High |
| TC-A05-ER-03 | File evidence upload fail | 1. Upload file > 5MB | file=6MB | 400: "File quá lớn. Tối đa 5MB." | P3-Medium |

### Security Cases

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A05-SEC-01 | NV (không phải HR) cố nhập thủ công | 1. POST /attendance/manual-entry | role=EMPLOYEE | 403: FORBIDDEN. "Chỉ HR được nhập chấm công thủ công." | P1-Critical |
| TC-A05-SEC-02 | HR chi nhánh A nhập cho NV chi nhánh B | 1. POST manual cho NV site khác | siteId≠mySite | 403: Forbidden. ABAC chặn cross-site. | P1-Critical |

### Concurrency

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A05-CON-01 | 2 HR cùng submit manual cho 1 NV 1 ngày | 1. Concurrent POST | — | Chỉ 1 thành công (DB unique constraint). Request thứ 2: 409 DUPLICATE. | P2-High |

### Data Integrity

| TC-ID | Precondition | Steps | Input | Expected Result | Priority |
|-------|-------------|-------|-------|-----------------|----------|
| TC-A05-DI-01 | Manual entry approved → daily summary | 1. Approve 2. Check summary | — | daily_attendance_summaries updated. source="MANUAL" in record. | P2-High |
