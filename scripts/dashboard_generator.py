#!/usr/bin/env python3
"""
CNT Dashboard Generator - Dataview 없이 동작하는 자동 대시보드 생성 시스템
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class DashboardGenerator:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.data_dir = self.repo_root / "data"
        self.docs_dir = self.repo_root / "docs"
        
    def load_strategy_metrics(self) -> Dict[str, Any]:
        """전략 메트릭 로드"""
        metrics_path = self.data_dir / "strategy_metrics.json"
        if not metrics_path.exists():
            return {}
        
        with open(metrics_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_portfolio_state(self) -> Dict[str, Any]:
        """포트폴리오 상태 로드"""
        state_path = self.data_dir / "portfolio_state.json"
        if not state_path.exists():
            return {}
        
        with open(state_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_shadow_snapshot(self) -> Dict[str, Any]:
        """섀도 스냅샷 로드"""
        snapshot_path = self.data_dir / "shadow_breakout_v3_snapshot.json"
        if not snapshot_path.exists():
            return {}
        
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def format_number(self, value: Any, decimals: int = 2) -> str:
        """숫자 포맷팅"""
        try:
            if isinstance(value, (int, float)):
                if abs(value) < 0.001 and value != 0:
                    return f"{value:.{decimals+3}f}"
                return f"{value:.{decimals}f}"
            return str(value)
        except:
            return "N/A"
    
    def format_percentage(self, value: Any, decimals: int = 1) -> str:
        """퍼센트 포맷팅"""
        try:
            if isinstance(value, (int, float)):
                return f"{value * 100:.{decimals}f}%"
            return "N/A"
        except:
            return "N/A"
    
    def generate_strategy_table(self, metrics: Dict[str, Any]) -> str:
        """전략 메트릭 테이블 생성"""
        if not metrics:
            return "| 전략 | 선택 | 종결 | 승률 | 기대값 | PF |\n|---|---|---|---|---|---|\n| 데이터 없음 | - | - | - | - | - |"
        
        table_lines = ["| 전략 | 선택 | 종결 | 승률 | 기대값 | PF |"]
        table_lines.append("|---|---|---|---|---|---|")
        
        for strategy_name, strategy_data in metrics.items():
            win_rate = self.format_percentage(strategy_data.get('win_rate', 0))
            expectancy = self.format_number(strategy_data.get('expectancy', 0), 6)
            profit_factor = self.format_number(strategy_data.get('profit_factor', 0), 3)
            
            table_lines.append(f"| {strategy_name} | "
                             f"{strategy_data.get('signals_selected', 0)} | "
                             f"{strategy_data.get('trades_closed', 0)} | "
                             f"{win_rate} | "
                             f"{expectancy} | "
                             f"{profit_factor} |")
        
        return "\n".join(table_lines)
    
    def generate_portfolio_summary(self, portfolio_state: Dict[str, Any]) -> str:
        """포트폴리오 요약 생성"""
        if not portfolio_state:
            return "포트폴리오 상태 데이터 없음"
        
        lines = [
            f"**총 노출**: {self.format_number(portfolio_state.get('total_exposure', 0))}",
            f"**현금 잔고**: {self.format_number(portfolio_state.get('cash_balance', 0))}",
            f"**일일 손실 횟수**: {portfolio_state.get('daily_loss_count', 0)}",
            f"**연속 손실**: {portfolio_state.get('consecutive_losses', 0)}",
            f"**개방 포지션**: {len(portfolio_state.get('open_positions', []))}",
            f"**마지막 갱신**: {portfolio_state.get('last_update_time', 'N/A')}"
        ]
        
        return "\n".join(lines)
    
    def generate_shadow_analysis(self, shadow_data: Dict[str, Any]) -> str:
        """섀도 분석 생성"""
        if not shadow_data:
            return "섀도 데이터 없음"
        
        total_signals = shadow_data.get('total_signals', 0)
        allowed_signals = shadow_data.get('allowed_signals', 0)
        allowed_ratio = (allowed_signals / total_signals * 100) if total_signals > 0 else 0
        
        lines = [
            f"**총 신호**: {total_signals}",
            f"**허용 신호**: {allowed_signals}",
            f"**허용률**: {self.format_percentage(allowed_ratio/100, 2)}",
            f"**관찰 시작**: {shadow_data.get('observation_start', 'N/A')}",
            f"**마지막 갱신**: {shadow_data.get('last_updated', 'N/A')}"
        ]
        
        # 첫 번째 차단기 분석
        blocker_dist = shadow_data.get('first_blocker_distribution', {})
        if blocker_dist:
            lines.append("\n**첫 번째 차단기 분포**:")
            for blocker, count in blocker_dist.items():
                ratio = (count / total_signals * 100) if total_signals > 0 else 0
                lines.append(f"- {blocker}: {count} ({self.format_percentage(ratio/100, 1)})")
        
        return "\n".join(lines)
    
    def generate_dashboard(self) -> str:
        """전체 대시보드 생성"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 데이터 로드
        strategy_metrics = self.load_strategy_metrics()
        portfolio_state = self.load_portfolio_state()
        shadow_data = self.load_shadow_snapshot()
        
        dashboard_content = f"""---
tags:
  - cnt
  - dashboard
  - auto-generated
generated_at: {current_time}
---

# CNT Auto-Generated Dashboard

*생성 시각: {current_time}*

---

## 📊 전략 성과

{self.generate_strategy_table(strategy_metrics)}

---

## 💼 포트폴리오 상태

{self.generate_portfolio_summary(portfolio_state)}

---

## 🔍 Breakout V3 섀도 분석

{self.generate_shadow_analysis(shadow_data)}

---

## 📈 주요 지표

### 현재 LIVE READY 상태
- **상태**: {'✅ LIVE_READY' if portfolio_state else '❌ DATA_REQUIRED'}
- **마지막 확인**: {current_time}

### 전략별 현황
{self._generate_strategy_status(strategy_metrics)}

---

## 🔄 데이터 소스

- `data/strategy_metrics.json`
- `data/portfolio_state.json`  
- `data/shadow_breakout_v3_snapshot.json`

*이 대시보드는 Python 스크립트로 자동 생성되었습니다. Dataview 플러그인이 필요 없습니다.*
"""
        
        return dashboard_content
    
    def _generate_strategy_status(self, metrics: Dict[str, Any]) -> str:
        """전략 상태 요약 생성"""
        if not metrics:
            return "- 전략 데이터 없음"
        
        lines = []
        for strategy_name, strategy_data in metrics.items():
            trades_closed = strategy_data.get('trades_closed', 0)
            win_rate = strategy_data.get('win_rate', 0)
            
            status = "🟢" if trades_closed >= 10 and win_rate > 0.5 else "🟡" if trades_closed >= 5 else "🔴"
            
            lines.append(f"- {status} **{strategy_name}**: {trades_closed}건 종료, 승률 {self.format_percentage(win_rate)}")
        
        return "\n".join(lines)
    
    def update_dashboard(self) -> str:
        """대시보드 업데이트"""
        dashboard_content = self.generate_dashboard()
        dashboard_path = self.docs_dir / "CNT AUTO DASHBOARD.md"
        
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_content)
        
        return str(dashboard_path)

def main():
    """메인 실행 함수"""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generator = DashboardGenerator(repo_root)
    
    print("CNT Dashboard Generator")
    print("=" * 50)
    
    try:
        dashboard_path = generator.update_dashboard()
        print(f"✓ Dashboard updated: {dashboard_path}")
    except Exception as e:
        print(f"✗ Failed to update dashboard: {e}")

if __name__ == "__main__":
    main()
