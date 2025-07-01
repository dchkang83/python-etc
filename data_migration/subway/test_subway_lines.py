#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from read_subway_data import get_subway_lines

def main():
    """
    노선번호별 노선명 딕셔너리 사용 예시
    """
    print("🚇 지하철 노선 정보 딕셔너리 사용 예시")
    print("=" * 50)
    
    # 노선 딕셔너리 가져오기
    subway_lines = get_subway_lines()
    
    if subway_lines is None:
        print("❌ 노선 정보를 가져올 수 없습니다.")
        return
    
    print(f"✅ 총 {len(subway_lines)}개의 노선 정보를 가져왔습니다.\n")
    
    # 사용 예시 1: 특정 노선번호의 노선명 찾기
    print("📋 사용 예시 1: 특정 노선번호의 노선명 찾기")
    test_line_numbers = ['I1101', 'S1102', 'I4105', 'I28A1']
    
    for line_number in test_line_numbers:
        if line_number in subway_lines:
            print(f"  {line_number} → {subway_lines[line_number]}")
        else:
            print(f"  {line_number} → 노선을 찾을 수 없습니다.")
    
    print()
    
    # 사용 예시 2: 모든 노선 정보 출력
    print("📋 사용 예시 2: 모든 노선 정보 (정렬된 순서)")
    for line_number, line_name in sorted(subway_lines.items()):
        print(f"  {line_number}: {line_name}")
    
    print()
    
    # 사용 예시 3: 노선명으로 노선번호 찾기
    print("📋 사용 예시 3: 노선명으로 노선번호 찾기")
    test_line_names = ['경인선', '2호선', '분당선', '인천국제공항선']
    
    for line_name in test_line_names:
        found_lines = [num for num, name in subway_lines.items() if line_name in name]
        if found_lines:
            print(f"  '{line_name}' → {found_lines}")
        else:
            print(f"  '{line_name}' → 노선을 찾을 수 없습니다.")
    
    print()
    
    # 사용 예시 4: 딕셔너리 키와 값 리스트
    print("📋 사용 예시 4: 딕셔너리 키와 값 리스트")
    line_numbers = list(subway_lines.keys())
    line_names = list(subway_lines.values())
    
    print(f"  노선번호 리스트 (처음 5개): {line_numbers[:5]}")
    print(f"  노선명 리스트 (처음 5개): {line_names[:5]}")
    
    print()
    print("🎉 노선 딕셔너리 사용 예시 완료!")

if __name__ == "__main__":
    main() 