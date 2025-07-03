import pandas as pd
import os
from datetime import datetime
import requests
import time
import json
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 파일 경로
file_path1 = "/Users/deokjoonkang/dev/projects/gundam/python/python-etc/data_migration/university/data/24년 하반기 대학 학교별 재적 재학 휴학 외국인유학생 교원_250109H.xlsx"
file_path2 = "/Users/deokjoonkang/dev/projects/gundam/python/python-etc/data_migration/university/data/학교개황(20250507 기준).xls"

# SCHOOL 테이블 컬럼명
SCHOOL_COLUMNS = [
    'TYPE', 'SIDO', 'NAME', 'CAMPUS', 'STATUS', 'OWNER',
    'POSTAL_CD', 'ADDRESS', 'TEL_NO', 'FAX_NO', 'URL', 'LATITUDE', 'LONGITUDE'
]

# 카카오 로컬 API 설정
KAKAO_API_KEY = os.getenv('KAKAO_REST_API_KEY', '')
KAKAO_LOCAL_API_URL = "https://dapi.kakao.com/v2/local/search/address.json"

# 주소별 좌표 캐시 (중복 API 호출 방지)
address_coordinates_cache = {}

def get_coordinates_from_address(address):
    """
    카카오 로컬 API를 사용하여 주소로부터 위도, 경도를 조회합니다.
    중복 호출을 방지하기 위해 캐시를 사용합니다.
    
    Args:
        address (str): 조회할 주소
        
    Returns:
        tuple: (latitude, longitude) 또는 (0.0, 0.0) if 실패
    """
    if not KAKAO_API_KEY:
        print("⚠️  카카오 REST API 키가 설정되지 않았습니다. 환경변수 KAKAO_REST_API_KEY를 설정해주세요.")
        return 0.0, 0.0
    
    if not address or address.strip() == '':
        return 0.0, 0.0
    
    # 캐시에서 확인
    clean_address = address.strip()
    if clean_address in address_coordinates_cache:
        lat, lng = address_coordinates_cache[clean_address]
        print(f"📋 캐시에서 조회: '{clean_address}' -> 좌표: ({lat}, {lng})")
        return lat, lng
    
    try:
        headers = {
            'Authorization': f'KakaoAK {KAKAO_API_KEY}'
        }
        
        params = {
            'query': clean_address
        }
        
        response = requests.get(KAKAO_LOCAL_API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['documents']:
            # 첫 번째 결과 사용
            first_result = data['documents'][0]
            latitude = float(first_result['y'])
            longitude = float(first_result['x'])
            print(f"📍 주소 '{clean_address}' -> 좌표: ({latitude}, {longitude})")
            
            # 캐시에 저장
            address_coordinates_cache[clean_address] = (latitude, longitude)
            return latitude, longitude
        else:
            print(f"❌ 주소 '{clean_address}'에 대한 좌표를 찾을 수 없습니다.")
            address_coordinates_cache[clean_address] = (0.0, 0.0)
            return 0.0, 0.0
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API 호출 중 오류 발생 (주소: {clean_address}): {str(e)}")
        address_coordinates_cache[clean_address] = (0.0, 0.0)
        return 0.0, 0.0
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"❌ API 응답 파싱 중 오류 발생 (주소: {clean_address}): {str(e)}")
        address_coordinates_cache[clean_address] = (0.0, 0.0)
        return 0.0, 0.0

