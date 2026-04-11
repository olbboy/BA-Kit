# US-NOTIF-04: Quản lý Template Email thông báo

---

**AS A** HR Admin,  
**I WANT TO** tạo, chỉnh sửa và quản lý các template email HTML cho từng loại thông báo hệ thống (approval, alert, reminder, welcome),  
**SO THAT** tất cả email gửi từ hệ thống có giao diện thống nhất, thương hiệu công ty, và nội dung phù hợp với ngữ cảnh — thay vì gửi email plain-text không chuyên nghiệp.

---

### **1. BUSINESS FLOW**

1. **Truy cập**: HR Admin mở "Cấu hình Thông báo" → Tab "Email Templates".
2. **Xem danh sách template**: Hiển thị danh sách template theo nhóm (Approval, Alert, Reminder, System, Welcome).
3. **Chỉnh sửa template**: HR nhấn vào template → Editor WYSIWYG mở ra. Chỉnh sửa header, body, footer, CTA button.
4. **Biến động**: HR chèn biến (VD: `{{employee_name}}`, `{{date}}`, `{{action_url}}`) bằng cách chọn từ dropdown.
5. **Preview**: HR nhấn "Xem trước" → Hiển thị email render với dữ liệu mẫu (mock data). Preview cả Desktop và Mobile layout.
6. **Publish**: HR nhấn "Lưu" → Template version mới active. Version cũ lưu lại trong lịch sử (max 10 versions).

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Tạo/Sửa template | HR_ADMIN | Nội dung tuỳ chỉnh per-tenant. |
| Duyệt template (publish) | GLOBAL_HR, SYS_ADMIN | Template system-wide cần duyệt. |
| Xem template | HR, IT Admin | Read-only. |
| Reset về mặc định | SYS_ADMIN | Rollback về template gốc hệ thống. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Danh sách templates theo nhóm**

| Nhóm | Template mẫu | Mặc định |
| --- | --- | --- |
| Approval | Đơn được phê duyệt, Đơn bị từ chối, Đơn cần duyệt (nhắc approver) | Có sẵn |
| Alert | Cảnh báo đi muộn, Cảnh báo vắng mặt, Cảnh báo OT vượt ngưỡng | Có sẵn |
| Reminder | Nhắc chấm công, Nhắc chốt công, Nhắc giải trình | Có sẵn |
| System | Camera offline, Batch job lỗi, Tài khoản bị khóa | Có sẵn |
| Welcome | Chào mừng NV mới (Onboarding), Thông báo offboarding | Có sẵn |

- Mỗi template có: ID, nhóm, tên, subject line, body HTML, biến hỗ trợ, ngày sửa cuối.
- Template mặc định (system): Không xóa được. Chỉ clone + customize.

#### **AC2. Email Template Editor (WYSIWYG)**

- Rich text editor: Bold, Italic, Link, Image, Button, Divider, Spacer.
- Layout builder: Header (logo công ty) + Body + CTA Button + Footer (disclaimer).
- **Branding config** (per-tenant):
  - Logo URL (upload hoặc URL)
  - Primary color (hex)
  - Company name
  - Footer text (mặc định: "© 2026 [Company Name]. Đây là email tự động.")
- **Biến động hỗ trợ**: `{{employee_name}}`, `{{employee_id}}`, `{{date}}`, `{{time}}`, `{{shift_name}}`, `{{request_type}}`, `{{approver_name}}`, `{{reason}}`, `{{action_url}}`, `{{company_name}}`, `{{support_email}}`.
- **Subject line**: Có riêng field nhập subject. Hỗ trợ biến. Giới hạn 150 ký tự.

#### **AC3. Preview & Test Send**

- **Preview**: Render HTML email với mock data. Hiển thị cả Desktop (600px) và Mobile (375px) layout.
- **Test Send**: Nút "Gửi email test" → Nhập email nhận → Gửi email thật với mock data. Giới hạn: 5 test/ngày/template.
- **Validation**: Kiểm tra biến chưa được điền (VD: `{{undefined_var}}`) → Cảnh báo trước khi lưu.

#### **AC4. Version History**

- Mỗi lần sửa template: Lưu version mới. Giữ tối đa 10 versions.
- HR có thể xem diff giữa 2 versions (side-by-side HTML preview).
- Nút "Rollback": Chọn version cũ → Active lại. Version hiện tại → archived.

---

### **4. DEFINITION OF DONE (DOD)**

1. **Templates**: Tất cả template mặc định (≥12) được seed khi khởi tạo tenant. Giao diện chuyên nghiệp.
2. **Branding**: Logo, màu, footer áp dụng đúng cho tất cả email gửi ra.
3. **Preview**: Desktop và Mobile preview khớp email thực tế nhận được.
4. **Biến động**: Tất cả biến được thay thế đúng khi gửi email thật. Không còn `{{...}}` raw.
5. **QA**: Kiểm thử: sửa template → preview → test send → nhận email đúng format.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| NF04-E1 | **HTML injection** — HR nhập `<script>alert()</script>` | CRITICAL | Sanitize HTML. Strip `<script>`, `<iframe>`, `onclick`. Chỉ cho phép safe HTML tags. |
| NF04-E2 | **Logo URL broken** — Logo CDN hết hạn | LOW | Fallback: hiển thị `{{company_name}}` text thay vì logo. Email vẫn gửi được. |
| NF04-E3 | **Biến không tồn tại** — HR sử dụng `{{salary}}` (không hỗ trợ) | MEDIUM | Validation trước khi lưu: "Biến `{{salary}}` không được hỗ trợ. Vui lòng xóa hoặc thay bằng biến hợp lệ." |
| NF04-E4 | **Email client compatibility** — Outlook không render CSS đúng | MEDIUM | Sử dụng inline CSS. Kiểm thử trên 5 email clients: Gmail, Outlook, Apple Mail, Yahoo, Thunderbird. |
| NF04-E5 | **Template quá lớn** — Body > 100KB (nhiều hình ảnh) | LOW | Cảnh báo: "Template quá lớn (>100KB). Email có thể bị cắt bởi Gmail." Gợi ý: giảm hình ảnh. |
