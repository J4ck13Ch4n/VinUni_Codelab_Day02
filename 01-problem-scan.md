# 01 — Problem Scan & Quick Cards

**Lab 02: AI Product Scoping — Vin Smart Future**
**Vai trò:** AI Product Engineer, Vin Smart Future
**Mảng khảo sát chính:** Vinhomes — Quản lý vận hành đô thị

---

## 🏛️ Bối cảnh khảo sát

Vin Smart Future được giao rà soát cơ hội tự động hoá tại khối vận hành các công ty thành viên. Nhóm chúng tôi tập trung khảo sát **Ban quản lý toà nhà Vinhomes**, nơi mỗi ngày tiếp nhận hàng trăm phản ánh của cư dân gửi qua app Vinhomes Resident dưới dạng **văn bản tiếng Việt tự do**.

Quan sát cốt lõi: phần mềm đã số hoá được khâu *tiếp nhận*, nhưng khâu *hiểu và điều hướng* vẫn hoàn toàn nằm trong đầu nhân viên trực hàng đợi. Đây chính là chỗ rò rỉ hiệu suất.

---

# 🔍 Phase 1 — SCAN: Quét cơ hội bằng 4 Lenses

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|---|---|---|
| 1 | **Vinhomes** | Lặp lại | Nhân viên ban quản lý đọc từng phản ánh text tự do trên app, gắn nhãn danh mục thủ công rồi tra bảng phân công để chuyển đúng bộ phận. Lặp lại vài trăm lần mỗi ngày trên mỗi cụm toà nhà. |
| 2 | **Vinhomes** | Tốn thời gian | Soạn phản hồi cho khiếu nại phí quản lý: phải mở hợp đồng từng căn, tra biểu phí, đối chiếu lịch sử đóng phí rồi mới viết được câu trả lời. |
| 3 | **Vinhomes** | Pain từ người khác | Vé bị route nhầm bộ phận nên bị đá qua lại giữa tổ kỹ thuật, tổ vệ sinh và nhà thầu. Cư dân phải nhắc lại nhiều lần, nhân viên bị khiển trách oan. |
| 4 | **VinFast** | Lặp lại | Đối chiếu hoá đơn sạc điện hằng tuần từ hàng nghìn trụ sạc đối tác với số liệu gửi về hệ thống tài chính. |
| 5 | **Vinmec** | Tốn thời gian | Bác sĩ soạn tóm tắt hồ sơ xuất viện thủ công, mất 20-30 phút mỗi bệnh nhân, trong khi phần lớn nội dung đã nằm sẵn trong bệnh án điện tử. |
| 6 | **Vinpearl** | AI có thể tốt hơn | Quét review trên Booking, Agoda, Google Maps để lọc ra phàn nàn khẩn cấp gửi về quản lý khu nghỉ, hiện làm thủ công và chậm vài ngày. |

**Nhận xét sau khi quét:** ba bài toán đầu thực chất là ba mặt của *cùng một* bottleneck tại Vinhomes. Bài toán #1 là nguyên nhân gốc, #2 và #3 là hệ quả. Xử lý được #1 thì #3 giảm theo, còn #2 phải để riêng vì chạm vào tiền và hợp đồng.

---

# 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

Chọn top 3 từ bảng SCAN: **#1 (Vinhomes triage vé), #2 (Vinhomes khiếu nại phí), #5 (Vinmec tóm tắt xuất viện).**

## Card #1 — Phân loại & điều hướng phản ánh cư dân

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Phản ánh của cư dân gửi qua app Vinhomes Resident │
│ phải được ban quản lý đọc, phân loại và chuyển tay thủ công │
│ đến đúng bộ phận xử lý.                                     │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau? Nhân viên ban quản lý trực hàng đợi vé.        │
│ Cư dân chịu hậu quả gián tiếp khi vé bị chuyển sai chỗ.     │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Cư dân gửi phản ánh text tự do trên app                │
│   → 2. NV ban quản lý đọc toàn văn trong hàng đợi           │
│   → 3. Gắn nhãn danh mục thủ công                           │
│   → 4. Tra bảng phân công, chọn bộ phận / nhà thầu          │
│   → 5. Chuyển vé kèm ghi chú tóm tắt                        │
│                                                             │
│ Bước nào tốn nhất? Bước 3 và 4 (⏱ ~7 phút/vé)               │
│ AI có thể nhảy vào ở bước nào? Bước 3 và 4                  │
│ (Phân loại danh mục + đề xuất bộ phận, ở dạng nháp)         │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│ ≥90% vé không nhạy cảm được phân loại và đề xuất route đúng;│
│ thời gian triage từ ~11 phút giảm xuống dưới 30 giây/vé.    │
│                                                             │
│ Quick Architecture: [x] LLM Feature                         │
└─────────────────────────────────────────────────────────────┘
```

## Card #2 — Soạn phản hồi khiếu nại phí quản lý

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Nhân viên phải tra hợp đồng và biểu phí từng căn  │
│ hộ để soạn phản hồi cho khiếu nại về phí quản lý.           │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau? NV ban quản lý và bộ phận tài chính cụm.       │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Nhận khiếu nại phí                                     │
│   → 2. Mở hợp đồng + biểu phí + lịch sử đóng phí của căn    │
│   → 3. Đối chiếu, xác định cư dân đúng hay sai              │
│   → 4. Soạn phản hồi, xin duyệt trưởng ban rồi gửi          │
│                                                             │
│ Bước nào tốn nhất? Bước 2 và 3 (⏱ ~18 phút/vé)              │
│ AI có thể nhảy vào ở bước nào? Chỉ bước 2 (gom dữ liệu),    │
│ tuyệt đối không bước 3 vì đó là phán quyết tài chính.       │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│ Giảm thời gian gom dữ liệu từ 18 phút xuống dưới 5 phút.    │
│                                                             │
│ Quick Architecture: [x] Rule / State-Machine                │
│ (truy vấn dữ liệu có cấu trúc, không cần LLM phán đoán)     │
└─────────────────────────────────────────────────────────────┘
```

