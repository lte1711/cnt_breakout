---
---

# CNT v2 BREAKOUT V2 SHADOW RUNTIME VERIFICATION

## Verification Scope

This document records one-shot runtime verification for the implemented `breakout_v2` shadow runtime.

Verification goal:

- confirm shadow files are created and updated
- confirm one-shot engine cycle still finishes normally
- confirm live execution path remains unchanged

## Runtime Timestamp

- verification run timestamp: `2026-04-22 15:21:04`
- entry chain used: `run.ps1 -> main.py -> src.engine.start_engine`

## Pre-Run Baseline

### Shadow Files

- `logs/shadow_breakout_v2.jsonl` existed
- pre-run log line count: `1`
- `data/shadow_breakout_v2_snapshot.json` existed
- pre-run snapshot `signal_count = 1`

### Live Runtime State

- `pending_order = null`
- `open_trade = null`
- `action = EXECUTION_BLOCKED_BY_RISK`
- `risk_metrics.daily_loss_count = 3`
- `risk_metrics.consecutive_losses = 2`

## Post-Run Result

### File Creation And Update Result

- `logs/shadow_breakout_v2.jsonl` update: `PASS`
- `data/shadow_breakout_v2_snapshot.json` update: `PASS`
- one-shot runtime finish: `PASS`

### Shadow Jsonl Sample

Latest appended event:

```json
{
  "ts": "2026-04-22T15:21:04+09:00",
  "symbol": "ETHUSDT",
  "strategy": "breakout_v2_shadow",
  "signal_generated": true,
  "entry_allowed": false,
  "filter_reason": "ema_fast_not_above_slow",
  "confidence": 0.0,
  "vwap": 2392.860945341745,
  "band_width_ratio": 0.0014372585160929232,
  "band_expansion_ratio": 0.9933736612462483,
  "volume_ratio": 0.009791072392259657,
  "hypothetical_entry": false
}
```

### Shadow Snapshot Sample

```json
{
  "strategy": "breakout_v2_shadow",
  "signal_count": 2,
  "filtered_signal_count": 2,
  "allowed_signal_count": 0,
  "filtered_signal_ratio": 1.0,
  "allowed_signal_ratio": 0.0,
  "hypothetical_trades_count": 0,
  "hypothetical_expectancy": 0.0,
  "hypothetical_profit_factor": 0.0,
  "stop_exit_ratio": 0.0,
  "reason_distribution": {
    "ema_fast_not_above_slow": 2
  },
  "last_updated": "2026-04-22T15:21:04+09:00"
}
```

## Execution Path Unchanged Confirmation

Observed live runtime remained on the existing production branch:

- selected strategy in portfolio log: `pullback_v1`
- runtime result: `EXECUTION_BLOCKED_BY_RISK`
- reason: `DAILY_LOSS_LIMIT`
- `pending_order` remained `null`
- `open_trade` remained `null`

No evidence was observed that `breakout_v2` entered:

- execution decision
- order submission
- pending order state
- open trade state

## Sanity Checks

- jsonl append count increased: `1 -> 2`
- snapshot `signal_count` increased: `1 -> 2`
- `reason_distribution` recorded correctly
- `last_updated` recorded correctly

## Known Limitations

Current shadow runtime is intentionally limited.

- `hypothetical_expectancy` is not yet lifecycle-derived
- `hypothetical_profit_factor` is not yet lifecycle-derived
- `stop_exit_ratio` is not yet lifecycle-derived
- current verification confirms runtime integration, not candidate profitability

## Final Verification Verdict

`breakout_v2` shadow runtime is integrated and writing safely.

Production execution remains unchanged.

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN]]

