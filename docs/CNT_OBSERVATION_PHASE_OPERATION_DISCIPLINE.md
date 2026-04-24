# CNT Observation Phase 운영 규율

**목적**: Breakout_v3 shadow validation 단계에서 흔들리지 않是기 위한 운영 기준  
**적용 시점**: 2026-04-24 ~ Observation Review 완료 시까지  
**상태**: ACTIVE (모든 팀원 준수)

---

## 🔒 철칙 01: 절대 변경 금지 영역

### 다음은 100% 금지

```
❌ 전략 파라미터 수정 (어떤 것도)
   - EMA fast/slow period
   - RSI threshold / overheat
   - ATR / Bollinger band settings
   - Any other filter parameter

❌ Interval 변경
   - PRIMARY_INTERVAL = 5m 유지
   - ENTRY_INTERVAL = 1m 유지

❌ Filter 제거/추가
   - Soft pass 6개 filter 모두 유지
   - Setup ready 3단계 모두 유지

❌ Breakout_v1 weight 적용
   - 격리 결정 기록 있음 (아직 적용 금지)
   - Observation Review 후에만 적용

❌ 로그 구조 변경
   - shadow_breakout_v3_snapshot.json 포맷 변경 금지
   - first_blocker_distribution 기록 방식 변경 금지
```

### 위반 결과

```
데이터 오염 → 모든 분석 무효 → 재처음부터 시작
```

---

## ✅ 철칙 02: 허용되는 유일한 행동 3가지

### 1. run.ps1 실행 유지

```powershell
# 매일 실행 (또는 24/7 운영 중이면 유지)
./run.ps1
```

**확인 사항**:
- 에러 없이 실행되는가?
- snapshot 파일이 업데이트되는가?

---

### 2. Snapshot 파일 확인

```json
data/shadow_breakout_v3_snapshot.json
```

**확인 대상**:
- `signal_count` 증가 추이
- `allowed_signal_count` 변화
- `first_blocker_distribution` 구성

**도구**:
- 텍스트 에디터 또는 JSON viewer
- 변경 금지

---

### 3. 로그 누적 (수동 개입 금지)

```
logs/shadow_breakout_v3.jsonl
```

**특징**:
- 자동으로 기록됨
- 손대지 말 것
- Observation Review 시 분석 대상

---

## 📊 철칙 03: 관측 중 반드시 보는 3개 신호

### ① market_not_trend_up 감소 추이

#### 신호 위치
```
shadow_breakout_v3_snapshot.json
  └─ first_blocker_distribution
      └─ market_not_trend_up
```

#### 정상 변화 패턴

```
Event #1-13:
  market_not_trend_up: 13 (100%)

Event #14-25:
  market_not_trend_up: 12 (80%)
  range_bias_pass: 1 (8%) ← 처음 변화
  
Event #26+:
  market_not_trend_up: 8-10 (변동)
  trend_up_pass: 2-3 (증가)
```

#### 해석 기준

```
| 상태 | 의미 |
|------|------|
| 100% 유지 | 여전히 5m 추세 없음 (정상) |
| 100% → 90% | 시장 구조 변화 시작 ✓ |
| 100% → 50% | 강한 상방 신호 ✓ |
| 100% → 0% | 강하고 지속된 상방 |
```

---

### ② allowed_signal_count > 0 (첫 출현)

#### 신호 정의

```json
{
  "allowed_signal_count": 1,
  "signal_event_index": 18,
  "soft_pass": [5, 4, 6]
}
```

#### 의미

```
❗ "Breakout_v3가 실제 시장에서 거래 신호를 발생시킨 순간"
```

#### 기대 시점

```
데이터: 20~40 events 사이
확률: 30~60% (시장 조건에 따라)
반드시 아님: 50 event 이상 allowed=0 가능 (시장 문제)
```

#### 감정적 주의

```
⚠️ 위험: 첫 allowed > 0이 나오면 "성공했다!"고 생각하기 쉬움

✅ 올바른: 첫 > 0은 "조사 신호" 일 뿐
   → 10+ events 이상 같은 패턴 반복되어야 "정상"
```

---

### ③ soft_pass_count_distribution 품질 분포

#### 신호 위치

