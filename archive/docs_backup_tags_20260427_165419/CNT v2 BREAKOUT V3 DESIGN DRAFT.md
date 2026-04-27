---
aliases:
  - CNT v2 BREAKOUT V3 DESIGN DRAFT
---

# CNT v2 BREAKOUT V3 DESIGN DRAFT

## Status

- status = `DRAFT`
- implementation = `NOT STARTED`
- validation_mode = `SHADOW_ONLY_REQUIRED_BEFORE_ANY_ACTIVATION`

## Objective

`breakout_v3` is a structural redesign candidate created after `breakout_v2` was classified as a failed design in its current form.

The goal is not to tune `breakout_v2`.

The goal is to define a breakout structure that:

1. can generate real candidates
2. preserves signal quality
3. remains explainable stage by stage
4. fits the existing CNT validation framework without forcing a full ranking-model rewrite

## Failure Lessons From breakout_v2

Observed lessons from `breakout_v2` shadow review:

- zero allowed signals across a materially sufficient shadow sample
- first blocker was not stable as one single dominant cause
- downstream blocker structure was strongly multi-stage
- the strategy behaved as an over-constrained all-gates-pass design

Key failure patterns included:

- market bias failure
- breakout confirmation failure
- VWAP distance failure
- band width failure
- band expansion failure
- volume confirmation failure

This means the next design should avoid a strict simultaneous-AND structure across every quality dimension.

## Core Design Principle

`breakout_v3` is not a tuned continuation of `breakout_v2`.
It is a structural redesign intended to replace the over-constrained all-gates-pass logic of `breakout_v2`.

The core redesign principle is sequential confirmation:

`market regime -> setup formation -> breakout trigger -> entry quality confirmation -> execution decision`

In `breakout_v3`, market regime and breakout confirmation remain hard requirements.
Secondary quality conditions are evaluated as a soft confirmation group rather than a strict all-pass chain.

Activation is prohibited at design stage.
Initial validation must be shadow-only.

## Design Principles

### 1. Sequential Confirmation

Market conditions should be evaluated in the order they actually emerge in live markets.

The design must avoid requiring every confirmation input at the same instant before a breakout is even structurally formed.

### 2. Hard vs Soft Separation

Only the most essential structural conditions should remain hard gates.

Secondary quality signals should be grouped into a soft confirmation layer.

### 3. Interpretability First

Every failed candidate should remain explainable by stage.

The design must preserve:

- first blocker readability
- downstream blocker readability
- shadow-only validation compatibility

### 4. No Immediate Scoring-Only Architecture

A pure weighted-scoring replacement is not the first move.

That remains a later research option because:

- it changes too many validation assumptions at once
- it weakens immediate explainability
- it complicates failure attribution during early redesign validation

## Proposed Evaluation Flow

## Stage 0 - Market Regime Filter

Purpose:

- reject obviously hostile market states
- preserve only strong high-level exclusion rules

Expected checks:

- `market_not_trend_up` or equivalent regime rejection
- `range_without_upward_bias` or equivalent bias rejection

Rule:

- this stage should answer only:
  - is this market structurally eligible for breakout observation?

It should not contain too many micro-quality filters.

## Stage 1 - Setup Formation

Purpose:

- decide whether breakout setup conditions are forming

Candidate checks:

- minimum volatility floor
- minimum band width
- acceptable price location
- acceptable directional bias continuation

Output:

- `setup_ready = true/false`

Important:

- no entry permission at this stage
- no trigger confirmation at this stage

## Stage 2 - Trigger Confirmation

Purpose:

- confirm that a breakout trigger actually occurred

Candidate checks:

- breakout confirmed above recent trigger level
- structure still valid at trigger time

Important:

- this stage must remain separate from downstream quality checks
- `breakout_confirmed` is a hard requirement

## Stage 3 - Entry Quality Confirmation

Purpose:

- evaluate whether the triggered breakout is good enough for candidate entry consideration

Candidate checks:

- `volume_pass`
- `vwap_distance_pass`
- `rsi_threshold_pass`
- `ema_pass`
- `band_expansion_pass`
- `band_width_pass`

Important:

- these are checked after trigger confirmation
- this stage should not be implemented as a strict all-pass chain

## Stage 4 - Execution Decision

Purpose:

- determine whether a breakout candidate should advance toward entry consideration

At design stage, this remains a shadow-only decision.

## Proposed Gating Model

### Hard Gates

The following remain mandatory:

- `market_bias_pass == true`
- `breakout_confirmed == true`

### Soft Confirmation Pool

The following become a pooled quality layer:

- `band_width_pass`
- `band_expansion_pass`
- `volume_pass`
- `vwap_distance_pass`
- `rsi_threshold_pass`
- `ema_pass`

### Initial Draft Rule

Entry candidate allowed only if:

- all hard gates pass
- soft confirmation pass count >= `3 of 6`

This is a design draft, not an approved runtime rule.

## Why 3 of 6 Is the Initial Draft

Reasoning:

- `breakout_v2` produced zero allowed candidates
- a very conservative threshold risks reproducing the same failure
- an overly loose threshold risks degrading quality too quickly

So `3 of 6` is a draft validation starting point, not a final production threshold.

## Why This Direction Was Chosen

### Chosen

- `Sequential Confirmation`
- `Partial Gate Reduction`

### Deferred

- `Weighted Scoring` as primary architecture

Reason:

- current CNT already has live runtime and validation structure
- the redesign should remain explainable and minimally disruptive during first validation

## Explicit Prohibitions

The following are explicitly prohibited at this stage:

- direct activation of `breakout_v3`
- direct production switch from `breakout_v1` or `breakout_v2`
- tuning `breakout_v2` in place
- single-gate shortcut relaxation
- volatility-only relaxation
- band-width-only relaxation
- scoring-only rewrite without staged validation

## Shadow-Only Validation Plan

When implementation begins, `breakout_v3` must start as:

- `shadow_only = true`
- `activation = prohibited`

Initial validation should record:

- stage-by-stage pass/fail traces
- hard-gate pass rate
- soft-pass-count distribution
- allowed candidate count
- downstream blocker distribution

Promotion toward any active runtime consideration remains blocked until:

- shadow evidence shows real candidate generation
- shadow evidence shows explainable blocker structure
- no clear structural regression appears relative to current live system safety

## Working Design Statement

The current working statement for `breakout_v3` is:

> `breakout_v3` should replace simultaneous all-gates-pass logic with a sequential, interpretable structure where market regime and breakout confirmation stay hard, and secondary quality checks become a soft confirmation pool.

## Final Draft Decision

At this stage, the design direction is fixed as:

- primary direction = `Sequential Confirmation + Partial Gate Reduction`
- secondary future research = `Weighted Scoring`

Implementation is not started yet.

## Obsidian Links

- [[00 Docs Index]]

