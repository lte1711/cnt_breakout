---
title: CNT REPOSITORY CLEANUP REPORT KO
status: completed
updated: 2026-04-24
---

# CNT 저장소 정리 보고서

## 목적

런타임 로직, 전략 로직, 공식 운영 문서는 건드리지 않고, 저장소 안의 명백한 불필요 파일만 정리한다.

## 삭제한 항목

### 불필요한 래퍼 스크립트

- `scripts/simplify_graph_links_fixed.py`

이유:
- 현재 그래프 정리의 단일 진입점은 `scripts/simplify_graph_links.py`다.
- 이 래퍼는 독립 기능이 없었다.

### 깨진 번역 소스 초안

- `docs/cnt_v1_final_strategy_architecture_spec_ko_source.md`
- `docs/cnt_v1_implementation_work_instruction_ko_source.md`

이유:
- 두 파일 모두 실제 CNT 문서가 아니라 인코딩이 깨진 소스 초안이었다.
- 현재 문서 체인에서 사용되지 않았다.

### 파이썬 캐시 산출물

- 모든 `__pycache__/` 디렉터리
- 저장소 내부의 모든 `.pyc` 캐시 파일

이유:
- 전부 자동 생성 산출물이다.
- 이미 `.gitignore` 대상이다.

## 의도적으로 유지한 항목

- `.obsidian/` 파일
  - 현재 사용자의 Vault 작업 상태 일부이므로 유지
- `data/*.json` 런타임 스냅샷
  - 현재 운영 증거이므로 유지
- `logs/` 파일
  - 런타임 증거 성격이 강하고, 대부분 Git 추적 제외 대상이므로 유지

## 검증

- 활성 런타임 코드 경로 변경 없음
- 전략 설정 변경 없음
- 공식 validation / gate 규칙 변경 없음
- `.gitignore`가 파이썬 캐시 산출물을 이미 제외하고 있음

## 결론

현재 CNT 저장소는 활성 운영 흐름은 그대로 둔 채, 명백히 불필요한 캐시, 래퍼, 깨진 소스 파일만 제거한 상태로 정리됐다.

## Obsidian Links

- [[00 Docs Index KO]]
