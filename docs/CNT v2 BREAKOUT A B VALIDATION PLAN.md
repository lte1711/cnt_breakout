---
tags:
  - cnt
  - type/documentation
  - status/active
  - post-logging
  - context-filter
  - type/validation
  - type/operation
  - strategy/breakout_v3
---

---
---

# CNT v2 BREAKOUT A B VALIDATION PLAN

## Purpose

This plan defines how to compare the currently observed `breakout_v1` against the newly implemented `breakout_v2` without immediately switching production runtime.

The purpose is validation, not direct promotion.

## Validation Scope

### A Arm

- `breakout_v1 observed baseline`
- role: current observed strategy under isolation review
- source type: observed runtime baseline

### B Arm

- `breakout_v2 candidate`
- role: stricter quality-filter breakout candidate
- source type: candidate strategy for next validation

## Baseline Preservation Rule

The current baseline must remain intact.

Rules:

- do not remove `breakout_v1`
- do not overwrite existing `breakout_v1` isolation observations
- do not silently replace `breakout_v1` with `breakout_v2`
- do not switch production runtime directly from A to B

## Direct Production Switch

Direct production switch is forbidden at this stage.

`breakout_v2` must pass validation gates before it can be considered for active strategy inclusion.

## Comparison Metrics

The A/B comparison must always include:

- `trades_closed`
- `expectancy`
- `profit_factor`
- `net_pnl`
- `win_rate`
- `execution_rate`
- `filtered_signal_ratio`
- `stop_exit_ratio`

### Metric Meaning

- `execution_rate`
  - executed trades divided by selected signals
- `filtered_signal_ratio`
  - filtered or blocked signals divided by total candidate opportunities in the validation window
- `stop_exit_ratio`
  - stop-based closes divided by all closed trades

## Activation Gating For `breakout_v2`

Before `breakout_v2` can be added to `ACTIVE_STRATEGIES`, all of the following must be satisfied:

1. minimum sample reached
   - recommended minimum: `trades_closed >= 5`
2. `expectancy > 0`
3. `profit_factor > 1`
4. no severe regression versus current breakout baseline
5. no structural issue
   - no logging breakage
   - no runtime state inconsistency
   - no dashboard or metrics mismatch caused by the new strategy

## Promotion And Rejection Criteria

Only the following final conclusions are allowed:

1. `promote breakout_v2 candidate`
2. `keep observing breakout_v1`
3. `reject breakout_v2 for now`
4. `insufficient sample`

### Promote `breakout_v2 candidate`

Use only if:

- sample is sufficient
- `expectancy > 0`
- `profit_factor > 1`
- stop exit pressure is not materially worse
- no structural/runtime regression appears

### Keep Observing `breakout_v1`

Use if:

- `breakout_v2` is still under-sampled
- `breakout_v1` isolation evidence is still incomplete
- the comparison window is not yet mature

### Reject `breakout_v2 for now`

Use if:

- `breakout_v2` remains negative
- stop exits dominate
- filtered quality does not translate into better closed-trade quality
- runtime behavior introduces operational noise or instability

### Insufficient Sample

Use if:

- either arm has too little closed-trade evidence for a fair comparison

## Validation Window Recommendation

- keep current `breakout_v1` isolation record intact
- define a separate validation window for `breakout_v2`
- compare observed outcomes only after the candidate has enough closed trades

## Reporting Rule

Observed and inferred baselines must remain clearly separated.

- `breakout_v1 observed baseline` = observed
- `breakout_v2 candidate` = candidate validation result
- `pullback baseline` = inferred unless directly isolated and observed

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]

