---
tags:
  - cnt
  - obsidian
  - version
  - visualization
  - setup
aliases:
  - CNT OBSIDIAN 버전 시각화 설정 KO
---

# CNT Obsidian 버전 시각화 설정

## 개요

CNT 프로젝트의 버전 분류 및 색상 코딩 시스템을 Obsidian에 적용하는 방법 안내

---

## 🎨 색상 코딩 적용

### 1. 문서명 색상 추가

#### v1.1 문서 (녹색 🟢)
```
🟢 CNT v1.1 ARCHITECTURE DESIGN DOCUMENT.md
🟢 CNT v1.1 IMPLEMENTATION VALIDATION REPORT.md
🟢 CNT v1.1 IMPLEMENTATION WORK INSTRUCTION.md
🟢 CNT v1.1 STAGE 2 ARCHITECTURE DESIGN DOCUMENT.md
🟢 CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION REPORT.md
🟢 CNT v1.1 STAGE 2 IMPLEMENTATION WORK INSTRUCTION.md
```

#### v2.0 문서 (파란색 🔵)
```
🔵 CNT v2 ARCHITECTURE DESIGN DOCUMENT.md
🔵 CNT v2 ENGINEERING PHASE PLAN.md
🔵 CNT v2 STRATEGIC ANALYSIS PLAN.md
```

#### v2.1 문서 (주황색 🟠)
```
🟠 CNT v2 BREAKOUT * (모든 breakout 관련)
🟠 CNT v2 CURRENT STATUS ASSESSMENT.md
🟠 CNT v2 LIVE READINESS GATE.md
🟠 CNT v2 LIVE READINESS REPORT.md
🟠 CNT v2 PERFORMANCE VALIDATION REPORT.md
🟠 CNT v2 VALIDATION REPORT.md
```

#### v2.2 문서 (보라색 🟣)
```
🟣 CNT v2 OBSIDIAN INTEGRATED OPERATING PROTOCOL.md
🟣 CNT v2 OBSIDIAN REVIEW WORKFLOW GUIDE.md
🟣 CNT v2 OBSIDIAN PLUGIN POLICY.md
🟣 CNT v2 OBSERVABILITY IMPLEMENTATION REPORT.md
```

#### v3.0 문서 (빨간색 🔴)
```
🔴 CNT V3 OBSERVATION INTERPRETATION GUIDE.md
🔴 [향후 v3.0 문서들]
```

---

## 🏷️ 태그 시스템 적용

### 1. 버전 태그
각 문서의 프론트매터에 버전 태그 추가:

```yaml
---
tags:
  - cnt/v1.1          # v1.1 문서
  - cnt/v2.0          # v2.0 문서
  - cnt/v2.1          # v2.1 문서
  - cnt/v2.2          # v2.2 문서
  - cnt/v3.0          # v3.0 문서
---
```

### 2. 상태 태그
```yaml
---
tags:
  - status/completed  # 완료
  - status/active     # 활성
  - status/planned    # 계획됨
  - status/archived   # 보관됨
---
```

### 3. 유형 태그
```yaml
---
tags:
  - type/architecture # 아키텍처
  - type/implementation # 구현
  - type/validation   # 검증
  - type/automation   # 자동화
  - type/operation     # 운영
---
```

---

## 📊 Dataview 쿼리 적용

### 1. 버전별 문서 목록
```dataview
TABLE
  file.mtime as "수정일시",
  file.size as "크기"
FROM "docs"
WHERE contains(file.name, "v2.1")
SORT file.mtime DESC
```

### 2. 색상별 그룹화
```dataview
LIST
FROM "docs"
WHERE any(tags, (t) => contains(t, "v2.1"))
GROUP BY file.folder
```

### 3. 상태별 필터링
```dataview
TABLE
  status as "상태",
  priority as "우선순위"
FROM "docs"
WHERE contains(tags, "status/active")
SORT priority DESC
```

### 4. 버전 분포 통계
```dataview
TABLE WITHOUT ID
  length(rows) as "문서 수"
FROM "docs"
FLATTEN file.tags as tag
WHERE startswith(tag, "cnt/v")
GROUP BY tag
```

---

## 🎨 Canvas 시각화 설정

### 1. 노드 색상 설정
Canvas에서 각 버전별 노드 색상 설정:

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

### 2. 연결선 색상
- **녹색**: 완료된 흐름
- **파란색**: 설계 흐름
- **주황색**: 운영 흐름
- **보라색**: 자동화 흐름
- **빨간색**: 개발 예정 흐름

