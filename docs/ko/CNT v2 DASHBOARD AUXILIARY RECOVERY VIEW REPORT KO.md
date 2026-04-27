---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - risk
  - strategy/pullback_v1
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - status/final
  - language:-ko
---

# CNT v2 대시보드 보조 회복 평가 뷰 반영 보고

## 목적

이번 패치는 공식 live gate를 변경하지 않고, 대시보드에 보조 회복 평가 패널을 추가하는 작업이다.

목적은 현재 CNT 운영 현실을 대시보드에 그대로 반영하는 것이다.

- 공식 live gate는 계속 보수적으로 유지
- 과거 `breakout_v1` 오염 때문에 공식 gate는 아직 음수일 수 있음
- 그와 별개로 post-isolation runtime 회복 상태는 따로 읽을 필요가 있음

## 추가된 내용

대시보드에 `Auxiliary Recovery` 전용 카드가 추가됐다.

이 카드는 명시적으로:

- 설명용 뷰
- 활성화 권한 없음
- `data/live_gate_decision.json`을 대체하지 않음

## 현재 보조 평가에 쓰는 신호

패널은 기존 runtime 데이터만 사용한다.

- `data/state.json`의 active runtime strategy
- `data/state.json`과 `data/portfolio_state.json`의 risk counter 유지 여부
- `data/performance_snapshot.json`의 `pullback_v1` 전략 성과
- `data/shadow_breakout_v3_snapshot.json`의 현재 shadow 누적 상태

## 읽는 방식

이제 대시보드는 다음 둘을 분리해서 보여준다.

1. `Official Live Gate`
   - 계속 최종 권위 유지
   - 계속 보수적 판단 유지
2. `Auxiliary Recovery`
   - post-isolation 회복 해석 전용
   - 공식 gate가 아직 음수여도 현재 런타임이 안정화되는지를 따로 관찰

## 왜 필요한가

이 분리가 없으면 대시보드는 다음 두 가지를 잘못 암시할 수 있다.

- 공식 gate가 음수이면 아무 개선도 없는 것처럼 보임
- 회복을 보려면 gate 자체를 바꿔야 하는 것처럼 보임

이번 패치는 그 두 오류를 동시에 피한다.

## 바뀌지 않은 것

이번 대시보드 패치는 다음을 **변경하지 않는다.**

- gate 로직
- threshold
- live gate status override
- `breakout_v1` 재활성화
- `breakout_v3` 활성화

## 결과

이제 CNT 대시보드는 한 화면에서 함께 보여준다.

- 공식 gate 상태
- 현재 pullback-only runtime 상태
- 현재 breakout_v3 shadow 관측 상태
- post-isolation 보조 회복 해석

즉 현재 운영 단계에 맞는 해석 구조가 대시보드에 직접 반영됐다.

## Obsidian Links

- [[CNT DATA DASHBOARD KO]]


