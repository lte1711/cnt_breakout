---
tags:
  - cnt
  - type/documentation
  - status/active
  - post-logging
  - type/operation
  - strategy/breakout_v3
  - type/analysis
  - cnt-v2-logs-folder-hygiene-report-ko
---

# CNT v2 logs 폴더 정합성 보고서

## 요약

이번 점검은 현재 `logs/` 아래 존재하는 모든 파일을 검토했습니다.

결과:

- 명확히 잘못된 runtime log target은 발견되지 않음
- 실제 문제는 `logs/scheduler_stdout.log`였음
- 이 파일에는 외부 process redirection 때문에 혼합 인코딩 내용이 들어 있었음
- `run.ps1`를 강화해 이후 scheduler stdout/stderr 기록이 UTF-8로 유지되도록 수정함
- 기존 `scheduler_stdout.log` 내용도 embedded NUL byte 제거 방식으로 정리함

## 점검한 파일

`logs/`에서 확인한 파일:

- `breakout_completion_alert.log`
- `breakout_review_timer.log`
- `portfolio.log`
- `runtime.log`
- `scheduler_stderr.log`
- `scheduler_stdout.log`
- `shadow_breakout_v2.jsonl`
- `signal.log`

## 유효한 파일

아래 파일들은 현재 저장소 설계와 script reference 기준으로 모두 유효합니다.

- `runtime.log`
- `signal.log`
- `portfolio.log`
- `shadow_breakout_v2.jsonl`
- `scheduler_stdout.log`
- `scheduler_stderr.log`
- `breakout_completion_alert.log`
- `breakout_review_timer.log`

이유:

- `runtime.log`, `signal.log`, `portfolio.log`는 AGENTS.md baseline에 포함됨
- `shadow_breakout_v2.jsonl`은 `config.py`에 정의됨
- `scheduler_stdout.log`, `scheduler_stderr.log`는 `run.ps1`에서 생성됨
- `breakout_completion_alert.log`는 `scripts/breakout_completion_alert.ps1`에서 생성됨
- `breakout_review_timer.log`는 `scripts/breakout_review_timer.ps1`에서 생성됨

## 실제 결함

### scheduler_stdout.log

관찰된 결함:

- `engine strategy v1 started` 같은 줄에 embedded NUL byte가 들어감
- 이 때문에 PowerShell과 일반 텍스트 리더에서 mojibake처럼 보이는 출력이 발생함

원인:

- `run.ps1`가 서로 다른 logging 경로를 혼용했음
  - scheduler marker는 `Add-Content`
  - Python stdout/stderr는 shell redirection
- 결과적으로 같은 파일 안에 혼합 인코딩이 들어갈 수 있었음

## 적용된 수정

### run.ps1

적용 사항:

- UTF-8 안전 log helper 추가
- scheduler marker append를 명시적 UTF-8 write로 교체
- 외부 process `1>>` / `2>>` redirection을 `System.Diagnostics.Process` 기반 capture로 교체
- stdout/stderr를 먼저 capture한 뒤 UTF-8 텍스트로 append하도록 변경

### 기존 scheduler_stdout.log

적용된 정리:

- embedded NUL byte 제거
- 파일을 일반 텍스트로 읽을 수 있는 상태로 정리

## 비결함 항목

### scheduler_stderr.log

현재 내용은 이전 scheduler run에서 남은 과거 Python path resolution error입니다.

해석:

- 현재 malformed file이 아니라 과거 증거입니다
- 별도 log rotation 정책을 도입하지 않는 한 유지해도 무방합니다

### breakout completion / review log

두 파일 모두 작고 유효하며 script 소유 파일입니다.

해석:

- stray file로 취급하면 안 됨
- 의도된 운영 산출물임

## 최종 결정

- `logs/`에는 알 수 없는 rogue file이 없었음
- 확인된 유일한 결함은 scheduler stdout 인코딩 손상이었음
- 이 결함은 아래 두 지점 모두에서 수정됨
  - source level (`run.ps1`)
  - existing file level (`scheduler_stdout.log`)

## Obsidian Links

- [[CNT v2 SCHEDULED DATA COLLECTION SETUP KO]]


