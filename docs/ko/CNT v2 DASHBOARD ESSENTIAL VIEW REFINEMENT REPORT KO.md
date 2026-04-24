---
title: CNT v2 DASHBOARD ESSENTIAL VIEW REFINEMENT REPORT KO
status: FINAL
language: ko
updated: 2026-04-24
---

# CNT v2 DASHBOARD ESSENTIAL VIEW REFINEMENT REPORT

## 목적

이번 refinement는 현재 운영 단계에 꼭 필요한 정보만 남기도록 operations dashboard를 정리한 것이다.

현재 CNT phase:

- `pullback_v1` = 유일한 live active runtime strategy
- `breakout_v3` = shadow-only
- 현재 작업 목표 = optimization이 아니라 observation

따라서 대시보드는 아래를 우선 보여줘야 한다.

- live gate 상태
- 현재 runtime mode
- 현재 engine state
- 현재 shadow observation 상태
- 현재 risk sync 상태
- 현재 상위 성과 건강도

## 제거하거나 축소한 영역

현재 단계에서 신호 대비 과한 영역은 메인 화면에서 제거했다.

- 큰 signal pipeline 블록
- live-ready baseline 비교 패널
- 전체 strategy quality 테이블
- 광범위한 blocker dump 섹션

이 섹션들은 넓은 진단 단계에서는 유용했지만,
현재 pullback-only observation phase에서는 최우선 화면이 아니다.

## 메인으로 유지한 영역

정리 후 대시보드는 아래를 중심으로 유지한다.

- `Live Gate`
- `System Health`
- `Runtime Mode`
- `Breakout V3 Shadow`
- `Expectancy / PF / Net PnL`
- `Engine State`
- `Risk Sync`

## 운영자가 바로 답할 수 있어야 하는 질문

이제 운영자는 화면을 보자마자 아래를 확인할 수 있어야 한다.

1. 시스템이 여전히 gate-failed 상태인가, 회복했는가?
2. `pullback_v1`가 계속 유일한 live runtime strategy인가?
3. 엔진은 risk로 막혔는가, 단순히 no entry인가?
4. `breakout_v3`는 여전히 shadow-only인가?
5. shadow observation count가 증가하고 있는가?
6. risk counter는 동기화된 상태인가?

## 범위

이번 변경은 dashboard visibility refinement만 해당한다.

즉 다음은 바꾸지 않는다.

- runtime logic
- strategy selection logic
- live gate logic
- shadow evaluator logic

## 결론

이제 대시보드는 pullback-only live observation과 breakout_v3 shadow monitoring에 필요한 고신호 패널만 보여주도록 정리되었다.

## Obsidian Links

- [[CNT DATA DASHBOARD KO]]


