# US-ATTEN-05: Nhập chấm công thủ công (Manual Entry)

---

**AS A** HR Admin,  
**I WANT TO** nhập thủ công mốc chấm công cho nhân viên khi hệ thống C-Vision gặp sự cố hoặc NV không thể quét khuôn mặt,  
**SO THAT** dữ liệu chấm công được ghi nhận đầy đủ, đảm bảo quyền lợi lương cho NV và không thiếu công trong kỳ tính lương.

---

### **1. BUSINESS FLOW**

1. **Trigger**: Camera AI gặp sự cố (offline, confidence thấp) hoặc NV đặc biệt (khuyết tật, từ chối biometric).
2. **Tạo yêu cầu**: HR truy cập "Nhập chấm công thủ công" → Chọn NV → Chọn loại (CHECK_IN / CHECK_OUT) → Nhập ngày giờ + lý do.
3. **Xử lý hệ thống**: Hệ thống tạo `AttendanceRecord` với `status: PENDING_APPROVAL` và `source: MANUAL_ENTRY`.
4. **Phê duyệt**: Hệ thống tạo Approval workflow tự động → Đơn xuất hiện trong Inbox phê duyệt (Module 10).
5. **Kết quả**: 
   - APPROVED → Record chuyển `APPROVED`, cập nhật `DailyAttendanceSummary`, tính lại giờ làm.
   - REJECTED → Record chuyển `REJECTED`, không ảnh hưởng bảng công.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin | Role | Ghi chú |
| --- | --- | --- |
| Tạo Manual Entry | SITE_HR_ADMIN, GLOBAL_HR_ADMIN | Chỉ HR mới được nhập thủ công. Manager KHÔNG có quyền này. |
| Phê duyệt Manual Entry | SITE_HR (nếu người tạo ≠ người duyệt), GLOBAL_HR | Self-approve bị chặn (người tạo ≠ người duyệt). |
| Xem lịch sử Manual Entry | HR Admin, Manager (read-only team mình) | ABAC: Manager chỉ xem NV thuộc team. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Form nhập liệu**

- Dropdown chọn NV: tìm kiếm theo Mã NV, Họ tên (unaccent, case-insensitive). Chỉ hiển thị NV Active tại site hiện tại.
- Chọn loại: CHECK_IN hoặc CHECK_OUT.
- Date picker: chỉ cho phép chọn ngày trong phạm vi **30 ngày trở lại** (không cho nhập tương lai).
- Time picker: HH:MM (24h format).
- Lý do (bắt buộc): Textarea ≥ 20 ký tự. Dropdown gợi ý: "Camera lỗi", "NV từ chối biometric", "Mất điện", "Khác".
- File đính kèm (tùy chọn): Ảnh/PDF ≤ 5MB (email xác nhận, ảnh chụp NV tại văn phòng).

#### **AC2. Validation**

- **Trùng mốc**: Không cho nhập nếu NV đã có AttendanceRecord tại cùng ngày/giờ ± 30 phút. Hiển thị: "NV đã có mốc chấm công lúc [HH:MM]. Sử dụng chức năng Điều chỉnh nếu cần sửa."
- **Check-out trước Check-in**: Nếu loại = CHECK_OUT mà NV chưa có CHECK_IN trong ngày → Cảnh báo: "NV chưa có mốc Check-in hôm nay."
- **Ngoài ca làm việc**: Nếu giờ nhập nằm ngoài Shift ± punch limit → Cảnh báo (không chặn): "Giờ nhập nằm ngoài khung ca làm việc."

#### **AC3. Audit Trail**

- Mỗi Manual Entry phải ghi nhận: `created_by`, `created_at`, `reason`, `approval_status`, `approved_by`, `approved_at`.
- Source field = `MANUAL_ENTRY` (phân biệt với `C_VISION`).
- Hiển thị icon "✋ Thủ công" trên nhật ký chấm công của NV (US-ATTEN-03) để phân biệt với mốc tự động.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| AT05-E1 | **HR nhập cho NV đã nghỉ việc** — NV status TERMINATED | HIGH | Chặn: "NV [Tên] đã nghỉ việc từ [DD/MM]. Không thể tạo chấm công." |
| AT05-E2 | **HR nhập cho NV khác site** — NV thuộc Site B, HR is Site A | HIGH | Chặn: "NV thuộc chi nhánh [Site B]. Bạn chỉ có quyền nhập cho NV tại [Site A]." GLOBAL_HR không bị giới hạn. |
| AT05-E3 | **Batch manual entry** — Camera offline 2h, cần nhập cho 100 NV | MEDIUM | Hỗ trợ upload Excel: Mã NV, Loại, Giờ, Lý do. Validate từng dòng. Tạo batch approval. |
| AT05-E4 | **Manual Entry trùng C-Vision record** — Camera recover sau 30 phút, gửi webhook delayed | MEDIUM | De-duplication: nếu C-Vision record xuất hiện sau Manual Entry ± 30 phút → giữ Manual Entry (đã approved). Log: "Skipped C-Vision record (duplicate with Manual Entry [ID])." |

---

### **DEFINITION OF DONE (DOD)**

1. **AC Verified**: Tất cả Acceptance Criteria pass QA testing.
2. **RBAC Enforced**: Self-approve bị chặn; Site-scope enforced cho SITE_HR.
3. **Audit Trail**: Mọi Manual Entry có đầy đủ log (created_by, reason, approval chain).
4. **Edge Cases Tested**: Tất cả edge cases pass.
5. **Integration**: Record Manual Entry hiển thị đúng trên US-ATTEN-01 (Hub) và US-ATTEN-03 (Nhật ký).
