---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/validation
  - risk
  - obsidian
  - type/analysis
  - cnt-v2-live-readiness-report-ko
---

# CNT v2 라이브 준비도 보고서

```text
DOCUMENT_NAME = cnt_v2_live_readiness_report_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = NOT_READY
REFERENCE_1   = CNT v2 LIVE READINESS GATE
REFERENCE_2   = CNT v2 PERFORMANCE VALIDATION REPORT
REFERENCE_3   = CNT v2 TESTNET DATA COLLECTION STATUS REPORT
```

## 1. 요약

이 문서는 당시 CNT v2 testnet 증거를 바탕으로 라이브 준비도를 평가한 결과다.

최종 결과:

- live 전환 승인 안 됨
- 자본 배분 판단 금지
- 프로젝트는 라이브 배포가 아니라 데이터 수집 단계로 돌아가야 함

## 2. 사전조건 점검

### 필수 사전조건

```text
closed_trades >= 50                    = FAIL
operation_period >= 3 days             = FAIL
strategy_metrics.json persistence      = PASS
portfolio.log field recording          = PASS
risk policy live trigger evidence      = FAIL
```

즉시 판정:

- preconditions not satisfied

## 3. 성능 게이트 점검

### 수익성

```text
Net PnL    = not measurable yet
Expectancy = not measurable yet
```

결과:

- 표본 부족으로 FAIL

### 안정성

```text
max_consecutive_losses          = not measurable yet
daily_loss_limit_trigger_count  = not measurable yet
cooldown_trigger_count          = not measurable yet
```

결과:

- 표본 부족으로 FAIL

### 분포 건강성

```text
single-strategy concentration = not measurable yet
multi-strategy execution      = not observed yet
```

결과:

- 표본 부족으로 FAIL

### 리스크 정책 검증

live-like 운영 로그 기준 관측 결과:

- `LOSS_COOLDOWN` = 미관측
- `DAILY_LOSS_LIMIT` = 미관측
- `MAX_PORTFOLIO_EXPOSURE` = 미관측
- `ONE_PER_SYMBOL_POLICY` = 미관측

결과:

- live-readiness 기준으로 FAIL

### Ranker 검증

확인된 것:

- `rank_score` 필드 존재
- `rank_score_components` 필드 존재

당시 운영 표본에서 아직 확인되지 않은 것:

- expectancy-adjusted live ranking behavior

결과:

- PARTIAL

## 4. 최종 결정

```text
STATUS   = NOT_READY
DECISION = RETURN_TO_TUNING
GO_LIVE  = NO
REASON   = PRECONDITIONS_NOT_MET
```

최소 표본과 gate evidence가 충족되기 전까지 CNT v2를 live trading으로 옮기면 안 된다.

## 링크

- CNT v2 LIVE READINESS REPORT
- CNT v2 LIVE READINESS GATE KO
- CNT v2 CURRENT STATUS ASSESSMENT KO

## Obsidian Links

- [[CNT v2 LIVE READINESS GATE KO]]


