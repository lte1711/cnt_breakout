# Breakout_v1 격리 결정 기록

**결정일**: 2026-04-24  
**상태**: DECISION RECORDED (미적용)  
**적용 시점**: First Observation Review 이후

---

## 결정 내용

### 조치: Breakout_v1 → weight = 0.0 (격리)

**이유:**
- Breakout_v1 단독 Expectancy: -0.0222 (심각한 음수)
- Profit Factor: 0.173 (1.0 미만)
- 35개 거래 중 3거래만 담당, 2 손실 1 승리
- 전체 시스템 Expectancy (-0.000335)를 직접 오염
- 현재 Live Gate FAIL의 직접 원인

### 격리 방식 (제거 아님)

| 항목 | 이유 |
|------|------|
| weight=0 유지 | 실행 영향 = 0 동시 로그 유지 |
| 데이터 보존 | v1 vs v3 비교 분석 가능 |
| 시간 가역성 | 언제든 weight 복구 가능 |

### 기대 효과

```
현재 상태:
- Expectancy: -0.000335 → FAIL
- Status: EXECUTION_BLOCKED_BY_RISK

적용 후 예상:
- Expectancy: +0.0017 근처 (Pullback_v1만 남음)
- Live Gate: PASS 가능성 높음
- New Trade 재개 가능
```

---

## 관찰 단계 의존성

### 현재 Observation 단계 (진행 중)
- Shadow Breakout_v3: 13 events 수집
- 목표: 30+ events (regime gate 검증 충분량)

### 적용 시점 기준

```
Trigger 1: Observation Review 완성
Trigger 2: 또는 Breakout_v3 regime gate 통과 확인

Whichever comes first
```

---

## Observation 중 추적 포인트

### A. V3 Regime 통과 여부
- `range_bias_pass` 출현 추적
- `first_blocker_distribution` 변화

### B. V3 Entry Quality 상태
- Soft Pass 분포 추이
- Setup Ready까지 도달 이벤트 수

### C. Pullback_v1 성능 검증
- Weight=0 격리 후 Pullback만의 Expectancy 재검증
- 예상: +0.0017 유지 확인

---

## 대안 평가 (검토됨)

| 옵션 | 평가 | 채택 |
|------|------|------|
| 완전 삭제 | 데이터 손실, 비교 불가 | ❌ |
| weight=0 격리 | 영향 제거, 데이터 유지, 가역성 | ✅ |
| weight 감소 | 여전히 음수 영향 존재 | ❌ |

---

## 코드 변경 스펙 (적용 시)

### 대상: config.py

```python
# Before:
STRATEGY_PARAMS = {
    "breakout_v1": {
        ...params...
    }
}

# After (적용 시):
STRATEGY_PARAMS = {
    "breakout_v1": {
        ...params...,
        "weight": 0.0,  # ← 추가 또는 설정
    }
}
```

### 또는 strategy_orchestrator.py

```python
# orchestrator에서 selection 시 weight 확인
if strategy_registry[name].weight == 0.0:
    skip_this_strategy()
```

**최종 적용 방식은 Observation Review 시 결정**

---

## Decision Log

- **2026-04-24 00:00** — Decision recorded
- **Result**: NON_IMMEDIATE (Observation phase 계속)
- **Next**: First Observation Review 시 적용

## Obsidian Links

- [[00 Docs Index]]
