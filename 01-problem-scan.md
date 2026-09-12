# 01 — Problem Scan &amp; Quick Cards

> Deliverable cá nhân — Phase 1 (SCAN) + Phase 2 (QUICK-ASSESS) từ `01-worksheet.md`.

---

## Phase 1 — SCAN

### 📝 List bài toán của tôi:

| # | Subsidiary (VinFast/Xanh SM...) | Lens | Mô tả ngắn bài toán |
|---|----------------------------------|------|---------------------|
| 1 | Vinhomes | Lặp lại | Phân loại & điều hướng phản ánh cư dân (mất nước, ồn ào, an ninh, phí quản lý...) từ App Vinhomes Resident — hiện Ban quản lý đọc và gắn thẻ thủ công từng ticket. |
| 2 | Xanh SM | Tốn thời gian | Điều phối viên xử lý thủ công sự cố pin/hết pin thực địa của tài xế, tra cứu trạm sạc trống bằng tay. |
| 3 | VinFast | Lặp lại | Đối chiếu hóa đơn sạc điện hằng tuần từ hàng nghìn trụ sạc liên kết ngoài với hệ thống tài chính nội bộ. |
| 4 | Vinmec | Pain từ người khác | Bác sĩ mất 20-30 phút/bệnh nhân để soạn tóm tắt hồ sơ xuất viện bằng tay, gây quá tải. |
| 5 | Vinpearl | Pain từ người khác | Quản lý phải tự đọc review trên Booking.com/Agoda/Google Map để lọc ra phàn nàn khẩn cấp. |

---

## Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

### Card #1 — Vinhomes: Phân loại &amp; điều hướng phản ánh cư dân *(lựa chọn Deep-Dive)*

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                        │
│                                                               │
│ Bài toán (1 câu): Ban quản lý đọc và tự tay gắn thể loại/     │
│ điều hướng từng phản ánh cư dân gửi qua App Vinhomes Resident.│
│ Công ty thành viên: [x] Vinhomes  [ ] VinFast  [ ] Xanh SM   │
│                     [ ] Vinmec    [ ] Khác_________          │
│                                                               │
│ Ai đang đau (Actor)? Nhân viên Ban quản lý (quá tải khi đông  │
│ ticket); cư dân (chờ lâu do gắn nhãn/điều hướng sai).         │
│                                                               │
│ Workflow thủ công hiện tại (4 bước):                         │
│   1. Cư dân gửi ticket ──> 2. BQL đọc, phân loại thủ công    │
│   ──> 3. Tra bộ phận phù hợp ──> 4. Soạn & chuyển ticket     │
│                                                               │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2-3 (⏱ ~7 phút/lượt,   │
│ gắn nhãn không đồng nhất giữa các nhân viên)                 │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2-3 (phân loại +   │
│ soạn nháp điều hướng)                                        │
│                                                               │
│ Đo thành công bằng gì (Metric có số)?                        │
│   "Giảm thời gian điều hướng từ ~10 phút ──> dưới 30 giây"   │
│                                                               │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent  │
└─────────────────────────────────────────────────────────────┘
```

### Card #2 — Xanh SM: Xử lý sự cố pin thực địa

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                        │
│                                                               │
│ Bài toán: Tài xế báo hết pin, điều phối viên tra cứu trạm     │
│ sạc trống thủ công rồi soạn tin chỉ dẫn.                     │
│ Công ty thành viên: [x] Xanh SM (GSM)                        │
│                                                               │
│ Ai đang đau? Tài xế (chờ đợi), Điều phối viên (quá tải)      │
│                                                               │
│ Workflow thủ công hiện tại (5 bước):                         │
│   1. Nhận báo hết pin ──> 2. Tra GPS xe ──> 3. Tra trạm sạc  │
│   trống ──> 4. Soạn tin chỉ dẫn ──> 5. Gọi cứu hộ nếu cần    │
│                                                               │
│ Bước nào tốn nhất? Bước 3-4 (⏱ 10 phút/lượt)                 │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 3-4               │
│                                                               │
│ Đo thành công bằng gì (Metric có số)?                        │
│   "Giảm thời gian xử lý sự cố từ 15 phút ──> dưới 3 phút"    │
│                                                               │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent  │
└─────────────────────────────────────────────────────────────┘
```

### Card #3 — VinFast: Đối chiếu hóa đơn sạc điện

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                        │
│                                                               │
│ Bài toán: So khớp dữ liệu sạc điện hằng tuần từ hàng nghìn   │
│ trụ sạc đối tác với hóa đơn tài chính nội bộ.                │
│ Công ty thành viên: [x] VinFast                              │
│                                                               │
│ Ai đang đau? Nhân viên tài chính đối soát (làm tay từng dòng)│
│                                                               │
│ Workflow thủ công hiện tại (4 bước):                         │
│   1. Export data trụ sạc ──> 2. Export hóa đơn nội bộ ──>    │
│   3. So khớp tay trên Excel ──> 4. Ghi chú lệch/sai sót      │
│                                                               │
│ Bước nào tốn nhất? Bước 3 (⏱ nhiều giờ/tuần, dễ sai do số    │
│ lượng dòng lớn)                                              │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 3 — nhưng đây là  │
│ bài toán so khớp dữ liệu có cấu trúc, không cần ngôn ngữ tự  │
│ nhiên → Rule/script đối soát tự động hợp lý hơn dùng LLM.    │
│                                                               │
│ Đo thành công bằng gì (Metric có số)?                        │
│   "Giảm thời gian đối soát từ vài giờ ──> vài phút/tuần"     │
│                                                               │
│ Quick Architecture: [ ] No AI  [x] Rule  [ ] LLM  [ ] Agent  │
└─────────────────────────────────────────────────────────────┘
```

**Ghi chú lựa chọn:** Card #1 (Vinhomes) được chọn cho Deep-Dive vì: (a) không trùng với worked example của lớp (Xanh SM battery — Card #2 ở đây), (b) có ranh giới an toàn rõ, dễ kiểm chứng bằng code (phí/tranh chấp luôn phải escalate), phù hợp để lập trình + stress-test ở Phase 4. Card #3 giữ lại để đối chiếu — minh hoạ trường hợp Rule-based thắng LLM (theo đúng nguyên tắc "Problem First, AI Second" trong `03-inspiration-kit.md`).
