---
tags:
  - cnt
  - type/documentation
  - status/active
  - type/operation
  - strategy/breakout_v3
  - obsidian
  - cnt-automation-tools-usage-guide
---

# CNT 자동화 도구 사용 가이드

## 개요

CNT 프로젝트의 Obsidian 관리 보완을 위해 개발된 자동화 도구 모음입니다. 이 도구들은 Dataview나 Templater 플러그인 의존성 없이 독립적으로 동작합니다.

---

##  도구 목록

### 1. Template Generator (`template_generator.py`)
템플릿 자동 생성 시스템

**기능:**
- Templater 변수를 실제 값으로 자동 대체
- 섀도 데이터에서 통계 자동 추출
- 관찰 리뷰 및 허용 신호 로그 자동 생성

**사용법:**
```bash
# 기본 실행
python scripts/template_generator.py

# Python 코드에서 직접 사용
from scripts.template_generator import TemplateGenerator
generator = TemplateGenerator("c:/cnt")
generator.create_observation_review_document()
```

**출력 파일:**
- `docs/CNT v2 BREAKOUT V3 OBSERVATION REVIEW [타임스탬프].md`
- `docs/breakout_v3 allowed signal log.md`

---

### 2. Dashboard Generator (`dashboard_generator.py`)
Dataview 없이 동작하는 자동 대시보드 생성

**기능:**
- 전략 메트릭 테이블 자동 생성
- 포트폴리오 상태 요약
- 섀도 분석 자동 업데이트
- LIVE READY 상태 판단

**사용법:**
```bash
# 대시보드 업데이트
python scripts/dashboard_generator.py

# Python 코드에서 직접 사용
from scripts.dashboard_generator import DashboardGenerator
generator = DashboardGenerator("c:/cnt")
dashboard_path = generator.update_dashboard()
```

**출력 파일:**
- `docs/CNT AUTO DASHBOARD.md`

---

### 3. Real-time Monitor (`realtime_monitor.py`)
런타임 데이터 변경 시 자동 문서/대시보드 갱신

**기능:**
- 파일 변경 감지 (30초 간격)
- 트리거 조건 자동 확인
- 관찰 리뷰 자동 생성 (20-30 신호마다)
- 허용 신호 로그 자동 업데이트

**사용법:**
```bash
# 실시간 모니터링 시작
python scripts/realtime_monitor.py

# Python 코드에서 직접 사용
from scripts.realtime_monitor import RealtimeMonitor
monitor = RealtimeMonitor("c:/cnt", check_interval=30)
monitor.start_monitoring()
```

**감시 파일:**
- `data/strategy_metrics.json`
- `data/portfolio_state.json`
- `data/shadow_breakout_v3_snapshot.json`
- `data/shadow_breakout_v3.jsonl`
- `logs/runtime.log`
- `logs/signal.log`

**트리거 조건:**
- 새 거래 종료 시 대시보드 자동 갱신
- 20-30개 섀도 신호 축적 시 관찰 리뷰 자동 생성
- 첫 허용 신호 감지 시 로그 자동 업데이트

---

### 4. Standalone Dashboard (`standalone_dashboard.py`)
Obsidian 플러그인 의존성 없는 독립형 대시보드

**기능:**
- 터미널에서 직접 대시보드 표시
- 자동 갱신 모드 지원
- 라이브 상태 실시간 모니터링

**사용법:**
```bash
# 단일 표시
python scripts/standalone_dashboard.py

# 자동 갱신 모드
python scripts/standalone_dashboard.py --watch

# 60초 간격 자동 갱신
python scripts/standalone_dashboard.py --watch --interval 60

# 최근 로그 포함
python scripts/standalone_dashboard.py --with-logs
```

**출력 형식:**
-  전략 성과 테이블
-  포트폴리오 상태
-  섀도 분석
-  라이브 상태 요약

---

##  빠른 시작

### 1. 기본 설정
```bash
# CNT 루트 디렉토리에서 실행
cd c:/cnt

# 스크립트 실행 권한 확인 (Linux/Mac)
chmod +x scripts/*.py
```

### 2. 대시보드 생성
```bash
# 자동 대시보드 생성
python scripts/dashboard_generator.py

# 결과 확인
cat docs/CNT\ AUTO\ DASHBOARD.md
```

### 3. 템플릿 생성
```bash
# 관찰 리뷰 자동 생성
python scripts/template_generator.py

# 결과 확인
ls docs/CNT*v3*OBSERVATION*REVIEW*.md
```

### 4. 실시간 모니터링
```bash
# 별도 터미널에서 실시간 모니터링 시작
python scripts/realtime_monitor.py

# 다른 터미널에서 독립형 대시보드 실행
python scripts/standalone_dashboard.py --watch
```

---

##  운영 시나리오

### 시나리오 1: 일일 운영 보고
```bash
# 1. 대시보드 업데이트
python scripts/dashboard_generator.py

# 2. 관찰 리뷰 생성 (필요시)
python scripts/template_generator.py

# 3. 결과 확인
python scripts/standalone_dashboard.py --with-logs
```

