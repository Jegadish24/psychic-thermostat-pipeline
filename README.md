# \# 🌡️ Psychic Thermostat: Predictive Thermal Management Pipeline

# 

# An end-to-end cloud data pipeline engineered to ingest, clean, aggregate, and visualize high-frequency telemetry from immersion-cooled data centers. Built using Azure Databricks, Delta Lake (Medallion Architecture), and PySpark.

# 

# \---

# 

# \## 📌 Architecture Overview

# 

# The pipeline follows a multi-hop \*\*Medallion Lakehouse Architecture\*\*:

# 

# ```text

# \[IoT Telemetry Simulator] 

# &#x20;      │ (JSON / Streaming Batch)

# &#x20;      ▼

# ┌────────────────────────┐

# │      Bronze Layer      │  raw\_telemetry (Delta) - Schema-on-read ingestion

# └──────────┬─────────────┘

# &#x20;          │

# &#x20;          ▼

# ┌────────────────────────┐

# │      Silver Layer      │  silver\_events (Delta) - Deduplication, type casting,

# └──────────┬─────────────┘                         validation \& anomaly flags

# &#x20;          │

# &#x20;          ▼

# ┌────────────────────────┐

# │       Gold Layer       │  gold\_metrics (Delta) - Tumbling time-window aggregates

# └──────────┬─────────────┘                         and cooling alert thresholds

# &#x20;          │

# &#x20;          ▼

# ┌────────────────────────┐

# │  Lakeview Operations   │  Real-time KPI monitor, utilization tracking \& filters

# └────────────────────────┘





# \---



# ⚙️ Automated Orchestration (Databricks Workflows):

# !\[Workflow DAG](assets/workflow\_dag.png)

# The Medallion pipeline is automated using a multi-task Databricks Workflow Job (DAG). Tasks enforce sequential execution and fault containment:

# 

* # bronze\_ingestion: Reads raw telemetry data into Delta format preserving raw schema and ingestion timestamps.

# 

* # silver\_transformation: Enforces strict schema constraints, parses timestamps, handles nulls, and standardizes compute telemetry.

# 

* # gold\_aggregations: Computes rolling window statistics (power draw, fluid temperatures, compute spikes) to trigger cooling alerts.

# 

# \---

# 

# 📊 Operations Monitor (Lakeview Dashboard):

# !\[Operations Dashboard](assets/dashboard\_preview.png)

# The aggregated Gold and Silver tables feed a production Operations Monitor:

# 

# Thermal Alert Counter: Instant KPI reflecting current threshold violations across server nodes.

# 

# Synchronized Telemetry: Correlates average power draw with liquid coolant temperatures.

# 

# Compute Utilization Split: Dual-axis tracking of CPU vs. GPU loads to anticipate thermal latency.

# 

# Global Filters: Dynamic time-range picker linked across Silver and Gold Delta tables.









# \---

# psychic-thermostat-pipeline/

# ├── assets/

# │   ├── dashboard\_preview.png

# │   └── workflow\_dag.png

# ├── notebooks/

# │   ├── 01\_bronze\_ingestion.py

# │   ├── 02\_clean\_silver.py

# │   └── 03\_gold\_aggregates.py

# ├── data\_generator/

# │   └── simulate.py

# ├── .gitignore

# └── README.md





# \---

# 

# 🚀 Getting Started

# Simulate Telemetry: Run python data\_generator/simulate.py to produce raw IoT telemetry.

# 

# Databricks Deployment: Import notebooks from /notebooks into your workspace.

# 

# Run Pipeline: Trigger the multi-task job via Databricks Workflows or run notebooks sequentially.

# 

## View Metrics: Open the Lakeview dashboard and link to the provisioned SQL Warehouse.

