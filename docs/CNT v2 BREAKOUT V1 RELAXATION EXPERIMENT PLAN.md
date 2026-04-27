---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - offline-experiment
  - type/operation
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - type/analysis
  - cnt-v2-breakout-v1-relaxation-experiment-plan
---

# CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT PLAN

```text
DOCUMENT_NAME = cnt_v2_breakout_v1_relaxation_experiment_plan
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = ACTIVE
PURPOSE       = start the first controlled breakout_v1 relaxation experiment on testnet
```

---

# 1. OBJECTIVE

Open the first candidate or selection path for `breakout_v1` without changing the overall engine structure.

This experiment is intended to test whether the current zero-selection state is caused by overly strict breakout thresholds.

---

# 2. PRECONDITIONS

Confirmed before experiment start:

* observability gate = PASS
* fresh runtime observability proof = PASS
* tests = PASS
* `pending_order = null`
* `open_trade = null`

---

# 3. CHANGE SCOPE

Only `config.py` breakout strategy parameters are changed.

Changed values:

* `atr_expansion_multiplier: 1.2 -> 1.05`
* `rsi_threshold: 55 -> 53`

Unchanged values:

* `breakout_lookback = 3`
* `target_pct`
* `stop_loss_pct`
* all pullback and portfolio risk settings

Not allowed:

* `atr_expansion_multiplier = 1.0`

---

# 4. EXECUTION MODE

```text
ENVIRONMENT = Binance Spot Testnet
MODE        = scheduled one-shot cycles
RANGE       = 20 to 50 cycles target observation window
```

Operational rule:

* no overlapping manual runs

---

# 5. REQUIRED OBSERVATION ITEMS

1. `breakout_v1` reaches `entry_allowed=True`
2. `candidate_count > 0` includes breakout
3. `selected_strategy=breakout_v1` occurs at least once
4. `selection_reason=highest_score` appears in runtime logs
5. `selected_strategy_counts` starts reflecting selection-path evidence
6. rejection distribution changes in:
   * `market_not_trend_up`
   * `trend_not_up`
   * `volatility_not_high`
   * `rsi_below_entry_threshold`
   * `breakout_not_confirmed`

---

# 6. KNOWN PARALLEL TRACKING ITEMS

These do not block experiment start, but must be tracked in the report:

1. `selected_strategy_counts` is still `{}` at experiment start
2. `run.ps1` can hit `scheduler_stdout.log` write collision during overlapping manual launches

---

# 7. SUCCESS RULE

Primary success:

* breakout enters candidate path or selection path

Still meaningful even without selection:

* rejection distribution changes in a way that shows the bottleneck moved

---

# 8. OUTPUT

Experiment result must be stored in:

* `docs/CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT REPORT.md`

---

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]

