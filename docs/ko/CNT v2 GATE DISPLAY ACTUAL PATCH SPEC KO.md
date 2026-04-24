---
aliases:
  - CNT v2 GATE DISPLAY ACTUAL PATCH SPEC KO
---

# CNT v2 gate display 실제 패치 명세

## 비교 파일

- `src/validation/live_gate_evaluator.py`
- `docs/cnt_operations_dashboard.html`

## Evaluator 실제 규칙

현재 evaluator는 실제로 아래 순서를 사용한다.

1. `closed_trades >= 20`
2. `expectancy > 0`
3. `net_pnl > 0`
4. `max_consecutive_losses <= 5`
5. 아래 중 하나의 observed risk guard trigger 존재
   - `LOSS_COOLDOWN`
   - `DAILY_LOSS_LIMIT`

## Dashboard 현재 표시 규칙

현재 dashboard는 다음을 암시한다.

- `closed trades >= 20`
- `PF >= 1.1`
- `expectancy > 0`

또한 fallback 함수 `gateReady(snapshot)`도 아래를 사용한다.

- `profit_factor >= 1.1`

이건 stale 상태다.

## 제거해야 할 정확한 stale 항목

### Visible Rule Text에서 제거

현재 operator-facing rule text에 포함된 아래 항목 삭제:

- `PF >= 1.1`

### Dashboard Fallback Logic에서 제거

아래 함수에서 `profit_factor >= 1.1` 조건 삭제:

- `function gateReady(snapshot)`
- `function gateReasons(snapshot)`

## 최종 단일 truth source

Evaluator logic을 유일한 유효 정책 소스로 채택한다.

Dashboard는 gate state를 아래 파일 기준으로 표시해야 한다.

- `live_gate_decision.json`

Dashboard의 gate 설명도 evaluator criteria만 사용해야 한다.

## 최종 operator-facing 문구

### Gate Rule Text

현재 rule text를 아래로 교체:

- `closed trades >= 20 | expectancy > 0 | net pnl > 0 | max consecutive losses <= 5 | risk guard observed`

### Gate Explanation Text

권장 문구:

- `Gate status is read from live_gate_decision.json. Runtime status must follow evaluator output, not dashboard fallback heuristics.`

### Fail Reason Text

Fail 발생 시 우선 사용:

- `Current fail reason: NON_POSITIVE_EXPECTANCY`

## Fallback 유지 여부

Fallback은 `live_gate_decision.json`을 로드하지 못할 때의 방어용 last resort로만 남길 수 있다.

단, fallback이 남는다면:

- evaluator policy를 정확히 복제해야 함
- 별도 PF threshold를 사용하면 안 됨

## 추가 UI 정리

추가 패치:

- footer의 깨진 separator character 정리

권장 footer text:

- `CNT runtime sources: snapshot | metrics | state | live gate`

## 패치 수용 기준

1. dashboard visible gate text가 evaluator logic과 일치
2. fallback logic이 더 이상 `PF >= 1.1`을 도입하지 않음
3. displayed fail reason은 계속 `live_gate_decision.json`에서 읽음
4. operator-facing wording이 net PnL과 risk guard requirement를 설명

## 필수 결론

**gate/display actual patch ready**

## Obsidian Links

- [[CNT v2 DASHBOARD PATCH TARGET MAPPING KO]]


