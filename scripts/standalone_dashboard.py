#!/usr/bin/env python3
"""
CNT Standalone Dashboard - Obsidian 플러그인 의존성 없는 독립형 대시보드
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import argparse

class StandaloneDashboard:
    """플러그인 독립형 대시보드"""
    
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.data_dir = self.repo_root / "data"
        self.logs_dir = self.repo_root / "logs"
        
    def load_json_file(self, file_path: Path) -> Dict[str, Any]:
        """JSON 파일 로드"""
        if not file_path.exists():
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load {file_path}: {e}")
            return {}
    
    def load_log_file(self, file_path: Path, lines: int = 50) -> List[str]:
        """로그 파일 최신 라인 로드"""
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return [line.strip() for line in all_lines[-lines:]]
        except Exception as e:
            print(f"❌ Failed to load {file_path}: {e}")
            return []
    
    def format_table_row(self, columns: List[str], widths: List[int]) -> str:
        """테이블 행 포맷팅"""
        formatted_columns = []
        for col, width in zip(columns, widths):
            formatted_columns.append(col.ljust(width))
        return " | ".join(formatted_columns)
    
    def format_table_separator(self, widths: List[int]) -> str:
        """테이블 구분자 포맷팅"""
        separators = []
        for width in widths:
            separators.append("-" * width)
        return "-+-".join(separators)
    
    def display_strategy_metrics(self, metrics: Dict[str, Any]):
        """전략 메트릭 표시"""
        if not metrics:
            print("📊 전략 메트릭: 데이터 없음")
            return
        
        print("\n📊 전략 성과")
        print("=" * 80)
        
        # 테이블 헤더
        headers = ["전략", "선택", "종결", "승률", "기대값", "PF"]
        widths = [15, 8, 8, 8, 10, 8]
        
        print(self.format_table_row(headers, widths))
        print(self.format_table_separator(widths))
        
        # 데이터 행
        for strategy_name, strategy_data in metrics.items():
            win_rate = strategy_data.get('win_rate', 0) * 100
            expectancy = strategy_data.get('expectancy', 0)
            profit_factor = strategy_data.get('profit_factor', 0)
            
            row = [
                strategy_name[:15],
                str(strategy_data.get('signals_selected', 0)),
                str(strategy_data.get('trades_closed', 0)),
                f"{win_rate:.1f}%",
                f"{expectancy:.6f}",
                f"{profit_factor:.3f}"
            ]
            
            print(self.format_table_row(row, widths))
    
    def display_portfolio_state(self, portfolio_state: Dict[str, Any]):
        """포트폴리오 상태 표시"""
        if not portfolio_state:
            print("\n💼 포트폴리오 상태: 데이터 없음")
            return
        
        print("\n💼 포트폴리오 상태")
        print("=" * 50)
        
        total_exposure = portfolio_state.get('total_exposure', 0)
        cash_balance = portfolio_state.get('cash_balance', 0)
        daily_loss_count = portfolio_state.get('daily_loss_count', 0)
        consecutive_losses = portfolio_state.get('consecutive_losses', 0)
        open_positions = portfolio_state.get('open_positions', [])
        last_update = portfolio_state.get('last_update_time', 'N/A')
        
        print(f"총 노출: {total_exposure:.6f}")
        print(f"현금 잔고: {cash_balance:.6f}")
        print(f"일일 손실 횟수: {daily_loss_count}")
        print(f"연속 손실: {consecutive_losses}")
        print(f"개방 포지션: {len(open_positions)}")
        print(f"마지막 갱신: {last_update}")
        
        # LIVE READY 상태 판단
        total_trades = sum(s.get('trades_closed', 0) for s in self.load_json_file(self.data_dir / "strategy_metrics.json").values())
        is_live_ready = total_trades >= 50 and consecutive_losses <= 2
        
        status = "✅ LIVE_READY" if is_live_ready else "❌ NOT_READY"
        print(f"라이브 준비 상태: {status}")
    
    def display_shadow_analysis(self, shadow_data: Dict[str, Any]):
        """섀도 분석 표시"""
        if not shadow_data:
            print("\n🔍 섀도 분석: 데이터 없음")
            return
        
        print("\n🔍 Breakout V3 섀도 분석")
        print("=" * 50)
        
        total_signals = shadow_data.get('total_signals', 0)
        allowed_signals = shadow_data.get('allowed_signals', 0)
        allowed_ratio = (allowed_signals / total_signals * 100) if total_signals > 0 else 0
        
        print(f"총 신호: {total_signals}")
        print(f"허용 신호: {allowed_signals}")
        print(f"허용률: {allowed_ratio:.2f}%")
        
        # 첫 번째 차단기 분석
        blocker_dist = shadow_data.get('first_blocker_distribution', {})
        if blocker_dist:
            print("\n첫 번째 차단기 분포:")
            for blocker, count in blocker_dist.items():
                ratio = (count / total_signals * 100) if total_signals > 0 else 0
                print(f"  {blocker}: {count} ({ratio:.1f}%)")
    
    def display_recent_logs(self, log_type: str = "runtime"):
        """최근 로그 표시"""
        log_file = self.logs_dir / f"{log_type}.log"
        recent_logs = self.load_log_file(log_file, 20)
        
        if not recent_logs:
            print(f"\n📋 최근 {log_type} 로그: 데이터 없음")
            return
        
        print(f"\n📋 최근 {log_type} 로그 (마지막 20줄)")
        print("=" * 80)
        
        for i, log_line in enumerate(recent_logs[-10:], 1):  # 마지막 10줄만 표시
            print(f"{i:2d}: {log_line}")
    
    def display_live_status(self):
        """라이브 상태 요약"""
        metrics = self.load_json_file(self.data_dir / "strategy_metrics.json")
        portfolio_state = self.load_json_file(self.data_dir / "portfolio_state.json")
        shadow_data = self.load_json_file(self.data_dir / "shadow_breakout_v3_snapshot.json")
        
        total_trades = sum(s.get('trades_closed', 0) for s in metrics.values())
        
        print("\n🎯 CNT 시스템 상태 요약")
        print("=" * 50)
        print(f"시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"총 거래: {total_trades}")
        print(f"섀도 신호: {shadow_data.get('total_signals', 0)}")
        print(f"허용 신호: {shadow_data.get('allowed_signals', 0)}")
        
        # 상태 아이콘
        if total_trades >= 50:
            trade_status = "✅"
        elif total_trades >= 10:
            trade_status = "🟡"
        else:
            trade_status = "❌"
        
        if shadow_data.get('allowed_signals', 0) > 0:
            shadow_status = "✅"
        else:
            shadow_status = "🟡"
        
        print(f"거래 상태: {trade_status} ({total_trades}/50)")
        print(f"섀도 상태: {shadow_status} (허용 신호: {shadow_data.get('allowed_signals', 0)})")
    
    def run_dashboard(self, watch_mode: bool = False, interval: int = 30):
        """대시보드 실행"""
        if watch_mode:
            print(f"🚀 CNT Standalone Dashboard (자동 갱신 모드)")
            print(f"⏱️ 갱신 간격: {interval}초")
            print("Ctrl+C로 종료")
            print("=" * 80)
            
            try:
                while True:
                    # 화면 클리어
                    os.system('cls' if os.name == 'nt' else 'clear')
                    
                    # 전체 표시
                    self.display_live_status()
                    self.display_strategy_metrics(self.load_json_file(self.data_dir / "strategy_metrics.json"))
                    self.display_portfolio_state(self.load_json_file(self.data_dir / "portfolio_state.json"))
                    self.display_shadow_analysis(self.load_json_file(self.data_dir / "shadow_breakout_v3_snapshot.json"))
                    
                    print(f"\n⏰ 다음 갱신: {interval}초 후...")
                    import time
                    time.sleep(interval)
            
            except KeyboardInterrupt:
                print("\n🛑 대시보드 종료")
        else:
            # 단일 표시 모드
            print("🚀 CNT Standalone Dashboard")
            print("=" * 80)
            
            self.display_live_status()
            self.display_strategy_metrics(self.load_json_file(self.data_dir / "strategy_metrics.json"))
            self.display_portfolio_state(self.load_json_file(self.data_dir / "portfolio_state.json"))
            self.display_shadow_analysis(self.load_json_file(self.data_dir / "shadow_breakout_v3_snapshot.json"))
            
            # 옵션: 최근 로그 표시
            if len(sys.argv) > 1 and sys.argv[1] == "--with-logs":
                self.display_recent_logs("runtime")
                self.display_recent_logs("signal")

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="CNT Standalone Dashboard")
    parser.add_argument("--watch", action="store_true", help="자동 갱신 모드")
    parser.add_argument("--interval", type=int, default=30, help="갱신 간격 (초)")
    parser.add_argument("--with-logs", action="store_true", help="최근 로그 포함")
    
    args = parser.parse_args()
    
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dashboard = StandaloneDashboard(repo_root)
    
    # 단일 표시 모드에서 로그 옵션 처리
    if not args.watch and args.with_logs:
        sys.argv.append("--with-logs")
    
    dashboard.run_dashboard(watch_mode=args.watch, interval=args.interval)

if __name__ == "__main__":
    main()