def update_coordinates_for_dataframe(df):
    """
    DataFrame의 ADDRESS 컬럼을 사용하여 위도, 경도를 업데이트합니다.
    
    Args:
        df (DataFrame): 업데이트할 DataFrame
        
    Returns:
        DataFrame: 위도, 경도가 업데이트된 DataFrame
    """
    print(f"\n🗺️  총 {len(df)}개 학교의 주소에서 좌표를 조회합니다...")
    
    success_count = 0
    fail_count = 0
    cache_hit_count = 0
    
    for idx, row in df.iterrows():
        address = row['ADDRESS']
        if address and str(address).strip():
            clean_address = str(address).strip()
            
            # 캐시 히트 여부 확인
            is_cache_hit = clean_address in address_coordinates_cache
            
            latitude, longitude = get_coordinates_from_address(address)
            df.at[idx, 'LATITUDE'] = latitude
            df.at[idx, 'LONGITUDE'] = longitude
            
            if latitude != 0.0 or longitude != 0.0:
                success_count += 1
            else:
                fail_count += 1
                
            if is_cache_hit:
                cache_hit_count += 1
            
            # API 호출 제한을 위한 딜레이 (캐시 히트가 아닌 경우에만)
            if not is_cache_hit:
                time.sleep(0.1)
        else:
            print(f"⚠️  인덱스 {idx}: 주소가 비어있습니다.")
            fail_count += 1
    
    print(f"\n✅ 좌표 조회 완료:")
    print(f"   - 성공: {success_count}개")
    print(f"   - 실패: {fail_count}개")
    print(f"   - 캐시 히트: {cache_hit_count}개")
    print(f"   - 실제 API 호출: {len(address_coordinates_cache)}개")
    
    return df

def clean_str(val):
    """다양한 데이터 타입을 안전하게 문자열로 변환합니다."""
    if pd.isna(val):
        return ''
    if val is None:
        return ''
    if isinstance(val, (int, float)):
        return str(val).strip()
    return str(val).replace("'", "''").strip()

def clean_campus(val):
    """CAMPUS 필드 값을 변환하는 함수"""
    if pd.isna(val):
        return ''
    
    val_str = str(val).strip()
    
    # 본교(제1캠퍼스) -> 본교
    if val_str == '본교(제1캠퍼스)':
        return '본교'
    
    # 본교(제2캠퍼스), 본교(제3캠퍼스) 등 -> 괄호 안의 텍스트
    if val_str.startswith('본교(') and val_str.endswith(')'):
        return val_str[3:-1]  # '본교(' 제거하고 ')' 제거
    
    return val_str

def extract_from_first_file():
    # 첫 번째 파일은 11번째 행(인덱스 10)이 실제 헤더
    df = pd.read_excel(file_path1, header=10)
    # 컬럼명을 모두 문자열로 변환 후 strip
    df.columns = [str(c).strip() for c in df.columns]
    print("첫 번째 파일 실제 컬럼명:", list(df.columns))  # 디버깅용
    
    # 첫 번째 파일의 실제 컬럼명에 맞게 매핑
    col_map = {
        '학제': 'TYPE',
        '시도': 'SIDO',
        '학교명': 'NAME',
        # '대학원 구분\n(부설/\n대학원대학)': 'CAMPUS',  # 본분교 정보
        '본분교': 'CAMPUS',  # 본분교 정보
        '학교상태': 'STATUS',
        '설립': 'OWNER',
        '우편번호': 'POSTAL_CD',
        '주소': 'ADDRESS',
        '전화번호': 'TEL_NO',
        '팩스번호': 'FAX_NO',
        '홈페이지': 'URL',
    }
    
    # 실제 데이터 구조를 파악하기 위해 첫 몇 행 출력
    print("첫 번째 파일 첫 3행 데이터:")
    print(df.head(3))
    
    # 컬럼이 존재하는지 확인하고 매핑
    use_cols = [c for c in col_map if c in df.columns]
    if use_cols:
        df = df[use_cols].rename(columns={k: v for k, v in col_map.items() if k in use_cols})
    
    # 누락된 컬럼 추가
    for col in SCHOOL_COLUMNS:
        if col not in df.columns:
            df[col] = '' if col not in ['LATITUDE', 'LONGITUDE'] else 0.0
    
    df['LATITUDE'] = 0.0
    df['LONGITUDE'] = 0.0
    # CAMPUS 필드 정리
    df['CAMPUS'] = df['CAMPUS'].apply(clean_campus)
    df = df.drop_duplicates(subset=['SIDO', 'NAME', 'CAMPUS'])
    
    # 위도, 경도 조회
    df = update_coordinates_for_dataframe(df)
    
    return df[SCHOOL_COLUMNS]

