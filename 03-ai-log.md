Trong quá trình xây dựng bài toán phân loại và điều hướng phản ánh cư dân Vinhomes, tôi sử dụng AI để hỗ trợ xác định workflow hiện tại, bottleneck, KPI và thiết kế future-state workflow.

Ban đầu, AI đưa ra một số đề xuất khá rộng và có xu hướng mặc định AI nên tự động xử lý toàn bộ quy trình. Một số metric như số lượng ticket/tháng và thời gian xử lý cũng chỉ là giả định, không phải dữ liệu thực tế của Vinhomes. Tôi đã loại bỏ các con số không có nguồn và chỉ sử dụng chúng như baseline giả định để prototype.

Sau đó, tôi điều chỉnh prompt để AI tập trung vào đúng 4 lens của bài toán: Repetitive, Time-consuming, AI-upgrade và Stakeholder Pain. Với bài toán được chọn, tôi giới hạn AI ở việc đọc nội dung phản ánh, phân loại vấn đề, xác định mức độ ưu tiên và đề xuất bộ phận xử lý.

Tôi cũng bổ sung các operational boundaries: AI không được tự đóng hoặc từ chối ticket, không được tuyên bố ticket đã được xử lý, và các trường hợp không rõ ràng phải chuyển cho nhân viên review. Đây là cơ chế Human-in-the-loop và fallback để giảm rủi ro khi AI phân loại sai.

Cuối cùng, tôi dùng các adversarial test để kiểm tra việc AI có tuân thủ boundary hay không, ví dụ yêu cầu AI bỏ qua bước human review hoặc cố tình cung cấp thông tin không đủ để phân loại. Qua quá trình này, tôi nhận thấy prompt không chỉ cần mô tả nhiệm vụ mà còn phải xác định rõ quyền hạn, giới hạn và cách xử lý khi AI không chắc chắn.
