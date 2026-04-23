---
tags:
  - cnt
  - docs
  - gate
  - validation
  - ko
aliases:
  - CNT v2 LIVE GATE ALIGNMENT REPORT KO
---

# CNT v2 라이브 게이트 정합성 보고서

## 요약

라이브 게이트가 `FAIL / COOLDOWN_NOT_OBSERVED`로 떨어졌던 원인을 코드와 데이터 기준으로 다시 검토한 결과,
문제는 성능 부족이 아니라 **게이트 판정 기준과 실제 리스크 로그 집계의 불일치**였다.

기존 로직은 `risk_trigger_stats.LOSS_COOLDOWN > 0`만 요구했다.

하지만 최신 운영 스냅샷에서는 `DAILY_LOSS_LIMIT`만 충분히 누적되어 있었고,
`LOSS_COOLDOWN`은 0이었다.

즉 기존 FAIL의 원인은:

- 수익성 부족이 아님
- 표본 부족이 아님
- 리스크 보호 계층 미동작이 아님
- 게이트가 리스크 보호 증거를 너무 좁게 해석한 상태였음

## 증거

### Snapshot Facts

- `closed_trades = 20`
- `expectancy = 0.002786549999999867`
- `net_pnl = 0.05573099999999734`
- `max_consecutive_losses = 2`
- `risk_trigger_stats.DAILY_LOSS_LIMIT = 80`
- `risk_trigger_stats.LOSS_COOLDOWN = 0`

### Previous Gate Result

- `status = FAIL`
- `reason = COOLDOWN_NOT_OBSERVED`

### 해석된 문제

실제 운영에서는 `DAILY_LOSS_LIMIT`도 분명한 리스크 보호 로직이다.
그런데 게이트는 `LOSS_COOLDOWN`만 요구했기 때문에 사실과 다른 FAIL을 만들고 있었다.

## 설계 보정

라이브 게이트의 리스크 보호 증거 조건은 아래처럼 정렬되었다.

- 기존: `LOSS_COOLDOWN`이 1회 이상 관측되어야 함
- 변경: 아래 중 하나라도 1회 이상 관측되면 리스크 보호 계층이 실제로 동작한 것으로 판정
  - `LOSS_COOLDOWN`
  - `DAILY_LOSS_LIMIT`

즉 기준이 `cooldown only`에서 `risk guard observed`로 보정되었다.

## 검증

### 코드 검증

- `python -m unittest discover -s tests -p "test_*.py"`
- 결과: `Ran 33 tests / OK`

- `python -m py_compile src\validation\live_gate_evaluator.py tests\test_live_gate.py scripts\generate_performance_report.py`
- 결과: `OK`

### Runtime Artifact 재생성

- `python scripts/generate_performance_report.py`

재생성 후 결과:

- `data/live_gate_decision.json`
  - `status = LIVE_READY`
  - `reason = ALL_GATES_PASSED`
  - `risk_trigger_stats = { LOSS_COOLDOWN: 0, DAILY_LOSS_LIMIT: 80 }`

## 최종 해석

이번 수정은 라이브 게이트를 느슨하게 만든 것이 아니다.

이것은 **실제 운영 보호 로직과 게이트 판정 기준을 일치시키는 정합성 수정**이다.

당시 CNT는 최신 스냅샷 기준으로:

- 표본 수 기준 충족
- 기대값 양수
- 순손익 양수
- 연속 손실 제한 충족
- 리스크 보호 로직 관측됨

상태였다.

## 링크

- [[CNT v2 LIVE GATE ALIGNMENT REPORT]]
- [[CNT v2 LIVE READINESS GATE KO]]
- [[CNT v2 CURRENT STATUS ASSESSMENT KO]]