```
shadow_breakout_v3_snapshot.json
  └─ soft_pass_count_distribution
      ├─ "6": n
      ├─ "5": n
      ├─ "4": n
      ├─ "3": n
      ├─ "2": n
      ├─ "1": n
      └─ "0": n
```

#### 정상 범위

```json
{
  "5": 1,    ← rare (5%)
  "4": 2,    ← occasional (10%)
  "3": 4,    ← common (25-40%)
  "2": 3,    ← some (15-25%)
  "1": 2,    ← few (10%)
  "0": 1     ← rare (5%)
}
```

#### 해석

```
| soft_pass | 평가 | 의미 |
|-----------|------|------|
| 6/6 | 훌륭함 | 모든 필터 통과, 매우 강한 신호 |
| 5/6 | 양호 | 대부분 필터 통과 |
| 4/6 | 중간 | 절반 이상 통과, 정상 범위 |
| 3/6 | 기준 | 최소 기준선, 정상 |
| 2/6 | 약함 | 차단 기준 미만 |
| 0-1 | 아주 약함 | 품질 부족 |
```

#### 주의

```
⚠️ 실수: "3~4만 나와야 한다"고 고집하기

✅ 올바른: 
   - soft_pass >= 3인 비율 > 30% → 설계 정상
   - soft_pass >= 3인 비율 < 10% AND 30개 이상 → 재검토 대상
```

---

## ⚠️ 철칙 04: 가장 위험한 순간과 대응

### 상황 1: "20 Events, Still allowed = 0"

#### 발생 시점
```
Event 20: allowed_signal_count = 0
```

#### 위험한 생각 (100% 금지)

```
❌ "뭔가 잘못되지 않았을까?"
❌ "threshold 낮춰야 하나?"
❌ "filter 하나 빼야 하나?"
❌ "interval 변경해봐야 할까?"
```

#### 올바른 반응

```
✅ "데이터 더 필요"
✅ "30 events까지 계속 보자"
✅ "regime 신호 대기"
```

#### 이유

```
원인 분석 (가능성 순):

1. 시장 자체가 breakout regime이 아님
   → "파라미터 문제 아님"
   → "시장 신호 기다려야 함"

2. 샘플 너무 작음 (20개는 부족)
   → "통계적으로 의미 부족"
   → "30~50 필요"

3. 설정이 과보수 (가능성 낮음)
   → "이미 검증된 설계"
   → "50 event 이후 판단"
```

---

### 상황 2: "Regime Open 되었는데 still allowed = 0"

#### 증상
```
first_blocker_distribution: {
  market_not_trend_up: 8,
  range_bias_pass: 3,
  trend_up_pass: 2
}
allowed_signal_count: 0
```

#### 위험한 생각

```
❌ "regime은 열렸는데 entry 조건이 너무 빡빡한가?"
❌ "soft_pass threshold 3이 너무 높나?"
```

#### 올바른 해석 절차

**Step 1**: setup_ready 달성 이벤트 몇 개?

```
regime pass: 5개
setup_ready: 2개 (40%)

→ setup_ready 통과율 낮음
→ volatility 또는 vwap 조건 분석 필요
```

**Step 2**: setup_ready까지 간 이벤트의 soft_pass?

```
setup_ready 2개 중:
  soft_pass: 2, 1

→ soft_pass < 3 → 정상 처리 (차단 의도대로)
→ "설정 문제 아님"
```

**Step 3**: 결론

```
✅ "설계가 정상적으로 작동 중"
✅ "시장 조건이 까다로운 단계"
✅ "계속 관찰"
```

#### 절대 금지

```
❌ 30 event 전에 조정
❌ 강제로 soft_pass threshold 낮추기
❌ setup_ready 조건 완화
```

---

### 상황 3: "Soft Pass = 0 계속"

#### 증상
```
regime open: YES (8 events)
setup_ready: YES (4 events)
soft_pass:
  "3": 0
  "2": 0
  "1": 0
  "0": 4

→ allowed_signal_count = 0
```

#### 해석

```
setup_ready까지는 자주 도달
하지만 quality filter 6개 모두 실패

가능성:
1. 이 구간 시장의 특징
   - Bollinger band 확장 없음
   - Volume spike 없음
   → "시장 상태, 설정 아님"

2. 시장이 너무 횡보
   → "breakout 환경 아님"
   → "정상" (다른 전략 대기)
```

