# US-APPR-03: Phê duyệt hàng loạt

---

**AS A** Quản lý / HR Admin,  
**I WANT TO** chọn nhiều đơn cùng loại và duyệt hoặc từ chối hàng loạt trong một thao tác,  
**SO THAT** tôi có thể xử lý ≤ 50 đơn/lần trong ≤ 3 giây khi có nhiều đơn tồn đọng, đặc biệt cuối tháng trước ngày chốt công.

---

### **1. BUSINESS FLOW**

1. **Chọn đơn:** Approver tick checkbox trên nhiều đơn trong inbox (cùng loại).
2. **Chọn hành động:** "Duyệt tất cả" hoặc "Từ chối tất cả".
3. **Xác nhận:**
   - Duyệt: Hiển thị tóm tắt "Duyệt X đơn [Loại]?" → Confirm.
   - Từ chối: Nhập lý do chung (áp dụng cho tất cả đơn) → Confirm.
4. **Xử lý:** Hệ thống xử lý từng đơn → Hiển thị kết quả: Thành công X / Thất bại Y.
5. **Thông báo:** Mỗi NV nhận Push riêng về kết quả đơn của mình.

---

### **2. ACCESS CONTROL (RBAC/ABAC)**

| Thông tin (Data Field) | Role (Access Right) | Ghi chú |
| --- | --- | --- |
| Batch approve/reject | MANAGER, DEPT_HEAD, SITE_HR, GLOBAL_HR | Chỉ xử lý đơn thuộc quyền duyệt. |
| Chọn nhiều đơn | Approver | Chỉ chọn đơn cùng loại trong 1 batch. |

---

### **3. TIÊU CHÍ CHẤP NHẬN (ACCEPTANCE CRITERIA)**

#### **AC1. Chọn đơn hàng loạt**

- Checkbox trên mỗi dòng đơn; "Chọn tất cả" cho trang hiện tại.
- Chỉ cho phép batch đơn cùng loại (VD: tất cả Leave hoặc tất cả OT).
- Hiển thị counter: "Đã chọn X đơn".
- Nút "Duyệt tất cả" và "Từ chối tất cả" chỉ hiện khi ≥ 1 đơn được chọn.

#### **AC2. Xử lý Batch**

- Hệ thống xử lý tuần tự từng đơn (đảm bảo validation riêng cho từng đơn).
- **Case thất bại:** Đơn A duyệt thành công, Đơn B thất bại (NV hết phép) → Đơn A vẫn APPROVED, Đơn B báo lỗi riêng.
- Không rollback đơn đã xử lý thành công.

#### **AC3. Kết quả Batch**

- Modal kết quả:
  - Thành công: X đơn ✅
  - Thất bại: Y đơn ❌ (kèm lý do từng đơn)
- Nút "Xem đơn thất bại" → Lọc inbox chỉ hiển thị đơn lỗi.

#### **AC4. Giới hạn**

- Tối đa 50 đơn/batch (tránh timeout).
- Thời gian xử lý ≤ 3 giây cho 50 đơn.
- Nếu > 50 đơn: Hiển thị "Vui lòng chọn tối đa 50 đơn mỗi lần".

---

### **4. DEFINITION OF DONE (DOD)**

1. **Partial success:** Batch 10 đơn, 2 thất bại → 8 đơn APPROVED + 2 báo lỗi.
2. **Thông báo:** Mỗi NV nhận Push riêng (không gom thành 1 thông báo batch).
3. **Hiệu năng:** 50 đơn ≤ 3 giây.
4. **QA:** Kiểm thử batch approve Leave, OT, Correction; case mixed success/failure.

---

### EDGE CASES & ERROR HANDLING

| # | Case | Severity | Expected Behavior |
|---|------|----------|-------------------|
| AP03-E1 | **Batch approve lỗi giữa chừng** — Đơn thứ 25/50 bị lỗi | MEDIUM | Xử lý tuần tự, không rollback đã duyệt. Kết quả: "24 ✓, 1 ✗, 25 ○". Retry riêng đơn lỗi. |
| AP03-E2 | **Batch quá lớn** — Chọn > 50 đơn | LOW | Chặn: "Tối đa 50 đơn/lần. Đã chọn [N]." |
| AP03-E3 | **Đơn bị cancel khi đang trong batch** — NV hủy đơn ngay lúc manager batch approve | MEDIUM | Check status trước khi approve. Đơn CANCELLED → skip, ghi nhận "Đã bị hủy bởi NV." |
