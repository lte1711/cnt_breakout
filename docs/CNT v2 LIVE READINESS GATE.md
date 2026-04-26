---
aliases:
  - CNT v2 LIVE READINESS GATE
---

# CNT v2 LIVE READINESS GATE

## Purpose

CNT v2의 라이브 게이트는 단순 수익 여부가 아니라, 실제 Testnet 운영에서 다음이 모두 관측됐는지 확인하는 보수적 판정 계층이다.

- 표본 수 충분성
- 양의 기대값과 순손익
- 손실 연속성 제한
- 리스크 보호 로직의 실제 발동 증거

## Current Rule

현재 게이트 판정은 아래 순서로 진행된다.

1. `closed_trades >= 50`
2. `expectancy > 0`
3. `net_pnl > 0`
4. `max_consecutive_losses <= 5`
5. `risk_trigger_stats` 안에서 아래 중 하나 이상이 실제로 관측됨
   - `LOSS_COOLDOWN`
   - `DAILY_LOSS_LIMIT`

즉, 현재 게이트는 `cooldown`만 강제하지 않는다. `daily loss guard` 또는 `cooldown guard` 중 하나라도 실제 로그/스냅샷에 나타나면 리스크 보호 계층이 동작한 것으로 본다.

## Reason Codes

- `NOT_READY / INSUFFICIENT_SAMPLE`
- `FAIL / NON_POSITIVE_EXPECTANCY`
- `FAIL / NON_POSITIVE_NET_PNL`
- `FAIL / MAX_CONSECUTIVE_LOSSES_EXCEEDED`
- `FAIL / RISK_GUARD_NOT_OBSERVED`
- `LIVE_READY / ALL_GATES_PASSED`

## Interpretation

현재 CNT 문맥에서 중요한 점은 이렇다.

- `NOT_READY`는 아직 표본이 부족한 상태다.
- `FAIL`은 표본은 찼지만 운영 품질 또는 보호 계층 조건이 미충족인 상태다.
- `LIVE_READY`는 수익성뿐 아니라 리스크 보호 로직이 실제로 관측됐을 때만 허용된다.

## Current Status Note

현재 CNT는 Testnet 실운영 단계이며, 라이브 게이트는 최신 스냅샷 기준으로 계속 재평가된다. 판정은 항상 아래 실데이터를 우선한다.

- `data/performance_snapshot.json`
- `data/live_gate_decision.json`
- `logs/runtime.log`
- `logs/portfolio.log`

## Obsidian Links

- [[00 Docs Index]]

