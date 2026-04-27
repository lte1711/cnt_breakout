---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - context-filter
  - type/validation
  - offline-experiment
  - type/operation
  - strategy/breakout_v3
  - type/analysis
  - cnt-v2-fresh-cycle-observability-validation-report-ko
---

# CNT v2 fresh cycle 관측성 검증 보고

```text
DOCUMENT_NAME = cnt_v2_fresh_cycle_observability_validation_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = PASS
REFERENCE_1   = CNT v2 OBSERVABILITY VALIDATION GATE
REFERENCE_2   = CNT v2 FRESH CYCLE OBSERVABILITY VALIDATION PLAN
```

---

# 1. 요약

Fresh-cycle observability validation은 실제로 실행됐고 PASS했다.

새 observability format은 이제 live runtime output 안에서 확인된 상태다.

이 결과는 first breakout relaxation experiment를 진행할 수 있는 gate를 열어 준다.

---

# 2. 검증 증거

`logs/portfolio.log`에서 포착된 fresh runtime evidence:

```text
[2026-04-20 00:32:46] symbol=ETHUSDT selected_strategy=NONE reason=no_ranked_signal rank_score=0.0 rank_score_components={} blocked_by_policy=no_ranked_signal blocked_detail=all_filtered total_signals=2 candidate_count=0 rejected_reasons={'market_not_trend_up': 1, 'trend_not_up': 1}
```

확인된 필드:

* `blocked_detail=all_filtered`
* `candidate_count=0`
* `rejected_reasons={'market_not_trend_up': 1, 'trend_not_up': 1}`

메모:

* `selection_reason=highest_score`와 `rank_candidates=...`는, 유효한 new-format runtime line 1개가 확보되면 PASS에 필수는 아니다

---

# 3. Snapshot 확인

갱신된 `data/performance_snapshot.json`은 mixed-format aggregation을 정상 반영한다.

```text
blocked_signal_stats.no_ranked_signal = {all_filtered=1, legacy=25}
```

해석:

* legacy portfolio log도 계속 반영됨
* new-format blocked-detail runtime line도 함께 반영됨
* mixed log stream 때문에 snapshot generation이 깨지지 않았음

---

# 4. 테스트 확인

실행:

```text
python -m unittest discover -s tests -p "test_*.py"
```

결과:

```text
Ran 16 tests
OK
```

---

# 5. 운영 메모

반복 manual launch 중 한 번은 성공했고, 추가 병렬 manual call에서는 `scheduler_skip`을 쓰는 중 scheduler log write collision이 발생했다.

관측 이슈:

* `logs/scheduler_stdout.log`는 overlapping manual invocation 중 일시적으로 lock될 수 있음

해석:

* 이 이슈는 observability PASS 결과를 무효화하지 않음
* 반복될 경우 별도로 추적할 가치가 있는 minor scheduler-wrapper 운영 이슈다

---

# 6. 최종 결과

```text
OBSERVABILITY_RUNTIME_PROOF = PASS
SNAPSHOT_REFLECTION         = PASS
TEST_STATUS                 = PASS
BREAKOUT_EXPERIMENT_GATE    = OPEN
```

## Obsidian Links

- [[CNT v2 OBSERVABILITY VALIDATION GATE KO]]


