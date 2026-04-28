---
title: 소규모 실거래 + 병행 검증 실행 가이드
date: 2026-04-28
status: READY
---

## 현재 상태 (확정)

| 항목 | 값 |
|------|-----|
| 폐장된 거래 | 53 개 |
| 기대값 | +0.000614 |
| 승률 | 52.83% |
| LIVE_GATE | LIVE_READY |
| 목표 거래 | 60 개 (7개 추가 필요) |

---

## 준비 완료 항목

✔ **성능 스냅샷 필터링 완료**
- breakout_v1 제외됨 (비활성화 전략)
- pullback_v1 순수 데이터만 집계

✔ **자동화 검증 시스템 준비**
- `mini_evaluator.py` - 5거래 단위 평가
- `live_monitor.py` - 실시간 상태 추적
- `auto_check.py` - 통합 자동 평가

✔ **실거래 + 검증 워크플로우**
- `trade_with_validation.ps1` - 자동화 스크립트

---

## 실행 방법

### Option 1: 단일 거래 + 검증

```powershell
# 1거래 실행 후 자동평가
& .\run.ps1
python -m src.validation.auto_check
python -m src.validation.mini_evaluator
```

### Option 2: 연속 거래 + 검증 (권장)

```powershell
# 7거래 실행 (53 -> 60)
# 거래마다 자동 검증
# 거래 간 5분 대기
.\trade_with_validation.ps1 -NumTrades 7 -IntervalSeconds 300
```

### Option 3: DryRun 모드 (검증만, 거래 안 함)

```powershell
# 검증 시스템 테스트 (실제 거래 없음)
.\trade_with_validation.ps1 -NumTrades 7 -IntervalSeconds 10 -DryRun
```

---

## 실행 시간 예상

| 모드 | 1거래 | 7거래 |
|------|-------|-------|
| 단일 거래 + 검증 | ~3분 | N/A |
| 연속 거래 (5분 간격) | N/A | ~40분 |
| 연속 거래 (1분 간격) | N/A | ~10분 |
| DryRun (검증만) | ~1분 | ~7분 |

---

## 검증 대시보드

### Mini Evaluation 출력

```
Timestamp: 2026-04-28 15:04:18
Progress: 53/60 trades (88.3%)
pullback_v1 trades: 53

Expectancy: 0.000614
Win Rate: 0.5283 (28W/25L)
Net PnL: 0.03256400 USDT
Profit Factor: 1.0911

LIVE_GATE Status: LIVE_READY

Passed: 4/4
Status: PASS
```

### Live Monitor 출력

```
System Status: stopped
Pending Order: (None)
Open Trade: (None)
Portfolio Exposure: 0.0
Daily Loss Count: 3
Consecutive Losses: 2
```

---

## 모니터링 포인트

### 각 거래 후 확인 사항

✔ **Expectancy 안정성**
- 목표: >= +0.0006
- 허용 범위: +0.0004 ~ +0.0008
- 주의: -0.0001 이상이면 검토

✔ **Win Rate 추이**
- 최소: > 50%
- 목표: > 52%
- 허용 범위: 50% ~ 55%

✔ **Risk Guards 작동**
- Daily Loss Count: 최대 3 (정상)
- Consecutive Losses: 최대 2 (정상)
- 초과 시: 자동 차단 확인

✔ **LIVE_GATE 상태**
- 유지: LIVE_READY
- 변동 감시: NOT_READY / FAIL 발생 시 즉시 중단

---

## 예상 결과 (60 거래)

```
Expectancy: ~+0.0006 (안정화)
Win Rate: ~52-53%
Net PnL: ~+0.032-0.040 USDT
Profit Factor: ~1.09-1.10
```

---

## 장애 대응

### Scenario 1: Expectancy 급락

```
현상: 통상 +0.0006 에서 급락
원인: 연속 손실 발생
대응:
  1. 현재 LIVE_GATE 상태 확인
  2. 신호 품질 검증
  3. 시스템 로그 검토
  4. 필요시 일시 중지
```

### Scenario 2: Risk Guard 트리거

```
현상: Daily Loss Count 또는 Consecutive Losses 초과
원인: 리스크 엔진 정상 작동 (의도된 차단)
대응:
  1. 쿨다운 대기
  2. 상태 자동 복구 대기
  3. 리스크 로그 검토
```

### Scenario 3: LIVE_GATE 상태 변경

```
현상: LIVE_READY -> NOT_READY / FAIL
원인: 데이터 품질 악화
대응:
  1. 즉시 거래 중단
  2. Mini evaluation 결과 검토
  3. 신호 품질 분석
  4. 위원회 검토
```

---

## 다음 단계

### 60 거래 도달 시

1. **최종 Mini Evaluation**
   - 모든 4/4 체크 통과 확인
   - expectancy 안정성 재확인

2. **FULL_FILTER_RERUN × 3**
   - 60-70 거래 구간에서 필터 최적화
   - 신호 품질 재평가

3. **배포 판정**
   - 50-70 거래 범위 최종 검증
   - 실거래 배포 승인

---

## 타임라인

```
Day 1 (28일):
  - 자동화 시스템 활성화
  - 1-2거래 테스트
  - 검증 프로세스 확인

Day 2 (29일):
  - 지속적 거래 (54-58)
  - 정기 Mini evaluation
  - 신호 품질 모니터링

Day 3 (30일):
  - 마지막 거래 (59-60)
  - 최종 평가
  - 배포 판정
```

---

## 체크리스트

### 시작 전

- [ ] `trade_with_validation.ps1` 실행 가능 확인
- [ ] 로그 디렉토리 존재 확인
- [ ] 데이터 파일 백업 준비
- [ ] Testnet API 연결 확인

### 실행 중

- [ ] 매 거래 후 Mini eval 모니터링
- [ ] LIVE_GATE 상태 유지 (LIVE_READY)
- [ ] Expectancy 추이 기록
- [ ] 예상 밖의 결과 로깅

### 완료 후

- [ ] 60 거래 달성 확인
- [ ] 최종 평가 리포트 생성
- [ ] FULL_FILTER_RERUN 준비
- [ ] 배포 판정 회의

---

## 문서 참조

- [2026-04-28-SMALL_TRADE_VALIDATION_PLAN.md](2026-04-28-SMALL_TRADE_VALIDATION_PLAN.md) - 전체 계획
- [00 Docs Index.md](00%20Docs%20Index.md) - 문서 목록
- [CNT AUTO DASHBOARD.md](CNT%20AUTO%20DASHBOARD.md) - 자동화 대시보드

