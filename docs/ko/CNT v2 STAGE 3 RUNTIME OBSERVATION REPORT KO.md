---
aliases:
  - CNT v2 STAGE 3 RUNTIME OBSERVATION REPORT KO
---

# CNT v2 Stage 3 Runtime Observation Report KO

## 요약

Stage 3의 목적은 2단계 후보 복구 조치가 **실제 운영 로그에서 살아 있는 후보 복구 효과를 내는지** 확인하는 것이다.

현재 판단:

> **Stage 3는 진행 중이다.**
> **조치 적용과 테스트 검증은 끝났지만 운영 효과는 아직 부분 확인 상태다.**

즉 현재 단계 정의는 `RUNTIME_OBSERVATION_ACTIVE`다.

## 관측 기준

이번 판단은 아래 최신 증거를 기준으로 한다.

- `data/performance_snapshot.json`
- `data/live_gate_decision.json`
- `data/strategy_metrics.json`
- `data/state.json`
- `logs/runtime.log`
- `logs/signal.log`
- `logs/portfolio.log`

## 현재 runtime state

- `pending_order = null`
- `open_trade = null`
- `action = EXECUTION_BLOCKED_BY_RISK`
- `live_gate.status = NOT_READY`
- `live_gate.reason = INSUFFICIENT_SAMPLE`

즉 시스템은 정상 동작 중이지만, 리스크 제약 때문에 진입이 막힌 상태였다.

## current performance snapshot

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

### Strategy breakdown

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

## Stage 2 patch runtime effect

### 확인된 것

- 2단계 조치는 저장소에 반영됨
- 테스트와 컴파일 검증 완료
- `near_trend_pullback_reentry`는 실제 운영 로그에서 확인됨
- ranker 재설계와 후보 복구 조치가 운영 경로에 반영되고 있음

### 아직 확인 안 된 것

- `trend_up_relaxed_volatility_breakout`
- `trend_pullback_reentry_relaxed_rsi`
- `candidate_count=0`의 의미 있는 감소
- `no_ranked_signal`의 의미 있는 감소
- breakout selection rate 개선

## 최근 관측 구간

최근 Stage 3 구간에서:

### breakout_v1

- allowed = `0`
- blocked = `3`
- top reason = `range_without_upward_bias`

### pullback_v1

- allowed = `2`
- blocked = `1`
- 확인된 reason:
  - `trend_pullback_reentry`
  - `near_trend_pullback_reentry`

즉 최근 구간만 보면 **후보 복구 효과는 pullback 쪽에서 먼저 보이고, breakout 쪽은 아직 증거가 부족**하다.

## 집계 해석

누적 기준에서 breakout의 주요 병목은 상위 market regime gate다.

- `market_not_trend_up = 119`
- `volatility_not_high = 46`
- `range_without_upward_bias = 26`
- `range_bias_up_but_entry_trend_not_up = 16`

이는 다음을 시사한다.

1. breakout은 완전히 dead branch는 아니다
2. 하지만 후보 부족의 본체는 상위 regime/filter 구조다
3. Stage 2 조치는 후보 복구 준비에는 성공했지만, breakout 측 운영 개선을 입증할 만큼의 로그는 아직 부족하다

## 운영 결론

> **Stage 3는 성공/실패 판정 단계가 아니라 운영 효과를 관측 중인 단계다.**
> **현재까지는 pullback 쪽에서만 부분적인 복구 신호가 보이고, breakout 쪽은 추가 관측이 필요하다.**

## 다음 행동

1. Stage 3 관측 지속
2. `closed_trades = 20` 도달 확인
3. breakout relaxed reason 출현 여부 관찰
4. `candidate_count`, `no_ranked_signal`, selection rate 변화 수집

지금 하지 않을 것:

- breakout 추가 완화
- ATR/RSI 추가 완화
- ranker 재수정
- pullback 규칙 수정

## 한 줄 결론

**CNT는 정상 운영 중이며 Stage 3 runtime observation 단계에 있다. 2단계 후보 복구 조치는 적용 완료됐지만, 현재까지 운영 로그에서 살아 있는 복구 효과는 pullback 쪽에서만 부분적으로 확인되고 breakout 쪽은 추가 관측이 필요하다.**

## 링크

- CNT v2 CANDIDATE RECOVERY STAGE 2 REPORT KO
- CNT v2 CURRENT STATUS ASSESSMENT KO
- CNT v2 TESTNET PERFORMANCE REPORT KO
- CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO
- 00 Docs Index KO

## Obsidian Links

- [[CNT v2 VALIDATION REPORT KO]]


