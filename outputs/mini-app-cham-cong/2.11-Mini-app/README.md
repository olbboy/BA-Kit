# 2.11 Mini app

---

### **1. MỤC TIÊU**

Hệ thống ra đời nhằm giải quyết bài toán chấm công thủ công thiếu minh bạch và chậm trễ trong việc cập nhật dữ liệu cho nhân viên.

- **Lý do tồn tại:** Tự động hóa việc ghi nhận công sức thông qua công nghệ AI Vision, giúp minh bạch hóa quyền lợi giữa NV và công ty.
- **Bài toán:** Loại bỏ việc "quên chấm công", giảm sai sót khi tính lương và tối ưu luồng đơn từ phê duyệt (Nghiệp phép, OT, Công tác).
- **Giá trị mang lại:** Giảm 70% khối lượng công việc đối soát cho HR, tăng 100% tính minh bạch dữ liệu cho nhân viên.** **

### **2.**** DANH SÁCH TÍNH NĂNG**

**Module 01: Chấm công & Nhật ký**

- Dashboard Trạng thái: Hiển thị mốc giờ Vào/Ra thực tế; Badge [Đã chấm công/Chưa chấm công].
- Thanh Tiến độ làm việc: Tính toán % dựa trên Giờ hiện tại so với Giờ vào của ca.
- Nhật ký Accordion: Tra cứu mốc quẹt kèm ảnh Face ID của 30 ngày gần nhất.
- Logic Ca Đêm (20h - 06h):    - Mốc quẹt từ 20:00 (Ngày T) đến 06:00 (Ngày T+1) được gán vào Nhật ký của Ngày T.
    - Thanh tiến độ tiếp tục chạy xuyên đêm (không bị reset tại mốc 24:00).

**Module 02: Trung tâm Đăng ký**

- Đăng ký nghỉ: Nghỉ phép (trừ quỹ phép), Nghỉ không lương, Nghỉ ốm/thực tế.
- Đổi ca & OT: Cho phép NV chọn ngày và ca cần đổi; Đăng ký làm thêm giờ (OT) kèm mốc thời gian cụ thể (Ví dụ: 18:00 - 20:00).
- Ràng buộc: Chặn đăng ký trùng ngày/giờ; Chặn xóa đơn đã được Duyệt.

**Module 03: Giải trình công**

- Tạo đơn giải trình: Bổ sung mốc giờ In/Out còn thiếu do lỗi thiết bị hoặc quên quẹt.
- Logic: Sau khi HR duyệt đơn ➔ Hệ thống tự động cập nhật giờ giải trình vào Nhật ký (Module 01) và tính lại trạng thái "Đủ công".

**Module 04: Báo cáo cá nhân**

- Thống kê hiệu suất: Tỷ lệ đi làm đúng giờ (%); Số ngày nghỉ trong tháng; Tổng giờ OT lũy kế.
- Cập nhật dữ liệu: Real-time ngay khi có mốc quét camera hoặc đơn từ được Phê duyệt.

**Module 05: Quản lý Nhân sự & Cơ cấu tổ chức**

- Danh bạ NV: Quản lý họ tên, Email, ID, Phòng ban, Trạng thái (Active/Inactive).
- Theo dõi hiện diện: Dashboard hiển thị ai đang có mặt, ai đang vắng mặt hoặc đang làm Work From Home.
- Bulk Import: Nhập danh sách NV mới từ Excel mẫu (.xlsx). Hệ thống Validate Mã nhân viên và Email duy nhất.

**Module 06: Quản lý Ca làm việc & Phân ca**

- Thư viện Ca: Cấu hình Ca Sáng, Ca Chiều, Ca Đêm (Bắt đầu T -> Kết thúc T+1).
- Import Phân ca: HR Import file Excel gán ca cho từng NV theo ngày trong tuần/tháng.

**Module 07: Cấu hình Lịch & Ngày nghỉ đặc biệt**

- Lịch Lễ: Tính công mặc định (Hợp lệ) cho toàn bộ NV vào các ngày lễ quốc gia.
- Chế độ đặc biệt: Đưa ra quy tắc cho phép đăng ký WFH (Làm việc tại nhà), Đi công tác, Nghỉ sinh nhật (được hưởng lương).

**Module 8: Quản lý & Cấu hình Camera AI**

- 
Định danh thiết bị: Mỗi Camera gắn với một Location ID (Văn phòng, Cổng ra vào, Tầng). Khi camera quét mặt, dữ liệu gửi về server sẽ kèm theo ID này để xác định vị trí chấm công trong Nhật ký (Module 01).

- 
Xử lý trùng lặp (De-duplication): Nếu một nhân viên đứng trong vùng quét và bị Camera ghi nhận nhiều lần trong 1 khoảng thời gian ngắn (ví dụ < 30 giây), hệ thống chỉ lấy mốc thời gian sớm nhất để đẩy lên App.

- 
Health Check: Hệ thống tự động kiểm tra tín hiệu (Heartbeat) của camera mỗi 5 phút. Nếu mất tín hiệu, gửi cảnh báo ngay cho bộ phận IT/Admin.

