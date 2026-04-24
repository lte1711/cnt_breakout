#!/usr/bin/env python3
"""
CNT Real-time Monitor - 런타임 데이터 변경 시 자동으로 문서/대시보드 갱신
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Set
import threading

from template_generator import TemplateGenerator
from dashboard_generator import DashboardGenerator

class FileWatcher:
    """파일 변경 감시자"""
    
    def __init__(self, watch_paths: list):
        self.watch_paths = [Path(p) for p in watch_paths]
        self.last_modified = {}
        self.update_timestamps()
    
    def update_timestamps(self):
        """타임스탬프 업데이트"""
        for path in self.watch_paths:
            if path.exists():
                self.last_modified[str(path)] = path.stat().st_mtime
    
    def has_changes(self) -> Set[str]:
        """변경된 파일 목록 반환"""
        changed_files = set()
        
        for path in self.watch_paths:
            if path.exists():
                current_mtime = path.stat().st_mtime
                last_mtime = self.last_modified.get(str(path), 0)
                
                if current_mtime > last_mtime:
                    changed_files.add(str(path))
                    self.last_modified[str(path)] = current_mtime
        
        return changed_files

class RealtimeMonitor:
    """실시간 모니터링 시스템"""
    
    def __init__(self, repo_root: str, check_interval: int = 30):
        self.repo_root = Path(repo_root)
        self.check_interval = check_interval
        self.data_dir = self.repo_root / "data"
        self.logs_dir = self.repo_root / "logs"
        
        # 컴포넌트 초기화
        self.template_generator = TemplateGenerator(repo_root)
        self.dashboard_generator = DashboardGenerator(repo_root)
        
        # 감시 파일 목록
        self.watch_files = [
            self.data_dir / "strategy_metrics.json",
            self.data_dir / "portfolio_state.json",
            self.data_dir / "shadow_breakout_v3_snapshot.json",
            self.data_dir / "shadow_breakout_v3.jsonl",
            self.logs_dir / "runtime.log",
            self.logs_dir / "signal.log"
        ]
        
        self.file_watcher = FileWatcher(self.watch_files)
        
        # 상태 추적
        self.last_trade_count = 0
        self.last_signal_count = 0
        self.last_allowed_signal_count = 0
        
    def load_strategy_metrics(self) -> Dict[str, Any]:
        """전략 메트릭 로드"""
        metrics_path = self.data_dir / "strategy_metrics.json"
        if not metrics_path.exists():
            return {}
        
        with open(metrics_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_shadow_data(self) -> Dict[str, Any]:
        """섀도 데이터 로드"""
        snapshot_path = self.data_dir / "shadow_breakout_v3_snapshot.json"
        if not snapshot_path.exists():
            return {}
        
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def count_total_trades(self, metrics: Dict[str, Any]) -> int:
        """총 거래 횟수 계산"""
        total = 0
        for strategy_data in metrics.values():
            total += strategy_data.get('trades_closed', 0)
        return total
    
    def check_trigger_conditions(self) -> Dict[str, bool]:
        """트리거 조건 확인"""
        metrics = self.load_strategy_metrics()
        shadow_data = self.load_shadow_data()
        
        current_trades = self.count_total_trades(metrics)
        current_signals = shadow_data.get('total_signals', 0)
        current_allowed = shadow_data.get('allowed_signals', 0)
        
        triggers = {
            'new_trade_closed': current_trades > self.last_trade_count,
            'new_signals_generated': current_signals > self.last_signal_count,
            'new_allowed_signals': current_allowed > self.last_allowed_signal_count,
            'signals_reached_threshold': current_signals >= self.last_signal_count + 20,
            'allowed_signal_detected': current_allowed > self.last_allowed_signal_count and self.last_allowed_signal_count == 0
        }
        
        # 상태 업데이트
        self.last_trade_count = current_trades
        self.last_signal_count = current_signals
        self.last_allowed_signal_count = current_allowed
        
        return triggers
    
    def handle_file_changes(self, changed_files: Set[str]):
        """파일 변경 처리"""
        actions = []
        
        for file_path in changed_files:
            file_name = Path(file_path).name
            
            if file_name == "strategy_metrics.json":
                actions.append("update_dashboard")
            elif file_name == "portfolio_state.json":
                actions.append("update_dashboard")
            elif file_name == "shadow_breakout_v3_snapshot.json":
                actions.append("update_dashboard")
            elif file_name == "shadow_breakout_v3.jsonl":
                actions.append("check_shadow_triggers")
            elif file_name == "runtime.log":
                actions.append("check_runtime_events")
            elif file_name == "signal.log":
                actions.append("check_signal_events")
        
        return actions
    
    def execute_actions(self, actions: list):
        """액션 실행"""
        triggers = self.check_trigger_conditions()
        
        for action in actions:
            try:
                if action == "update_dashboard":
                    dashboard_path = self.dashboard_generator.update_dashboard()
                    print(f"[{datetime.now()}] ✅ Dashboard updated: {dashboard_path}")
                
                elif action == "check_shadow_triggers":
                    if triggers['signals_reached_threshold']:
                        self.create_observation_review()
                    
                    if triggers['allowed_signal_detected']:
                        self.create_allowed_signal_log()
                
                elif action == "check_runtime_events":
                    if triggers['new_trade_closed']:
                        self.dashboard_generator.update_dashboard()
                        print(f"[{datetime.now()}] 🔄 New trade detected, dashboard updated")
                
                elif action == "check_signal_events":
                    if triggers['new_allowed_signals']:
                        self.create_allowed_signal_log()
                        print(f"[{datetime.now()}] 🎯 New allowed signal detected")
            
            except Exception as e:
                print(f"[{datetime.now()}] ❌ Action '{action}' failed: {e}")
    
    def create_observation_review(self):
        """관찰 리뷰 자동 생성"""
        try:
            review_path = self.template_generator.create_observation_review_document()
            print(f"[{datetime.now()}] 📝 Observation review auto-created: {review_path}")
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Failed to create observation review: {e}")
    
    def create_allowed_signal_log(self):
        """허용 신호 로그 자동 생성"""
        shadow_data = self.load_shadow_data()
        
        if shadow_data:
            signal_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "soft_pass_count": "N/A",
                "key_conditions": "Auto-detected",
                "notes": f"Allowed signal #{shadow_data.get('allowed_signals', 0)} detected"
            }
            
            try:
                log_path = self.template_generator.create_allowed_signal_log(signal_data)
                print(f"[{datetime.now()}] 🎯 Allowed signal log updated: {log_path}")
            except Exception as e:
                print(f"[{datetime.now()}] ❌ Failed to create allowed signal log: {e}")
    
    def start_monitoring(self):
        """모니터링 시작"""
        print(f"[{datetime.now()}] 🚀 CNT Real-time Monitor started")
        print(f"[{datetime.now()}] 📁 Watching: {[str(p) for p in self.watch_files]}")
        print(f"[{datetime.now()}] ⏱️  Check interval: {self.check_interval} seconds")
        
        try:
            while True:
                # 파일 변경 감지
                changed_files = self.file_watcher.has_changes()
                
                if changed_files:
                    print(f"[{datetime.now()}] 🔄 Files changed: {changed_files}")
                    
                    # 액션 결정 및 실행
                    actions = self.handle_file_changes(changed_files)
                    if actions:
                        self.execute_actions(actions)
                
                # 대기
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            print(f"[{datetime.now()}] 🛑 Monitor stopped by user")
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Monitor error: {e}")

def main():
    """메인 실행 함수"""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 모니터 설정
    monitor = RealtimeMonitor(repo_root, check_interval=30)
    
    # 초기 대시보드 생성
    try:
        dashboard_path = monitor.dashboard_generator.update_dashboard()
        print(f"✅ Initial dashboard created: {dashboard_path}")
    except Exception as e:
        print(f"❌ Failed to create initial dashboard: {e}")
    
    # 모니터링 시작
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
