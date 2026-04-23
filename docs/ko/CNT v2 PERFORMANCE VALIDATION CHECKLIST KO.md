---
tags:
  - cnt
  - docs
  - performance
  - validation
  - instruction
  - v2
  - ko
aliases:
  - CNT v2 PERFORMANCE VALIDATION CHECKLIST KO
---

# CNT v2 성능 검증 체크리스트

문서 목적:

Testnet 운영 데이터를 기반으로

- 전략 성능을 수치로 검증하고
- ranker / 리스크 / 파라미터 조정 여부를 판단하며
- 실제 전환 가능 여부를 평가하기 위한 체크리스트다.

문서 상태:

- Execution Phase / Mandatory Validation

## 1. 운영 단계 정의

### Phase 1 - Data Collection

- 목표: 데이터 확보
- 판단 금지
- 파라미터 변경 금지

### Phase 2 - Analysis

- 목표: 숫자 기반 분석
- 전략별 성능 비교

### Phase 3 - Tuning

- 목표: 제한된 파라미터 수정
- 변경 전후 비교

## 2. 최소 데이터 기준

아래 중 하나를 충족하기 전까지는 **최종 결론 금지**

- closed trades `>= 20`
- 운영 기간 `>= 3일`

## 3. 필수 수집 항목

### 3.1 전체 성능

- total_signals
- selected_signals
- executed_trades
- closed_trades

### 3.2 손익 관련

- total_profit
- total_loss
- net_pnl
- avg_win
- avg_loss
- win_rate

### 3.3 리스크 관련

- max_consecutive_losses
- daily_loss_count_peak
- cooldown_trigger_count
- daily_loss_limit_trigger_count

### 3.4 정책 차단 분포

로그 기준 집계:

- `no_ranked_signal`
- `stale_signal`
- `LOSS_COOLDOWN`
- `DAILY_LOSS_LIMIT`
- `MAX_PORTFOLIO_EXPOSURE`
- `ONE_PER_SYMBOL_POLICY`

### 3.5 전략별 성능

각 strategy마다:

- trades_closed
- wins
- losses
- win_rate
- expectancy
- profit_factor

## 4. 분석 체크리스트

### 4.1 기본 성능

- win_rate `> 40%` 인가
- expectancy `> 0` 인가
- net_pnl `> 0` 인가

### 4.2 전략 비교

- 어떤 전략이 더 많은 trade를 생성하는가
- 어떤 전략이 더 높은 expectancy를 보이는가
- 어떤 전략에서 손실 집중이 발생하는가

결론 분류:

- 유지 / 개선 / 제거 후보

### 4.3 ranker 검증

로그 확인:

- `rank_score`
- `rank_score_components`

확인 항목:

- expectancy가 반영되는가
- fallback과 dynamic 전환이 정상인가
- 선택 성과와 전략 품질이 분리되는가

### 4.4 리스크 정책 검증

확인:

- cooldown이 실제로 트리거되는가
- daily_loss_limit이 실제로 작동하는가
- exposure 차단이 정상인가

## 5. 튜닝 규칙

### 기본 규칙

- 한 번에 하나만 변경
- 변경 전후 기록 필수
- 최소 10 trades 이후 평가

### 5.1 전략 파라미터

조정 대상:

- target_pct
- stop_loss_pct
- signal_age_limit_sec

### 5.2 리스크 파라미터

조정 대상:

- MAX_PORTFOLIO_EXPOSURE
- LOSS_COOLDOWN
- DAILY_LOSS_LIMIT

### 5.3 ranker 튜닝

조정 대상:

- expectancy weight
- confidence multiplier

## 6. 로그 검증 필수 항목

`portfolio.log`에서 반드시 확인:

- selected_strategy
- rank_score
- rank_score_components
- requested_notional
- blocked_by_policy
- close_pnl_estimate
- strategy_expectancy_snapshot

## 7. 실패 징후 감지

위험 신호:

- expectancy < 0 지속
- 동일 전략에서 손실 집중
- ranker가 계속 같은 전략만 선택
- 정책 차단이 거의 없음

## 8. 성공 기준

아래 4개를 모두 만족해야 통과:

1. expectancy > 0
2. net_pnl > 0
3. risk 정책 정상 작동
4. 전략 간 성능 차이 명확

## 9. 결과물

반드시 작성:

- `TESTNET PERFORMANCE REPORT`
- `PERFORMANCE TUNING LOG`
- `PERFORMANCE VALIDATION REPORT`

## 링크

- [[CNT v2 PERFORMANCE VALIDATION CHECKLIST]]
- [[CNT v2 TESTNET PERFORMANCE REPORT KO]]
- [[CNT v2 PERFORMANCE TUNING LOG KO]]
