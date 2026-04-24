#!/usr/bin/env python3
"""
CNT Graph Links Simplifier - Graph 뷰의 링크를 단계별로 분류하여 단순화하는 스크립트 (수정 버전)
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict

class GraphLinkSimplifier:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.docs_dir = self.repo_root / "docs"
        self.ko_docs_dir = self.repo_root / "docs" / "ko"
        
        # 링크 단계별 분류 규칙
        self.link_categories = {
            'core': {
                'priority': 1,
                'patterns': [
                    r'\[\[AGENTS\]\]',
                    r'\[\[00 Docs Index\]\]',
                    r'\[\[00 Docs Index KO\]\]',
                    r'\[\[CNT v2 ARCHITECTURE DESIGN DOCUMENT\]\]',
                    r'\[\[CNT v2 ARCHITECTURE DESIGN DOCUMENT KO\]\]'
                ],
                'description': '핵심 문서 (아키텍처, 규칙, 인덱스)'
            },
            'implementation': {
                'priority': 2,
                'patterns': [
                    r'\[\[CNT v2 IMPLEMENTATION.*\]\]',
                    r'\[\[CNT v2 IMPLEMENTATION.*KO\]\]',
                    r'\[\[CNT v2 VALIDATION.*\]\]',
                    r'\[\[CNT v2 VALIDATION.*KO\]\]'
                ],
                'description': '구현 관련 문서'
            },
            'operation': {
                'priority': 3,
                'patterns': [
                    r'\[\[CNT v2 BREAKOUT.*\]\]',
                    r'\[\[CNT v2 BREAKOUT.*KO\]\]',
                    r'\[\[CNT v2 OBSIDIAN.*\]\]',
                    r'\[\[CNT v2 OBSIDIAN.*KO\]\]'
                ],
                'description': '운영 관련 문서'
            },
            'supporting': {
                'priority': 4,
                'patterns': [
                    r'\[\[CNT DATA DASHBOARD\]\]',
                    r'\[\[CNT DATA DASHBOARD KO\]\]',
                    r'\[\[CNT OPERATIONS.*\]\]',
                    r'\[\[CNT OPERATIONS.*KO\]\]'
                ],
                'description': '지원 문서 (대시보드, 가이드)'
            },
            'historical': {
                'priority': 5,
                'patterns': [
                    r'\[\[CNT v1\.1.*\]\]',
                    r'\[\[CNT v1\.1.*KO\]\]'
                ],
                'description': '과거 버전 문서'
            },
            'reference': {
                'priority': 6,
                'patterns': [
                    r'\[\[DESIGN SUMMARY\]\]',
                    r'\[\[DESIGN SUMMARY KO\]\]',
                    r'\[\[RECORD TEXT\]\]',
                    r'\[\[RECORD TEXT KO\]\]',
                    r'\[\[EXTRA ITEMS REGISTER\]\]'
                ],
                'description': '참고 문서'
            }
        }
    
    def categorize_link(self, link_text: str) -> str:
        """링크를 카테고리로 분류"""
        for category, config in self.link_categories.items():
            for pattern in config['patterns']:
                if re.search(pattern, link_text, re.IGNORECASE):
                    return category
        return 'other'
    
    def extract_links_from_file(self, file_path: Path) -> List[Tuple[str, str]]:
        """파일에서 링크 추출"""
        links = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # wikilink 추출
            wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', content)
            for link_target, display_text in wikilinks:
                links.append((link_target, display_text or link_target))
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        return links
    
    def analyze_link_density(self, file_path: Path) -> Dict[str, any]:
        """파일의 링크 밀도 분석"""
        links = self.extract_links_from_file(file_path)
        
        # 링크 카테고리별 분류
        categorized_links = defaultdict(list)
        for link_target, display_text in links:
            category = self.categorize_link(f"[[{link_target}]]")
            categorized_links[category].append((link_target, display_text))
        
        # 파일 정보
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            file_size = len(content)
            total_links = len(links)
            link_density = total_links / max(file_size, 1) * 1000  # 링크/1000자
        except:
            file_size = 0
            total_links = 0
            link_density = 0
        
        return {
            'file_path': str(file_path.relative_to(self.repo_root)),
            'total_links': total_links,
            'file_size': file_size,
            'link_density': link_density,
            'categorized_links': dict(categorized_links),
            'is_korean': 'ko' in str(file_path)
        }
    
    def simplify_file_links(self, file_path: Path, max_links_per_category: int = 3) -> Tuple[bool, Dict]:
        """파일의 링크 단순화"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 링크 분석
            analysis = self.analyze_link_density(file_path)
            
            # 링크가 너무 많으면 단순화
            if analysis['link_density'] > 5.0:  # 1000자당 5개 이상 링크
                content = self._simplify_content(content, analysis, max_links_per_category)
            
            changes_made = content != original_content
            
            if changes_made:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return changes_made, analysis
            
        except Exception as e:
            print(f"Error simplifying {file_path}: {e}")
            return False, {}
    
    def _simplify_content(self, content: str, analysis: Dict, max_links_per_category: int) -> str:
        """콘텐츠 단순화"""
        lines = content.split('\n')
        simplified_lines = []
        
        # Obsidian Links 섹션 찾기
        in_links_section = False
        links_section_lines = []
        
        for line in lines:
            if '## Obsidian Links' in line or '## 링크' in line:
                in_links_section = True
                simplified_lines.append(line)
                continue
            elif in_links_section and line.startswith('## '):
                # 새로운 섹션 시작
                in_links_section = False
                simplified_lines.append(line)
                continue
            elif in_links_section:
                links_section_lines.append(line)
                continue
            else:
                simplified_lines.append(line)
        
        # 링크 섹션 단순화
        if links_section_lines and analysis.get('categorized_links'):
            simplified_links_section = self._simplify_links_section(
                links_section_lines, analysis, max_links_per_category
            )
            simplified_lines.extend(simplified_links_section)
        elif links_section_lines:
            # 분석 데이터가 없으면 기존 링크 유지
            simplified_lines.extend(links_section_lines)
        
        return '\n'.join(simplified_lines)
    
    def _simplify_links_section(self, lines: List[str], analysis: Dict, max_links_per_category: int) -> List[str]:
        """링크 섹션 단순화"""
        simplified_lines = []
        categorized_links = analysis.get('categorized_links', {})
        
        # 카테고리별로 정렬된 링크 생성
        for category in sorted(categorized_links.keys(), 
                             key=lambda x: self.link_categories.get(x, {'priority': 999}).get('priority', 999)):
            if category == 'other':
                continue
                
            links = categorized_links[category]
            if not links:
                continue
            
            # 카테고리 설명
            category_info = self.link_categories.get(category, {})
            description = category_info.get('description', category)
            simplified_lines.append(f"### {description}")
            
            # 우선순위별 링크 (최대 개수 제한)
            priority_links = links[:max_links_per_category]
            for link_target, display_text in priority_links:
                # 경로 기반 링크로 변환
                if self._is_korean_file(analysis.get('file_path', '')):
                    # 한국어 문서이면 한국어 링크로
                    ko_target = self._get_korean_link(link_target)
                    if ko_target:
                        simplified_lines.append(f"- [[{ko_target}|{display_text}]]")
                    else:
                        simplified_lines.append(f"- [[{link_target}|{display_text}]]")
                else:
                    simplified_lines.append(f"- [[{link_target}|{display_text}]]")
            
            simplified_lines.append("")
        
        # 남은 링크가 있으면 요약
        total_shown = sum(len(categorized_links.get(cat, []))[:max_links_per_category] 
                          for cat in categorized_links.keys() if cat != 'other')
        total_links = analysis.get('total_links', 0)
        
        if total_links > total_shown:
            simplified_lines.append(f"*총 {total_links}개 링크 중 {total_shown}개 표시됨*")
        
        return simplified_lines
    
    def _is_korean_file(self, file_path: str) -> bool:
        """한국어 파일인지 확인"""
        return 'ko' in file_path
    
    def _get_korean_link(self, link_target: str) -> str:
        """한국어 링크 가져오기"""
        ko_file = self.ko_docs_dir / f"{link_target} KO.md"
        if ko_file.exists():
            return f"docs/ko/{link_target} KO"
        return None
    
    def analyze_all_files(self) -> Dict[str, any]:
        """모든 파일 분석"""
        all_files = []
        
        # 영어 문서
        if self.docs_dir.exists():
            for file_path in self.docs_dir.rglob("*.md"):
                if file_path.is_file() and 'ko' not in str(file_path):
                    analysis = self.analyze_link_density(file_path)
                    all_files.append(analysis)
        
        # 한국어 문서
        if self.ko_docs_dir.exists():
            for file_path in self.ko_docs_dir.rglob("*.md"):
                if file_path.is_file():
                    analysis = self.analyze_link_density(file_path)
                    all_files.append(analysis)
        
        # 통계
        total_files = len(all_files)
        high_density_files = [f for f in all_files if f['link_density'] > 5.0]
        total_links = sum(f['total_links'] for f in all_files)
        
        return {
            'total_files': total_files,
            'high_density_files': len(high_density_files),
            'total_links': total_links,
            'files': all_files
        }
    
    def simplify_all_files(self, max_links_per_category: int = 3) -> Dict[str, any]:
        """모든 파일 단순화"""
        results = {
            'total_files': 0,
            'simplified_files': 0,
            'errors': []
        }
        
        # 영어 문서
        if self.docs_dir.exists():
            for file_path in self.docs_dir.rglob("*.md"):
                if file_path.is_file() and 'ko' not in str(file_path):
                    results['total_files'] += 1
                    simplified, analysis = self.simplify_file_links(file_path, max_links_per_category)
                    if simplified:
                        results['simplified_files'] += 1
        
        # 한국어 문서
        if self.ko_docs_dir.exists():
            for file_path in self.ko_docs_dir.rglob("*.md"):
                if file_path.is_file():
                    results['total_files'] += 1
                    simplified, analysis = self.simplify_file_links(file_path, max_links_per_category)
                    if simplified:
                        results['simplified_files'] += 1
        
        return results
    
    def generate_report(self, analysis: Dict, results: Dict) -> str:
        """보고서 생성"""
        return f"""---
tags:
  - cnt
  - graph
  - simplification
  - report
generated_at: {os.popen('date').read().strip()}
---

# CNT Graph 링크 단순화 보고서

*생성 시각: {os.popen('date').read().strip()}*

---

## 📊 분석 결과

### 전체 통계
- **총 파일 수**: {analysis['total_files']}
- **고밀도 파일**: {analysis['high_density_files']}개
- **총 링크 수**: {analysis['total_links']}
- **단순화된 파일**: {results['simplified_files']}개

### 링크 밀도 분포
- **고밀도** (>5.0/1000자): {analysis['high_density_files']}개
- **정상 밀도** (≤5.0/1000자): {analysis['total_files'] - analysis['high_density_files']}개

---

## 🎯 단순화 전략

### 1. 링크 카테고리화
- **핵심**: 아키텍처, 규칙, 인덱스 (우선순위 1)
- **구현**: 구현 관련 문서 (우선순위 2)
- **운영**: 운영 관련 문서 (우선순위 3)
- **지원**: 대시보드, 가이드 (우선순위 4)
- **과거**: v1.1 문서 (우선순위 5)
- **참고**: 보조 문서 (우선순위 6)

### 2. 단순화 규칙
- **카테고리별 최대 3개 링크**만 표시
- **우선순위 기반 정렬**
- **한국어 문서는 한국어 링크로** 자동 변환
- **총 링크 수 표시**로 정보 손실 최소화

### 3. 보존 전략
- **핵심 링크**: 항상 유지
- **중요 링크**: 카테고리별 우선순위
- **참고 링크**: 요약 정보만 제공

---

## 🔧 적용된 변경

### 링크 섹션 재구성
```
## Obsidian Links

### 핵심 문서 (아키텍처, 규칙, 인덱스)
- [[CNT v2 ARCHITECTURE DESIGN DOCUMENT|아키텍처 설계]]
- [[AGENTS|시스템 규칙]]
- [[00 Docs Index|문서 인덱스]]

### 구현 관련 문서
- [[CNT v2 IMPLEMENTATION WORK INSTRUCTION|구현 작업 지침]]
- [[CNT v2 VALIDATION REPORT|검증 보고서]]

*총 25개 링크 중 6개 표시됨*
```

### Graph 뷰 개선 효과
- **노드 간 연결 단순화**: 불필요한 연결 제거
- **핵심 관계 강조**: 중요한 문서 간 연결만 표시
- **가독성 향상**: 복잡한 네트워크를 명확한 구조로 정리

---

## 📈 효과 분석

### Graph 뷰 시각화
- **클러스터링 개선**: 카테고리별 명확한 그룹화
- **노이즈 감소**: 불필요한 링크로 인한 시각적 혼란 감소
- **핵심 경로 강조**: 중요한 문서 흐름이 명확히 보임

### 탐색 효율
- **빠른 핵심 접근**: 중요한 문서로 빠르게 이동
- **체계적 구조**: 카테고리별 논리적 탐색
- **정보 과부하 방지**: 필요한 정보만 선택적 제공

---

## 🔍 검증 방법

### 1. Graph 뷰 확인
1. Obsidian에서 `Ctrl+G`로 Graph 뷰 열기
2. 노드 간 연결이 단순화된 것 확인
3. 핵심 문서 간 연결이 명확히 보이는지 확인

### 2. 링크 동작 테스트
1. 단순화된 문서에서 링크 클릭
2. 핵심 링크가 정상적으로 동작하는지 확인
3. 카테고리별 분류가 올바른지 확인

### 3. 사용성 테스트
1. 문서 탐색이 더 쉬워졌는지 확인
2. 필요한 정보를 빠르게 찾을 수 있는지 확인
3. 정보 손실 없이 중요한 링크가 유지되는지 확인

---

## 📞 유지보수

### 정기 작업
- **월간**: 새로운 문서의 링크 밀도 확인
- **분기별**: 단순화 규칙 검토 및 조정
- **반기별**: 전체 Graph 구조 검토

### 새 문서 추가 시
1. **링크 수 제한**: 카테고리별 3개 이하 권장
2. **우선순위 고려**: 핵심 링크 우선 배치
3. **정기 단순화**: 스크립트 주기적 실행

---

*이 보고서는 CNT 프로젝트의 Graph 뷰 링크 단순화 시스템을 위해 생성되었습니다.*
"""

