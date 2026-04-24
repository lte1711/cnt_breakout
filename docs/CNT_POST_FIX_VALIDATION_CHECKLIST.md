# Shadow Evaluator 수정 후 검증 체크리스트

**목적**: Breakout_v3 shadow evaluator 코드 수정이 실제로 반영되었는지 확인  
**적용 시점**: 수정 후 run.ps1 재실행 후  
**예상 변화**: allowed_signal_count 0 → 1+ 증가, blocker 분포 변화

---

## 📋 검증 단계 1: 코드 확인 (재검증)

### Task 1.1: Shadow Evaluator 코드 상태 확인

**파일**: `src/shadow/breakout_v3_shadow_eval.py`  
**라인**: 63-76

```python
# ✅ 확인할 코드 (현재 수정 반영됨):
regime_fail_reasons: list[str] = []
if not conditions.market_bias_pass:
    regime_fail_reasons.append("market_not_trend_up")
regime = _stage_result(
    "regime",
    ["market_bias_pass"],  # ← 1개만 존재
    regime_fail_reasons,
)
```

**체크**:
- [ ] trend_up_pass 독립 체크 제거됨 ✓
- [ ] range_bias_pass 독립 체크 제거됨 ✓
- [ ] _stage_result 호출 시 ["market_bias_pass"]만 전달 ✓

### Task 1.2: 테스트 통과 확인

```bash
python -m pytest tests/ -v
```

**기대**:
```
51 passed in 0.6x
```

**체크**:
- [ ] 모든 테스트 pass
- [ ] 구조 변경 없음 (회귀 테스트 정상)

---

## 📊 검증 단계 2: Shadow 데이터 갱신 상태 확인

### Task 2.1: Snapshot 파일 타임스탬프 확인

현재 상태 (수정 전):
```
data/shadow_breakout_v3_snapshot.json
  - last_updated: 2026-04-24T05:14:05...
  - allowed_signal_count: 0
  - first_blocker_distribution:
    - market_not_trend_up: 13
    - trend_not_up: 2  ← 이건 이제 안 나와야 함
    - range_without_upward_bias: 2  ← 이것도 안 나와야 함
```

**확인 방법**:
```bash
# PowerShell
Get-Item c:\cnt\data\shadow_breakout_v3_snapshot.json | 
  Select-Object -Property LastWriteTime, Length
```

**기대**:
- LastWriteTime이 최근 시간 (지금으로부터 1시간 이내)
- 수정 직후 run.ps1 실행했다면 방금 시간

### Task 2.2: Snapshot 내용 구조 변화 확인

```bash
# PowerShell - 현재 snapshot 확인
Get-Content c:\cnt\data\shadow_breakout_v3_snapshot.json | 
  ConvertFrom-Json | 
  Select-Object -Property signal_count, allowed_signal_count, 
    @{N='blockers';E={$_.first_blocker_distribution}}
```

**기대 결과** (수정 후):
```json
{
  "signal_count": 17-20,
  "allowed_signal_count": 1-3,  ← 0이 아님
  "blockers": {
    "market_not_trend_up": 13-14,
    "setup_not_ready": 1,
    "trigger_fail": 0,
    "quality_fail": 0
  }
}
```

**없어야 하는 blocker**:
- [ ] "trend_not_up" 없음
- [ ] "range_without_upward_bias" 없음

### Task 2.3: 로그 파일 최신 항목 확인

```bash
# PowerShell - 최근 5개 이벤트 확인
Get-Content c:\cnt\logs\shadow_breakout_v3.jsonl | 
  Select-Object -Last 5 | 
  ConvertFrom-Json | 
  Select-Object -Property event_index, market_bias_pass, 
    trend_up_pass, range_bias_pass, first_blocker, allowed
```

**기대** (샘플):
```
event_index  market_bias_pass  trend_up_pass  range_bias_pass  first_blocker          allowed
-----------  ---------------  ------------- ---------------  -----------------      -------
13           true             false         true             (다른 단계로 옮겨감)  false/true
14           true             true          false            (다른 단계로 옮겨감)  false/true
15           false            false         false            market_not_trend_up     false
```

**체크**:
- [ ] 최근 이벤트에 "trend_not_up"이 first_blocker로 나타나지 않음
- [ ] 최근 이벤트에 "range_without_upward_bias"가 first_blocker로 나타나지 않음

---

## 🎯 검증 단계 3: 핵심 지표 변화

### Task 3.1: allowed_signal_count 변화 추적

**이전 (수정 전)**:
```json
{
  "signal_count": 15,
  "allowed_signal_count": 0,
  "allowed_signal_ratio": 0.0
}
```

**현재 (수정 후 예상)**:
```json
{
  "signal_count": 17+,
  "allowed_signal_count": 1+,
  "allowed_signal_ratio": 5%+
}
```

**확인**:
```bash
# PowerShell
$snapshot = Get-Content c:\cnt\data\shadow_breakout_v3_snapshot.json | ConvertFrom-Json
Write-Host "Signal Count: $($snapshot.signal_count)"
Write-Host "Allowed Count: $($snapshot.allowed_signal_count)"
Write-Host "Allowed Ratio: $($snapshot.allowed_signal_ratio)"
```

**체크**:
- [ ] allowed_signal_count > 0
- [ ] allowed_signal_ratio > 0.0

