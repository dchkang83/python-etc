import pandas as pd
import os
from datetime import datetime

# 파일 경로
file_path1 = "/Users/deokjoonkang/dev/projects/gundam/python/python-etc/data_migration/university/data/24년 하반기 대학 학교별 재적 재학 휴학 외국인유학생 교원_250109H.xlsx"
file_path2 = "/Users/deokjoonkang/dev/projects/gundam/python/python-etc/data_migration/university/data/학교개황(20250507 기준).xls"

# SCHOOL 테이블 컬럼명
SCHOOL_COLUMNS = [
    'TYPE', 'SIDO', 'NAME', 'CAMPUS', 'STATUS', 'OWNER',
    'POSTAL_CD', 'ADDRESS', 'TEL_NO', 'FAX_NO', 'URL', 'LATITUDE', 'LONGITUDE'
]

def clean_str(val):
    if pd.isna(val):
        return ''
    return str(val).replace("'", "''").strip()

def extract_from_first_file():
    df = pd.read_excel(file_path1, header=11)
    # 컬럼명을 모두 문자열로 변환 후 strip
    df.columns = [str(c).strip() for c in df.columns]
    print("실제 컬럼명:", list(df.columns))  # 디버깅용
    col_map = {
        '학제': 'TYPE',
        '시도': 'SIDO',
        '학교명': 'NAME',
        '본분교': 'CAMPUS',
        '학교상태': 'STATUS',
        '설립': 'OWNER',
        '우편번호': 'POSTAL_CD',
        '주소': 'ADDRESS',
        '전화번호': 'TEL_NO',
        '팩스번호': 'FAX_NO',
        '홈페이지': 'URL',
    }
    use_cols = [c for c in col_map if c in df.columns]
    df = df[use_cols].rename(columns={k: v for k, v in col_map.items() if k in use_cols})
    for col in SCHOOL_COLUMNS:
        if col not in df.columns:
            df[col] = '' if col not in ['LATITUDE', 'LONGITUDE'] else 0.0
    df['LATITUDE'] = 0.0
    df['LONGITUDE'] = 0.0
    df = df.drop_duplicates(subset=['NAME', 'CAMPUS'])
    return df[SCHOOL_COLUMNS]

def extract_from_second_file():
    df = pd.read_excel(file_path2, header=0)
    # 컬럼명 매핑 (캡처 참고, 실제 컬럼명에 맞게 조정)
    col_map = {
        '학제': 'TYPE',
        '시도': 'SIDO',
        '학교명': 'NAME',
        '본분교': 'CAMPUS',
        '학교상태': 'STATUS',
        '설립': 'OWNER',
        '우편번호': 'POSTAL_CD',
        '주소': 'ADDRESS',
        '전화번호': 'TEL_NO',
        '팩스번호': 'FAX_NO',
        '홈페이지': 'URL',
    }
    df = df[[c for c in col_map if c in df.columns]].rename(columns=col_map)
    for col in SCHOOL_COLUMNS:
        if col not in df.columns:
            df[col] = '' if col not in ['LATITUDE', 'LONGITUDE'] else 0.0
    df['LATITUDE'] = 0.0
    df['LONGITUDE'] = 0.0
    df = df.drop_duplicates(subset=['NAME', 'CAMPUS'])
    return df[SCHOOL_COLUMNS]

def merge_and_dedup(df1, df2):
    # 첫 번째 파일에 없는 (학교명+캠퍼스)만 두 번째 파일에서 추가
    merged = pd.concat([df1, df2], ignore_index=True)
    merged = merged.drop_duplicates(subset=['NAME', 'CAMPUS'], keep='first')
    return merged

def generate_school_insert_sql():
    df1 = extract_from_first_file()
    df2 = extract_from_second_file()
    df = merge_and_dedup(df1, df2)
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
