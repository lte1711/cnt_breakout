---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - type/operation
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - status/completed
  - cnt-docs-korean-migration-plan-ko
---

# CNT 문서 한글화 단계별 이행 계획

## 목적

이 문서는 CNT 문서 전체를 한글 미러 체계로 확장하기 위한 단계별 계획이다.

목표는 한 번에 전부 번역하는 것이 아니다.

목표는 현재의 runtime 관측 흐름을 깨지 않으면서, 한글을 실제 작업 언어로 만드는 것이다.

## 현재 스냅샷

계획 수립 시점 기준:

- `docs/` 아래 루트 마크다운 문서 수: `132`
- `docs/ko/` 아래 한글 미러 문서 수: `4`

즉 한글 문서 체계는 시작됐지만, 아직 전체 운영 문서 대부분은 영문 중심 상태다.

## 이행 원칙

한글화는 아래 순서로 진행한다.

1. 현재 운영 중인 문서
2. 현재 breakout 관측 문서
3. 현재 workflow / protocol 문서
4. 주요 validation / architecture 문서
5. 장기 보관 메모

이 순서를 지켜야 현재 전략 관측 작업을 방해하지 않는다.

## 1단계

우선순위:

- 현재 Obsidian workflow
- 현재 operating protocol
- 현재 breakout_v3 observation start / review 경로

상태:

- 시작됨
- 부분 완료

## 2단계

우선순위:

- 앞으로 새로 생성되는 breakout_v3 review / observation 문서
- 앞으로 새로 생성되는 activation 관련 문서
- 앞으로 새로 생성되는 CNT 운영 및 validation 문서

규칙:

- 중요한 새 문서는 같은 변경 안에서 한글 미러도 같이 생성

## 3단계

우선순위:

- breakout_v2 archive 및 redesign 체인
- 주요 v2 validation report
- live readiness / gate 문서

목표:

- 가장 자주 참조되는 과거 문서를 한글로 읽을 수 있게 만들기

## 4단계

우선순위:

- v1 archive
- long-term memo
- 오래된 engineering / implementation 기록

이 단계는 현재 breakout_v3 운영에 직접적 영향이 적으므로 우선순위가 낮다.

## 앞으로의 새 문서 규칙

이제부터는:

- 중요한 새 문서를 `docs/`에만 단독 생성하지 않는다
- 반드시 `docs/ko/` 아래 대응 한글 미러를 함께 만든다

## 리뷰 트리거

이 이행 계획은 아래 조건에서 다시 점검한다.

- 한글 미러 문서 수가 의미 있게 증가했을 때
- 새 운영 단계로 넘어갈 때
- breakout_v3 상태가 바뀔 때

## 최종 방향

CNT 문서 체계는 아래의 안정된 이중 구조로 가야 한다.

- `docs/` = 공식 저장소 문서
- `docs/ko/` = 사용자 열람용 한글 미러

이 방향은 사용자가 명시적으로 바꾸기 전까지 앞으로의 문서 기본 방향으로 유지한다.

## Obsidian Links

- [[00 Docs Index KO]]


