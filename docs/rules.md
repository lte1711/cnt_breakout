---
tags:
  - cnt
  - type/documentation
  - status/active
  - market-context
  - type/validation
  - type/operation
  - risk
  - status/completed
  - rules
---

# CNT v0.1 공식 운영 규칙

## 문서 정보

```text
STATUS=ACTIVE
PROJECT=CNT
VERSION=0.1
DOCUMENT=rules.md
UPDATED=2026-04-17
POLICY=BUILD_FROM_ZERO
ENTRY=run.ps1 -> main.py -> src/engine.py
DOC_PATH=cnt/docs/rules.md
```

---

## 1. 문서 목적

이 문서는 CNT v0.1의 공식 운영 기준이다.
모든 구성원은 작업 시작 전 이 문서를 확인해야 하며, 설계·구현·검증·보고는 본 문서를 기준으로 수행한다.

이 문서는 다음을 강제한다.

- 프로젝트 정체성
- 폴더 및 파일 네이밍 기준
- 공식 실행 경로
- 작업 순서
- 검증 기준
- 변경 통제 방식

---

## 2. 프로젝트 선언

```text
PROJECT_NAME=CNT
PROJECT_VERSION=0.1
PROJECT_MODE=BUILD_FROM_ZERO
OLD_PROJECT_POLICY=REFERENCE_ONLY
ARCHITECTURE_POLICY=SIMPLE_AND_MODULAR
PRIORITY=ENGINE_FIRST
VALIDATION=MANDATORY
```

### 선언 해석

- CNT는 새 프로젝트다.
- 기존 프로젝트는 참고 자료로만 사용한다.
- 기존 코드, 구조, 파일명은 그대로 복사하지 않는다.
- 모든 설계는 단순하고 유지보수 가능해야 한다.
- 전략보다 엔진 구조를 먼저 만든다.

---

## 3. 최상위 원칙

### RULE 1. 새 프로젝트 원칙

```text
CNT는 기존 프로젝트의 수정판이 아니다.
CNT는 처음부터 다시 만드는 독립 프로젝트다.
기존 프로젝트는 참고만 허용한다.
```

### RULE 2. 단순성 원칙

```text
모든 이름은 짧고 명확해야 한다.
이름만 보고 역할이 이해되어야 한다.
불필요하게 긴 이름과 과장된 이름을 금지한다.
```

### RULE 3. 단일 실행 경로 원칙

```text
공식 실행 경로는 하나만 둔다.
공식 실행 경로는 다음과 같다.
run.ps1 -> main.py -> src/engine.py
```

### RULE 4. 엔진 우선 원칙

```text
전략보다 엔진이 먼저다.
실행 구조, 상태, 로그, 검증 체계가 완성되기 전 전략 확장을 금지한다.
```

### RULE 5. 기록 우선 원칙

```text
모든 작업과 실행은 기록되어야 한다.
상태와 로그는 분리한다.
기록 없는 실행은 공식 실행으로 인정하지 않는다.
```

### RULE 6. 단계 진행 원칙

```text
한 번에 하나의 기능만 진행한다.
여러 기능을 동시에 설계하거나 구현하지 않는다.
한 단계가 검증되기 전 다음 단계로 넘어가지 않는다.
```

---

## 4. 네이밍 규칙

### 4-1. 폴더명 규칙

```text
- 소문자만 사용
- 짧고 명확하게 작성
- 역할 중심 이름 사용
```

### 4-2. 파일명 규칙

```text
- 소문자 사용
- 기능 중심 이름 사용
- 가능하면 한 단어 또는 두 단어 이내
- 버전, final, complete, fixed, merged 같은 누적 표현 금지
```

### 4-3. 허용 예시

```text
main.py
config.py
engine.py
market.py
signal.py
order.py
position.py
risk.py
state.py
logger.py
utils.py
run.ps1
```

### 4-4. 금지 예시

```text
auto_strategy_trading_v5_complete_final.py
super_advanced_execution_handler.py
completely_fixed_merged_runtime_final_v2.py
```

---

## 5. 폴더 구조 규칙

### 공식 기본 구조

```text
cnt/
├─ run.ps1
├─ main.py
├─ config.py
├─ requirements.txt
├─ README.md
├─ src/
│  ├─ engine.py
│  ├─ market.py
│  ├─ signal.py
│  ├─ strategy.py
│  ├─ order.py
│  ├─ position.py
│  ├─ risk.py
│  ├─ state.py
│  ├─ logger.py
│  └─ utils.py
├─ data/
│  ├─ state.json
│  └─ cache/
├─ logs/
│  ├─ runtime.log
│  ├─ trade.log
│  └─ error.log
├─ tests/
└─ docs/
   ├─ rules.md
   ├─ design.md
   └─ plan.md
```

### 구조 해석 규칙

```text
src   = 로직
data  = 상태와 내부 데이터
logs  = 실행 기록
tests = 검증 코드
docs  = 문서
```

### 금지

```text
- logs 안에 상태 파일 저장 금지
- data 안에 운영 문서 저장 금지
- docs 안에 실행 코드 저장 금지
- src 안에 임시 보고서 저장 금지
```

---

## 6. 실행 규칙

### 공식 실행 경로

```text
run.ps1 -> main.py -> src/engine.py
```

### 실행 원칙

```text
- 사용자는 항상 run.ps1로 시작한다.
- main.py는 파이썬 시작 진입점이다.
- src/engine.py는 엔진 제어를 담당한다.
```

### 금지

```text
- src/engine.py 직접 실행 금지
- 임시 실행 진입점 추가 금지
- 같은 역할의 run 파일 다중 생성 금지
```

---

## 7. 상태 및 로그 규칙

