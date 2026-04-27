---
tags:
  - cnt
  - type/documentation
  - status/active
  - context-filter
  - type/operation
  - strategy/breakout_v3
---

---
---

# CNT v2 BREAKOUT V2 SHADOW SCHEMA LIMITATION REVIEW

## Scope

This review documents what the current `breakout_v2` shadow schema can and cannot directly prove.

## Currently Observable Fields

Current shadow event schema in shadow_eval.py directly records:

- `ts`
- `symbol`
- `strategy`
- `signal_generated`
- `entry_allowed`
- `filter_reason`
- `confidence`
- `vwap`
- `band_width_ratio`
- `band_expansion_ratio`
- `volume_ratio`
- `hypothetical_entry`

Current shadow snapshot directly records:

- `signal_count`
- `filtered_signal_count`
- `allowed_signal_count`
- `filtered_signal_ratio`
- `allowed_signal_ratio`
- `hypothetical_trades_count`
- `hypothetical_expectancy`
- `hypothetical_profit_factor`
- `stop_exit_ratio`
- `reason_distribution`
- `last_updated`

## What The Current Schema Can Prove

The schema is sufficient to prove:

- first-blocker distribution
- total candidate starvation
- current measured ratios for:
  - band width
  - band expansion
  - volume
- whether shadow output is being written safely at runtime

## What The Current Schema Cannot Prove Directly

The schema does **not** directly expose downstream secondary failures once the first blocker has already fired.

That means it cannot directly answer, per event:

- whether EMA would also have failed
- whether breakout confirmation would also have failed
- whether VWAP distance would also have failed
- whether multiple downstream failures coexisted in the same event

## Why EMA Secondary Tracking Is Needed

Current shadow data shows `ema_fast_not_above_slow` as a meaningful first blocker in the overall set.

But for volatility-blocked events, we cannot tell:

- how many would still fail EMA if volatility were relaxed

Without that visibility, volatility-only relaxation cannot be evaluated safely.

## Why Breakout Confirmation Secondary Tracking Is Needed

Current shadow data shows `breakout_not_confirmed` as a meaningful first blocker elsewhere in the stack.

But for volatility-blocked events, we cannot tell:

- how many would later collapse at breakout confirmation even after volatility relaxation

That means the current schema can only approximate downstream survivability, not prove it.

## Why VWAP / Band / Volume Boolean Trace Still Matters

Although current numeric fields help, numeric ratios alone do not preserve the exact pass/fail trace of the live code path.

For example:

- `band_expansion_ratio` may be known
- but whether the event had already failed earlier gates remains implicit

This makes conditional decomposition weaker than it should be.

## Current Limitation Verdict

`schema expansion required before further tuning decisions`

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN]]

