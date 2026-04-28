# Breakout V3 Shadow Analysis Report

**Date:** 2026-04-29
**Strategy:** breakout_v3
**Symbol:** ETHUSDT → BNBUSDT (transitioning)

## Executive Summary

- **Total Signals:** 353
- **Allowed Signals:** 15 (4.25%)
- **Main Blocker:** market_not_trend_up (55.5%)
- **Secondary Blocker:** vwap_distance_fail (92.9%)

## Primary Blocker Distribution

| Blocker | Count | Percentage |
|---------|-------|------------|
| market_not_trend_up | 196 | 55.5% |
| setup_not_ready | 113 | 32.0% |
| breakout_not_confirmed | 27 | 7.6% |
| band_width_fail | 2 | 0.6% |

## Secondary Blocker Distribution

| Blocker | Count | Percentage |
|---------|-------|------------|
| vwap_distance_fail | 328 | 92.9% |
| band_width_fail | 310 | 87.8% |
| volume_fail | 284 | 80.5% |
| band_expansion_fail | 256 | 72.5% |
| rsi_threshold_fail | 210 | 59.5% |
| ema_fail | 175 | 49.6% |

## Stage Performance

| Stage | Pass Count | Fail Count | Pass Rate |
|-------|------------|------------|-----------|
| regime | 157 | 196 | 44.5% |
| trigger | 83 | 270 | 23.5% |
| quality | 86 | 267 | 24.4% |
| setup | 32 | 321 | 9.1% |

## Soft Pass Distribution

| Pass Count | Frequency |
|------------|-----------|
| 0 | 92 |
| 1 | 86 |
| 2 | 89 |
| 3 | 58 |
| 4 | 23 |
| 5 | 5 |

## Key Findings

1. **Market Regime Issue:** 55.5% of signals blocked by market_not_trend_up, indicating the strategy is too restrictive on market conditions
2. **VWAP Distance Too Strict:** 92.9% fail vwap_distance check, suggesting min_vwap_distance_ratio is too high
3. **Band Width Too Strict:** 87.8% fail band width check, indicating min_band_width_ratio needs adjustment
4. **Volume Requirements High:** 80.5% fail volume check, min_volume_multiplier may be too aggressive
5. **Low Quality Gate Pass:** Only 24.4% pass quality gate with min_soft_pass_required=3

## Recommendations

### Immediate Actions

1. **Reduce min_vwap_distance_ratio:** Current 0.0015 → 0.0008 (more lenient)
2. **Reduce min_band_width_ratio:** Current 0.006 → 0.004 (allow narrower bands)
3. **Reduce min_volume_multiplier:** Current 1.5 → 1.2 (lower volume threshold)
4. **Adjust min_soft_pass_required:** Current 3 → 2 (increase signal allowance)
5. **Consider Range Bias:** Allow range_bias_pass to count toward market_bias_pass

### Parameter Optimization Priority

1. **High Priority:** vwap_distance_ratio, band_width_ratio
2. **Medium Priority:** volume_multiplier, soft_pass_required
3. **Low Priority:** rsi_threshold, ema parameters

## Next Steps

1. Implement parameter adjustments
2. Run shadow evaluation with new parameters
3. Compare performance metrics
4. Iterate based on results
