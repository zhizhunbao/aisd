# Data Engineer — Architecture & Reference

## Architecture Decision Framework

Use this framework to choose the right approach for your data pipeline.

### Batch vs Streaming

| Criteria | Batch | Streaming |
|----------|-------|-----------|
| **Latency requirement** | Hours to days | Seconds to minutes |
| **Data volume** | Large historical datasets | Continuous event streams |
| **Processing complexity** | Complex transformations, ML | Simple aggregations, filtering |
| **Cost sensitivity** | More cost-effective | Higher infrastructure cost |
| **Error handling** | Easier to reprocess | Requires careful design |

**Decision Tree:**
```
Is real-time insight required?
├── Yes → Use streaming
│   └── Is exactly-once semantics needed?
│       ├── Yes → Kafka + Flink/Spark Structured Streaming
│       └── No → Kafka + consumer groups
└── No → Use batch
    └── Is data volume > 1TB daily?
        ├── Yes → Spark/Databricks
        └── No → dbt + warehouse compute
```

### Lambda vs Kappa Architecture

| Aspect | Lambda | Kappa |
|--------|--------|-------|
| **Complexity** | Two codebases (batch + stream) | Single codebase |
| **Maintenance** | Higher (sync batch/stream logic) | Lower |
| **Reprocessing** | Native batch layer | Replay from source |
| **Use case** | ML training + real-time serving | Pure event-driven |

**When to choose Lambda:**
- Need to train ML models on historical data
- Complex batch transformations not feasible in streaming
- Existing batch infrastructure

**When to choose Kappa:**
- Event-sourced architecture
- All processing can be expressed as stream operations
- Starting fresh without legacy systems

### Data Warehouse vs Data Lakehouse

| Feature | Warehouse (Snowflake/BigQuery) | Lakehouse (Delta/Iceberg) |
|---------|-------------------------------|---------------------------|
| **Best for** | BI, SQL analytics | ML, unstructured data |
| **Storage cost** | Higher (proprietary format) | Lower (open formats) |
| **Flexibility** | Schema-on-write | Schema-on-read |
| **Performance** | Excellent for SQL | Good, improving |
| **Ecosystem** | Mature BI tools | Growing ML tooling |

---


## Tech Stack

| Category | Technologies |
|----------|--------------|
| **Languages** | Python, SQL, Scala |
| **Orchestration** | Airflow, Prefect, Dagster |
| **Transformation** | dbt, Spark, Flink |
| **Streaming** | Kafka, Kinesis, Pub/Sub |
| **Storage** | S3, GCS, Delta Lake, Iceberg |
| **Warehouses** | Snowflake, BigQuery, Redshift, Databricks |
| **Quality** | Great Expectations, dbt tests, Monte Carlo |
| **Monitoring** | Prometheus, Grafana, Datadog |

---


## Reference Documentation

### 1. Data Pipeline Architecture
See `references/data_pipeline_architecture.md` for:
- Lambda vs Kappa architecture patterns
- Batch processing with Spark and Airflow
- Stream processing with Kafka and Flink
- Exactly-once semantics implementation
- Error handling and dead letter queues

### 2. Data Modeling Patterns
See `references/data_modeling_patterns.md` for:
- Dimensional modeling (Star/Snowflake)
- Slowly Changing Dimensions (SCD Types 1-6)
- Data Vault modeling
- dbt best practices
- Partitioning and clustering

### 3. DataOps Best Practices
See `references/dataops_best_practices.md` for:
- Data testing frameworks
- Data contracts and schema validation
- CI/CD for data pipelines
- Observability and lineage
- Incident response

---


## Troubleshooting

### Pipeline Failures

**Symptom:** Airflow DAG fails with timeout
```
Task exceeded max execution time
```

**Solution:**
1. Check resource allocation
2. Profile slow operations
3. Add incremental processing
```python
# Increase timeout
default_args = {
    'execution_timeout': timedelta(hours=2),
}

# Or use incremental loads
WHERE updated_at > '{{ prev_ds }}'
```

---

**Symptom:** Spark job OOM
```
java.lang.OutOfMemoryError: Java heap space
```

**Solution:**
1. Increase executor memory
2. Reduce partition size
3. Use disk spill
```python
spark.conf.set("spark.executor.memory", "8g")
spark.conf.set("spark.sql.shuffle.partitions", "200")
spark.conf.set("spark.memory.fraction", "0.8")
```

---

**Symptom:** Kafka consumer lag increasing
```
Consumer lag: 1000000 messages
```

**Solution:**
1. Increase consumer parallelism
2. Optimize processing logic
3. Scale consumer group
```bash
# Add more partitions
kafka-topics.sh --alter \
  --bootstrap-server localhost:9092 \
  --topic user-events \
  --partitions 24
```

---

### Data Quality Issues

**Symptom:** Duplicate records appearing
```
Expected unique, found 150 duplicates
```

**Solution:**
1. Add deduplication logic
2. Use merge/upsert operations
```sql
-- dbt incremental with dedup
{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

SELECT * FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY updated_at DESC
        ) as rn
    FROM {{ source('raw', 'orders') }}
) WHERE rn = 1
```

---

**Symptom:** Stale data in tables
```
Last update: 3 days ago
```

**Solution:**
1. Check upstream pipeline status
2. Verify source availability
3. Add freshness monitoring
```yaml
# dbt freshness check
sources:
  - name: raw
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _loaded_at
```

---

**Symptom:** Schema drift detected
```
Column 'new_field' not in expected schema
```

**Solution:**
1. Update data contract
2. Modify transformations
3. Communicate with producers
```python
# Handle schema evolution
df = spark.read.format("delta") \
    .option("mergeSchema", "true") \
    .load("/data/orders")
```

---

### Performance Issues

**Symptom:** Query takes hours
```
Query runtime: 4 hours (expected: 30 minutes)
```

**Solution:**
1. Check query plan
2. Add proper partitioning
3. Optimize joins
```sql
-- Before: Full table scan
SELECT * FROM orders WHERE order_date = '2024-01-15';

-- After: Partition pruning
-- Table partitioned by order_date
SELECT * FROM orders WHERE order_date = '2024-01-15';

-- Add clustering for frequent filters
ALTER TABLE orders CLUSTER BY (customer_id);
```

---

**Symptom:** dbt model takes too long
```
Model fct_orders completed in 45 minutes
```

**Solution:**
1. Use incremental materialization
2. Reduce upstream dependencies
3. Pre-aggregate where possible
```sql
-- Convert to incremental
{{
    config(
        materialized='incremental',
        unique_key='order_id',
        on_schema_change='sync_all_columns'
    )
}}

SELECT * FROM {{ ref('stg_orders') }}
{% if is_incremental() %}
WHERE _loaded_at > (SELECT MAX(_loaded_at) FROM {{ this }})
{% endif %}
```

