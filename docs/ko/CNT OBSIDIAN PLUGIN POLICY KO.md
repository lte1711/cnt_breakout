---
tags:
  - cnt
  - obsidian
  - tooling
aliases:
  - CNT Obsidian Plugin Policy KO
---

# CNT Obsidian Plugin Policy KO

## 목적

이 문서는 CNT 저장소에서 Obsidian 플러그인을 어떤 방식으로 다루는지 정의한다.

## 현재 정책

- CNT 저장소는 `.obsidian/community-plugins.json`으로 플러그인 활성화 의도를 추적한다.
- 저장소는 기본적으로 `.obsidian/plugins/` 아래에 서드파티 플러그인 코드를 포함하지 않는다.
- 따라서 새 클론에서는 활성화된 플러그인 이름은 보이더라도 실제 플러그인 번들은 로컬에 없을 수 있다.

## 이 정책의 이유

- 서드파티 플러그인 번들은 사용자 환경 의존성이 크다.
- 플러그인 코드를 저장소에 포함하면 변경 노이즈와 업데이트 churn이 커진다.
- Obsidian 플러그인이 없어도 저장소 자체는 이식 가능해야 한다.

## 기대 동작

- [[CNT DATA DASHBOARD]] 문서는 CNT 저장소 루트를 Vault 루트로 쓰는 Obsidian 환경을 전제로 설계된다.
- Dataview가 필요한 대시보드 쿼리는 사용자가 `dataview` 플러그인을 로컬 설치해야 동작한다.
- Templater 기반 템플릿 워크플로는 사용자가 `templater-obsidian` 플러그인을 로컬 설치해야 동작한다.

## 재현성 규칙

- 저장소 기본 상태는 `.obsidian/plugins/`에 플러그인 번들이 있다고 가정하면 안 된다.
- 문서는 플러그인이 없어도 일반 Markdown으로 읽을 수 있어야 한다.
- 플러그인 의존 기능은 플러그인이 없을 때도 문서 자체는 읽히도록 점진적으로 저하되어야 한다.

## 설치 메모

로컬 환경에서 대시보드/템플릿 전체 기능이 필요하면, 이 Vault에서 `.obsidian/community-plugins.json`에 적힌 플러그인을 Obsidian 안에서 직접 설치한다.

## 링크

- [[CNT DATA DASHBOARD KO]]
- [[CNT TOOLCHAIN INTEGRATION REPORT KO]]
- [[00 Docs Index KO]]
