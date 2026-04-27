---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - status/final
  - language:-en
---

# CNT v2 DASHBOARD ESSENTIAL VIEW REFINEMENT REPORT

## Purpose

This refinement reduces the operations dashboard to the information needed for the current operating phase only.

Current CNT phase:

- `pullback_v1` is the only live active runtime strategy
- `breakout_v3` is shadow-only
- the current task is observation, not optimization

Because of that, the dashboard should prioritize:

- live gate status
- current runtime mode
- current engine state
- current shadow observation state
- current risk sync state
- current top-level performance health

## Removed or De-emphasized Areas

The following broad or distracting areas were removed from the main screen:

- large signal pipeline block
- live-ready baseline comparison panel
- full strategy quality table
- broad blocker dump section

These sections were useful during broader diagnosis, but they are not the highest-signal view for the current pullback-only observation phase.

## Kept as Primary

The refined dashboard keeps:

- `Live Gate`
- `System Health`
- `Runtime Mode`
- `Breakout V3 Shadow`
- `Expectancy / PF / Net PnL`
- `Engine State`
- `Risk Sync`

## Expected Operator Experience

An operator should now be able to answer these questions immediately:

1. Is the system still gate-failed or recovered?
2. Is `pullback_v1` still the only live runtime strategy?
3. Is the engine blocked by risk or simply seeing no entry?
4. Is `breakout_v3` still shadow-only?
5. Is the shadow observation count increasing?
6. Are risk counters synchronized?

## Scope

This is a dashboard visibility refinement only.

It does not:

- change runtime logic
- change strategy selection logic
- change live gate logic
- change shadow evaluator logic

## Conclusion

The dashboard now reflects the current CNT operating phase more cleanly by showing only the high-signal panels needed for pullback-only live observation and breakout_v3 shadow monitoring.

## Obsidian Links

- [[CNT DATA DASHBOARD]]

