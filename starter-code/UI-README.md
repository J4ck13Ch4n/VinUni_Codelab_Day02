# Giao diện demo Vinhomes

Chạy tại thư mục gốc:

```powershell
python starter-code/app.py
```

Mở http://127.0.0.1:8000 trong trình duyệt.

1. Chọn **Demo từ khóa** để chạy ngay không cần cài thư viện/API key.
2. Chọn tòa, nhập mất nước/hỏng đèn/ồn ào và bấm **Gửi & đề xuất nơi xử lý**.
3. Xem đề xuất phía ban quản lý, sửa bộ phận nếu cần, nhập tên và duyệt.

Muốn dùng Gemini thật, cài google-genai và khai báo GEMINI_API_KEY trong terminal trước khi khởi động server. Chọn Gemini AI trên UI. Lỗi 429 hiển thị rõ và chuyển xử lý thủ công, không âm thầm dùng kết quả từ khóa thay AI.

Đây là demo local cho một người trình bày hai vai trò, không có xác thực nhân viên. Kết quả duyệt chỉ lưu trong bộ nhớ, tối đa 200 vé; mất khi tắt server. Không gửi thông báo hoặc ticket thật. Ca cần escalation chỉ được duyệt chuyển BQL xem xét thủ công. Bộ từ khóa còn hạn chế về ngữ cảnh và phủ định.
