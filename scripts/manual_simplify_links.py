#!/usr/bin/env python3
"""
CNT Manual Link Simplifier - 수동으로 특정 파일의 링크를 단순화하는 스크립트
"""

import os
import re
from pathlib import Path

def simplify_extra_items_register():
    """EXTRA ITEMS REGISTER.md 파일의 링크 단순화"""
    file_path = Path("c:/cnt/docs/EXTRA ITEMS REGISTER.md")
    
    if not file_path.exists():
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Obsidian Links 섹션 찾기 및 단순화
        lines = content.split('\n')
        simplified_lines = []
        in_links_section = False
        
        for line in lines:
            if '## Obsidian Links' in line:
                in_links_section = True
                simplified_lines.append(line)
                # 핵심 링크만 남기고 단순화
                simplified_lines.append("")
                simplified_lines.append("### 핵심 링크")
                simplified_lines.append("- [[00 Docs Index|문서 인덱스]]")
                simplified_lines.append("- [[AGENTS|시스템 규칙]]")
                simplified_lines.append("")
                simplified_lines.append("### 관련 문서")
                simplified_lines.append("- [[CNT v2 ARCHITECTURE DESIGN DOCUMENT|아키텍처 설계]]")
                simplified_lines.append("- [[CNT DATA DASHBOARD|데이터 대시보드]]")
                simplified_lines.append("")
                simplified_lines.append("*링크가 단순화되었습니다*")
                continue
            elif in_links_section and line.startswith('## '):
                in_links_section = False
                simplified_lines.append(line)
                continue
            elif in_links_section:
                # 기존 링크 섹션은 건너뛰기
                continue
            else:
                simplified_lines.append(line)
        
        simplified_content = '\n'.join(simplified_lines)
        
        if simplified_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(simplified_content)
            print(f"✅ 단순화 완료: {file_path}")
            return True
        else:
            print("변경사항이 없습니다.")
            return False
            
    except Exception as e:
        print(f"오류 발생: {e}")
        return False

def simplify_docs_index():
    """00 Docs Index.md 파일의 링크 단순화"""
    file_path = Path("c:/cnt/docs/00 Docs Index.md")
    
    if not file_path.exists():
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 각 섹션의 링크를 3개로 제한
        lines = content.split('\n')
        simplified_lines = []
        current_section = ""
        link_count = 0
        
        for line in lines:
            if line.startswith('## '):
                current_section = line
                simplified_lines.append(line)
                link_count = 0
                continue
            elif line.startswith('- [['):
                link_count += 1
                # 각 섹션별 최대 3개 링크만 유지
                if link_count <= 3:
                    simplified_lines.append(line)
                else:
                    continue
            else:
                simplified_lines.append(line)
        
        simplified_content = '\n'.join(simplified_lines)
        
        if simplified_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(simplified_content)
            print(f"✅ 단순화 완료: {file_path}")
            return True
        else:
            print("변경사항이 없습니다.")
            return False
            
    except Exception as e:
        print(f"오류 발생: {e}")
        return False

def simplify_korean_docs_index():
    """00 Docs Index KO.md 파일의 링크 단순화"""
    file_path = Path("c:/cnt/docs/ko/00 Docs Index KO.md")
    
    if not file_path.exists():
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 각 섹션의 링크를 3개로 제한
        lines = content.split('\n')
        simplified_lines = []
        current_section = ""
        link_count = 0
        
        for line in lines:
            if line.startswith('## '):
                current_section = line
                simplified_lines.append(line)
                link_count = 0
                continue
            elif line.startswith('- [['):
                link_count += 1
                # 각 섹션별 최대 3개 링크만 유지
                if link_count <= 3:
                    simplified_lines.append(line)
                else:
                    continue
            else:
                simplified_lines.append(line)
        
        simplified_content = '\n'.join(simplified_lines)
        
        if simplified_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(simplified_content)
            print(f"✅ 단순화 완료: {file_path}")
            return True
        else:
            print("변경사항이 없습니다.")
            return False
            
    except Exception as e:
        print(f"오류 발생: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("CNT Manual Link Simplifier")
    print("=" * 40)
    
    # 주요 파일들 단순화
    files_simplified = 0
    
    print("\n1. EXTRA ITEMS REGISTER.md 단순화...")
    if simplify_extra_items_register():
        files_simplified += 1
    
    print("\n2. 00 Docs Index.md 단순화...")
    if simplify_docs_index():
        files_simplified += 1
    
    print("\n3. 00 Docs Index KO.md 단순화...")
    if simplify_korean_docs_index():
        files_simplified += 1
    
    print(f"\n✅ 완료: {files_simplified}개 파일 단순화됨")
    
    # Graph 뷰 확인 안내
    print("\n🔍 Graph 뷰 확인 방법:")
    print("1. Obsidian에서 Ctrl+G로 Graph 뷰 열기")
    print("2. 노드 간 연결이 단순화된 것 확인")
    print("3. 핵심 문서 간 연결이 명확히 보이는지 확인")

if __name__ == "__main__":
    main()
