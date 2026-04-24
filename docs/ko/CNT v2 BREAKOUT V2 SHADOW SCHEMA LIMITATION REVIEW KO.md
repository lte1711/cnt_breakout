---
---

# CNT v2 BREAKOUT V2 SHADOW SCHEMA LIMITATION REVIEW KO

## 범위

이 문서는 현재 `breakout_v2` shadow schema가 무엇을 직접 증명할 수 있고, 무엇을 직접 증명할 수 없는지 정리한다.

## 현재 직접 관측 가능한 필드

current shadow event schema:

- `ts`
- `symbol`
- `strategy`
- `signal_generated`
- `entry_allowed`
- `filter_reason`
- `confidence`
- `vwap`
- `band_width_ratio`
- `band_expansion_ratio`
- `volume_ratio`
- `hypothetical_entry`

current shadow snapshot:

- `signal_count`
- `filtered_signal_count`
- `allowed_signal_count`
- `filtered_signal_ratio`
- `allowed_signal_ratio`
- `hypothetical_trades_count`
- `hypothetical_expectancy`
- `hypothetical_profit_factor`
- `stop_exit_ratio`
- `reason_distribution`
- `last_updated`

## 현재 schema로 증명 가능한 것

- first-blocker distribution
- total candidate starvation
- 현재 측정되는 ratio:
  - band width
  - band expansion
  - volume
- runtime에서 shadow output이 안전하게 기록되는지

## 현재 schema로 직접 증명할 수 없는 것

first blocker가 이미 발생한 뒤의 downstream secondary failures는 직접 드러나지 않는다.

즉 per-event 기준으로 다음을 직접 답할 수 없다.

- EMA도 같이 실패했는지
- breakout confirmation도 같이 실패했는지
- VWAP distance도 같이 실패했는지
- 여러 downstream failure가 같은 event에 동시에 있었는지

## 왜 EMA secondary tracking이 필요한가

현재 shadow data에서 `ema_fast_not_above_slow`는 의미 있는 first blocker다.

하지만 volatility-blocked event 안에서:

- volatility를 풀었을 때도 EMA가 계속 실패하는지

를 알 수 없다.

그래서 volatility-only relaxation을 안전하게 평가할 수 없다.

## 왜 breakout confirmation secondary tracking이 필요한가

현재 shadow data는 `breakout_not_confirmed`도 의미 있는 first blocker임을 보여준다.

하지만 volatility-blocked subset 안에서:

- volatility relaxation 이후 breakout confirmation에서 다시 무너지는지

를 알 수 없다.

## 왜 VWAP / Band / Volume boolean trace가 여전히 필요한가

현재 numeric field는 도움은 되지만, live code path의 정확한 pass/fail trace를 그대로 보존하지는 못한다.

예:

- `band_expansion_ratio`는 볼 수 있지만
- 그 event가 더 앞선 gate에서 이미 실패했는지는 암묵적이다

## 현재 limitation verdict

`schema expansion required before further tuning decisions`

## 링크

- CNT v2 BREAKOUT V2 GATE REDUNDANCY REVIEW KO
- CNT v2 BREAKOUT V2 SHADOW RUNTIME IMPLEMENTATION KO
- CNT v2 BREAKOUT V2 SHADOW SCHEMA EXPANSION PLAN KO

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN KO]]


