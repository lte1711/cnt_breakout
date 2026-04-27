---
aliases:
  - CNT Version Classification And Color Coding Guide
---

# CNT 버전 분류 및 색상 코딩 가이드

## 개요

CNT 프로젝트의 모든 문서를 버전별로 분류하고 색상 코딩을 통해 시각적 구분을 제공하는 가이드입니다.

---

##  버전 분류 체계

###  v1.x 시리즈 (초기 단일 전략)
**상태**:  **완료 및 보관**
**특징**: 단일 전략 엔진, 기본 구조 확립

#### v1.0 (기초)
- **문서**: 없음 (초기 개념 단계)
- **색상**:  **노란색** (개념 단계)

#### v1.1 (안정화)
- **문서**: `CNT v1.1 *`
- **색상**:  **녹색** (안정화 완료)
- **주요 문서**:
  - `CNT v1.1 ARCHITECTURE DESIGN DOCUMENT.md`
  - `CNT v1.1 IMPLEMENTATION VALIDATION REPORT.md`
  - `CNT v1.1 STAGE 2 ARCHITECTURE DESIGN DOCUMENT.md`

---

###  v2.x 시리즈 (멀티 전략 확장)
**상태**:  **현재 운영 중**
**특징**: 멀티 전략 엔진, 포트폴리오 관리, 자동화

#### v2.0 (아키텍처 설계)
- **문서**: `CNT v2 ARCHITECTURE DESIGN DOCUMENT.md`
- **색상**:  **파란색** (설계 단계)

#### v2.1 (구현 및 검증)
- **문서**: `CNT v2 *` (대부분)
- **색상**:  **주황색** (구현 단계)
- **주요 카테고리**:
  - 아키텍처 및 설계
  - 구현 검증
  - 성능 튜닝
  - 운영 프로토콜

#### v2.2 (자동화 및 최적화)
- **문서**: `CNT v2 *` (최신)
- **색상**:  **보라색** (자동화 단계)
- **주요 기능**:
  - Obsidian 자동화
  - 실시간 모니터링
  - 독립형 대시보드

---

###  v3.x 시리즈 (미래 확장)
**상태**:  **개발 예정**
**특징**: 고급 기능, AI 통합, 완전 자동화

#### v3.0 (차세대)
- **문서**: `CNT V3 *`
- **색상**:  **빨간색** (개발 예정)

---

##  색상 코딩 시스템

### 주요 색상 정의

| 색상 | 버전 | 의미 | 상태 | 이모지 |
|------|------|------|------|-------|
|  **녹색** | v1.1 | 완료 및 보관 |  안정 |  |
|  **파란색** | v2.0 | 설계 완료 |  설계 |  |
|  **주황색** | v2.1 | 구현 및 운영 |  진행 중 |  |
|  **보라색** | v2.2 | 자동화 완료 |  자동화 |  |
|  **빨간색** | v3.0 | 개발 예정 |  예정 |  |
|  **노란색** | v1.0 | 개념 단계 |  아이디어 |  |

### 보조 색상

| 색상 | 용도 | 의미 |
|------|------|------|
|  **흰색** | 일반 문서 | 범용 |
|  **검정색** | 기술 문서 | 핵심 |
|  **회색** | 보조 문서 | 참고 |

---

##  문서 분류 매트릭스

### v1.x 문서 목록
```
 CNT v1.1 ARCHITECTURE DESIGN DOCUMENT.md
 CNT v1.1 IMPLEMENTATION VALIDATION REPORT.md
 CNT v1.1 IMPLEMENTATION WORK INSTRUCTION.md
 CNT v1.1 STAGE 2 ARCHITECTURE DESIGN DOCUMENT.md
 CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION REPORT.md
 CNT v1.1 STAGE 2 IMPLEMENTATION WORK INSTRUCTION.md
```

### v2.x 문서 분류

####  v2.0 (설계)
```
 CNT v2 ARCHITECTURE DESIGN DOCUMENT.md
 CNT v2 ENGINEERING PHASE PLAN.md
 CNT v2 STRATEGIC ANALYSIS PLAN.md
```

####  v2.1 (구현 및 운영)
```
 CNT v2 BREAKOUT * (모든 breakout 관련 문서)
 CNT v2 CURRENT STATUS ASSESSMENT.md
 CNT v2 LIVE READINESS GATE.md
 CNT v2 LIVE READINESS REPORT.md
 CNT v2 PERFORMANCE VALIDATION REPORT.md
 CNT v2 VALIDATION REPORT.md
```

####  v2.2 (자동화)
```
 CNT v2 OBSIDIAN INTEGRATED OPERATING PROTOCOL.md
 CNT v2 OBSIDIAN REVIEW WORKFLOW GUIDE.md
 CNT v2 OBSERVABILITY IMPLEMENTATION REPORT.md
 CNT v2 OBSIDIAN PLUGIN POLICY.md
```

