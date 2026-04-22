---
tags:
  - cnt
  - breakout
  - isolation
  - review
---

# CNT v2 BREAKOUT ISOLATION FINAL REVIEW

## Isolation Window Status

- `isolation review closed`
- `baseline locked`
- `no further midpoint waiting`

## Purpose

This document closes the current `breakout_v1` isolation window after the midpoint target was exceeded without meaningful breakout trade growth.

## Baseline Versus Latest Delta

- isolation baseline snapshot:
  - `2026-04-22 12:44:03`
  - `total_signals = 660`
- latest review snapshot:
  - `2026-04-22 14:44:04`
  - `total_signals = 684`
- observed additional cycles:
  - `(684 - 660) / 2 = 12`

## Breakout_v1 Observed Result

- baseline
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`

- latest
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`

Interpretation:

- observed breakout trade sample did not grow
- observed breakout quality did not recover

## Mixed Portfolio Result

- baseline
  - `expectancy = -0.0007807916666668097`
  - `profit_factor = 0.9158659890090017`
  - `net_pnl = -0.018739000000003447`

- latest
  - `expectancy = -0.0007807916666668097`
  - `profit_factor = 0.9158659890090017`
  - `net_pnl = -0.018739000000003447`

Interpretation:

- mixed portfolio remains degraded
- no recovery signal was confirmed during this window

## Pullback Inferred Reference

- `trades_closed = 21`
- `expectancy = 0.0022788095238093107`
- `profit_factor = 1.3365141201619735`

Interpretation:

- pullback remains the positive reference strategy
- this remains an inferred reference, not a separately isolated observed portfolio

## Runtime Pattern Summary

Recent runtime outcomes were mostly:

- `DAILY_LOSS_LIMIT`
- `no_ranked_signal`

Observed sequence in the closing part of the window:

- repeated `EXECUTION_BLOCKED_BY_RISK`
- repeated `NO_ENTRY_SIGNAL`
- no new breakout close event

## Low-Sample Limitation

`breakout_v1` still has a low observed trade sample.

This review must not overstate certainty beyond the observed facts.
The correct conclusion is limited by the unchanged `trades_closed = 3`.

## Required Contents

This review includes:

- baseline versus latest delta
- `breakout_v1 observed` result
- `mixed portfolio observed` result
- `pullback inferred` reference

## Required Final Verdict

- `breakout remains negative, with low-sample limitation`

## Baseline Preservation Rule

This review must preserve:

- the original `LIVE_READY` record
- the later `FAIL / NON_POSITIVE_EXPECTANCY` record
- the distinction between observed and inferred baselines

## Obsidian Links

- [[CNT v2 BREAKOUT ISOLATION RUNTIME START]]
- [[CNT v2 BREAKOUT ISOLATION MIDPOINT CHECK]]
- [[CNT v2 POST-READY DEGRADATION REVIEW]]
