---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - type/operation
  - obsidian
  - type/analysis
  - status/completed
  - cnt-v2-scheduled-data-collection-setup-report-ko
---

# CNT v2 SCHEDULED DATA COLLECTION SETUP REPORT KO

```text
DOCUMENT_NAME = cnt_v2_scheduled_data_collection_setup_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = SCHEDULER_REGISTERED_AND_INITIAL_RUN_VERIFIED
```

## 1. 요약

이 보고서는 CNT v2 데이터 수집을 위한 scheduler setup과 초기 운영 검증을 추적한다.

구현된 것:

- scheduler-friendly `run.ps1`
- lock-file 기반 중복 실행 방지
- scheduler run용 stdout / stderr 분리
- setup 문서 저장
- Windows Task Scheduler 등록 완료
- 초기 scheduler execution 정상 검증

## 2. 수동 검증 결과

확인된 것:

- `run.ps1` 정상 실행
- `scheduler_stdout.log` 생성
- 수동 실행 중 `scheduler_stderr.log` 비어 있음
- `portfolio.log` 갱신
- `performance_snapshot.json` 갱신
- `live_gate_decision.json` 갱신

관찰:

```text
scheduler_finish exit_code=0
live_gate_decision = NOT_READY / INSUFFICIENT_SAMPLE
```

## 3. Task Scheduler 등록 결과

등록된 작업:

```text
TASK_NAME   = CNT v2 Scheduler
RUN_AS_USER = SYSTEM
COMMAND     = powershell.exe -ExecutionPolicy Bypass -File C:\cnt\run.ps1
INTERVAL    = every 10 minutes
STATUS      = Ready
LAST_RESULT = 0
```

초기 보정:

- 첫 SYSTEM 실행에서 Python path resolution issue 노출
- `run.ps1`를 concrete Python executable path를 우선 찾도록 보강
- 수정 후 scheduler launch `Last Result = 0`

## 4. 남은 확인 사항

- 20~30분 동안 2~3회 반복 실행 관찰
- lock-skip이 비정상적으로 많지 않은지 확인
- sample threshold 도달 전까지 runtime data 누적 지속

## 5. 현재 단계 결정

```text
SCHEDULER_STATUS = ACTIVE
DATA_COLLECTION  = STARTED
GATE_STATUS      = NOT_READY / INSUFFICIENT_SAMPLE
NEXT             = CONTINUE_AUTOMATED_COLLECTION_AND_OBSERVATION
```

## 링크

- CNT v2 SCHEDULED DATA COLLECTION SETUP KO
- CNT v2 NEXT PHASE PLAN KO
- CNT v2 AUTO VALIDATION & DECISION SYSTEM PROGRESS REPORT KO
- 00 Docs Index KO

## Obsidian Links

- [[CNT v2 TESTNET PERFORMANCE REPORT KO]]


