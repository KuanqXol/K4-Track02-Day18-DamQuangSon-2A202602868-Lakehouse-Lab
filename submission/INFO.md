# Thông Tin Bài Nộp — K4-Track02-Day18 Lakehouse Lab

- **Họ và tên:** Đàm Quang Sơn
- **Mã số sinh viên (MSSV):** 2A202602868
- **Tên Repository cá nhân:** `K4-Track02-Day18-DamQuangSon-2A202602868-Lakehouse-Lab`
- **Mã bài lab:** `K4-Track02-Day18`
- **Chủ đề:** Data Lakehouse Architecture (Delta Lake, Apache Iceberg, Medallion, Maintenance, Vectors & Multimodal, Agents & Provenance)
- **Đường chạy thực hiện:** Lightweight Path (Python 100% — `deltalake` 1.x, `pyiceberg`, DuckDB, Polars; không dùng Docker/JVM)
- **Phiên bản Python:** Python 3.11.9
- **Hệ điều hành:** Windows 11 (PowerShell 7 / Windows Terminal, `$env:PYTHONUTF8 = '1'`)

---

## Tóm tắt kết quả kiểm tra cục bộ (Local Reproducibility)

1. **Smoke test (`scripts/verify_lite.py`):** **9/9 checks PASS** (Delta write/read, time travel, maintenance, CDF, Iceberg catalog & planning, Iceberg maintenance, DuckDB vector search, DuckDB ↔ Delta Arrow zero-copy).
2. **Pytest test suite (`tests/test_lab18.py`):** **24/24 tests PASS** (100% pass trong 2.62s).
3. **Headless script runner (`scripts/run_all.py`):** **8/8 notebooks PASS** (toàn bộ assertion nội tại pass).
4. **Jupyter Notebook execution (`submission/notebooks/`):** **8/8 notebooks đã chạy hoàn chỉnh, lưu đầy đủ output kết quả.**

---

## Danh mục tài liệu nộp

- `submission/INFO.md`: File này.
- `submission/REFLECTION.md`: Trả lời bài học rút ra về Lakehouse Anti-Patterns (≤ 200 từ) và khai báo phạm vi dùng AI.
- `submission/AI_USAGE.md`: Chi tiết phạm vi hỗ trợ của công cụ AI theo quy định RULES.md.
- `submission/notebooks/`: 8 file `.ipynb` thực thi đầy đủ output:
  - `01_delta_basics.ipynb`
  - `02_optimize_zorder.ipynb`
  - `03_time_travel.ipynb`
  - `04_medallion.ipynb`
  - `05_iceberg_catalog.ipynb`
  - `06_maintenance.ipynb`
  - `07_vectors_multimodal.ipynb`
  - `08_agents_provenance.ipynb`
- `submission/screenshots/`: Ảnh chụp màn hình kết quả đầu ra then chốt của cả 8 notebook.
- `submission/bonus/`:
  - `ARCHITECTURE.md`: Tài liệu kiến trúc hoàn chỉnh cho Topic A: LLM Observability ở quy mô 1B requests/ngày (đầy đủ 6 phần, tính toán chi phí chi tiết, sơ đồ Mermaid, 5 quyết định và failure modes).
  - `poc/`: Code PoC minh họa cơ chế partitioning & tokenization / cost aggregation.