def extract_from_second_file():
    df = pd.read_excel(file_path2, header=0)
    print("두 번째 파일 실제 컬럼명:", list(df.columns))  # 디버깅용
    
    # 두 번째 파일의 실제 컬럼명에 맞게 매핑
    col_map = {
        '학제': 'TYPE',
        '지역': 'SIDO',
        '학교명': 'NAME',
        '본분교': 'CAMPUS',
        '학교상태': 'STATUS',
        '설립구분': 'OWNER',
        '우편번호': 'POSTAL_CD',
        '주소': 'ADDRESS',
        '학교대표\r\n번호': 'TEL_NO',
        '학교대표\r\n팩스번호': 'FAX_NO',
        '학교홈페이지': 'URL',
    }
    
    # 실제 데이터 구조를 파악하기 위해 첫 몇 행 출력
    print("두 번째 파일 첫 3행 데이터:")
    print(df.head(3))
    
    # 컬럼이 존재하는지 확인하고 매핑
    use_cols = [c for c in col_map if c in df.columns]
    if use_cols:
        df = df[use_cols].rename(columns={k: v for k, v in col_map.items() if k in use_cols})
    
    # 누락된 컬럼 추가
    for col in SCHOOL_COLUMNS:
        if col not in df.columns:
            df[col] = '' if col not in ['LATITUDE', 'LONGITUDE'] else 0.0
    
    df['LATITUDE'] = 0.0
    df['LONGITUDE'] = 0.0
    # CAMPUS 필드 정리
    df['CAMPUS'] = df['CAMPUS'].apply(clean_campus)
    df = df.drop_duplicates(subset=['SIDO', 'NAME', 'CAMPUS'])
    
    # 위도, 경도 조회
    df = update_coordinates_for_dataframe(df)
    
    return df[SCHOOL_COLUMNS]

def merge_and_dedup(df1, df2):
    """
    두 DataFrame을 병합하고 중복을 제거합니다.
    첫 번째 파일을 우선하되, 위도/경도가 없으면 두 번째 파일에서 보완합니다.
    
    Args:
        df1 (DataFrame): 첫 번째 파일 데이터 (우선)
        df2 (DataFrame): 두 번째 파일 데이터 (보완용)
        
    Returns:
        DataFrame: 병합된 데이터
    """
    print(f"\n🔄 데이터 병합 및 중복 제거 시작...")
    print(f"   - 첫 번째 파일: {len(df1)}개")
    print(f"   - 두 번째 파일: {len(df2)}개")
    
    # 첫 번째 파일을 기준으로 병합
    merged = df1.copy()
    
    # 두 번째 파일에서 보완할 데이터 찾기
    supplement_count = 0
    
    for idx1, row1 in merged.iterrows():
        # 위도/경도가 없는 경우에만 보완 시도
        if (row1['LATITUDE'] == 0.0 and row1['LONGITUDE'] == 0.0) or \
           (pd.isna(row1['LATITUDE']) and pd.isna(row1['LONGITUDE'])):
            
            # 두 번째 파일에서 동일한 학교 찾기
            matching_rows = df2[
                (df2['SIDO'] == row1['SIDO']) & 
                (df2['NAME'] == row1['NAME']) & 
                (df2['CAMPUS'] == row1['CAMPUS'])
            ]
            
            if not matching_rows.empty:
                row2 = matching_rows.iloc[0]
                
                # 두 번째 파일에 위도/경도가 있으면 보완
                if (row2['LATITUDE'] != 0.0 or row2['LONGITUDE'] != 0.0) and \
                   (not pd.isna(row2['LATITUDE']) and not pd.isna(row2['LONGITUDE'])):
                    
                    print(f"   🔄 보완: {row1['NAME']} ({row1['CAMPUS']}) - 위도/경도 추가")
                    
                    # 위도/경도 보완
                    merged.at[idx1, 'LATITUDE'] = row2['LATITUDE']
                    merged.at[idx1, 'LONGITUDE'] = row2['LONGITUDE']
                    
                    # 주소와 우편번호도 보완 (첫 번째 파일에 없거나 비어있는 경우)
                    if not row1['ADDRESS'] or str(row1['ADDRESS']).strip() == '':
                        merged.at[idx1, 'ADDRESS'] = row2['ADDRESS']
                        print(f"      📍 주소도 보완: {row2['ADDRESS']}")
                    
                    if not row1['POSTAL_CD'] or str(row1['POSTAL_CD']).strip() == '':
                        merged.at[idx1, 'POSTAL_CD'] = row2['POSTAL_CD']
                        print(f"      📮 우편번호도 보완: {row2['POSTAL_CD']}")
                    
                    supplement_count += 1
    
    # 두 번째 파일에서 첫 번째 파일에 없는 학교 추가
    for idx2, row2 in df2.iterrows():
        # 첫 번째 파일에 없는 학교인지 확인
        existing = merged[
            (merged['SIDO'] == row2['SIDO']) & 
            (merged['NAME'] == row2['NAME']) & 
            (merged['CAMPUS'] == row2['CAMPUS'])
        ]
        
        if existing.empty:
            merged = pd.concat([merged, pd.DataFrame([row2])], ignore_index=True)
            print(f"   ➕ 추가: {row2['NAME']} ({row2['CAMPUS']}) - 두 번째 파일에서")
    
    print(f"\n✅ 데이터 병합 완료:")
    print(f"   - 최종 데이터: {len(merged)}개")
    print(f"   - 위도/경도 보완: {supplement_count}개")
    
    return merged

