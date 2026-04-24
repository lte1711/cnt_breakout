---
tags:
  - cnt
  - docs
aliases:
  - DESIGN SUMMARY KO
---

# DESIGN SUMMARY KO

## STEP-ENGINE-STRATEGY-INTEGRATION-RESULT-1

### 목표

`strategy_signal` 기반 신규 BUY 진입 게이트를 `engine` 실행 흐름에 연결하고, 아래 경로를 실제 실행으로 검증하는 것이 목적이었다.

- 신규 진입 차단
- 신규 BUY 체결
- 보유 상태 유지
- 보호 스탑 발동
- 목표가 청산

### 단계 배치

1. `pending_order` 처리 우선
2. `open_trade` 처리 우선
3. target exit / stop exit 우선
4. 신규 BUY 직전에만 전략 게이트 적용
5. 테스트 종료 후 운영 모드로 복귀

### 적용 결과

- 전략 게이트 연결 완료
- 운영 기준 실행 체인 유지
- 테스트 종료 후 운영 상태 복귀 확인

## 링크

- [[RECORD TEXT KO]]
- [[00 Docs Index KO]]
