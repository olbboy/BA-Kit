# BRD HR (Admin)

---

| Thông tin | Nội dung |
| --- | --- |
| Target release | Version 1.0 |
| Epic | STRATOS-ADMIN: Hệ thống Quản trị & Cấu hình tập trung |
| Document owner | ndthuy1 |
| Stakeholder | CEO, HR Admin, IT |
| Status | Open |

### **1. MỤC TIÊU**

- **Lý do tồn tại:** Doanh nghiệp cần công cụ quản lý nhân sự tập trung, thay thế các phương thức thủ công.
- **Bài toán:** Giải quyết việc cấu hình ca làm việc phức tạp (ca đêm, ca hành chính), quản lý thiết bị AI Camera và phê duyệt yêu cầu từ nhân viên trên một nền tảng duy nhất.
- **Giá trị mang lại:** Tự động hóa dữ liệu chấm công, tăng tính minh bạch và cung cấp báo cáo quản trị tức thời.

### **2. MÔ TẢ QUY TRÌNH NGHIỆP VỤ**

```mermaid
graph TD
    A(["📋 HR Admin đăng nhập"]) --> B["📊 Dashboard Admin<br/><i>Trực tuyến · WFH · Vắng mặt</i>"]

    subgraph modules [" 🛠️ 8 chức năng quản trị "]
        C["🏢 Cơ cấu tổ chức<br/><i>Sơ đồ cây + Import NV</i>"]
        D["⏰ Cấu hình Ca<br/><i>In/Out/Break + Punch Limit</i>"]
        E["📅 Lịch & Ngày nghỉ<br/><i>Lễ tết + Chính sách</i>"]
        F["📷 Camera AI<br/><i>Thiết bị + Ánh xạ + Giám sát</i>"]
        G["🔔 Thông báo<br/><i>36 sự kiện × 3 kênh</i>"]
        H["✅ Phê duyệt<br/><i>Nghỉ/OT/Giải trình/Đổi ca</i>"]
        I["📈 Báo cáo & Xuất<br/><i>Payroll Excel + KPI</i>"]
    end

    B --> C & D & E & F & G & H & I

    subgraph engine [" ⚙️ Engine xử lý "]
        J[("💾 Dữ liệu NV")]
        K["🔄 Engine tính công"]
    end

    C -->|"Import Excel"| J
    D -->|"Áp dụng quy tắc"| K
    E -->|"Batch Job"| K
    F -->|"Webhook C-Vision"| K
    K --> I

    style modules fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
    style engine fill:#FFF3E0,stroke:#E65100,stroke-width:2px

    classDef admin fill:#FF9800,color:#fff,stroke-width:2px
    classDef dash fill:#1976D2,color:#fff,stroke-width:2px
    classDef mod fill:#BBDEFB,stroke:#1565C0,color:#0D47A1
    classDef eng fill:#FFE0B2,stroke:#E65100,color:#BF360C

    class A admin
    class B dash
    class C,D,E,F,G,H,I mod
    class J,K eng
```

### **3. NHU CẦU NGƯỜI DÙNG**

| Persona | Nhu cầu cụ thể | Tài liệu |
| --- | --- | --- |
| HR | Cần quản lý camera điểm danh và cài đặt quy tắc bắn thông báo login fail/muộn sớm. | Cấu hình camera & Notification |
| Quản lý | Xem báo cáo tổng hợp quân số theo phòng ban để nắm bắt tình hình đi làm thực tế. | Dashboard Admin |
| HR Admin | Thiết lập các ca làm dự kiến và giờ nghỉ để hệ thống tính công tương ứng. | Quản lý Ca làm việc |

### **4. USE CASE**

