---
tags:
  - cnt
  - breakout
  - shadow
  - review
---

# CNT v2 BREAKOUT V2 FILTER STACK DECOMPOSITION REVIEW

## Scope

This review decomposes the `breakout_v2` shadow filter stack using the completed shadow collection window.

Locked baseline facts:

- total shadow signals = `51`
- allowed signals = `0`
- filtered signals = `51`
- `breakout_v2` actual activation remains prohibited

## Current Outcome

`breakout_v2` did not produce a single allowed candidate during the 51-signal shadow window.

Current interpretation:

- quality is still unproven
- usability is currently too restrictive
- candidate generation remains blocked

## Filter Stack Order

Actual code order in [[breakout_v2]]:

1. range / upward bias gate
2. volatility gate
3. EMA trend gate
4. RSI threshold gate
5. breakout confirmation gate
6. VWAP distance gate
7. band width gate
8. band expansion gate
9. volume gate

## First Filter Fail Distribution

Observed first-blocker distribution from `logs/shadow_breakout_v2.jsonl`:

- `volatility_not_high = 28`
- `range_without_upward_bias = 7`
- `ema_fast_not_above_slow = 6`
- `range_bias_up_but_entry_trend_not_up = 5`
- `breakout_not_confirmed = 3`
- `vwap_distance_too_small = 1`
- `band_width_too_narrow = 1`
- `band_not_expanding = 0`
- `volume_not_confirmed = 0`

## Cumulative Pass / Fail By Stage

Using the observed first-blocker distribution in code order:

### Stage 1: Range / Upward Bias Gate

- fail count = `12`
  - `range_without_upward_bias = 7`
  - `range_bias_up_but_entry_trend_not_up = 5`
- remaining after stage 1 = `39`

### Stage 2: Volatility Gate

- fail count = `28`
- remaining after stage 2 = `11`

### Stage 3: EMA Trend Gate

- fail count = `6`
- remaining after stage 3 = `5`

### Stage 4: RSI Threshold Gate

- observed first failures = `0`
- remaining after stage 4 = `5`

### Stage 5: Breakout Confirmation Gate

- fail count = `3`
- remaining after stage 5 = `2`

### Stage 6: VWAP Distance Gate

- fail count = `1`
- remaining after stage 6 = `1`

### Stage 7: Band Width Gate

- fail count = `1`
- remaining after stage 7 = `0`

### Stage 8: Band Expansion Gate

- observed first failures = `0`
- remaining after stage 8 = `0`

### Stage 9: Volume Gate

- observed first failures = `0`
- remaining after stage 9 = `0`

## Conditional Analysis

### If Volatility Gate Were Hypothetically Bypassed

Current dominant first blocker is `volatility_not_high`.

If only the volatility gate were hypothetically bypassed while keeping the rest unchanged:

- raw first-blocker survivors from stage 2 onward would become `23`
  - calculation: `51 total - 28 volatility failures = 23`

But those 23 do **not** imply allowed candidates.

The observed first-blocker distribution already shows that, among non-volatility failures:

- `12` are still blocked by market/range structure
- `6` are still blocked by EMA trend
- `3` are still blocked by breakout confirmation
- `1` is still blocked by VWAP distance
- `1` is still blocked by band width

Therefore, a volatility-only relaxation is not yet proven to generate viable allowed candidates.

### Later-Stage Threshold Evidence

Observed numeric evidence from shadow events:

- `band_expansion_ratio >= 1.03` occurred `15` times
- `volume_ratio >= 1.5` occurred `13` times
- `band_width_ratio >= 0.006` occurred only `1` time

This means:

- band expansion alone is not sufficient
- volume strength alone is not sufficient
- band width is structurally tight in most sampled conditions

### Why Allowed Signal Still Remains Zero

The zero-allowed outcome is not explained by one metric alone.

The practical sequence is:

1. range/upward bias blocks a non-trivial base layer
2. volatility blocks the largest single layer
3. EMA trend removes more survivors
4. breakout confirmation removes more survivors
5. the final narrow-band condition removes the last remaining path

## Dominant Blocker Identification

Primary first blocker:

- `volatility_not_high`

But this is not sufficient to conclude that volatility is the only structural bottleneck.

More accurate wording:

`volatility_not_high` is the dominant first blocker, but candidate generation is still jointly constrained by multiple downstream filters.

## Single Or Multi-Blocker Judgment

Final judgment:

`multi-stage filtering is jointly blocking candidate generation`

Reason:

- there is a clear dominant first blocker
- but cumulative pass-through still reaches zero even after accounting for non-volatility stages
- later-stage metrics show occasional threshold success without producing allowed candidates

## Safe Next Adjustment Candidate

No immediate parameter change is safe yet.

The safest next candidate for future review is:

- **review the volatility gate first**

But current evidence does **not** support:

- immediate volatility-only relaxation
- immediate activation
- immediate parameter tuning

The next safe action remains analytical, not mutational.

## Final Conclusion

`breakout_v2 remains too restrictive without a single dominant bottleneck`

Supporting note:

- `volatility_not_high` is the primary first blocker
- candidate generation failure is still jointly enforced by multiple downstream gates

## Obsidian Links

- [[CNT v2 BREAKOUT V2 SHADOW VALIDATION SPEC]]
- [[CNT v2 BREAKOUT V2 SHADOW RUNTIME VERIFICATION]]
- [[CNT v2 BREAKOUT V2 DESIGN]]