## Card #3 — Tóm tắt hồ sơ xuất viện Vinmec

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Bác sĩ soạn tóm tắt hồ sơ xuất viện thủ công cho  │
│ từng bệnh nhân, dù dữ liệu đã có trong bệnh án điện tử.     │
│ Công ty thành viên: [x] Vinmec                              │
│                                                             │
│ Ai đang đau? Bác sĩ điều trị, đang quá tải cuối ca.         │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Mở bệnh án điện tử, đọc lại diễn biến điều trị         │
│   → 2. Đối chiếu kết quả xét nghiệm và đơn thuốc            │
│   → 3. Viết tóm tắt bằng ngôn ngữ bệnh nhân hiểu được       │
│   → 4. Ký duyệt và bàn giao                                 │
│                                                             │
│ Bước nào tốn nhất? Bước 3 (⏱ ~20 phút/bệnh nhân)            │
│ AI có thể nhảy vào ở bước nào? Bước 3 (soạn nháp)           │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│ Giảm thời gian soạn từ 25 phút xuống dưới 8 phút.           │
│                                                             │
│ Quick Architecture: [x] LLM Feature                         │
└─────────────────────────────────────────────────────────────┘
```

---

# 🗳️ Quyết định lựa chọn của nhóm

Nhóm chọn **Card #1 — Phân loại & điều hướng phản ánh cư dân Vinhomes** để Deep-Dive.

## Lý do chọn Card #1

1. **Bottleneck đúng là bài toán ngôn ngữ.** Nút thắt nằm ở việc đọc hiểu tiếng Việt tự do rồi ánh xạ sang danh mục, chứ không phải ở việc tra cứu dữ liệu. Đây đúng là chỗ LLM mạnh hơn hẳn con người về tốc độ và hơn hẳn rule-based về độ phủ.
2. **Khối lượng lặp lại lớn và đều đặn.** Vé đến hằng ngày, quanh năm, nên giá trị tích luỹ nhanh thay vì phụ thuộc mùa vụ.
3. **Rủi ro cắt được bằng thiết kế, không phải bằng hy vọng.** Toàn bộ nhóm nhạy cảm được tách khỏi luồng tự động ngay từ taxonomy, và cưỡng chế bằng code chứ không chỉ bằng câu chữ trong prompt.
4. **Scope pilot gọn.** Một cụm toà nhà, bốn danh mục, không cần tích hợp hệ thống mới nào ngoài hàng đợi vé sẵn có.

## Lý do loại hai card còn lại

* **Card #2 (khiếu nại phí quản lý):** phần tốn thời gian nhất là tra cứu dữ liệu có cấu trúc, không phải hiểu ngôn ngữ. Một truy vấn cơ sở dữ liệu cộng vài rule là đủ, rẻ hơn và chính xác hơn LLM. Phần còn lại là phán quyết tài chính, thứ mà nhóm chủ trương không giao cho AI ở bất kỳ mức độ nào. Dùng LLM ở đây là dùng sai công cụ.
* **Card #3 (tóm tắt xuất viện Vinmec):** bài toán hay nhưng nằm trong lĩnh vực y tế, nơi sai sót nội dung có thể gây hại trực tiếp cho bệnh nhân. Không thành viên nào trong nhóm nắm được quy trình lâm sàng thực tế để vẽ đúng current-state workflow và đặt ranh giới an toàn có trách nhiệm. Chọn bài mình không hiểu nghề sẽ cho ra một bản scoping đẹp nhưng sai.

## Phản biện với ví dụ mẫu của lab

File `02-deliverable-example.md` dùng chính bài toán Vinhomes này làm ví dụ về một card **bị loại**, với lý do rủi ro sai sót liên quan phí quản lý và tranh chấp căn hộ có thể dẫn tới khiếu nại pháp lý.

Nhóm đồng ý với chẩn đoán nhưng không đồng ý với kết luận. Rủi ro đó không nằm đều trên toàn bộ bài toán, nó tập trung ở hai danh mục cụ thể. Cách xử lý đúng là **thu hẹp scope**, không phải bỏ cả bài toán:

* `phi_quan_ly` và `tranh_chap` bị tách khỏi luồng tự động ngay ở tầng taxonomy, giữ human-only vô thời hạn.
* Việc tách đó được cưỡng chế bằng hàm `validate_boundaries()` chạy sau khi parse output, không phụ thuộc vào việc model có ngoan hay không.
* Phần còn lại, gồm mất nước, hỏng đèn, ồn ào, vệ sinh, là các danh mục không chạm tới tiền và hợp đồng, và chiếm phần lớn khối lượng vé.

Nói cách khác, phần rủi ro cao bị cắt ra khỏi phạm vi, phần khối lượng lớn và rủi ro thấp được giữ lại. Chi tiết lập luận và bằng chứng kiểm thử nằm ở `02-deep-dive-report.md`.
