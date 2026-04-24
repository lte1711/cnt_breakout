---
tags:
  - cnt
  - breakout
  - isolation
  - midpoint
aliases:
  - CNT v2 BREAKOUT ISOLATION MIDPOINT CHECK KO
---

# CNT v2 BREAKOUT 격리 중간 점검

## 현재 점검 위치

- baseline commit: `be75061`
- isolation runtime start commit: `e27f3b9`
- isolation runtime start time: `2026-04-22 13:40:36`
- midpoint target: `10 additional cycles`
- currently observed additional cycles: `6`
- current snapshot timestamp: `2026-04-22 13:44:03`

## 중간 점검 라벨

- current label: `STRUCTURALLY_HEALTHY, PERFORMANCE_DEGRADED`
- current gate: `FAIL / NON_POSITIVE_EXPECTANCY`
- midpoint status: `insufficient sample`

## 기준선 대비 현재

### Mixed Portfolio Observed

- baseline
  - `expectancy = -0.0007807916666668097`
  - `profit_factor = 0.9158659890090017`
  - `execution_rate = 24 / 86 = 27.91%`
  - `execution_block_rate = 62 / 86 = 72.09%`
  - `no_candidate_rate = 244 / 330 = 73.94%`

- current
  - `expectancy = -0.0007807916666668097`
  - `profit_factor = 0.9158659890090017`
  - `execution_rate = 24 / 90 = 26.67%`
  - `execution_block_rate = 66 / 90 = 73.33%`
  - `no_candidate_rate = 246 / 336 = 73.21%`

- delta
  - `expectancy delta = 0.000000`
  - `profit_factor delta = 0.000`
  - `execution_rate delta = -1.24 pts`
  - `execution_block_rate delta = +1.24 pts`
  - `no_candidate_rate delta = -0.73 pts`

### Breakout Observed Baseline

- baseline
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`

- current
  - `trades_closed = 3`
  - `expectancy = -0.022197999999999656`
  - `profit_factor = 0.17295081967214201`

- delta
  - `trades_closed delta = 0`
  - `expectancy delta = 0.000000`
  - `profit_factor delta = 0.000`

### Pullback Inferred Baseline

- baseline
  - `trades_closed = 21`
  - `expectancy = 0.0022788095238093107`
  - `profit_factor = 1.3365141201619735`

- current
  - `trades_closed = 21`
  - `expectancy = 0.0022788095238093107`
  - `profit_factor = 1.3365141201619735`

- delta
  - `trades_closed delta = 0`
  - `expectancy delta = 0.000000`
  - `profit_factor delta = 0.000`

## 처리량과 차단 압력

- selection rate current
  - `90 / 672 = 13.39%`
- execution rate current
  - `24 / 90 = 26.67%`
- execution block pressure current
  - `66 / 90 = 73.33%`
- no candidate pressure current
  - `246 / 336 = 73.21%`

해석:

- mixed expectancy와 PF는 아직 회복되지 않았다
- breakout 관측 품질도 아직 개선되지 않았다
- execution throughput은 기준선보다 약간 약해졌다
- no candidate pressure도 여전히 높다

## 저표본 경고

이건 아직 완전한 midpoint completion이 아니다.

- midpoint target은 `10-cycle`
- 현재 추가 관측은 `6 cycles`

또한 `breakout_v1` 자체도 여전히 저표본 상태다.  
현재 breakout 지표가 변하지 않았다고 해서 강한 결론을 내려서는 안 된다.

## Push 상태

- `be75061` push status: not pushed yet
- `e27f3b9` push status: not pushed yet
- local branch status at check time: `ahead of origin/main by 2 commits`

## 중간 결론

- `insufficient sample`

## Obsidian Links

- [[CNT v2 BREAKOUT ISOLATION RUNTIME START]]
- [[CNT v2 POST-READY DEGRADATION REVIEW]]
- [[CNT v2 STRATEGY ISOLATION COMPARISON]]
