---
aliases:
  - CNT v2 BREAKOUT TREND FILTER CHANGE REPORT KO
---

# CNT v2 BREAKOUT 추세 필터 변경 보고

```text
DOCUMENT_NAME = cnt_v2_breakout_trend_filter_change_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = IMPLEMENTED_INITIAL_RUNTIME_CHECK_DONE
REFERENCE_1   = CNT v2 BREAKOUT TREND FILTER REVIEW REPORT
REFERENCE_2   = CNT v2 BREAKOUT TREND FILTER CHANGE PLAN
```

---

# 1. 요약

권장된 trend-filter 변경은 실제로 구현됐다.

이 변경은 ATR / RSI threshold를 더 완화하는 변경이 아니다.

이 변경은 상위 breakout trend gate만 부드럽게 만들어, 통제된 `RANGE + UP_BIAS` 경로가 하위 breakout 체크로 내려가게 하는 변경이다.

---

# 2. 구현된 코드 변경

업데이트:

* `src/strategies/breakout_v1.py`

구현된 추가 사항:

* `trend_bias`가 이제 market classification 중 기록됨
* `RANGE`가 더 이상 모든 경우의 자동 reject를 뜻하지 않음
* 아래 조건이면 breakout이 계속 진행될 수 있음
  * `market_state == RANGE`
  * `trend_bias == UP`
  * entry-frame `ema_fast > ema_slow`

즉 기존 `TREND_UP` 경로는 유지하면서, 좁고 통제된 완화 경로 하나를 추가했다.

---

# 3. 테스트 검증

추가:

* `tests/test_breakout_trend_filter.py`

커버한 내용:

1. upward bias가 `RANGE` 내부에서도 유지되는지
2. `RANGE + UP_BIAS`가 breakout setup evaluation까지 도달하는지
3. upward bias가 없는 `RANGE`는 계속 차단되는지

실행:

```text
python -m unittest discover -s tests -p "test_*.py"
```

결과:

```text
Ran 19 tests
OK
```

---

# 4. 초기 런타임 체크

하나의 fresh cycle은 아래 엔트리 체인으로 실행됐다.

```text
run.ps1 -> main.py -> src.engine.start_engine
```

초기 post-change runtime 관측:

* breakout candidate 아직 없음
* breakout selection 아직 없음
* 최신 저장 breakout line은 여전히:
  * `reason=market_not_trend_up`

해석:

* 변경은 실제로 구현됐고 test도 통과했다
* 하지만 fresh runtime cycle 1회로는 결과 판단 불가
* blocker가 실제로 아래 단계로 이동했는지 주장하려면 scheduler cycle 누적이 더 필요하다

---

# 5. 현재 판단

```text
CODE_CHANGE_STATUS     = COMPLETE
TEST_STATUS            = PASS
INITIAL_RUNTIME_CHECK  = DONE
BREAKOUT_PROGRESS_YET  = NOT_CONFIRMED
NEXT_ACTION            = CONTINUE_OBSERVATION
```

---

# 6. 다음 점검

계속 관찰할 항목:

* `market_not_trend_up`
* `volatility_not_high`
* `breakout_not_confirmed`
* breakout candidate appearance
* breakout selection appearance

다음 의미 있는 판단은 즉시 1회 런타임 라인이 아니라, post-change cycle이 누적된 뒤 내려야 한다.

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]


