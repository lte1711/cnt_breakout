---
aliases:
  - CNT DOCS KOREAN MIRROR POLICY KO
---

# CNT 문서 한글 미러 정책

## 목적

이 정책은 CNT 문서를 앞으로 `영문 공식 경로 + 한글 미러 경로`의 이중 구조로 고정하기 위한 문서다.

사용자 작업 언어는 한글로 둔다.

저장소 호환 구조는 다음처럼 유지한다.

- `docs/` = 공식 저장소 문서 경로
- `docs/ko/` = 사용자 열람과 판단 작업을 위한 한글 미러 경로

이 정책은 runtime, engine, strategy, validation 로직을 바꾸지 않는다.

## 고정 규칙

앞으로 CNT의 새 문서는 아래 두 조건을 동시에 만족해야 한다.

1. `docs/` 아래 공식 문서가 있어야 한다
2. `docs/ko/` 아래 한글 미러 문서가 있어야 한다

가능하면 같은 작업 턴에서 함께 만든다.

## 파일명 규칙

CNT는 유니코드 파일명을 금지하므로, 파일명은 계속 ASCII만 사용한다.

권장 패턴:

- 공식 문서: `docs/CNT ... .md`
- 한글 미러: `docs/ko/CNT ... KO.md`

예시:

- `docs/CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW.md`
- `docs/ko/CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW KO.md`

## 한글 우선 작업 규칙

사용자는 앞으로 한글 미러 문서를 기준으로 읽고 작업할 수 있다.

운영 해석:

- 한글 미러 = 기본 열람 및 판단 표면
- 공식 문서 경로 = 인덱스와 참조 안정성을 유지하는 저장소 경로

즉, 새 review, plan, checklist, protocol 문서는 처음부터 한글로 읽을 수 있어야 한다.

## 적용 범위

이 규칙은 아래 문서에 적용한다.

- plan
- report
- checklist
- review
- observation 문서
- protocol 문서
- workflow guide

단, 이 규칙이 모든 레거시 문서를 한 번에 전부 번역해야 한다는 뜻은 아니다.

기존 문서의 한글화는 현재 관측과 검증 흐름을 깨지 않도록 단계별로 진행한다.

## 새 문서 생성 체크리스트

새 문서를 만들 때마다 아래를 확인한다.

- [ ] `docs/` 아래 공식 문서 생성
- [ ] `docs/ko/` 아래 한글 미러 생성
- [ ] 두 파일 모두 ASCII 파일명 유지
- [ ] 중요한 공식 문서면 루트 인덱스 반영
- [ ] 한글 미러가 생겼으면 한글 인덱스 반영
- [ ] Obsidian 내부 링크가 읽기 가능하게 유지됨

## 비침투 규칙

이 정책을 이유로 아래를 해서는 안 된다.

- runtime 흐름 변경
- strategy 로직 변경
- observation threshold 변경
- review 기준 변경
- 근거 없는 상태 재분류

문서 현지화와 runtime 판단은 별개다.

## 실행 규칙

문서 작업만 하는 경우에는 이중 언어 구조를 적용해도 된다.

반대로 runtime이나 strategy 동작에 영향을 주는 작업에서는, 한글화가 현재 검증 흐름을 바꾸는 이유가 되어서는 안 된다.

## 현재 방향

현재 방향은 다음과 같다.

- CNT runtime과 breakout 관측은 그대로 유지
- 앞으로 생성되는 중요한 문서는 한글 미러를 함께 생성
- 기존 문서는 단계적으로 한글화

## 최종 고정

CNT 문서 체계는 이제 `한글 우선 + 이중 경로` 규칙으로 운영한다.

사용자가 별도로 중단 지시를 하지 않는 한, 앞으로의 새 공식 CNT 문서는 한글 미러를 함께 가져야 한다.

## Obsidian Links

- [[00 Docs Index KO]]


