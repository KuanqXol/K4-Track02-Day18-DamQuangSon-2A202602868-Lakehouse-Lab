# Reflection — Top Lakehouse Anti-Pattern

Trong các hệ thống xử lý streaming logs và LLM observability mà tôi quan tâm, anti-pattern dễ mắc phải và gây tổn thất lớn nhất là **Small-File Problem do Micro-batching**, đi kèm với **thiếu hụt quy trình Maintenance định kỳ**.

Khi hàng trăm worker ghi telemetry liên tục mỗi vài giây, hàng triệu tệp Parquet kích thước chỉ vài chục KB được sinh ra. Bẫy sản xuất này trừng phạt hệ thống hai lần: vừa làm bùng nổ chi phí I/O khi đọc (mỗi tệp chịu overhead mở/đóng và đọc Parquet footer riêng), vừa làm phình to cây metadata (như đo đạc ở NB5, metadata có thể chiếm tỷ trọng áp đảo so với data thực tế, gây nghẽn driver khi scan planning).

Để phòng tránh, kiến trúc cần áp dụng phân tầng: cho phép Bronze đệm micro-batch thô, sau đó định kỳ kích hoạt background compaction gộp các tệp về kích thước tối ưu (128–256 MB) kết hợp Z-ORDER theo các trường hay truy vấn lọc (`user_id`, `model`). Song song đó, phải thiết lập tự động snapshot expiry, VACUUM và dọn dẹp orphan files theo chính sách retention rõ ràng.

*Khai báo AI: Sử dụng AI hỗ trợ phân tích checklist và tự động hóa thực thi; chi tiết tại [AI_USAGE.md](AI_USAGE.md).*
