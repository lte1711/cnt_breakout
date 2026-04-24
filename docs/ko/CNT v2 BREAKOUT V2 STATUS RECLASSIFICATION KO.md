---
aliases:
  - CNT v2 BREAKOUT V2 STATUS RECLASSIFICATION KO
---

# CNT v2 BREAKOUT V2 상태 재분류

## 이전 상태

- `shadow candidate`

## 새 상태

- `failed design`
- `inactive experimental strategy`

## 근거

이 재분류는 아래 근거 위에서 내려졌다.

- 충분한 expanded shadow sample 확보
- `allowed_signal_count = 0`
- hypothetical candidate generation 없음
- multi-stage blockage의 안정적 증거

## 의미

이 상태는 아래를 의미하지 않는다.

- 즉시 코드 삭제
- registry에서 강제 제거
- 전략 activation

이 상태가 의미하는 것은 아래다.

- 추가 shadow collection 없이도 판단이 가능하다
- 현재 설계는 promotion하면 안 된다
- 다음 작업은 redesign preparation으로 넘어가야 한다

## 운영 규칙

재설계가 명시적으로 승인되고 구현되기 전까지:

- `breakout_v2`는 off 유지
- `breakout_v1`는 reference only 유지
- `pullback_v1`는 live positive driver 유지

## 링크

- CNT v2 BREAKOUT V2 STATUS RECLASSIFICATION
- CNT v2 BREAKOUT V2 REDESIGN PREPARATION
- CNT v2 BREAKOUT V3 DESIGN DRAFT KO

## Obsidian Links

- [[CNT v2 BREAKOUT V2 DESIGN KO]]


