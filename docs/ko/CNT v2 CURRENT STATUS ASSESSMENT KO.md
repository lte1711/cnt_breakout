---
aliases:
  - CNT v2 CURRENT STATUS ASSESSMENT KO
---

# CNT v2 현재 상태 평가

```text
DOCUMENT_NAME = cnt_v2_current_status_assessment_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-22
STATUS        = LIVE_READY_POST_READINESS_BASELINE
LAST_UPDATED  = 2026-04-22 02:44:03
REFERENCE_1   = CNT v2 TESTNET PERFORMANCE REPORT
REFERENCE_2   = CNT v2 LIVE READINESS GATE
REFERENCE_3   = CNT v2 LIVE GATE ALIGNMENT REPORT
REFERENCE_4   = CNT v2 LIVE READY POST-READINESS MONITORING PLAN
```

## 1. 현재 검증된 상태

당시 저장소 상태와 runtime evidence 기준:

- assessment 시점 latest code baseline = `8718981`
- market mode = `BINANCE_SPOT_TESTNET`
- engine mode = `ONE_SHOT`
- scheduler rhythm = `10 minutes`
- current state 포함 항목:
  - `pending SELL TARGET = present`
  - `open_trade = present`
  - `strategy_name = pullback_v1`
- last action = `SELL_SUBMITTED`
- live gate = `LIVE_READY / ALL_GATES_PASSED`

## 2. 성능 상태

당시 testnet performance snapshot:

- total signals = `558`
- selected signals = `62`
- executed trades = `22`
- closed trades = `21`
- wins = `12`
- losses = `9`
- win rate = `0.5714`
- expectancy = `0.001319`
- net pnl = `0.027703`
- profit factor = `1.1969`
- max consecutive losses = `2`

해석:

- CNT는 최소 readiness gate를 넘어 post-readiness stabilization 단계에 들어갔다
- 전략 성과는 여전히 양수지만, 초기 최적 스냅샷보다 품질은 약해졌다
- `LIVE_READY`에도 불구하고 throughput은 제한적이다

## 3. 전략 상태

## pullback_v1

- `signals_generated = 279`
- `signals_selected = 57`
- `trades_closed = 19`
- 실질적인 현재 운영 전략
- 양수 testnet evidence:
  - `win_rate = 0.5789`
  - `profit_factor = 1.1915`
  - `expectancy > 0`
  - `net_pnl > 0`

## breakout_v1

- `signals_generated = 279`
- `signals_selected = 5`
- `trades_closed = 2`
- 더 이상 dead branch는 아님
- 첫 real trade lifecycle은 검증됨
- 현재 단계는 activation verification이 아니라 low-sample quality observation

해석:

- strategy selection path는 작동 중
- ranker도 동작하지만, 현재의 주된 병목은 아님
- breakout은 aggregate sample 기준으로 여전히 upstream gating에 크게 묶여 있다
- `selected_strategy_counts`는 전체 historical selected signals가 아니라 new-format selection-path logs만 반영하므로 주의가 필요하다
- candidate recovery와 gate alignment 수정은 적용 및 검증되었지만, throughput은 execution block과 no-candidate cycle 때문에 제한적이다

## 4. 현재 병목 해석

현재 동작은 아래처럼 해석해야 한다.

- `LIVE_READY`는 true지만 throughput은 아직 강하지 않다
- measured post-readiness baseline:
  - `selection_rate = 62 / 558 = 11.11%`
  - `execution_rate = 22 / 62 = 35.48%`
  - `no_ranked_signal_total = 217`
- 현재 controlled bottleneck split:
  - primary = observed risk guard activity에 따른 execution blocking
  - secondary = no-candidate / no-ranked-signal cycles
- breakout은 살아 있지만 여전히 low-sample
- pullback은 여전히 주된 운영 증거원

## 5. 현재 운영 방향

올바른 현재 작업 순서:

1. 현재 `LIVE_READY` snapshot을 operating baseline으로 고정
2. parameter change 없이 post-readiness sample을 계속 수집
3. 아래 추적:
   - `selection_rate`
   - `execution_rate`
   - `no_ranked_signal`
   - `strategy_split`
   - `LIVE_READY` persistence
4. `pullback_v1`와 `breakout_v1` 품질 평가는 분리
5. post-readiness evidence가 `20 to 30 additional cycles` 쌓인 뒤에만 다음 변경 검토

현재 권장되지 않는 것:

- 추가 filter loosening
- risk guard loosening
- ranker retuning
- symbol expansion
- multi-position expansion

## 6. 최종 결론

CNT는 더 이상 설계 전용 저장소가 아니다.

현재 CNT는:

- Binance Spot Testnet에서 실제로 동작하는 운영 시스템
- active runtime evidence 보유
- `LIVE_READY` gate alignment 복구 완료
- 의미 있는 pullback 양수 증거 확보
- breakout 품질 평가는 계속 진행 중
- 현시점의 초점은 새 최적화가 아니라 post-readiness stabilization

한 줄 결론:

**CNT는 사실 기반 게이트 결정으로 `LIVE_READY` 상태에 도달했지만, post-readiness 운영 품질은 여전히 낮은 throughput과 no-candidate cycle의 영향을 받고 있으므로, 다음 올바른 단계는 새 튜닝이 아니라 안정화와 baseline 지속성 모니터링이다.**

## 링크

- CNT v2 CURRENT STATUS ASSESSMENT
- CNT v2 LIVE READINESS GATE KO
- CNT v2 LIVE GATE ALIGNMENT REPORT KO
- CNT v2 LIVE READY POST-READINESS MONITORING PLAN KO

## Obsidian Links

- [[CNT v2 LIVE READINESS GATE KO]]


