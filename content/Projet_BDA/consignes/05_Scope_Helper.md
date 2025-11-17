# Scope Helper – Bitcoin Predictor Project

**Author:** Badr TAJINI - Big Data Analytics - ESIEE 2025-2026  
**Date:** Oct 16, 2025

## Why the Scope is Bigger Than It Looks

This project is **not** "just running a regression on prices." We combine two raw data streams:

1. **Blockchain blocks** (`blk*.dat` from Bitcoin Core in prune mode) → decode into full transaction tables
2. **Market price history** (Kaggle BTC candles) → labels/features for supervised learning

### Key Requirements

- **Two complementary datasets**
  - Raw `blk*.dat` delivers the full transaction graph
  - Kaggle candles supply market labels/features
  - **You need both** to ground the predictor in on-chain behavior

- **Non-trivial ETL**
  - Raw blocks must be decoded into Spark tables (transactions, addresses, flows)
  - This is **much tougher than loading CSVs**

- **Feature + Model Work**
  - Near-term movement features plus a direction/magnitude model in Spark
  - Windowed joins, aggregations, proper evaluation

- **Reproducibility**
  - `explain("formatted")`, Spark UI evidence, configs, metrics logs
  - One-shot runner to automate the entire pipeline

---

## Extra Uses Beyond "Predict Up/Down"

The same feature stack supports:

| Use Case | Description |
|----------|-------------|
| **Risk Alerts** | Flag drawdown/pump patterns for treasury or trading desks |
| **Liquidity Planning** | Warn market makers about likely volatility → adjust spreads/capital |
| **Automated Hedging** | Feed probabilities into rules that size hedges or unwind positions |
| **Anomaly Detection** | Spot unusual whale/exchange flows before prices react |
| **Scenario Backtesting** | Target realized volatility, spreads, or other derivatives |

---

## Scope Explained with Real-World Analogies

| Scope Item | Real-World Analogy |
|------------|-------------------|
| **Acquire recent Bitcoin data (raw blocks + prices)** | Stand up a data pipeline that pulls shipping manifests (blocks) and market quotes daily. Run Bitcoin Core in prune mode to keep disk manageable while staying current. |
| **Extract transactions to tables** | Build ingestion jobs that parse binary blocks into Spark tables (transactions, addresses, flows). Like turning raw JSON logs into bronze/silver tables in a lakehouse. |
| **Engineer features for near-term price moves** | Enrich the data: rolling volumes, UTXO age, whale alerts, momentum. These become the feature sets your ML service consumes. |
| **Train and evaluate direction/magnitude predictor** | Operate a Spark ML training pipeline. Version the model, store metrics, ensure it beats baselines, log Spark plans for reproducibility. |
| **Provide reproducible evidence** | Ship proper documentation and automation: notebook/job configs, `explain("formatted")` outputs, Spark UI screenshots, metrics logs, one-shot runners. Another engineer can replay everything end-to-end. |

---

## Key Takeaway

**This is an end-to-end big data stack** with:
- Collection
- ETL
- Feature engineering
- Modeling
- Reproducibility

It is **not** a small Kaggle script. Plan accordingly.
