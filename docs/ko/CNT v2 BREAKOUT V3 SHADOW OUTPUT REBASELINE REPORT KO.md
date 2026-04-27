---
tags:
  - cnt
  - type/documentation
  - status/active
  - strategy/breakout_v3
  - obsidian
  - type/analysis
  - type/validation
  - cnt-v2-breakout-v3-shadow-output-rebaseline-report-ko
---

# CNT v2 BREAKOUT V3 SHADOW OUTPUT 기준선 재설정 보고서

## 요약

이번 단계에서는 `breakout_v3` shadow output에 대해 post-fix 기준의 깨끗한 관측 기준선을 새로 만들었습니다.

목적:

- 수정 전/후 의미가 섞인 기존 산출물 보존
- 현재 `breakout_v3` shadow output 파일 초기화
- 현재 evaluator logic만 반영된 새 기준선 재생성

## 1. 왜 재기준선이 필요했는가

관찰된 문제:

- 과거 `shadow_breakout_v3.jsonl` 라인에 pre-fix blocker semantics가 남아 있었음
- snapshot 집계도 old/new 의미가 섞여 있었음

의미:

- 현재 shadow output을 순수 post-fix 기준선으로 해석할 수 없었음

## 2. 보존 조치

reset 전에 archive로 보존:

- `logs/archive/shadow_breakout_v3_pre_rebaseline_20260424_064140.jsonl`
- `data/archive/shadow_breakout_v3_snapshot_pre_rebaseline_20260424_064140.json`

해석:

- 과거 증거는 유지됨
- 현재 기준선은 깨끗하게 다시 시작할 수 있게 됨

## 3. Reset 및 One-Shot 검증

실행:

- 현재 `logs/shadow_breakout_v3.jsonl` reset
- 현재 `data/shadow_breakout_v3_snapshot.json` 제거
- 정상 entry chain으로 `run.ps1` 1회 실행

결과:

- 새 `breakout_v3` shadow event 기록
- post-fix 기준선만 반영한 snapshot 재생성

## 4. BOM 호환성 보강

rebaseline 검증 중, 외부 도구가 만든 UTF-8 BOM 포함 JSONL 파일에서 snapshot rebuild가 실패할 수 있는 edge case가 드러났습니다.

적용한 보강:

- `update_breakout_v3_shadow_snapshot()`가 이제 `utf-8-sig`로 log를 읽음

효과:

- BOM이 붙은 JSONL 파일도 snapshot rebuild에서 안전하게 처리 가능

## 5. 현재 post-rebaseline 의미

현재 재기준선 이후 해석:

- 이제 `breakout_v3` shadow output은 post-fix-only observation 기준으로 사용할 수 있음
- pre-fix blocker 명칭은 archive 파일에만 남음
- 이후 snapshot 증가는 새 기준선 기준으로 해석하면 됨

## 6. 변경하지 않은 것

이번 단계에서도 변경하지 않음:

- `ACTIVE_STRATEGIES`
- `breakout_v1` active 상태
- 주문 라우팅
- live activation

## Obsidian Links

- [[CNT v2 BREAKOUT V3 DESIGN DRAFT KO]]


