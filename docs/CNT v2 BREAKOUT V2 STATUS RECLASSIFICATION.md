---
tags:
  - cnt
  - breakout
  - status
aliases:
  - CNT v2 BREAKOUT V2 STATUS RECLASSIFICATION
---

# CNT v2 BREAKOUT V2 STATUS RECLASSIFICATION

## Previous Status

- `shadow candidate`

## New Status

- `failed design`
- `inactive experimental strategy`

## Basis

The reclassification is based on:

- sufficient expanded shadow sample
- `allowed_signal_count = 0`
- no hypothetical candidate generation
- stable evidence of multi-stage blockage

## Meaning

This status does **not** mean:

- immediate code deletion
- forced removal from registry
- strategy activation

It means:

- no further shadow collection is required before judgment
- current design should not be promoted
- future work should move to redesign preparation

## Operational Rule

Until redesign is explicitly approved and implemented:

- keep `breakout_v2` off
- keep `breakout_v1` as reference only
- keep `pullback_v1` as the live positive driver
