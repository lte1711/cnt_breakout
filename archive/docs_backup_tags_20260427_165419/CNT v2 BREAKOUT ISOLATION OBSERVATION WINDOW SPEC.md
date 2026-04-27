---
aliases:
  - CNT v2 BREAKOUT ISOLATION OBSERVATION WINDOW SPEC
---

# CNT v2 BREAKOUT ISOLATION OBSERVATION WINDOW SPEC

## Purpose

This spec defines the observation window for breakout isolation diagnosis.

It does **not** disable breakout immediately.

It defines how breakout quality should be separated from mixed portfolio quality.

## Observation Window

- duration basis: `20 to 30 additional runtime cycles`
- review mode: fact-based observation only
- parameter changes: frozen during this window

## Minimum Sample Requirement

Breakout-specific observation must not be overstated before:

- `breakout_v1 trades_closed >= 5`

Until then:

- breakout quality can be described only as low-sample observed quality

## Mid-Window Checkpoints

Use two checkpoints:

1. midpoint review:
   - after `10 additional cycles`
2. final review:
   - after `20 to 30 additional cycles`

## Required Comparison Axes

Always compare these three baselines separately:

1. `mixed portfolio`
2. `breakout observed baseline`
3. `pullback inferred baseline`

## Required Metrics

Track all of the following for each review:

- `expectancy`
- `profit_factor`
- `execution_rate`
- `execution_block_rate`
- `no_candidate_rate`

Where applicable, also include:

- `trades_closed`
- `wins`
- `losses`
- `net_pnl`

## Comparison Table Format

| Baseline | Closed Trades | Expectancy | PF | Net PnL | Execution Rate | Execution Block Rate | No Candidate Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Mixed | ... | ... | ... | ... | ... | ... | ... |
| Breakout observed | ... | ... | ... | ... | ... | ... | ... |
| Pullback inferred | ... | ... | ... | ... | ... | ... | ... |

## Exit Conditions

### Exit 1 — Breakout Quality Recover

Use if:

- breakout expectancy turns positive
- breakout PF rises above 1
- additional observed trades support that improvement

### Exit 2 — Breakout Remains Negative

Use if:

- breakout expectancy stays negative
- breakout PF remains below 1
- negative contribution continues after additional sample

### Exit 3 — Insufficient Sample

Use if:

- breakout still has too few closed trades to support a stronger claim

## Required Guardrails

- no immediate breakout disable
- no risk guard loosening
- no large parameter tuning before the window completes

## Overstatement Prohibition

The following wording is forbidden:

- calling an inferred pullback baseline an observed baseline
- claiming breakout is permanently invalid from only the current 3-trade sample
- claiming recovery from only one positive breakout trade

## Recommended Review Sentence

Use wording like:

- `breakout remains under isolated observation and has not yet earned an operating-quality conclusion beyond the current observed sample`

## Required Conclusion

**breakout isolation window ready**

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT]]

