# Breakout Strategy Comparison Report

**Date:** 2026-04-29
**Strategies:** breakout_v1, breakout_v2, breakout_v3
**Symbol:** BNBUSDT

## Executive Summary

This report provides a comprehensive comparison of the three breakout strategy versions (v1, v2, v3) to understand their evolution, differences, and appropriate use cases.

## Strategy Evolution Overview

| Version | Release Focus | Key Innovations | Complexity |
|---------|--------------|-----------------|------------|
| v1 | Basic breakout | EMA + RSI + ATR, relaxed volatility handling | Low |
| v2 | Enhanced filtering | Bollinger Bands + VWAP + Volume | Medium |
| v3 | Quality gate | Soft pass system, adaptive quality gate | High |

## Detailed Comparison

### 1. breakout_v1 - Basic Breakout

**Core Indicators:**
- EMA Fast (9) / EMA Slow (20)
- RSI (14)
- ATR (14)

**Entry Conditions:**
1. **Market Regime:** TREND_UP or RANGE with UP bias
2. **EMA Alignment:** EMA Fast > EMA Slow
3. **RSI Range:** 52 ≤ RSI < 75
4. **Breakout Confirmation:** Price > max(highs of last 3 candles)
5. **Volatility Floor:** HIGH (with relaxed handling)

**Special Features:**
- **Relaxed Volatility Handling:** In TREND_UP with LOW volatility, allows entry if RSI ≥ 54 (threshold + buffer)
- **Confidence Levels:**
  - High volatility: 0.82
  - Relaxed volatility: 0.68

**Advantages:**
- Simple and fast execution
- Handles low volatility gracefully in trends
- Clear confidence differentiation

**Disadvantages:**
- No volume confirmation
- No price position validation (VWAP)
- No band expansion check
- May generate false breakouts in choppy markets

---

### 2. breakout_v2 - Enhanced Filtering

**Core Indicators:**
- EMA Fast (9) / EMA Slow (20)
- RSI (14)
- ATR (14)
- Bollinger Bands (20, 2.0)
- VWAP (20)
- Volume (20 SMA)

**Entry Conditions:**
1. **Market Regime:** TREND_UP or RANGE with UP bias
2. **EMA Alignment:** EMA Fast > EMA Slow
3. **RSI Range:** 52 ≤ RSI < 75
4. **Breakout Confirmation:** Price > max(highs of last 3 candles)
5. **Volatility Floor:** HIGH (strict - no relaxed handling)
6. **VWAP Position:** Price > VWAP
7. **VWAP Distance:** (Price - VWAP) / Price ≥ 0.15%
8. **Band Width:** (Upper - Lower) / Price ≥ 0.6%
9. **Band Expansion:** Current width ≥ Previous width × 1.03
10. **Volume Confirmation:** Current volume ≥ Average volume × 1.5

**Special Features:**
- **Strict Volatility:** No relaxed handling - requires HIGH volatility
- **Multi-layer Filtering:** 6 additional filters beyond v1
- **Confidence:** Fixed at 0.78

**Advantages:**
- Comprehensive filtering reduces false breakouts
- Volume confirmation ensures liquidity
- Band expansion confirms momentum
- VWAP confirms price position

**Disadvantages:**
- Very restrictive (low signal rate)
- No relaxed volatility handling
- May miss valid opportunities in low volatility trends
- Fixed confidence doesn't adapt to signal quality

---

### 3. breakout_v3 - Quality Gate

**Core Indicators:**
- EMA Fast (9) / EMA Slow (20)
- RSI (14)
- ATR (14)
- Bollinger Bands (20, 2.0)
- VWAP (20)
- Volume (20 SMA)

**Entry Conditions:**
1. **Market Regime:** TREND_UP or RANGE with UP bias
2. **EMA Alignment:** EMA Fast > EMA Slow
3. **RSI Range:** 52 ≤ RSI < 75
4. **Breakout Confirmation:** Price > max(highs of last 3 candles)
5. **Volatility Floor:** HIGH (strict - no relaxed handling)
6. **Quality Gate:** At least 2 of 6 soft conditions must pass

**Soft Conditions (Quality Gate):**
1. **Band Width:** (Upper - Lower) / Price ≥ 0.4%
2. **Band Expansion:** Current width ≥ Previous width × 1.03
3. **Volume Confirmation:** Current volume ≥ Average volume × 1.2
4. **VWAP Distance:** (Price - VWAP) / Price ≥ 0.08%
5. **RSI Threshold:** 52 ≤ RSI < 75
6. **EMA Alignment:** EMA Fast > EMA Slow

**Special Features:**
- **Adaptive Quality Gate:** Soft pass system allows flexibility
- **Optimized Parameters:** Less restrictive than v2
- **Confidence:** Fixed at 0.78
- **Conditional Trigger Price:** Optional buffer for breakout confirmation

**Advantages:**
- Balanced between strictness and opportunity
- Adaptive quality gate allows variable signal quality
- Optimized parameters for current market conditions
- Maintains v2's comprehensive indicators

**Disadvantages:**
- Still requires HIGH volatility (no relaxed handling)
- Quality gate adds complexity
- May need parameter tuning for different market regimes

---

## Parameter Comparison

