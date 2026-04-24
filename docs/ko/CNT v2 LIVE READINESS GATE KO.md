---
aliases:
  - CNT v2 LIVE READINESS GATE KO
---

# CNT v2 라이브 준비도 게이트

## 목적

CNT v2의 라이브 준비도 게이트는 단순 수익 여부만 보는 기준이 아니다.

이 문서는 Testnet 운영에서 아래 항목이 실제로 관측되었는지를 바탕으로
보수적으로 `NOT_READY`, `FAIL`, `LIVE_READY`를 판정하는 기준 문서다.

핵심 확인 항목:

- 충분한 표본 수
- 기대값과 순손익의 양수 여부
- 연속 손실 통제 여부
- 리스크 보호 로직의 실제 발동 증거

## 현재 규칙

현재 게이트 판정은 아래 순서로 진행된다.

1. `closed_trades >= 20`
2. `expectancy > 0`
3. `net_pnl > 0`
4. `max_consecutive_losses <= 5`
5. `risk_trigger_stats` 안에서 아래 중 하나 이상이 실제로 관측되어야 함
   - `LOSS_COOLDOWN`
   - `DAILY_LOSS_LIMIT`

즉 현재 게이트는 `cooldown`만 강제하는 것이 아니라,
`daily loss guard` 또는 `cooldown guard` 중 하나라도 실제 로그/스냅샷에 남으면
리스크 보호 계층이 동작한 것으로 본다.

## Reason Codes

- `NOT_READY / INSUFFICIENT_SAMPLE`
- `FAIL / NON_POSITIVE_EXPECTANCY`
- `FAIL / NON_POSITIVE_NET_PNL`
- `FAIL / MAX_CONSECUTIVE_LOSSES_EXCEEDED`
- `FAIL / RISK_GUARD_NOT_OBSERVED`
- `LIVE_READY / ALL_GATES_PASSED`

## 해석 규칙

현재 CNT 문맥에서 각 상태의 의미는 다음과 같다.

- `NOT_READY` = 아직 표본이 부족한 상태
- `FAIL` = 표본은 있지만 운영 성과 또는 보호 계층 조건이 부족한 상태
- `LIVE_READY` = 수익만이 아니라 리스크 보호 로직이 실제로 관측된 상태

즉 `LIVE_READY`는 “최적화 완료”가 아니라
“최소 준비 기준을 사실 기반으로 통과함”을 뜻한다.

## 현재 상태 메모

현재 CNT는 Testnet 운영 단계이며,
라이브 게이트는 최신 산출물을 기준으로 계속 재평가된다.

우선 참조 데이터:

- `data/performance_snapshot.json`
- `data/live_gate_decision.json`
- `logs/runtime.log`
- `logs/portfolio.log`

## 링크

- CNT v2 LIVE READINESS GATE
- CNT v2 LIVE READINESS REPORT KO
- CNT v2 CURRENT STATUS ASSESSMENT KO
- 00 Docs Index KO

## Obsidian Links

- [[CNT v2 LIVE READINESS GATE KO]]


