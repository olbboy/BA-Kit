# US-RPT-04: Khóa kỳ lương (Payroll Lock)

---

**AS A** HR Admin,  
**I WANT TO** tự động khóa dữ liệu chấm công khi xuất payroll và quản lý kỳ bổ sung cho các thay đổi sau khi khóa,  
**SO THAT** dữ liệu payroll đã xuất không bị thay đổi ngầm, đảm bảo tính toàn vẹn tài chính và tuân thủ quy trình kiểm toán nội bộ.

---

### **1. BUSINESS FLOW**

1. **Xuất payroll** (trigger): Khi HR xuất file payroll qua US-RPT-02, hệ thống đánh dấu kỳ lương = `LOCKED` cho (tháng + site).
2. **Cảnh báo thay đổi**: Sau LOCKED, mọi correction/approval cho tháng đã khóa → popup cảnh báo: "Kỳ lương tháng X đã xuất. Thay đổi sẽ được ghi vào Kỳ bổ sung."
3. **Kỳ bổ sung (Supplementary Payroll)**: Các thay đổi sau lock được tách riêng, không ghi đè lên file gốc. HR xuất "Supplementary Report" chứa chỉ các delta.
4. **Re-export**: HR có thể xuất lại toàn bộ (tạo version mới). File cũ vẫn được lưu giữ để đối chiếu.
5. **Unlock kỳ**: Chỉ GLOBAL_HR có thể unlock kỳ lương (hiếm, cho trường hợp xuất sai).

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Xuất payroll (trigger lock) | SITE_HR, GLOBAL_HR | Auto-lock khi xuất. |
| Xem trạng thái kỳ (OPEN/LOCKED) | HR Admin, Manager | HR xem toàn site; Manager xem phòng ban. |
| Xuất Supplementary Report | SITE_HR, GLOBAL_HR | Chỉ delta sau lock. |
| Re-export (tạo version mới) | GLOBAL_HR | Tạo version mới, giữ lịch sử. |
| Unlock kỳ lương | GLOBAL_HR | Chỉ dùng khi xuất sai. Audit log bắt buộc. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Auto-lock khi xuất payroll**

- Khi HR nhấn "Xuất Payroll" trong US-RPT-02, sau khi file download thành công → kỳ lương (month + year + siteId) chuyển sang `LOCKED`.
- Hiển thị badge "🔒 LOCKED" bên cạnh kỳ lương trên dashboard.
- Ghi audit log: `{actor, action: PAYROLL_EXPORT, month, site, timestamp, fileVersion: 1}`.

#### **AC2. Cảnh báo thay đổi sau lock**

- Khi approver duyệt đơn giải trình/OT/nghỉ phép cho ngày thuộc kỳ LOCKED:
  - Popup: "⚠️ Kỳ lương tháng X/YYYY đã xuất. Thay đổi sẽ được ghi vào Kỳ bổ sung. Tiếp tục?"
  - Nếu confirm → change vẫn apply nhưng ghi vào bảng `SupplementaryPayrollChanges`.
  - Nếu cancel → không thay đổi.

#### **AC3. Supplementary Payroll Report**

- Tab mới trong US-RPT-02: "Kỳ bổ sung".
- Hiển thị danh sách changes sau lock: NV, ngày, loại thay đổi, giá trị cũ → mới, người duyệt, timestamp.
- Xuất CSV/Excel riêng biệt, cấu trúc: delta (difference) format.

#### **AC4. Re-export & Versioning**

- Nút "Xuất lại" (chỉ GLOBAL_HR): tạo file mới bao gồm cả thay đổi bổ sung.
- Version tracking: v1 (original), v2 (re-export), v3... Tất cả versions lưu trong lịch sử.
- Download lại file cũ bất kỳ.

---

### **EDGE CASES & ERROR HANDLING**

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RP04-E1 | **HR xuất payroll 2 lần** — Click "Xuất" 2 lần liên tiếp | MEDIUM | Idempotent: nếu kỳ đã LOCKED → không tạo version mới. Chỉ download lại file version hiện tại. |
| RP04-E2 | **Correction approved TRƯỚC khi HR xuất** — 23:59 approve, 00:01 export | HIGH | Correction đã apply trước lock → nằm trong file gốc (v1), KHÔNG ở supplementary. Dùng timestamp so sánh. |
| RP04-E3 | **2 site cùng tháng, 1 locked 1 open** — GLOBAL_HR quản lý cả 2 | MEDIUM | Lock scope = per-site. Dashboard hiển thị rõ: Site A (LOCKED ✅), Site B (OPEN 🔓). Xuất payroll độc lập per-site. |
| RP04-E4 | **Unlock rồi re-lock** — GLOBAL_HR unlock để sửa, quên lock lại | HIGH | Auto re-lock sau 48h nếu không có export mới. Push notification: "Kỳ lương tháng X đã được mở khóa 47h. Sẽ tự khóa lại trong 1h." |

---

### **4. DEFINITION OF DONE (DOD)**

1. **Auto-lock:** Xuất payroll → kỳ LOCKED tự động. Badge hiển thị đúng.
2. **Cảnh báo:** Approve đơn cho kỳ LOCKED → popup cảnh báo → ghi supplementary.
3. **Supplementary:** Report chỉ chứa delta, export riêng biệt.
4. **Versioning:** Re-export tạo version mới. Download version cũ vẫn hoạt động.
5. **QA:** Test concurrent export, race condition approve vs lock, multi-site scope.