#### 대응

```
✅ "이것도 정상 동작"
✅ "계속 관찰"
✅ 50 event 후 최종 판단
```

---

## 📋 철칙 05: 체크리스트 (Daily)

### 매일 운영 확인

```markdown
### Daily Checklist

- [ ] run.ps1 정상 실행
- [ ] shadow_breakout_v3_snapshot.json 업데이트 확인
- [ ] signal_count 증가 중
- [ ] 에러 로그 없음
- [ ] config.py 변경 없음

**기록**: _______ (날짜)
          _______ (이벤트 수)
          _______ (allowed_signal_count)
          _______ (이상 사항)
```

### 매 20 Events 마다

```markdown
### Event Checkpoint

- [ ] first_blocker_distribution 확인
- [ ] allowed_signal_count 증가 여부
- [ ] soft_pass_distribution 패턴 확인
- [ ] setup_ready 통과율 계산
- [ ] 이상 신호 체크

**분석**: 
```

---

## 🔄 철칙 06: Observation Review 진입 기준

### Trigger 1: 30 Events + 신호 출현

```
조건:
├─ signal_count >= 30
└─ allowed_signal_count >= 1

→ Observation Review 작성 시작
```

### Trigger 2: 50 Events 도달

```
조건:
└─ signal_count >= 50

→ 신호 여부 무관하게 리뷰 작성
   (결론: "정상" 또는 "재검토 필요")
```

### Trigger 3: 이상 신호

```
조건:
└─ 50 event 이후에도 allowed = 0 AND regime = 0

→ "설계 재검토" 필요 가능성
→ 당시에 분석 후 결정
```

---

## 📌 철칙 07: Breakout_v1 격리 적용 절차

### 현재 상태

```
✔ 격리 결정 완료
✔ 문서화 완료 (CNT_BREAKOUT_V1_ISOLATION_DECISION.md)
⏳ 적용 보류
```

### 적용 시점

```
Observation Review 완성 AND
v3 검증 완료 (allowed_signal_count > 0 또는 50 event)

시점: 2026-04-27 이후 예상
```

### 적용 방식

```python
# config.py
STRATEGY_PARAMS = {
    "breakout_v1": {
        ...existing_params...,
        "weight": 0.0,  # ← 추가
    }
}
```

### 적용 후 검증

```
적용 직후:
├─ performance_snapshot.json 재생성
├─ Expectancy 값 확인 (기대: +0.0017)
└─ Live Gate 상태 확인 (기대: PASS)
```

---

## 🧠 철칙 08: 운영 사고방식

### 현재 단계의 본질

```
❌ "성능 개선 단계"
❌ "트레이딩 최적화"
❌ "수익 창출"

✅ "시스템 검증 단계"
✅ "설계 정당성 증명"
✅ "신뢰도 구축"
```

### 성공의 정의

```
❌ "allowed_signal 많이 나오기"
❌ "승률 높게 나오기"

✅ "설계대로 작동하는가?"
✅ "데이터가 일관성 있는가?"
✅ "이상 신호는 없는가?"
```

### 실패의 정의

```
❌ "0% 통과율"

✅ "무작위처럼 보이는 패턴"
✅ "설계와 다른 동작"
✅ "기록 불일치"
```

---

## 🚫 절대 금지 리스트 (한 번 더 강조)

```
❌ config.py 수정
❌ 전략 클래스 수정
❌ indicator 계산 방식 변경
❌ snapshot 포맷 변경
❌ 로그 구조 변경
❌ filter 개수 변경
❌ threshold 조정
❌ interval 변경
❌ weight 적용 (v1 만)
❌ parameter file 수정
```

→ **모두 Observation Review 완료 후**

---

## ✅ 최종 확인

이 문서를 읽었다면:

- [ ] Breakout_v3 파라미터 변경하지 않겠다
- [ ] 첫 allowed > 0 출현해도 흔들리지 않겠다
- [ ] 50 events까지 관찰할 것이다
- [ ] Observation Review 완료할 때까지 손 떼겠다
- [ ] Breakout_v1 격리는 Review 후에만 적용하겠다

---

**이 규율이 지켜져야만, 다음 단계 (적용)도 의미가 있습니다.**

**지금부터는 인내심이 최고의 능력입니다.**
