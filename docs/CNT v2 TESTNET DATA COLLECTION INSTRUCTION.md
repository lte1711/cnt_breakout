---
aliases:
  - CNT v2 TESTNET DATA COLLECTION INSTRUCTION
---

맞다. 현재 판정은 **`PERFORMANCE_VALIDATION_IN_PROGRESS`**가 정확하다.

# 현재 상태 정리

## 확정 가능한 것

* 구조 패치 완료
* 운영 정합성 확보
* 계측 계층 추가 완료
* performance-aware ranker 구현 완료
* metrics persistence 가능
* 로그 필드 확보 완료

## 아직 확정 불가한 것

* 전략 우열
* 실제 expectancy 우위
* 파라미터 튜닝 필요 여부
* broader deployment 가능 여부

## 이유

체크리스트 최소 기준 미충족:

* `closed trades = 0`
* 운영 기간 `< 3일`

즉,

> **지금은 성능 검증 시스템이 준비된 상태이지, 성능이 검증된 상태가 아니다.**

---

# 현재 최종 판정 문구

```text
STATUS   = PERFORMANCE_VALIDATION_IN_PROGRESS
DECISION = HOLD_JUDGMENT
REASON   = INSUFFICIENT_SAMPLE
NEXT     = TESTNET_DATA_COLLECTION
```

---

# 다음 진행지시서

아래 기준으로 바로 이어가면 된다.

# CNT v2 TESTNET DATA COLLECTION INSTRUCTION

## 목적

최소 표본을 확보해 performance validation을 가능 상태로 만든다.

## 종료 조건

아래 둘 중 하나 충족 시 종료:

* `closed_trades >= 50`
* `testnet operation >= 3 days`

## 운영 중 금지

* 전략 우열 단정 금지
* ranker weight 수정 금지
* risk parameter 수정 금지
* target/stop 임의 조정 금지

## 운영 중 허용

* 로그 수집
* metrics 파일 누적
* 리포트 숫자 갱신
* 명백한 버그만 수정

## 매 실행 후 기록 항목

* total_signals
* selected_signals
* executed_trades
* closed_trades
* blocked_by_policy 분포
* strategy_metrics snapshot
* rank_score sample logs
* close_pnl_estimate sample logs

## 중간 점검 기준

### closed trades 5건 시

* 로그 누락 여부만 점검
* 성능 결론 금지

### closed trades 10건 시

* 분포 이상치만 점검
* 튜닝 금지

### closed trades 20건 또는 3일 시

* 그때 처음으로

  * expectancy
  * win_rate
  * strategy comparison
  * tuning 필요 여부
    판정 시작

## 필수 산출물 유지

* `CNT v2 TESTNET PERFORMANCE REPORT.md`
* `CNT v2 PERFORMANCE TUNING LOG.md`
* `CNT v2 PERFORMANCE VALIDATION REPORT.md`

## 중간 판정 규칙

표본 충족 전 상태는 항상 아래로 유지:

```text
PERFORMANCE_VALIDATION_IN_PROGRESS
```

---

# 핵심 결론

지금 단계에서 가장 중요한 건 이것이다.

> **분석은 가능하지만 판단은 아직 금지다.**

다음 커밋 목표도 명확하다.

> **“구현 완료”가 아니라 “표본 확보 완료”**

---

## Obsidian Links

- [[CNT v2 TESTNET PERFORMANCE REPORT]]

