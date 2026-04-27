---
tags:
  - cnt
  - type/documentation
  - status/active
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - status/completed
---

# CNT v2 BREAKOUT V3 Setup 병목 분리 보고서

## 목적

현재 `breakout_v3`의 setup 병목을 감이 아니라 수치와 trace로 공식 고정한다.

## 소스

- `data/shadow_breakout_v3_snapshot.json`
- `logs/shadow_breakout_v3.jsonl`
- `reports/breakout_v3_setup_bottleneck_report.md`
- `reports/breakout_v3_allowed_trace.json`
- `reports/breakout_v3_setup_pass_blocked_trace.json`

## 핵심 사실

| 항목 | 값 |
|---|---:|
| total_signal_count | 42 |
| allowed_signal_count | 2 |
| allowed_signal_ratio | 0.047619 |
| setup_pass_count | 4 |
| setup_fail_count | 38 |
| setup_pass_blocked_trace_count | 3 |
| allowed_trace_count | 2 |

## 단계 해석

- `regime_pass = 24 / 42`
- `setup_pass = 4 / 42`
- `trigger_pass = 11 / 42`
- `quality_pass = 12 / 42`

현재 주된 병목은 `trigger`가 아니라 `setup`이다.

## Setup 병목 초점

### Setup Stage 내부 실패 수

| 조건 | count |
|---|---:|
| setup_not_ready | 38 |
| volatility_floor_fail | 29 |
| price_position_fail | 21 |

### 요청된 병목 키 기준

| 조건 | count |
|---|---:|
| vwap_distance_fail | 35 |
| band_width_fail | 34 |
| volume_fail | 33 |
| band_expansion_fail | 31 |
| setup_not_ready | 19 |

## Allowed Trace 해석

allowed trace 수는 아직 activation 판단에 충분하지 않다.

이 값이 증명하는 것:
- `breakout_v3`는 죽은 전략이 아님
- 매우 좁은 구간에서는 hard/soft 조건을 통과할 수 있음

이 값이 아직 증명하지 못하는 것:
- 반복 가능한 edge
- activation readiness
- tuning readiness

## Setup Pass But Blocked 해석

`setup_pass = 4`인데 `allowed = 2`다.

즉 setup 병목이 매우 강하고, setup을 통과한 뒤에도 추가 차단 사례가 남아 있어서 trace 검토가 필요하다는 뜻이다.

## 최종 판정

`breakout_v3`는 부분적으로 살아 있지만, 현재 구조는 여전히 좁은 setup 계층 병목에 강하게 제한되어 있다. 따라서 다음 유효 단계는 activation도 tuning도 아니고, setup bottleneck isolation이다.

## 공식 상태 고정

```text
FINAL_JUDGEMENT = PARTIALLY_ALIVE_BUT_SETUP_CONSTRAINED
ACTIVATION_READY = NO
TUNING_READY = NO
NEXT_PHASE = CONTINUE_SETUP_BOTTLENECK_ISOLATION
```

## 다음 필수 단계

- `breakout_v3 = SHADOW_ONLY` 유지
- `activation = FORBIDDEN` 유지
- `tuning = FORBIDDEN` 유지
- redesign 논의 전까지 setup 계층 압력을 trace 기반으로 분리 해석

## Obsidian Links

- [[CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW KO]]
- [[CNT v2 DASHBOARD SETUP BOTTLENECK ISOLATION UPGRADE REPORT KO]]
