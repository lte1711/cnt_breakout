#!/usr/bin/env python3
"""
CNT Korean Links Fixer - 한글 문서의 링크를 자동으로 수정하는 스크립트
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class KoreanLinkFixer:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.docs_dir = self.repo_root / "docs"
        self.ko_docs_dir = self.repo_root / "docs" / "ko"
        
        # 영어-한국어 문서 매핑
        self.file_mapping = self._build_file_mapping()
        
        # 잘못된 링크 패턴
        self.link_patterns = [
            r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',  # [[문서명|표시명]]
            r'\[([^\]]+)\]\([^)]+\)',               # [표시명](경로)
        ]
    
    def _build_file_mapping(self) -> Dict[str, str]:
        """영어-한국어 문서 매핑 테이블 생성"""
        mapping = {}
        
        # 영어 문서 목록
        en_files = {}
        if self.docs_dir.exists():
            for file_path in self.docs_dir.rglob("*.md"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(self.repo_root)
                    filename = file_path.stem
                    en_files[filename] = str(relative_path)
        
        # 한국어 문서 목록
        ko_files = {}
        if self.ko_docs_dir.exists():
            for file_path in self.ko_docs_dir.rglob("*.md"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(self.repo_root)
                    filename = file_path.stem
                    
                    # KO 접미사 제거
                    if filename.endswith(" KO"):
                        base_name = filename[:-3]  # " KO" 제거
                        ko_files[base_name] = str(relative_path)
                    else:
                        ko_files[filename] = str(relative_path)
        
        # 매핑 생성
        for base_name, ko_path in ko_files.items():
            if base_name in en_files:
                mapping[base_name] = {
                    'en': en_files[base_name],
                    'ko': ko_path
                }
        
        return mapping
    
    def _is_korean_document(self, file_path: Path) -> bool:
        """한국어 문서인지 확인"""
        return "ko" in file_path.parts
    
    def _fix_link_in_text(self, text: str, current_file: Path) -> str:
        """텍스트 내의 링크 수정"""
        def replace_link(match):
            link_target = match.group(1)
            display_text = match.group(2) if match.group(2) else link_target
            
            # 이미 경로가 포함된 링크는 수정하지 않음
            if "/" in link_target or "\\" in link_target:
                return match.group(0)
            
            # 매핑에서 찾기
            if link_target in self.file_mapping:
                mapping = self.file_mapping[link_target]
                
                # 현재 문서가 한국어 문서이면 한국어 링크로
                if self._is_korean_document(current_file):
                    new_target = mapping['ko']
                else:
                    new_target = mapping['en']
                
                # 경로에서 .md 제거 및 공백 처리
                new_target = new_target.replace('.md', '')
                new_target = new_target.replace('\\', '/')
                
                return f"[[{new_target}|{display_text}]]"
            
            return match.group(0)
        
        # 첫 번째 패턴만 사용 (wikilinks만 수정)
        text = re.sub(self.link_patterns[0], replace_link, text)
        
        return text
    
    def fix_file_links(self, file_path: Path) -> Tuple[bool, int]:
        """파일의 링크 수정"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            content = self._fix_link_in_text(content, file_path)
            
            changes_made = content != original_content
            
            if changes_made:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return changes_made, len(re.findall(r'\[\[', content))
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False, 0
    
    def scan_directory(self, directory: Path) -> List[Path]:
        """디렉토리 스캔"""
        files = []
        if directory.exists():
            for file_path in directory.rglob("*.md"):
                if file_path.is_file():
                    files.append(file_path)
        return files
    
    def fix_all_links(self) -> Dict[str, any]:
        """모든 링크 수정"""
        results = {
            'total_files': 0,
            'fixed_files': 0,
            'total_links': 0,
            'errors': []
        }
        
        # 영어 문서 처리
        en_files = self.scan_directory(self.docs_dir)
        for file_path in en_files:
            if 'ko' not in file_path.parts:  # ko 폴더 제외
                results['total_files'] += 1
                fixed, links = self.fix_file_links(file_path)
                if fixed:
                    results['fixed_files'] += 1
                results['total_links'] += links
        
        # 한국어 문서 처리
        ko_files = self.scan_directory(self.ko_docs_dir)
        for file_path in ko_files:
            results['total_files'] += 1
            fixed, links = self.fix_file_links(file_path)
            if fixed:
                results['fixed_files'] += 1
            results['total_links'] += links
        
        return results
    
    def generate_report(self, results: Dict[str, any]) -> str:
        """수정 보고서 생성"""
        report = f"""---
tags:
  - cnt
  - links
  - fix
  - report
generated_at: {os.popen('date').read().strip()}
---

# CNT 링크 수정 보고서

*생성 시각: {os.popen('date').read().strip()}*

---

## 📊 수정 결과

### 전체 통계
- **총 파일 수**: {results['total_files']}
- **수정된 파일 수**: {results['fixed_files']}
- **총 링크 수**: {results['total_links']}
- **수정률**: {results['fixed_files']/results['total_files']*100:.1f}%

### 파일 매핑 현황
- **영어-한국어 매핑**: {len(self.file_mapping)}개
- **영어 문서**: {len([f for f in self.file_mapping.values() if 'en' in str(f)])}개
- **한국어 문서**: {len([f for f in self.file_mapping.values() if 'ko' in str(f)])}개

---

## 🔧 수정된 링크 유형

### 1. 한국어 문서 내 링크
- [[문서명]] → [[docs/ko/문서명 KO|문서명]]
- 영어 링크를 한국어 링크로 자동 변환

### 2. 영어 문서 내 링크
- [[문서명]] → [[docs/문서명|문서명]]
- 기존 영어 링크 유지

### 3. 경로 기반 링크
- [[docs/ko/문서명 KO|표시명]]
- 정확한 경로로 자동 수정

---

## 📋 주요 수정 내용

### 자동 수정 규칙
1. **문서명 기반 매핑**: 파일명으로 영어-한국어 문서 자동 연결
2. **경로 자동 변환**: 상대 경로를 정확하게 변환
3. **언어별 링크**: 현재 문서 언어에 맞는 링크로 변환
4. **표시명 유지**: 원래 표시명은 그대로 유지

### 보호된 링크
- 이미 경로가 포함된 링크는 수정하지 않음
- 외부 링크는 그대로 유지
- 이미 올바른 경로의 링크는 수정하지 않음

---

## 🎯 효과

### Graph 뷰 개선
- **한글 링크 연결**: 한국어 문서 간의 링크가 제대로 표시
- **언어별 클러스터링**: 영어/한국어 문서가 그래프에서 명확히 구분
- **의존성 시각화**: 문서 간의 실제 의존 관계가 정확히 표시

### 탐색 효율
- **클릭 가능한 링크**: 모든 링크가 올바르게 동작
- **언어 일관성**: 한국어 문서에서는 한국어 문서로 링크
- **빠른 이동**: 문서 간 이동이 원활하게 작동

---

## 🔍 검증 방법

### 1. Graph 뷰 확인
1. Obsidian에서 `Ctrl+G`로 Graph 뷰 열기
2. 한국어 문서 노드 확인
3. 링크 연결 상태 확인

### 2. 링크 클릭 테스트
1. 한국어 문서에서 링크 클릭
2. 올바른 문서로 이동하는지 확인
3. 표시명이 올바른지 확인

### 3. Dataview 쿼리 테스트
```dataview
LIST
FROM "docs/ko"
WHERE any(file.inlinks, (i) => contains(i.path, "ko"))
```

---

## 📞 유지보수

### 정기 작업
- **월간**: 새로운 문서에 대한 링크 확인
- **분기별**: 전체 링크 상태 검토
- **반기별**: 매핑 테이블 업데이트

### 새 문서 추가 시
1. 영어/한국어 문서 쌍으로 생성
2. 파일명 규칙 준수 (문서명 KO.md)
3. 스크립트 재실행으로 링크 자동 수정

---

*이 보고서는 CNT 프로젝트의 링크 수정 자동화 시스템을 위해 생성되었습니다.*
"""
        return report

