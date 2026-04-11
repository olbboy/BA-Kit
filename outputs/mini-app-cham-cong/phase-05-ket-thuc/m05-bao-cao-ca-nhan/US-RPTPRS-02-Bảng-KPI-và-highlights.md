# US-RPTPRS-02: Bảng KPI và Highlights

---

**AS A** Nhân viên,  
**I WANT TO** xem bảng tổng hợp KPI chuyên cần theo quý kèm Performance Highlights so sánh với kỳ trước,  
**SO THAT** tôi có thể đánh giá xu hướng hiệu suất dài hạn và biết mình cần cải thiện ở đâu.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** NV cuộn xuống phần "KPI & Highlights" trong Báo cáo cá nhân.
2. **Khởi tạo:** Hệ thống tổng hợp dữ liệu theo quý (Q1-Q4).
3. **Hiển thị:** Bảng KPI dạng scorecard + highlights so sánh kỳ trước.
4. **Tương tác:** NV chọn quý để xem chi tiết.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Bảng KPI cá nhân | Nhân viên | ABAC: Chỉ xem KPI của chính mình. |
| So sánh trung bình phòng ban | Nhân viên | Hiển thị trung bình ẩn danh, không tiết lộ cá nhân. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Bảng KPI Scorecard**

Hiển thị các chỉ số theo quý:

| Chỉ số | Công thức | Đơn vị |
| --- | --- | --- |
| % Đúng giờ | (Ngày đúng giờ / Tổng ngày làm) × 100 | % |
| Số lần đi trễ | COUNT(status=LATE) | lần |
| Số lần về sớm | COUNT(status=EARLY_LEAVE) | lần |
| Tổng ngày vắng | COUNT(status=ABSENT) | ngày |
| Giờ OT lũy kế | SUM(approvedOTHours) | giờ |
| Tổng ngày nghỉ | COUNT(LeaveRequest APPROVED) | ngày |

#### **AC2. Performance Highlights**

- So sánh quý hiện tại với quý trước:
  - Mũi tên xanh ↑ nếu cải thiện (VD: % đúng giờ tăng).
  - Mũi tên đỏ ↓ nếu giảm sút.
  - "—" nếu không có dữ liệu quý trước (NV mới).
- Highlight đặc biệt: "Không trễ lần nào trong quý" (badge thành tích).

#### **AC3. So sánh trung bình phòng ban**

- Hiển thị dòng: "Trung bình phòng ban: X%" bên cạnh Score cá nhân.
- Dữ liệu ẩn danh — không hiển thị thông tin cá nhân đồng nghiệp.
- Nếu Score cá nhân < trung bình → Hiển thị gợi ý cải thiện nhẹ nhàng.

#### **AC4. Chọn kỳ báo cáo**

- Dropdown: Q1 (T1-T3), Q2 (T4-T6), Q3 (T7-T9), Q4 (T10-T12).
- Mặc định: Quý hiện tại.
- Khi quý chưa kết thúc → Hiển thị "Dữ liệu tạm tính đến dd/MM/yyyy".

---

### **4. DEFINITION OF DONE (DOD)**

1. **Dữ liệu:** KPI phải khớp với Dashboard hiệu suất (US-RPTPRS-01) khi cùng kỳ tháng.
2. **So sánh:** Highlight mũi tên phải chính xác khi so 2 quý liên tiếp.
3. **NV mới:** Không hiển thị so sánh nếu NV chưa có dữ liệu quý trước.
4. **QA:** Kiểm thử chuyển quý, NV nghỉ thai sản dài hạn, NV chuyển phòng ban giữa quý.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RP02-E1 | **KPI target chưa được cấu hình** — HR chưa set target cho site | MEDIUM | Hiển thị actual values, cột target hiển thị "N/A". Badge: "Target chưa được thiết lập — liên hệ HR." |
| RP02-E2 | **Dữ liệu OT bị điều chỉnh sau chốt công** — Review lại số liệu sau correction | LOW | Hiển thị giá trị sau correction kèm icon "Đã điều chỉnh". Tooltip: "Giá trị gốc: X, Sau điều chỉnh: Y." |
