# 2.11.1. Chấm công và Nhật ký chấm công

---

| Thông tin | Nội dung |
| --- | --- |
| Target release | [Giai đoạn 1 - MVP] |
| Epic | Quản lý Chấm công (Attendance Management) |
| Document owner | ndthuy1 |
| Stakeholder | Nhân viên, HR Admin, Ban Giám đốc |
| Status | Open |

### **1. MỤC TIÊU**

- **Lý do tồn tại:** Cung cấp kênh phản hồi dữ liệu tức thời từ hệ thống AI Vision về cho người lao động.
- **Bài toán:** Trực quan hóa trong việc ghi nhận giờ công và giải quyết nhu cầu tự đối soát dữ liệu của nhân sự.
- **Giá trị mang lại:** Tăng tính minh bạch trong quản trị, giảm các thắc mắc/khiếu nại về mốc giờ chấm công vào cuối tháng.

---

### **2. MÔ TẢ QUY TRÌNH NGHIỆP VỤ**

```mermaid
graph TD
    subgraph input [" 📷 Nguồn dữ liệu "]
        A(["Camera AI C-Vision<br/>Quét khuôn mặt NV"])
    end

    subgraph processing [" ⚙️ Xử lý Backend "]
        B["🔐 Xác thực Webhook<br/><i>HMAC-SHA256 + Idempotency</i>"]
        C["📨 Hàng đợi xử lý<br/><i>BullMQ Queue</i>"]
        D{"Độ tin cậy<br/>≥ 0.85?"}
        F["🔗 Ánh xạ danh tính<br/><i>personId → employeeId</i>"]
        G{"Xác định<br/>hướng ra/vào"}
    end

    subgraph result [" 📊 Kết quả "]
        H["✅ CHECK_IN"]
        I["✅ CHECK_OUT"]
        J[("💾 Tạo bản ghi chấm công<br/><i>AttendanceRecord — APPROVED</i>")]
        K["📊 Cập nhật tổng hợp ngày<br/><i>DailyAttendanceSummary</i>"]
        L(["📱 Mini App cập nhật<br/><i>Dashboard + Nhật ký</i><br/><b>⏱️ ≤ 60 giây</b>"])
    end

    subgraph error [" ❌ Xử lý lỗi "]
        E["⚠️ Thất bại<br/><i>Cần HR xem xét</i>"]
    end

    A -->|"Webhook"| B --> C --> D
    D -->|"Không đạt"| E
    D -->|"Đạt"| F --> G
    G -->|"Cổng vào"| H
    G -->|"Cổng ra"| I
    H & I --> J --> K --> L

    style input fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
    style processing fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
    style result fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px
    style error fill:#FFEBEE,stroke:#C62828,stroke-width:2px

    classDef camera fill:#7B1FA2,color:#fff,stroke:#4A148C,stroke-width:2px
    classDef fail fill:#EF5350,color:#fff,stroke:#C62828
    classDef ok fill:#66BB6A,color:#fff,stroke:#2E7D32
    classDef app fill:#1565C0,color:#fff,stroke:#0D47A1,stroke-width:2px

    class A camera
    class E fail
    class H,I ok
    class L app
```

---

### **3. NHU CẦU NGƯỜI DÙNG**

| Persona | Nhu cầu cụ thể | Tài liệu / Căn cứ |
| --- | --- | --- |
| Nhân viên (Staff) | Muốn biết mình đã chấm công thành công chưa ngay sau khi bước qua cửa sảnh. | Dashboard Trạng thái hôm nay |
| Nhân viên (Staff) | Muốn biết mình còn phải làm bao nhiêu tiếng nữa mới đủ ca (8h) để sắp xếp việc cá nhân. | Thanh Tiến độ làm việc |
| Nhân viên (Staff) | Muốn xem lại ảnh chụp của mình khi quẹt thẻ để chắc chắn hệ thống không nhận diện nhầm người. | Nhật ký Chấm công |

---

### **4. USE CASE**

