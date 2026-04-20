---
tags:
  - cnt
  - docs
  - v2
aliases:
  - CNT v2 LIVE READINESS GATE
---

# CNT v2 LIVE READINESS GATE

문서 목적:
CNT v2가 Testnet 검증을 통과했는지 판단하고,
실거래(Live Trading) 전환 여부를 **객관적 기준으로 결정**한다.

문서 상태:
Final Gate / Go-No-Go Decision

---

# 1. 게이트 철학

이 문서는 감이 아니라 **데이터로 결정한다.**

> ❗ “돌아간다” → 부족
> ❗ “수익 난다” → 아직 부족
> ✅ **“통계적으로 유지 가능한 구조다” → 통과**

---

# 2. 사전 조건 (Preconditions)

아래 조건 미충족 시 즉시 FAIL

## 필수 조건

* `closed_trades >= 20`
* 운영 기간 ≥ 3일
* `strategy_metrics.json` 정상 누적
* `portfolio.log` 필드 정상 기록
* risk policy 실제 작동 로그 존재

---

# 3. 핵심 성능 기준

## 3.1 수익성

| 항목         | 기준  |
| ---------- | --- |
| Net PnL    | > 0 |
| Expectancy | > 0 |

👉 둘 중 하나라도 실패 시 FAIL

---

## 3.2 안정성

| 항목                       | 기준     |
| ------------------------ | ------ |
| max_consecutive_losses   | ≤ 5    |
| daily_loss_limit_trigger | 0~2 범위 |
| cooldown_trigger         | 정상 발생  |

👉 cooldown이 한 번도 안 걸리면 FAIL (리스크 무력화 의심)

---

## 3.3 분포 건강성

| 항목           | 기준          |
| ------------ | ----------- |
| 단일 전략 의존도    | ≤ 80%       |
| strategy 다양성 | 최소 2개 전략 실행 |

👉 한 전략만 계속 쓰면 FAIL

---

## 3.4 리스크 정책 검증

아래가 **실제 로그에서 확인**되어야 한다:

* `LOSS_COOLDOWN`
* `DAILY_LOSS_LIMIT`
* `MAX_PORTFOLIO_EXPOSURE`
* `ONE_PER_SYMBOL_POLICY`

👉 하나라도 “전혀 안 걸림” → FAIL

---

## 3.5 랭커 검증

확인 항목:

* `rank_score` 변화 존재
* `rank_score_components` 비어있지 않음
* expectancy 반영 로그 존재

👉 항상 동일 score → FAIL

---

# 4. 전략별 판정

각 전략별로 아래 평가:

## 유지 기준

* expectancy > 0
* trades ≥ 5
* win_rate ≥ 35%

## 개선 대상

* expectancy ≈ 0
* 변동성 큼

## 제거 대상

* expectancy < 0
* losses 지속

---

# 5. FAIL 조건 (즉시 차단)

아래 중 하나라도 해당되면:

```text
STATUS = NOT_READY
```

* Net PnL < 0
* Expectancy < 0
* closed_trades < 20
* 단일 전략 90% 이상 사용
* risk policy 미작동
* ranker 비동작 (fallback 고정)

---

# 6. PASS 조건

모든 조건 만족 시:

```text
STATUS = LIVE_READY
```

---

# 7. 조건부 PASS (권장 상태)

```text
STATUS = LIVE_READY_WITH_GUARDRAILS
```

조건:

* Net PnL > 0
* Expectancy > 0
* 일부 전략 성능 불안정
* 리스크 정책 정상 작동

---

# 8. Live 전환 규칙

## 초기 설정

* 자본: 최소 (예: 1~5% 계정)
* 포지션 크기: 축소
* exposure 제한 강화

---

## 금지 사항

* 첫날부터 full size 운영 금지
* 동시에 여러 전략 확장 금지
* 파라미터 즉시 변경 금지

---

## 필수 보호 장치

* DAILY_LOSS_LIMIT 유지
* LOSS_COOLDOWN 유지
* ONE_PER_SYMBOL_POLICY 유지

---

# 9. Live 초기 모니터링

## 첫 24시간

* 모든 trade 수동 검토
* 로그 상세 확인
* unexpected behavior 체크

---

## 첫 3일

* strategy별 성과 재확인
* ranker 선택 패턴 분석
* risk trigger 정상 여부 확인

---

# 10. 산출물

최종 작성 문서:

## CNT v2 LIVE READINESS REPORT

포함 내용:

```text
- closed_trades
- net_pnl
- expectancy
- win_rate
- max_consecutive_losses
- strategy breakdown
- risk trigger stats
- final decision (PASS / FAIL)
```

---

# 11. 최종 결정

## PASS

```text
GO LIVE (LIMITED CAPITAL)
```

## FAIL

```text
RETURN TO TUNING
```

---

# 12. 핵심 결론

이 단계의 핵심은 단 하나다:

> ❗ “좋아 보인다”는 이유로 통과시키지 않는다
> ❗ **“숫자가 증명했다”만 통과한다**

---

# 마지막 한 줄

> CNT v2는 이제 구조 문제가 아니라
> **실제로 돈을 벌 수 있는 시스템인지 검증하는 단계다**

---

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]
