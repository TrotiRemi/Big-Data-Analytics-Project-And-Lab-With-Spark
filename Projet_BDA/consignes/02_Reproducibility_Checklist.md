# Reproducibility Checklist

**Author:** Badr TAJINI - Big Data Analytics - ESIEE 2025-2026  
**Date:** Oct 16, 2025

## Requirements Checklist

### Documentation
- [ ] `ENV.md` with OS, Python, Java, Spark, key confs

### Configuration & Setup
- [ ] `bda_project_config.yml` committed

### Data Acquisition
- [ ] Data-fetch README with exact commands/links
- [ ] Raw blocks archived (`data/btc_blocks_pruned_1GiB.tar.gz`)
- [ ] Live `data/blocks/blocks/` documented

### ETL & Processing
- [ ] ETL outputs: transactions table (tx_id, from, to, amount, ts, …)

### Evidence & Validation
- [ ] Evidence: `explain("formatted")` text files
- [ ] Evidence: Spark UI screenshots

### Metrics & Logging
- [ ] `project_metrics_log.csv` populated (run_id, stage, metric, value, ts)

### Automation & Reproducibility
- [ ] One-shot runner (`run_all.sh` or `make all`)

### Deliverables
- [ ] Video ≤10 min
- [ ] Report with figures

### Legal & Attribution
- [ ] Licenses/citations for all data/code
