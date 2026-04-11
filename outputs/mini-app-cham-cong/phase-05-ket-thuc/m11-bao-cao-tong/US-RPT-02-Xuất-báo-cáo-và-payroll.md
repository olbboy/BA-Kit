# US-RPT-02: Xuất báo cáo và Payroll

---

**AS A** HR Admin,  
**I WANT TO** xuất các loại báo cáo chấm công và file payroll chuẩn định dạng Excel/CSV,  
**SO THAT** tôi có dữ liệu sẵn sàng để tính lương, nộp cho kế toán và lưu trữ hồ sơ theo quy định.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** HR mở "Báo cáo tổng" → Tab "Xuất báo cáo".
2. **Chọn loại báo cáo:** Báo cáo ngày / Bảng chấm công tháng / Báo cáo OT / Báo cáo nghỉ phép / Xuất payroll.
3. **Thiết lập bộ lọc:** Tháng/năm, phòng ban, chi nhánh.
4. **Preview:** Xem trước dữ liệu trên giao diện (bảng).
5. **Xuất file:** Chọn định dạng (Excel .xlsx hoặc CSV) → Download.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Xuất báo cáo phòng ban | MANAGER, DEPT_HEAD | Chỉ xuất data team/phòng. |
| Xuất báo cáo site | SITE_HR | Xuất toàn bộ NV site. |
| Xuất payroll | SITE_HR, GLOBAL_HR | Chỉ HR có quyền xuất payroll. |
| Xuất toàn hệ thống | GLOBAL_HR, SYS_ADMIN | Tất cả site. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Các loại báo cáo**

| Báo cáo | Nội dung | Bộ lọc |
| --- | --- | --- |
| Báo cáo ngày | Check-in/out, giờ làm, trạng thái mỗi NV | Ngày, phòng ban |
| Bảng chấm công tháng | Lưới ngày × NV, tổng hợp tháng | Tháng/năm, phòng ban |
| Báo cáo OT | Giờ OT theo loại ngày, hệ số, giờ quy đổi | Tháng/năm, phòng ban |
| Báo cáo nghỉ phép | Loại phép, ngày nghỉ, số ngày, lý do | Khoảng ngày, phòng ban |
| Xuất payroll | 13 cột chuẩn tính lương | Tháng/năm, phòng ban |

#### **AC2. Cấu trúc file Payroll (13 cột)**

| # | Cột | Mô tả |
| --- | --- | --- |
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

#### **AC3. Preview trước khi xuất**

- Hiển thị bảng dữ liệu trên giao diện (tối đa 50 dòng preview).
- Cho phép sort theo từng cột.
- Hiển thị tổng cộng (summary row) ở cuối bảng.

#### **AC4. Xuất file**

- Định dạng: Excel (.xlsx) và CSV.
- File name: `[Loại]_[Tháng]_[Site]_[Timestamp].xlsx`.
- Lưu trữ: File xuất được lưu 90 ngày trên server để tải lại.
- Thời gian xuất: ≤ 10 giây cho 5,000+ NV.

---

### **4. DEFINITION OF DONE (DOD)**

1. **Dữ liệu:** File payroll phải khớp 100% với dữ liệu trên Dashboard.
2. **Tương thích:** File Excel mở đúng trên MISA, SAP, Oracle HCM.
3. **Hiệu năng:** Xuất 5,000 NV ≤ 10 giây.
4. **QA:** Kiểm thử xuất từng loại báo cáo; file CSV encoding UTF-8 BOM cho tiếng Việt.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RT02-E1 | **Export file > 10MB** — 5000 NV × 12 tháng | MEDIUM | Async export: "File đang được tạo. Bạn sẽ nhận email khi hoàn tất." Không block UI. |
| RT02-E2 | **Template payroll không khớp** — MISA format khác SAP format | MEDIUM | Dropdown chọn template: MISA / SAP / Oracle / Custom. Preview 5 dòng đầu trước khi export. |
| RT02-E3 | **Export dữ liệu chưa chốt công** — Tháng chưa complete | HIGH | Cảnh báo: "Dữ liệu tháng [MM] chưa chốt công. File export có thể thay đổi." Yêu cầu confirm. |
| RT02-E4 | **NV có OT qua 2 tháng** — OT ca đêm T cuối tháng → T+1 đầu tháng kế | MEDIUM | Split: giờ trước 00:00 tính tháng M, giờ sau 00:00 tính tháng M+1. Ghi chú trong file export. |
