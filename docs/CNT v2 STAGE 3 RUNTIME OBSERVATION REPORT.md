---
aliases:
  - CNT v2 STAGE 3 RUNTIME OBSERVATION REPORT
---

# CNT v2 Stage 3 Runtime Observation Report

## Summary

Stage 3의 목적은 2단계 후보 회복 패치가 **실제 운영 로그에서 의미 있는 후보 회복 효과를 냈는지** 확인하는 것이다.

현재 판정은 다음과 같다.

> **Stage 3는 진행 중이다.**
> **패치 적용과 테스트 검증은 완료됐지만, 운영 효과는 아직 부분 확인 수준이다.**

즉, 지금 단계의 정확한 상태는 `RUNTIME_OBSERVATION_ACTIVE`다.

## Observation Basis

이번 판단은 아래 최신 런타임 근거를 기준으로 했다.

- `data/performance_snapshot.json`
- `data/live_gate_decision.json`
- `data/strategy_metrics.json`
- `data/state.json`
- `logs/runtime.log`
- `logs/signal.log`
- `logs/portfolio.log`

기준 시각:

- snapshot timestamp = `2026-04-21 13:54:02`
- state last_run_time = `2026-04-21 13:54:00`

## Current Runtime State

- `pending_order = null`
- `open_trade = null`
- `action = EXECUTION_BLOCKED_BY_RISK`
- `live_gate.status = NOT_READY`
- `live_gate.reason = INSUFFICIENT_SAMPLE`

즉, 시스템은 정상 동작 중이지만 현재 사이클은 리스크 정책에 의해 진입이 차단되고 있다.

## Current Performance Snapshot

- total signals = `426`
- selected signals = `25`
- executed trades = `19`
- closed trades = `19`
- wins = `11`
- losses = `8`
- win rate = `0.5789`
- expectancy = `0.0020717`
- net pnl = `0.039363`
- profit factor = `1.349458`

### Strategy Breakdown

#### pullback_v1

- `signals_generated = 213`
- `signals_selected = 23`
- `trades_closed = 17`
- `wins = 10`
- `losses = 7`
- `expectancy = 0.0021459`
- `profit_factor = 1.359079`

#### breakout_v1

- `signals_generated = 213`
- `signals_selected = 2`
- `trades_closed = 2`
- `wins = 1`
- `losses = 1`
- `expectancy = 0.001441`
- `profit_factor = 1.260956`

## Stage 2 Patch Runtime Effect

### Confirmed

- 2단계 패치 코드는 저장소에 적용돼 있다.
- 테스트와 컴파일 검증은 이미 완료됐다.
- `near_trend_pullback_reentry`는 실제 운영 로그에서 확인됐다.
- 랭커 재설계와 후보 회복 패치가 함께 런타임에 반영되고 있다.

### Not Yet Confirmed

아래는 아직 운영 로그 기준으로 충분히 확인되지 않았다.

- `trend_up_relaxed_volatility_breakout`
- `trend_pullback_reentry_relaxed_rsi`
- `candidate_count=0`의 의미 있는 감소
- `no_ranked_signal`의 유의미한 감소
- breakout selection rate의 실질 개선

## Recent Observation Window

최근 Stage 3 관측 구간에서 확인된 사실:

### breakout_v1

- allowed = `0`
- blocked = `3`
- top reason = `range_without_upward_bias`

### pullback_v1

- allowed = `2`
- blocked = `1`
- confirmed reason:
  - `trend_pullback_reentry`
  - `near_trend_pullback_reentry`

즉, 최근 구간만 보면 **후보 회복 효과는 pullback 쪽에서 부분 관측**됐고, **breakout 쪽에서는 아직 의미 있는 회복 증거가 부족**하다.

## Aggregate Bottleneck Interpretation

누적 기준으로 breakout의 주 병목은 여전히 상위 market regime gate다.

- `market_not_trend_up = 119`
- `volatility_not_high = 46`
- `range_without_upward_bias = 26`
- `range_bias_up_but_entry_trend_not_up = 16`

이 수치는 다음을 의미한다.

1. breakout은 더 이상 dead branch는 아니다.
2. 하지만 후보 부족 문제의 본체는 여전히 상위 regime/filter 구조다.
3. Stage 2 패치는 “후보 회복 준비”에는 성공했지만, breakout 운영 개선을 입증할 만큼의 로그 효과는 아직 부족하다.

## Operational Conclusion

현재 가장 정확한 결론은 아래와 같다.

> **Stage 3는 성공/실패 판정 단계가 아니라, 운영 효과를 관측 중인 단계다.**
> **현재까지는 pullback 쪽에서 부분 신호가 보이고, breakout 쪽의 의미 있는 후보 회복은 아직 입증되지 않았다.**

## Next Action

다음 우선순위:

1. Stage 3 관측 지속
2. `closed_trades = 20` 도달 확인
3. breakout의 신규 relaxed reason 출현 여부 재관측
4. `candidate_count`, `no_ranked_signal`, selection rate 변화 재집계

현재 시점에서 아직 하지 않을 것:

- breakout 추가 파라미터 완화
- ATR/RSI 추가 완화
- ranker 재수정
- pullback 튜닝

## Final One-Line Judgment

**CNT는 정상적으로 운영 중이며 Stage 3 런타임 관측 단계에 있다. 2단계 후보 회복 패치는 적용 완료됐지만, 현재까지 운영 로그상 의미 있는 회복 효과는 pullback 쪽에서만 부분적으로 보이고 breakout 쪽은 아직 추가 관측이 필요하다.**

---

## Obsidian Links

- [[CNT v2 VALIDATION REPORT]]