```mermaid
graph LR
    subgraph actors [" 👥 Vai trò "]
        NV(["🧑‍💼 Nhân viên"])
        HRS(["📋 HR Admin"])
        MGR(["👔 Quản lý"])
        SYS(["⚙️ Hệ thống"])
    end

    subgraph module [" 📊 Chấm công & Nhật ký "]
        UC1["Dashboard trạng thái<br/>hôm nay"]
        UC2["Thanh tiến độ<br/>ca làm việc"]
        UC3["Thống kê hiệu suất<br/>tháng"]
        UC4["Tra cứu Nhật ký<br/>+ Ảnh Face ID"]
    end

    subgraph alert [" ⚠️ Cảnh báo "]
        UC5["Cảnh báo vi phạm<br/><i>Muộn · Sớm · Vắng</i>"]
        UC6["Giải trình ngay<br/><i>Tự điền ngày vi phạm</i>"]
    end

    NV --> UC1 & UC2 & UC3 & UC4 & UC5
    UC5 -.->|"liên kết"| UC6
    HRS --> UC4
    MGR --> UC3
    SYS -->|"cập nhật ≤ 60s"| UC1

    style actors fill:none,stroke:#546E7A,stroke-width:2px,stroke-dasharray:5
    style module fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
    style alert fill:#FFF3E0,stroke:#E65100,stroke-width:2px

    classDef actorNode fill:#37474F,color:#fff,stroke:#263238,stroke-width:2px
    classDef ucNode fill:#BBDEFB,stroke:#1565C0,color:#0D47A1
    classDef alertNode fill:#FFE0B2,stroke:#E65100,color:#BF360C

    class NV,HRS,MGR,SYS actorNode
    class UC1,UC2,UC3,UC4 ucNode
    class UC5,UC6 alertNode
```

---

### **5. PHẠM VI CHỨC NĂNG**

| Mã | Chức năng | Mô tả | User Story |
| --- | --- | --- | --- |
| ATTEN_1 | Dashboard Hôm nay | Hiển thị mốc giờ Vào/Ra, Ngày tháng và Badge trạng thái (Đã chấm công/Chưa chấm công). | Là NV, tôi muốn thấy giờ vào sảnh ngay lập tức để an tâm bắt đầu ca làm việc. |
| ATTEN_2 | Thanh Tiến độ | Hiển thị dạng Progress Bar: Giờ làm thực tế/8h. Tự động cập nhật theo thời gian thực. | Là NV, tôi muốn biết mình đã hoàn thành bao nhiêu % ca làm để cân đối thời gian ra về. |
| ATTEN_3 | Thẻ Thống kê tháng | Hiển thị 03 chỉ số: % Đúng giờ, Tổng ngày nghỉ và Giờ tăng ca lũy kế đến hiện tại. | Là NV, tôi muốn theo dõi hiệu suất tháng của mình để đảm bảo KPI chuyên cần. |
| ATTEN_4 | Nhật ký chi tiết | Danh sách nhật ký dạng Accordion. Mở rộng để xem Ảnh Face ID, Địa điểm và mốc giây quẹt. | Là NV, tôi muốn xem lại ảnh đối soát để minh bạch hóa giờ công khi có tranh chấp. |

---

### **6. YÊU CẦU PHI CHỨC NĂNG**

- **Độ trễ đồng bộ**: Dữ liệu từ Camera hiển thị trên App không chậm quá **60 giây**.
- **Hiệu năng**: Tốc độ tải màn Dashboard và Nhật ký trong **≤ 3 giây**.
- **Bảo mật**: Cơ chế **RBAC** đảm bảo nhân viên chỉ nhìn thấy dữ liệu cá nhân của chính mình.

---

### **7. ĐIỀU KIỆN GIẢ ĐỊNH**

1. Người dùng đã đăng nhập thành công vào hệ thống Mini App.
2. Nhân viên đã được HR gán Lịch làm việc/Ca kíp hợp lệ.
3. C-Vision Camera đã được kích hoạt và đồng bộ Internet ổn định.
