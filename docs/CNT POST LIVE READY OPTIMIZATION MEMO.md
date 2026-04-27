---
tags:
  - cnt
  - type/documentation
  - status/active
  - context-filter
  - type/operation
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - type/analysis
  - cnt-post-live-ready-optimization-memo
---

# CNT POST LIVE READY OPTIMIZATION MEMO

## Classification

This document is a **long-term optimization memo**, not a fact-based operating report.

It must not replace the current operational truth sources:

- `data/performance_snapshot.json`
- `data/strategy_metrics.json`
- `data/live_gate_decision.json`
- `logs/runtime.log`
- `logs/portfolio.log`
- `logs/signal.log`

## Purpose

This memo captures higher-level improvement ideas that may become relevant **after** the current `LIVE_READY` baseline is stabilized.

It is intended for backlog planning, not for immediate runtime judgment.

## Why This Is Not A Current-State Report

CNT has already moved beyond the “no real data” stage.

The current repository has:

- real snapshot data
- real strategy metrics
- real runtime logs
- real live gate decisions

So ideas such as multi-asset expansion, Kelly sizing, or advanced regime switching should be treated as future refinement topics, not as current operating conclusions.

## Long-Term Improvement Themes

### 1. Signal Quality Refinement

- Reduce noisy low-value selections
- Improve selection efficiency rather than raw signal volume
- Revisit filter layering only after current baseline remains stable

### 2. Execution Efficiency

- Track execution rate after `LIVE_READY`
- Separate policy blocks from candidate starvation
- Review execution friction only with enough post-ready evidence

### 3. Risk Adaptation

- Future guardrail tuning can be considered after stability is proven
- Any adaptive risk control should be added only after baseline operating quality is measured over time

### 4. Strategy Diversification

- `pullback_v1` is still the primary strategy
- `breakout_v1` remains a lower-sample secondary strategy
- Multi-asset or multi-strategy portfolio expansion is a later phase, not a current action item

### 5. Advanced Optimization Backlog

The following belong to a future backlog, not the current sprint:

- capital allocation models
- volatility regime switching
- AI/ML-assisted tuning
- multi-asset orchestration
- chaos or resilience simulation beyond current runtime validation

## Current Boundary

For the current CNT phase, the operational focus remains:

- `selection_rate`
- `execution_rate`
- `no_ranked_signal`
- `strategy_split`
- `LIVE_READY` persistence

This memo must stay below the fact-based runtime reports in priority.

## Recommended Use

Use this document only when:

- preparing future backlog items
- discussing post-stabilization improvements
- separating current runtime facts from future ideas

Do not use this memo as evidence for changing runtime parameters immediately.

## Obsidian Links

- [[00 Docs Index]]

