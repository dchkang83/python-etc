#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
from datetime import datetime
from read_subway_data import get_subway_lines

def generate_subway_insert_sql():
    """
    지하철 엑셀 파일을 읽어서 SUBWAY 테이블 INSERT SQL을 생성하는 함수
    """
    # 파일 경로 설정
    file_path = "/Users/deokjoonkang/dev/projects/gundam/claude/subway/전체_도시철도역사정보_20250417.xlsx"
    
    try:
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            print(f"파일을 찾을 수 없습니다: {file_path}")
            return None
        
        # 엑셀 파일 읽기
        print("지하철 데이터를 읽는 중...")
        df = pd.read_excel(file_path)
        
        # 노선 딕셔너리 가져오기
        subway_lines = get_subway_lines()
        if subway_lines is None:
            print("노선 정보를 가져올 수 없습니다.")
            return None
        
        print(f"총 {len(df)}개의 지하철역 데이터를 처리합니다.")
        
        # SQL 파일 생성
        output_file = "subway_insert.sql"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # SQL 파일 헤더 작성
            f.write("-- 지하철역 데이터 INSERT SQL\n")
            f.write(f"-- 생성일시: {current_time}\n")
            f.write(f"-- 총 {len(df)}개의 지하철역 데이터\n\n")
            
            # INSERT 문 시작
            f.write("INSERT INTO SUBWAY (PLACE_CODE, FULL_NAME, LINE_CODE, LINE, LINE_SHORT, NAME, LATITUDE, LONGITUDE, USE_YN, REG_DT) VALUES\n")
            
            # 각 행을 SQL INSERT 값으로 변환
            sql_values = []
            
            for index, row in df.iterrows():
                try:
                    # 각 컬럼 데이터 추출 및 변환
                    place_code = str(row['역번호']).strip() if pd.notna(row['역번호']) else ''
                    full_name = str(row['역사명']).strip() if pd.notna(row['역사명']) else ''
                    line_code = str(row['노선번호']).strip() if pd.notna(row['노선번호']) else ''
                    line = str(row['노선명']).strip() if pd.notna(row['노선명']) else ''
                    
                    # 노선 단축명 생성 (노선명에서 숫자만 추출)
                    import re
                    line_short_match = re.search(r'(\d+)호선', line)
                    if line_short_match:
                        line_short = f"{line_short_match.group(1)}호선"
                    else:
                        # 특별한 노선들의 단축명 처리
                        line_short_map = {
                            '경인선': '경인선',
                            '신분당선': '신분당선',
                            '분당선': '분당선',
                            '경춘선': '경춘선',
                            '인천국제공항선': '공항선',
                            '수인선': '수인선',
                            '경의중앙선': '경의중앙선',
                            '서해선': '서해선',
                            '김포도시철도': '김포선',
                            '에버라인': '에버라인',
                            '우이신설선': '우이선',
                            '신림선': '신림선'
                        }
                        line_short = line_short_map.get(line, line)
                    
                    name = full_name  # 지하철 명은 역사명과 동일
                    
                    # 위도/경도 처리
                    latitude = float(row['역위도']) if pd.notna(row['역위도']) else 0.0
                    longitude = float(row['역경도']) if pd.notna(row['역경도']) else 0.0
                    
                    # 데이터 유효성 검사
                    if not place_code or not full_name or not line_code or not line:
                        print(f"⚠️  행 {index+1}: 필수 데이터 누락 - 건너뜀")
                        continue
                    
                    if latitude == 0.0 and longitude == 0.0:
                        print(f"⚠️  행 {index+1}: 위도/경도 데이터 없음 - 건너뜀")
                        continue
                    
                    # SQL 값 생성
                    sql_value = f"('{place_code}', '{full_name}', '{line_code}', '{line}', '{line_short}', '{name}', {latitude}, {longitude}, 'Y', NOW())"
                    sql_values.append(sql_value)
                    
                    if (index + 1) % 100 == 0:
                        print(f"진행률: {index + 1}/{len(df)} ({((index + 1) / len(df) * 100):.1f}%)")
                
                except Exception as e:
                    print(f"❌ 행 {index+1} 처리 중 오류: {str(e)}")
                    continue
            
            # SQL 값들을 파일에 작성
            for i, sql_value in enumerate(sql_values):
                if i == len(sql_values) - 1:
                    f.write(sql_value + ";\n")
                else:
                    f.write(sql_value + ",\n")
            
            # SQL 파일 푸터
            f.write(f"\n-- 총 {len(sql_values)}개의 INSERT 문이 생성되었습니다.\n")
            f.write(f"-- 생성 완료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"\n✅ SQL 파일이 성공적으로 생성되었습니다!")
        print(f"📁 파일명: {output_file}")
        print(f"📊 총 {len(sql_values)}개의 INSERT 문이 생성되었습니다.")
        print(f"📈 처리된 데이터: {len(sql_values)}/{len(df)} ({len(sql_values)/len(df)*100:.1f}%)")
        
        return output_file
        
    except Exception as e:
        print(f"SQL 생성 중 오류가 발생했습니다: {str(e)}")
        return None

def preview_sql_file(filename, lines=10):
    """
    생성된 SQL 파일의 미리보기를 출력하는 함수
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.readlines()
        
        print(f"\n📋 SQL 파일 미리보기 (처음 {lines}줄):")
        print("=" * 60)
        for i, line in enumerate(content[:lines]):
            print(f"{i+1:2d}: {line.rstrip()}")
        
        if len(content) > lines:
            print("...")
            print(f"총 {len(content)}줄")
        
    except Exception as e:
        print(f"파일 미리보기 중 오류: {str(e)}")

if __name__ == "__main__":
    # SQL 파일 생성
    sql_file = generate_subway_insert_sql()
    
    if sql_file:
        # 생성된 SQL 파일 미리보기
        preview_sql_file(sql_file, 15)
        
        print(f"\n🎉 지하철역 데이터 INSERT SQL 생성이 완료되었습니다!")
        print(f"💡 생성된 파일을 데이터베이스에서 실행하세요.")
    else:
        print("❌ SQL 파일 생성에 실패했습니다.") 