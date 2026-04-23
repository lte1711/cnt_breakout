---
tags:
  - cnt
  - docs
  - patch
  - shadow
  - state
  - v2
  - ko
aliases:
  - CNT v2 SHADOW SEMANTICS AND PORTFOLIO STATE PATCH REPORT KO
---

# CNT v2 shadow 의미 일관성 및 portfolio state 패치 보고서

## 요약

이번 패치는 live strategy activation을 바꾸지 않고도 안전하게 수정 가능한 두 가지 runtime 정합성 문제를 다룹니다.

수정된 항목:

- `breakout_v3` shadow event 의미 일관성
- `portfolio_state` rebuild 시 risk counter 보존

변경하지 않은 항목:

- `ACTIVE_STRATEGIES`
- 주문 경로
- live activation policy
- `breakout_v1` active 상태

## 1. Breakout V3 Shadow 의미 일관성 수정

관찰된 결함:

- `allowed=true` 이벤트에도 `first_blocker`가 남을 수 있었음
- `summary_reason`은 `trigger_blocked`인데 실제 첫 blocker는 `setup` 단계에서 나오는 경우가 있었음

적용한 수정:

- 허용된 이벤트는 이제 `first_blocker`, `hard_blocker`가 모두 `null`
- `summary_reason`은 최초 실패 stage 순서를 따르도록 정렬
  - `regime_blocked`
  - `setup_blocked`
  - `trigger_blocked`
  - `hard_pass_but_soft_count_insufficient`

해석:

- evaluator 수준에서 shadow event의 내부 의미 일관성이 맞춰짐
- 다만 과거 로그는 과거 로그이므로, post-fix 순수 기준선으로 해석하면 안 됨

## 2. Portfolio State Risk Counter 보존

관찰된 결함:

- `build_portfolio_state()`는 runtime state를 바탕으로 `portfolio_state.json`을 재구성하지만
- 이 과정에서 `daily_loss_count`, `consecutive_losses`가 0으로 떨어질 수 있었음

적용한 수정:

- rebuild 시 `runtime_state["risk_metrics"]`에서 risk counter를 복사
- 이 동작은
  - open trade가 없을 때
  - open trade가 있을 때
  모두 적용됨

해석:

- 이제 `portfolio_state.json`이 runtime loss counter 현실과 맞춰짐
- 모니터링과 후속 자동화에서 실제보다 안전하게 읽히는 위험이 줄어듦

## 3. 검증

실행:

```text
PYTHONPATH=. python -m pytest -q
```

결과:

```text
53 passed
```

## 4. 남은 우선순위

이번 패치는 가장 큰 live 성과 문제 자체를 해결하지는 않습니다.

여전히 열려 있는 항목:

- `breakout_v1`는 active 상태이며 음수 성과를 내고 있음

이 문제는 shadow/state 정합성 문제가 아니라 운영 의사결정 문제로 남아 있습니다.

## Obsidian Links

- [[CNT v2 BREAKOUT V3 SHADOW EVALUATOR IMPLEMENTATION REPORT KO]]
- [[CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START KO]]
- [[CNT v2 CURRENT STATUS ASSESSMENT KO]]
- [[00 Docs Index KO|Docs Index KO]]
