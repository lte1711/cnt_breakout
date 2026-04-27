---
tags:
  - cnt
  - full-filter-rerun
  - evaluation
  - statistical-power
  - hold-decision
created: 2026-04-27
---

# CNT Full Filter Rerun Evaluation Report 20260427

## Executive Summary

```text
OVERALL_ALIGNMENT = PARTIAL_MATCH
FINAL_DECISION = HOLD (승격 보류)
FILTER_STATUS = PROMISING_BUT_UNPROVEN
STATISTICAL_POWER = INSUFFICIENT
```

---

## Comparative Analysis

### 1. Offline vs Online Results

| Metric | Offline Baseline | Online Rerun | Status |
|--------|------------------|--------------|---------|
| Trades (baseline) | 42 | 9 | - |
| Trades (filtered) | 29 (retained) | 9 | X Sample Collapse |
| Expectancy | -0.000578 → +0.004825 | +0.000451 | OK Directional Match |
| Profit Factor | 0.931 → 1.967 | 1.078 | OK Improvement |
| Win Rate | 50% → 58.6% | 66.7% | OK Improvement |

### 2. Directional Alignment Verification

#### Confirmed Alignments
1. **Expectancy Improvement**: Negative → Positive (Confirmed)
2. **Profit Factor**: Below 1.0 → Above 1.0 (Confirmed)
3. **Win Rate**: Improvement maintained (Confirmed)

#### Critical Misalignments
1. **Sample Size**: 29 → 9 (67% reduction) (Issue)
2. **Statistical Power**: Insufficient for validation (Issue)
3. **Context Stability**: Regime dependency detected (Issue)

---

## 🔍 Statistical Power Analysis

### Current Sample Size Issues

```text
Current trades = 9
CNT Minimum Standard = 50
Statistical Power = INSUFFICIENT
```

### Evidence from Project Standards

From `CNT_PRECISION_ANALYSIS_REPORT_20260426.md`:
> "The aggregate strategy set remains below live readiness because total sample size is still `42 < 50`"

From `CNT_LIVE_GATE_THRESHOLD_50_UPDATE_20260426.md`:
> "The live gate target count has been corrected from `20` to `50` across the official evaluator"

### Statistical Implications

| Sample Size | Statistical Confidence | Decision Reliability |
|-------------|----------------------|---------------------|
| < 20 | Very Low | Unreliable |
| 20-29 | Low | Questionable |
| 30-49 | Medium | Cautious |
| >= 50 | High | Reliable |

**Current Status**: 9 trades = Very Low Confidence

---

## Context Split Analysis

### Performance by Market Context

| Context | Trades | Win Rate | Expectancy | Assessment |
|---------|--------|----------|------------|------------|
| PRIMARY_DOWN_ENTRY_UP | 3 | 100% | +0.009328 | Excellent |
| PRIMARY_DOWN_ENTRY_DOWN | 1 | 100% | +0.009306 | Excellent |
| PRIMARY_UP_ENTRY_DOWN | 2 | 50% | -0.001254 | Poor |
| PRIMARY_UP_ENTRY_UP | 3 | 33% | -0.010241 | Very Poor |

### Key Findings

1. **Strong Downward Market Performance**: 100% win rate in down contexts
2. **Weak Upward Market Performance**: 33% win rate in up contexts
3. **Regime Dependency**: Filter effectiveness varies by market direction
4. **Sample Distribution**: Insufficient samples per context for validation

---

## Decision Framework Application

### CNT Official Gate Requirements

From project documentation:
```text
Minimum closed trades = 50
Positive expectancy required
Positive profit factor required
Max consecutive losses limited
```

### Current Status vs Requirements

| Requirement | Current Status | Meets Standard |
|-------------|----------------|----------------|
| Min Trades (50) | 9 | No |
| Positive Expectancy | +0.000451 | Yes |
| Positive Profit Factor | 1.078 | Yes |
| Statistical Confidence | Very Low | No |

---

## Risk Assessment

### Implementation Risks

1. **Sample Size Risk**: 82% reduction in sample size
2. **Regime Dependency**: Poor performance in upward markets
3. **Statistical Uncertainty**: High variance with small samples
4. **Operational Risk**: Premature deployment without validation

### Mitigation Requirements

1. **Increase Sample Size**: Minimum 20-30 trades for basic validation
2. **Context Balancing**: Ensure sufficient samples across all contexts
3. **Stability Testing**: Multiple reruns to verify consistency
4. **Gradual Deployment**: Phased implementation with monitoring

---

## Next Phase Requirements

### Critical Actions Required

```text
1. Trade Accumulation: Collect minimum 20-30 additional trades
2. Stability Verification: Run identical rerun with new data
3. Context Analysis: Ensure balanced distribution across market contexts
4. Consistency Testing: Verify results repeat with larger samples
```

### Prohibited Actions

```text
- config.py modification
- filter promotion to production
- strategy parameter changes
- live deployment without validation
```

### Timeline Projections

| Phase | Target Trades | Estimated Timeline | Confidence |
|-------|---------------|-------------------|------------|
| Current | 9 | Now | Low |
| Minimum Viable | 20 | 1-2 weeks | Medium |
| Statistical Valid | 30 | 2-3 weeks | Medium |
| CNT Standard | 50 | 4-6 weeks | High |

---

## Final Verdict

### Decision Matrix

| Factor | Weight | Score | Weighted Score |
|--------|--------|-------|----------------|
| Directional Alignment | 30% | 85% | 25.5% |
| Performance Improvement | 25% | 80% | 20.0% |
| Statistical Power | 25% | 20% | 5.0% |
| Stability | 20% | 30% | 6.0% |
| **Total** | **100%** | **56.5%** | **HOLD** |

### Executive Recommendation

```text
FILTER_STATUS = PROMISING_BUT_UNPROVEN
ACTION = HOLD AND ACCUMULATE_DATA
NEXT_EVALUATION = AFTER 20+ TRADES
DEPLOYMENT_READINESS = NOT READY
```

---

## Monitoring Plan

### Weekly Checkpoints
1. **Trade Count**: Monitor accumulation rate
2. **Context Distribution**: Track market context balance
3. **Performance Metrics**: Maintain expectancy and PF tracking
4. **Risk Metrics**: Ensure no degradation in risk controls

### Monthly Reviews
1. **Statistical Power Assessment**: Re-evaluate confidence levels
2. **Stability Analysis**: Check for performance consistency
3. **Readiness Evaluation**: Assess against CNT standards
4. **Deployment Planning**: Prepare for potential promotion

---

## Conclusion

**The Full Filter Rerun shows promising directional improvements but suffers from critical statistical power limitations.**

### Key Takeaways
1. **Positive Signals**: Expectancy and PF improvements align with offline predictions
2. **Critical Flaw**: Sample size collapse from 29 to 9 trades
3. **Regime Risk**: Strong performance only in downward markets
4. **Statistical Reality**: Current sample size insufficient for reliable decisions

### Strategic Position
```
Current State: Good signals, insufficient proof
Next Action: Accumulate data, maintain monitoring
Timeline: 4-6 weeks to CNT standard validation
Risk Level: High for immediate deployment
```

**Recommendation: Hold position, accumulate additional trades, and re-evaluate when statistical power reaches acceptable levels.**

---

*This evaluation follows CNT project standards and maintains alignment with documented gate requirements and statistical validation protocols.*