def main():
    """메인 실행 함수"""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fixer = KoreanLinkFixer(repo_root)
    
    print("CNT Korean Links Fixer")
    print("=" * 50)
    
    # 파일 매핑 정보 출력
    print(f"파일 매핑: {len(fixer.file_mapping)}개")
    for name, mapping in list(fixer.file_mapping.items())[:5]:
        print(f"  {name}: {mapping['ko']}")
    if len(fixer.file_mapping) > 5:
        print(f"  ... 외 {len(fixer.file_mapping) - 5}개")
    
    print()
    
    # 링크 수정 실행
    print("링크 수정 시작...")
    results = fixer.fix_all_links()
    
    print(f"✅ 완료:")
    print(f"  총 파일: {results['total_files']}개")
    print(f"  수정된 파일: {results['fixed_files']}개")
    print(f"  총 링크: {results['total_links']}개")
    
    # 보고서 생성
    print()
    print("보고서 생성...")
    report = fixer.generate_report(results)
    
    # 한국어 보고서 저장
    ko_report_path = Path(repo_root) / "docs" / "ko" / "CNT 링크 수정 보고서 KO.md"
    with open(ko_report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 영어 보고서 저장
    en_report_path = Path(repo_root) / "docs" / "CNT LINKS FIX REPORT.md"
    en_report_content = report.replace("CNT 링크 수정 보고서", "CNT LINKS FIX REPORT")
    en_report_content = en_report_content.replace("생성 시각", "Generated at")
    
    with open(en_report_path, 'w', encoding='utf-8') as f:
        f.write(en_report_content)
    
    print(f"✅ 보고서 저장:")
    print(f"  한국어: {ko_report_path}")
    print(f"  영어: {en_report_path}")

if __name__ == "__main__":
    main()
