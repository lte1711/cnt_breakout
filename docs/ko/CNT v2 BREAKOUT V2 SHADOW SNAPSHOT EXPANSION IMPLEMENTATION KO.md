---
tags:
  - cnt
  - breakout
  - shadow
  - snapshot
aliases:
  - CNT v2 BREAKOUT V2 SHADOW SNAPSHOT EXPANSION IMPLEMENTATION KO
---

# CNT v2 BREAKOUT V2 SHADOW SNAPSHOT EXPANSION IMPLEMENTATION KO

## 목적

이 변경은 `data/shadow_breakout_v2_snapshot.json`을 확장해서, 매번 전체 JSONL을 다시 파싱하지 않아도 최신 expanded shadow observation을 snapshot layer에서 직접 읽을 수 있게 만든다.

## 추가된 필드

기존 호환성을 깨지 않는 additive 방식으로 다음 필드가 추가됐다.

- `expanded_event_count`
- `secondary_fail_distribution`
- `stage_false_counts`

## 추가 이유

이전 snapshot은 다음에는 충분했다.

- total signal count
- allowed vs filtered count
- first-blocker distribution

하지만 다음에는 부족했다.

- downstream blocker inspection
- expanded-schema observation review
- stage-level failure pattern의 빠른 operator review

## backward compatibility

기존 필드는 그대로 유지된다.

- `signal_count`
- `filtered_signal_count`
- `allowed_signal_count`
- `filtered_signal_ratio`
- `allowed_signal_ratio`
- `hypothetical_trades_count`
- `reason_distribution`
- `last_updated`

## aggregation rules

- `expanded_event_count`
  - shadow event에 다음이 있을 때만 증가
    - `secondary_fail_reasons`
    - `evaluated_stage_trace`
    - `stage_flags`
- `secondary_fail_distribution`
  - `secondary_fail_reasons`의 downstream fail reason count
- `stage_false_counts`
  - `stage_flags` 중 값이 `false`인 항목 count

## safety

- execution path 변경 없음
- `ACTIVE_STRATEGIES` 변경 없음
- `breakout_v2` activation 없음
- tuning / gate relaxation 없음

## 알려진 한계

이 snapshot은 아직 hypothetical expectancy / profit factor를 shadow event lifecycle에서 계산하지 않는다. observability layer이지, 단독 promotion-decision engine은 아니다.
