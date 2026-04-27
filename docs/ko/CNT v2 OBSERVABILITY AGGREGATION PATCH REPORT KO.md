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
  - status/completed
  - cnt-v2-observability-aggregation-patch-report-ko
---

# CNT v2 관측성 집계 패치 보고

```text
DOCUMENT_NAME = cnt_v2_observability_aggregation_patch_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = COMPLETE
REFERENCE_1   = CNT v2 OBSERVABILITY IMPLEMENTATION REPORT
REFERENCE_2   = CNT v2 OBSERVABILITY VALIDATION GATE
```

---

# 1. 요약

필요한 observability 해석 보정이 구현됐다.

이번 단계에서 완료된 것:

* `selected_strategy_counts` 집계 보정
* old/new blocked-signal mixed parsing 지원
* snapshot parsing regression test 추가

또한 이 단계에서 fresh runtime proof도 확보됐다.

현재 다음 단계:

```text
breakout_v1 first relaxation experiment is now allowed
```

---

# 2. 구현된 코드 수정

업데이트:

* `src/analytics/performance_snapshot.py`

구현 내용:

1. `selected_strategy_counts`는 이제 `selection_reason=highest_score`가 있는 line만 count
2. legacy `reason=no_ranked_signal` line도 계속 지원
3. new `blocked_detail` 구조도 계속 지원
4. old/new mixed log stream이 snapshot generation을 깨뜨리지 않음
5. entry-gate blocked detail을 별도 집계 가능

추가된 테스트:

* `tests/test_performance_snapshot.py`

커버한 case:

1. legacy-only logs
2. new-format logs
3. mixed legacy + new logs
4. `selection_reason=highest_score` selection counting
5. entry-gate blocked-detail aggregation

---

# 3. 검증

실행:

```text
python -m unittest discover -s tests -p "test_*.py"
```

결과:

```text
Ran 16 tests
OK
```

fresh validation 이후 현재 파일에서도 추가 확인:

* `data/state.json`의 `pending_order = null`
* `data/state.json`의 `open_trade = null`
* `logs/runtime.log`는 fresh validation cycle에서 `NO_ENTRY_SIGNAL`로 종료
* `logs/portfolio.log`는 이제 new-format observability field를 포함

---

# 4. 운영 해석

Fresh-cycle observability proof는 이제 확인된 상태다.

확인된 fresh evidence:

* `blocked_detail=all_filtered`
* `candidate_count=0`
* `rejected_reasons={'market_not_trend_up': 1, 'trend_not_up': 1}`

Snapshot 반영도 확인:

* `blocked_signal_stats.no_ranked_signal`는 이제 `{all_filtered=1, legacy=25}`로 저장

---

# 5. 현재 상태

```text
OBSERVABILITY_CODE_FIX     = COMPLETE
OBSERVABILITY_TEST_FIX     = COMPLETE
FRESH_RUNTIME_PROOF        = COMPLETE
BREAKOUT_EXPERIMENT_STATUS = ALLOWED
```

---

# 6. 필수 다음 단계

필수 다음 조치:

1. breakout_v1 first relaxation experiment 시작
2. 실험 동안 observability field 계속 활성 유지
3. 실험 결과와 rejection distribution을 전용 보고서로 저장

## Obsidian Links

- [[CNT v2 OBSERVABILITY PRIORITY PLAN KO]]


