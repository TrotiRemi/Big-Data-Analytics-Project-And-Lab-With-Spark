# BDA Final Project Brief

**Author:** Badr TAJINI - Big Data Analytics - ESIEE 2025-2026  
**Date:** Oct 24, 2025

## Theme
Bitcoin price movement prediction with PySpark on blockchain-derived data plus market traces.

## Scope

Build an **end-to-end PySpark pipeline**:

- Acquire recent Bitcoin data (raw blocks or faithful derived dump)
- Extract transactions to tables
- Engineer features for near-term price moves
- Train and evaluate a direction and/or magnitude predictor
- Provide reproducible evidence: `explain("formatted")`, Spark UI screenshots, configs, metrics logs

**Team size:** 1-2  
**Effort scales with team size**

## Datasets

- **Blockchain:** raw blocks or faithful derivatives with tx graph and timestamps
- **Market prices:** historical BTC candles (minute/hour)
- **Optional:** mempool stats, exchange metrics, on-chain indicators

## Deliverables

- ≤10-min video: idea → methodology → implementation → results
- Report: `BDA_Project_Report.md`
- Code+Config: PySpark entry points or notebook, `bda_project_config.yml`
- Evidence: plans and Spark UI screenshots; metrics CSV
- Reproducibility: exact commands and a one-shot runner

## Guardrails

- Use **PySpark** for ETL and analytics
- Streaming optional; batch on offline traces acceptable
- Use public, citeable data only

## Suggested Milestones

| Milestone | Description |
|-----------|-------------|
| **M1** | Dataset + ingestion plan |
| **M2** | ETL + baseline |
| **M3** | Experiments |
| **M4** | Package + video |

## Organization

- **Team:** Pair or solo
- **Submission:** Upload `bda_project_name1-name2.zip` containing code, outputs, proof, metrics, report, config to your Github private repo, then share in the Google Form
- **Due Date:** **07/12/2025 23:59 Paris time**

## References

- Syllabus & practical labs
- Final Project pageY
- Cryptocurrency predictor with blockchain + prices
