---
title: CNT v2 DASHBOARD AUXILIARY RECOVERY VIEW REPORT
status: FINAL
language: en
updated: 2026-04-24
---

# CNT v2 DASHBOARD AUXILIARY RECOVERY VIEW REPORT

## Purpose

This update adds an auxiliary recovery panel to the operations dashboard without changing the official live gate.

The goal is to make the dashboard reflect the current CNT operating reality:

- official live gate remains conservative
- `breakout_v1` historical contamination can still keep the official gate negative
- post-isolation runtime recovery still needs to be interpreted separately

## What Was Added

The dashboard now includes a dedicated `Auxiliary Recovery` card.

This card is explicitly:

- explanatory only
- non-authoritative for activation
- non-overriding relative to `data/live_gate_decision.json`

## Current Auxiliary Signals Used

The panel derives its status from existing runtime data only:

- active runtime strategy from `data/state.json`
- preserved risk counters from `data/state.json` and `data/portfolio_state.json`
- `pullback_v1` strategy edge from `data/performance_snapshot.json`
- current `breakout_v3` shadow accumulation from `data/shadow_breakout_v3_snapshot.json`

## Intended Reading

The dashboard now distinguishes between:

1. `Official Live Gate`
   - still authoritative
   - still conservative
2. `Auxiliary Recovery`
   - post-isolation interpretation only
   - used to observe whether the current runtime is stabilizing even while the official gate remains negative

## Why This Matters

Without this separation, the dashboard can wrongly imply that:

- a negative official gate means nothing is improving, or
- improvement requires changing the official gate

The new view avoids both errors.

## Explicit Non-Changes

This dashboard patch does **not**:

- modify gate logic
- modify thresholds
- override live gate status
- reactivate `breakout_v1`
- activate `breakout_v3`

## Result

The CNT dashboard now presents:

- the official gate status
- the current pullback-only runtime condition
- the current shadow observation condition
- the auxiliary post-isolation recovery interpretation

in one coherent operating view.

## Obsidian Links

- [[CNT DATA DASHBOARD]]

