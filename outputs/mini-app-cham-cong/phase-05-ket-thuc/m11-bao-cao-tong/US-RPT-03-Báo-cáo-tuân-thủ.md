# US-RPT-03: Báo cáo tuân thủ

---

**AS A** HR Admin,  
**I WANT TO** xem báo cáo tuân thủ quy chế lao động: vi phạm chuyên cần, giới hạn OT theo Nghị định 13/2023, và giải trình quá hạn,  
**SO THAT** tôi có thể đảm bảo công ty tuân thủ pháp luật lao động Việt Nam và xử lý kịp thời các trường hợp vi phạm.

---

### **1. BUSINESS FLOW**

1. **Truy cập:** HR mở "Báo cáo tổng" → Tab "Tuân thủ".
2. **Hiển thị:** 3 phần chính: Vi phạm chuyên cần, Giới hạn OT, Giải trình quá hạn.
3. **Lọc:** Theo kỳ (tháng/quý), phòng ban, chi nhánh, mức độ nghiêm trọng.
4. **Xuất:** Export báo cáo tuân thủ dạng Excel/PDF.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Báo cáo vi phạm team | MANAGER, DEPT_HEAD | Chỉ xem data team/phòng. |
| Báo cáo tuân thủ site | SITE_HR | Xem toàn site. |
| Báo cáo tuân thủ toàn hệ thống | GLOBAL_HR, SYS_ADMIN | Xem tất cả. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Báo cáo vi phạm chuyên cần**

- Danh sách NV có vi phạm trong kỳ: Đi trễ, Về sớm, Vắng mặt không phép.
- Mỗi dòng: Mã NV, Tên, Phòng ban, Số lần trễ, Số lần sớm, Số ngày vắng, Tổng phút trễ.
- Phân loại mức độ:
  - **Nhẹ:** 1-3 lần trễ/tháng (Vàng).
  - **Trung bình:** 4-6 lần trễ/tháng (Cam).
  - **Nghiêm trọng:** > 6 lần trễ hoặc vắng không phép (Đỏ).

#### **AC2. Giới hạn OT theo Nghị định 13/2023**

- Bảng tổng hợp OT lũy kế:
  - Cột: Mã NV, Tên, OT tháng (giới hạn 40h), OT năm (giới hạn 200h/300h), % sử dụng.
  - Badge: Xanh (< 80%), Vàng (80-99%), Đỏ (≥ 100%).
- Cảnh báo: Danh sách NV đang ≥ 80% giới hạn OT (cần theo dõi).
- Vi phạm: Danh sách NV đã vượt giới hạn (cần xử lý ngay).

#### **AC3. Giải trình quá hạn**

- Danh sách NV có lỗi chấm công chưa giải trình và đã qua ngày chốt công.
- Mỗi dòng: Mã NV, Tên, Ngày vi phạm, Loại lỗi, Trạng thái (VI PHẠM QUY CHẾ).
- Tổng hợp: X NV có giải trình quá hạn trong kỳ.

#### **AC4. Xuất báo cáo tuân thủ**

- Định dạng: Excel (.xlsx) với 3 sheet (Vi phạm, OT, Giải trình).
- Header: Tên công ty, Chi nhánh, Kỳ báo cáo, Ngày xuất.
- Phục vụ: Nộp cho thanh tra lao động khi có yêu cầu.

---

### **4. DEFINITION OF DONE (DOD)**

1. **OT limit:** Dữ liệu OT lũy kế phải khớp với tổng từ OvertimeRequest APPROVED.
2. **Vi phạm:** Mức độ phân loại chính xác theo ngưỡng đã cấu hình.
3. **Giải trình:** Danh sách quá hạn phải khớp với logic ngày chốt công (Module 10).
4. **QA:** Kiểm thử xuất báo cáo; NV không có vi phạm → Không xuất hiện; NV OT vượt → Badge đỏ.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| RT03-E1 | **OT vượt giới hạn pháp luật** — NV > 200h/năm | CRITICAL | Highlight đỏ trong báo cáo. Alert HR + Ban Giám đốc. Ghi nhận risk: "Vi phạm ND 13/2023 Điều [X]." |
| RT03-E2 | **Nghỉ phép vượt quota** — NV nghỉ > số phép cho phép (do approved nhầm) | HIGH | Flag trong báo cáo: "Vượt hạn mức [N] ngày." Gợi ý: trừ lương hoặc chuyển sang nghỉ không lương. |
| RT03-E3 | **Data discrepancy** — Tổng ngày công dashboard ≠ file export | HIGH | Checksum validation trước khi export. Nếu khác biệt > 0.5 ngày → alert: "Dữ liệu không nhất quán. Liên hệ IT." |
