---
tags:
  - cnt
  - full-filter-rerun
  - readiness
created: 2026-04-27
---

# CNT Full Filter Rerun Ready Prep 20260427

## Verdict

```text
FULL_FILTER_RERUN_READY_PREP = COMPLETE
RUNTIME_CHANGE = NO
CONFIG_CHANGE = NO
STRATEGY_CHANGE = NO
POST_LOGGING_CLOSED_TRADES = 9
MIN_REQUIRED = 10
STATUS = WAIT
```

## Prepared Tool

```text
TOOL = tools/full_filter_rerun_exchange_replay.py
OUTPUT_JSON = reports/cnt_full_filter_rerun_20260427.json
OUTPUT_DOC = docs/CNT_FULL_FILTER_RERUN_20260427.md
```

## Execution Rule

```text
IF post_logging_closed_trades >= 10:
  python tools/full_filter_rerun_exchange_replay.py
ELSE:
  wait
```

## Feature Coverage

```text
PRE_RUNUP_30M = prepared
ENTRY_NEAR_HIGH = prepared
MFE = prepared
MAE = prepared
FAST_ADVERSE_MOVE = prepared
PRIMARY_UP_ENTRY_UP = prepared through market_context split
```

## Current Decision

```text
FILTER_PROMOTION = NO
CONFIG_CHANGE = HOLD
LIVE_TRANSITION = HOLD
```

## Record Text

2026-04-27: Full filter rerun preparation was completed. The replay tool is ready, but actual full rerun remains gated until one more post-logging closed trade is available.

Related:
- [[CNT_POST_LOGGING_PARTIAL_VALIDATION_20260427]]
- [[CNT_PRE_RUNUP_THRESHOLD_ANALYSIS_20260427]]
