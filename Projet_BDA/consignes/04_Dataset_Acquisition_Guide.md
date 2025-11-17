# Big Data Analytics — Dataset Acquisition Guide

**Author:** Badr TAJINI - Big Data Analytics - ESIEE 2025-2026  
**Date:** Oct 16, 2025

## Purpose

This guide explains how to:
- Acquire ~1 GiB of raw Bitcoin block files (`blk*.dat`) using Bitcoin Core in prune mode
- Download Bitcoin price history for labels and features using the Kaggle API

---

## Part A: Raw Bitcoin Blocks from Bitcoin Core (~1 GiB)

### A.1 Install Bitcoin Core

Download from the official project site and verify signatures.

**For Linux/WSL (without sudo):**

```bash
BITCOIN_VERSION=27.0
BITCOIN_TARBALL="bitcoin-${BITCOIN_VERSION}-x86_64-linux-gnu.tar.gz"
mkdir -p ~/.local/opt
cd ~/.local/opt
wget "https://bitcoincore.org/bin/bitcoin-core-${BITCOIN_VERSION}/${BITCOIN_TARBALL}"
tar -xzf "${BITCOIN_TARBALL}"
ln -sfn "bitcoin-${BITCOIN_VERSION}" bitcoin
echo 'export PATH="$HOME/.local/opt/bitcoin/bin:$PATH"' >> ~/.profile
source ~/.profile
bitcoind --version
```

**Why Bitcoin Core?** The project requires raw binary blocks (`blk*.dat`), not preprocessed tables.

**Default data directories:**
- **Windows:** `%APPDATA%\Bitcoin\`
- **macOS:** `~/Library/Application Support/Bitcoin/`
- **Linux/WSL:** `~/.bitcoin/`

### A.2 Enable Pruning (~1 GiB target)

Create or edit your configuration file:
- **Linux/WSL/macOS:** `~/.bitcoin/bitcoin.conf`
- **Windows:** `%APPDATA%\Bitcoin\bitcoin.conf`

Add:
```ini
prune=2048          # ~2 GiB on disk gives headroom to capture ~1 GiB archive
blocksdir=/path/to/where/you/want/blocks
```

### A.3 Start and Monitor the Node

```bash
# Daemon start
bitcoind -daemon

# Status
bitcoin-cli getblockchaininfo | jq '{blocks, headers, pruned, size_on_disk}'
```

### A.4 Stop and Package ~1 GiB of Raw Blocks

```bash
BLOCKS_DIR="${BLOCKS_DIR:-$HOME/.bitcoin}"

# Track live size
du -sh "${BLOCKS_DIR}/blocks"
ls -lh "${BLOCKS_DIR}/blocks/blk"*.dat | tail

# Clean shutdown
bitcoin-cli stop

# Package only raw blocks
tar -C "$BLOCKS_DIR" -czf btc_blocks_pruned_1GiB.tar.gz blocks
ARCHIVE_OUT="${ARCHIVE_OUT:-$PWD}"
mv btc_blocks_pruned_1GiB.tar.gz "$ARCHIVE_OUT/"
```

**Notes:**
- Set `prune=2048` when targeting ~1 GiB
- Core may exceed the target slightly to preserve at least 288 recent blocks
- When blocks reach ~1–1.2 GiB, stop the daemon before pruning removes older files

---

## Part B: Historical Bitcoin Prices from Kaggle

### B.1 Configure Kaggle API

```bash
conda create -n bda-env python=3.10 -y
conda activate bda-env
conda install -c conda-forge openjdk=21 maven -y
pip install --upgrade pip jupyterlab kaggle

mkdir -p ~/.kaggle
# Download kaggle.json from Kaggle: Account → Create New Token
mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json

# Sanity check
conda run -n bda-env kaggle --version
conda run -n bda-env kaggle datasets list -s bitcoin
```

### B.2 Download Candidate Datasets

**Option 1: Bitcoin Historical Data (multi-exchange, 1-minute bars)**

```bash
conda run -n bda-env kaggle datasets download \
  -d mczielinski/bitcoin-historical-data \
  -p project-final/data/prices --unzip --force
```

**Option 2: Bitcoin Historical Datasets 2018–2024 (Binance)**

```bash
conda run -n bda-env kaggle datasets download \
  -d novandraanugrah/bitcoin-historical-datasets-2018-2024 \
  -p project-final/data/prices --unzip --force
```

### B.3 Quick Load Test in Spark

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("bda-price-check").getOrCreate()
df = spark.read.option("header", True).csv("project-final/data/prices/*.csv")
df.select("date", "open", "high", "low", "close", "volume").show(5, truncate=False)
spark.stop()
```

---

## Sanity Checklist

- [ ] Bitcoin Core pruning configured: `prune=1024` in `bitcoin.conf`
- [ ] `bitcoin-cli getblockchaininfo` shows `"pruned": true`
- [ ] Raw blocks present: `blk*.dat` under data directory
- [ ] Size ~1–2 GiB after running for a while
- [ ] Price data available: CSV files in `project-final/data/prices/`
- [ ] Spark can read price CSVs without errors

---

## Useful References

- [Bitcoin Core Download](https://bitcoincore.org/en/download/)
- [Running a Full Node](https://bitcoin.org/en/full-node)
- [Prune Mode Release Notes](https://bitcoincore.org/en/releases/0.11.0/)
- [bitcoind Manual](https://man.archlinux.org/man/bitcoind.1)
- [Data Directory Locations](https://en.bitcoin.it/wiki/Data_directory)
- [Kaggle API Docs](https://www.kaggle.com/docs/api)
- [Kaggle: Bitcoin Historical Data](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data)
- [Kaggle: BTC/USDT Binance 2018–2024](https://www.kaggle.com/datasets/novandraanugrah/bitcoin-historical-datasets-2018-2024)
