---
tags:
  - cnt
  - live-readiness
  - gate
  - testnet
  - ko
  - status/active
  - type/documentation
  - type/validation
  - type/operation
  - risk
  - obsidian
  - type/analysis
  - status/completed
  - cnt-v2-live-readiness-gate-ko
---

# CNT v2 라이브 준비도 게이트

## 목적

이 문서는 Binance Spot Testnet 운영 기준의 CNT v2 공식 라이브 준비도 게이트를 정의한다.

이 게이트는 단순 수익 여부만 보는 기준이 아니다. 실제 런타임 증거에서 아래 조건이 모두 확인되는지를 보수적으로 판단하는 운영 기준이다.

- 충분한 종료 거래 표본 수
- 양수 기대값
- 양수 순손익
- 제한 범위 안의 연속 손실
- 리스크 보호 계층의 실제 작동 증거

## 현재 규칙

공식 라이브 게이트는 아래 순서로 평가한다.

1. `closed_trades >= 50`
2. `expectancy > 0`
3. `net_pnl > 0`
4. `max_consecutive_losses <= 5`
5. `risk_trigger_stats` 안에 아래 리스크 가드 중 하나 이상이 실제로 관측되어야 한다.
   - `LOSS_COOLDOWN`
   - `DAILY_LOSS_LIMIT`

리스크 가드 증거 조건은 두 보호 장치가 모두 발동해야 한다는 뜻이 아니다. 런타임 로그와 스냅샷 데이터에서 둘 중 하나 이상이 관측되면 보호 계층이 작동한 것으로 본다.

## 사유 코드

- `NOT_READY / INSUFFICIENT_SAMPLE`
- `FAIL / NON_POSITIVE_EXPECTANCY`
- `FAIL / NON_POSITIVE_NET_PNL`
- `FAIL / MAX_CONSECUTIVE_LOSSES_EXCEEDED`
- `FAIL / RISK_GUARD_NOT_OBSERVED`
- `LIVE_READY / ALL_GATES_PASSED`

## 해석 규칙

- `NOT_READY`는 아직 표본이 부족해 최종 준비도 판단을 할 수 없다는 뜻이다.
- `FAIL`은 표본은 있으나 성과 또는 보호 조건 중 하나 이상이 충족되지 않았다는 뜻이다.
- `LIVE_READY`는 정의된 증거 게이트를 통과했다는 뜻이다. 수익 보장을 의미하지 않는다.

## 현재 증거 소스

게이트는 요약 문서만이 아니라 현재 프로젝트 증거를 기준으로 평가해야 한다.

- `data/performance_snapshot.json`
- `data/live_gate_decision.json`
- `logs/runtime.log`
- `logs/portfolio.log`
- `src/validation/live_gate_evaluator.py`

## 현재 상태 메모

검증된 `2026-04-26 14:34:05` 스냅샷 기준:

```text
closed_trades = 42
expectancy    = -0.0005784761904763167
net_pnl       = -0.024296000000005313
status        = NOT_READY
reason        = INSUFFICIENT_SAMPLE
```

따라서 현재 CNT v2는 Testnet 데이터 수집 단계이며, 공식 게이트 기준으로 라이브 준비 완료 상태가 아니다.

## Obsidian Links

- [[00 Docs Index KO]]
- [[CNT v2 TESTNET PERFORMANCE REPORT KO]]
- [[CNT_PROJECT_STATUS_REPORT_20260426]]
- [[CNT_PRECISION_ANALYSIS_REPORT_20260426]]
