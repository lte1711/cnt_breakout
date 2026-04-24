---
aliases:
  - CNT v2 PERFORMANCE VALIDATION CHECKLIST
---

# CNT v2 PERFORMANCE VALIDATION CHECKLIST

문서 목적:
Testnet 운영 데이터를 기반으로

* 전략 성능을 수치로 검증하고
* ranker/리스크 파라미터를 조정하며
* 실전 전환 가능 여부를 판단한다.

문서 상태:
Execution Phase / Mandatory Validation

---

# 1. 운영 단계 정의

## Phase 1 — Data Collection

* 목표: 데이터 확보
* 판단 금지
* 파라미터 변경 금지

## Phase 2 — Analysis

* 목표: 숫자 기반 분석
* 전략별 성능 비교

## Phase 3 — Tuning

* 목표: 제한적 파라미터 수정
* 변경 전/후 비교

---

# 2. 최소 데이터 기준

아래 중 하나 충족 전까지 **절대 결론 금지**

* ✔ closed trades ≥ 20
  또는
* ✔ 운영 기간 ≥ 3일

---

# 3. 필수 수집 항목

## 3.1 전체 성능

* total_signals
* selected_signals
* executed_trades
* closed_trades

---

## 3.2 손익 관련

* total_profit
* total_loss
* net_pnl
* avg_win
* avg_loss
* win_rate

---

## 3.3 리스크 관련

* max_consecutive_losses
* daily_loss_count_peak
* cooldown_trigger_count
* daily_loss_limit_trigger_count

---

## 3.4 정책 차단 분포

로그 기준 집계:

* `no_ranked_signal`
* `stale_signal`
* `LOSS_COOLDOWN`
* `DAILY_LOSS_LIMIT`
* `MAX_PORTFOLIO_EXPOSURE`
* `ONE_PER_SYMBOL_POLICY`

---

## 3.5 전략별 성능 (핵심)

각 strategy마다:

* trades_closed
* wins
* losses
* win_rate
* expectancy
* profit_factor

---

# 4. 분석 체크리스트

## 4.1 기본 성능

* win_rate ≥ 40% ?
* expectancy > 0 ?
* net_pnl > 0 ?

---

## 4.2 전략 비교

* 어떤 전략이 가장 많은 trade 생성?
* 어떤 전략이 가장 높은 expectancy?
* 어떤 전략이 손실 집중 발생?

👉 결과:

* 유지 / 개선 / 제거 후보 분류

---

## 4.3 ranker 검증

로그 확인:

* `rank_score`
* `rank_score_components`

확인 항목:

* expectancy 반영되는가?
* fallback → dynamic 전환 정상인가?
* 낮은 성과 전략이 밀리는가?

---

## 4.4 리스크 정책 검증

확인:

* cooldown 실제로 트리거되는가?
* daily_loss_limit 실제 작동하는가?
* exposure 차단 정상인가?

👉 하나라도 “안 걸리는” 정책이 있으면 문제

---

# 5. 튜닝 규칙

## 절대 규칙

* 한 번에 하나만 변경
* 변경 전/후 기록 필수
* 최소 10 trades 후 평가

---

## 5.1 전략 파라미터

조정 대상:

* target_pct
* stop_loss_pct
* signal_age_limit_sec

### 판단 기준

| 상황                | 조치          |
| ----------------- | ----------- |
| win_rate 높고 수익 낮음 | target ↑    |
| win_rate 낮고 손실 큼  | stop ↓      |
| 신호 늦음             | age_limit ↓ |

---

## 5.2 리스크 파라미터

조정 대상:

* MAX_PORTFOLIO_EXPOSURE
* LOSS_COOLDOWN
* DAILY_LOSS_LIMIT

### 판단 기준

| 상황          | 조치         |
| ----------- | ---------- |
| 연속 손실 많음    | cooldown ↑ |
| 기회 너무 많이 놓침 | cooldown ↓ |
| 과도한 노출      | exposure ↓ |

---

## 5.3 ranker 튜닝

조정 대상:

* expectancy weight
* confidence multiplier

### 판단 기준

| 상황          | 조치                  |
| ----------- | ------------------- |
| 랜덤 선택 느낌    | expectancy weight ↑ |
| 데이터 부족 영향 큼 | confidence ↓        |

---

# 6. 로그 검증 필수 항목

`portfolio.log`에서 반드시 확인:

* selected_strategy
* rank_score
* rank_score_components
* requested_notional
* blocked_by_policy
* close_pnl_estimate
* strategy_expectancy_snapshot

---

# 7. 실패 패턴 감지

## 위험 신호

* expectancy < 0 지속
* 동일 전략에서 연속 손실 집중
* ranker가 계속 같은 전략만 선택
* 정책 차단이 거의 없음 (리스크 무력화)

---

# 8. 성공 기준

다음 4개 만족 시 “통과”:

1. expectancy > 0
2. net_pnl > 0
3. risk 정책 정상 작동
4. 전략 간 성능 차이 명확

---

# 9. 산출물

다음 문서 반드시 작성:

## 1) TESTNET PERFORMANCE REPORT

* 실제 숫자 기록

## 2) PERFORMANCE TUNING LOG

* 변경 이력

## 3) 전략 평가 요약

```text
pullback_v1        → 유지 / 개선 / 제거
mean_reversion_v1  → 유지 / 개선 / 제거
breakout_v1        → 유지 / 개선 / 제거
```

---

# 10. 최종 판정 단계

## 조건 충족 시

```text
STATUS = PERFORMANCE_VALIDATED
NEXT   = CAPITAL_ALLOCATION / LIVE_PREP
```

---

# 11. 핵심 결론

지금부터 중요한 건 하나다:

> ❗ “코드가 맞다”가 아니라
> ❗ **“숫자가 맞다”를 증명해야 한다**

---

---

## Obsidian Links

- [[CNT v2 VALIDATION REPORT]]

