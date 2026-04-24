---
tags:
  - cnt
  - obsidian
  - graph
  - color
  - configuration
aliases:
  - CNT GRAPH VIEW COLOR CONFIGURATION
---

# CNT Graph View 색상 구성

## 개요

CNT 프로젝트의 버전 분류 및 색상 코딩 시스템을 Obsidian Graph View에 적용하는 방법

---

## 🎨 Graph View 색상 설정

### 1. 버전별 색상 그룹

| 버전 | 색상 | HEX 코드 | 태그 쿼리 | 설명 |
|------|------|----------|-----------|------|
| 🟢 v1.1 | 녹색 | #4CAF50 | `tag:cnt/v1.1` | 완료된 버전 |
| 🔵 v2.0 | 파란색 | #2196F3 | `tag:cnt/v2.0` | 설계된 버전 |
| 🟠 v2.1 | 주황색 | #FF9800 | `tag:cnt/v2.1` | 구현 중인 버전 |
| 🟣 v2.2 | 보라색 | #9C27B0 | `tag:cnt/v2.2` | 자동화 버전 |
| 🔴 v3.0 | 빨간색 | #F44336 | `tag:cnt/v3.0` | 계획된 버전 |

### 2. 상태별 색상 그룹

| 상태 | 색상 | HEX 코드 | 태그 쿼리 | 설명 |
|------|------|----------|-----------|------|
| 완료 | 녹색 | #4CAF50 | `tag:status/completed` | 완료된 문서 |
| 활성 | 주황색 | #FF9800 | `tag:status/active` | 활성 문서 |
| 계획 | 빨간색 | #F44336 | `tag:status/planned` | 계획된 문서 |

### 3. 유형별 색상 그룹

| 유형 | 색상 | HEX 코드 | 태그 쿼리 | 설명 |
|------|------|----------|-----------|------|
| 아키텍처 | 파란색 | #2196F3 | `tag:type/architecture` | 설계 문서 |
| 구현 | 주황색 | #FF9800 | `tag:type/implementation` | 구현 문서 |
| 검증 | 녹색 | #4CAF50 | `tag:type/validation` | 검증 문서 |
| 자동화 | 보라색 | #9C27B0 | `tag:type/automation` | 자동화 문서 |
| 운영 | 청회색 | #607D8B | `tag:type/operation` | 운영 문서 |

---

## 🔧 설정 파일 구조

### `.obsidian/graph.json` 설정

```json
{
  "collapse-filter": false,
  "search": "",
  "showTags": true,
  "showAttachments": true,
  "hideUnresolved": true,
  "showOrphans": true,
  "collapse-color-groups": true,
  "colorGroups": [
    {
      "query": "tag:cnt/v1.1",
      "color": "#4CAF50",
      "name": "v1.1 Completed"
    },
    {
      "query": "tag:cnt/v2.1",
      "color": "#FF9800",
      "name": "v2.1 Implementation"
    }
    // ... 추가 색상 그룹
  ],
  "collapse-display": false,
  "showArrow": true,
  "textFadeMultiplier": 0,
  "nodeSizeMultiplier": 1.2,
  "lineSizeMultiplier": 1.1,
  "collapse-forces": false,
  "centerStrength": 0.2,
  "repelStrength": 25,
  "linkStrength": 1,
  "linkDistance": 600,
  "scale": 0.05607756585711719,
  "close": true
}
```

---

## 📊 Graph View 최적화 설정

### 1. 표시 설정
- **showTags**: `true` - 태그 표시
- **showAttachments**: `true` - 첨부 파일 표시
- **hideUnresolved**: `true` - 해결되지 않은 링크 숨김
- **showOrphans**: `true` - 고립 노드 표시

### 2. 색상 그룹화
- **collapse-color-groups**: `true` - 색상 그룹 활성화
- **colorGroups**: 태그 기반 색상 그룹 정의

### 3. 시각적 효과
- **nodeSizeMultiplier**: `1.2` - 노드 크기 증가
- **lineSizeMultiplier**: `1.1` - 선 굵기 증가
- **textFadeMultiplier**: `0` - 텍스트 페이드 없음

### 4. 레이아웃 최적화
- **centerStrength**: `0.2` - 중심력 약화
- **repelStrength**: `25` - 반발력 증가
- **linkDistance**: `600` - 링크 거리 증가
- **linkStrength**: `1` - 링크 강도 유지

---

## 🎯 적용 효과

### 1. 시각적 구분
- **버전별 색상**: 각 버전의 문서가 고유 색상으로 표시
- **상태별 구분**: 완료/활성/계획 상태 시각화
- **유형별 분류**: 아키텍처/구현/검증 등 유형별 색상