### 3. Canvas 구조 예시
```
CNT SYSTEM (중앙)
├── 🟢 v1.1 (완료) → 📦 보관됨
├── 🔵 v2.0 (설계) → 🏗️ 기반
├── 🟠 v2.1 (운영) → ⚙️ 현재
├── 🟣 v2.2 (자동화) → 🤖 진행 중
└── 🔴 v3.0 (계획) → 🎯 미래
```

---

## 🔧 Obsidian 설정

### 1. 플러그인 설정
`.obsidian/community-plugins.json` 확인:
```json
[
  "dataview",
  "templater-obsidian"
]
```

### 2. 템플릿 업데이트
`templates/` 폴더의 템플릿에 버전 정보 추가:

#### observation_review.md
```yaml
---
type: observation_review
strategy: breakout_v3
version: v2.1
tags:
  - cnt/v2.1
  - type/validation
---
```

### 3. 워크스페이스 설정
`.obsidian/workspace.json`에 색상 테마 적용:
- 현재 테마: moonstone
- 글꼴 크기: 16px
- 네이티브 메뉴: 활성화

---

## 📋 적용 확인 체크리스트

### ✅ 기본 설정
- [ ] 버전 분류 가이드 읽기
- [ ] 색상 코딩 시스템 이해
- [ ] 태그 시스템 숙지

### ✅ 문서 적용
- [ ] 주요 문서에 색상 이모지 추가
- [ ] 버전 태그 추가
- [ ] 상태 태그 추가
- [ ] 유형 태그 추가

### ✅ Dataview 적용
- [ ] 버전별 쿼리 작성
- [ ] 상태별 필터 설정
- [ ] 통계 쿼리 확인

### ✅ Canvas 적용
- [ ] 노드 색상 설정
- [ ] 연결선 색상 구성
- [ ] 버전별 그룹화

### ✅ 테스트
- [ ] Dataview 쿼리 동작 확인
- [ ] 태그 필터링 확인
- [ ] Canvas 시각화 확인

---

## 🚀 자동화 적용

### 1. 스크립트 실행
```bash
# 버전 분류 보고서 생성
python scripts/version_classifier.py

# 결과 확인
cat "docs/CNT Version Classification Report.md"
```

### 2. 정기 업데이트
```bash
# 월간 실행 권장
python scripts/version_classifier.py

# 변경사항 커밋
git add docs/CNT*Classification*.md
git commit -m "Update version classification"
```

---

## 📈 효과 확인

### 1. 시각적 개선
- 색상으로 버전 즉시 식별
- 이모지로 상태 한눈에 파악
- Canvas에서 시각적 구분

### 2. 검색 효율
- 태그 기반 필터링
- Dataview 쿼리로 빠른 검색
- 버전별 문서 그룹화

### 3. 관리 효율
- 체계적인 문서 분류
- 자동화된 통계 관리
- 일관된 명명 규칙

---

## 🔧 문제 해결

### 일반적인 문제

#### 1. Dataview 쿼리 오류
```dataview
# 잘못된 쿼리
FROM "docs" WHERE contains(file.name, "v2.1")

# 올바른 쿼리
FROM "docs" WHERE contains(file.name, "v2.1")
```

#### 2. 태그 인식 문제
- 태그에 공백 없이 사용
- 소문자로 통일
- 슬래시(/) 구조 사용

#### 3. Canvas 색상 문제
- HEX 코드 정확히 입력
- 노드별 개별 설정
- 연결선 색상 구분

### 고급 문제 해결

#### 1. 대량 문서 일괄 처리
```python
# Python 스크립트로 일괄 처리
import os
from pathlib import Path

def add_version_tags(directory):
    for file_path in directory.rglob("*.md"):
        if "v2.1" in file_path.name:
            # 파일 내용 수정 로직
            pass
```

#### 2. Canvas 자동 설정
- JSON 설정 파일 직접 수정
- 스크립트로 자동 생성
- 템플릿으로 재사용

---

## 📞 지원

### 도움말
- Obsidian 공식 문서
- Dataview 문서
- Canvas 가이드

### 커뮤니티
- Obsidian Discord
- CNT 프로젝트 저장소
- GitHub Issues

---

*이 설정 가이드는 CNT 프로젝트의 버전 관리 시스템을 Obsidian에 완벽하게 적용하기 위해 작성되었습니다.*
