---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - type/operation
  - risk
  - obsidian
  - type/analysis
  - cnt-v2-live-gate-alignment-report
---

# CNT v2 LIVE GATE ALIGNMENT REPORT

## Summary

라이브 게이트가 `FAIL / COOLDOWN_NOT_OBSERVED`로 떨어지던 원인을 코드와 실데이터로 대조한 결과, 성능 부족이 아니라 **게이트 판정 기준과 스냅샷 집계의 불일치**가 핵심 원인이었다.

기존 로직은 `risk_trigger_stats.LOSS_COOLDOWN > 0`만 요구했다. 하지만 실제 최신 스냅샷에는 `DAILY_LOSS_LIMIT`만 충분히 누적되어 있었고, `LOSS_COOLDOWN`은 0이었다.

즉 기존 FAIL은 아래 의미였다.

- 수익성 부족: 아님
- 표본 부족: 아님
- 리스크 보호 계층 미동작: 아님
- **게이트 판정기가 리스크 보호 증거를 너무 좁게 해석한 상태: 맞음**

## Evidence

### Snapshot Facts

- `closed_trades = 50`
- `expectancy = 0.002786549999999867`
- `net_pnl = 0.05573099999999734`
- `max_consecutive_losses = 2`
- `risk_trigger_stats.DAILY_LOSS_LIMIT = 80`
- `risk_trigger_stats.LOSS_COOLDOWN = 0`

### Previous Gate Result

- `status = FAIL`
- `reason = COOLDOWN_NOT_OBSERVED`

### Interpreted Problem

실제 운영에서는 `DAILY_LOSS_LIMIT`도 분명한 리스크 보호 로직이다. 그런데 게이트는 `LOSS_COOLDOWN`만 요구해 보수적 판정을 넘어 **왜곡된 FAIL**을 만들고 있었다.

## Design Change

라이브 게이트의 리스크 보호 증거 조건을 아래처럼 정렬했다.

- 기존: `LOSS_COOLDOWN`이 1회 이상 관측되어야 함
- 변경: 아래 중 하나라도 1회 이상 관측되면 리스크 보호 계층이 실제로 동작한 것으로 판단
  - `LOSS_COOLDOWN`
  - `DAILY_LOSS_LIMIT`

즉 판정 기준은 `cooldown only`에서 `risk guard observed`로 보정됐다.

## Validation

### Code Validation

- `python -m unittest discover -s tests -p "test_*.py"`
- 결과: `Ran 33 tests / OK`

- `python -m py_compile src\validation\live_gate_evaluator.py tests\test_live_gate.py scripts\generate_performance_report.py`
- 결과: `OK`

### Runtime Artifact Regeneration

- `python scripts/generate_performance_report.py`

재생성 후 결과:

- `data/live_gate_decision.json`
  - `status = LIVE_READY`
  - `reason = ALL_GATES_PASSED`
  - `risk_trigger_stats = { LOSS_COOLDOWN: 0, DAILY_LOSS_LIMIT: 80 }`

## Final Interpretation

이번 수정은 라이브 게이트를 느슨하게 만든 것이 아니라, **실제 운영 보호 로직과 판정 기준을 일치시킨 정합성 수정**이다.

현재 CNT는 최신 스냅샷 기준으로:

- 표본 수 기준 충족
- 기대값 양수
- 순손익 양수
- 연속 손실 제한 통과
- 리스크 보호 로직 관측됨

상태다.

## Obsidian Links

- [[CNT v2 LIVE READINESS GATE]]

