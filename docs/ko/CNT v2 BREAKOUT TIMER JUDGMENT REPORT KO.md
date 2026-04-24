---
aliases:
  - CNT v2 BREAKOUT TIMER JUDGMENT REPORT KO
---

# CNT v2 BREAKOUT 타이머 판단 보고

```text
DOCUMENT_NAME = cnt_v2_breakout_timer_judgment_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = COMPLETE
REFERENCE_1   = CNT v2 BREAKOUT REVIEW TIMER REPORT
REFERENCE_2   = CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT REPORT
```

---

# 1. 요약

8시간 breakout review timer는 정상적으로 발동했고, 다음 판단도 완료됐다.

결과:

* breakout은 candidate path에 도달하지 못함
* selection-path observability는 시스템 안에서 확인됨
* 지배적인 breakout blocker는 `market_not_trend_up`
* 다음 단계는 추가 ATR / RSI 완화가 아니라 trend-filter review

---

# 2. 타이머 확인

Timer evidence:

* `data/breakout_review_due.json` 존재
* `status = READY_FOR_NEXT_JUDGMENT`
* `timestamp = 2026-04-20 09:10:34`
* `logs/breakout_review_timer.log`에 due marker 존재

---

# 3. 리뷰 사실

Snapshot facts:

* `closed_trades = 8`
* `wins = 5`
* `losses = 3`
* `selected_strategy_counts = {'pullback_v1': 3}`

Breakout facts:

* `signals_generated = 82`
* `signals_selected = 0`
* `trades_closed = 0`

실험 구간 breakout rejection distribution:

* `market_not_trend_up = 45`
* `volatility_not_high = 3`
* total = `48`
* `market_not_trend_up share = 93.75%`

---

# 4. 결정

```text
BREAKOUT_CANDIDATE_PATH = NOT_OBSERVED
BREAKOUT_SELECTION_PATH = NOT_OBSERVED
SELECTION_PATH_SYSTEM   = CONFIRMED
SELECTED_COUNTS_SYSTEM  = CONFIRMED
NEXT_ACTION             = REVIEW_TREND_FILTER
```

---

# 5. 운영 메모

아직 추적은 하지만 이번 판단을 막지는 않은 것:

1. `scheduler_stdout.log` encoding noise
2. overlapping manual run 중 가능한 log write collision

이 이슈들은 이번 실험 구간 판단을 바꾸지는 않았다.

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]