```mermaid
graph LR
    subgraph actors [" 👥 Vai trò "]
        HR(["📋 HR Admin"])
        MGR(["👔 Quản lý"])
        IT(["🔧 IT Admin"])
    end

    subgraph functions [" 🛠️ Chức năng quản trị "]
        F01["<b>F01</b> Dashboard<br/><i>Quân số + Biểu đồ</i>"]
        F02["<b>F02</b> Cơ cấu tổ chức<br/><i>NV + Phòng ban</i>"]
        F03["<b>F03</b> Cấu hình Ca<br/><i>In/Out/Break</i>"]
        F04["<b>F04</b> Lịch & Ngày nghỉ<br/><i>Lễ + Chính sách</i>"]
        F05["<b>F05</b> Camera AI<br/><i>Thiết bị + Ánh xạ</i>"]
        F06["<b>F06</b> Thông báo<br/><i>36 sự kiện + Policy</i>"]
        F07["<b>F07</b> Phê duyệt<br/><i>Nghỉ/OT/Giải trình</i>"]
        F08["<b>F08</b> Báo cáo & Xuất<br/><i>Payroll + KPI</i>"]
    end

    HR --> F01 & F02 & F03 & F04 & F07 & F08
    MGR --> F01 & F07 & F08
    IT --> F05 & F06

    classDef actor fill:#37474F,color:#fff,stroke-width:2px
    classDef func fill:#E3F2FD,stroke:#1565C0,color:#0D47A1

    class HR,MGR,IT actor
    class F01,F02,F03,F04,F05,F06,F07,F08 func
```

### **5. PHẠM VI CHỨC NĂNG**

| Mã | Chức năng | Mô tả | User Story |
| --- | --- | --- | --- |
| F01 | Màn hình chính | Số lượng nhân viên (On-site/WFH/Vắng). Biểu đồ chuyên cần hằng ngày. | Là Manager, tôi muốn xem nhanh danh sách nhân viên trong ngày. |
| F02 | Cơ cấu tổ chức | View danh sách NV: ID, Phòng ban, Giờ check-in cuối và trạng thái hiện tại. | Là HR, tôi muốn biết ai đang hiện diện thực tế tại VP. |
| F03 | Cấu hình Ca | Thiết lập In/Out/Break. Case: Ca đêm (Crossing 00:00). Case: Punch limit. | Là Admin, tôi muốn tạo ca làm việc linh hoạt. |
| F04 | Lịch & Ngày nghỉ | Quản lý nghỉ lễ & nghỉ chính sách (Nghỉ sinh nhật, hạn mức WFH). | Là Admin, tôi muốn quản lý lịch nghỉ lễ toàn công ty. |
| F05 | Cấu hình Camera | Chọn Device ID từ C-Cam. Gán mục đích In/Out cho từng Camera. | Là IT, tôi muốn chọn camera sảnh làm máy chấm công. |
| F06 | Cấu hình Thông báo | Cấu hình cho 36 sự kiện. Chọn Policy (Gom tin/Chống nhiễu/Lập lịch). | Là Admin, tôi muốn nhận cảnh báo security tức thời. |
| F07 | Trung tâm Phê duyệt | Xử lý tập trung đơn Nghỉ/OT/Giải trình/Đổi ca từ nhân viên. | Là Quản lý, tôi muốn duyệt đơn nhanh gọn trên mobile. |
| F08 | Báo cáo & Xuất | Kết xuất Excel: Payroll chuẩn, Báo cáo Tuân thủ, Báo cáo KPI tổng. | Là HR, tôi muốn xuất dữ liệu chuẩn để tính lương tháng. |

### **6. YÊU CẦU PHI CHỨC NĂNG**

- Giao diện web, tương thích trên cả web và mobile.
- Hỗ trợ tìm kiếm nhanh, không phân biệt hoa/thường/dấu.
- Role-based & attribute-based access (RBAC + ABAC) theo Phòng ban.
- Xuất dữ liệu định dạng Excel theo mẫu chuẩn.

### **7. ĐIỀU KIỆN GIẢ ĐỊNH**

- Người dùng đã đăng nhập vào hệ thống quản trị trung tâm.
- Thiết bị Camera AI đã hoạt động và stream được dữ liệu ID về Server.

---