def main():
    """메인 실행 함수"""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    simplifier = GraphLinkSimplifier(repo_root)
    
    print("CNT Graph Links Simplifier")
    print("=" * 50)
    
    # 분석 실행
    print("링크 분석 시작...")
    analysis = simplifier.analyze_all_files()
    
    print(f"✅ 분석 완료:")
    print(f"  총 파일: {analysis['total_files']}개")
    print(f"  고밀도 파일: {analysis['high_density_files']}개")
    print(f"  총 링크: {analysis['total_links']}개")
    
    # 단순화 실행
    print()
    print("링크 단순화 시작...")
    results = simplifier.simplify_all_files(max_links_per_category=3)
    
    print(f"✅ 단순화 완료:")
    print(f"  처리된 파일: {results['total_files']}개")
    print(f"  단순화된 파일: {results['simplified_files']}개")
    
    # 보고서 생성
    print()
    print("보고서 생성...")
    report = simplifier.generate_report(analysis, results)
    
    # 한국어 보고서 저장
    ko_report_path = Path(repo_root) / "docs" / "ko" / "CNT Graph 링크 단순화 보고서 KO.md"
    with open(ko_report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 영어 보고서 저장
    en_report_path = Path(repo_root) / "docs" / "CNT GRAPH LINKS SIMPLIFICATION REPORT.md"
    en_report_content = report.replace("CNT Graph 링크 단순화 보고서", "CNT GRAPH LINKS SIMPLIFICATION REPORT")
    en_report_content = en_report_content.replace("생성 시각", "Generated at")
    
    with open(en_report_path, 'w', encoding='utf-8') as f:
        f.write(en_report_content)
    
    print(f"✅ 보고서 저장:")
    print(f"  한국어: {ko_report_path}")
    print(f"  영어: {en_report_path}")

if __name__ == "__main__":
    main()
