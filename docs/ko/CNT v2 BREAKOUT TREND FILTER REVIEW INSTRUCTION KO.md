---
tags:
  - cnt
  - docs
  - breakout
  - instruction
  - v2
aliases:
  - CNT v2 BREAKOUT TREND FILTER REVIEW INSTRUCTION KO
---

# CNT v2 BREAKOUT 추세 필터 리뷰 지시문

```text
DOCUMENT_NAME = cnt_v2_breakout_trend_filter_review_instruction_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = ACTIVE
PURPOSE       = 추가 parameter relaxation 전에 breakout_v1 상위 진입 필터 구조 진단
```

---

# 1. 목표

첫 완화 이후에도 `breakout_v1`가 candidate path에 들어가지 못하는 이유가 ATR / RSI threshold가 아니라 상위 trend-filter 구조에 있는지 리뷰한다.

이 단계는 code patch가 아니라 design review를 만들어야 한다.

---

# 2. 현재 고정 사실

최신 확인된 runtime facts:

* `breakout_v1.signals_generated = 85`
* `breakout_v1.signals_selected = 0`
* `breakout_v1.trades_closed = 0`
* `selected_strategy_counts = {'pullback_v1': 3}`
* selection-path observability는 정상 동작
* breakout은 아직 candidate path에 들어가지 못함

관측된 breakout rejection bottleneck:

* 실험 구간 대부분의 main bottleneck:
  * `market_not_trend_up`
* 이후 보이기 시작한 secondary bottleneck:
  * `volatility_not_high`

---

# 3. 필수 작업

STEP 1

* 아래 파일의 current breakout filter-chain structure를 분석
  * `src/strategies/breakout_v1.py`
* 다음 항목 문서화
  * filter order
  * `market_not_trend_up` 결정 기준
  * `volatility_not_high` 결정 기준
  * 첫 rejection이 결정되는 위치
  * `TREND_UP` 만족 후 병목이 어디로 이동하는지

STEP 2

* trend-filter review design note 작성
* 평가할 내용
  * 현재 `TREND_UP`가 지나치게 엄격한지
  * `RANGE` 안의 breakout candidate를 전부 차단하는 것이 적절한지
  * `TREND_UP -> then LOW volatility fail` 구조가 의도된 동작인지
  * 상위 gate를 계속
    * `strict trend-first`
    * 또는 `trend-or-breakout-setup`
    중 무엇으로 둘 것인지

STEP 3

* 최대 두 개의 change candidate만 제안
  * proposal A = trend-filter relaxation
  * proposal B = filter-order rearrangement

STEP 4

* 예상 영향 문서화
  * false-positive 증가 위험
  * signal-count 증가 위험
  * pullback collision 위험
  * ranker candidate-count 변화
  * testnet에서 새로 관찰할 rejection reason

STEP 5

* 리뷰 보고서 저장 위치
  * `docs/CNT v2 BREAKOUT TREND FILTER REVIEW REPORT.md`

---

# 4. 범위 밖

이 단계에서 허용되지 않는 것:

* `config.py` threshold 추가 변경
* ATR / RSI 2차 완화
* ranker modifications
* engine decomposition
* live-trading decision

---

# 5. 완료 규칙

이 단계는 아래가 모두 충족될 때만 완료다.

* breakout filter chain 문서화 완료
* 로그를 근거로 trend-filter review 필요성 설명 완료
* 최대 두 개의 change option 제안 완료
* 하나의 recommendation 선택 완료
* code 변경 없음

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]
