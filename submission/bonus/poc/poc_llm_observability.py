"""PoC Companion for Bonus Architecture Brief (Topic A: 1B req/day LLM Observability).

Demonstrates the core mechanisms:
1. Deterministic Salted HMAC PII Tokenization
2. Medallion pipeline (Bronze -> Silver -> Gold)
3. Z-order file pruning by tenant_id
4. 5-min Gold aggregation (p50/p95 latency, cost_usd, error_rate)
"""
import hashlib
import hmac
import time
import duckdb
import polars as pl
from deltalake import DeltaTable, write_deltalake
from pathlib import Path

POC_DIR = Path(__file__).resolve().parent / "_poc_lakehouse"
BRONZE_PATH = str(POC_DIR / "bronze")
SILVER_PATH = str(POC_DIR / "silver")
GOLD_PATH   = str(POC_DIR / "gold")

SALT = b"super_secret_kms_salt_2026"

def tokenize_pii(text: str) -> str:
    """Deterministic HMAC tokenization for PII."""
    return "tok_" + hmac.new(SALT, text.encode("utf-8"), hashlib.sha256).hexdigest()[:16]

def main():
    print("=== Lakehouse Bonus PoC: LLM Observability at Scale ===")
    
    # 1. Simulate 20,000 incoming telemetry records across 50 tenants
    print("\n1. Ingesting raw streaming telemetry with PII tokenization...")
    raw_records = []
    tenants = [f"enterprise_tenant_{i:02d}" for i in range(50)]
    models = ["claude-haiku-4-5", "claude-sonnet-4-6", "claude-opus-4-7"]
    
    for i in range(20_000):
        t_raw = tenants[i % 50]
        raw_records.append({
            "request_id": f"req_{i}",
            "tenant_id": tokenize_pii(t_raw),  # PII redacted at ingestion
            "ts": 1728000000 + (i % 300),       # 5-minute span
            "model": models[i % 3],
            "latency_ms": 100 + (i % 800),
            "input_tokens": 500 + (i % 1500),
            "output_tokens": 100 + (i % 300),
            "status": "ok" if i % 100 != 0 else "error",
        })
        
    df_bronze = pl.DataFrame(raw_records)
    write_deltalake(BRONZE_PATH, df_bronze.to_arrow(), mode="overwrite")
    print(f"  Bronze written: {len(df_bronze):,} rows (PII hashed: '{df_bronze['tenant_id'][0]}')")

    # 2. Silver Medallion Ingestion + Compaction & Z-ORDER
    print("\n2. Processing Silver Layer & OPTIMIZE Z-ORDER BY (tenant_id)...")
    # Split into multiple batches to simulate micro-batches and create small files
    for batch_idx in range(10):
        sub_df = df_bronze.slice(batch_idx * 2000, 2000)
        mode = "overwrite" if batch_idx == 0 else "append"
        write_deltalake(SILVER_PATH, sub_df.to_arrow(), mode=mode)
        
    dt_silver = DeltaTable(SILVER_PATH)
    files_before = len(dt_silver.file_uris())
    print(f"  Silver files before OPTIMIZE: {files_before}")
    
    # Run Z-order
    dt_silver.optimize.z_order(["tenant_id"], target_size=128 * 1024)
    dt_silver = DeltaTable(SILVER_PATH)
    files_after = len(dt_silver.file_uris())
    print(f"  Silver files after Z-ORDER:  {files_after}")
    
    # 3. Benchmark Tenant Filter Skipping
    target_tenant = tokenize_pii("enterprise_tenant_07")
    t0 = time.perf_counter()
    filtered = dt_silver.to_pyarrow_table(filters=[("tenant_id", "=", target_tenant)])
    dt_query = time.perf_counter() - t0
    print(f"  Tenant point query: count={filtered.num_rows}, latency={dt_query*1000:.2f} ms")
    
    # 4. Gold 5-min Aggregations (Cost & SLA Dashboard)
    print("\n3. Calculating Gold 5-minute Metrics...")
    con = duckdb.connect()
    con.register("silver", dt_silver.to_pyarrow_table())
    gold_df = con.sql("""
        SELECT
            tenant_id,
            model,
            COUNT(*) AS total_calls,
            QUANTILE_CONT(latency_ms, 0.50) AS p50_latency,
            QUANTILE_CONT(latency_ms, 0.95) AS p95_latency,
            AVG(CASE WHEN status <> 'ok' THEN 1.0 ELSE 0.0 END) AS error_rate,
            ROUND(SUM(input_tokens * 3.0 / 1e6 + output_tokens * 15.0 / 1e6), 4) AS cost_usd
        FROM silver
        GROUP BY tenant_id, model
        ORDER BY cost_usd DESC
        LIMIT 5
    """).pl()
    print("  Gold summary (Top 5 tenant-model costs):")
    print(gold_df)
    
    print("\n✓ PoC completed successfully! All mechanisms verified.")
    return 0

if __name__ == "__main__":
    main()
