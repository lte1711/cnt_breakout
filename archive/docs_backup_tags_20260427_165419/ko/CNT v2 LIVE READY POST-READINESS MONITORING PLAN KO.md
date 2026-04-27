---
aliases:
  - CNT v2 LIVE READY POST-READINESS MONITORING PLAN KO
---

# CNT v2 라이브 준비도 통과 이후 모니터링 계획

## 분류

이 문서는 CNT가 `LIVE_READY`에 도달한 이후의 사실 기반 post-readiness 운영 계획이다.

라이브 준비도 모니터링 모드에서 반드시 계속 보여야 하는 baseline metric을 고정한다.

## Baseline Snapshot

기준 데이터:

- `data/performance_snapshot.json`
- `data/live_gate_decision.json`

기준 시각:

- `2026-04-22 02:44:03`

기준 게이트 결정:

- `LIVE_READY`
- `ALL_GATES_PASSED`

## 고정 Baseline Metrics

- `closed_trades = 21`
- `executed_trades = 22`
- `selected_signals = 62`
- `total_signals = 558`
- `win_rate = 0.5714285714285714`
- `expectancy = 0.0013191904761903238`
- `net_pnl = 0.027702999999996814`
- `profit_factor = 1.196938891574459`
- `selection_rate = 62 / 558 = 11.11%`
- `execution_rate = 22 / 62 = 35.48%`
- `no_ranked_signal_total = 192 + 25 = 217`

전략 분리 baseline:

- `pullback_v1 signals_selected = 57`
- `breakout_v1 signals_selected = 5`
- `pullback_share = 91.94%`
- `breakout_share = 8.06%`

## Monitoring Window

다음 모니터링 창:

- `20 to 30 additional cycles`

이 창 동안에는 별도 설계 및 validation 기록이 없는 한 runtime parameter를 바꾸지 않는다.

## 주요 추적 지표

아래 항목을 계속 추적해야 한다.

1. `selection_rate`
2. `execution_rate`
3. `no_ranked_signal`
4. `strategy_split`
5. `LIVE_READY` 유지 여부
6. `profit_factor`
7. `expectancy`

## 해석 규칙

이 단계의 CNT는 다음처럼 해석해야 한다.

- `LIVE_READY`
- 하지만 throughput-constrained
- operating quality stabilization이 아직 필요함

즉:

- `LIVE_READY`는 “완전 최적화됨”을 뜻하지 않는다
- `LIVE_READY`는 최소 준비 기준을 충족했다는 뜻이다
- 다음 질문은 이 품질이 runtime이 계속돼도 유지되는가이다

## No-Change Window

post-readiness observation window 동안 아래는 동결된다.

- risk guard 완화 금지
- 새 filter 완화 금지
- symbol expansion 금지
- multi-position expansion 금지
- ranker retuning 금지

## 다음 리뷰 트리거

아래 중 하나가 발생하면 다음 design review로 올린다.

1. `profit_factor < 1.1`이 반복 스냅샷에서 관측됨
2. `expectancy <= 0`
3. `LIVE_READY` 상실
4. `breakout_v1 trades_closed >= 5`
5. `no_ranked_signal`가 의미 있게 증가 또는 감소함

## 한 줄 운영 규칙

**CNT는 이제 post-readiness stabilization 단계다. 설정을 고정하고, baseline delta를 추적하며, 새로운 최적화 전에 지속성을 먼저 판단해야 한다.**

## 링크

- CNT v2 LIVE READY POST-READINESS MONITORING PLAN
- CNT v2 CURRENT STATUS ASSESSMENT KO
- CNT v2 LIVE READINESS GATE KO
- CNT v2 LIVE GATE ALIGNMENT REPORT KO

## Obsidian Links

- [[CNT v2 LIVE READINESS GATE KO]]


