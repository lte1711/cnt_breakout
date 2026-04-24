---
aliases:
  - CNT v2 OBSIDIAN REVIEW WORKFLOW GUIDE KO
---

# CNT v2 Obsidian 리뷰 워크플로 가이드 (한글판)

## 목적

이 문서는 `breakout_v3`용 Obsidian 리뷰 템플릿을 실제 운영에서 어떻게 써야 하는지 한글로 정리한 가이드다.

핵심 원칙:

- 분석은 Python과 runtime artifact에서 한다
- 판단은 Obsidian 호환 markdown에 기록한다
- Obsidian은 문서 허브 역할을 한다
- 이 워크플로는 CNT의 runtime이나 strategy code를 바꾸지 않는다

## 추가된 템플릿 파일

현재 템플릿은 `templates/` 아래에 있고, 한글 버전은 `templates/ko/` 아래에 있다.

영문:

- `templates/observation_review.md`
- `templates/allowed_signal_log.md`
- `templates/activation_review_checklist.md`

한글:

- `templates/ko/observation_review_ko.md`
- `templates/ko/allowed_signal_log_ko.md`
- `templates/ko/activation_review_checklist_ko.md`

템플릿은 작성 보조 도구일 뿐이며, 공식 판단 문서는 여전히 `docs/` 아래에 생성하는 것을 권장한다.

## 권장 폴더 사용 방식

```text
Vault/
|- docs/
|- daily/
|- templates/
|  |- observation_review.md
|  |- allowed_signal_log.md
|  \- activation_review_checklist.md
|- templates/ko/
|  |- observation_review_ko.md
|  |- allowed_signal_log_ko.md
|  \- activation_review_checklist_ko.md
\- dashboard/
```

해석:

- `docs/` = 공식 CNT 기록
- `templates/` = 영문 템플릿
- `templates/ko/` = 한글 템플릿

## 템플릿 사용 규칙

### 1. Observation Review

사용 시점:

- `breakout_v3` shadow 이벤트가 추가로 `20~30건` 누적됐을 때
- 또는 의미 있는 구조 변화가 생겼을 때
  - 첫 allowed signal
  - blocker 분포 변화
  - `soft_pass_count >= 3` 반복

권장 출력 경로:

- `docs/CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW.md`
- `docs/CNT v2 BREAKOUT V3 SECOND SHADOW OBSERVATION REVIEW.md`

### 2. Allowed Signal Log

사용 시점:

- 실제 `allowed = true` shadow 이벤트가 발생했을 때만

권장 출력 경로:

- `docs/breakout_v3 allowed signal log.md`

### 3. Activation Review Checklist

현재 단계에서는 사용하지 않는다.

사용 시점:

- allowed signal이 실제로 존재하고
- observation review가 최소 1회 이상 완료됐고
- activation 검토 질문이 현실화됐을 때

권장 출력 경로:

- `docs/CNT v2 BREAKOUT V3 ACTIVATION REVIEW CHECKLIST.md`

## Templater 없이 수동 사용

가장 안전한 방식이다.

1. `templates/` 또는 `templates/ko/`에서 적절한 템플릿 파일을 연다
2. 전체 내용을 복사한다
3. `docs/` 아래 새 공식 문서를 만든다
4. 붙여 넣고 값을 채운다

장점:

- 플러그인 의존성 없음
- 예측 가능함
- 저장소 규칙과 충돌이 적음

## Templater 사용

Obsidian `Templater`를 쓰는 경우:

1. 템플릿 폴더를 `templates` 또는 `templates/ko`로 지정한다
2. `docs/` 아래 새 문서를 만든다
3. 원하는 템플릿을 삽입한다

날짜 placeholder:

- `<% tp.date.now("YYYY-MM-DD") %>`
- `<% tp.date.now("YYYY-MM-DD HH:mm") %>`

는 Templater가 켜져 있을 때만 자동 동작한다.

## 권장 리뷰 순서

1. runtime이 `shadow_breakout_v3.jsonl`을 누적한다
2. runtime이 `shadow_breakout_v3_snapshot.json`을 업데이트한다
3. `20~30`개의 새 이벤트가 쌓이면 observation review를 만든다
4. allowed signal이 생기면 allowed signal log를 만든다
5. 충분한 증거가 쌓이면 activation checklist를 연다

## Canvas 역할

Canvas는 단순한 시각화가 아니라 전략 상태 지도 역할을 한다.

권장 구조:

```text
CNT SYSTEM
|- pullback_v1 (ACTIVE)
|- breakout_v2 (FAILED)
\- breakout_v3 (OBSERVATION -> REVIEW -> FUTURE)
```

권장 색상:

- active = 초록
- failed = 빨강
- observation = 노랑

연결 권장 문서:

- CNT v2 BREAKOUT V3 DESIGN DRAFT
- CNT v2 BREAKOUT V3 SHADOW OBSERVATION WINDOW START
- CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW

## 상태 전이 규칙

### STILL_OVER_FILTERED

- allowed가 계속 `0`
- soft pass가 `0~1`에 집중

다음 단계:

- continue observation

### FIRST_ALLOWED_DETECTED

- `allowed_signal_count >= 1`

다음 단계:

- allowed signal log 작성
- continue observation

### STRUCTURE_IMPROVING

- `soft_pass_count` 분포가 위로 이동
- blocker 집중도가 약해짐

다음 단계:

- continue observation
- 반복되면 threshold review를 나중에 고려

### NEEDS_REDESIGN

- allowed가 계속 `0`
- blocker dominance가 구조적으로 강함

다음 단계:

- redesign preparation

## 현재 규칙 고정

현재 CNT 단계:

- `breakout_v3 = SHADOW_ONLY`
- `activation = PROHIBITED`
- `tuning = PROHIBITED`

따라서 현재 활성 문서 타입은 observation review이고, activation checklist는 아직 보류 상태다.

## Obsidian Links

- [[00 Docs Index KO]]