### 2. 네트워크 시각화
- **연결 관계**: 문서 간의 연결이 명확히 표시
- **클러스터링**: 동일 버전/유형 문서들이 자연스럽게 그룹화
- **중요도 파악**: 노드 크기로 중요 문서 식별

### 3. 탐색 효율
- **빠른 식별**: 색상으로 원하는 문서 그룹 즉시 찾기
- **패턴 인식**: 프로젝트 구조를 한눈에 파악
- **의존성 분석**: 문서 간의 의존 관계 시각화

---

## 🔍 그래프 해석 가이드

### 1. 색상 패턴
- **녹색 클러스터**: 완료된 v1.1 및 검증 문서
- **파란색 클러스터**: v2.0 설계 및 아키텍처 문서
- **주황색 클러스터**: v2.1 구현 및 활성 문서
- **보라색 클러스터**: v2.2 자동화 문서
- **빨간색 클러스터**: v3.0 계획 문서

### 2. 연결 패턴
- **중앙 허브**: 핵심 문서들 (AGENTS, 아키텍처 등)
- **버전 간 연결**: 버전 진화에 따른 문서 연결
- **기능별 연결**: 동일 기능 영역 내 문서 연결

### 3. 구조 패턴
- **계층 구조**: 버전별 계층적 배치
- **네트워크 구조**: 기능별 네트워크 연결
- **혼합 구조**: 계층과 네트워크의 조합

---

## 🚀 사용 방법

### 1. Graph View 열기
1. Obsidian에서 `Ctrl+G` (또는 `Cmd+G`)로 Graph View 열기
2. 왼쪽 패널에서 그래프 아이콘 클릭
3. 또는 명령 팔레트에서 "Open graph view" 실행

### 2. 색상 필터링
1. 그래프 우측의 필터 패널 열기
2. 원하는 색상 그룹 선택/해제
3. 특정 버전이나 유형만 표시

### 3. 검색 및 탐색
1. 검색창에 키워드 입력
2. 관련 노드들이 강조 표시
3. 마우스 휠로 확대/축소

### 4. 상호작용
1. 노드 클릭: 해당 문서 열기
2. 노드 드래그: 위치 조정
3. 확대/축소: 전체 구조 파악

---

## 🔧 고급 설정

### 1. 동적 색상 그룹
```json
{
  "query": "tag:cnt/v2.1 AND tag:status/active",
  "color": "#FF9800",
  "name": "v2.1 Active"
}
```

### 2. 복합 쿼리
```json
{
  "query": "tag:type/architecture OR tag:type/validation",
  "color": "#2196F3",
  "name": "Architecture & Validation"
}
```

### 3. 제외 쿼리
```json
{
  "query": "-tag:status/archived",
  "color": "#9E9E9E",
  "name": "Active Documents"
}
```

---

## 📈 성능 최적화

### 1. 대규모 저장소
- **nodeSizeMultiplier**: `0.8`로 감소
- **repelStrength**: `30`으로 증가
- **linkDistance**: `800`으로 증가

### 2. 고해상도 디스플레이
- **textFadeMultiplier**: `0.1`로 설정
- **lineSizeMultiplier**: `1.5`로 증가
- **nodeSizeMultiplier**: `1.5`로 증가

### 3. 저사양 시스템
- **collapse-color-groups**: `false`로 설정
- **showOrphans**: `false`로 설정
- **showAttachments**: `false`로 설정

---

## 🛠️ 문제 해결

### 일반적인 문제

#### 1. 색상이 표시되지 않음
- 태그가 정확히 추가되었는지 확인
- `collapse-color-groups`가 `true`인지 확인
- Graph View 새로고침

#### 2. 그래프가 너무 복잡함
- 필터링으로 특정 그룹만 표시
- `hideUnresolved`를 `true`로 설정
- `repelStrength`를 증가

#### 3. 성능이 느림
- `showTags`를 `false`로 설정
- `nodeSizeMultiplier`를 감소
- 불필요한 색상 그룹 제거

### 고급 문제 해결

#### 1. 메모리 사용량 과다
```json
{
  "collapse-filter": true,
  "showOrphans": false,
  "nodeSizeMultiplier": 0.6
}
```

#### 2. 렌더링 깨짐
- Graph View 재시작
- Obsidian 재시작
- 설정 파일 재생성

---

## 📞 유지보수

### 정기 작업
1. **월간**: 색상 그룹 검토 및 업데이트
2. **분기별**: 성능 최적화 점검
3. **반기별**: 구조 재설계 검토

### 모니터링 항목
- 색상 일관성
- 성능 지표
- 사용자 피드백
- 구조 변화

---

*이 가이드는 CNT 프로젝트의 Graph View 시각화를 최적화하기 위해 작성되었습니다.*
