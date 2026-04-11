# US-SYS-06: Cấu hình Data Retention Policy

---

**AS A** System Admin,  
**I WANT TO** cấu hình chính sách lưu trữ dữ liệu (Data Retention Policy) cho từng loại dữ liệu trong hệ thống — bao gồm thời hạn lưu trữ, quy tắc xóa/archive, và cảnh báo compliance,  
**SO THAT** hệ thống tuân thủ quy định pháp luật Việt Nam (Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân), tiết kiệm chi phí lưu trữ, và có audit trail cho mọi thao tác xóa dữ liệu.

---

### **1. BUSINESS FLOW**

1. **Truy cập**: SYS_ADMIN mở "Quản trị hệ thống" → "Data Retention Policy".
2. **Xem hiện trạng**: Dashboard hiển thị danh sách data categories + retention hiện tại + dung lượng + compliance status.
3. **Cấu hình retention**: SYS_ADMIN chọn category → Thiết lập retentionDays, archivePolicy, purgePolicy.
4. **Preview impact**: Hệ thống hiển thị: "Policy mới sẽ ảnh hưởng X records (Y GB). Z records sẽ bị archive/purge."
5. **Apply**: Confirm → Cron job chạy hàng đêm để enforce retention.
6. **Audit**: Mọi thay đổi retention config và mọi thao tác purge/archive được ghi audit log immutable.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Xem retention dashboard | SYS_ADMIN, GLOBAL_HR | Read. |
| Cấu hình retention policy | SYS_ADMIN, SUPER_ADMIN | Chỉ admin cấp cao nhất. |
| Execute purge/archive thủ công | SUPER_ADMIN | Cần confirm 2 lần. Audit log bắt buộc. |
| Xem audit log retention changes | SYS_ADMIN | Truy vết mọi thay đổi. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Data Categories & Default Retention**

| Category | Data Types | Default Retention | Regulation |
| --- | --- | --- | --- |
| Attendance Records | attendance_records, daily_attendance_summaries | 5 năm | Luật LĐ VN Điều 12 |
| Leave & OT Requests | leave_requests, overtime_requests, shift_changes | 3 năm | Luật LĐ VN |
| Face ID Images | face_enrollments (ảnh khuôn mặt) | 90 ngày sau offboarding | NĐ 13/2023 (PDPA VN) |
| Audit Logs | audit_logs | 3 năm | BRD-04 §4 NFR |
| Notification Logs | notification_logs, notification_events | 1 năm | Internal policy |
| Payroll Exports | payroll_exports, payroll_periods | 10 năm | Luật Kế toán VN |
| Camera Webhooks | webhook_raw_logs | 30 ngày | Performance |
| Employee Data | employees (active) | Indefinite (while active) | — |
| Employee Data | employees (offboarded) | 3 năm sau offboarding | NĐ 13/2023 |

- Mỗi category có: retentionDays (hoặc INDEFINITE), archivePolicy (ARCHIVE_COLD / PURGE / NONE), scheduleFrequency (DAILY / WEEKLY / MONTHLY).

#### **AC2. Retention Configuration Dashboard**

- **Summary cards**: Tổng dung lượng DB, Dung lượng per category, Records sắp hết hạn (30 ngày tới).
- **Compliance indicator**: 🟢 Compliant / 🟡 Warning (sắp vi phạm) / 🔴 Non-compliant (giữ quá hạn hoặc xóa sớm).
- **Timeline visualization**: Biểu đồ Gantt hiển thị retention window cho mỗi category.

#### **AC3. Archive vs. Purge**

- **ARCHIVE_COLD**: Di chuyển dữ liệu sang cold storage (S3 Glacier / separate DB partition). Dữ liệu vẫn truy vấn được (latency cao hơn). Audit log ghi: "Archived X records to cold storage."
- **PURGE**: Xóa vĩnh viễn (hard delete). Không thể khôi phục. Cần confirm 2 lần + nhập reason. Audit log ghi: "Purged X records. Reason: [...]."
- **NONE**: Giữ indefinite. Chỉ áp dụng cho active employee data.

#### **AC4. Automated Enforcement (Cron Job)**

- Cron job chạy hàng đêm (02:00 AM server time).
- Xử lý batch: scan dữ liệu hết hạn → archive/purge theo policy.
- Report hàng ngày gửi SYS_ADMIN: "Đêm qua: X records archived, Y records purged, Z errors."
- **Safety**: Nếu purge > 10,000 records/ngày → Dừng + alert SYS_ADMIN để confirm thủ công.

#### **AC5. Legal Compliance Dashboard**

- Checklist compliance per regulation:
  - ☑️ NĐ 13/2023: Face ID data deleted within 90 days of offboarding
  - ☑️ Luật LĐ VN: Attendance records kept ≥ 5 years
  - ☑️ Luật Kế toán: Payroll data kept ≥ 10 years
- Auto-scan: Hệ thống quét hàng ngày. Nếu phát hiện vi phạm → Alert SUPER_ADMIN + GLOBAL_HR.
- Export compliance report (PDF) cho external audit.

---

### **4. DEFINITION OF DONE (DOD)**

1. **9 categories**: Tất cả data categories có retention config mặc định.
2. **Cron job**: Chạy đúng lịch. Archive/Purge đúng policy. Không mất dữ liệu ngoài ý muốn.
3. **Compliance**: Dashboard hiển thị đúng status. Alert khi vi phạm.
4. **Audit**: Mọi thay đổi config + mọi thao tác purge/archive có audit log immutable.
5. **QA**: Kiểm thử: sửa retention → cron chạy → data bị archive/purge đúng → audit log ghi → compliance dashboard cập nhật.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SY06-E1 | **Purge nhầm dữ liệu active** — Bug tính retention | CRITICAL | Safety: soft-delete trước, hard-delete sau 7 ngày. SYS_ADMIN có 7 ngày để rollback. |
| SY06-E2 | **Cron job fail** — DB connection lost | HIGH | Retry 3 lần, interval 30 phút. If still fail → Alert SYS_ADMIN. Không skip batch — chạy lại hôm sau. |
| SY06-E3 | **Retention config conflict** — Face ID = 90 ngày nhưng audit log = 3 năm (audit log reference Face ID) | MEDIUM | Audit log giữ metadata (action, actor, timestamp) nhưng purge reference data (ảnh). Log: "Referenced Face ID data purged — metadata retained." |
| SY06-E4 | **Admin đặt retention = 0 ngày (xóa ngay)** | CRITICAL | Chặn: "Retention tối thiểu 1 ngày. Đề xuất: archive thay vì purge." |
| SY06-E5 | **Cold storage query — HR cần dữ liệu archived** | MEDIUM | Request form: "Yêu cầu truy xuất dữ liệu archive." SYS_ADMIN duyệt → restore temporary (24h) → auto-re-archive. |
| SY06-E6 | **Data subject request (NĐ 13/2023 — Right to Erasure)** | HIGH | Per-employee purge: xóa toàn bộ dữ liệu cá nhân (Face ID, attendance, logs) cho 1 NV. Giữ aggregated data (ẩn danh). Audit log: "GDPR/PDPA erasure request processed for EMP-[X]." |
