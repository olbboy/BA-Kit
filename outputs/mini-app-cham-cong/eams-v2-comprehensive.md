# TÀI LIỆU NGHIỆP VỤ TOÀN DIỆN - EAMS
# Hệ thống Quản lý Chấm công Doanh nghiệp

**Phiên bản:** 2.0
**Ngày cập nhật:** 17/03/2026
**Trạng thái:** Production Ready

---

## MỤC LỤC

1. [Tổng quan dự án](#1-tổng-quan-dự-án)
2. [Mô hình tổ chức & phân quyền](#2-mô-hình-tổ-chức--phân-quyền)
3. [Luồng nghiệp vụ chấm công](#3-luồng-nghiệp-vụ-chấm-công)
4. [Quản lý ca làm việc](#4-quản-lý-ca-làm-việc)
5. [Quản lý tăng ca](#5-quản-lý-tăng-ca)
6. [Quản lý nghỉ phép](#6-quản-lý-nghỉ-phép)
7. [Quy trình phê duyệt](#7-quy-trình-phê-duyệt)
8. [Tích hợp C-Vision](#8-tích-hợp-c-vision)
9. [Dashboard & báo cáo](#9-dashboard--báo-cáo)
10. [Ngày chốt công](#10-ngày-chốt-công-closing-date)
11. [Hệ thống thông báo](#11-hệ-thống-thông-báo)
12. [Đăng ký khuôn mặt (Face ID)](#12-đăng-ký-khuôn-mặt-face-id-enrollment)
13. [Cấu hình chính sách phép năm](#13-cấu-hình-chính-sách-phép-năm-leave-policy)
14. [Quản trị hệ thống](#14-quản-trị-hệ-thống)
15. [Tuân thủ pháp luật Việt Nam](#15-tuân-thủ-pháp-luật-việt-nam)
16. [Ma trận quyền hạn](#16-ma-trận-quyền-hạn)
17. [Cross-module edge cases & policies](#17-cross-module-edge-cases--policies)

---

## 1. TỔNG QUAN DỰ ÁN

### 1.1 Mục tiêu

EAMS (Enterprise Attendance Management System) là hệ thống quản lý chấm công doanh nghiệp quy mô lớn, tích hợp C-Vision Face Recognition. Hệ thống phục vụ:

- **5,000+ nhân viên** đồng thời trên nhiều chi nhánh
- **Tuân thủ** Luật Lao động Việt Nam & Nghị định 13/2023/NĐ-CP
- **Tích hợp payroll** với MISA, SAP, Oracle HCM
- **Multi-tenant**: nhiều tổ chức dùng chung hệ thống, dữ liệu cách ly hoàn toàn
- **Multi-site**: mỗi tổ chức có nhiều chi nhánh/văn phòng

### 1.2 Phạm vi hệ thống

**TRONG PHẠM VI:**
- Tiếp nhận dữ liệu chấm công từ C-Vision Face Recognition (nguồn chính)
- Nhập chấm công thủ công (Manual Entry) - phương thức dự phòng
- Quản lý ca làm việc, tăng ca, nghỉ phép
- Quy trình phê duyệt đa cấp theo chi nhánh
- Báo cáo tổng hợp và xuất dữ liệu payroll (Excel/CSV)
- Ứng dụng web và mobile (xem thông tin, không chấm công qua mobile)

**NGOÀI PHẠM VI:**
- Hệ thống C-Vision Face Recognition (đối tác cung cấp)
- Các phương thức chấm công khác (vân tay, thẻ từ, QR code)
- Module tính lương chi tiết
- Quản lý hợp đồng lao động

### 1.3 Nguồn dữ liệu chấm công

| Nguồn | Mô tả | Tự động | Phê duyệt |
|-------|-------|---------|------------|
| C-Vision Face Recognition | Camera nhận diện khuôn mặt tại cổng vào/ra | Có | Tự động APPROVED |
| Manual Entry | HR/Manager nhập khi C-Vision lỗi hoặc NV từ chối biometric | Không | Cần phê duyệt |

### 1.4 Các bên liên quan

| Vai trò | Mô tả | Quyền hạn chính |
|---------|-------|-----------------|
| EMPLOYEE | Nhân viên | Xem chấm công cá nhân, tạo yêu cầu nghỉ phép/OT/điều chỉnh |
| MANAGER | Quản lý trực tiếp | Phê duyệt yêu cầu của team trực thuộc |
| DEPT_HEAD | Trưởng phòng ban | Phê duyệt cấp 2, xem báo cáo phòng ban |
| SITE_MANAGER | Quản lý chi nhánh | Xem báo cáo toàn chi nhánh |
| SITE_HR_ADMIN | HR chi nhánh | Quản lý NV chi nhánh, nhập thủ công, cấu hình phê duyệt |
| GLOBAL_HR_ADMIN | HR tổng | Quản lý NV toàn hệ thống, báo cáo tổng hợp |
| SYSTEM_ADMIN | Quản trị viên | Cấu hình hệ thống, quản lý tenant/site |
| SUPER_ADMIN | Siêu quản trị | Toàn quyền không giới hạn |

---

## 2. MÔ HÌNH TỔ CHỨC & PHÂN QUYỀN

### 2.1 Cấu trúc tổ chức

```
Organization (Tenant) ─── VD: Công ty ABC
├─ Site A (Chi nhánh HCM)
│  ├─ Phòng Kỹ thuật
│  │  ├─ Trưởng phòng (DEPT_HEAD)
│  │  ├─ Quản lý nhóm 1 (MANAGER)
│  │  │  ├─ NV1 (EMPLOYEE)
│  │  │  └─ NV2 (EMPLOYEE)
│  │  └─ Quản lý nhóm 2 (MANAGER)
│  │     └─ NV3 (EMPLOYEE)
│  ├─ Phòng Kinh doanh
│  │  └─ ...
│  ├─ HR chi nhánh (SITE_HR_ADMIN)
│  └─ Quản lý chi nhánh (SITE_MANAGER)
│
├─ Site B (Chi nhánh Hà Nội)
│  ├─ Phòng Kỹ thuật
│  ├─ HR chi nhánh (SITE_HR_ADMIN)
│  └─ Quản lý chi nhánh (SITE_MANAGER)
│
└─ HR Tổng công ty (GLOBAL_HR_ADMIN, scope: ALL_SITES)
```

### 2.2 Phân quyền theo site (Multi-Site)

Mỗi user có thể có **vai trò khác nhau** tại **các chi nhánh khác nhau**:

| User | Site A | Site B | Scope |
|------|--------|--------|-------|
| Nguyễn Văn A | MANAGER | - | SITE |
| Trần Thị B | SITE_HR_ADMIN | SITE_HR_ADMIN | SITE (mỗi site) |
| Lê Văn C | GLOBAL_HR_ADMIN | GLOBAL_HR_ADMIN | ALL_SITES |

- **Scope SITE**: quyền chỉ áp dụng tại 1 chi nhánh cụ thể
- **Scope ALL_SITES**: quyền áp dụng tại tất cả chi nhánh

### 2.3 Nhân viên thuộc nhiều chi nhánh

Một nhân viên có thể được assign vào nhiều chi nhánh (VD: nhân viên IT hỗ trợ nhiều site):

| Nhân viên | Site A | Site B | Primary |
|-----------|--------|--------|---------|
| NV IT-01 | ACTIVE | ACTIVE | Site A |
| NV Sales-01 | ACTIVE | - | Site A |
| NV Sales-02 | TRANSFERRED | ACTIVE | Site B |

- **Primary Site**: chi nhánh chính của nhân viên
- **Status**: ACTIVE / INACTIVE / TRANSFERRED

---

## 3. LUỒNG NGHIỆP VỤ CHẤM CÔNG

### 3.1 Chấm công tự động (C-Vision)

```
NV đến công ty → Camera nhận diện khuôn mặt
                        ↓
              C-Vision gửi webhook đến EAMS
                        ↓
              EAMS xác thực signature (HMAC-SHA256)
                        ↓
              Kiểm tra idempotency (tránh xử lý trùng)
                        ↓
              Kiểm tra confidence score ≥ 0.85
                        ↓   (< 0.85 → đánh dấu failed, cần HR review)
              Mapping: C-Vision personId → Employee
                        ↓   (không tìm thấy → failed, cần tạo mapping)
              Xác định hướng: CHECK_IN hay CHECK_OUT
                        ↓
              Tạo AttendanceRecord (status: APPROVED)
                        ↓
              Cập nhật DailyAttendanceSummary
                        ↓
              Tính toán: giờ làm, OT, đi trễ/về sớm
```

**Xác định hướng (Direction Detection)** - theo thứ tự ưu tiên:
1. **Cấu hình thiết bị**: Camera cổng vào = IN_ONLY, cổng ra = OUT_ONLY
2. **Tên thiết bị**: chứa "entrance/vào/checkin" = IN, chứa "exit/ra/checkout" = OUT
3. **Xen kẽ**: nếu lần cuối là CHECK_IN → lần này CHECK_OUT, và ngược lại

### 3.2 Chấm công thủ công (Manual Entry)

```
HR/Manager tạo yêu cầu nhập thủ công
  ├─ Chọn nhân viên, loại (CHECK_IN/CHECK_OUT)
  ├─ Nhập thời gian và lý do
  └─ Gửi yêu cầu
        ↓
Tạo AttendanceRecord (status: PENDING_APPROVAL)
        ↓
Hệ thống tạo Approval workflow tự động
        ↓
Quản lý phê duyệt
  ├─ APPROVED → Record chuyển APPROVED, cập nhật summary
  └─ REJECTED → Record chuyển REJECTED
```

### 3.3 Điều chỉnh chấm công (Correction)

Nhân viên có thể yêu cầu sửa chấm công sai:

| Loại điều chỉnh | Mô tả | Ví dụ |
|-----------------|-------|-------|
| ADD | Thêm record mới | Quên check-out |
| MODIFY | Sửa thời gian | Check-in sai giờ |
| DELETE | Xóa record | Check-in nhầm |

```
NV tạo yêu cầu điều chỉnh + lý do + file đính kèm (nếu có)
        ↓
Tạo AttendanceCorrection (status: PENDING)
        ↓
Approval workflow theo cấu hình site
        ↓
  ├─ APPROVED → Áp dụng điều chỉnh, recalculate summary
  └─ REJECTED → Giữ nguyên record gốc
```

### 3.4 Công thức tính giờ làm việc

| Loại giờ | Công thức | Ví dụ |
|----------|-----------|-------|
| Gross Hours | SUM(CheckOut - CheckIn) cho mỗi cặp | 17:30 - 08:00 = 9.5h |
| Break Hours | Tổng giờ nghỉ không lương trong ca | Nghỉ trưa 12:00-13:00 = 1h |
| Net Hours | Gross - Break | 9.5 - 1.0 = 8.5h |
| Regular Hours | MIN(Net, WorkingHours ca) | MIN(8.5, 8.0) = 8.0h |
| Overtime Hours | MAX(0, Net - WorkingHours) | MAX(0, 8.5 - 8.0) = 0.5h |
| Night Hours | Giao thời gian làm với 22:00-06:00 | Tính phút overlap |
| Late Minutes | MAX(0, FirstCheckIn - ShiftStart - GracePeriod) | 08:20 - 08:00 - 15min = 5min |
| Early Leave | MAX(0, ShiftEnd - LastCheckOut) | 17:30 - 17:00 = 30min |

### 3.5 Trạng thái chấm công hàng ngày

| Status | Điều kiện |
|--------|-----------|
| PRESENT | Có check-in, không trễ, không về sớm |
| LATE | Late Minutes > 0 |
| EARLY_LEAVE | Early Leave Minutes > 0 |
| LATE_AND_EARLY | Cả trễ và về sớm |
| ABSENT | Không có record nào trong ngày |
| ON_LEAVE | Có đơn nghỉ phép APPROVED |
| HOLIDAY | Ngày lễ |
| WEEKEND | Thứ 7 / Chủ nhật |

---

## 4. QUẢN LÝ CA LÀM VIỆC

### 4.1 Loại ca

| Loại ca | Mô tả | Ví dụ |
|---------|-------|-------|
| FIXED | Ca cố định | 08:00 - 17:00 |
| FLEXIBLE | Ca linh hoạt (core hours) | 10:00-15:00 core, ±2h linh hoạt |
| ROTATING | Ca xoay | Sáng/Chiều/Đêm luân phiên |
| SPLIT | Ca chia (2 buổi) | 08:00-12:00, 14:00-18:00 |
| FREE | Tự do | Chỉ cần đủ giờ/ngày |

### 4.2 Cấu hình ca

| Thuộc tính | Mô tả | Mặc định |
|------------|-------|----------|
| startTime / endTime | Giờ bắt đầu/kết thúc | - |
| workingHours | Số giờ làm | - |
| gracePeriodMinutes | Thời gian ân hạn (không tính trễ) | 15 phút |
| earlyCheckInMinutes | Cho phép check-in sớm | 30 phút |
| lateCheckOutMinutes | Check-out muộn tối đa | 120 phút |
| breaks | Danh sách nghỉ giải lao [{ startTime, endTime, isPaid }] | [] |
| autoDetectOvertime | Tự động phát hiện OT | true |
| requireOvertimeApproval | OT cần phê duyệt | true |
| isNightShift | Ca đêm | false |

### 4.3 Phân ca

**Phân theo ngày**: assign 1 ca cho 1 NV tại 1 ngày cụ thể (unique constraint: tenant + employee + date)

**Phân theo pattern**: VD ca xoay ["MORNING", "AFTERNOON", "NIGHT", "OFF"] lặp lại trong khoảng ngày

```
Pattern: [CA_SANG, CA_CHIEU, CA_DEM, OFF]
  Thứ 2: CA_SANG
  Thứ 3: CA_CHIEU
  Thứ 4: CA_DEM
  Thứ 5: OFF
  Thứ 6: CA_SANG  (lặp lại)
  ...
```

---

## 5. QUẢN LÝ TĂNG CA

### 5.1 Hệ số tăng ca (theo Luật Lao động VN)

| Loại ngày | Hệ số | Mô tả |
|-----------|--------|-------|
| WEEKDAY | 1.5x | Ngày thường |
| WEEKEND | 2.0x | Thứ 7, Chủ nhật |
| HOLIDAY | 3.0x | Ngày lễ, tết |

### 5.2 Giới hạn OT (Luật Lao động VN - Nghị định 13/2023)

| Chu kỳ | Giới hạn mặc định | Giới hạn mở rộng |
|--------|-------------------|-------------------|
| Ngày | 4 giờ | - |
| Tuần | 12 giờ | - |
| Tháng | 40 giờ | - |
| Năm | 200 giờ | 300 giờ (cần phê duyệt đặc biệt) |

**Cảnh báo**: khi sử dụng ≥ 80% giới hạn → cảnh báo cho HR/Manager

### 5.3 Luồng yêu cầu tăng ca

```
Nguồn 1: NV tạo yêu cầu OT trước (PRE_APPROVED)
Nguồn 2: NV tạo sau khi đã OT (POST_APPROVED)
Nguồn 3: Hệ thống tự phát hiện OT từ chấm công (AUTO_DETECTED)
        ↓
Kiểm tra giới hạn OT (ngày/tuần/tháng/năm)
  ├─ Vượt giới hạn → TỪ CHỐI + thông báo lý do
  └─ Trong giới hạn → Tiếp tục
        ↓
Tính hệ số: weekday=1.5x, weekend=2.0x, holiday=3.0x
        ↓
Tạo OvertimeRequest (status: PENDING)
        ↓
Approval workflow theo cấu hình site
        ↓
  ├─ APPROVED → Ghi nhận OT, cập nhật summary
  └─ REJECTED → OT không được tính
```

**Ràng buộc DB**: Chỉ 1 request OT ACTIVE (PENDING/APPROVED) cho mỗi NV mỗi ngày (partial unique index).

---

## 6. QUẢN LÝ NGHỈ PHÉP

### 6.1 Loại nghỉ phép

| Loại | Ngày/năm | Trả lương | Cần phê duyệt | Cần file đính kèm | Báo trước |
|------|----------|-----------|----------------|--------------------| ----------|
| ANNUAL (Phép năm) | 12 | Có | Có | Không | 3 ngày |
| SICK (Ốm) | 30 | Có | Có | Có | - |
| MATERNITY (Thai sản) | 180 | Có | Có | Có | 30 ngày |
| PATERNITY (Cha) | 7 | Có | Có | Có | - |
| MARRIAGE (Kết hôn) | 3 | Có | Có | Không | - |
| BEREAVEMENT (Tang) | 3 | Có | Có | Không | - |
| UNPAID (Không lương) | Tùy chỉnh | Không | Có | Không | - |
| COMPENSATORY (Bù) | Tùy chỉnh | Có | Có | Không | - |

### 6.2 Tính phép năm (Vietnam Labor Law)

```
Phép cơ bản: 12 ngày/năm (hoặc theo policy công ty)

Thâm niên: +1 ngày mỗi 5 năm làm việc
  VD: 7 năm → 12 + 1 = 13 ngày

Nhân viên mới (chưa đủ 12 tháng):
  Phép = (entitlement × số_tháng_làm) / 12
  VD: vào tháng 7, phép năm = (12 × 6) / 12 = 6 ngày

Chuyển tiếp (Carryover):
  - Tối đa 5 ngày phép chưa dùng → chuyển sang năm sau
  - Hết hạn sau 31/03 năm mới
  VD: năm 2025 dư 8 ngày → chuyển 5 ngày → dùng trước 31/03/2026
```

### 6.3 Luồng yêu cầu nghỉ phép

```
NV tạo đơn nghỉ phép
  ├─ Chọn loại, ngày bắt đầu/kết thúc, nửa ngày (AM/PM)
  ├─ Nhập lý do, đính kèm file (nếu bắt buộc)
  └─ Gửi yêu cầu
        ↓
Hệ thống tính số ngày làm việc (trừ T7/CN và ngày lễ)
        ↓
Kiểm tra số dư phép (pessimistic lock để tránh race condition)
  ├─ Không đủ phép → TỪ CHỐI
  └─ Đủ phép → Tiếp tục
        ↓
Kiểm tra trùng ngày nghỉ (DB exclusion constraint)
  ├─ Trùng → TỪ CHỐI
  └─ Không trùng → Tiếp tục
        ↓
Tạo LeaveRequest (status: PENDING)
Cập nhật: balance.pending += workingDays
        ↓
Approval workflow
  ├─ APPROVED → balance.used += days, balance.pending -= days
  └─ REJECTED → balance.pending -= days, refund
```

**Ràng buộc DB**: PostgreSQL EXCLUSION constraint ngăn chặn nghỉ phép trùng ngày ở cấp database (dùng daterange + GiST index). Đây là lớp bảo vệ cuối cùng ngoài validation ở application layer.

---

## 7. QUY TRÌNH PHÊ DUYỆT

### 7.1 Các loại yêu cầu cần phê duyệt

| Loại yêu cầu | Mô tả |
|--------------|-------|
| LEAVE | Yêu cầu nghỉ phép |
| OT_REQUEST | Yêu cầu tăng ca |
| CORRECTION | Điều chỉnh chấm công |
| MANUAL_ATTENDANCE | Nhập chấm công thủ công |

### 7.2 Chuỗi phê duyệt (Approval Chain)

Mỗi chi nhánh có cấu hình phê duyệt riêng:

```
Ví dụ: Leave Request tại Site A
  Level 1: DIRECT_MANAGER (quản lý trực tiếp)
  Level 2: DEPT_HEAD (trưởng phòng) [nếu > 3 ngày]
  Level 3: SITE_HR (HR chi nhánh) [nếu > 5 ngày]

Ví dụ: OT Request tại Site B
  Level 1: DIRECT_MANAGER
  Level 2: SITE_MANAGER [nếu > 8 giờ]
```

### 7.3 Xác định người phê duyệt (Approver Resolution)

Hệ thống tự động xác định người phê duyệt dựa trên:

| Loại approver | Cách xác định |
|--------------|---------------|
| DIRECT_MANAGER | Employee.managerId (quan hệ trực tiếp) |
| DEPT_HEAD | Trưởng phòng ban của NV |
| SITE_MANAGER | User có role SITE_MANAGER tại site |
| SITE_HR | User có role SITE_HR_ADMIN tại site |
| GLOBAL_HR | User có role GLOBAL_HR_ADMIN, scope ALL_SITES |

**Chuỗi dự phòng (Fallback)**: nếu người phê duyệt chính không có quyền tại site:

```
DIRECT_MANAGER → SITE_MANAGER → SITE_HR → GLOBAL_HR
DEPT_HEAD → SITE_MANAGER → SITE_HR → GLOBAL_HR
SITE_MANAGER → SITE_HR → GLOBAL_HR
SITE_HR → GLOBAL_HR
```

### 7.4 Trạng thái phê duyệt

```
PENDING (chờ) ──→ APPROVED (chấp thuận)
      │                     ↓
      ├──→ REJECTED     Nếu multi-level:
      │   (từ chối)     Level 1 APPROVED → Level 2 PENDING → ...
      └──→ CANCELLED    Tất cả levels APPROVED → Final APPROVED
          (hủy bởi NV)
```

### 7.5 Sự kiện sau phê duyệt

| Loại yêu cầu | Khi APPROVED | Khi REJECTED |
|--------------|-------------|-------------|
| Leave | Trừ phép, cập nhật balance | Hoàn phép pending |
| OT | Ghi nhận giờ OT | Không tính OT |
| Correction | Áp dụng điều chỉnh, recalculate | Giữ nguyên gốc |
| Manual Entry | Record → APPROVED | Record → REJECTED |

---

## 8. TÍCH HỢP C-VISION

### 8.1 Tổng quan

C-Vision là hệ thống nhận diện khuôn mặt của đối tác. EAMS nhận dữ liệu qua webhook:

```
C-Vision Camera → Webhook → EAMS Queue (BullMQ) → Processor → AttendanceRecord
```

### 8.2 Dữ liệu webhook

```json
{
  "id": "notif-001",
  "personId": "person-123",
  "personName": "Nguyen Van A",
  "deviceId": "camera-001",
  "deviceName": "Cong vao - Tang 1",
  "recognitionTime": "2026-03-17T08:00:15Z",
  "confidence": 0.95,
  "capturedImageUrl": "/ai/proxy-image?key=captures/face-001.jpg"
}
```

### 8.3 Pipeline xử lý

| Bước | Hành động | Xử lý lỗi |
|------|----------|-----------|
| 1 | Xác thực signature HMAC-SHA256 | Reject webhook |
| 2 | Kiểm tra idempotency (Redis) | Skip nếu đã xử lý |
| 3 | Tìm tenant từ deviceId | Failed: device chưa đăng ký |
| 4 | Tải cấu hình device (site, threshold) | Failed: device không tồn tại |
| 5 | Kiểm tra confidence ≥ threshold | Failed: cần HR review |
| 6 | Mapping personId → employeeId | Failed: cần tạo mapping |
| 7 | Xác định CHECK_IN/CHECK_OUT | Dùng thuật toán xen kẽ |
| 8 | Tạo attendance record (circuit breaker) | Retry hoặc fallback |
| 9 | Cập nhật device lastEventTime | Log error |

### 8.4 Quản lý thiết bị

| Thuộc tính | Mô tả |
|------------|-------|
| deviceId | ID trong hệ thống C-Vision |
| siteId | Chi nhánh lắp đặt |
| directionType | IN_ONLY / OUT_ONLY / BIDIRECTIONAL |
| confidenceThreshold | Ngưỡng tin cậy (mặc định 0.85) |
| status | ACTIVE / INACTIVE |

### 8.5 Mapping nhân viên

C-Vision dùng `personId` riêng. EAMS duy trì bảng mapping:

```
CVisionPersonMapping:
  cvisionPersonId  ←→  employeeId + employeeCode
```

HR có thể bulk-create mapping từ danh sách NV hiện có.

---

## 9. DASHBOARD & BÁO CÁO

### 9.1 Dashboard tổng quan

| Metric | Nguồn dữ liệu | Mô tả |
|--------|---------------|-------|
| Tổng NV | EmployeeAggregator | Số NV active |
| Có mặt | AttendanceAggregator | PRESENT + EARLY_LEAVE hôm nay |
| Đi trễ | AttendanceAggregator | LATE + LATE_AND_EARLY |
| Vắng mặt | Tính toán | Tổng - Có mặt - Nghỉ phép - Chưa check-in |
| Nghỉ phép | LeaveAggregator | Đơn APPROVED trùng hôm nay |
| Chờ phê duyệt | ApprovalAggregator | PENDING của user hiện tại |
| Xu hướng 7 ngày | AttendanceAggregator | Biểu đồ status theo ngày |

### 9.2 Các loại báo cáo

| Báo cáo | Nội dung | Lọc theo |
|---------|---------|---------|
| **Báo cáo ngày** | Check-in/out, giờ làm, trạng thái mỗi NV | Ngày, phòng ban |
| **Bảng chấm công tháng** | Lưới ngày × NV, tổng hợp tháng | Tháng/năm, phòng ban |
| **Báo cáo OT** | Giờ OT theo loại ngày, hệ số, giờ quy đổi | Tháng/năm, phòng ban |
| **Báo cáo nghỉ phép** | Loại phép, ngày nghỉ, số ngày, lý do | Khoảng ngày, phòng ban |
| **Xuất payroll** | Tổng hợp: ngày công, nghỉ phép, OT cho tính lương | Tháng/năm, phòng ban |

### 9.3 Xuất dữ liệu Payroll

Format: Excel (.xlsx) và CSV

Các cột trong file payroll:

| # | Cột | Mô tả |
|---|-----|-------|
| 1 | Mã NV | employeeCode |
| 2 | Họ tên | fullName |
| 3 | Phòng ban | departmentName |
| 4 | Ngày công | Số ngày có mặt |
| 5 | Nghỉ phép (có lương) | Ngày nghỉ có lương |
| 6 | Nghỉ không lương | Ngày nghỉ không lương |
| 7 | Giờ làm thường | Regular hours |
| 8 | OT ngày thường | Giờ OT × 1.5 |
| 9 | OT cuối tuần | Giờ OT × 2.0 |
| 10 | OT ngày lễ | Giờ OT × 3.0 |
| 11 | Số ngày đi trễ | Late count |
| 12 | Số ngày về sớm | Early leave count |
| 13 | Tổng phút đi trễ | Sum late minutes |

### 9.4 Báo cáo cá nhân (Employee Self-Service)

Nhân viên xem trực tiếp trên Mini App:

| Chỉ số | Công thức | Cập nhật |
|--------|-----------|---------|
| Score chuyên cần | (Ngày đúng giờ / Tổng ngày làm) × 100 | Real-time |
| Tổng giờ làm tháng | SUM(netHours) | Real-time |
| Tổng ngày nghỉ | COUNT(LeaveRequest APPROVED) | Khi đơn duyệt |
| Giờ OT lũy kế | SUM(approvedOTHours) | Khi đơn duyệt |
| Biểu đồ trend | Score theo tuần (4 điểm) | Cuối mỗi tuần |
| KPI Highlights quý | So sánh quý hiện tại vs quý trước | Cuối mỗi quý |

**Scope dữ liệu:** NV chỉ xem dữ liệu cá nhân (ABAC: User_ID). Trung bình phòng ban hiển thị ẩn danh.

### 9.5 Cảnh báo vi phạm

Hệ thống quét cuối mỗi ngày, so khớp chấm công thực tế với lịch phân ca:

| Loại vi phạm | Điều kiện | Hiển thị |
|-------------|----------|---------|
| ĐI MUỘN (LATE) | CheckIn > ShiftStart + GracePeriod | Badge đỏ + số phút trễ |
| VỀ SỚM (EARLY) | CheckOut < ShiftEnd | Badge đỏ + số phút sớm |
| THIẾU QUẸT (MISSING) | Chỉ có CheckIn, không có CheckOut sau 24h | Badge vàng "Quên check-out" |
| VẮNG MẶT (ABSENT) | Không có record nào + không có đơn phép | Badge đỏ "Vắng không phép" |

- Cảnh báo hiển thị tối đa 3 mới nhất trên Dashboard NV
- Nút "Giải trình ngay" → chuyển sang Module 03 với ngày vi phạm tự điền
- Cảnh báo biến mất khi NV gửi đơn giải trình (PENDING)
- Push notification nhắc nhở 08:00 sáng hôm sau nếu chưa xử lý

### 9.6 Payroll Lock

Cơ chế khóa dữ liệu sau khi xuất payroll:

- **Khi HR xuất payroll:** Hệ thống đánh dấu kỳ lương "LOCKED" (tháng + site)
- **Sau LOCKED:** Mọi correction/approval → cảnh báo "Kỳ lương tháng X đã xuất"
- **Thay đổi sau lock:** Ghi nhận vào "Kỳ bổ sung" (supplementary payroll)
- **Re-export:** HR có thể xuất lại (tạo version mới, giữ lịch sử version cũ)

---

## 10. NGÀY CHỐT CÔNG (CLOSING DATE)

### 10.1 Định nghĩa

Ngày chốt công là mốc thời gian hàng tháng, sau đó:
- Dữ liệu chấm công tháng cũ bị **khóa** (read-only)
- Đơn giải trình cho tháng cũ bị **vô hiệu hóa** (nút disabled)
- Vi phạm chưa giải trình chuyển thành **"VI PHẠM QUY CHẾ"** vĩnh viễn

### 10.2 Cấu hình

| Tham số | Mặc định | Mô tả |
|---------|----------|-------|
| closingDay | 25 | Ngày chốt (1-28) |
| closingScope | PER_SITE | Mỗi site cấu hình riêng |
| graceDays | 3 | Số ngày buffer sau chốt cho correction cuối cùng |
| weekendRule | PREV_WORKDAY | Nếu ngày chốt rơi vào T7/CN → đẩy về thứ 6 trước đó |

### 10.3 Exception Approval (sau chốt)

- Chỉ **GLOBAL_HR** hoặc **SYS_ADMIN** có quyền mở khóa (Unlock)
- Form: chọn NV + ngày + lý do ngoại lệ
- Giới hạn: tối đa 30 ngày sau chốt công
- Mọi Unlock ghi audit log immutable

---

## 11. HỆ THỐNG THÔNG BÁO

### 11.1 Kênh thông báo

| Kênh | Mô tả | Ưu tiên |
|------|-------|---------|
| App Push Notification | Thông báo đẩy trên điện thoại (Firebase/APNs) | 1 (chính) |
| Email | Gửi qua SMTP, cho đơn từ cần lưu trữ | 2 (dự phòng) |
| Popup Dashboard | Hiển thị trên giao diện web | 3 (bổ sung) |

**Fallback chain:** Push fail → Email → Popup → Dead letter queue + Admin alert.

### 11.2 Sự kiện kích hoạt (36 events)

| Nhóm | Ví dụ | Bắt buộc |
|------|-------|----------|
| Chấm công | Check-in/out thành công, nhận diện thất bại | Không |
| Đơn từ | Đơn được duyệt/từ chối, đơn mới cần duyệt | Có |
| Cảnh báo | Vi phạm quy chế, gần hạn chốt công, vượt OT | Có |
| Nhắc nhở | Nhắc chấm công đầu/cuối ca, lịch nghỉ lễ | Không |
| Hệ thống | Camera offline, batch job lỗi, security event | Có (Admin) |

**Thông báo bắt buộc:** NV không thể tắt (kết quả phê duyệt, kỷ luật lao động).

### 11.3 Policy gửi

| Policy | Mô tả | Mặc định |
|--------|-------|----------|
| Batching | Gom nhiều event cùng loại → 1 thông báo tổng hợp | 15 phút |
| Throttle | Tối đa N thông báo/giờ/NV | 20/giờ |
| Schedule | Chỉ gửi trong khung giờ (trừ khẩn cấp) | 07:00-22:00 |
| Night Shift | NV ca đêm exempt khỏi schedule restriction | ON |

---

## 12. ĐĂNG KÝ KHUÔN MẶT (FACE ID ENROLLMENT)

### 12.1 Quy trình 3 bước

```
Bước 1: Xác nhận thông tin cá nhân (read-only từ hệ thống)
    ↓
Bước 2: Chụp ảnh khuôn mặt
    ├─ Camera trước điện thoại
    ├─ Kiểm tra tự động: face detection, ánh sáng, góc, không che mặt
    └─ Tối đa 5 lần chụp lại/phiên
    ↓
Bước 3: Đồng bộ C-Vision
    ├─ Gửi ảnh → POST /persons → nhận personId
    ├─ Tự động tạo CVisionPersonMapping
    └─ NV có thể chấm công Face ID ngay lập tức
```

### 12.2 Trạng thái Enrollment

| Trạng thái | Mô tả |
|------------|-------|
| NOT_ENROLLED | NV chưa đăng ký |
| PENDING | Ảnh đã gửi, đang chờ C-Vision xử lý |
| ENROLLED | Thành công, NV chấm công được |
| FAILED | Thất bại, cho phép thử lại |
| RE_ENROLLMENT | HR yêu cầu đăng ký lại |

### 12.3 Bảo mật

- Ảnh truyền qua HTTPS
- Lưu trữ theo Data Retention Policy (90 ngày)
- Chỉ dùng cho mục đích chấm công (tuân thủ NĐ 13/2023)

---

## 13. CẤU HÌNH CHÍNH SÁCH PHÉP NĂM (LEAVE POLICY)

### 13.1 Tham số cấu hình

| Tham số | Mặc định | Mô tả |
|---------|----------|-------|
| baseEntitlement | 12 | Số ngày phép năm cơ bản |
| seniorityBonus | 1 ngày / 5 năm | Thâm niên cộng thêm |
| carryoverMax | 5 | Số ngày tối đa chuyển tiếp |
| carryoverExpiry | 31/03 | Hạn sử dụng carryover |
| proRataMethod | MONTHLY | Tính phép cho NV mới: (entitlement × months) / 12 |
| halfDayAllowed | true | Cho phép nghỉ nửa ngày (AM/PM) |

### 13.2 Batch Recalculate

- Khi HR thay đổi policy → chạy batch recalculate balance cho toàn bộ NV
- Hiển thị preview: "Thay đổi sẽ ảnh hưởng X NV. Balance trung bình thay đổi ±Y ngày."
- Yêu cầu confirm trước khi áp dụng
- Ghi audit log: policy cũ → policy mới

---

## 14. QUẢN TRỊ HỆ THỐNG

### 14.1 Quản lý chi nhánh (Site Management)

| Hành động | Mô tả |
|-----------|-------|
| Tạo site | Tên, Mã, Timezone, Ngày chốt công, Địa chỉ |
| Sửa site | Cập nhật thông tin (không đổi Mã sau khi có dữ liệu) |
| Deactivate | Vô hiệu hóa site khi thu hẹp. NV phải chuyển trước. |

### 14.2 Audit Log Viewer

- Xem toàn bộ nhật ký hoạt động: ai, làm gì, khi nào, dữ liệu thay đổi
- Filter: user, module, action (CREATE/UPDATE/DELETE), time range
- Export CSV cho compliance
- Retention: 3 năm

### 14.3 Phê duyệt hàng loạt (Batch Approve)

- Chọn nhiều đơn cùng loại → duyệt/từ chối 1 lần
- Giới hạn: tối đa 50 đơn/batch
- Xử lý tuần tự, không rollback đơn đã xử lý thành công
- Kết quả: hiển thị thành công/thất bại/chưa xử lý cho từng đơn

---

## 15. TUÂN THỦ PHÁP LUẬT VIỆT NAM

### 15.1 Luật Lao động 2019 & Nghị định 13/2023

| Quy định | Cách tuân thủ trong EAMS |
|----------|-------------------------|
| Phép năm 12 ngày + thâm niên | LeaveBalanceService tự động tính |
| OT tối đa 200h/năm (300h đặc biệt) | OTLimitService kiểm tra mỗi request |
| OT tối đa 4h/ngày | Kiểm tra trước khi tạo OT request |
| Hệ số OT ngày thường 1.5x | OTRulesEngine tự động áp dụng |
| Hệ số OT cuối tuần 2.0x | Tự động theo dayType |
| Hệ số OT ngày lễ 3.0x | Tự động kết hợp Holiday module |
| Thai sản 6 tháng | LeavePolicy: 180 ngày mặc định |
| Ngày lễ quốc gia | HolidayService seed tự động (Tết, 30/4, 1/5...) |

### 15.2 Ngày lễ Việt Nam (tự động seed)

| Ngày lễ | Ngày | Ghi chú |
|---------|------|---------|
| Tết Dương lịch | 01/01 | 1 ngày |
| Tết Nguyên Đán | Âm lịch | 5 ngày (29 tháng Chạp - 3 tháng Giêng) |
| Giỗ Tổ Hùng Vương | 10/3 Âm lịch | 1 ngày |
| Ngày Giải phóng | 30/04 | 1 ngày |
| Ngày Quốc tế Lao động | 01/05 | 1 ngày |
| Ngày Quốc khánh | 02/09 | 2 ngày (01-02/09) |

---

## 16. MA TRẬN QUYỀN HẠN

### 16.1 Quyền theo module

| Module/Hành động | EMPLOYEE | MANAGER | DEPT_HEAD | SITE_HR | SITE_MGR | GLOBAL_HR | SYS_ADMIN | SUPER |
|-------------------|----------|---------|-----------|---------|----------|-----------|-----------|-------|
| **Chấm công** | | | | | | | | |
| Xem chấm công cá nhân | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Xem chấm công team | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Nhập thủ công | - | - | - | ✓ | - | ✓ | ✓ | ✓ |
| **Nghỉ phép** | | | | | | | | |
| Tạo đơn nghỉ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Phê duyệt đơn | - | ✓ | ✓ | ✓ | - | ✓ | ✓ | ✓ |
| Cấu hình policy | - | - | - | ✓ | - | ✓ | ✓ | ✓ |
| **Tăng ca** | | | | | | | | |
| Tạo yêu cầu OT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Phê duyệt OT | - | ✓ | ✓ | ✓ | - | ✓ | ✓ | ✓ |
| Cấu hình giới hạn OT | - | - | - | - | - | ✓ | ✓ | ✓ |
| **Nhân viên** | | | | | | | | |
| Xem thông tin cá nhân | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Quản lý NV (CRUD) | - | - | - | ✓ | - | ✓ | ✓ | ✓ |
| Import NV (Excel) | - | - | - | ✓ | - | ✓ | ✓ | ✓ |
| **Báo cáo** | | | | | | | | |
| Xem báo cáo cá nhân | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Xem báo cáo team/phòng | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Xuất payroll | - | - | - | ✓ | - | ✓ | ✓ | ✓ |
| **Quản trị** | | | | | | | | |
| Quản lý ca | - | - | - | ✓ | - | ✓ | ✓ | ✓ |
| Quản lý phòng ban | - | - | - | ✓ | - | ✓ | ✓ | ✓ |
| Quản lý site | - | - | - | - | - | - | ✓ | ✓ |
| Quản lý ngày lễ | - | - | - | ✓ | - | ✓ | ✓ | ✓ |
| Audit log | - | - | - | - | - | - | ✓ | ✓ |
| Circuit breaker | - | - | - | - | - | - | ✓ | ✓ |

### 16.2 Phạm vi dữ liệu

| Vai trò | Dữ liệu được xem |
|---------|------------------|
| EMPLOYEE | Chỉ dữ liệu cá nhân |
| MANAGER | Team trực thuộc (employee.managerId = self) |
| DEPT_HEAD | Toàn phòng ban |
| SITE_HR / SITE_MANAGER | Toàn chi nhánh (siteId) |
| GLOBAL_HR | Tất cả chi nhánh (scope: ALL_SITES) |
| SYSTEM_ADMIN / SUPER_ADMIN | Toàn hệ thống |

---

## 17. CROSS-MODULE EDGE CASES & POLICIES

### 12.1 Employee Offboarding

Khi nhân viên nghỉ việc (status → TERMINATED):

| Hệ thống con | Hành động tự động |
|--------------|-------------------|
| Đơn PENDING (Leave/OT/Correction) | Auto-cancel tất cả. Push HR: "X đơn của [NV] đã tự động hủy do nghỉ việc". |
| Leave Balance | Freeze. Tính ngày phép chưa sử dụng → gửi Payroll module để quyết toán. |
| Shift Assignment | Remove từ ngày hiệu lực (terminationDate + 1). |
| C-Vision Mapping | Deactivate (soft delete). Webhook với personId cũ → ignored. |
| Approval Chain | Re-route đơn đang duyệt sang fallback. Remove khỏi approver pool. |
| Notification | Deactivate Push token. Gửi email cuối cùng: "Tài khoản đã bị vô hiệu hóa". |

### 12.2 Data Retention Policy

| Loại dữ liệu | Thời gian lưu | Cơ sở pháp lý |
|--------------|---------------|---------------|
| Attendance Records | 5 năm | Luật Lao động 2019 §12 |
| Ảnh Face ID (captures) | 90 ngày | NĐ 13/2023 về BVDL cá nhân |
| Audit Logs | 3 năm | Quy định nội bộ |
| Payroll Exports | 10 năm | Luật Kế toán |
| Leave/OT Requests | 3 năm | Quy định nội bộ |
| C-Vision Mapping | Xóa khi NV nghỉ việc + 90 ngày | NĐ 13/2023 |

Batch job dọn dẹp chạy 00:00 ngày 01 hàng tháng: xóa dữ liệu hết hạn retention.

### 12.3 System Failure & Recovery

| Scenario | Recovery Procedure |
|----------|-------------------|
| EAMS Backend down 2h (08:00-10:00) | C-Vision queue webhooks (Redis). Khi recovery → replay toàn bộ từ dead letter queue. BullMQ tự động xử lý backlog. |
| Database failover | PostgreSQL streaming replication. RTO < 5 phút. Không mất dữ liệu (RPO = 0). |
| Batch Job 00:01 fail | Per-employee transaction. Retry queue cho NV lỗi. Admin alert + manual retry button. |
| Push Service down | Exponential backoff retry → fallback Email → dead letter queue. |

### 12.4 Concurrent Modification Protection

| Conflict | Resolution |
|----------|-----------|
| HR sửa ca + NV gửi đơn đổi ca cùng lúc | Optimistic locking (version field trên ShiftAssignment). Ai save sau → nhận lỗi "Dữ liệu đã thay đổi, vui lòng tải lại". |
| 2 HR cùng approve 1 đơn | Pessimistic lock trên ApprovalStep. Người approve sau → nhận thông báo "Đơn đã được [Tên] xử lý". |
| NV hủy đơn + Manager approve cùng lúc | Approve có priority cao hơn. Nếu approve xong trước → NV nhận "Đơn đã được duyệt, không thể hủy". |

---

## PHỤ LỤC: THUẬT NGỮ

| Thuật ngữ | Tiếng Việt | Mô tả |
|-----------|-----------|-------|
| Tenant | Đơn vị thuê | Tổ chức sử dụng hệ thống |
| Site | Chi nhánh | Địa điểm làm việc |
| Shift | Ca làm việc | Khung giờ làm việc |
| Grace Period | Thời gian ân hạn | Phút cho phép trễ không tính |
| Carryover | Chuyển tiếp phép | Phép năm dư chuyển sang năm sau |
| Exclusion Constraint | Ràng buộc loại trừ | DB constraint ngăn dữ liệu trùng |
| Circuit Breaker | Ngắt mạch | Pattern ngăn lỗi lan truyền |
| Idempotency | Tính bình đẳng | Xử lý cùng request nhiều lần cho cùng kết quả |
| Pessimistic Lock | Khóa bi quan | Khóa DB row để tránh đọc/ghi đồng thời |
| CASL | - | Thư viện quản lý quyền (isomorphic authorization) |
