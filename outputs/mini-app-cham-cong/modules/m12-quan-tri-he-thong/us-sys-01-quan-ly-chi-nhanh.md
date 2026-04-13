# US-SYS-01: Quản lý chi nhánh (Site Management)

---

**AS A** System Admin,  
**I WANT TO** thêm, sửa, deactivate chi nhánh trên hệ thống mà không cần can thiệp kỹ thuật,  
**SO THAT** công ty có thể mở rộng hoặc thu hẹp quy mô hoạt động mà hệ thống luôn phản ánh đúng cấu trúc tổ chức thực tế.

---

### **1. BUSINESS FLOW**

1. **Thêm site**: Admin nhập: Tên, Mã, Địa chỉ, Timezone, Closing date (ngày chốt công).
2. **Cấu hình ban đầu**: Gán SITE_HR_ADMIN, SITE_MANAGER cho site mới.
3. **Activate**: Site mới có status ACTIVE → hiển thị trong dropdown chọn site trên toàn hệ thống.
4. **Deactivate**: Soft-delete → site không hiển thị nhưng dữ liệu lịch sử giữ nguyên.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin | Role | Ghi chú |
| --- | --- | --- |
| CRUD Site | SYSTEM_ADMIN, SUPER_ADMIN | Chỉ admin hệ thống. |
| Xem danh sách site | Tất cả các role | Filtered theo scope (SITE_HR chỉ xem site mình). |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Thêm Site**
- Mã site: unique, alphanumeric, 3-10 ký tự.
- Timezone: dropdown chuẩn IANA (VD: Asia/Ho_Chi_Minh).
- Closing date: ngày chốt công mặc định (1-28).
- Sau tạo: site xuất hiện ngay trong dropdown chọn site.

#### **AC2. Sửa Site**
- Cho phép sửa: Tên, Địa chỉ, Closing date, Timezone.
- KHÔNG cho phép sửa: Mã site (immutable).
- Sửa closing date cảnh báo: "Thay đổi ngày chốt công ảnh hưởng [N] NV."

#### **AC3. Deactivate Site**
- Soft-delete: status → INACTIVE.
- NV thuộc site bị deactivate → cần chuyển sang site khác trước.
- Dữ liệu lịch sử (chấm công, đơn từ) vẫn truy vấn được.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| SY01-E1 | **Deactivate site có NV active** | CRITICAL | Chặn: "Site [Tên] có [N] NV active. Chuyển NV sang site khác trước." |
| SY01-E2 | **Mã site trùng** | HIGH | Validation: "Mã site [X] đã tồn tại." Chặn tạo. |
| SY01-E3 | **Sửa timezone** — Site đã có dữ liệu chấm công | MEDIUM | Cảnh báo: "Thay đổi timezone không ảnh hưởng dữ liệu lịch sử. Chỉ áp dụng cho dữ liệu mới." |

---

### **DEFINITION OF DONE (DOD)**

1. **AC Verified**: CRUD site hoạt động đúng.
2. **RBAC**: Chỉ SYSTEM_ADMIN/SUPER_ADMIN truy cập được.
3. **Data Integrity**: Deactivate không xóa dữ liệu lịch sử.
4. **Edge Cases Tested**: Site có NV, mã trùng, sửa timezone.
5. **Integration**: Site mới xuất hiện trong dropdown trên toàn hệ thống.

---

### **GHERKIN SCENARIOS**

```gherkin
Feature: US-SYS-01 — Quản lý chi nhánh
  As a System Admin
  I want to CRUD site mà không cần can thiệp kỹ thuật
  So that hệ thống phản ánh đúng cấu trúc tổ chức thực tế.

  # --- AC1: Thêm Site ---
  Scenario: AC1.1 — Tạo site mới
    Given Admin nhấn "Thêm site"
    When nhập: Mã="BD01", Tên="Bình Dương", Timezone=Asia/Ho_Chi_Minh, ClosingDay=25
    Then site ACTIVE. Xuất hiện ngay trong dropdown chọn site toàn hệ thống.

  # --- AC2: Sửa Site ---
  Scenario: AC2.1 — Sửa closing date → cảnh báo
    Given site HCM có 200 NV, closingDay=25
    When Admin sửa closingDay → 20
    Then cảnh báo: "Thay đổi ngày chốt ảnh hưởng 200 NV." Mã site immutable.

  # --- AC3: Deactivate ---
  Scenario: AC3.1 — Deactivate site không có NV
    Given site "Test" có 0 NV active
    When Admin deactivate
    Then status=INACTIVE. Dữ liệu lịch sử giữ nguyên.

  # --- Edge Cases ---
  Scenario: Edge1 — Deactivate site có NV → chặn
    Given site HCM có 200 NV active
    When Admin deactivate
    Then chặn: "Site HCM có 200 NV active. Chuyển NV sang site khác trước."

  Scenario: Edge2 — Mã site trùng
    Given mã "HCM" đã tồn tại
    When Admin tạo site mới mã "HCM"
    Then chặn: "Mã site HCM đã tồn tại."

  Scenario: Edge3 — Sửa timezone site có dữ liệu
    Given site HCM có 12 tháng dữ liệu
    When Admin sửa timezone → Asia/Bangkok
    Then cảnh báo: "Thay đổi timezone chỉ áp dụng cho dữ liệu mới."
```