### 시나리오 2: 실시간 모니터링
```bash
# 터미널 1: 실시간 모니터링
python scripts/realtime_monitor.py

# 터미널 2: 대시보드 자동 갱신
python scripts/standalone_dashboard.py --watch --interval 60
```

### 시나리오 3: 수동 분석
```bash
# 1. 최신 상태 확인
python scripts/standalone_dashboard.py

# 2. 필요한 문서 생성
python scripts/template_generator.py

# 3. 상세 분석
cat docs/CNT\ AUTO\ DASHBOARD.md
```

---

##  고급 설정

### 모니터링 간격 조정
```python
# realtime_monitor.py에서 간격 조정
monitor = RealtimeMonitor("c:/cnt", check_interval=60)  # 60초로 변경
```

### 템플릿 사용자 정의
```python
# template_generator.py에서 데이터 소스 추가
def load_custom_data(self):
    # 사용자 정의 데이터 로드 로직
    pass
```

### 대시보드 형식 수정
```python
# dashboard_generator.py에서 표시 형식 변경
def format_number(self, value, decimals=2):
    # 사용자 정의 포맷팅 로직
    pass
```

---

##  파일 구조

```
c:/cnt/
├── scripts/
│   ├── template_generator.py      # 템플릿 자동 생성
│   ├── dashboard_generator.py     # 대시보드 자동 생성
│   ├── realtime_monitor.py        # 실시간 모니터링
│   └── standalone_dashboard.py    # 독립형 대시보드
├── data/
│   ├── strategy_metrics.json      # 전략 메트릭
│   ├── portfolio_state.json       # 포트폴리오 상태
│   └── shadow_breakout_v3_snapshot.json  # 섀도 스냅샷
├── docs/
│   ├── CNT AUTO DASHBOARD.md      # 자동 생성 대시보드
│   └── [자동 생성된 리뷰 문서들]
└── logs/
    ├── runtime.log                # 런타임 로그
    └── signal.log                 # 신호 로그
```

---

##  문제 해결

### 일반적인 문제

**1. 파일을 찾을 수 없음**
```bash
# 경로 확인
python -c "import os; print('Current dir:', os.getcwd())"
```

**2. JSON 파싱 오류**
```bash
# 데이터 파일 유효성 확인
python -c "import json; print(json.load(open('data/strategy_metrics.json')))"
```

**3. 인코딩 오류**
```bash
# UTF-8 인코딩으로 파일 확인
file -bi data/strategy_metrics.json
```

### 모니터링 문제

**1. 파일 변경 감지 안됨**
- 파일 권한 확인
- 디스크 공간 확인
- 파일 시스템 타입 확인

**2. 메모리 사용량 증가**
- 모니터링 간격 늘리기
- 로그 파일 정기적으로 정리

---

##  자동화 팁

### 1. 스케줄러 등록 (Windows)
```batch
# 매 시간 대시보드 업데이트
schtasks /create /tn "CNT Dashboard" /tr "python c:/cnt/scripts/dashboard_generator.py" /sc hourly
```

### 2. 스케줄러 등록 (Linux/Mac)
```bash
# crontab에 추가
0 * * * * cd /path/to/cnt && python scripts/dashboard_generator.py
```

### 3. 스타트업 스크립트
```bash
#!/bin/bash
# startup.sh
cd /path/to/cnt
python scripts/realtime_monitor.py &
python scripts/standalone_dashboard.py --watch &
```

---

##  성능 최적화

### 1. 메모리 사용량 감소
- 불필요한 데이터 로드 제거
- 캐시 메커니즘 구현

### 2. 디스크 I/O 최적화
- 배치 처리로 파일 접근 감소
- 압축 저장 고려

### 3. 네트워크 트래픽 감소
- 로컬 캐시 활용
- 증분 업데이트 구현

---

##  향후 개선 계획

1. **웹 인터페이스**: 브라우저 기반 대시보드
2. **알림 시스템**: 중요 이벤트 푸시 알림
3. **데이터 시각화**: 그래프 및 차트 추가
4. **API 통합**: 외부 데이터 소스 연동
5. **머신러닝**: 예측 분석 기능

---

##  지원

문제 발생 시:
1. 이 가이드의 문제 해결 섹션 확인
2. 로그 파일 검토 (`logs/`)
3. GitHub Issues 생성 (프로젝트 저장소)

---

##  변경 로그

- **v1.0**: 초기 자동화 도구 모음
- **v1.1**: 실시간 모니터링 추가
- **v1.2**: 독립형 대시보드 추가
- **v1.3**: 사용법 문서화 완료

---

*이 가이드는 CNT 프로젝트의 Obsidian 관리 자동화를 돕기 위해 작성되었습니다.*

## Obsidian Links

- [[CNT TOOLCHAIN INTEGRATION REPORT]]

