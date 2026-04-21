---
tags:
  - cnt
  - dashboard
  - operations
  - guide
aliases:
  - CNT Operations Dashboard Guide
---

# CNT Operations Dashboard Guide

## Purpose

This guide explains how to use the CNT operations dashboard that reads current runtime data and presents decision-oriented status for CNT testnet operation.

## Files

- HTML dashboard: [cnt_operations_dashboard.html](</c:/cnt/docs/cnt_operations_dashboard.html>)
- launcher script: [serve_dashboard.py](/c:/cnt/scripts/serve_dashboard.py)

## What This Dashboard Adds

The dashboard is not only a metric viewer.

It adds:

- system health interpretation
- gate readiness interpretation
- alert blocks for weak operating states
- pipeline bottleneck visibility
- strategy quality labels
- small delta tracking using browser local storage

## Runtime Sources

The dashboard reads:

- `data/performance_snapshot.json`
- `data/strategy_metrics.json`
- `data/state.json`
- `data/live_gate_decision.json`

## How To Use

Run from repository root:

```powershell
python scripts/serve_dashboard.py
```

Then open:

```text
http://127.0.0.1:8000/docs/cnt_operations_dashboard.html
```

## Interpretation Notes

- `READY` is not based only on `closed_trades >= 20`
- dashboard gate rule is:
  - `closed_trades >= 20`
  - `profit_factor >= 1.1`
  - `expectancy > 0`
- `RANKER FAILURE` and `CANDIDATE STARVATION` are heuristic warning layers for operation support
- candidate shortage is currently inferred from pipeline ratios and blocked counts because dedicated candidate-count telemetry is not yet stored in the snapshot

## Limitation

- this dashboard depends on the repository being served over HTTP
- it must be opened relative to CNT repository root
- it uses current runtime files and does not replace fact-based CNT reports
- delta comparison is browser-local and based on previous snapshot stored in local storage

## Obsidian Links

- [[CNT DATA DASHBOARD]]
- [[CNT TOOLCHAIN INTEGRATION REPORT]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[00 Docs Index|Docs Index]]
