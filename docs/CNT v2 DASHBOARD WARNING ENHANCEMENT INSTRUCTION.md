---
tags:
  - cnt
  - docs
  - v2
  - dashboard
  - instruction
aliases:
  - CNT v2 DASHBOARD WARNING ENHANCEMENT INSTRUCTION
---

# CNT v2 DASHBOARD WARNING ENHANCEMENT INSTRUCTION

## Purpose

The current dashboard already loads the correct runtime files, but it should show post-ready degradation signals more directly at the top of the screen.

## Required Warning Additions

Expose the following warnings more prominently in the top alert area:

1. `FAIL reason`
2. `expectancy < 0`
3. `PF < 1`
4. `daily_loss_count reached`
5. `breakout_v1 negative expectancy`

## Exact Warning Targets

### A. Fail Reason Banner

If `live_gate_decision.status = FAIL`, show:

- `FAIL`
- `reason = NON_POSITIVE_EXPECTANCY` or current evaluator reason

This should appear above or alongside the current gate card, not only inside secondary text.

### B. Negative Expectancy Warning

If `snapshot.expectancy <= 0`, show:

- `EXPECTANCY BELOW ZERO`

Include the current value.

### C. PF Below One Warning

If `snapshot.profit_factor < 1`, show:

- `PF BELOW 1`

Include the current PF value.

### D. Daily Loss Count Warning

If `state.risk_metrics.daily_loss_count >= 3`, show:

- `DAILY LOSS COUNT REACHED`

This is different from cumulative `DAILY_LOSS_LIMIT` runtime hits and should be displayed separately.

### E. Breakout Negative Expectancy Warning

If `metrics.breakout_v1.expectancy < 0`, show:

- `BREAKOUT NEGATIVE EXPECTANCY`

Include:

- current breakout expectancy
- current breakout PF
- current breakout trades_closed

## UI Placement

Recommended placement:

- first row alert stack
- or a dedicated top banner above `System Health`

These warnings should not require scrolling.

## Why This Matters

The current dashboard already shows:

- system state
- gate state
- baseline deltas

But it does not yet force the operator to see the exact reason why `LIVE_READY` was lost.

The warning enhancement should reduce interpretation delay.

## Required Conclusion

**gate/display consistency patch required**

## Obsidian Links

- [[CNT v2 GATE DISPLAY CONSISTENCY AUDIT]]
- [[CNT v2 POST-READY DEGRADATION REVIEW]]
- [[00 Docs Index|Docs Index]]
