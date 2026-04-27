---
tags:
  - cnt
  - type/documentation
  - status/active
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - status/completed
---

# CNT v2 Dashboard Setup Bottleneck Isolation Upgrade Report

## Objective

Expose the `breakout_v3` setup bottleneck directly on the operations dashboard so the current shadow phase is read as setup isolation, not generic improvement.

## Dashboard Change

Added a dedicated `V3 Setup Bottleneck` card to:
- show setup pass scarcity
- show allowed trace count
- show setup-pass-but-blocked trace count
- surface the dominant setup-side failure from the current shadow snapshot

## Intended Reading

- official gate remains authoritative
- auxiliary recovery remains explanatory
- setup bottleneck card explains why `breakout_v3` is still shadow-only

## Obsidian Links

- [[CNT DATA DASHBOARD]]
