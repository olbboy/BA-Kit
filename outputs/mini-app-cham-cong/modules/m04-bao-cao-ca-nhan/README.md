# 2.11.5. Báo cáo cá nhân

---

| Thông tin | Nội dung |
| --- | --- |
| Target release | Version 1.0 (Sprint 10) |
| Epic | STRATOS-ESS: Trải nghiệm dành cho Nhân viên |
| Document owner | BA Team |
| Stakeholder | Nhân viên, Quản lý |
| Status | Draft |
| Tham chiếu | EAMS v2.0 §9.1 (Dashboard tổng quan) |

---

### **1. MỤC TIÊU**

- **Lý do tồn tại:** Nhân viên cần tự theo dõi hiệu suất chuyên cần cá nhân mà không phải hỏi HR mỗi cuối tháng.
- **Bài toán:** Tổng hợp và trực quan hóa các chỉ số KPI chuyên cần: tỷ lệ đúng giờ, tổng giờ làm, ngày nghỉ, giờ OT theo kỳ.
- **Giá trị mang lại:** Tăng tính minh bạch dữ liệu, giúp NV tự điều chỉnh hành vi; giảm khiếu nại cuối tháng.

---

### **2. MÔ TẢ QUY TRÌNH NGHIỆP VỤ**

```mermaid
graph TD
    A([NV truy cập Báo cáo CN]) --> B[Load DailyAttendanceSummary]
    B --> C[Tính KPI tháng hiện tại]
    C --> D[Render Dashboard]
    D --> E{NV chọn action}
    E -->|Xem KPI| F[Bảng KPI + Highlights]
    E -->|Xem chi tiết| G[Drill-down theo ngày]
    E -->|So sánh| H[Chart so sánh tháng]
    F & G & H --> I([Hiển thị kết quả])

    classDef start fill:#455A64,color:#fff,stroke-width:0
    classDef ok fill:#66BB6A,color:#fff,stroke-width:0
    class A start
    class I ok
```


### USE CASE DIAGRAM

```mermaid
graph LR
    NV[👤 Nhân viên]
    SYS[⚙️ System]

    NV --> UC1[Dashboard hiệu suất cá nhân]
    NV --> UC2[Bảng KPI & Highlights]
    SYS --> UC3[Tính toán metrics]
    SYS --> UC4[Aggregate tháng/tuần]
```


```
NV mở mục "Báo cáo cá nhân" trên Mini App
        ↓
Hệ thống tổng hợp dữ liệu từ:
  ├─ AttendanceAggregator (chấm công)
  ├─ LeaveAggregator (nghỉ phép)
  └─ OTAggregator (tăng ca)
        ↓
Hiển thị:
  ├─ Score chuyên cần tổng (điểm/100)
  ├─ Biểu đồ xu hướng theo tuần/tháng
  ├─ Bảng KPI Highlights
  └─ So sánh với trung bình phòng ban (ẩn danh)
        ↓
NV chọn kỳ báo cáo (tháng/quý) để xem chi tiết
```

---

### **3. NHU CẦU NGƯỜI DÙNG**

| Persona | Nhu cầu cụ thể | Tài liệu / Căn cứ |
| --- | --- | --- |
| Nhân viên | Muốn biết điểm chuyên cần của mình để đảm bảo KPI và quyền lợi thưởng. | Score chuyên cần |
| Nhân viên | Muốn theo dõi xu hướng đi trễ/về sớm theo thời gian để tự cải thiện. | Biểu đồ trend |
| Quản lý | Muốn xem tổng quan hiệu suất team trên giao diện quản lý (cross-ref Module 11). | KPI Highlights |

---

### **4. PHẠM VI CHỨC NĂNG**

| Mã | Chức năng | Mô tả chi tiết | User Story |
| --- | --- | --- | --- |
| F05.1 | Dashboard hiệu suất cá nhân | Score chuyên cần (0-100), tổng giờ làm tháng, tổng ngày nghỉ, tổng giờ OT. Biểu đồ trend 4 tuần. Cập nhật real-time khi có dữ liệu mới. | [US-RPTPRS-01](./us-rptprs-01-dashboard-hieu-suat-ca-nhan.md) |
| F05.2 | Bảng KPI & Highlights | Bảng tổng hợp KPI theo quý: % đúng giờ, số lần trễ, số ngày vắng, giờ OT lũy kế. Performance highlights so sánh kỳ trước. | [US-RPTPRS-02](./us-rptprs-02-bang-kpi-va-highlights.md) |

---

### **5. CÔNG THỨC TÍNH** *(Nguồn: EAMS v2.0 §3.4, §9.1)*

| Chỉ số | Công thức | Nguồn dữ liệu |
| --- | --- | --- |
| Score chuyên cần | (Ngày đúng giờ / Tổng ngày làm) × 100 | DailyAttendanceSummary |
| Tổng giờ làm | SUM(netHours) trong tháng | DailyAttendanceSummary |
| Tổng ngày nghỉ | COUNT(LeaveRequest status=APPROVED) | LeaveRequest |
| Giờ OT lũy kế | SUM(approvedOTHours) trong tháng | OvertimeRequest |
| Số lần đi trễ | COUNT(status=LATE or LATE_AND_EARLY) | DailyAttendanceSummary |

---

### **6. YÊU CẦU PHI CHỨC NĂNG**

- **Hiệu năng:** Tải dashboard báo cáo ≤ 2 giây.
- **Cập nhật:** Dữ liệu tự động refresh khi có sự kiện chấm công hoặc đơn từ được duyệt.
- **Bảo mật:** NV chỉ xem được báo cáo của chính mình (ABAC: filter theo User_ID).
- **Responsive:** Hiển thị tốt trên cả mobile và web.

---

### **EDGE CASES & ERROR HANDLING**

| # | US | Case | Severity | Expected Behavior |
|---|-----|------|----------|-------------------|
| P01-E1 | RPTPRS-01 | **NV chuyển phòng ban giữa kỳ** — NV chuyển từ Phòng A sang Phòng B giữa tháng | MEDIUM | Score so sánh với trung bình phòng tại thời điểm hiện tại (Phòng B). Ghi chú: "Bạn chuyển phòng ngày dd/MM — dữ liệu trước đó tính tại Phòng A". |
| P01-E2 | RPTPRS-01 | **Dữ liệu đang bị dispute** — NV có 5 đơn giải trình PENDING trong tháng | LOW | Hiển thị label "Tạm tính — X đơn đang chờ duyệt" bên cạnh Score. Sử dụng icon cảnh báo. Score sẽ tự cập nhật khi đơn được duyệt. |
| P02-E1 | RPTPRS-02 | **Quý chưa kết thúc** — So sánh Q2 (đang giữa) với Q1 (đã kết thúc) không công bằng | LOW | Hiển thị "Dữ liệu tạm tính đến dd/MM/yyyy" + ghi chú "So sánh sẽ chính xác hơn khi quý kết thúc". Mũi tên trend chỉ hiển thị khi quý hiện tại đã qua ≥ 2 tháng. |

---

### **7. ĐIỀU KIỆN GIẢ ĐỊNH**

1. Nhân viên đã có dữ liệu chấm công ít nhất 1 tháng.
2. Hệ thống đã tính toán DailyAttendanceSummary cho các ngày đã qua.
3. Các đơn nghỉ phép và OT đã được phê duyệt xong.
