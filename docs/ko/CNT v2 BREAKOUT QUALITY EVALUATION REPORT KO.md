---
aliases:
  - CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO
---

# CNT v2 BREAKOUT 품질 평가 보고

```text
DOCUMENT_NAME = cnt_v2_breakout_quality_evaluation_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-21
STATUS        = QUALITY_EVALUATION_ACTIVE
REFERENCE_1   = CNT v2 BREAKOUT FIRST TRADE REVIEW
REFERENCE_2   = CNT v2 CURRENT STATUS ASSESSMENT
REFERENCE_3   = CNT v2 TESTNET PERFORMANCE REPORT
```

---

# 1. 설계 요약

이 문서는 dead-branch 상태를 벗어난 뒤 `breakout_v1`의 현재 품질 상태를 평가한다.

이 단계의 목표는 최적화가 아니다.

이 단계의 목표는 아래 세 질문에 답하는 것이다.

1. `breakout_v1`가 실제 런타임 경로에서 살아 있는가?
2. 현재 지배적인 병목은 어디인가?
3. 다음 단계는 튜닝인가, 아니면 관측인가?

---

# 2. 검증 결과

최신 snapshot 기준 확인된 값:

- `snapshot timestamp = 2026-04-21 01:04:04`
- `breakout_v1.signals_generated = 149`
- `breakout_v1.signals_selected = 1`
- `breakout_v1.trades_closed = 1`
- `breakout_v1.wins = 0`
- `breakout_v1.losses = 1`
- `breakout_v1.expectancy = -0.011044`
- `selected_strategy_counts.breakout_v1 = 1`

현재 `signal.log` 기준 aggregate rejection distribution:

- `market_not_trend_up = 100`
- `volatility_not_high = 29`
- `range_bias_up_but_entry_trend_not_up = 8`
- `range_without_upward_bias = 8`
- `ema_fast_not_above_slow = 3`
- `rsi_below_entry_threshold = 2`
- `breakout_not_confirmed = 1`
- `trend_up_high_volatility_breakout = 1`

해석:

- `breakout_v1`는 더 이상 dead branch가 아니다
- lower-gate rejection이 실제 런타임 증거에 나타나기 시작했다
- 그러나 가장 큰 aggregate bottleneck은 여전히 `market_not_trend_up`
- 추가 cycle에서도 아직 두 번째 breakout selection은 생기지 않았다

---

# 3. 기록 문장

## 3.1 현재 품질 상태

현재 `breakout_v1`의 품질 상태는 다음처럼 표현하는 것이 맞다.

- activation objective = completed
- quality evaluation objective = active
- profitability judgment = not yet reliable

즉:

- “breakout이 실제로 살아났는가?”에 대한 답은 `yes`
- “breakout이 이미 좋은 전략인가?”에 대한 답은 `not yet judgeable`

## 3.2 실제로 증명된 것

이제 실제 런타임에서 아래가 증명됐다.

1. breakout이 candidate path에 들어갈 수 있다
2. breakout이 ranking에서 이겨서 선택될 수 있다
3. breakout이 BUY order를 제출할 수 있다
4. breakout이 full trade lifecycle을 완료할 수 있다

이건 구조적으로 의미 있는 성공이다.

## 3.3 아직 해결되지 않은 것

주요 미해결 항목은 다음과 같다.

1. 지배적인 aggregate rejection reason이 여전히 `market_not_trend_up`
2. breakout은 아직 closed trade가 1건뿐이라 profitability 판단 불가
3. lower-gate failure는 보이지만 여전히 under-sampled

따라서 다음 질문은:

- “ATR/RSI를 더 풀어야 하나?”

가 아니라,

- “market regime gate가 breakout 의도 대비 아직도 너무 빡빡한가?”
- “표본이 더 쌓이면 lower-gate reason이 지배적으로 바뀌는가?”

가 되어야 한다.

## 3.4 현재 운영 권고

현재 시점의 권고 운영 방식:

1. `pullback_v1`를 메인 운영 전략으로 유지
2. `breakout_v1`는 실험 전략으로 유지
3. breakout 표본을 더 누적
4. `market_not_trend_up` 비중을 계속 추적
5. 추가 ATR/RSI 완화는 아직 하지 않음
6. post-activation window에서 `volatility_not_high` 비중이 계속 커지는지도 확인

## 3.5 최종 판단

현재 breakout 품질 판단:

```text
STATUS = QUALITY_EVALUATION_ACTIVE
ACTIVATION = PASSED
PROFITABILITY = NOT_YET_JUDGEABLE
PRIMARY_BOTTLENECK = market_not_trend_up
NEXT_ACTION = CONTINUE_OBSERVATION
```

한 줄 결론:

**`breakout_v1`는 이제 실제 런타임 경로에서 살아 있지만, 지배적인 aggregate bottleneck은 여전히 `market_not_trend_up`이므로, 지금 맞는 다음 단계는 추가 튜닝이 아니라 더 많은 품질 관측이다.**

---

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]