| Parameter | v1 | v2 | v3 |
|-----------|----|----|----|
| ema_fast_period | 9 | 9 | 9 |
| ema_slow_period | 20 | 20 | 20 |
| rsi_period | 14 | 14 | 14 |
| atr_period | 14 | 14 | 14 |
| rsi_threshold | 52 | 52 | 52 |
| rsi_overheat | 75 | 75 | 75 |
| breakout_lookback | 3 | 3 | 3 |
| target_pct | 0.002 | 0.002 | 0.002 |
| stop_loss_pct | 0.0015 | 0.0015 | 0.0015 |
| min_band_width_ratio | N/A | 0.006 | 0.004 |
| min_band_expansion_ratio | N/A | 1.03 | 1.03 |
| min_vwap_distance_ratio | N/A | 0.0015 | 0.0008 |
| min_volume_multiplier | N/A | 1.5 | 1.2 |
| min_soft_pass_required | N/A | N/A | 2 |

**Key Parameter Changes in v3:**
- min_band_width_ratio: 0.006 → 0.004 (33% reduction)
- min_vwap_distance_ratio: 0.0015 → 0.0008 (47% reduction)
- min_volume_multiplier: 1.5 → 1.2 (20% reduction)
- Added min_soft_pass_required: 2 (quality gate)

---

## Filter Comparison

| Filter | v1 | v2 | v3 |
|--------|----|----|----|
| Market Regime (TREND_UP/RANGE+UP) | ✅ | ✅ | ✅ |
| EMA Alignment | ✅ | ✅ | ✅ (soft) |
| RSI Range | ✅ | ✅ | ✅ (soft) |
| Breakout Confirmation | ✅ | ✅ | ✅ |
| Volatility Floor (HIGH) | ✅ (relaxed) | ✅ (strict) | ✅ (strict) |
| VWAP Position | ❌ | ✅ | ✅ (soft) |
| VWAP Distance | ❌ | ✅ | ✅ (soft) |
| Band Width | ❌ | ✅ | ✅ (soft) |
| Band Expansion | ❌ | ✅ | ✅ (soft) |
| Volume Confirmation | ❌ | ✅ | ✅ (soft) |
| Quality Gate | ❌ | ❌ | ✅ |

---

## Performance Characteristics

### Signal Generation Rate (Estimated)

| Strategy | Expected Signal Rate | Market Conditions |
|----------|---------------------|-------------------|
| v1 | Medium-High | All conditions (including low volatility trends) |
| v2 | Very Low | Only HIGH volatility with all filters passing |
| v3 | Low-Medium | HIGH volatility with quality gate passing |

### Risk Profile

| Strategy | False Positive Risk | False Negative Risk |
|----------|-------------------|-------------------|
| v1 | High (minimal filtering) | Low (relaxed volatility) |
| v2 | Very Low (extensive filtering) | High (very restrictive) |
| v3 | Low-Medium (balanced filtering) | Medium (quality gate) |

### Adaptability

| Strategy | Volatility Adaptability | Market Regime Adaptability |
|----------|------------------------|---------------------------|
| v1 | High (relaxed handling) | Medium |
| v2 | Low (strict only) | Medium |
| v3 | Low (strict only) | Medium-High (quality gate) |

---

## Use Case Recommendations

### breakout_v1 - Best For:
- **Trending markets** with varying volatility
- **Higher signal frequency** desired
- **Simple execution** with proven logic
- **Markets with consistent trends** but variable volatility

### breakout_v2 - Best For:
- **High volatility markets** with clear momentum
- **Low false positive tolerance**
- **Liquidity-sensitive trading** (volume confirmation)
- **Choppy market avoidance**

### breakout_v3 - Best For:
- **Balanced approach** between signal quality and frequency
- **Current BNBUSDT market conditions** (optimized parameters)
- **Adaptive quality control** without excessive restriction
- **Production deployment** with comprehensive monitoring

---

## Current Deployment Status

| Strategy | Status | Active | Notes |
|----------|--------|--------|-------|
| breakout_v1 | Available | ❌ | Legacy, replaced by v3 |
| breakout_v2 | Available | ❌ | Too restrictive for current conditions |
| breakout_v3 | Active | ✅ | Optimized for BNBUSDT, quality gate enabled |

---

## Recommendations

### Immediate Actions
1. ✅ **Continue with breakout_v3** as active strategy
2. **Monitor signal quality** with new parameters
3. **Track quality gate pass rate** to validate effectiveness

### Future Considerations
1. **Hybrid Approach:** Consider adding relaxed volatility handling to v3
2. **Dynamic Parameters:** Implement adaptive parameter tuning based on market regime
3. **Multi-Strategy:** Deploy v1 alongside v3 for different market conditions
4. **Backtesting:** Comprehensive backtest all three strategies on historical data

### Parameter Tuning Opportunities
- **v3 Volatility:** Consider adding relaxed volatility handling from v1
- **v3 Quality Gate:** Dynamically adjust min_soft_pass_required based on market volatility
- **v3 Soft Conditions:** Weight soft conditions by importance

---

## Conclusion

**breakout_v3 represents the optimal balance** between signal quality and frequency for current BNBUSDT market conditions:

- **v1** is too permissive with minimal filtering
- **v2** is too restrictive with extensive hard filters
- **v3** provides adaptive quality control with optimized parameters

The quality gate system in v3 allows for flexibility while maintaining signal quality, making it the best choice for current deployment. However, future iterations should consider adding relaxed volatility handling from v1 to improve performance in low volatility trend scenarios.

**Recommendation:** Continue with breakout_v3 as the primary strategy, monitor performance, and iterate based on live data.
