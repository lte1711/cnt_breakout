#!/usr/bin/env python3
"""
CNT Version Classifier - 문서 버전별 분류 및 색상 코딩 자동화
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re

class VersionClassifier:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.docs_dir = self.repo_root / "docs"
        self.ko_docs_dir = self.repo_root / "docs" / "ko"
        
        # 버전 색상 매핑
        self.color_mapping = {
            "v1.0": {"emoji": "🟡", "color": "yellow", "status": "concept"},
            "v1.1": {"emoji": "🟢", "color": "green", "status": "completed"},
            "v2.0": {"emoji": "🔵", "color": "blue", "status": "designed"},
            "v2.1": {"emoji": "🟠", "color": "orange", "status": "implementation"},
            "v2.2": {"emoji": "🟣", "color": "purple", "status": "automation"},
            "v3.0": {"emoji": "🔴", "color": "red", "status": "planned"}
        }
        
        # 문서 유형 분류
        self.document_types = {
            "ARCHITECTURE DESIGN DOCUMENT": "architecture",
            "IMPLEMENTATION VALIDATION REPORT": "validation",
            "IMPLEMENTATION WORK INSTRUCTION": "implementation",
            "OPERATION DISCIPLINE": "operation",
            "AUTOMATION TOOLS USAGE GUIDE": "automation",
            "PERFORMANCE VALIDATION REPORT": "performance",
            "OBSIDIAN PLUGIN POLICY": "obsidian",
            "INTEGRATED OPERATING PROTOCOL": "protocol",
            "CURRENT STATUS ASSESSMENT": "status",
            "METRICS AND STRATEGY ATTRIBUTION FIX REPORT": "fix"
        }
    
    def extract_version_from_filename(self, filename: str) -> Optional[str]:
        """파일명에서 버전 추출"""
        # v1.1, v2.0, v3.0 등의 패턴
        version_patterns = [
            r'(CNT v\d+\.\d+)',
            r'(CNT V\d+\.\d+)',
            r'(v\d+\.\d+)',
            r'(V\d+\.\d+)'
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                version = match.group(1).lower()
                # 정규화
                version = version.replace('cnt ', '').replace('cnt', '')
                return version
        
        return None
    
    def extract_document_type(self, filename: str) -> Optional[str]:
        """파일명에서 문서 유형 추출"""
        for doc_type, category in self.document_types.items():
            if doc_type in filename:
                return category
        return "general"
    
    def classify_documents(self, directory: Path) -> List[Dict]:
        """디렉토리 내 문서 분류"""
        classified_docs = []
        
        if not directory.exists():
            return classified_docs
        
        for file_path in directory.rglob("*.md"):
            if file_path.is_file():
                filename = file_path.name
                relative_path = file_path.relative_to(self.repo_root)
                
                # 버전 추출
                version = self.extract_version_from_filename(filename)
                
                # 문서 유형 추출
                doc_type = self.extract_document_type(filename)
                
                # 파일 정보
                stat = file_path.stat()
                
                classified_docs.append({
                    "filename": filename,
                    "path": str(relative_path),
                    "version": version,
                    "type": doc_type,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                    "color_info": self.color_mapping.get(version, {"emoji": "⚪", "color": "white", "status": "unknown"})
                })
        
        return classified_docs
    
    def generate_version_matrix(self, classified_docs: List[Dict]) -> Dict:
        """버전별 문서 매트릭스 생성"""
        matrix = {}
        
        for doc in classified_docs:
            version = doc["version"] or "general"
            if version not in matrix:
                matrix[version] = {
                    "count": 0,
                    "documents": [],
                    "types": {},
                    "color_info": doc["color_info"]
                }
            
            matrix[version]["count"] += 1
            matrix[version]["documents"].append(doc)
            
            # 문서 유형 집계
            doc_type = doc["type"]
            if doc_type not in matrix[version]["types"]:
                matrix[version]["types"][doc_type] = 0
            matrix[version]["types"][doc_type] += 1
        
        return matrix
    
    def generate_classification_report(self, language: str = "en") -> str:
        """분류 보고서 생성"""
        # 영어 문서 분류
        en_docs = self.classify_documents(self.docs_dir)
        en_matrix = self.generate_version_matrix(en_docs)
        
        # 한국어 문서 분류
        ko_docs = self.classify_documents(self.ko_docs_dir)
        ko_matrix = self.generate_version_matrix(ko_docs)
        
        # 보고서 생성
        if language == "ko":
            return self._generate_korean_report(en_matrix, ko_matrix)
        else:
            return self._generate_english_report(en_matrix, ko_matrix)
    
    def _generate_english_report(self, en_matrix: Dict, ko_matrix: Dict) -> str:
        """영어 보고서 생성"""
        report = f"""---
