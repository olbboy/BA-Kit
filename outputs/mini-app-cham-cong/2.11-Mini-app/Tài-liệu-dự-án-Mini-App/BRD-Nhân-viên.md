# BRD Nhân viên

---

| Thông tin | Nội dung |
| --- | --- |
| Target release | Version 1.0 |
| Epic | STRATOS-ESS: Trải nghiệm dành cho Nhân viên |
| Document owner | ndthuy1 |
| Stakeholder | Toàn bộ Nhân viên |
| Status | Open |

### **1. MỤC TIÊU**

- **Lý do tồn tại:** Nhân viên cần quyền truy cập thông tin công việc, chấm công và hiệu suất cá nhân chủ động.
- **Bài toán:** Loại bỏ việc hỏi đáp thủ công về giờ công, gửi đơn giấy và giúp nhân viên tự định danh khuôn mặt chấm công.
- **Giá trị mang lại:** Nâng cao sự hài lòng của nhân viên thông qua sự minh bạch về dữ liệu giờ công và KPIs.

### **2. MÔ TẢ QUY TRÌNH NGHIỆP VỤ**

```mermaid
graph TD
    A(["🧑‍💼 Nhân viên mở Mini App"]) --> B["📊 Dashboard Cá nhân<br/><i>Giờ vào + Thanh tiến độ 8h</i>"]

    subgraph features [" 📱 6 chức năng ESS "]
        C["📒 Nhật ký Chấm công<br/><i>In/Out + Ảnh Face ID</i>"]
        D["📝 Trung tâm Đăng ký<br/><i>Nghỉ phép · Đổi ca · OT</i>"]
        E["⚠️ Giải trình công<br/><i>Muộn/Sớm + Minh chứng</i>"]
        F["📈 Báo cáo cá nhân<br/><i>KPI + Điểm chuyên cần</i>"]
        G["⚙️ Setup Hồ sơ<br/><i>Thông tin + Face ID</i>"]
    end

    B --> C & D & E & F & G

    subgraph approval [" ✅ Luồng phê duyệt "]
        H["📤 Gửi đơn → PENDING"]
        I{"👔 Manager / HR<br/>phê duyệt"}
        J["✅ Cập nhật dữ liệu"]
        K["❌ Phản hồi lý do<br/>từ chối"]
    end

    D & E --> H --> I
    I -->|"Duyệt"| J
    I -->|"Từ chối"| K

    subgraph setup [" 🆔 Đăng ký Face ID "]
        G1["<b>Bước 1</b><br/>Thông tin cá nhân"]
        G2["<b>Bước 2</b><br/>📷 Định danh khuôn mặt AI"]
        G3["<b>Bước 3</b><br/>✅ Hoàn tất"]
    end

    G --> G1 --> G2 --> G3

    style features fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
    style approval fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px
    style setup fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px

    classDef start fill:#4CAF50,color:#fff,stroke-width:2px
    classDef dash fill:#1976D2,color:#fff,stroke-width:2px
    classDef ok fill:#66BB6A,color:#fff
    classDef fail fill:#EF5350,color:#fff

    class A start
    class B dash
    class J,G3 ok
    class K fail
```

### **3. NHU CẦU NGƯỜI DÙNG**

| Persona | Nhu cầu cụ thể | Tài liệu |
| --- | --- | --- |
| Nhân viên | Muốn biết hôm nay mình đã làm được bao nhiêu tiếng (Progress) và bao giờ thì đủ 8 tiếng. | Dashboard Cá nhân |
| Nhân viên | Cần tự cập nhật ảnh quét khuôn mặt Face ID để không phải nhờ IT hỗ trợ. | Setup cá nhân |
| Nhân viên | Muốn xem báo cáo hiệu suất cá nhân (KPI) để biết mình có được thưởng năng suất. | Báo cáo hiệu suất cá nhân |

### **4. USE CASE**

