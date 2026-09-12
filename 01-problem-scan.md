# 01 — Quét cơ hội và Quick Problem Cards

Đề tài chọn: **Phân loại và điều hướng phản ánh cư dân Vinhomes**.

Tài liệu phục vụ bài lab. Các quy trình dưới đây là mô hình giả định để khảo sát, không phải mô tả đã xác nhận với doanh nghiệp. Thời gian, sản lượng và mục tiêu là giả định thiết kế; chưa có log vận hành hoặc phỏng vấn stakeholder để xác minh.

## Phase 1 — SCAN

| # | Công ty | Lens | Bài toán và bottleneck | Cơ hội hỗ trợ |
|---|---|---|---|---|
| 1 | Vinhomes | Lặp lại | Nhân viên đọc từng phản ánh mất nước, hỏng đèn, ồn ào và tìm bộ phận tiếp nhận | LLM phân loại; code tra danh mục tòa/bộ phận; nhân viên duyệt |
| 2 | Vinpearl | Tốn thời gian | Nhân viên tổng hợp đánh giá lưu trú từ nhiều nội dung tự do | Gom chủ đề và tạo bản tóm tắt có tham chiếu đánh giá gốc |
| 3 | VinFast | Lặp lại | Nhân viên đối chiếu hóa đơn dịch vụ với lệnh sửa chữa, tìm sai lệch | Quy tắc đối chiếu trường dữ liệu; AI chỉ hỗ trợ trích xuất nếu cần |
| 4 | Xanh SM | Pain từ người khác | Tài xế phải đọc lại mô tả điểm đón không rõ ràng | Tóm tắt địa điểm, yêu cầu xác minh thông tin còn thiếu |
| 5 | Vinmec | AI có thể tốt hơn | Khách hàng khó tìm hướng dẫn hành chính trước buổi khám trong nhiều tài liệu | Tra cứu nội dung đã duyệt, không tư vấn chẩn đoán hoặc điều trị |

## Phase 2 — QUICK-ASSESS

### Card 1 — Phân loại phản ánh cư dân (đề tài chọn)

- **Công ty / Actor:** Vinhomes; nhân viên ban quản lý phụ trách tiếp nhận vé.
- **Bài toán:** Rút ngắn bước đọc, gắn nhãn và đề xuất nơi tiếp nhận phản ánh tiếng Việt.
- **Quy trình giả định:** Nhận vé → đọc và xác minh tòa → phân loại → tìm bộ phận và giao vé → bộ phận xác nhận.
- **Bottleneck:** Phân loại 3 phút + tìm bộ phận 2 phút = 5 phút/vé; cách diễn đạt khác nhau dẫn đến nhãn không nhất quán.
- **AI Solution:** Gemini đề xuất nhãn; Python kiểm tra đầu ra, chặn ca nhạy cảm, tra bộ phận từ mã tòa; con người duyệt.
- **Metric mục tiêu:** ≥90% đề xuất nhãn và nơi tiếp nhận đúng trên tập vé không nhạy cảm; p95 thời gian tạo đề xuất <30 giây; thời gian thao tác triage trung vị ≤2 phút/vé.
- **Quick Architecture:** LLM Feature + Rule. Không cần agent tự hành.
- **Dữ liệu cần:** Nội dung đã khử thông tin cá nhân, mã tòa, nhãn đúng, nơi xử lý đúng, thời điểm và lịch sử chuyển giao.
- **Ranh giới:** Không tự gửi, đóng vé, hoàn tiền hoặc phán xử tranh chấp. Mọi kết quả là bản nháp.
- **Lý do chọn:** Scope đủ nhỏ để kiểm chứng bằng một script, có tiêu chí kiểm thử ranh giới rõ ràng.

### Card 2 — Tổng hợp đánh giá lưu trú

- **Công ty / Actor:** Vinpearl; quản lý trải nghiệm khách hàng.
- **Bài toán:** Tạo bản tổng hợp chủ đề phản hồi để quản lý xác định vấn đề cần kiểm tra.
- **Quy trình giả định:** Xuất đánh giá → đọc → gắn chủ đề → tổng hợp báo cáo → quản lý kiểm tra.
- **Bottleneck:** Đọc và nhóm 50 đánh giá mất khoảng 60 phút/báo cáo.
- **AI Solution:** LLM nhóm chủ đề và tóm tắt; mỗi kết luận gắn ID đánh giá nguồn, người dùng đối chiếu trước khi dùng.
- **Metric mục tiêu:** Tổng thời gian tạo và duyệt báo cáo ≤20 phút/50 đánh giá; ≥95% nhận định được hỗ trợ bởi nội dung nguồn trong tập kiểm thử.
- **Quick Architecture:** LLM Feature; code đếm số lượng và kiểm tra ID nguồn.
- **Dữ liệu cần:** Đánh giá giả lập/đã khử PII, thang điểm, ngày và danh mục chủ đề.
- **Ranh giới:** Không bịa số liệu, không suy diễn danh tính, không tự phản hồi khách hoặc hứa bồi thường.
- **Đánh giá nhanh:** Tiềm năng tốt nhưng cần rubric chấm tính trung thực của bản tóm tắt; ưu tiên sau Card 1.

### Card 3 — Đối chiếu hóa đơn dịch vụ

- **Công ty / Actor:** VinFast; nhân viên kế toán/đối soát dịch vụ.
- **Bài toán:** Phát hiện sai lệch giữa hóa đơn và lệnh sửa chữa.
- **Quy trình giả định:** Nhận hóa đơn → tìm lệnh sửa chữa → đối chiếu mã/số lượng/đơn giá → đánh dấu sai lệch → nhân viên xác nhận.
- **Bottleneck:** Đối chiếu thủ công khoảng 8 phút/hóa đơn.
- **AI Solution:** Bắt đầu bằng rule so khớp dữ liệu có cấu trúc; chỉ bổ sung trích xuất tài liệu khi đầu vào là ảnh/PDF không có trường dữ liệu.
- **Metric mục tiêu:** Thời gian đối chiếu và duyệt ≤3 phút/hóa đơn; recall phát hiện sai lệch ≥95% trên tập hóa đơn được gắn nhãn.
- **Quick Architecture:** Rule trước; chưa cần LLM nếu có dữ liệu bảng sạch.
- **Dữ liệu cần:** Hóa đơn, lệnh sửa chữa, danh mục mã dịch vụ, quy tắc làm tròn và nhãn sai lệch chuẩn.
- **Ranh giới:** Không tự thanh toán, sửa hóa đơn hoặc kết luận gian lận.
- **Đánh giá nhanh:** Có thể đạt hiệu quả bằng code thông thường; không chọn làm prototype LLM của lab.

## Cách xác minh các giả định

Thu thập mẫu được phép sử dụng, đo thời gian thao tác thực tế, phỏng vấn người tiếp nhận và người nhận vé; thống nhất nhãn chuẩn trước khi thử nghiệm. Chưa dùng các mục tiêu trên như kết quả đã đạt.
