---
---

# CNT v2 BREAKOUT V2 DESIGN

## Purpose

`breakout_v2` is introduced as a separate strategy design so the current `breakout_v1` isolation baseline remains intact.

The goal is not to mutate `breakout_v1` during the current observation window.
The goal is to prepare a stricter breakout candidate for the next validation stage.

## Why `breakout_v1` Stays Unchanged

`breakout_v1` is the current isolation observation target.

If `breakout_v1` is changed now:

- the isolation baseline is broken
- the current observed degradation record becomes harder to interpret
- `breakout_v1 observed` and `breakout_v2 candidate` can no longer be compared cleanly

Therefore:

- keep `breakout_v1` unchanged
- add `breakout_v2` separately

## Core Difference Between `breakout_v1` and `breakout_v2`

### `breakout_v1`

Current breakout logic is primarily built around:

- market classification
- EMA alignment
- RSI threshold
- ATR/high-volatility confirmation
- recent-high breakout

This structure can detect a breakout, but it does not fully judge breakout quality.

### `breakout_v2`

`breakout_v2` keeps the breakout structure but adds quality filters before entry:

- VWAP direction filter
- VWAP distance filter
- Bollinger band width filter
- Bollinger band expansion filter
- volume confirmation filter

## New Filter List

### 1. VWAP Direction

Long breakout requires:

- `price > vwap`

Filtered reason:

- `price_not_above_vwap`

### 2. VWAP Distance

Breakout must be meaningfully above VWAP:

- `vwap_distance_ratio >= min_vwap_distance_ratio`

Filtered reason:

- `vwap_distance_too_small`

### 3. Bollinger Band Width

Breakout requires a minimum band width:

- `band_width_ratio >= min_band_width_ratio`

Filtered reason:

- `band_width_too_narrow`

### 4. Bollinger Band Expansion

Current band width must be wider than the previous width by a minimum ratio:

- `band_width_ratio >= previous_band_width_ratio * min_band_expansion_ratio`

Filtered reason:

- `band_not_expanding`

### 5. Volume Confirmation

Current volume must confirm the breakout:

- `current_volume >= average_volume * min_volume_multiplier`

Filtered reason:

- `volume_not_confirmed`

## Why VWAP, Bollinger, And Volume Are Needed

### VWAP

VWAP helps reject weak long breakouts that happen below or too close to fair intraday positioning.

### Bollinger Width / Expansion

Bollinger filters help reject narrow-band and non-expanding conditions where false breakouts are more likely.

### Volume

Volume confirmation helps reject breakouts that occur without participation.

## Registration Policy

`breakout_v2` is:

- implemented
- parameterized
- registered in the strategy registry

But `breakout_v2` is **not activated immediately**.

Reason:

- current isolation runtime must remain valid
- current `breakout_v1` record must remain comparable
- `breakout_v2` should enter through a separate validation step, not silent replacement

## Activation Rule

At this stage:

- `breakout_v2` is registered
- `ACTIVE_STRATEGIES` remains unchanged

This preserves the current runtime baseline while making the next validation stage executable.

## Related Files

- [config.py](../config.py)
- [strategy_registry.py](../src/strategy_registry.py)
- [indicators.py](../src/indicators.py)
- [breakout_v2.py](../src/strategies/breakout_v2.py)
- [test_breakout_v2_filters.py](../tests/test_breakout_v2_filters.py)

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN]]
