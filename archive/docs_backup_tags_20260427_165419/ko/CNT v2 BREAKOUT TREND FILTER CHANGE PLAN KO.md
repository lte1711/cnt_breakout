---
aliases:
  - CNT v2 BREAKOUT TREND FILTER CHANGE PLAN KO
---

# CNT v2 BREAKOUT 추세 필터 변경 계획

```text
DOCUMENT_NAME = cnt_v2_breakout_trend_filter_change_plan_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = APPLIED
PURPOSE       = breakout_v1에 대해 권장안 A 추세 필터 완화를 적용
```

---

# 1. 변경 대상

대상 파일:

* `src/strategies/breakout_v1.py`

대상 범위:

* 상위 trend filter만

범위 밖:

* ATR / RSI 2차 완화
* ranker 변경
* engine 변경

---

# 2. 적용된 변경

적용 옵션:

```text
OPTION A = trend-filter relaxation
```

구현 규칙:

* 기존처럼 `TREND_UP`는 계속 허용
* 추가로 아래 조건이면 `RANGE`도 하위 breakout 체크로 진행 허용
  * primary trend bias가 `UP`
  * entry-frame `ema_fast > ema_slow`

의도:

* 기존에는 상단 trend gate에서 바로 멈추던 cycle에서도, 하위 breakout blocker를 관측 가능하게 만들기
* 변경 폭은 좁고 설명 가능하게 유지하기

---

# 3. 필수 검증

검증 요구사항:

1. tests가 계속 green이어야 함
2. breakout trend-bias 동작을 새 테스트가 커버해야 함
3. one fresh runtime cycle 실행
4. runtime evidence 없이 성공 주장 금지

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]


