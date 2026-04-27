---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - cnt-v2-breakout-last-3-trades-review-ko
---

# CNT v2 BREAKOUT 최근 3개 거래 리뷰

## 범위

이 리뷰는 `logs/portfolio.log`만을 기준으로 작성한다.

최근 breakout selection 이벤트 중, 이후 실제 close까지 확정된 마지막 세 건을 짝지어 읽는다.

## Trade 1

- `selection_time = 2026-04-20 17:14:03`
- `reason = trend_up_high_volatility_breakout`
- `confidence = 0.82`
- `selection_expectancy_snapshot = 0.0`
- `close_time = 2026-04-20 17:44:03`
- `close_action = STOP_MARKET_FILLED`
- `close_pnl_estimate = -0.01104399999999996`
- `post_trade_expectancy_snapshot = -0.01104399999999996`
- `post_trade_profit_factor_snapshot = 0.0`

해석:

- 첫 breakout 실거래가 곧바로 음수 expectancy 기준선을 만들었다
- 이후 breakout selection은 이미 손상된 표본 상태에서 시작했다

## Trade 2

- `selection_time = 2026-04-21 03:04:03`
- `reason = trend_up_high_volatility_breakout`
- `confidence = 0.82`
- `selection_expectancy_snapshot = -0.01104399999999996`
- `close_time = 2026-04-21 03:54:02`
- `close_action = SELL_FILLED`
- `close_pnl_estimate = 0.01392600000000084`
- `post_trade_expectancy_snapshot = 0.0014410000000004402`
- `post_trade_profit_factor_snapshot = 1.2609561752988854`

해석:

- recovery win 1건은 있었다
- 하지만 표본이 너무 작아서 안정적인 edge를 증명하진 못했다

## Trade 3

- `selection_time = 2026-04-22 04:14:04`
- `reason = trend_up_relaxed_volatility_breakout`
- `confidence = 0.68`
- `selection_expectancy_snapshot = 0.0014410000000004402`
- `close_time = 2026-04-22 04:44:04`
- `close_action = STOP_MARKET_FILLED`
- `close_pnl_estimate = -0.06947599999999984`
- `post_trade_expectancy_snapshot = -0.022197999999999656`
- `post_trade_profit_factor_snapshot = 0.17295081967214201`

해석:

- 세 번째 breakout 종료 거래가 결정적인 품질 붕괴를 만들었다
- 동시에 relaxed breakout path도 테스트가 아니라 실제 런타임 증거에 포함되게 됐다

## 종합 해석

최근 세 개의 확정 breakout 거래를 합치면:

- wins = `1`
- losses = `2`
- net_pnl = `-0.06659399999999896`
- expectancy after trade 3 = `-0.022197999999999656`

## 필수 결론

**breakout_v1 isolation required**

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]