def generate_school_insert_sql():
    df1 = extract_from_first_file()
    df2 = extract_from_second_file()
    df = merge_and_dedup(df1, df2)
    
    # 캐시 통계 출력
    print(f"\n📊 API 호출 통계:")
    print(f"   - 고유 주소 수: {len(address_coordinates_cache)}개")
    print(f"   - 캐시된 좌표 수: {len([v for v in address_coordinates_cache.values() if v != (0.0, 0.0)])}개")
    print(f"   - 실패한 주소 수: {len([v for v in address_coordinates_cache.values() if v == (0.0, 0.0)])}개")
    
    output_file = "/Users/deokjoonkang/dev/projects/gundam/python/python-etc/data_migration/university/output/school_insert.sql"
    # 디렉토리 없으면 생성
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- SCHOOL 테이블 INSERT SQL\n")
        f.write(f"-- 생성일시: {current_time}\n")
        f.write(f"-- 총 {len(df)}개 학교 데이터\n\n")
        f.write("INSERT INTO SCHOOL (TYPE, SIDO, NAME, CAMPUS, STATUS, OWNER, POSTAL_CD, ADDRESS, TEL_NO, FAX_NO, URL, LATITUDE, LONGITUDE) VALUES\n")
        sql_values = []
        for _, row in df.iterrows():
            values = [
                f"'{clean_str(row['TYPE'])}'",
                f"'{clean_str(row['SIDO'])}'",
                f"'{clean_str(row['NAME'])}'",
                f"'{clean_str(row['CAMPUS'])}'",
                f"'{clean_str(row['STATUS'])}'",
                f"'{clean_str(row['OWNER'])}'",
                f"'{clean_str(row['POSTAL_CD'])}'",
                f"'{clean_str(row['ADDRESS'])}'",
                f"'{clean_str(row['TEL_NO'])}'",
                f"'{clean_str(row['FAX_NO'])}'",
                f"'{clean_str(row['URL'])}'",
                f"{row['LATITUDE']}",
                f"{row['LONGITUDE']}"
            ]
            sql_values.append(f"({', '.join(values)})")
        for i, sql_value in enumerate(sql_values):
            if i == len(sql_values) - 1:
                f.write(sql_value + ";\n")
            else:
                f.write(sql_value + ",\n")
        f.write(f"\n-- 총 {len(sql_values)}개의 INSERT 문이 생성되었습니다.\n")
        f.write(f"-- 생성 완료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"\n✅ SQL 파일이 성공적으로 생성되었습니다!")
    print(f"📁 파일명: {output_file}")
    print(f"📊 총 {len(sql_values)}개의 INSERT 문이 생성되었습니다.")
    return output_file

def preview_sql_file(filename, lines=10):
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
    sql_file = generate_school_insert_sql()
    if sql_file:
        preview_sql_file(sql_file, 15)
        print(f"\n🎉 SCHOOL 테이블 INSERT SQL 생성이 완료되었습니다!")
        print(f"💡 생성된 파일을 데이터베이스에서 실행하세요.")
    else:
        print("❌ SQL 파일 생성에 실패했습니다.")
