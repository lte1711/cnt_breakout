---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - strategy/breakout_v3
  - graph-view
  - obsidian
  - type/analysis
  - status/final
  - language:-ko
---

# CNT Obsidian 그래프 하드 단순화 보고서

## 목적

Obsidian 그래프를 더 단순하게 만들기 위해 링크와 태그를 함께 정리했다.

## 적용한 변경

### 1. 링크 단순화

- 인덱스 문서를 제외한 모든 문서는 문서 전체에 wiki-link를 1개만 남긴다
- 남는 링크 1개는 바로 위 부모 문서 링크다
- 본문 안 교차 링크는 필요한 경우 일반 텍스트로 내렸다

### 2. 부모 그룹 재배치

기존에 `00 Docs Index`로 바로 붙던 문서들을 파일명 패턴 기준으로 상위 허브 문서에 재배치했다.

대표 부모 허브는 아래와 같다.

- `CNT v2 BREAKOUT QUALITY EVALUATION REPORT`
- `CNT v2 BREAKOUT V2 DESIGN`
- `CNT v2 BREAKOUT V3 DESIGN DRAFT`
- `CNT v2 VALIDATION REPORT`
- `CNT v2 LIVE READINESS GATE`
- `CNT v2 TESTNET PERFORMANCE REPORT`
- `CNT DATA DASHBOARD`
- `CNT TOOLCHAIN INTEGRATION REPORT`

### 3. 태그 단순화

- 인덱스 문서를 제외한 모든 마크다운 문서의 태그를 제거했다
- `00 Docs Index.md`는 `cnt`만 유지한다
- `00 Docs Index KO.md`는 `cnt`, `ko`만 유지한다

## 검증

- 인덱스를 제외한 마크다운 문서 중 wiki-link가 2개 이상인 문서: `0`
- 인덱스 외 문서 중 단순화 기준을 넘는 태그가 남은 문서: `0`

## 결과

이제 그래프는 다음 이유로 더 단순해졌다.

- 말단 문서끼리 옆으로 얽히는 링크망 제거
- 대량 태그 노드 제거
- 이동은 부모 허브 문서와 인덱스 문서를 통해 유지
