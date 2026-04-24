---
tags:
  - cnt
  - breakout
  - shadow
  - verification
---

# CNT v2 BREAKOUT V2 SHADOW RUNTIME VERIFICATION KO

## 검증 범위

이 문서는 구현된 `breakout_v2` shadow runtime에 대한 one-shot runtime verification을 기록한다.

검증 목표:

- shadow 파일 생성/갱신 확인
- one-shot engine cycle 정상 종료 확인
- live execution path 변경 없음 확인

## runtime 시각

- verification run timestamp: `2026-04-22 15:21:04`
- entry chain: `run.ps1 -> main.py -> src.engine.start_engine`

## pre-run baseline

### shadow files

- `logs/shadow_breakout_v2.jsonl` existed
- pre-run log line count: `1`
- `data/shadow_breakout_v2_snapshot.json` existed
- pre-run snapshot `signal_count = 1`

### live runtime state

- `pending_order = null`
- `open_trade = null`
- `action = EXECUTION_BLOCKED_BY_RISK`
- `risk_metrics.daily_loss_count = 3`
- `risk_metrics.consecutive_losses = 2`

## post-run 결과

### file update result

- `logs/shadow_breakout_v2.jsonl` update: `PASS`
- `data/shadow_breakout_v2_snapshot.json` update: `PASS`
- one-shot runtime finish: `PASS`

### shadow jsonl sample

최신 append event는 `entry_allowed = false`, `filter_reason = ema_fast_not_above_slow`로 기록됐다.

### shadow snapshot sample

핵심 값:

- `signal_count = 2`
- `filtered_signal_count = 2`
- `allowed_signal_count = 0`
- `filtered_signal_ratio = 1.0`
- `allowed_signal_ratio = 0.0`
- `reason_distribution.ema_fast_not_above_slow = 2`

## execution path unchanged confirmation

관찰된 live runtime은 기존 production branch에 그대로 남아 있었다.

- selected strategy in portfolio log: `pullback_v1`
- runtime result: `EXECUTION_BLOCKED_BY_RISK`
- reason: `DAILY_LOSS_LIMIT`
- `pending_order = null`
- `open_trade = null`

즉 `breakout_v2`가 다음으로 들어간 흔적은 없다.

- execution decision
- order submission
- pending order state
- open trade state

## sanity checks

- jsonl append count: `1 -> 2`
- snapshot `signal_count`: `1 -> 2`
- `reason_distribution` 정상 기록
- `last_updated` 정상 기록

## 알려진 한계

- `hypothetical_expectancy` lifecycle-derived 아님
- `hypothetical_profit_factor` lifecycle-derived 아님
- `stop_exit_ratio` lifecycle-derived 아님
- 현재 검증은 profitability가 아니라 runtime integration을 확인한 것

## 최종 판정

`breakout_v2` shadow runtime은 안전하게 통합되었고, production execution은 바뀌지 않았다.

## 링크

- [[CNT v2 BREAKOUT V2 SHADOW RUNTIME IMPLEMENTATION KO]]
- [[CNT v2 BREAKOUT V2 SHADOW RUNTIME INTEGRATION KO]]
