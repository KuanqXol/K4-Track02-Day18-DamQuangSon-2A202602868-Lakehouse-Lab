# Khai Báo Sử Dụng Công Cụ AI (AI Usage Declaration)

Theo quy định tại [RULES.md](../docs/RULES.md), học viên khai báo đầy đủ các công cụ AI và phạm vi sử dụng trong bài lab này:

## 1. Công cụ sử dụng
- **Google Antigravity IDE (Gemini / Claude)**: Trợ lý AI lập trình cặp (Pair-programming assistant).

## 2. Phạm vi hỗ trợ
- **Đọc hiểu tài liệu & Lập kế hoạch:** Hỗ trợ phân tích tổng thể các file hướng dẫn (`README.md`, `SUBMISSION.md`, `RUBRIC.md`, `CHECKPOINTS.md`), từ đó trích xuất ra checklist chi tiết từng bước.
- **Tự động hóa pipeline thực thi:** Hỗ trợ viết script runner tự động hóa quá trình chuyển đổi Jupytext (`.py` → `.ipynb`) và thực thi tuần tự 8 notebook bằng `nbconvert` nhằm đảm bảo toàn bộ output tế bào được ghi nhận chính xác vào `submission/notebooks/`.
- **Hỗ trợ định dạng tài liệu:** Hỗ trợ soạn thảo bảng biểu và cấu trúc tài liệu kiến trúc bonus `ARCHITECTURE.md` theo đúng tiêu chuẩn 6 tiêu chí của Rubric.

## 3. Cam kết tính trung thực học thuật
- **Thực thi thực tế:** Toàn bộ 8 notebook, 9 smoke tests và 24 unit tests đều được thực thi trực tiếp trên môi trường máy local (Windows 11, Python 3.11).
- **Không làm giả dữ liệu:** Không có bất kỳ kết quả giả tạo (fake output), không sửa đổi hay hạ thấp ngưỡng kiểm tra (assertion) trong mã nguồn gốc của ban tổ chức.
- **Làm chủ kiến thức:** Học viên hoàn toàn hiểu rõ bản chất kỹ thuật, cơ chế hoạt động của Delta Lake, Apache Iceberg, cơ chế Z-order file pruning, và các bài toán lifecycle/provenance được triển khai trong bài làm.
