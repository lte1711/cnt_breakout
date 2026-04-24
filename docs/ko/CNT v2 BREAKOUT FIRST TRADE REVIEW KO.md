---
tags:
  - cnt
  - docs
  - breakout
  - report
  - v2
aliases:
  - CNT v2 BREAKOUT FIRST TRADE REVIEW KO
---

# CNT v2 BREAKOUT 첫 거래 리뷰

```text
DOCUMENT_NAME = cnt_v2_breakout_first_trade_review_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = FIRST_BREAKOUT_TRADE_REVIEWED
REFERENCE_1   = CNT v2 BREAKOUT TREND FILTER REDESIGN REPORT
REFERENCE_2   = CNT v2 CURRENT STATUS ASSESSMENT
REFERENCE_3   = CNT v2 TESTNET PERFORMANCE REPORT
```

---

# 1. 목적

이 문서는 trend-filter redesign 이후 처음 발생한 실제 `breakout_v1` 거래를 리뷰한다.

목표는 아직 최적화가 아니다.

이 문서의 질문은 다음과 같다.

- breakout이 실제로 candidate와 selection path에 들어갔는가
- breakout이 실제 거래를 만들었는가
- 첫 breakout 종료 거래가 다음 병목에 대해 무엇을 말해 주는가

---

# 2. 검증된 사실

현재 런타임 증거는 아래를 확인해 준다.

- `breakout_v1.signals_selected = 1`
- `breakout_v1.trades_closed = 1`
- `selected_strategy_counts.breakout_v1 = 1`

Selection-path 증거:

- `2026-04-20 17:14:03`
- `selected_strategy=breakout_v1`
- `selection_reason=highest_score`
- `candidate_count=1`
- `rank_score=1.9`

Trade lifecycle 증거:

- `2026-04-20 17:14:00` `BUY_SUBMITTED`
- `2026-04-20 17:34:00` `PROMOTE_TO_OPEN_TRADE`
- `2026-04-20 17:44:00` `STOP_MARKET_FILLED`

---

# 3. 첫 breakout 거래 요약

## 진입

- entry price = `2300.0`
- stop price = `2296.55`
- target price = `2304.6`
- strategy = `breakout_v1`

## 종료

- close action = `STOP_MARKET_FILLED`
- close pnl estimate = `-0.011044`

## 성과 영향

현재 `breakout_v1` strategy metrics:

- `trades_closed = 1`
- `wins = 0`
- `losses = 1`
- `expectancy = -0.011044`
- `profit_factor = 0.0`

해석:

- breakout은 더 이상 dead branch가 아니다
- breakout은 이제 실제 전략이지만 표본은 아직 작다
- 패배한 거래 1건만으로 전략 실패라고 단정할 수는 없다

---

# 4. 중요한 구조적 결과

이 redesign은 구조 수준에서는 성공했다.

이제 실제로 증명된 것:

1. breakout이 candidate path에 도달할 수 있다
2. breakout이 ranking에서 이겨 선택될 수 있다
3. breakout이 live testnet entry를 제출할 수 있다
4. breakout이 full trade lifecycle을 마칠 수 있다

즉, 이전 핵심 문제였던

- `generated > 0`
- `selected = 0`

상태는 해결됐다.

---

# 5. activation 이후 새 병목

첫 breakout 거래 이후 rejection reason은 더 아래 단계로 내려왔다.

- `breakout_not_confirmed`
- `ema_fast_not_above_slow`
- `range_bias_up_but_entry_trend_not_up`
- `volatility_not_high`

해석:

- 이제 주 문제는 상단 trend exclusion 하나가 아니다
- 전략은 더 아래 단계의 setup quality check에서 제약되고 있다
- 이건 “아예 선택되지 않는 구조”보다 건강한 실패 형태다

---

# 6. 현재 판단

## 지금 사실인 것

- breakout activation objective = achieved
- breakout profitability objective = not yet achieved
- breakout sample size = still too small

## 올바른 다음 단계

현재 올바른 다음 단계는:

- 관측 계속
- breakout 표본 추가 수집
- 즉시 ATR / RSI 튜닝 금지
- pullback 튜닝 금지

다음 설계 질문은:

- 표본이 충분히 쌓였을 때 lower-gate quality check를 재설계해야 하는가

이지,

- breakout을 즉시 꺼야 하는가

가 아니다.

---

# 7. 권고

권고 순서:

1. 현재 breakout redesign 유지
2. breakout trade sample 추가 누적
3. activation 이후 breakout rejection distribution 비교
4. 그 다음에야 다음 리뷰 타겟을 결정
   - volatility gate
   - entry EMA confirmation
   - breakout confirmation strictness

---

# 8. 최종 결론

첫 breakout 거래는 손실로 끝났지만, 그게 핵심 결론은 아니다.

핵심 결론은 다음이다.

**`breakout_v1`는 이제 실제 런타임 경로에서 살아 있다. 현재 단계는 activation이 아니라 quality evaluation 단계다.**

---

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[CNT v2 BREAKOUT TREND FILTER REDESIGN REPORT]]
- [[CNT v2 CURRENT STATUS ASSESSMENT]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