```mermaid
graph LR
    subgraph actor [" 👤 "]
        NV(["🧑‍💼 Nhân viên"])
    end

    subgraph view [" 👁️ Xem thông tin "]
        F01["<b>F01</b> Dashboard Cá nhân<br/><i>Giờ vào + Tiến độ 8h</i>"]
        F02["<b>F02</b> Nhật ký Chấm công<br/><i>In/Out + Tag trạng thái</i>"]
        F05["<b>F05</b> Báo cáo cá nhân<br/><i>Điểm chuyên cần + KPI</i>"]
    end

    subgraph action [" ✏️ Thao tác "]
        F03["<b>F03</b> Trung tâm Đăng ký<br/><i>Nghỉ phép · Đổi ca · OT</i>"]
        F04["<b>F04</b> Giải trình<br/><i>Muộn/Sớm + Ảnh</i>"]
        F06["<b>F06</b> Setup Hồ sơ<br/><i>Thông tin + Face ID</i>"]
    end

    NV --> F01 & F02 & F05
    NV --> F03 & F04 & F06

    style actor fill:none,stroke:#546E7A,stroke-width:2px,stroke-dasharray:5
    style view fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
    style action fill:#FFF3E0,stroke:#E65100,stroke-width:2px

    classDef actorNode fill:#37474F,color:#fff,stroke-width:2px
    classDef viewNode fill:#BBDEFB,stroke:#1565C0,color:#0D47A1
    classDef action fill:#FFF3E0,stroke:#E65100,color:#BF360C

    class NV actor
    class F01,F02,F05 view
    class F03,F04,F06 action
```

### **5. PHẠM VI CHỨC NĂNG**

| Mã | Chức năng | Mô tả | User Story |
| --- | --- | --- | --- |
| F01 | Dashboard Cá nhân | Xem giờ vào, Thanh tiến độ 8h (Progress bar) nhảy real-time. % Đúng giờ. | Là NV, tôi muốn xem mình đã làm đủ ca hôm nay chưa. |
| F02 | Nhật ký Chấm công | Danh sách ngày vào/ra kèm tag trạng thái (Đúng giờ/Vào trễ). | Là NV, tôi muốn đối soát lại giờ quẹt mặt tuần qua. |
| F03 | Trung tâm đăng ký | Form: Nghỉ phép, Đổi ca, OT, Nghỉ ko lương. Theo dõi hạn mức phép năm. | Là NV, tôi muốn gửi đơn xin nghỉ ngay trên điện thoại. |
| F04 | Giải trình cá nhân | Case: Giải trình muộn/sớm kèm ảnh. Case: Tự động khóa nút giải trình sau ngày chốt công. | Là NV, tôi muốn giải trình lỗi công để giữ chuyên cần. |
| F05 | Báo cáo cá nhân | Score chuyên cần, Tổng giờ làm tháng, Bảng KPI Highlights. | Là NV, tôi muốn theo dõi KPI năng lực quý của mình. |
| F06 | Setup Hồ sơ | Quy trình 3 bước: Thông tin cá nhân ➔ Định danh khuôn mặt AI ➔ Hoàn tất. | Là NV mới, tôi muốn tự đăng ký khuôn mặt để điểm danh. |

### **6. YÊU CẦU PHI CHỨC NĂNG**

- Giao diện  Web/Mobile Mini App, hỗ trợ đa nền tảng (iOS/Android).
- Đồng bộ dữ liệu khuôn mặt sang Camera AI thành công trong vòng < 60 giây.
- Thông báo Push Notification ngay khi trạng thái đơn phê duyệt thay đổi.
- Bảo mật thông tin khuôn mặt chỉ dùng cho định danh chấm công.

### **7. ĐIỀU KIỆN GIẢ ĐỊNH**

- Nhân viên đã được cấp tài khoản định danh trên hệ thống Stratos.
- Smartphone của nhân viên có camera hoạt động để thực hiện định danh (Enrollment).
