# Breakout V3 Live Readiness Checklist

**Date:** 2026-04-29
**Strategy:** breakout_v3
**Target:** BNBUSDT

## Pre-Live Validation Checklist

### 1. Strategy Implementation
- [x] Strategy class implemented (BreakoutV3Strategy)
- [x] Parameter validation implemented
- [x] Signal generation logic complete
- [x] Exit model integration complete
- [x] Market context logging integrated

### 2. Configuration
- [x] Strategy parameters configured in config.py
- [x] Active strategy set to breakout_v3
- [x] Symbol updated to BNBUSDT
- [x] Target pct and stop loss pct configured
- [x] Signal age limit configured

### 3. Registry and Integration
- [x] Strategy registered in STRATEGY_REGISTRY
- [x] Import statements updated
- [x] No pullback_v1 references remaining
- [x] Test files updated to breakout_v3

### 4. Parameter Optimization
- [x] Shadow analysis completed
- [x] Parameters adjusted based on analysis:
  - min_vwap_distance_ratio: 0.0015 → 0.0008
  - min_band_width_ratio: 0.006 → 0.004
  - min_volume_multiplier: 1.5 → 1.2
  - min_soft_pass_required: 3 → 2

### 5. Shadow Evaluation
- [x] Shadow evaluation infrastructure exists
- [x] Shadow data collected (353 signals)
- [x] Shadow snapshot available
- [x] Analysis report generated
- [ ] New parameter shadow run needed

### 6. Testing
- [x] Unit tests exist (test_breakout_v3_shadow_eval.py)
- [x] Integration tests exist (test_breakout_v3_shadow_aggregator.py)
- [ ] Run full test suite
- [ ] Validate test coverage

### 7. Risk Management
- [x] Exit model configured (target_pct, stop_loss_pct)
- [x] Risk guard integration exists
- [x] Portfolio risk manager integration exists
- [ ] Validate risk parameters for BNBUSDT

### 8. Monitoring and Logging
- [x] Signal logging integrated
- [x] Portfolio logging integrated
- [x] Runtime logging integrated
- [ ] Real-time monitoring setup
- [ ] Alert thresholds configured

### 9. Exchange Integration
- [x] Binance client configured
- [x] Testnet environment set
- [x] API keys configured
- [ ] Validate testnet connectivity
- [ ] Validate order execution

### 10. Data Quality
- [x] Market context structure defined
- [x] Feature snapshot implemented
- [x] Indicator calculations validated
- [ ] Validate BNBUSDT data quality

## Critical Path Items

1. **Run shadow evaluation with new parameters** - HIGH PRIORITY
2. **Validate testnet connectivity** - HIGH PRIORITY
3. **Run full test suite** - MEDIUM PRIORITY
4. **Setup real-time monitoring** - MEDIUM PRIORITY

## Blocking Issues

None identified.

## Recommendations

1. **Immediate:** Run shadow evaluation with optimized parameters
2. **Before Live:** Complete testnet validation
3. **Before Live:** Setup monitoring and alerting
4. **Before Live:** Complete full test suite

## Sign-off

- [ ] Engineering review completed
- [ ] Risk review completed
- [ ] Operations review completed
- [ ] Final approval granted
