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

if __name__ == "__main__":
    # 메인 실행
    subway_df = read_subway_data()
    
    if subway_df is not None:
        print(f"\n✅ 성공적으로 지하철역 데이터를 읽었습니다!")
        print(f"📊 총 {len(subway_df):,}개의 지하철역 정보가 있습니다.")
    else:
        print("❌ 데이터 읽기에 실패했습니다.") 