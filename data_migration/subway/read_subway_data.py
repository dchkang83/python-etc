import pandas as pd
import os
from pathlib import Path

def read_subway_data():
    """
    지하철 엑셀 파일을 읽어서 pandas DataFrame에 담고 총 개수를 출력하는 함수
    """
    # 파일 경로 설정
    file_path = "/Users/deokjoonkang/dev/projects/gundam/claude/subway/전체_도시철도역사정보_20250417.xlsx"
    
    try:
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            print(f"파일을 찾을 수 없습니다: {file_path}")
            return None
        
        # 엑셀 파일 읽기
        print("엑셀 파일을 읽는 중...")
        df = pd.read_excel(file_path)
        
        # 데이터 정보 출력
        print(f"\n=== 지하철역 데이터 정보 ===")
        print(f"총 행 개수: {len(df):,}개")
        print(f"총 열 개수: {len(df.columns)}개")
        print(f"데이터 형태: {df.shape}")
        
        # 컬럼 정보 출력
        print(f"\n=== 컬럼 정보 ===")
        for i, col in enumerate(df.columns, 1):
            print(f"{i}. {col}")
        
        # 처음 5행 미리보기
        print(f"\n=== 처음 5행 미리보기 ===")
        print(df.head())
        
        return df
        
    except Exception as e:
        print(f"파일 읽기 중 오류가 발생했습니다: {str(e)}")
        return None

def get_subway_lines_dict():
    """
    지하철 엑셀 파일을 읽어서 노선번호별 노선명을 딕셔너리로 반환하는 함수
    """
    # 파일 경로 설정
    file_path = "/Users/deokjoonkang/dev/projects/gundam/claude/subway/전체_도시철도역사정보_20250417.xlsx"
    
    try:
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            print(f"파일을 찾을 수 없습니다: {file_path}")
            return None
        
        # 엑셀 파일 읽기
        print("지하철 노선 정보를 읽는 중...")
        df = pd.read_excel(file_path)
        
        # 노선번호와 노선명 컬럼 찾기
        line_number_col = None
        line_name_col = None
        
        # 컬럼명에서 노선번호와 노선명을 찾기
        for col in df.columns:
            if col == '노선번호':
                line_number_col = col
            elif col == '노선명':
                line_name_col = col
        
        if line_number_col is None or line_name_col is None:
            print("노선번호 또는 노선명 컬럼을 찾을 수 없습니다.")
            print("사용 가능한 컬럼:")
            for i, col in enumerate(df.columns, 1):
                print(f"{i}. {col}")
            return None
        
        print(f"노선번호 컬럼: {line_number_col}")
        print(f"노선명 컬럼: {line_name_col}")
        
        # 노선번호와 노선명으로 중복 제거하여 딕셔너리 생성
        lines_dict = {}
        
        # NaN 값 제거하고 중복 제거
        clean_df = df[[line_number_col, line_name_col]].dropna()
        unique_lines = clean_df.drop_duplicates()
        
        for _, row in unique_lines.iterrows():
            line_number = str(row[line_number_col]).strip()
            line_name = str(row[line_name_col]).strip()
            
            if line_number and line_name and line_number != 'nan' and line_name != 'nan':
                lines_dict[line_number] = line_name
        
        print(f"\n=== 노선번호별 노선명 딕셔너리 ===")
        print(f"총 {len(lines_dict)}개의 노선이 있습니다.")
        for line_number, line_name in sorted(lines_dict.items()):
            print(f"{line_number}: {line_name}")
        
        return lines_dict
        
    except Exception as e:
        print(f"노선 정보 추출 중 오류가 발생했습니다: {str(e)}")
        return None

def get_subway_lines():
    """
    프로그램에서 사용하기 위한 간단한 함수
    노선번호별 노선명 딕셔너리를 반환합니다.
    """
    return get_subway_lines_dict()

if __name__ == "__main__":
    # 메인 실행
    subway_df = read_subway_data()
    
    if subway_df is not None:
        print(f"\n✅ 성공적으로 지하철역 데이터를 읽었습니다!")
        print(f"📊 총 {len(subway_df):,}개의 지하철역 정보가 있습니다.")
        
        # 노선번호별 노선명 딕셔너리 생성
        print(f"\n" + "="*50)
        lines_dict = get_subway_lines()
        
        if lines_dict:
            print(f"\n✅ 노선번호별 노선명 딕셔너리가 성공적으로 생성되었습니다!")
            print(f"📊 총 {len(lines_dict)}개의 노선 정보가 있습니다.")
        else:
            print("❌ 노선 정보 딕셔너리 생성에 실패했습니다.")
    else:
        print("❌ 데이터 읽기에 실패했습니다.") 