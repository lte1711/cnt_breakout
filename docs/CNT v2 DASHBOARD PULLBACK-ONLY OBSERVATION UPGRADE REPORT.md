---
title: CNT v2 DASHBOARD PULLBACK-ONLY OBSERVATION UPGRADE REPORT
status: FINAL
language: en
updated: 2026-04-24
tags:
  - cnt
  - dashboard
  - observation
  - pullback_v1
  - breakout_v3
---

# CNT v2 DASHBOARD PULLBACK-ONLY OBSERVATION UPGRADE REPORT

## Purpose

This patch upgrades the operations dashboard so the current runtime mode is visible without reading raw files first.

The new dashboard state must reflect:

- `pullback_v1` as the only live active runtime strategy
- `breakout_v1` as isolated from active runtime
- `breakout_v3` as shadow-only
- current `breakout_v3` shadow observation progress

## Files Changed

- `docs/cnt_operations_dashboard.html`
- `docs/CNT v2 DASHBOARD PULLBACK-ONLY OBSERVATION UPGRADE REPORT.md`
- `docs/ko/CNT v2 DASHBOARD PULLBACK-ONLY OBSERVATION UPGRADE REPORT KO.md`

## Dashboard Changes

### 1. Runtime Mode card added

The dashboard now explicitly shows:

- current live active runtime strategy
- current runtime action
- pullback-only operation badge
- breakout_v3 shadow-only badge

### 2. Breakout V3 Shadow card added

The dashboard now reads `data/shadow_breakout_v3_snapshot.json` directly and shows:

- `signal_count`
- `allowed_signal_count`
- `soft 3+` count
- `last_updated`
- top first blockers
- top hard blockers
- soft-pass distribution
- stage-fail summary

### 3. Top warning refinement

The top warning row now also includes:

- `PULLBACK-ONLY RUNTIME ACTIVE`

This makes the current operating mode visible immediately.

### 4. Footer source expansion

The dashboard source list now includes:

- `../data/shadow_breakout_v3_snapshot.json`

## Why This Matters

Before this patch, the dashboard showed degradation well, but it did not clearly expose the current controlled runtime mode.

After this patch, an operator can immediately see:

- which strategy is actually live
- whether breakout_v3 is still only observational
- whether shadow observation is progressing toward the next review threshold

## Validation

Validation for this step focused on:

- ensuring the dashboard still loads the existing data files
- ensuring the new shadow snapshot source path is correct
- ensuring the current runtime state maps naturally into the new cards

Operational cross-check used:

- `data/state.json`
- `data/live_gate_decision.json`
- `data/performance_snapshot.json`
- `data/shadow_breakout_v3_snapshot.json`

## Current Intended Reading

At the time of this report, the dashboard should present the following interpretation:

- live runtime = `pullback_v1` only
- Live Gate = still `FAIL / NON_POSITIVE_EXPECTANCY`
- breakout_v3 = clean shadow observation in progress
- next formal review = after enough post-fix shadow samples accumulate

## Conclusion

This dashboard upgrade aligns the visual operating interface with the actual post-isolation CNT runtime state.
