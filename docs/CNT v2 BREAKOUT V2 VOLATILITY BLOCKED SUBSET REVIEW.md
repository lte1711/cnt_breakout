---
tags:
  - cnt
  - type/documentation
  - status/active
  - strategy/breakout_v3
---

---
---

# CNT v2 BREAKOUT V2 VOLATILITY BLOCKED SUBSET REVIEW

## Scope

This review isolates the `volatility_not_high` first-blocker subset from the 51-event `breakout_v2` shadow dataset.

Goal:

- test whether volatility-only relaxation could produce viable candidates
- measure downstream blocking inside the volatility-blocked subset

## Subset Size

- total shadow signals = `51`
- volatility-blocked subset = `28`

## Subset Timestamps

- `2026-04-22T15:54:03+09:00`
- `2026-04-22T16:04:03+09:00`
- `2026-04-22T16:14:03+09:00`
- `2026-04-22T16:44:03+09:00`
- `2026-04-22T16:54:03+09:00`
- `2026-04-22T17:04:03+09:00`
- `2026-04-22T17:14:04+09:00`
- `2026-04-22T17:24:04+09:00`
- `2026-04-22T18:14:03+09:00`
- `2026-04-22T18:24:03+09:00`
- `2026-04-22T18:34:04+09:00`
- `2026-04-22T18:44:04+09:00`
- `2026-04-22T19:44:04+09:00`
- `2026-04-22T20:04:04+09:00`
- `2026-04-22T20:24:04+09:00`
- `2026-04-22T20:34:08+09:00`
- `2026-04-22T20:44:03+09:00`
- `2026-04-22T20:54:03+09:00`
- `2026-04-22T21:04:03+09:00`
- `2026-04-22T21:14:04+09:00`
- `2026-04-22T21:24:03+09:00`
- `2026-04-22T21:34:03+09:00`
- `2026-04-22T21:44:04+09:00`
- `2026-04-22T21:54:03+09:00`
- `2026-04-22T22:04:03+09:00`
- `2026-04-22T22:14:03+09:00`
- `2026-04-22T22:24:03+09:00`
- `2026-04-22T22:34:03+09:00`

## Review Limitation

Current shadow log schema preserves:

- first blocker reason
- `band_width_ratio`
- `band_expansion_ratio`
- `volume_ratio`

It does **not** preserve per-event downstream boolean results for:

- EMA trend gate
- breakout confirmation gate
- VWAP distance gate

Therefore, this subset review can confirm downstream bottlenecks only for the measured shadow fields and can infer the rest only conservatively.

## Secondary Blockers Inside The Volatility-Blocked Set

### Measured Post-Volatility Checks

Among the 28 volatility-blocked events:

- `EMA fail count = not directly observed in shadow schema`
- `breakout confirmation fail count = not directly observed in shadow schema`
- `band width fail count = 28`
- `band expansion fail count = 19`
  - because only `9 / 28` reached `band_expansion_ratio >= 1.03`
- `volume fail count = 20`
  - because only `8 / 28` reached `volume_ratio >= 1.5`

### Measured Threshold Summary

- `band_expansion_ratio >= 1.03` occurred `9 / 28`
- `volume_ratio >= 1.5` occurred `8 / 28`
- `band_width_ratio >= 0.006` occurred `0 / 28`

This is the strongest observed result in the subset:

`band width remains below threshold for all 28 volatility-blocked events`

## Conditional Pass-Through

### Assumption

Hypothetical review assumes:

- volatility gate only is relaxed
- all later gates remain unchanged

### Survivors After Volatility Relaxation

From the measured subset metrics:

- survive `band_expansion` threshold: `9`
- survive `volume` threshold: `8`
- survive `band_width` threshold: `0`
- survive all measured later thresholds together: `0`

## Meaning

Even if volatility were relaxed:

- some events would still show sufficient band expansion
- some events would still show sufficient volume
- **none** of the 28 events would pass the current `band_width_ratio >= 0.006` threshold

So the subset collapses before any final candidate can emerge.

## Interpretation

This does **not** prove that volatility is unimportant.

It proves a narrower statement:

`volatility relaxation alone is insufficient`

Why:

1. volatility is the dominant first blocker
2. but inside that subset, `band_width` still rejects all measured events
3. and EMA / breakout confirmation are not yet proven to become non-issues

## Final Conclusion

`subset still collapses in later filters`

Supporting interpretation:

- volatility remains the primary first blocker
- but volatility-only relaxation would still leave the subset with zero measured survivors because `band_width` remains structurally below threshold

## Safe Next Adjustment Candidate

No immediate config change is justified.

The safest next analytical candidate is:

- review the relationship between `volatility_not_high` and `band_width_too_narrow`

In practical terms:

- determine whether the volatility gate and band-width gate are partially redundant
- determine whether one should dominate the other in future design review

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN]]

