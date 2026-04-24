---
aliases:
  - CNT v2 OBSIDIAN INTEGRATED OPERATING PROTOCOL KO
---

# CNT v2 Obsidian 통합 운영 프로토콜 (한글판)

## 목적

이 문서는 CNT의 `breakout_v3` 운영을 위해 다음을 하나의 프로토콜로 묶는다.

- runtime 실행
- shadow observation
- Obsidian 리뷰 작성
- Canvas 상태 추적

즉 단순 노트 체계가 아니라 실제 운영 판단 프로토콜이다.

## 핵심 원칙

운영 역할 분리는 다음과 같이 고정한다.

- code = 실행
- Python / runtime data = 분석
- Obsidian markdown = 판단
- Canvas = 상태 인터페이스

Obsidian은 따라서 노트 앱이 아니라 전략 판단 UI 역할을 한다.

## 구성 요소

### 1. Templates

판단 도구:

- `templates/observation_review.md`
- `templates/allowed_signal_log.md`
- `templates/activation_review_checklist.md`
- `templates/ko/observation_review_ko.md`
- `templates/ko/allowed_signal_log_ko.md`
- `templates/ko/activation_review_checklist_ko.md`

### 2. Canvas

상태 지도:

```text
CNT SYSTEM
|- pullback_v1 (ACTIVE)
|- breakout_v2 (FAILED)
\- breakout_v3 (OBSERVATION -> REVIEW -> FUTURE)
```

색상 규칙:

- active = 초록
- failed = 빨강
- observation = 노랑

### 3. Workflow

언제 문서를 써야 하는지 결정한다.

### 4. State Transition Rules

리뷰 후 다음 단계 결정을 고정한다.

## 템플릿 사용 고정 규칙

### Observation Review

사용:

- shadow 이벤트 `20~30건`마다

목적:

- 주기적 구조 판단

### Allowed Signal Log

사용:

- 실제 allowed shadow signal이 나왔을 때만

목적:

- 이벤트성 증거 기록

### Activation Review Checklist

사용:

- activation 검토가 현실적인 질문이 됐을 때만

목적:

- 최종 go / no-go 판단

## 워크플로 트리거

### 평상시

대부분의 시간에는 문서를 새로 쓰지 않는다.

정상 흐름:

- `run.ps1` 계속 실행
- shadow event 누적
- snapshot 갱신

### Trigger 1: 이벤트 `20~30건` 추가 누적

행동:

- observation review 작성

### Trigger 2: 첫 allowed signal 발생

행동:

- allowed signal log 작성 또는 갱신

### Trigger 3: activation 검토 질문 발생

행동:

- activation checklist 열기

## 상태 전이 규칙

### STILL_OVER_FILTERED

패턴:

- allowed = `0`
- soft pass가 낮은 구간에 몰림

다음 단계:

- continue observation

### FIRST_ALLOWED_DETECTED

패턴:

- `allowed_signal_count >= 1`

다음 단계:

- allowed signal log 작성
- continue observation

### STRUCTURE_IMPROVING

패턴:

- blocker 집중도가 약해짐
- soft pass가 위로 이동

다음 단계:

- continue observation
- 반복되면 threshold review를 나중에 고려

### NEEDS_REDESIGN

패턴:

- allowed = `0` 지속
- 특정 blocker 또는 stage dominance가 구조적으로 강함

다음 단계:

- redesign preparation

## Canvas 업데이트 규칙

Canvas는 매 사이클마다 바꾸지 않고, formal review 이후에만 갱신한다.

### STILL_OVER_FILTERED

- `breakout_v3 -> Observation Window` 유지

### FIRST_ALLOWED_DETECTED

- allowed signal node 추가

### STRUCTURE_IMPROVING

- review branch와 observation progress 강조

### NEEDS_REDESIGN

- `breakout_v3 -> redesign branch`로 이동

## 현재 단계 고정

현재 CNT는 다음 상태를 유지한다.

- `breakout_v3 = SHADOW_ONLY`
- activation = prohibited
- tuning = prohibited
- observation 중에는 engine path 변경 금지

따라서 지금 허용되는 것은:

- event accumulation
- periodic review writing
- evidence logging

허용되지 않는 것은:

- activation
- threshold relaxation
- 초기 observation 중 hard/soft gate 재설계

## 최종 기록

CNT의 Obsidian 운영 스택은 이제 다음으로 정의된다.

- templates = 판단 형식
- Canvas = 상태 표시
- workflow = 시점 제어
- transition rules = 다음 단계 제어

즉 이 프로토콜은 runtime 실행과 전략 판단을 분리한 상태에서, 일관된 전략 검증 운영을 가능하게 한다.

## Obsidian Links

- [[00 Docs Index KO]]


