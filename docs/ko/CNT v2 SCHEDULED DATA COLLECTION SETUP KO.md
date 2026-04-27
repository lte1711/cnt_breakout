---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - cnt-v2-scheduled-data-collection-setup-ko
---

# CNT v2 예약 데이터 수집 설정

## 1. `run.ps1` 최종 형태

scheduler 대응 버전의 `run.ps1`은 아래를 수행합니다.

* repo root로 이동
* `data`, `logs` 폴더가 없으면 생성
* `data/engine.lock`으로 중복 실행 방지
* stdout/stderr를 아래 파일로 분리
  * `logs/scheduler_stdout.log`
  * `logs/scheduler_stderr.log`
* `scheduler_start`, `scheduler_finish`, lock skip 기록

## 2. Windows Task Scheduler 값

Program:

```text
powershell.exe
```

Arguments:

```text
-ExecutionPolicy Bypass -File "C:\cnt\run.ps1"
```

Start in:

```text
C:\cnt
```

## 3. 권장 Task 설정

General:

* task name: `CNT v2 Scheduler`
* run whether user is logged on or not
* run with highest privileges

Trigger:

* daily
* repeat every `10 minutes`
* indefinitely

Settings:

* start when available
* if task is already running: `Do not start a new instance`

## 4. PowerShell 등록 명령

```powershell
$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument '-ExecutionPolicy Bypass -File "C:\cnt\run.ps1"' `
    -WorkingDirectory "C:\cnt"

$Trigger = New-ScheduledTaskTrigger -Daily -At 00:00
$Trigger.Repetition = (New-ScheduledTaskTrigger -Once -At (Get-Date).Date -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration ([TimeSpan]::MaxValue)).Repetition

$Settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopIfGoingOnBatteries `
    -AllowStartIfOnBatteries `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName "CNT v2 Scheduler" `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Run CNT v2 every 10 minutes for data collection"
```

필요하면 기존 task를 먼저 제거:

```powershell
Unregister-ScheduledTask -TaskName "CNT v2 Scheduler" -Confirm:$false
```

## 5. 등록 전 수동 검증

```powershell
cd C:\cnt
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

확인 항목:

* `logs\scheduler_stdout.log`
* `logs\scheduler_stderr.log`
* `logs\portfolio.log`
* `data\performance_snapshot.json`
* `data\live_gate_decision.json`

## 6. 운영 규칙

충분한 표본이 쌓이기 전 상태:

```text
STATUS = PERFORMANCE_VALIDATION_IN_PROGRESS
```

금지:

* ranker weight 튜닝
* risk parameter 변경
* 전략 제거

허용:

* 명백한 버그 수정만 허용

---

## Obsidian Links

- [[CNT v2 TESTNET PERFORMANCE REPORT KO]]


