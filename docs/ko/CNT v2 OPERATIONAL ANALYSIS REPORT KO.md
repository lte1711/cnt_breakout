---
tags:
  - cnt
  - docs
  - report
  - v2
aliases:
  - CNT v2 OPERATIONAL ANALYSIS REPORT KO
---

# CNT v2 OPERATIONAL ANALYSIS REPORT KO

테스트 버전: CNT v2.0  
분석 기준일: 2026-04-19  
환경: Binance Testnet (`ETHUSDT`, `5m / 1m`)

## 1. 시스템 상태

```text
STATUS          = ACTIVE
SCHEDULER       = RUNNING (10min interval)
DATA_COLLECTION = STARTED
LIVE_GATE       = NOT_READY
REASON          = INSUFFICIENT_SAMPLE
```

당시 기준으로 시스템은 정상 실행 중이었고, 데이터 수집 단계가 시작된 상태로 평가됐다.

## 2. 아키텍처 개요

CNT v2는 다음 4단계 파이프라인으로 해석됐다.

1. Signal Generation (`3 strategies`)
2. Signal Ranking (`signal_ranker`)
3. Risk Evaluation (`portfolio + risk_guard`)
4. Execution + Exit Management (`engine + enhanced_exit_manager`)

또한 `state.json` 기반 상태 머신으로 `pending -> open_trade -> closed` 흐름을 관리한다.

## 3. 전략 상태

### breakout_v1

- 상태: `NOT_SELECTED`
- 신호 발생은 있으나 선택은 0
- 당시 판단: 구조 오류보다는 파라미터/경쟁력 문제에 가까우며, 이후 단계에서 조정 검토 대상

### pullback_v1

- 상태: `ACTIVE`
- 거래: `2`
- 결과: `1 win / 1 loss`
- expectancy: 양수
- 당시 판단: 현재 유일한 실행 전략이지만 표본 부족으로 성능 확정은 불가

### mean_reversion_v1

- 상태: `REGISTERED_NOT_ACTIVE`
- 별도 검증 필요

## 4. 실행 흐름

`engine.run_cycle()`은 다음 순서를 따른다.

1. 상태 로드 (`state.json / portfolio_state.json`)
2. pending 처리
3. `open_trade` exit 평가
4. 신규 진입 평가

### Exit Failsafe

pending 상태에서 TARGET LIMIT 주문이 있고 동시에 STOP/TRAILING 조건이 발생하면:

1. 기존 LIMIT 주문 취소
2. 즉시 MARKET 청산 실행

## 5. 성능 상태

```text
closed_trades = 2
win           = 1
loss          = 1
expectancy    > 0
profit_factor > 1
```

당시 판단:

- 통계적으로 충분하지 않음
- 성능 확정 금지
- `SAMPLE_INSUFFICIENT`

## 6. 이슈 분류

### 실제 문제

1. `breakout_v1` 선택 수 0

### 문제 아님

1. `no_ranked_signal` 발생
2. 일부 전략 비선택
3. `expectancy_weighted` 비활성 (`sample < 5`)

## 7. 현재 단계

```text
CURRENT_PHASE = DATA_COLLECTION_RUNNING
```

즉 당시에는 구조 수정이 아니라 데이터 누적이 우선이라는 결론이었다.

## 8. 다음 단계 계획

- Phase 1: 데이터 수집 유지
- Phase 2: ranking activation
- Phase 3: strategy adjustment
- Phase 4: live gate evaluation
- Phase 5: risk expansion

## 링크

- [[CNT v2 CURRENT STATUS ASSESSMENT KO]]
- [[CNT v2 TESTNET PERFORMANCE REPORT KO]]
- [[00 Docs Index KO]]
