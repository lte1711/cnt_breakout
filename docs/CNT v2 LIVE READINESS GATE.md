---
tags:
  - cnt
  - docs
  - v2
  - gate
aliases:
  - CNT v2 LIVE READINESS GATE
---

# CNT v2 LIVE READINESS GATE

## Purpose

CNT v2의 Live 전환은 감이나 기대가 아니라 **실제 Testnet 표본과 리스크 동작 증거**로만 결정한다.

이 문서는 현재 시스템이 `GO LIVE`, `NOT_READY`, `LIVE_READY_WITH_GUARDRAILS` 중 어디에 해당하는지 판단하는 기준 문서다.

## Current Rule

아래 중 하나라도 충족하지 못하면 기본 판정은 `NOT_READY`다.

- `closed_trades >= 20`
- `net_pnl > 0`
- `expectancy > 0`
- 리스크 정책 로그가 실제로 관측됨
- selection / ranking / state persistence가 정상 동작함

## Readiness Criteria

### Sample Sufficiency

- `closed_trades >= 20`
- 운영 기간은 최소 3일 이상이 권장된다

### Profitability

- `net_pnl > 0`
- `expectancy > 0`
- `profit_factor > 1.0`

### Stability

- `max_consecutive_losses <= 5`
- `daily_loss_limit` 및 `cooldown` 계열 정책이 로그에서 실제 관측 가능해야 한다

### Strategy Diversity

- 단일 전략만 장기적으로 선택되는 구조는 Live 확대 전에 재검토한다
- 현재 단계에서는 `pullback_v1`가 주 운영 전략이고 `breakout_v1`는 품질 평가 전략이다

## Current Interpreted Status

최신 기준으로 CNT v2는 아래 상태다.

- `STATUS = NOT_READY`
- 주된 이유: `INSUFFICIENT_SAMPLE`
- `pullback_v1`는 의미 있는 Testnet 성과를 보이고 있음
- `breakout_v1`는 dead branch를 벗어났지만 아직 저표본 품질 평가 단계임

즉, 전략 성과와 Live 전환 판정은 분리해서 해석해야 한다.

## Decision Rule

### PASS

아래를 모두 만족하면 `LIVE_READY`

- 충분한 표본
- 양의 `net_pnl`
- 양의 `expectancy`
- 리스크 정책 실제 동작 증거

### CONDITIONAL PASS

아래를 만족하면 `LIVE_READY_WITH_GUARDRAILS`

- 표본은 충분
- 수익성은 양호
- 다만 전략 분산이나 리스크 로그 증거가 아직 약함

### FAIL

아래 중 하나라도 해당하면 `NOT_READY`

- 표본 부족
- 음수 `net_pnl`
- 음수 `expectancy`
- 리스크 정책 무증거
- ranking / selection / state persistence 이상

## Operating Note

현재 CNT v2의 가장 정확한 운영 해석은 아래와 같다.

- 시스템은 정상 운영 중
- Live 전환은 아직 이르다
- `pullback_v1` 표본 축적을 계속한다
- `breakout_v1`는 품질 평가를 계속한다

## Obsidian Links

- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT v2 CURRENT STATUS ASSESSMENT]]
- [[CNT v2 BREAKOUT FIRST TRADE REVIEW]]
- [[00 Docs Index|Docs Index]]
