---
tags:
  - cnt
  - docs
  - performance
  - report
  - v2
  - ko
aliases:
  - CNT v2 TESTNET PERFORMANCE REPORT KO
---

# CNT v2 TESTNET 성능 보고서

```text
DOCUMENT_NAME = cnt_v2_testnet_performance_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-24
STATUS        = DATA_COLLECTION_IN_PROGRESS
LAST_UPDATED  = 2026-04-24 04:04:03
```

## 자동 스냅샷

```text
OBSERVATION_WINDOW: up to 2026-04-24 04:04:03
TOTAL_SIGNALS: 1066
TOTAL_SELECTED_SIGNALS: 194
TOTAL_EXECUTED_TRADES: 35
TOTAL_CLOSED_TRADES: 35
CURRENT_OPEN_POSITIONS: 0
WINS: 18
LOSSES: 17
WIN_RATE: 0.5143
AVG_WIN: 0.016800
AVG_LOSS: 0.018479
EXPECTANCY: -0.000335
PROFIT_FACTOR: 0.962647
NET_PNL: -0.011734
MAX_CONSECUTIVE_LOSSES: 3
TOP_STRATEGY: pullback_v1
WORST_STRATEGY: breakout_v1
BLOCKED_REASON_DISTRIBUTION: DAILY_LOSS_LIMIT=159, no_ranked_signal{all_filtered=314, legacy=25}
RISK_TRIGGER_STATS: DAILY_LOSS_LIMIT=318
STRATEGY_BREAKDOWN: breakout_v1: trades_closed=3, wins=1, losses=2, win_rate=0.3333, expectancy=-0.022198, profit_factor=0.172951 | pullback_v1: trades_closed=32, wins=17, losses=15, win_rate=0.5312, expectancy=0.001714, profit_factor=1.234829
SELECTION_LOG_COUNTS: breakout_v1=15, pullback_v1=174
SELECTION_LOG_BASIS: new-format selection-path logs only
NOTES: auto-generated from performance snapshot
```

## 요약 해석

이 시점의 CNT는 표본은 충분히 누적됐지만, 혼합 포트폴리오 기준 성능은 다시 약한 음수 구간에 있다.

핵심 해석:

- 전체 closed trades는 `35`
- 승률은 `0.5143`
- expectancy는 `-0.000335`
- profit factor는 `0.962647`
- net pnl은 `-0.011734`

전략별로 보면:

- `pullback_v1`는 여전히 양수 전략
- `breakout_v1`는 적은 표본에서도 음수 기여

즉 혼합 포트폴리오 성과는 breakout 계열의 약한 품질과 risk block 압력이 함께 반영된 상태다.

## 현재 의미

이 문서는 자동 생성된 성능 스냅샷 문서다.

따라서 현재 상태를 판단할 때는 아래 문서와 함께 읽는 것이 적절하다.

- [[CNT v2 CURRENT STATUS ASSESSMENT KO]]
- [[CNT v2 LIVE READINESS GATE KO]]
- [[CNT v2 POST-READY DEGRADATION REVIEW KO]]

## 링크

- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT v2 TESTNET DATA COLLECTION STATUS REPORT KO]]
- [[CNT v2 PERFORMANCE VALIDATION REPORT KO]]
