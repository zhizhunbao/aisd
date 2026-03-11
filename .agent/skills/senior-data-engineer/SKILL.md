---
name: senior-data-engineer
description: Data engineering skill for building scalable data pipelines, ETL/ELT systems, and data infrastructure. Expertise in Python, SQL, Spark, Airflow, dbt, Kafka, and modern data stack. Includes data modeling, pipeline orchestration, data quality, and DataOps. Use when designing data architectures, building data pipelines, optimizing data workflows, implementing data governance, or troubleshooting data issues.
---

# Senior Data Engineer

Production-grade data engineering skill for building scalable, reliable data systems.

## Table of Contents

1. [Trigger Phrases](#trigger-phrases)
2. [Quick Start](#quick-start)
3. [Workflows](#workflows)
   - [Building a Batch ETL Pipeline](#workflow-1-building-a-batch-etl-pipeline)
   - [Implementing Real-Time Streaming](#workflow-2-implementing-real-time-streaming)
   - [Data Quality Framework Setup](#workflow-3-data-quality-framework-setup)
4. [Architecture Decision Framework](#architecture-decision-framework)
5. [Tech Stack](#tech-stack)
6. [Reference Documentation](#reference-documentation)
7. [Troubleshooting](#troubleshooting)

---

## Trigger Phrases

Activate this skill when you see:

**Pipeline Design:**
- "Design a data pipeline for..."
- "Build an ETL/ELT process..."
- "How should I ingest data from..."
- "Set up data extraction from..."

**Architecture:**
- "Should I use batch or streaming?"
- "Lambda vs Kappa architecture"
- "How to handle late-arriving data"
- "Design a data lakehouse"

**Data Modeling:**
- "Create a dimensional model..."
- "Star schema vs snowflake"
- "Implement slowly changing dimensions"
- "Design a data vault"

**Data Quality:**
- "Add data validation to..."
- "Set up data quality checks"
- "Monitor data freshness"
- "Implement data contracts"

**Performance:**
- "Optimize this Spark job"
- "Query is running slow"
- "Reduce pipeline execution time"
- "Tune Airflow DAG"

---

## Quick Start

### Core Tools

```bash
# Generate pipeline orchestration config
python scripts/pipeline_orchestrator.py generate \
  --type airflow \
  --source postgres \
  --destination snowflake \
  --schedule "0 5 * * *"

# Validate data quality
python scripts/data_quality_validator.py validate \
  --input data/sales.parquet \
  --schema schemas/sales.json \
  --checks freshness,completeness,uniqueness

# Optimize ETL performance
python scripts/etl_performance_optimizer.py analyze \
  --query queries/daily_aggregation.sql \
  --engine spark \
  --recommend
```

---

<!-- Detailed content moved to references/workflows_reference.md -->

> 📖 See [references/workflows_reference.md](references/workflows_reference.md) for detailed content on the following topics:
> - ## Workflows

<!-- Detailed content moved to references/architecture_reference.md -->

> 📖 See [references/architecture_reference.md](references/architecture_reference.md) for detailed content on the following topics:
> - ## Architecture Decision
> - ## Tech Stack
> - ## Reference Documentation
> - ## Troubleshooting
