---
aliases:
  - CNT v2 GATE DISPLAY CONSISTENCY AUDIT KO
---

# CNT v2 gate display 정합성 감사

## 범위

비교 파일:

- `src/validation/live_gate_evaluator.py`
- `docs/cnt_operations_dashboard.html`

## Evaluator 규칙

`live_gate_evaluator.py`는 현재 아래 순서로 평가한다.

1. `closed_trades >= 50`
2. `expectancy > 0`
3. `net_pnl > 0`
4. `max_consecutive_losses <= 5`
5. 아래 중 하나의 observed risk guard trigger 존재
   - `LOSS_COOLDOWN`
   - `DAILY_LOSS_LIMIT`

실제 evaluator에는 **PF threshold가 없다.**

## Dashboard Gate Rule Text

현재 dashboard는 아래 gate rule text를 보여준다.

- `closed trades >= 20 | PF >= 1.1 | expectancy > 0`

그리고 fallback `gateReady(snapshot)` 함수도 아래를 사용한다.

- `closed_trades >= 50`
- `profit_factor >= 1.1`
- `expectancy > 0`

## Displayed Fail Reason Source

Dashboard는 이 부분은 올바르게 동작한다.

- `gateStatus = gate?.status ?? ...`
- `gateReason = gate?.reason ?? ...`

즉 `live_gate_decision.json`이 존재하면, 표시되는 fail reason은 dashboard fallback text가 아니라 evaluator output에서 온다.

## 확인된 불일치

### 1. PF Threshold Inconsistency

확인됨.

- evaluator는 `PF >= 1.1`을 요구하지 않음
- dashboard fallback과 gate text는 아직 요구하는 것처럼 보임

### 2. Net PnL Visibility Gap

확인됨.

- evaluator는 `net_pnl <= 0`이면 FAIL
- dashboard gate rule text에는 net PnL이 아예 언급되지 않음

### 3. Display Source Is Mostly Correct

이 부분도 확인됨.

- `live_gate_decision.json`이 로드되면 fail status와 fail reason은 올바르게 표시됨
- 다만 operator가 보는 rule explanation은 여전히 실제 evaluator와 맞지 않음

### 4. Additional Display Quality Issue

Dashboard footer에는 아직 runtime source line에 깨진 separator character가 남아 있다.

이건 핵심 논리 불일치는 아니지만, 남아 있는 UI 품질 결함이다.

## 감사 결과

현재 상황:

- evaluator logic = 현재 정책 기준으로 올바름
- dashboard status source = 대체로 올바름
- dashboard rule explanation = stale / inconsistent

## 필수 결론

**gate/display consistency patch required**

## Obsidian Links

- [[CNT v2 POST-READY DEGRADATION REVIEW KO]]