### Task 3.2: Soft Pass Distribution 변화

**전에**:
```json
{
  "soft_pass_count_distribution": {
    "0": 0,
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0
  }
}
```

**현재 (예상)**:
```json
{
  "soft_pass_count_distribution": {
    "3": 1,
    "4": 1,
    "5": 0
  }
}
```

**확인**:
```bash
$snapshot = Get-Content c:\cnt\data\shadow_breakout_v3_snapshot.json | ConvertFrom-Json
$snapshot.soft_pass_count_distribution | ConvertTo-Json
```

**체크**:
- [ ] 3 이상의 soft_pass 이벤트 1개 이상 존재

---

## 🔄 검증 단계 4: 블로커 분포 구조 변화

### Task 4.1: First Blocker Distribution 검토

**수정 전 (현재)**:
```json
{
  "first_blocker_distribution": {
    "market_not_trend_up": 13,
    "trend_not_up": 2,
    "range_without_upward_bias": 2
  }
}
```

**수정 후 예상**:
```json
{
  "first_blocker_distribution": {
    "market_not_trend_up": 13,
    "setup_not_ready": 1-2,
    "volatility_floor_fail": 0-1,
    "quality_fail": 0-1
  }
}
```

**확인**:
```bash
$snapshot = Get-Content c:\cnt\data\shadow_breakout_v3_snapshot.json | ConvertFrom-Json
"=== First Blocker Distribution ==="
$snapshot.first_blocker_distribution | Format-Table

"=== Regime Stage Results ==="
$snapshot.stage_fail_counts.regime
```

**체크**:
- [ ] "trend_not_up" 0개 (제거됨)
- [ ] "range_without_upward_bias" 0개 (제거됨)
- [ ] "market_not_trend_up" 여전히 존재 (regime 필터)

### Task 4.2: Secondary Blocker Distribution 검토

**확인**:
```bash
$snapshot.secondary_blocker_distribution | Format-Table
```

**기대**:
```
band_width_fail: 1-2
band_expansion_fail: 1-2
vwap_distance_fail: 0-1
volume_fail: 0-1
rsi_threshold_fail: 0-1
ema_fail: 0
```

**의미**:
- Setup/trigger를 통과한 이벤트들이 이제 quality 단계에서 필터됨
- 이전처럼 regime에서 모두 탈락하지 않음

---

## ⚠️ 검증 단계 5: 상태 파일 동기화 확인

### Task 5.1: Risk Metrics 불일치 확인

**확인**:
```bash
# state.json
$state = Get-Content c:\cnt\data\state.json | ConvertFrom-Json
"=== state.json ==="
"Daily Loss Count: $($state.risk_metrics.daily_loss_count)"
"Consecutive Losses: $($state.risk_metrics.consecutive_losses)"

# portfolio_state.json
$portfolio = Get-Content c:\cnt\data\portfolio_state.json | ConvertFrom-Json
"=== portfolio_state.json ==="
"Daily Loss Count: $($portfolio.daily_loss_count)"
"Consecutive Losses: $($portfolio.consecutive_losses)"
```

**현재 상태 (아직 미해결)**:
```
state.json: 3 / 3
portfolio_state.json: 0 / 0  ← 불일치
```

**체크**:
- [ ] 두 파일의 손실 카운터가 일치하는가?
- [ ] 아니면 여전히 불일치하는가?

### Task 5.2: Source 필드 확인

```bash
$portfolio.source
```

**기대**:
- `"runtime_state_synced"` 또는 유사한 값 (재동기화 후)
- 현재는 `"rebuild_from_runtime"` (부분 초기화)

---

## 🧾 검증 요약 템플릿

```markdown
## Shadow Evaluator 수정 후 검증 결과

**검증 날짜**: ________
**최종 상태**: [완전 성공 | 부분 성공 | 재실행 필요]

### 코드 수정
- [x] Shadow evaluator 코드 확인
- [x] 테스트 51/51 pass

### Shadow 데이터 갱신
- [ ] Snapshot 최신화됨 (타임스탬프: ________)
- [ ] allowed_signal_count > 0 확인됨 (값: __)
- [ ] trend_not_up blocker 제거 확인됨
- [ ] range_without_upward_bias blocker 제거 확인됨

### 상태 파일 동기화
- [ ] risk_metrics 일치함
- [ ] portfolio_state source 갱신됨

### 다음 액션
- [ ] Shadow 데이터 동기화 완료 → run.ps1 재실행
- [ ] 상태 파일 동기화 진행 (별도 이슈)
- [ ] Breakout_v1 격리 적용 (다음 단계)

### 기타 관찰
_결과 요약_
```

---

## 🎯 의사결정 기준

| 결과 | 해석 | 다음 액션 |
|------|------|---------|
| allowed > 0 AND blocker 분포 변화 | ✅ 수정 성공 | 상태 파일 동기화 진행 |
| allowed = 0 AND blocker 분포 미변 | ❌ 데이터 미갱신 | run.ps1 재실행 |
| allowed = 0 AND blocker 분포 변함 | ⚠️ 설정 재검토 필요 | 50+ events 대기 |
| risk_metrics 불일치 유지 | ⚠️ 별도 이슈 | 포트폴리오 로거 점검 |

---

**검증 완료 후 이 체크리스트를 저장하고 다음 단계 (Breakout_v1 격리)로 진행하세요.**
