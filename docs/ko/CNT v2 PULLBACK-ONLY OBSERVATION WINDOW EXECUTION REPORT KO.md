---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - type/analysis
  - type/validation
  - status/final
  - language:-ko
---

# CNT v2 PULLBACK-ONLY OBSERVATION WINDOW EXECUTION REPORT

## 목적

이 보고서는 `9a29d34` 기준선 이후 다음 단계 지시를 실제로 실행한 결과를 기록한다.

- live active runtime set은 `pullback_v1` 단독
- `breakout_v1`는 active runtime에서 격리
- `breakout_v3`는 shadow-only 유지
- observation window 동안 threshold 및 execution path 튜닝 금지

## 수행한 검증

### 테스트 검증

- `PYTHONPATH=. python -m pytest -q`
- 결과: `56 passed`

### 컴파일 검증

- `python -m py_compile config.py src\shadow\breakout_v3_shadow_eval.py src\state\state_manager.py`
- 결과: `OK`

### 런타임 검증

- `run.ps1`로 entry chain 실행
- execution path regression 없음

## 실행 후 런타임 상태

`data/state.json` 기준:

- `strategy_name = pullback_v1`
- `action = NO_ENTRY_SIGNAL`
- `last_run_time = 2026-04-24 07:14:00`

즉 현재 live active runtime strategy는 `pullback_v1`로 유지된다.

## Portfolio Risk 정합성

`data/state.json`과 `data/portfolio_state.json` 기준:

- `daily_loss_count = 3`
- `consecutive_losses = 3`

두 상태 파일의 risk counter는 계속 동기화되어 있다.

## Live Runtime 관찰

active-set isolation 이후 최신 runtime log는 다음처럼 기록됐다.

- `2026-04-24 06:50:10` -> `strategy_name=pullback_v1`
- `2026-04-24 06:54:00` -> `strategy_name=pullback_v1`
- `2026-04-24 07:04:00` -> `strategy_name=pullback_v1`
- `2026-04-24 07:14:00` -> `strategy_name=pullback_v1`

같은 로그 파일 안에 과거 `breakout_v1` 기록은 남아 있지만,
격리 이후 새 runtime action에서 `breakout_v1`가 다시 active selected strategy로 기록되지는 않았다.

## Signal 관찰

pullback-only window에서 최신으로 추가된 signal log는 다음이었다.

- `pullback_v1 / NO_SETUP / pullback_rsi_not_in_range`
- `pullback_v1 / PULLBACK / trend_pullback_reentry_relaxed_rsi`
- `pullback_v1 / PULLBACK / near_trend_pullback_reentry`
- `pullback_v1 / NO_SETUP / trend_not_up`

이번 보고 구간에서는 `breakout_v1` 신규 signal line이 추가되지 않았다.

## Breakout V3 Shadow 관찰

보고 시점의 `data/shadow_breakout_v3_snapshot.json`:

- `signal_count = 8`
- `allowed_signal_count = 0`
- `allowed_signal_ratio = 0.0`

### First blocker 분포

- `setup_not_ready = 5`
- `breakout_not_confirmed = 3`

### Soft pass count 분포

- `1 -> 1`
- `2 -> 2`
- `3 -> 2`
- `4 -> 3`

### Stage 집계

- `stage_pass_counts`
  - `regime = 8`
  - `setup = 3`
  - `trigger = 2`
  - `quality = 5`
- `stage_fail_counts`
  - `setup = 5`
  - `trigger = 6`
  - `quality = 3`

## Shadow Semantic 정합성

현재 post-fix shadow log 기준 검사 결과:

- `allowed=true with blocker = 0`
- `summary_reason / hard_blocker conflict = 0`
- `trend_not_up first_blocker = 0`
- `range_without_upward_bias first_blocker = 0`

즉 현재 shadow observation 데이터는 수정된 evaluator 의미 규칙을 계속 유지하고 있다.

## Live Gate 상태

`data/live_gate_decision.json`는 아직:

- `status = FAIL`
- `reason = NON_POSITIVE_EXPECTANCY`

짧은 관측 구간에서는 아직 이 값이 개선되지 않았다.

## 해석

이번 실행으로 확인된 사실은 다음과 같다.

1. `pullback_v1`는 여전히 유일한 active runtime strategy다.
2. portfolio risk counter 동기화는 계속 유지된다.
3. `breakout_v3` shadow output은 semantic clean 상태를 유지한다.
4. shadow observation window는 정상적인 post-fix 데이터로 누적 중이다.
5. Live Gate는 과거 음수 오염 이력이 아직 반영되어 있으므로, post-isolation 성과 결론을 내리기에는 관측 시간이 더 필요하다.

## Review Threshold 상태

다음 정식 review threshold는 아직 도달하지 않았다.

현재 상태:

- `shadow_breakout_v3_snapshot.signal_count = 8`
- review threshold = `>= 20`

## 다음 조치

다음까지 계속 유지해야 할 것은:

- `breakout_v1` 재활성화 금지
- `breakout_v3` live activation 금지
- threshold 변경 금지
- interval 변경 금지
- execution path 변경 금지

다음 정식 review는 아래 중 하나일 때 수행한다.

- `shadow_breakout_v3_snapshot.signal_count >= 20`
- semantic conflict 재발
- 예상 밖의 live runtime behavior 발생

## 결론

이번 next-stage execution instruction은 정상적으로 적용됐다.

현재 CNT 상태는 다음처럼 정리된다.

- live active runtime = `pullback_v1` 단독
- `breakout_v3` = shadow-only
- shadow semantics = clean
- portfolio risk sync = 유지
- Live Gate = 아직 음수, 추가 post-isolation observation 필요

## Obsidian Links

- [[CNT v2 LIVE READINESS GATE KO]]


