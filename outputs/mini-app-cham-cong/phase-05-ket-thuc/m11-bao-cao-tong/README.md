# 2.11.11. Báo cáo tổng & Xuất dữ liệu

---

| Thông tin | Nội dung |
| --- | --- |
| Target release | Version 1.0 (Sprint 10) |
| Epic | STRATOS-ADMIN: Hệ thống Quản trị & Cấu hình tập trung |
| Document owner | BA Team |
| Stakeholder | HR Admin, Quản lý, Ban Giám đốc |
| Status | Draft |
| Tham chiếu | EAMS v2.0 §9.2-9.3 (Báo cáo & Xuất payroll) |

---

### **1. MỤC TIÊU**

- **Lý do tồn tại:** HR và Ban Giám đốc cần báo cáo tổng hợp chuyên cần theo phòng ban, chi nhánh để ra quyết định quản trị và tính lương.
- **Bài toán:** Tổng hợp dữ liệu chấm công toàn hệ thống thành dashboard trực quan và file Excel chuẩn payroll.
- **Giá trị mang lại:** Giảm 90% thời gian đối soát công cuối tháng; file payroll sẵn sàng import vào MISA/SAP.

---

### **2. MÔ TẢ QUY TRÌNH NGHIỆP VỤ**

```
HR/Manager truy cập "Báo cáo tổng"
        ↓
  ├─ Dashboard quản lý:
  │   ├─ Biểu đồ tỷ lệ chuyên cần theo phòng ban
  │   ├─ Danh sách NV đi muộn/về sớm nhiều nhất
  │   ├─ Xu hướng 7 ngày (status theo ngày)
  │   └─ Chờ phê duyệt count
  │
  ├─ Xuất báo cáo:
  │   ├─ Báo cáo ngày / Bảng chấm công tháng
  │   ├─ Báo cáo OT / Báo cáo nghỉ phép
  │   └─ Xuất payroll (Excel/CSV chuẩn)
  │
  └─ Lọc & phân quyền:
      ├─ SITE_HR: dữ liệu chi nhánh
      ├─ GLOBAL_HR: tất cả chi nhánh
      └─ MANAGER: team trực thuộc
```

---

### **3. NHU CẦU NGƯỜI DÙNG**

| Persona | Nhu cầu cụ thể | Tài liệu / Căn cứ |
| --- | --- | --- |
| HR Admin | Muốn xuất file payroll chuẩn để import vào phần mềm tính lương cuối tháng. | Payroll Export |
| Quản lý | Muốn xem biểu đồ chuyên cần phòng ban để đánh giá hiệu suất team. | Manager Dashboard |
| Ban Giám đốc | Muốn xem tổng quan toàn công ty: tỷ lệ có mặt, xu hướng vắng mặt. | Executive Summary |

---

### **4. PHẠM VI CHỨC NĂNG**

| Mã | Chức năng | Mô tả chi tiết | User Story |
| --- | --- | --- | --- |
| F11.1 | Dashboard quản lý | Biểu đồ chuyên cần theo phòng ban (donut/bar). Top NV vi phạm. Xu hướng 7/30 ngày. Counter: Tổng NV, Có mặt, Trễ, Vắng, Nghỉ phép, Chờ duyệt. | [US-RPT-01](./US-RPT-01-Dashboard-quản-lý.md) |
| F11.2 | Xuất báo cáo & Payroll | Xuất Excel/CSV: Báo cáo ngày, bảng công tháng, báo cáo OT, nghỉ phép. File payroll 13 cột chuẩn tính lương. Lọc theo tháng/phòng ban/site. | [US-RPT-02](./US-RPT-02-Xuất-báo-cáo-và-payroll.md) |
| F11.3 | Báo cáo tuân thủ | Báo cáo vi phạm quy chế theo kỳ. Thống kê giới hạn OT (so với Nghị định 13/2023). Danh sách NV có giải trình quá hạn. | [US-RPT-03](./US-RPT-03-Báo-cáo-tuân-thủ.md) |
| F11.4 | Khóa kỳ lương (Payroll Lock) | Auto-lock khi xuất payroll. Cảnh báo thay đổi sau lock. Kỳ bổ sung (supplementary). Re-export versioning. | [US-RPT-04](./US-RPT-04-Khóa-kỳ-lương.md) |

