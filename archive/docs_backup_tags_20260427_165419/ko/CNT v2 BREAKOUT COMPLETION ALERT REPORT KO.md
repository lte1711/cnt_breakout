---
aliases:
  - CNT v2 BREAKOUT COMPLETION ALERT REPORT KO
---

# CNT v2 BREAKOUT 완료 알림 보고

```text
DOCUMENT_NAME = cnt_v2_breakout_completion_alert_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-20
STATUS        = APPLIED
PURPOSE       = breakout post-change 관측이 완료 기준에 도달하면 알림 발생
```

---

# 1. 알림 규칙

설정된 completion rule:

```text
TARGET = breakout post-change 30 cycles
ALERT  = trigger once when target is reached
```

이유:

* `20 cycles`는 가장 이른 의미 있는 리뷰 시점
* `30 cycles`는 이 관측 단계에서 더 안정적인 완료 기준

---

# 2. 구현

추가:

* `scripts/breakout_completion_alert.ps1`

Runtime outputs:

* `data/breakout_completion_alert.json`
* `logs/breakout_completion_alert.log`

동작:

1. `logs/signal.log`에서 breakout post-change cycles 계산
2. threshold에 아직 못 미치면 pending log만 append
3. threshold 도달 시:
   * completion marker json 기록
   * completion log append
   * `msg *`를 통한 OS message 시도

---

# 3. 운영 가정

이 알림은 현재 phase를 아래 기준에서 complete로 본다.

```text
POST_CHANGE_BREAKOUT_CYCLES >= 30
```

이후 더 짧은 review point가 필요하면 그때 명시적으로 threshold를 변경해야 한다.

## Obsidian Links

- [[CNT v2 BREAKOUT QUALITY EVALUATION REPORT KO]]


