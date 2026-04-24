#!/usr/bin/env python3
"""
CNT Template Generator - Obsidian 템플릿 자동 생성 시스템
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class TemplateGenerator:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.templates_dir = self.repo_root / "templates"
        self.docs_dir = self.repo_root / "docs"
        self.data_dir = self.repo_root / "data"
        
    def load_template(self, template_name: str) -> str:
        """템플릿 파일 로드"""
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def replace_templater_variables(self, content: str) -> str:
        """Templater 변수를 실제 값으로 대체"""
        now = datetime.now()
        replacements = {
            '<% tp.date.now("YYYY-MM-DD") %>': now.strftime("%Y-%m-%d"),
            '<% tp.date.now("YYYY-MM-DD HH:mm") %>': now.strftime("%Y-%m-%d %H:%M"),
        }
        
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        
        return content
    
    def load_shadow_data(self) -> Dict[str, Any]:
        """섀도 데이터 로드"""
        snapshot_path = self.data_dir / "shadow_breakout_v3_snapshot.json"
        if not snapshot_path.exists():
            return {}
        
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_observation_review(self, review_data: Optional[Dict[str, Any]] = None) -> str:
        """관찰 리뷰 생성"""
        template = self.load_template("observation_review.md")
        content = self.replace_templater_variables(template)
        
        # 기본 데이터 설정
        shadow_data = self.load_shadow_data()
        current_time = datetime.now()
        
        # 기본 메타데이터
        metadata = {
            "window_start": review_data.get("window_start", "") if review_data else "",
            "baseline_commit": review_data.get("baseline_commit", "") if review_data else "",
            "status": "completed",
            "final_judgement": ""
        }
        
        # 섀도 데이터에서 통계 추출
        if shadow_data:
            signal_count = shadow_data.get("total_signals", 0)
            allowed_count = shadow_data.get("allowed_signals", 0)
            allowed_ratio = (allowed_count / signal_count * 100) if signal_count > 0 else 0
            
            # 기본 통계 채우기
            content = content.replace("| signal_count | |", f"| signal_count | {signal_count} |")
            content = content.replace("| allowed_signal_count | |", f"| allowed_signal_count | {allowed_count} |")
            content = content.replace("| allowed_signal_ratio | |", f"| allowed_signal_ratio | {allowed_ratio:.2f}% |")
            
            # 첫 번째 차단기 분석 (데이터가 있다면)
            blocker_stats = shadow_data.get("first_blocker_distribution", {})
            if blocker_stats:
                for blocker, count in blocker_stats.items():
                    ratio = (count / signal_count * 100) if signal_count > 0 else 0
                    content = content.replace(f"| {blocker} | | | |", f"| {blocker} | {count} | {ratio:.1f}% | |")
        
        # 메타데이터 업데이트
        for key, value in metadata.items():
            content = content.replace(f"| {key} | |", f"| {key} | {value} |")
        
        return content
    
    def generate_allowed_signal_log(self, signal_data: Dict[str, Any]) -> str:
        """허용 신호 로그 생성"""
        template = self.load_template("allowed_signal_log.md")
        content = self.replace_templater_variables(template)
        
        # 신호 데이터 채우기
        for key, value in signal_data.items():
            content = content.replace(f"| {key} | |", f"| {key} | {value} |")
        
        return content
    
    def create_observation_review_document(self, output_name: Optional[str] = None) -> str:
        """관찰 리뷰 문서 생성"""
        if output_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            output_name = f"CNT v2 BREAKOUT V3 OBSERVATION REVIEW {timestamp}.md"
        
        content = self.generate_observation_review()
        output_path = self.docs_dir / output_name
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_path)
    
    def create_allowed_signal_log(self, signal_data: Dict[str, Any]) -> str:
        """허용 신호 로그 문서 생성"""
        content = self.generate_allowed_signal_log(signal_data)
        output_path = self.docs_dir / "breakout_v3 allowed signal log.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_path)

def main():
    """메인 실행 함수"""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generator = TemplateGenerator(repo_root)
    
    print("CNT Template Generator")
    print("=" * 50)
    
    # 관찰 리뷰 생성
    try:
        review_path = generator.create_observation_review_document()
        print(f"✓ Observation review created: {review_path}")
    except Exception as e:
        print(f"✗ Failed to create observation review: {e}")
    
    # 예시 허용 신호 로그 생성
    example_signal_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soft_pass_count": 3,
        "key_conditions": "regime_pass, trigger_pass, setup_soft_pass",
        "notes": "First allowed signal detected in observation window"
    }
    
    try:
        signal_log_path = generator.create_allowed_signal_log(example_signal_data)
        print(f"✓ Allowed signal log created: {signal_log_path}")
    except Exception as e:
        print(f"✗ Failed to create allowed signal log: {e}")

if __name__ == "__main__":
    main()
