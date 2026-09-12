# 🔍 Phase 1 — SCAN (Cá nhân, 20 min)

Dùng 4 Lenses quét qua vận hành của các công ty thành viên Vingroup.

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|---|---|---|
| 1 | Xanh SM | Pain từ người khác (Stakeholder Pain) | Phân tích nội dung tin nhắn của tài xế kết hợp với dữ liệu GPS để xác định tình trạng, vị trí thực tế của xe và hỗ trợ điều phối xe đến khu vực có nhu cầu phù hợp. |
| 2 | VinFast | AI có thể tốt hơn (AI-upgrade) | Tự động đề xuất trạm sạc và thời điểm sạc phù hợp dựa trên mức pin, lộ trình, tình trạng trạm và loại cổng sạc của từng dòng xe điện. |
| 3 | Vinhomes | Lặp lại (Repetitive) | Tự động phân loại các phản ánh của cư dân như mất nước, hỏng đèn, thang máy, tiếng ồn và chuyển đến đúng bộ phận hoặc ban quản lý phụ trách. |
| 4 | Vinhomes | AI có thể tốt hơn (AI-upgrade) | Hỗ trợ cư dân tra cứu thủ tục, kiểm tra hồ sơ còn thiếu và hướng dẫn hoặc draft nhanh các yêu cầu như đăng ký thi công nội thất, thẻ xe và tiện ích. |
| 5 | Vinpearl | Tốn thời gian (Time-consuming) | Tự động tổng hợp và phân tích review từ nhiều nền tảng, phát hiện các vấn đề hoặc phàn nàn nổi bật và gửi cảnh báo đến quản lý để xử lý kịp thời. |

# 🃏 Phase 2 — QUICK-ASSESS (Cá nhân, 30 min)

Chọn **top 3 bài toán** từ danh sách trên và hoàn thiện **3 Quick Problem Cards** dưới đây (10 phút/card).

```
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Tài xế Xanh SM gửi tin nhắn báo vị trí, tình      │
│ trạng hoặc nhu cầu đón khách nhưng điều phối viên phải      │
│ đọc và xử lý thủ công.                                      │
│ Công ty thành viên: [x] Xanh SM (GSM)                       │
│                                                             │
│ Ai đang đau? Điều phối viên (quá tải), Tài xế (chờ điều     │
│ phối), Khách hàng (thời gian chờ lâu)                      │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Tài xế gửi tin nhắn báo tình trạng/vị trí              │
│   → 2. Điều phối viên đọc và xác định nội dung              │
│   → 3. Đối chiếu vị trí xe với dữ liệu nhu cầu              │
│   → 4. Gửi hướng dẫn hoặc điều phối chuyến tiếp theo       │
│                                                             │
│ Bước nào tốn nhất? Bước 2-3 (5 phút/lượt)                 │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2-3              │
│ (Phân tích tin nhắn + đối chiếu GPS + đề xuất điều phối)    │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian xử lý yêu cầu điều phối từ 5 phút ──>        │
│ dưới 1 phút/lượt.                                           │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent│
└─────────────────────────────────────────────────────────────┘

│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Tự động đề xuất trạm sạc phù hợp cho xe VinFast   │
│ dựa trên mức pin, lộ trình và tình trạng trạm sạc.          │
│ Công ty thành viên: [x] VinFast                             │
│                                                             │
│ Ai đang đau? Tài xế/Chủ xe (mất thời gian tìm trạm),        │
│ CSKH (nhiều yêu cầu hỗ trợ), Vận hành trạm (phân bổ         │
│ không tối ưu)                                               │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Người dùng kiểm tra mức pin và nhu cầu di chuyển       │
│   → 2. Tìm các trạm sạc trên bản đồ                         │
│   → 3. Kiểm tra loại cổng và tình trạng trạm                │
│   → 4. Chọn trạm và điều chỉnh lộ trình                     │
│                                                             │
│ Bước nào tốn nhất? Bước 2-4 (5 phút/lượt)                 │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2-4              │
│ (Tổng hợp dữ liệu trạm + dự đoán phù hợp + đề xuất          │
│ lộ trình)                                                   │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian tìm và lựa chọn trạm từ 5 phút ──>           │
│ dưới 1 phút/lượt.                                           │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent│
└─────────────────────────────────────────────────────────────┘

│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Phân loại và chuyển phản ánh cư dân Vinhomes      │
│ đến đúng bộ phận xử lý mà không cần nhân viên đọc thủ công. │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau? Nhân viên ban quản lý (xử lý nhiều ticket),    │
│ Cư dân (chờ phản hồi), Bộ phận kỹ thuật/vận hành             │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Cư dân gửi phản ánh qua App                             │
│   → 2. Nhân viên đọc nội dung                               │
│   → 3. Phân loại vấn đề và xác định bộ phận phụ trách       │
│   → 4. Chuyển ticket và theo dõi xử lý                      │
│                                                             │
│ Bước nào tốn nhất? Bước 2-3 (3 phút/ticket)               │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2-3              │
│ (Phân loại nội dung + xác định bộ phận + mức độ ưu tiên)    │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian phân loại và chuyển ticket từ 3 phút ──>     │
│ dưới 30 giây/ticket.                                        │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule  [ ] LLM  [ ] Agent│
└─────────────────────────────────────────────────────────────┘
```