tags:
  - cnt
  - version
  - classification
  - report
generated_at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

# CNT Version Classification Report

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

## 📊 Overview

### English Documents
"""
        
        # 영어 문서 요약
        total_en = sum(matrix["count"] for matrix in en_matrix.values())
        report += f"- **Total**: {total_en} documents\n"
        
        for version, info in sorted(en_matrix.items()):
            emoji = info["color_info"]["emoji"]
            count = info["count"]
            report += f"- {emoji} **{version}**: {count} documents\n"
        
        report += "\n### Korean Documents\n"
        
        # 한국어 문서 요약
        total_ko = sum(matrix["count"] for matrix in ko_matrix.values())
        report += f"- **Total**: {total_ko} documents\n"
        
        for version, info in sorted(ko_matrix.items()):
            emoji = info["color_info"]["emoji"]
            count = info["count"]
            report += f"- {emoji} **{version}**: {count} documents\n"
        
        report += "\n### Combined Statistics\n"
        report += f"- **Total Documents**: {total_en + total_ko}\n"
        report += f"- **English**: {total_en} ({total_en/(total_en+total_ko)*100:.1f}%)\n"
        report += f"- **Korean**: {total_ko} ({total_ko/(total_en+total_ko)*100:.1f}%)\n"
        
        # 상세 분류
        report += "\n---\n\n## 📋 Detailed Classification\n\n### English Documents by Version\n"
        
        for version, info in sorted(en_matrix.items()):
            emoji = info["color_info"]["emoji"]
            report += f"\n#### {emoji} {version} ({info['count']} documents)\n"
            
            for doc_type, count in sorted(info["types"].items()):
                report += f"- **{doc_type}**: {count}\n"
        
        report += "\n### Korean Documents by Version\n"
        
        for version, info in sorted(ko_matrix.items()):
            emoji = info["color_info"]["emoji"]
            report += f"\n#### {emoji} {version} ({info['count']} documents)\n"
            
            for doc_type, count in sorted(info["types"].items()):
                report += f"- **{doc_type}**: {count}\n"
        
        return report
    
    def _generate_korean_report(self, en_matrix: Dict, ko_matrix: Dict) -> str:
        """한국어 보고서 생성"""
        report = f"""---
tags:
  - cnt
  - version
  - classification
  - report
generated_at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

# CNT 버전 분류 보고서

*생성 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

## 📊 개요