### 상태 파일

```text
PRIMARY_STATE=data/state.json
```

### 로그 파일

```text
RUNTIME_LOG=logs/runtime.log
TRADE_LOG=logs/trade.log
ERROR_LOG=logs/error.log
```

### 상태 규칙

```text
- state.json에는 현재 상태만 저장한다.
- 상태는 기계가 읽기 쉬운 형태로 유지한다.
- 상태 저장 형식은 JSON을 기본으로 한다.
```

### 로그 규칙

```text
- runtime.log는 시작, 종료, 루프, 주요 시스템 이벤트 기록용이다.
- trade.log는 진입, 청산, 주문, 체결 관련 기록용이다.
- error.log는 예외, 실패, 복구 시도 기록용이다.
```

### 금지

```text
- 로그 파일에 현재 상태를 덮어쓰기 형태로 저장 금지
- 상태 파일에 장문 로그 누적 금지
- 기록되지 않은 주문 흐름 인정 금지
```

---

## 8. 개발 규칙

### RULE 1. 파일 하나 = 역할 하나

```text
한 파일은 하나의 핵심 책임만 가진다.
여러 책임을 한 파일에 섞지 않는다.
```

### RULE 2. 의존성 최소화

```text
모듈 간 직접 의존은 최소화한다.
순환 참조를 금지한다.
```

### RULE 3. 작은 단위 구현

```text
기능은 작게 나눈다.
작게 설계하고, 작게 구현하고, 작게 검증한다.
```

### RULE 4. 임시 코드 통제

```text
임시 테스트 코드, 디버그 코드, 우회 코드는 작업 종료 전에 정리한다.
삭제하지 못하면 명확히 표시하고 문서에 남긴다.
```

---

## 9. 전략 규칙

### v0.1 허용 범위

```text
- 단순 조건 기반 전략
- MA
- EMA
- RSI
- 기본 필터 조합
```

### v0.1 금지 범위

```text
- 복잡한 다중 전략 동시 운용
- AI 모델 도입
- 외부 신호 혼합
- 설명하기 어려운 블랙박스 전략
```

### 전략 도입 조건

```text
전략은 엔진, 상태, 로그, 검증 구조가 먼저 준비된 후에만 추가한다.
```

---

## 10. 검증 규칙

### 필수 검증 항목

```text
- 실행 가능 여부
- 종료 가능 여부
- 상태 저장 여부
- 로그 기록 여부
- 오류 발생 여부
- 오류 발생 시 기록 여부
```

### 최소 통과 기준

```text
- run.ps1로 시작 가능해야 한다.
- main.py가 정상 호출되어야 한다.
- 엔진 시작 기록이 runtime.log에 남아야 한다.
- state.json이 생성 또는 갱신되어야 한다.
- 오류가 나면 error.log에 남아야 한다.
```

### 판정 원칙

```text
기록이 없으면 실행으로 인정하지 않는다.
검증이 없으면 완료로 인정하지 않는다.
```

---

## 11. 기존 프로젝트 참조 규칙

### 허용

```text
- 아이디어 참고
- 실패 사례 참고
- 운영 사고 사례 참고
- 로그 구조 참고
- 테스트 항목 참고
```

### 금지

```text
- 코드 복사
- 폴더 구조 복사
- 파일명 재사용
- 복잡한 레거시 흐름 이식
```

### 참조 기록 규칙

```text
기존 프로젝트에서 아이디어를 참고했으면 문서나 작업 기록에 참고 사실을 남긴다.
단, 코드 복사로 이어져서는 안 된다.
```

---

## 12. 작업 시작 절차

모든 작업은 아래 순서로 시작한다.

```text
1. rules.md 확인
2. 현재 작업 범위 정의
3. 이번 단계의 단일 기능 선택
4. 설계 작성
5. 구현 수행
6. 검증 수행
7. 결과 기록
```

### 작업 시작 체크 항목

```text
- 이번 작업은 한 기능만 다루는가?
- 파일명은 단순한가?
- 공식 실행 경로를 해치지 않는가?
- 상태와 로그를 분리했는가?
- 검증 방법이 준비되었는가?
```

---

## 13. 변경 통제 규칙

### 문서 변경 원칙

```text
rules.md는 공식 기준 문서다.
규칙 변경은 이유 없이 수행할 수 없다.
```

### 규칙 변경 시 필수 기록

```text
- 변경 날짜
- 변경 항목
- 변경 이유
- 영향 범위
```

### 권장 변경 기록 형식

```text
CHANGE_LOG:
- DATE=YYYY-MM-DD
- SECTION=...
- CHANGE=...
- REASON=...
```

---

## 14. 위반 금지 규칙

다음은 즉시 중단 및 수정 대상이다.

```text
- 복잡한 이름 사용
- 여러 실행 경로 생성
- 기존 코드 복사
- 상태와 로그 혼합
- 기록 없이 실행
- 검증 없이 완료 선언
- 구조 변경 후 문서 미반영
```

---

## 15. 적용 방식

모든 구성원은 반드시 다음 순서를 따른다.

```text
작업 전   -> rules.md 확인
작업 중   -> 규칙 준수
작업 후   -> 검증 및 위반 여부 점검
보고 시   -> 결과와 근거 기록
```

---

## 16. 최종 선언

```text
이 문서는 CNT v0.1의 공식 운영 기준이다.
규칙 위반 작업은 공식 작업으로 인정하지 않는다.
규칙 준수와 검증 기록이 있는 작업만 공식 작업으로 인정한다.
```

---

## 17. 저장 위치

```text
cnt/docs/rules.md
```

---

## Obsidian Links

- [[00 Docs Index]]

