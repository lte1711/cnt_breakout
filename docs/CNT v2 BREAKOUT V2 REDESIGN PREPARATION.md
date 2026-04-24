---
aliases:
  - CNT v2 BREAKOUT V2 REDESIGN PREPARATION
---

# CNT v2 BREAKOUT V2 REDESIGN PREPARATION

## Current Status

- `breakout_v2` = `FAILED_DESIGN_IN_CURRENT_FORM`
- runtime mode = `SHADOW_ONLY`
- activation = `PROHIBITED`
- tuning = `PROHIBITED`

This document is a redesign-preparation note, not an implementation instruction.

## Why Redesign Is Required

The latest expanded shadow evidence shows:

- sufficient shadow sample
- `allowed_signal_count = 0`
- no hypothetical trade generation
- multi-stage failure structure across:
  - market bias
  - breakout confirmation
  - VWAP distance
  - band width
  - band expansion
  - volume

This means the current design does not merely need threshold adjustment. It needs structural reconsideration.

## Redesign Constraints

The following remain fixed:

- `breakout_v2` must not be activated
- `ACTIVE_STRATEGIES` must remain unchanged
- `risk guard` must not be modified
- `live gate evaluator` must not be relaxed
- `pullback_v1` remains the active positive driver
- `breakout_v1` remains the negative reference strategy

## Candidate Redesign Directions

### Option A: Gate Reduction

Keep only a smaller set of hard mandatory conditions and move the rest into scoring or confidence shaping.

Possible structure:

- hard gate:
  - market bias
  - breakout confirmation
- soft score:
  - VWAP distance
  - band width
  - band expansion
  - volume

### Option B: Sequential Confirmation

Split the design into:

1. breakout trigger detection
2. confirmation stage
3. entry permission stage

This could reduce the current all-at-once AND-stack behavior.

### Option C: Weighted Scoring

Replace strict AND stacking with weighted quality scoring.

Possible structure:

- breakout detected
- each confirmation factor contributes score
- entry only if aggregate score crosses threshold

## What Must Not Happen Next

The following are explicitly blocked:

- volatility-only relaxation
- band-width-only relaxation
- partial ad hoc threshold edits
- direct production activation

## Immediate Next Design Deliverable

The next safe deliverable is a redesign option review that compares:

- gate reduction
- sequential confirmation
- weighted scoring

without changing runtime behavior.

## Recommended Status Label

For repository and operational interpretation, the correct current label is:

> `breakout_v2 = failed design (inactive experimental strategy)`

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN]]

