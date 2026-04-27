---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - strategy/breakout_v3
  - status/completed
---

---
---

# CNT v2 BREAKOUT V2 GATE REDUNDANCY REVIEW

## Scope

This review evaluates the relationship between the `volatility_not_high` gate and the `band_width_too_narrow` gate in `breakout_v2`.

The goal is not to tune either gate.

The goal is to determine whether they appear:

- structurally redundant
- structurally dependent
- or still too weakly evidenced for a stronger conclusion

## Observed Facts

Locked facts from the completed shadow window:

- total shadow signals = `51`
- first blocker `volatility_not_high = 28`
- volatility-blocked subset = `28`
- inside that subset:
  - `band_width_ratio >= 0.006` occurred `0 / 28`
  - `band_expansion_ratio >= 1.03` occurred `9 / 28`
  - `volume_ratio >= 1.5` occurred `8 / 28`
- hypothetical survivors after volatility-only relaxation = `0`

## Overlap Observation

The strongest overlap finding is:

- `volatility_not_high` blocks `28` events
- all `28` of those events also have `band_width_ratio < 0.006`

This means that, within the volatility-blocked subset:

- the current band-width threshold would reject every event even if the volatility gate were bypassed

## Same-Market-State Hypothesis

This pattern strongly suggests that the two gates may be responding to the same underlying market condition:

- weak volatility regime
- narrow range structure
- insufficient breakout expansion context

That said, the current evidence supports a hypothesis, not a proof.

Why it is not yet proven:

- current shadow schema captures first blocker plus numeric ratios
- it does not capture a full per-stage boolean trace for every gate
- therefore the exact dependency direction is still unobserved

## Redundancy Candidate Assessment

Possible interpretations:

1. `volatility_not_high` and `band_width_too_narrow` are partially redundant
2. `volatility_not_high` is a coarse upstream regime gate while `band_width_too_narrow` is a narrower downstream structure gate

Current evidence is strongest for the second interpretation.

## Dependency Assessment

Current best-fit interpretation:

`volatility_not_high` and `band_width_too_narrow` are dependent but not yet proven redundant

Reason:

- they co-occur strongly in the reviewed subset
- but they operate at different conceptual layers
  - volatility gate = regime filter
  - band width gate = local structure filter
- no direct per-event stage trace currently proves that one can fully replace the other

## Representative Gate Candidate

At this stage, no gate should be removed.

However, for future design review:

- `volatility_not_high` is the better candidate for the upstream representative regime gate
- `band_width_too_narrow` is the better candidate for the downstream local-structure gate

This distinction should be preserved until a richer shadow schema proves one gate can safely absorb the role of the other.

## Why Immediate Threshold Tuning Is Prohibited

Immediate tuning is not justified because:

1. volatility-only relaxation still produces zero measured survivors
2. band-width-only relaxation has not been validated
3. the dependency structure between the two gates is not fully traced
4. downstream EMA and breakout confirmation interactions remain only partially observed

## Final Conclusion

`volatility and band_width are dependent but not yet proven redundant`

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN]]

