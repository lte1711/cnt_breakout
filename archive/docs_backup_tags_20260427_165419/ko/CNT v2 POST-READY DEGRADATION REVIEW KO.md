---
aliases:
  - CNT v2 POST-READY DEGRADATION REVIEW KO
---

# CNT v2 라이브 준비도 이후 성능 저하 리뷰

## 분류

이 문서는 CNT가 `LIVE_READY`에 도달한 뒤 다시 `FAIL`로 떨어졌을 때 작성된 사실 기반 degradation review다.

## 현재 라벨

`STRUCTURALLY_HEALTHY, PERFORMANCE_DEGRADED`

## 현재 Fail 상태

최신 검증 소스:

- `data/performance_snapshot.json`
- `data/strategy_metrics.json`
- `data/live_gate_decision.json`

현재 게이트 결과:

- `status = FAIL`
- `reason = NON_POSITIVE_EXPECTANCY`

리뷰 시점 snapshot:

- `timestamp = 2026-04-22 12:44:03`
- `closed_trades = 24`
- `selected_signals = 86`
- `executed_trades = 24`
- `win_rate = 0.5416666666666666`
- `expectancy = -0.0007807916666668097`
- `net_pnl = -0.018739000000003447`
- `profit_factor = 0.9158659890090017`

## 왜 구조적 실패가 아닌가

현재 `FAIL`은 engine malfunction으로 설명되지 않는다.

여전히 정상 동작하는 항목:

- state persistence
- runtime logging
- strategy selection
- execution counting
- performance snapshot generation
- live gate evaluation

즉 문제는 orchestration failure가 아니다.

이것은 **performance deterioration** 문제다.

## Breakout의 음수 기여

`breakout_v1`의 현재 품질:

- `trades_closed = 3`
- `wins = 1`
- `losses = 2`
- `expectancy = -0.022197999999999656`
- `profit_factor = 0.17295081967214201`
- `gross_profit = 0.01392600000000084`
- `gross_loss = 0.0805199999999998`
- `net_pnl = -0.06659399999999896`

기여 해석:

- breakout은 닫힌 거래 비중으로는 `3 / 24 = 12.5%`
- 하지만 순기여는 `-0.066594`
- 혼합 포트폴리오의 총 net은 `-0.018739`

즉 breakout 손실이 pullback의 양수 edge를 지워 전체 포트폴리오를 음수 기대값으로 밀어냈다.

## Pullback 단독 품질은 여전히 양수

`pullback_v1` 단독 품질:

- `trades_closed = 21`
- `wins = 12`
- `losses = 9`
- `expectancy = 0.0022788095238093107`
- `profit_factor = 1.3365141201619735`
- `gross_profit = 0.19006300000000023`
- `gross_loss = 0.14220800000000472`
- `inferred_net_pnl = +0.04785499999999551`

해석:

- pullback은 단독으로는 여전히 유효하다
- 현재 combined `FAIL`은 pullback 품질 붕괴 증거가 아니다
- 저하는 low-quality breakout sample과의 포트폴리오 혼합이 지배한다

## Throughput 약점

`LIVE_READY` 이후에도 throughput은 여전히 약하다.

- `selection_rate = 86 / 660 = 13.03%`
- `execution_rate = 24 / 86 = 27.91%`

blocked-signal evidence:

- `DAILY_LOSS_LIMIT = 62`
- `no_ranked_signal = 219 + 25 = 244`

운영 압력:

- `execution_block_rate = 62 / 86 = 72.09%`
- `no_candidate_rate = 244 / 330 = 73.94%`

즉 문제는 포트폴리오 품질뿐 아니라 throughput 제한도 함께 존재한다.

## Risk Block 압력

관측된 보호 압력:

- `risk_trigger_stats.DAILY_LOSS_LIMIT = 124`
- `state.risk_metrics.daily_loss_count = 3`
- `state.risk_metrics.consecutive_losses = 2`

해석:

- risk layer는 정당한 이유로 계속 작동 중이다
- 이것을 버그로 해석하면 안 된다
- 최근 trade quality가 아직 충분히 안정적이지 않다는 신호다

## 최종 리뷰 문장

현재 단계는 아래처럼 해석해야 한다.

- structurally healthy
- further loosening은 아직 부적절
- separated quality diagnosis 필요

## 요구 결론

**portfolio quality degraded but structurally healthy**

## 링크

- CNT v2 POST-READY DEGRADATION REVIEW
- CNT v2 CURRENT STATUS ASSESSMENT KO
- CNT v2 LIVE READY POST-READINESS MONITORING PLAN KO

## Obsidian Links

- [[00 Docs Index KO]]


