# Breakout V3 Normalization Summary

**Date:** 2026-04-29
**Status:** IN PROGRESS
**Objective:** Normalize breakout_v3 for live trading on BNBUSDT

## Completed Tasks

### 1. Shadow Data Analysis ✅
- Analyzed 353 shadow signals
- Identified key blockers:
  - market_not_trend_up (55.5%)
  - vwap_distance_fail (92.9%)
  - band_width_fail (87.8%)
  - volume_fail (80.5%)
- Generated analysis report: `docs/breakout_v3_shadow_analysis_report.md`

### 2. Parameter Optimization ✅
- Adjusted parameters based on shadow analysis:
  - `min_vwap_distance_ratio`: 0.0015 → 0.0008
  - `min_band_width_ratio`: 0.006 → 0.004
  - `min_volume_multiplier`: 1.5 → 1.2
  - `min_soft_pass_required`: 3 → 2
- Updated config.py with optimized parameters

### 3. Live Readiness Preparation ✅
- Created comprehensive checklist: `docs/breakout_v3_live_readiness_checklist.md`
- Verified strategy implementation
- Verified configuration
- Verified registry integration
- Identified critical path items

### 4. Monitoring Infrastructure ✅
- Created live monitoring script: `tools/monitor_breakout_v3_live.py`
- Supports real-time status checks
- Supports continuous monitoring mode
- Tracks strategy activity, positions, and signals

## Current Status

**Strategy:** breakout_v3
**Symbol:** BNBUSDT
**Active Strategy:** breakout_v3
**Configuration:** Optimized for BNBUSDT market

## Next Steps

### Immediate Actions
1. Run shadow evaluation with new parameters
2. Validate testnet connectivity
3. Run full test suite

### Pre-Live Actions
1. Complete shadow evaluation validation
2. Setup monitoring and alerting
3. Complete risk parameter validation
4. Final engineering review

### Live Transition
1. Execute on testnet for validation
2. Monitor performance for minimum sample size
3. Evaluate live gate decision
4. Transition to live if criteria met

## Key Metrics to Monitor

- Signal generation rate
- Entry allowed rate
- Quality gate pass rate
- Trade execution success rate
- Position profitability
- Risk metrics (daily loss count, consecutive losses)

## Risk Considerations

1. **Parameter Sensitivity:** New parameters need validation in live conditions
2. **Market Volatility:** BNBUSDT may have different volatility profile
3. **Execution Risk:** Testnet validation required before live
4. **Monitoring Gap:** Real-time monitoring needs to be established

## Success Criteria

- [ ] Shadow evaluation shows improved signal rate (>10%)
- [ ] Testnet execution successful
- [ ] Full test suite passes
- [ ] Monitoring system operational
- [ ] Risk parameters validated
- [ ] Live gate decision shows LIVE_READY

## Documentation

- Analysis Report: `docs/breakout_v3_shadow_analysis_report.md`
- Readiness Checklist: `docs/breakout_v3_live_readiness_checklist.md`
- Monitoring Tool: `tools/monitor_breakout_v3_live.py`
- Configuration: `config.py` (breakout_v3 section)

## Notes

- Pullback_v1 strategy completely removed from codebase
- All references updated to breakout_v3
- Symbol changed from ETHUSDT to BNBUSDT
- Git repository synchronized with changes
