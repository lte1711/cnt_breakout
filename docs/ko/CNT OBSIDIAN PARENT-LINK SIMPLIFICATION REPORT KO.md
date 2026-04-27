---
tags:
  - cnt
  - type/documentation
  - status/active
  - graph-view
  - obsidian
  - type/analysis
  - type/validation
---

---
---

# CNT Obsidian 상위 부모 링크 단순화 보고서

## 목적

Obsidian에서 말단 문서가 바로 위 상위 문서 하나에만 연결되도록 문서 링크 구조를 단순화한다.

## 적용한 규칙

- 영문 상위 문서는 `00 Docs Index`에 연결
- 한글 미러 상위 문서는 `00 Docs Index KO`에 연결
- `00 Docs Index`는 `00 CNT Vault Home`에 연결
- `00 Docs Index KO`는 `00 Docs Index`에 연결
- 말단 문서는 `## Obsidian Links` 섹션 안에 부모 링크 1개만 남긴다

## 적용 내용

- `scripts/simplify_graph_links.py`를 부모 링크 전용 구조로 다시 작성
- `docs/`와 `docs/ko/` 전체에 일괄 적용

## 검증

- 영문/한글 말단 문서 샘플에서 Obsidian 링크가 1개만 남는 것 확인
- 대시보드 가이드 계열 문서가 상위 부모 1개만 가리키는 것 확인
- 자동 검증 결과, 인덱스를 제외한 어떤 마크다운 문서도 문서 전체에 2개 이상의 wiki-link를 남기지 않음
- 즉 말단 문서는 본문 안의 교차 wiki-link까지 일반 텍스트로 내려간 상태임

## 결과

문서 그래프는 다음 상태로 정리됐다.

- 말단 문서는 부모 1개만 연결
- 인덱스 문서는 허브 역할 유지
- 전용 Obsidian 링크 섹션의 불필요한 교차 링크 제거
- 말단 문서 본문의 교차 wiki-link도 일반 텍스트로 단순화

## Obsidian Links

- [[00 Docs Index KO]]


