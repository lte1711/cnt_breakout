---
title: CNT v2 DASHBOARD PULLBACK-ONLY OBSERVATION UPGRADE REPORT KO
status: FINAL
language: ko
updated: 2026-04-24
---

# CNT v2 DASHBOARD PULLBACK-ONLY OBSERVATION UPGRADE REPORT

## 목적

이번 패치는 운영자가 raw 파일을 먼저 열지 않아도 현재 런타임 모드를 즉시 볼 수 있도록 대시보드를 올리는 것이다.

새 대시보드는 다음 상태를 직접 보여줘야 한다.

- `pullback_v1` = 유일한 live active runtime strategy
- `breakout_v1` = active runtime에서 격리됨
- `breakout_v3` = shadow-only
- 현재 `breakout_v3` shadow observation 진행 상황

## 변경 파일

- `docs/cnt_operations_dashboard.html`
- `docs/CNT v2 DASHBOARD PULLBACK-ONLY OBSERVATION UPGRADE REPORT.md`
- `docs/ko/CNT v2 DASHBOARD PULLBACK-ONLY OBSERVATION UPGRADE REPORT KO.md`

## 대시보드 변경 내용

### 1. Runtime Mode 카드 추가

이제 대시보드는 다음을 명시적으로 보여준다.

- 현재 live active runtime strategy
- 현재 runtime action
- pullback-only operation badge
- breakout_v3 shadow-only badge

### 2. Breakout V3 Shadow 카드 추가

이제 `data/shadow_breakout_v3_snapshot.json`를 직접 읽어 다음을 표시한다.

- `signal_count`
- `allowed_signal_count`
- `soft 3+` count
- `last_updated`
- 상위 first blocker
- 상위 hard blocker
- soft-pass distribution
- stage-fail summary

### 3. 상단 경고 보강

상단 warning row에 아래가 추가된다.

- `PULLBACK-ONLY RUNTIME ACTIVE`

즉 현재 운영 모드가 바로 보이게 된다.

### 4. Footer source 확장

대시보드 source 목록에 아래가 추가된다.

- `../data/shadow_breakout_v3_snapshot.json`

## 왜 중요한가

기존 대시보드는 성과 악화 경고는 잘 보여줬지만,
현재 CNT가 어떤 제어된 운영 모드로 돌아가는지는 충분히 드러내지 못했다.

이번 패치 이후 운영자는 즉시 다음을 볼 수 있다.

- 실제 live strategy가 무엇인지
- breakout_v3가 아직 observation 전용인지
- shadow observation이 다음 review threshold를 향해 누적 중인지

## 검증

이번 단계 검증은 아래에 초점을 맞췄다.

- 대시보드가 기존 data 파일을 계속 정상 로드하는지
- 새 shadow snapshot 경로가 올바른지
- 현재 runtime state가 새 카드에 자연스럽게 매핑되는지

운영 교차 확인 source:

- `data/state.json`
- `data/live_gate_decision.json`
- `data/performance_snapshot.json`
- `data/shadow_breakout_v3_snapshot.json`

## 현재 의도된 해석

이 보고 시점에서 대시보드는 다음 상태를 읽도록 도와야 한다.

- live runtime = `pullback_v1` 단독
- Live Gate = 아직 `FAIL / NON_POSITIVE_EXPECTANCY`
- breakout_v3 = clean shadow observation 진행 중
- 다음 정식 review = post-fix shadow sample이 충분히 쌓인 뒤

## 결론

이번 대시보드 업그레이드는 post-isolation CNT 런타임의 실제 상태를 시각 운영 인터페이스에 맞춰 정렬한 패치다.

## Obsidian Links

- [[CNT DATA DASHBOARD KO]]