---

### **5. CẤU TRÚC FILE PAYROLL** *(Nguồn: EAMS v2.0 §9.3)*

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

---

### **6. YÊU CẦU PHI CHỨC NĂNG**

- **Hiệu năng:** Dashboard tải ≤ 3 giây cho 5,000+ NV; xuất Excel ≤ 10 giây.
- **Phân quyền:** SITE_HR chỉ xem dữ liệu chi nhánh; GLOBAL_HR xem tất cả.
- **Định dạng:** Excel (.xlsx) và CSV; tương thích MISA, SAP, Oracle HCM.
- **Lưu trữ:** File xuất được lưu 90 ngày trên server để tải lại.

---

### **EDGE CASES & ERROR HANDLING (toàn module)**

| # | US | Case | Severity | Expected Behavior |
|---|-----|------|----------|-------------------|
| RP01-E1 | RPT-01 | **Counter không cân bằng** — Tổng NV ≠ Có mặt + Trễ + Vắng + Nghỉ phép | HIGH | Thêm trạng thái "Chưa xác định" = NV chưa qua giờ bắt đầu ca HOẶC NV ca linh hoạt (FREE). Công thức: Tổng = Có mặt + Trễ + Vắng + Nghỉ phép + **Chưa xác định**. Counter luôn cân bằng. |
| RP02-E1 | RPT-02 | **Payroll exported nhưng có correction sau** — HR xuất payroll ngày 26, ngày 27 có correction được duyệt | CRITICAL | **Payroll Lock:** Sau khi xuất payroll → đánh dấu kỳ đó "LOCKED". Mọi correction sau lock → cảnh báo: "Kỳ lương tháng X đã xuất. Thay đổi này sẽ áp dụng cho kỳ bổ sung". Hiển thị badge "Có X thay đổi sau lần xuất cuối" trên nút Export. Cho phép HR "Xuất lại" (re-export) với timestamp mới. |
| RP02-E2 | RPT-02 | **CSV encoding tiếng Việt** — MISA/phần mềm kế toán VN đọc UTF-8 sai | MEDIUM | Cung cấp dropdown chọn encoding khi xuất: UTF-8 BOM (default), Windows-1258 (cho MISA), Shift-JIS (cho phần mềm Nhật). Preview 5 dòng đầu trước khi download. |
| RP03-E1 | RPT-03 | **OT 300h đặc biệt — ai duyệt?** — Giới hạn mở rộng 300h/năm cần phê duyệt đặc biệt | CRITICAL | **Workflow bổ sung:** Khi NV đạt 200h OT/năm → hệ thống chặn đơn OT mới. HR gửi "Yêu cầu mở rộng OT 300h" cho NV, kèm lý do kinh doanh. Phê duyệt: GLOBAL_HR + SITE_MANAGER (2 level). Sau khi duyệt → mở giới hạn cho NV đến hết năm. Báo cáo tuân thủ hiển thị rõ: NV nào đang dùng quota 300h. |

---

### **7. ĐIỀU KIỆN GIẢ ĐỊNH**

1. Dữ liệu chấm công đã được tổng hợp (DailyAttendanceSummary) cho kỳ báo cáo.
2. Tất cả đơn nghỉ phép và OT trong kỳ đã được phê duyệt xong.
3. Payroll Lock: HR nên xuất payroll SAU ngày chốt công + 3 ngày buffer cho correction cuối cùng.
3. Người dùng có role HR Admin, Manager hoặc cao hơn.
