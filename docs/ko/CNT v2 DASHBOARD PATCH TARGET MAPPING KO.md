---
tags:
  - cnt
  - docs
  - v2
  - dashboard
  - mapping
aliases:
  - CNT v2 DASHBOARD PATCH TARGET MAPPING KO
---

# CNT v2 대시보드 패치 대상 매핑

## 대상 파일

- `docs/cnt_operations_dashboard.html`

## 패치 목표

현재 `FAIL` 상태를 operator가 스크롤 없이 바로 볼 수 있도록, 현시점 degradation signal을 대시보드 상단에 직접 노출한다.

## 패치 위치

### Primary Placement

기존 hero section 안에 **새 top warning strip** 삽입:

- 위치: 현재 `Live Gate`와 `System Health` 카드 바로 아래
- host section: `<section class="hero"> ... </section>`
- 권장 삽입 지점:
  - 현재 `<div class="card">System Health</div>` 뒤
  - 첫 metrics row (`Win Rate / Profit Factor / Expectancy / Net PnL`) 전

### Secondary Placement

기존 `System Health` 카드 안의 `alerts` 컨테이너는 유지한다.

새 top strip은 직접 operator-facing fail / degradation warning 전용으로만 사용한다.

## 데이터 소스

Dashboard가 이미 쓰고 있는 기존 runtime source만 사용:

- `../data/performance_snapshot.json`
- `../data/strategy_metrics.json`
- `../data/state.json`
- `../data/live_gate_decision.json`

이 패치를 위해 새 runtime 파일을 추가하면 안 된다.

## 필수 경고 조건

### 1. FAIL Reason

소스:

- `live_gate_decision.status`
- `live_gate_decision.reason`

조건:

- `status === "FAIL"`

표시 문구:

- title: `LIVE GATE FAIL`
- body: `reason = NON_POSITIVE_EXPECTANCY`

실제 reason string은 반드시 `live_gate_decision.json`에서 직접 읽어야 한다.

### 2. Expectancy Below Zero

소스:

- `performance_snapshot.expectancy`

조건:

- `expectancy <= 0`

표시 문구:

- title: `EXPECTANCY BELOW ZERO`
- body: `current expectancy = {value}`

### 3. Net PnL Below Zero

소스:

- `performance_snapshot.net_pnl`

조건:

- `net_pnl < 0`

표시 문구:

- title: `NET PNL BELOW ZERO`
- body: `current net pnl = {value}`

### 4. Profit Factor Below One

소스:

- `performance_snapshot.profit_factor`

조건:

- `profit_factor < 1`

표시 문구:

- title: `PF BELOW 1`
- body: `current PF = {value}`

### 5. Daily Loss Count Reached

소스:

- `state.risk_metrics.daily_loss_count`

조건:

- `daily_loss_count >= 3`

표시 문구:

- title: `DAILY LOSS COUNT REACHED`
- body: `daily_loss_count = 3`

중요:

- 이건 cumulative `DAILY_LOSS_LIMIT` runtime hit와 다름
- 둘 다 표시한다면 별도 개념으로 분리해야 함

### 6. Breakout Negative Expectancy

소스:

- `strategy_metrics.breakout_v1.expectancy`
- `strategy_metrics.breakout_v1.profit_factor`
- `strategy_metrics.breakout_v1.trades_closed`

조건:

- `breakout_v1.expectancy < 0`

표시 문구:

- title: `BREAKOUT NEGATIVE EXPECTANCY`
- body: `expectancy = {value}, PF = {value}, trades_closed = {value}`

## 심각도 매핑

- `FAIL reason`
  - severity = `bad`
- `expectancy < 0`
  - severity = `bad`
- `net_pnl < 0`
  - severity = `bad`
- `PF < 1`
  - severity = `bad`
- `daily_loss_count reached`
  - severity = `warn`
- `breakout negative expectancy`
  - severity = `warn`

## 표시 우선순위

Top strip 순서:

1. `LIVE GATE FAIL`
2. `EXPECTANCY BELOW ZERO`
3. `NET PNL BELOW ZERO`
4. `PF BELOW 1`
5. `BREAKOUT NEGATIVE EXPECTANCY`
6. `DAILY LOSS COUNT REACHED`

## 비목표

이 패치는 다음을 해서는 안 된다.

- evaluator logic 변경
- runtime JSON schema 변경
- 기존 lower-priority alert 숨기기

## 필수 결론

**dashboard patch spec ready**

## Obsidian Links

- [[CNT v2 GATE DISPLAY ACTUAL PATCH SPEC]]
- [[CNT v2 BREAKOUT ISOLATION OBSERVATION WINDOW SPEC]]
- [[00 Docs Index|Docs Index]]