### 영어 문서
"""
        
        # 영어 문서 요약
        total_en = sum(matrix["count"] for matrix in en_matrix.values())
        report += f"- **전체**: {total_en}개 문서\n"
        
        for version, info in sorted(en_matrix.items()):
            emoji = info["color_info"]["emoji"]
            count = info["count"]
            report += f"- {emoji} **{version}**: {count}개 문서\n"
        
        report += "\n### 한국어 문서\n"
        
        # 한국어 문서 요약
        total_ko = sum(matrix["count"] for matrix in ko_matrix.values())
        report += f"- **전체**: {total_ko}개 문서\n"
        
        for version, info in sorted(ko_matrix.items()):
            emoji = info["color_info"]["emoji"]
            count = info["count"]
            report += f"- {emoji} **{version}**: {count}개 문서\n"
        
        report += "\n### 통계\n"
        report += f"- **전체 문서**: {total_en + total_ko}개\n"
        report += f"- **영어**: {total_en}개 ({total_en/(total_en+total_ko)*100:.1f}%)\n"
        report += f"- **한국어**: {total_ko}개 ({total_ko/(total_en+total_ko)*100:.1f}%)\n"
        
        # 상세 분류
        report += "\n---\n\n## 📋 상세 분류\n\n### 영어 문서 (버전별)\n"
        
        for version, info in sorted(en_matrix.items()):
            emoji = info["color_info"]["emoji"]
            report += f"\n#### {emoji} {version} ({info['count']}개 문서)\n"
            
            for doc_type, count in sorted(info["types"].items()):
                report += f"- **{doc_type}**: {count}개\n"
        
        report += "\n### 한국어 문서 (버전별)\n"
        
        for version, info in sorted(ko_matrix.items()):
            emoji = info["color_info"]["emoji"]
            report += f"\n#### {emoji} {version} ({info['count']}개 문서)\n"
            
            for doc_type, count in sorted(info["types"].items()):
                report += f"- **{doc_type}**: {count}개\n"
        
        return report
    
    def generate_canvas_config(self) -> Dict:
        """Canvas 색상 구성 생성"""
        canvas_config = {
            "version_colors": {},
            "type_colors": {},
            "connection_colors": {}
        }
        
        # 버전별 색상
        for version, info in self.color_mapping.items():
            canvas_config["version_colors"][version] = {
                "hex": self._get_hex_color(info["color"]),
                "emoji": info["emoji"],
                "status": info["status"]
            }
        
        # 문서 유형별 색상
        type_colors = {
            "architecture": "#2196F3",    # 파란색
            "validation": "#4CAF50",      # 녹색
            "implementation": "#FF9800",  # 주황색
            "operation": "#9C27B0",       # 보라색
            "automation": "#F44336",      # 빨간색
            "performance": "#00BCD4",     # 청록색
            "obsidian": "#795548",        # 갈색
            "protocol": "#607D8B",        # 청회색
            "status": "#FFC107",          # 노란색
            "fix": "#E91E63",             # 핑크색
            "general": "#9E9E9E"          # 회색
        }
        
        canvas_config["type_colors"] = type_colors
        
        # 연결선 색상
        canvas_config["connection_colors"] = {
            "completed": "#4CAF50",    # 완료
            "designed": "#2196F3",     # 설계
            "implementation": "#FF9800", # 구현
            "automation": "#9C27B0",    # 자동화
            "planned": "#F44336"        # 계획
        }
        
        return canvas_config
    
    def _get_hex_color(self, color_name: str) -> str:
        """색상 이름을 HEX 코드로 변환"""
        color_map = {
            "green": "#4CAF50",
            "blue": "#2196F3",
            "orange": "#FF9800",
            "purple": "#9C27B0",
            "red": "#F44336",
            "yellow": "#FFC107",
            "white": "#FFFFFF"
        }
        return color_map.get(color_name.lower(), "#9E9E9E")
    
    def save_classification_report(self, language: str = "en") -> str:
        """분류 보고서 저장"""
        report = self.generate_classification_report(language)
        
        if language == "ko":
            filename = "CNT 버전 분류 보고서.md"
            output_dir = self.docs_dir / "ko"
        else:
            filename = "CNT Version Classification Report.md"
            output_dir = self.docs_dir
        
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(output_path)
    
    def save_canvas_config(self) -> str:
        """Canvas 설정 저장"""
        config = self.generate_canvas_config()
        
        config_path = self.docs_dir / "canvas_color_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return str(config_path)

def main():
    """메인 실행 함수"""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    classifier = VersionClassifier(repo_root)
    
    print("CNT Version Classifier")
    print("=" * 50)
    
    # 영어 보고서 생성
    try:
        en_report_path = classifier.save_classification_report("en")
        print(f"✅ English report saved: {en_report_path}")
    except Exception as e:
        print(f"❌ Failed to save English report: {e}")
    
    # 한국어 보고서 생성
    try:
        ko_report_path = classifier.save_classification_report("ko")
        print(f"✅ Korean report saved: {ko_report_path}")
    except Exception as e:
        print(f"❌ Failed to save Korean report: {e}")
    
    # Canvas 설정 생성
    try:
        config_path = classifier.save_canvas_config()
        print(f"✅ Canvas config saved: {config_path}")
    except Exception as e:
        print(f"❌ Failed to save Canvas config: {e}")
    
    # 통계 출력
    en_docs = classifier.classify_documents(classifier.docs_dir)
    ko_docs = classifier.classify_documents(classifier.ko_docs_dir)
    
    total_en = len(en_docs)
    total_ko = len(ko_docs)
    total = total_en + total_ko
    
    print(f"\n📊 Classification Summary:")
    print(f"Total Documents: {total}")
    print(f"English: {total_en} ({total_en/total*100:.1f}%)")
    print(f"Korean: {total_ko} ({total_ko/total*100:.1f}%)")

if __name__ == "__main__":
    main()
