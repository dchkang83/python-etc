#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
from datetime import datetime
from subway_line_mapping import get_line_mapping_dict, get_line_short_mapping_dict

def generate_subway_insert_sql():
    """
    지하철 엑셀 파일을 읽어서 SUBWAY 테이블 INSERT SQL을 생성하는 함수
    """
    # 파일 경로 설정
    file_path = "/Users/deokjoonkang/dev/projects/gundam/python/python-etc/data_migration/subway/전체_도시철도역사정보_20250417.xlsx"
    
    try:
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            print(f"파일을 찾을 수 없습니다: {file_path}")
            return None
        
        # 엑셀 파일 읽기
        print("지하철 데이터를 읽는 중...")
        df = pd.read_excel(file_path)
        
        # 노선 매핑 딕셔너리 가져오기
        line_mapping = get_line_mapping_dict()
        line_short_mapping = get_line_short_mapping_dict()
        
        print(f"총 {len(df)}개의 지하철역 데이터를 처리합니다.")
        print(f"노선 매핑 딕셔너리: {len(line_mapping)}개 노선")
        
        # SQL 파일 생성
        output_file = "data_migration/subway/subway_insert.sql"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # SQL 파일 헤더 작성
            f.write("-- 지하철역 데이터 INSERT SQL\n")
            f.write(f"-- 생성일시: {current_time}\n")
            f.write(f"-- 총 {len(df)}개의 지하철역 데이터\n")
            f.write("-- 노선번호 코드별 매핑된 노선명 사용\n")
            f.write("-- FULL_NAME 형식: LINE_NAME\n\n")
            
            # INSERT 문 시작
            f.write("INSERT INTO SUBWAY (PLACE_CODE, FULL_NAME, LINE_CODE, LINE, LINE_SHORT, NAME, LATITUDE, LONGITUDE, USE_YN, REG_DT) VALUES\n")
            
            # 각 행을 SQL INSERT 값으로 변환
            sql_values = []
            skipped_count = 0
            
            for index, row in df.iterrows():
                try:
                    # 각 컬럼 데이터 추출 및 변환
                    place_code = str(row['역번호']).strip() if pd.notna(row['역번호']) else ''
                    raw_full_name = str(row['역사명']).strip() if pd.notna(row['역사명']) else ''
                    line_code = str(row['노선번호']).strip() if pd.notna(row['노선번호']) else ''
                    
                    # 노선번호 코드에 따른 노선명 매핑
                    if line_code in line_mapping:
                        line = line_mapping[line_code]
                        line_short = line_short_mapping[line_code]
                        
                        # 빈 값으로 설정된 노선은 제외
                        if not line or line.strip() == '':
                            print(f"⚠️  행 {index+1}: 제외된 노선번호 코드 '{line_code}' - 건너뜀")
                            skipped_count += 1
                            continue
                    else:
                        print(f"⚠️  행 {index+1}: 알 수 없는 노선번호 코드 '{line_code}' - 건너뜀")
                        skipped_count += 1
                        continue
                    
                    # NAME 처리: 괄호 제거 후 "역" 추가
                    # 괄호가 포함된 경우 괄호 부분 제거
                    if '(' in raw_full_name and ')' in raw_full_name:
                        # 괄호 시작 위치 찾기
                        bracket_start = raw_full_name.find('(')
                        name_without_bracket = raw_full_name[:bracket_start].strip()
                    else:
                        name_without_bracket = raw_full_name
                    
                    # "역"이 없으면 "역" 추가
                    if name_without_bracket and not name_without_bracket.endswith('역'):
                        name = name_without_bracket + '역'
                    else:
                        name = name_without_bracket
                    
                    # FULL_NAME 처리: LINE + '_' + NAME 형태 (NAME에 이미 역이 포함됨)
                    full_name = f"{line}_{name}"
                    
                    # 위도/경도 처리
                    latitude = float(row['역위도']) if pd.notna(row['역위도']) else 0.0
                    longitude = float(row['역경도']) if pd.notna(row['역경도']) else 0.0
                    
                    # 데이터 유효성 검사
                    if not place_code or not full_name or not line_code:
                        print(f"⚠️  행 {index+1}: 필수 데이터 누락 - 건너뜀")
                        skipped_count += 1
                        continue
                    
                    if latitude == 0.0 and longitude == 0.0:
                        print(f"⚠️  행 {index+1}: 위도/경도 데이터 없음 - 건너뜀")
                        skipped_count += 1
                        continue
                    
                    # SQL 값 생성
                    sql_value = f"('{place_code}', '{full_name}', '{line_code}', '{line}', '{line_short}', '{name}', {latitude}, {longitude}, 'Y', NOW())"
                    sql_values.append(sql_value)
                    
                    if (index + 1) % 100 == 0:
                        print(f"진행률: {index + 1}/{len(df)} ({((index + 1) / len(df) * 100):.1f}%)")
                
                except Exception as e:
                    print(f"❌ 행 {index+1} 처리 중 오류: {str(e)}")
                    skipped_count += 1
                    continue
            
            # SQL 값들을 파일에 작성
            for i, sql_value in enumerate(sql_values):
                if i == len(sql_values) - 1:
                    f.write(sql_value + ";\n")
                else:
                    f.write(sql_value + ",\n")
            
            # SQL 파일 푸터
            f.write(f"\n-- 총 {len(sql_values)}개의 INSERT 문이 생성되었습니다.\n")
            f.write(f"-- 제외된 데이터: {skipped_count}개\n")
            f.write(f"-- 생성 완료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"\n✅ SQL 파일이 성공적으로 생성되었습니다!")
        print(f"📁 파일명: {output_file}")
        print(f"📊 총 {len(sql_values)}개의 INSERT 문이 생성되었습니다.")
        print(f"📈 처리된 데이터: {len(sql_values)}/{len(df)} ({len(sql_values)/len(df)*100:.1f}%)")
        print(f"❌ 제외된 데이터: {skipped_count}개")
        
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