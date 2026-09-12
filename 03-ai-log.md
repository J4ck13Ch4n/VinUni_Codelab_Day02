# 03 — Nhật ký sử dụng AI và phản ánh

> Bản dự thảo dựa trên cuộc trao đổi thực tế với trợ lý AI. Người học cần đọc, chỉnh lại cách diễn đạt và bổ sung trải nghiệm riêng trước khi nộp. Không có nội dung giả định đã phỏng vấn doanh nghiệp hoặc đã chạy Gemini thành công.

## Mục tiêu và AI đã giúp gì

Tôi chọn đề tài phân loại và điều hướng phản ánh cư dân Vinhomes từ hình ảnh bài toán được cung cấp. Tôi nhờ AI đọc workspace, giải thích PRD/TRD, xác định phần cần triển khai và tạo demo đơn giản. AI giúp chuyển một mô tả ngắn thành đầu vào, danh mục nhãn, quy tắc chuyển người xử lý và các ca kiểm thử.

AI cũng giúp phân biệt yêu cầu sản phẩm và phạm vi lab. Sản phẩm tương lai cần tích hợp nguồn vé, dashboard phê duyệt và audit; bài lab có thể kiểm chứng một phần bằng script Python. Việc tách phạm vi này giúp tránh dành thời gian xây giao diện trước khi kiểm tra được hành vi mô hình.

## Nhật ký các điểm trao đổi chính

| Tình huống thực tế | AI hỗ trợ | Vấn đề / cách điều chỉnh |
|---|---|---|
| Tôi gửi ảnh đề tài Vinhomes | AI chuyển mã mẫu xe điện sang phân loại phản ánh | Bản đầu chưa có nhãn phí/tranh chấp như PRD/TRD |
| Tôi đưa PRD và TRD | AI chỉ ra lệch giữa auto-route và duyệt mọi vé, thiếu metadata tòa và hợp đồng JSON chưa rõ | Chốt kết quả chỉ là đề xuất; code quyết định nơi nhận từ danh mục |
| Tôi yêu cầu demo đơn giản | AI tạo demo từ khóa không cần API | Demo này không đáp ứng phần gọi Gemini thật; sau khi tôi gửi ảnh hướng dẫn lab, AI xác nhận giới hạn đó |
| Tôi gửi log stress-test có AFC warning và model_request_failed | AI phân biệt cảnh báo AFC với lỗi yêu cầu API | Không kết luận nguyên nhân là key/quota khi chưa có mã lỗi; bổ sung mã HTTP khi có |
| Tôi gửi yêu cầu bộ hồ sơ nộp bài | AI soạn scan, deep-dive, sơ đồ và nhật ký dự thảo | Số liệu phải ghi là giả định; không được kể rằng đã đạt 90% hoặc pilot thành công |

## AI trả lời chưa đúng hoặc chưa đủ ở đâu?

Sai lệch quan trọng nhất là scope: demo từ khóa chạy được nhưng không phải prototype Gemini mà bài lab yêu cầu. Một chương trình chạy được không đồng nghĩa đã đáp ứng tiêu chí bài tập.

Bản code đầu chỉ bảo vệ khẩn cấp dựa vào cờ mô hình, chưa có kiểm soát riêng cho phí/tranh chấp. Vì vậy chỉ viết “không được” trong system prompt là chưa đủ. Kết quả còn có thể đúng định dạng nhưng sai nghiệp vụ.

Trong log tôi cung cấp, tất cả ca trả về `model_request_failed`. Không thể dùng log đó để khẳng định AI đã vượt qua hoặc vi phạm ranh giới: chưa nhận được kết quả phân loại hợp lệ. Cảnh báo AFC xuất hiện cùng lúc cũng chưa chứng minh nó là nguyên nhân thất bại.

Một giới hạn được phát hiện khi kiểm tra code là chuẩn hóa mất dấu khiến “chạy” và “cháy” trùng nhau. Prototype giữ chính sách chuyển người kiểm tra bảo thủ và ghi rõ nguy cơ báo nhầm; đây chưa phải vấn đề đã giải quyết triệt để.

## Prompt và ranh giới đã thay đổi như thế nào?

Prompt được chuyển từ điều phối xe điện sang phân loại phản ánh Vinhomes, nêu danh mục nhãn cố định, ưu tiên nội dung tài chính/tranh chấp và cấm tự gửi/đóng vé. Nội dung cư dân được xác định là dữ liệu, không phải chỉ thị có thể thay thế system prompt.

Phần kiểm soát được đưa vào Python: kiểm tra schema và confidence; dò dấu hiệu nhạy cảm trong nội dung gốc; xóa nơi định tuyến thông thường khi cần escalation; dùng mẫu ghi chú trung tính; giữ trạng thái nháp và người duyệt. Mã tòa được truyền riêng, không cho AI tự chọn.

Code vẫn có giới hạn: từ khóa chưa bao phủ mọi cách diễn đạt, confidence chưa hiệu chuẩn, chưa có cơ chế duyệt thật và chuyển hàng đợi tức thời. Không coi các sửa đổi này là bảo đảm an toàn tuyệt đối.

## Bằng chứng và bài học

- Có 16 kiểm tra offline cho lớp code; đây là kiểm tra với dữ liệu mô hình giả lập.
- Có 5 ca đối kháng để gọi Gemini; chưa xác minh thành công trên API thật trong lần hoàn thiện hồ sơ này.
- Chưa có dữ liệu vận hành, phỏng vấn stakeholder, số đo độ chính xác, latency hay mức tiết kiệm thực tế.

Bài học của quá trình này là phải kiểm tra ba lớp riêng: yêu cầu có đúng không, chương trình có chạy đúng không và mô hình có cho kết quả hữu ích trên dữ liệu phù hợp không. Tôi cần đọc lại code, chạy bằng môi trường/API của mình, lưu kết quả thật và sửa báo cáo theo bằng chứng trước khi nộp. Nhật ký này không thay cho phần phản ánh cá nhân của người học.
