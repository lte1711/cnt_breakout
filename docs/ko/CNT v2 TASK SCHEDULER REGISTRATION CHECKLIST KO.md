---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - obsidian
  - type/analysis
  - type/validation
  - status/completed
  - cnt-v2-task-scheduler-registration-checklist-ko
---

# CNT v2 작업 스케줄러 등록 체크리스트

문서 목적:
Windows Task Scheduler 설정이 올바른지 빠르게 검증하기 위한 체크리스트입니다.

문서 상태:
Execution Checklist / Must Pass Before Data Collection

---

# 1. 사전 점검

## 경로와 파일

* [x] `C:\cnt\run.ps1` 존재
* [x] `C:\cnt\main.py` 존재
* [x] `C:\cnt\src\engine.py` 존재
* [x] Python 실행 가능

## 폴더 구조

* [x] `C:\cnt\data` 존재
* [x] `C:\cnt\logs` 존재

## 수동 실행 테스트

* [x] `powershell -ExecutionPolicy Bypass -File .\run.ps1` 실행 성공
* [x] runtime error 없이 종료
* [x] `logs\portfolio.log` 갱신됨
* [x] `logs\scheduler_stdout.log` 생성됨
* [x] `data\performance_snapshot.json` 생성됨
* [x] `data\live_gate_decision.json` 생성됨

---

# 2. 작업 스케줄러 등록 체크리스트

## Task 기본값

* [x] task name: `CNT v2 Scheduler`
* [x] task registration completed

## Program 설정

* [x] program: `powershell.exe`
* [x] argument:

```text
-ExecutionPolicy Bypass -File "C:\cnt\run.ps1"
```

* [x] task command 기준 start in 경로 일치 확인

```text
C:\cnt
```

## General 탭

* [x] run whether user is logged on or not
* [x] run with highest privileges

## Trigger

* [x] daily trigger / one-time repeating scheduler path registered
* [x] repeat every `10 minutes`
* [x] indefinite repetition behavior configured

## Settings

* [x] start-missed-task behavior configured
* [x] 이미 실행 중이면 새 instance 시작 안 함

---

# 3. 즉시 실행 점검

* [x] scheduler에서 task가 정상 시작됨
* [x] scheduler last result가 success로 표시됨
* [x] stdout log에 `scheduler_start` 존재
* [x] stdout log에 `scheduler_finish exit_code=0` 존재
* [x] `scheduler_stderr.log`에는 과거에 수정된 Python-path 오류만 있고 현재 blocking error는 없음

---

# 4. 지속 관측

* [ ] 20~30분 동안 2~3회 scheduler run 관측
* [x] 초기 검증에서 중복 실행 없음
* [x] 초기 검증에서 lock file 생성/제거 정상
* [x] 성공 실행 시 snapshot / decision 파일이 갱신됨

---

# 5. 성공 상태

```text
SCHEDULER_STATUS = ACTIVE
DATA_COLLECTION  = STARTED
CURRENT_GATE     = NOT_READY / INSUFFICIENT_SAMPLE
```

---

## Obsidian Links

- [[CNT v2 TESTNET PERFORMANCE REPORT KO]]


