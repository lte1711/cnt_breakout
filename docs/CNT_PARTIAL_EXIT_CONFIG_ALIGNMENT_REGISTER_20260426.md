---
tags:
  - cnt
  - config
  - risk
  - follow-up
status: ACTIVE
created: 2026-04-26
---

# CNT Partial Exit Config Alignment Register 20260426

## Design Summary

- Scope: register the current `ENABLE_PARTIAL_EXIT` and `PARTIAL_EXIT=FORBIDDEN` mismatch as a follow-up item.
- No code, config, runtime state, or order behavior was changed in this step.
- Current decision: keep the running system unchanged for now, continue observation, and fix the mismatch before live readiness approval.

## Registered Item

```text
DATE=2026-04-26
TYPE=config
PATH=config.py
SUMMARY=ENABLE_PARTIAL_EXIT remains True while AGENTS.md forbids partial exit.
REASON=Current runtime has no open_trade and no pending_order, and DAILY_LOSS_LIMIT is blocking new entries. Immediate runtime risk is low, but the config and constitution are not aligned.
CURRENT_DECISION=review_next
NEXT_ACTION=Before live approval, set ENABLE_PARTIAL_EXIT=False and add a runtime guard so stored partial_exit_levels cannot trigger partial exits when the feature is disabled.
NOTE=Do not change during active observation unless a controlled patch window is opened and tests are updated.
```

## Current Risk Judgment

```text
LEAVE_AS_IS_NOW              = ACCEPTABLE
IMMEDIATE_RUNTIME_RISK       = LOW
CONSTITUTION_ALIGNMENT       = NOT_CLEAN
ACTION_URGENCY              = NOT_URGENT
LIVE_APPROVAL_BLOCKER        = YES_UNTIL_ALIGNED
```

## Required Follow-Up

1. Reconfirm `data/state.json` has no `open_trade` and no `pending_order`.
2. Change `config.py` from `ENABLE_PARTIAL_EXIT = True` to `ENABLE_PARTIAL_EXIT = False`.
3. Add a runtime guard so existing `partial_exit_levels` are ignored when partial exits are disabled.
4. Update or reclassify tests that currently expect partial exit execution.
5. Run validation with `PYTHONPATH=.` and `pytest -q`.
6. Record the result in a follow-up implementation report.

## Validation Result

FACT:

- `config.py` currently contains `ENABLE_PARTIAL_EXIT = True`.
- `AGENTS.md` currently contains `PARTIAL_EXIT=FORBIDDEN`.
- Current local runtime state previously showed no open trade and no pending order at the latest reviewed checkpoint.

VERIFIED:

- Leaving the setting unchanged is acceptable for current observation, but not acceptable as a final live-readiness state.

## Record Text

The partial-exit mismatch is registered as a follow-up alignment item. It is not being changed immediately because current runtime exposure is zero and new entries are blocked by the daily loss guard. The next implementation pass must align config and runtime behavior with the constitution before any live readiness approval.

Related documents:

- [[AGENTS]]
- [[CNT_PRECISION_ANALYSIS_REPORT_20260426]]
- [[CNT_PROJECT_STATUS_REPORT_20260426]]
- [[CNT v2 LIVE READINESS GATE]]
- [[00 Docs Index]]
