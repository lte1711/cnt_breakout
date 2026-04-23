---
tags:
  - cnt
  - docs
  - patch
  - shadow
  - state
  - v2
aliases:
  - CNT v2 SHADOW SEMANTICS AND PORTFOLIO STATE PATCH REPORT
---

# CNT v2 SHADOW SEMANTICS AND PORTFOLIO STATE PATCH REPORT

## Summary

This patch addresses two runtime-integrity problems that were safe to fix without changing live strategy activation.

Fixed:

- `breakout_v3` shadow event meaning consistency
- `portfolio_state` rebuild risk counter preservation

Not changed:

- `ACTIVE_STRATEGIES`
- order path
- live activation policy
- `breakout_v1` active status

## 1. Breakout V3 Shadow Semantics Fix

Observed defects:

- `allowed=true` events could still emit `first_blocker`
- `summary_reason` could indicate `trigger_blocked` while the first blocker came from `setup`

Applied fix:

- `first_blocker` and `hard_blocker` are now `null` for allowed events
- `summary_reason` now follows the first failed stage order:
  - `regime_blocked`
  - `setup_blocked`
  - `trigger_blocked`
  - `hard_pass_but_soft_count_insufficient`

Interpretation:

- shadow events are now internally self-consistent at the evaluator level
- historical log lines remain historical and should not be interpreted as post-fix pure baseline

## 2. Portfolio State Risk Counter Preservation

Observed defect:

- `build_portfolio_state()` rebuilt `portfolio_state.json` from runtime state
- but `daily_loss_count` and `consecutive_losses` could fall back to zero during rebuild

Applied fix:

- rebuild now copies risk counters from `runtime_state["risk_metrics"]`
- this applies both:
  - when no open trade exists
  - when an open trade exists

Interpretation:

- `portfolio_state.json` is now aligned with runtime loss-counter reality
- this reduces monitoring and downstream automation misread risk

## 3. Validation

Executed:

```text
PYTHONPATH=. python -m pytest -q
```

Result:

```text
53 passed
```

## 4. Remaining Priority

This patch does not resolve the primary live-performance issue.

Still open:

- `breakout_v1` remains active and negative

That issue remains an operating decision problem, not a shadow/state integrity problem.

## Obsidian Links

- [[CNT v2 BREAKOUT V3 SHADOW EVALUATOR IMPLEMENTATION REPORT]]
- [[CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START]]
- [[CNT v2 CURRENT STATUS ASSESSMENT]]
- [[00 Docs Index|Docs Index]]
