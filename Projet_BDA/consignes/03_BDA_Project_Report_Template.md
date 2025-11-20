# BDA Final Project — Report Template

**Author:** Badr TAJINI - Big Data Analytics - ESIEE 2025-2026  
**Date:** Oct 16, 2025

This document outlines the structure for your project report.

## 1. Problem & Objectives

- Target prediction (direction, magnitude, or both)
- Time horizon (e.g., 1-hour, 4-hour)
- Key hypotheses about on-chain data driving price moves

## 2. Data

- Sources (blockchain, Kaggle, other)
- Licenses and citations
- Fetch method (Bitcoin Core, Kaggle API, etc.)
- Coverage window (date range)
- Sample sizes (rows/GB)

## 3. Pipeline

### Data Ingestion
- Sources and acquisition process

### ETL Process
- Parsing raw blocks → transaction tables
- Schema definitions
- Sample data

### Feature Engineering
- Joins (blocks + prices)
- Feature descriptions
- Window functions

### Data Sizes
- Input, intermediate, and output table sizes

## 4. Experiments

- Train/test splits (temporal or random)
- Baselines (naive, statistical)
- Ablations (feature importance)
- Hyperparameter tuning
- **All metrics logged to `project_metrics_log.csv`**

## 5. Performance Evidence

- `explain("formatted")` excerpts (from key jobs)
- **Spark UI screenshots:**
  - Job stages
  - Shuffle operations
  - Data skew patterns
  - Execution times

## 6. Results & Discussion

- Metrics tables and figures
- Model performance vs. baselines
- Limitations and caveats
- Ethical considerations (market impact, data privacy)

## 7. Reproducibility

- **Exact commands to:**
  - Set up environment (`ENV.md`)
  - Fetch data
  - Run ETL
  - Train models
  - Generate evidence
- Configuration file: `bda_project_config.yml`
- One-shot runner: `run_all.sh` or `Makefile`
