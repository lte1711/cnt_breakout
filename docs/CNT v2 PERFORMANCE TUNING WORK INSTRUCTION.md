---
tags:
  - cnt
  - docs
  - performance
  - instruction
  - v2
aliases:
  - CNT v2 PERFORMANCE TUNING WORK INSTRUCTION
---

﻿# CNT v2 PERFORMANCE TUNING WORK INSTRUCTION

문서 목적:
CNT v2가 구조/운영 정합성 패치를 완료한 상태에서,
이제 **전략 성능, 신호 선택 품질, 리스크 파라미터 정밀도**를 높여
Spot Testnet 기준의 “운영 가능” 상태를 **실전형 성능 검증 단계**로 끌어올린다.

문서 상태:
Performance Tuning / Required Before Broader Deployment

적용 원칙:
이번 단계는 구조 수정이 아니라 **성능 측정 → 튜닝 → 검증** 중심으로 진행한다.
새 기능 추가보다 **측정 가능한 개선**을 우선한다.

---

# 1. 현재 기준선

## 현재 확정 상태

* P0 완료: 운영 차단 버그 해소
* P1 완료: exposure / 전략 활성 범위 정합화
* P2 완료: 파라미터 검증 강화
* P3 완료: 로그/관측/책임 경계 정리

## 현재 운영 기준

```text
STATUS   = PATCH_COMPLETE
BASELINE = PRODUCTION-READY (Spot Testnet)
NEXT     = PERFORMANCE TUNING
```

---

# 2. 이번 단계 목표

이번 단계 목표는 4개다.

1. **전략별 성능을 수치로 계측**
2. **signal_ranker를 단순 선택기에서 기대값 중심 선택기로 고도화**
3. **리스크 파라미터를 실제 결과 기반으로 조정**
4. **paper/testnet 운영 검증 기준을 문서화**

---

# 3. P4-1 전략 성능 계측 계층 추가

## 목적

현재는 전략이 신호를 생성하고 ranker가 선택하지만,
각 전략의 실제 성능이 **지속적으로 수치화되어 있지 않다.**

## 대상 파일

* `src/portfolio/signal_ranker.py`
* `src/portfolio/strategy_orchestrator.py`
* 신규 권장:

  * `src/analytics/strategy_metrics.py`
  * `src/models/strategy_performance.py`

## 구현 요구

### 1) 전략별 성능 지표 저장 구조 추가

최소 저장 항목:

* `strategy_name`
* `signals_generated`
* `signals_selected`
* `trades_closed`
* `wins`
* `losses`
* `gross_profit`
* `gross_loss`
* `avg_win`
* `avg_loss`
* `win_rate`
* `expectancy`
* `last_updated`

### 2) 종료 거래 기준으로 성과 반영

반영 기준:

* `SELL_FILLED`
* `STOP_MARKET_FILLED`
* `TRAILING_STOP_FILLED`

주의:

* pending 단계가 아니라 **close 확정 시점** 기준
* 전략 귀속은 entry 시점의 `strategy_name` 기준

### 3) 영속 저장

권장 파일:

* `data/strategy_metrics.json`

완료 조건:

* 전략별 누적 성과가 파일로 남아야 함
* 엔진 재시작 후에도 유지돼야 함

---

# 4. P4-2 signal_ranker 고도화

## 목적

현재 ranker는 구조상 작동하지만, 선택 기준이 충분히 정교하지 않다.
이제는 “들어오는 신호 중 하나를 고르는 것”이 아니라
**“기대 성과가 더 나은 신호를 고르는 것”**으로 바꿔야 한다.

## 대상 파일

* `src/portfolio/signal_ranker.py`

## 구현 요구

### 1) score 구성 표준화

최소 score 구성:

```text
score =
  base_signal_score
+ expectancy_weighted_score
+ trend_alignment_bonus
- volatility_penalty
- recent_loss_penalty
```

### 2) 반영 요소

최소 반영 후보:

* 전략 자체 우선순위
* signal strength
* 최근 전략 expectancy
* 최근 연속 손실 여부
* 변동성 상태
* 동일 심볼 최근 실패 이력

### 3) fallback 규칙 유지

전략 성과 데이터가 충분하지 않을 때:

* 기존 deterministic ranking 유지
* 데이터 부족으로 ranker가 불안정해지지 않게 한다

권장 규칙:

```text
if trades_closed < minimum_sample:
    use static base score
else:
    include expectancy adjustment
```

완료 조건:

* 성과 데이터가 없는 초기 상태에서도 동작
* 데이터가 쌓이면 동적으로 순위가 달라짐

---

# 5. P4-3 성능 지표 계산 규칙 표준화

## 목적

“잘 되는 전략”을 감각으로 판단하지 않고 숫자로 판단한다.

## 대상

* 신규 analytics/helper 모듈 권장

## 필수 계산식

### 1) Win Rate

```text
wins / trades_closed
```

### 2) Avg Win / Avg Loss

```text
avg_win  = gross_profit / wins
avg_loss = gross_loss / losses
```

### 3) Expectancy

```text
expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
```

### 4) Profit Factor

```text
gross_profit / gross_loss
```

### 5) Strategy Confidence

샘플 수 기반 보정 필요:

