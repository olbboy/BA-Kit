# US-EXPL-02: Yêu cầu sửa chấm công (Attendance Correction)

---

**AS A** Nhân viên,  
**I WANT TO** gửi yêu cầu điều chỉnh (thêm / sửa / xóa) mốc chấm công khi phát hiện dữ liệu sai và đính kèm minh chứng,  
**SO THAT** bảng công của tôi phản ánh chính xác thực tế làm việc, đảm bảo quyền lợi lương không bị ảnh hưởng bởi lỗi hệ thống hoặc thao tác.

---

### **1. BUSINESS FLOW**

1. **Phát hiện sai**: NV thấy mốc chấm công bị sai/thiếu tại US-ATTEN-03 (Nhật ký) hoặc US-RPTPRS-01 (Báo cáo cá nhân).
2. **Tạo yêu cầu**: NV nhấn "Yêu cầu điều chỉnh" → Chọn loại: ADD (thêm), MODIFY (sửa giờ), DELETE (xóa nhầm).
3. **Điền thông tin**: Chọn ngày, nhập giờ mới (nếu MODIFY/ADD), lý do, đính kèm file.
4. **Gửi yêu cầu**: Hệ thống tạo `AttendanceCorrection` (status: PENDING) → Tạo Approval workflow.
5. **Phê duyệt**: Manager/HR duyệt tại Module 10 (Inbox phê duyệt).
6. **Kết quả**:
   - APPROVED → Hệ thống áp dụng điều chỉnh, tính lại `DailyAttendanceSummary` (giờ làm, OT, đi trễ/về sớm).
   - REJECTED → Giữ nguyên record gốc. NV nhận phản hồi (lý do từ chối).

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin | Role | Ghi chú |
| --- | --- | --- |
| Tạo yêu cầu sửa | Nhân viên, Manager, HR | NV chỉ sửa của mình. Manager/HR có thể tạo cho NV trong team/site. |
| Xem yêu cầu đã gửi | Nhân viên (của mình), Manager (team), HR (site) | ABAC theo user scope. |
| Phê duyệt yêu cầu | Manager (Level 1), SITE_HR (Level 2) | Theo approval chain cấu hình tại Module 10. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Loại điều chỉnh**

| Loại | Mô tả | Trường bắt buộc |
| --- | --- | --- |
| **ADD** | Thêm mốc mới (quên check-in/out) | Ngày, Giờ, Loại (IN/OUT), Lý do |
| **MODIFY** | Sửa giờ mốc hiện có | Mốc gốc (auto-populated), Giờ mới, Lý do |
| **DELETE** | Xóa mốc nhầm (VD: check-in nhầm site) | Mốc gốc (auto-populated), Lý do |

#### **AC2. Form yêu cầu**

- Ngày: Chỉ cho phép chọn trong **15 ngày trở lại** *(hoặc trước ngày chốt công)*. Ngày đã chốt: "Không thể điều chỉnh ngày đã chốt công."
- Giờ: HH:MM (24h) — Nếu MODIFY: hiển thị giờ cũ readonly + field giờ mới.
- Lý do: Textarea ≥ 20 ký tự (bắt buộc).
- File đính kèm: Ảnh/PDF ≤ 5MB (ảnh chụp màn hình, email xác nhận có mặt).

#### **AC3. Trạng thái theo dõi**

| Status | Màu | Mô tả |
| --- | --- | --- |
| PENDING | 🟡 Vàng | Đang chờ duyệt |
| APPROVED | 🟢 Xanh | Đã duyệt, giờ đã cập nhật |
| REJECTED | 🔴 Đỏ | Bị từ chối, kèm lý do |
| CANCELLED | ⚪ Xám | NV tự hủy (chỉ khi PENDING) |

#### **AC4. Hiệu ứng sau Approve**

- **ADD**: Tạo `AttendanceRecord` mới với source = `CORRECTION`. Tính lại giờ làm, OT.
- **MODIFY**: Update giờ record gốc. Giữ lịch sử (old_value, new_value). Tính lại summary.
- **DELETE**: Soft-delete record. Tính lại summary. Nếu xóa CHECK_IN → giờ làm ngày đó = 0.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| EX02-E1 | **Correction cho ngày đã chốt công** — NV sửa ngày 20 nhưng chốt công ngày 25 đã qua | HIGH | Chặn: "Ngày [DD/MM] đã chốt công. Liên hệ HR để được hỗ trợ." HR có Exception Approval để sửa sau chốt. |
| EX02-E2 | **Correction trùng Manual Entry** — NV yêu cầu ADD nhưng HR đã tạo Manual Entry cùng mốc | MEDIUM | Cảnh báo: "Đã có mốc [HH:MM] được tạo bởi HR. Sử dụng MODIFY nếu cần sửa giờ." |
| EX02-E3 | **DELETE check-in duy nhất** — NV xóa mốc check-in duy nhất trong ngày có OT approved | HIGH | Cảnh báo: "Xóa mốc này sẽ ảnh hưởng OT đã duyệt ([N] giờ). OT request sẽ bị tính lại." Yêu cầu confirm. |
| EX02-E4 | **Nhiều correction cùng ngày** — NV gửi 3 yêu cầu sửa cho cùng 1 ngày | MEDIUM | Cho phép nếu cho các mốc khác nhau. Chặn nếu cùng mốc: "Bạn đã có yêu cầu PENDING cho mốc [HH:MM]. Hủy yêu cầu cũ trước khi tạo mới." |

---

### **DEFINITION OF DONE (DOD)**

1. **AC Verified**: Tất cả 3 loại (ADD/MODIFY/DELETE) hoạt động đúng.
2. **Recalculation**: DailyAttendanceSummary được tính lại chính xác sau mỗi correction approved.
3. **Audit Trail**: Lịch sử sửa đổi (old_value → new_value) được lưu hoàn chỉnh.
4. **Edge Cases Tested**: Ngày chốt công, trùng Manual Entry, DELETE ảnh hưởng OT.
5. **Integration**: Hiển thị icon "✏️ Đã sửa" trên US-ATTEN-03 cho các mốc đã correction.