###  v3.x 문서 (예정)
```
 CNT V3 OBSERVATION INTERPRETATION GUIDE.md
 [향후 v3.0 관련 문서들]
```

---

##  태그 시스템

### 버전 태그
```yaml
tags:
  - cnt/v1.1          # v1.1 문서
  - cnt/v2.0          # v2.0 문서
  - cnt/v2.1          # v2.1 문서
  - cnt/v2.2          # v2.2 문서
  - cnt/v3.0          # v3.0 문서
```

### 상태 태그
```yaml
tags:
  - status/completed  # 완료
  - status/active     # 활성
  - status/planned    # 계획됨
  - status/archived   # 보관됨
```

### 유형 태그
```yaml
tags:
  - type/architecture # 아키텍처
  - type/implementation # 구현
  - type/validation   # 검증
  - type/automation   # 자동화
  - type/operation     # 운영
```

---

##  Obsidian Canvas 색상 구성

### Canvas 노드 색상
```javascript
// Canvas 색상 설정
{
  "v1.1": "#4CAF50",    // 녹색
  "v2.0": "#2196F3",    // 파란색
  "v2.1": "#FF9800",    // 주황색
  "v2.2": "#9C27B0",    // 보라색
  "v3.0": "#F44336",    // 빨간색
  "general": "#9E9E9E"   // 회색
}
```

### Canvas 연결선 색상
- **녹색**: 완료된 흐름
- **파란색**: 설계 흐름
- **주황색**: 운영 흐름
- **보라색**: 자동화 흐름
- **빨간색**: 개발 예정 흐름

---

##  Dataview 쿼리 예시

### 버전별 문서 조회
```dataview
TABLE
  file.mtime as "수정일시",
  file.size as "크기"
FROM "docs"
WHERE contains(file.name, "v1.1")
SORT file.mtime DESC
```

### 색상별 그룹화
```dataview
LIST
FROM "docs"
WHERE any(tags, (t) => contains(t, "v2.1"))
GROUP BY file.folder
```

### 상태별 필터링
```dataview
TABLE
  status as "상태",
  priority as "우선순위"
FROM "docs"
WHERE contains(tags, "status/active")
SORT priority DESC
```

---

##  문서 명명 규칙

### 버전별 접두사
```
v1.1: "CNT v1.1 [문서유형]"
v2.0: "CNT v2.0 [문서유형]"
v2.1: "CNT v2.1 [문서유형]"
v2.2: "CNT v2.2 [문서유형]"
v3.0: "CNT v3.0 [문서유형]"
```

### 문서 유형 분류
```
ARCHITECTURE DESIGN DOCUMENT     # 아키텍처 설계
IMPLEMENTATION VALIDATION REPORT # 구현 검증 보고
OPERATION DISCIPLINE            # 운영 규율
AUTOMATION TOOLS USAGE GUIDE    # 자동화 도구 사용 가이드
PERFORMANCE VALIDATION REPORT   # 성능 검증 보고
```

---

##  적용 가이드

### 1. 새 문서 생성 시
1. 버전 결정 (v1.1, v2.0, v2.1, v2.2, v3.0)
2. 해당 색상 이모지 추가
3. 버전 태그 추가
4. 상태 태그 추가
5. 유형 태그 추가

### 2. 기존 문서 수정 시
1. 버전 재확인
2. 색상 업데이트
3. 태그 검증
4. 상태 변경 시 태그 업데이트

### 3. Canvas 업데이트 시
1. 노드 색상 설정
2. 연결선 색상 구성
3. 버전별 그룹화
4. 상태별 시각화

---

##  진행 상태 추적

### 현재 버전 분포
- **v1.1**:  6개 문서 (완료)
- **v2.0**:  3개 문서 (설계 완료)
- **v2.1**:  85개 문서 (운영 중)
- **v2.2**:  15개 문서 (자동화 진행 중)
- **v3.0**:  1개 문서 (개발 예정)

### 전체 문서 수: **110개**

---

##  미래 계획

### 단기 목표
- v2.2 자동화 문서 완성
- v3.0 기초 설계 시작
- Canvas 시각화 완성

### 장기 목표
- v3.0 완전 자동화 시스템
- AI 통합 기능
- 클라우드 배포

---

##  유지보수

### 정기 작업
1. 월간 문서 분류 검토
2. 분기별 색상 코딩 업데이트
3. 반기별 버전 상태 평가

### 책임자
- **문서 관리**: 시스템 관리자
- **버전 관리**: 기술 리드
- **색상 코딩**: UI/UX 담당자

---

*이 가이드는 CNT 프로젝트의 체계적인 문서 관리를 위해 작성되었습니다.*

## Obsidian Links

- [[CNT TOOLCHAIN INTEGRATION REPORT]]

