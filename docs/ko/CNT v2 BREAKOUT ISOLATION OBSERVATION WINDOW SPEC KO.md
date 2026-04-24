---
tags:
  - cnt
  - docs
  - v2
  - breakout
  - isolation
aliases:
  - CNT v2 BREAKOUT ISOLATION OBSERVATION WINDOW SPEC KO
---

# CNT v2 BREAKOUT 격리 관측 창 명세

## 목적

이 명세는 breakout 격리 진단을 위한 관측 창을 정의한다.

이 문서는 breakout을 즉시 비활성화하는 문서가 아니다.  
이 문서는 breakout 품질을 mixed portfolio 품질과 분리해서 어떻게 읽을지 정의한다.

## 관측 창

- duration basis: `20 to 30 additional runtime cycles`
- review mode: fact-based observation only
- parameter changes: frozen during this window

## 최소 표본 요구

Breakout 전용 관측은 아래 조건 전까지 과장해서 해석하면 안 된다.

- `breakout_v1 trades_closed >= 5`

그 전까지는:

- breakout 품질은 low-sample observed quality라고만 표현해야 한다

## 창 중간 체크포인트

두 개의 체크포인트를 사용한다.

1. midpoint review
   - `10 additional cycles` 이후
2. final review
   - `20 to 30 additional cycles` 이후

## 필수 비교 축

항상 아래 세 기준선을 분리해서 비교한다.

1. `mixed portfolio`
2. `breakout observed baseline`
3. `pullback inferred baseline`

## 필수 지표

각 리뷰마다 아래 항목을 모두 추적한다.

- `expectancy`
- `profit_factor`
- `execution_rate`
- `execution_block_rate`
- `no_candidate_rate`

필요한 경우 아래도 포함한다.

- `trades_closed`
- `wins`
- `losses`
- `net_pnl`

## 비교 표 형식

| Baseline | Closed Trades | Expectancy | PF | Net PnL | Execution Rate | Execution Block Rate | No Candidate Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Mixed | ... | ... | ... | ... | ... | ... | ... |
| Breakout observed | ... | ... | ... | ... | ... | ... | ... |
| Pullback inferred | ... | ... | ... | ... | ... | ... | ... |

## 종료 조건

### Exit 1 - Breakout Quality Recover

다음 조건이면 사용한다.

- breakout expectancy가 양수로 전환
- breakout PF가 1 이상으로 상승
- 추가 관측 거래가 그 개선을 지지

### Exit 2 - Breakout Remains Negative

다음 조건이면 사용한다.

- breakout expectancy가 계속 음수
- breakout PF가 계속 1 미만
- 추가 표본 이후에도 음수 기여 지속

### Exit 3 - Insufficient Sample

다음 조건이면 사용한다.

- breakout closed trades가 여전히 너무 적어서 더 강한 주장 불가

## 필수 가드레일

- no immediate breakout disable
- no risk guard loosening
- no large parameter tuning before the window completes

## 과장 금지

아래 표현은 금지한다.

- inferred pullback baseline을 observed baseline으로 부르기
- 현재 `3-trade sample`만으로 breakout이 영구적으로 무효라고 단정하기
- positive breakout trade 1건만으로 recovery를 주장하기

## 권장 리뷰 문장

아래 같은 표현을 권장한다.

- `breakout remains under isolated observation and has not yet earned an operating-quality conclusion beyond the current observed sample`

## 필수 결론

**breakout isolation window ready**

## Obsidian Links

- [[CNT v2 BREAKOUT LAST 3 TRADES REVIEW]]
- [[CNT v2 STRATEGY ISOLATION COMPARISON]]
- [[00 Docs Index|Docs Index]]