**Module 09: Cấu hình Thông báo**

- 
Kênh thông báo (Channels): Hỗ trợ đa kênh gồm App Push Notification (ưu tiên), Email (cho các đơn từ cần lưu trữ) và Popup Dashboard.

- 
Điều kiện kích hoạt (Triggers):
    - 
Sự kiện chấm công: Thông báo thành công ngay khi Camera nhận diện xong (< 60s).

    - 
Sự kiện đơn từ: Trạng thái đơn thay đổi (Chờ duyệt -> Đã duyệt/Từ chối).

    - 
Sự kiện định kỳ: Nhắc nhở chấm công đầu/cuối ca hoặc thông báo lịch nghỉ lễ/tết diện rộng.

- 
Ràng buộc: Cho phép nhân viên tắt/mở thông báo nhắc nhở cá nhân, nhưng không được tắt các thông báo quan trọng liên quan đến kết quả phê duyệt đơn từ và kỷ luật lao động.

**Module 10: Trung tâm Phê duyệt**

- Luồng Duyệt: Manager Duyệt đơn của NV thuộc team ➔ HR Duyệt cuối hoặc Duyệt đơn nhạy cảm (Giải trình/Hủy công).
- Phản hồi: Lưu trữ lý do từ chối (Rejection Reason) gửi về App cho nhân viên.

**Module 11: Báo cáo tổng & Xuất dữ liệu**

- Manager Dashboard: Biểu đồ tỷ lệ chuyên cần theo phòng ban; Danh sách NV đi muộn/về sớm nhiều nhất.
- Excel Export: Xuất bảng công tổng hợp (Attendance Report) có cấu trúc phù hợp để tính lương.


**Module 12: Quản trị hệ thống**

- Quản lý chi nhánh: CRUD site (Tên, Mã, Timezone, Ngày chốt công). Deactivate site khi thu hẹp.
- Audit Log: Xem toàn bộ nhật ký hoạt động hệ thống. Filter theo user, module, action, time range. Export CSV.
- Employee Offboarding: Quy trình 7 bước tự động khi NV nghỉ việc (cancel đơn, freeze phép, deactivate camera, re-route approval).

### **3. USE CASE DIAGRAM**

```mermaid
graph LR
    subgraph actors [" 👥 Vai trò người dùng "]
        NV(["🧑‍💼 Nhân viên"])
        MGR(["👔 Quản lý"])
        HR(["📋 HR Admin"])
        IT(["🔧 IT Admin"])
        BGD(["🏛️ Ban Giám đốc"])
        SYS(["⚙️ System Admin"])
    end

    subgraph ess [" 📱 Nhân viên tự phục vụ "]
        M01["<b>01</b> · Chấm công<br/>& Nhật ký"]
        M02["<b>02</b> · Trung tâm<br/>Đăng ký"]
        M03["<b>03</b> · Giải trình<br/>công"]
        M04["<b>04</b> · Báo cáo<br/>cá nhân"]
    end

    subgraph admin [" 🛠️ Quản trị & Cấu hình "]
        M05["<b>05</b> · Quản lý<br/>Nhân sự"]
        M06["<b>06</b> · Ca làm việc<br/>& Phân ca"]
        M07["<b>07</b> · Lịch nghỉ<br/>& Ngày lễ"]
        M08["<b>08</b> · Camera<br/>AI"]
        M09["<b>09</b> · Cấu hình<br/>Thông báo"]
    end

    subgraph wf [" ✅ Quy trình & Báo cáo "]
        M10["<b>10</b> · Trung tâm<br/>Phê duyệt"]
        M11["<b>11</b> · Báo cáo tổng<br/>& Xuất dữ liệu"]
    end

    subgraph sys [" 🔐 Quản trị hệ thống "]
        M12["<b>12</b> · Quản trị<br/>hệ thống"]
    end

    NV --> M01 & M02 & M03 & M04
    MGR --> M01 & M10 & M11
    HR --> M05 & M06 & M07 & M09 & M10 & M11
    IT --> M08 & M09
    BGD --> M11
    SYS --> M12
    HR --> M12

    style actors fill:none,stroke:#546E7A,stroke-width:2px,stroke-dasharray:5
    style ess fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    style admin fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    style wf fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20
    style sys fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px,color:#4A148C

    classDef actorNode fill:#37474F,color:#fff,stroke:#263238,stroke-width:2px,font-size:13px
    classDef essNode fill:#BBDEFB,stroke:#1565C0,color:#0D47A1,stroke-width:1px
    classDef adminNode fill:#FFE0B2,stroke:#E65100,color:#BF360C,stroke-width:1px
    classDef wfNode fill:#C8E6C9,stroke:#2E7D32,color:#1B5E20,stroke-width:1px
    classDef sysNode fill:#E1BEE7,stroke:#6A1B9A,color:#4A148C,stroke-width:1px

    class NV,MGR,HR,IT,BGD,SYS actorNode
    class M01,M02,M03,M04 essNode
    class M05,M06,M07,M08,M09 adminNode
    class M10,M11 wfNode
    class M12 sysNode
```