* 표본 적으면 confidence 낮게
* 표본 충분하면 ranker 반영 강하게

권장:

```text
confidence_multiplier = min(1.0, trades_closed / N)
```

완료 조건:

* 각 계산식이 코드/문서에 명시
* 0 나누기 방어 포함

---

# 6. P4-4 리스크 파라미터 실측 튜닝

## 목적

현재 리스크 파라미터는 구조적으로 작동하지만,
최적값인지 검증되지 않았다.

## 대상 파일

* `config.py`
* 관련 risk/decision 모듈
* 문서

## 튜닝 대상

최소 대상 항목:

* `MAX_PORTFOLIO_EXPOSURE`
* `ONE_PER_SYMBOL_POLICY`
* `DAILY_LOSS_LIMIT`
* `LOSS_COOLDOWN`
* 전략별 `target_pct`
* 전략별 `stop_loss_pct`
* 전략별 `signal_age_limit_sec`

## 작업 요구

### 1) 보수적 시작

초기 기준:

* exposure 낮게 유지
* cooldown 강하게 유지
* stop loss 보수적으로 유지

### 2) 조정 방식

* 임의 변경 금지
* 최소 20~30 closed trades 기준으로 재평가
* 변경 전/후 성과 비교 기록 필수

### 3) 변경 로그 남기기

권장 문서:

* `docs/CNT v2 PERFORMANCE TUNING LOG.md`

완료 조건:

* 파라미터 변경은 근거와 함께 남아야 함
* “느낌상 좋아 보임” 방식 금지

---

# 7. P4-5 Testnet 운영 검증 단계 추가

## 목적

코드/합성 테스트가 아니라 **운영 시나리오 기준 성능 확인**을 수행한다.

## 요구 사항

### 1) 최소 관찰 기간

권장:

* 최소 3일 이상
* 또는 최소 20건 이상 closed trades

### 2) 필수 수집 항목

* 총 signal 수
* 총 selected signal 수
* 총 executed trade 수
* 승률
* 평균 수익/손실
* 연속 손실 최대치
* 최대 일일 손실 횟수
* 전략별 성과 비교
* 차단 사유 분포

  * `LOSS_COOLDOWN`
  * `DAILY_LOSS_LIMIT`
  * `MAX_PORTFOLIO_EXPOSURE`
  * `ONE_PER_SYMBOL_POLICY`
  * `stale_signal`
  * 기타

### 3) 운영 기록 파일

권장:

* `docs/CNT v2 TESTNET PERFORMANCE REPORT.md`

완료 조건:

* 운영 결과가 숫자로 정리돼야 함
* “잘 돌아갔다”가 아니라 “얼마나 잘/나쁘게 돌아갔는지”를 기록해야 함

---

# 8. P4-6 로그/리포트 보강

## 목적

나중에 원인 분석이 가능해야 한다.

## 대상 파일

* `src/logging/portfolio_logger.py`
* 필요 시 runtime log 포맷

## 추가 권장 로그 항목

* `selected_strategy`
* `rank_score`
* `rank_score_components`
* `requested_notional`
* `blocked_by_policy`
* `close_pnl_estimate`
* `strategy_expectancy_snapshot`

완료 조건:

* 신호 선택 이유와 차단 이유를 로그로 재구성할 수 있어야 함

---

# 9. 구현 순서

## 1단계

* 전략 성능 지표 저장 구조 추가
* 종료 거래 시 metrics 업데이트 연결

## 2단계

* signal_ranker에 expectancy 반영
* 초기 fallback 규칙 추가

## 3단계

* testnet 관찰 운영
* 결과 수집

## 4단계

* 리스크/전략 파라미터 미세조정
* tuning log 작성

---

# 10. 검증 지시

## 필수 검증

### A. 단위 검증

* 전략 성과 파일 save/load 정상
* close action 후 metrics 업데이트 정상
* expectancy 계산 0 division 방어

### B. synthetic 검증

* 승/패 거래를 인위적으로 넣어

  * win_rate
  * expectancy
  * confidence
  * rank adjustment
    정상 반영 확인

### C. 운영 검증

* testnet에서 실제 로그 기준

  * rank score 기록
  * selected strategy 기록
  * 차단 사유 집계 가능 여부 확인

---

# 11. 완료 판정 기준

## P4 완료 기준

다음을 모두 만족해야 한다.

1. 전략별 성과가 누적 저장된다
2. ranker가 성과 데이터를 반영한다
3. testnet 운영 결과가 수치로 정리된다
4. 리스크/전략 파라미터 변경 이력이 문서화된다

---

# 12. 금지 사항

* 성능 개선 전제 없이 구조 리팩터링만 반복하는 것 금지
* 지표 없이 파라미터를 자주 바꾸는 것 금지
* closed trade 표본이 충분하지 않은데 전략 우열을 단정하는 것 금지
* 문서 표현이 실제 성능보다 앞서가는 것 금지

---

# 13. 최종 목표

이번 단계의 목표는 단순하다.

> **CNT v2를 “운영 가능한 엔진”에서 “성능이 검증되는 엔진”으로 올린다.**

그리고 그 다음 단계는 자연스럽다.

> P4가 끝나면
> **전략별 수익성 비교 → 자본 배분 → 실전 전환 기준 정의**
> 단계로 넘어간다.

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]
