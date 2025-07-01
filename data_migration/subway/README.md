# 지하철역 데이터 분석 프로그램

## 가상환경 설정 및 사용법

### 1. 가상환경 생성 (이미 완료됨)

```bash
python3 -m venv subway_env
```

### 2. 가상환경 활성화

```bash
source subway_env/bin/activate
```

활성화되면 프롬프트 앞에 `(subway_env)`가 표시됩니다.

### 3. 필요한 라이브러리 설치 (이미 완료됨)

```bash
pip install -r requirements.txt
```

### 4. 프로그램 실행

```bash
python read_subway_data.py
```

### 5. 가상환경 비활성화

```bash
deactivate
```

## 프로그램 기능

- 엑셀 파일에서 지하철역 데이터 읽기
- 총 지하철역 개수 출력 (1,087개)
- 데이터 형태 및 컬럼 정보 표시
- 처음 5행 미리보기
- **노선번호별 노선명 딕셔너리 생성** (46개 노선)
- **SUBWAY 테이블 INSERT SQL 생성** (1,081개 데이터)

## 파일 구조

```
subway/
├── subway_env/          # 가상환경 폴더
├── read_subway_data.py  # 메인 프로그램
├── test_subway_lines.py # 노선 딕셔너리 사용 예시
├── generate_subway_sql.py # SUBWAY 테이블 INSERT SQL 생성
├── subway_line_mapping.py # 노선번호 코드별 매핑 정보
├── subway_insert.sql    # 생성된 INSERT SQL 파일
├── requirements.txt     # 필요한 라이브러리 목록
└── README.md           # 이 파일
```

## 데이터 정보

- **총 지하철역 수**: 1,087개
- **컬럼 수**: 15개
- **데이터 기준일자**: 2025-04-08
- **포함 정보**: 역번호, 역사명, 노선정보, 위치정보, 연락처 등

## 노선 딕셔너리 사용법

### 기본 사용법

```python
from read_subway_data import get_subway_lines

# 노선번호별 노선명 딕셔너리 가져오기
subway_lines = get_subway_lines()

# 특정 노선번호의 노선명 찾기
line_name = subway_lines['I1101']  # '경인선'
line_name = subway_lines['S1102']  # '2호선'

# 모든 노선 정보 확인
for line_number, line_name in subway_lines.items():
    print(f"{line_number}: {line_name}")
```

### 사용 예시 실행

```bash
python test_subway_lines.py
```

### 주요 노선 정보

- **I1101**: 경인선
- **S1102**: 2호선
- **I4105**: 분당선
- **I28A1**: 인천국제공항선
- **I11D1**: 신분당선
- **I41K2**: 경춘선

## SUBWAY 테이블 INSERT SQL 생성

### SQL 생성 실행

```bash
python generate_subway_sql.py
```

### 노선 매핑 정보 확인

```bash
python subway_line_mapping.py
```

### 생성된 SQL 파일 정보

- **파일명**: `subway_insert.sql`
- **총 INSERT 문**: 1,081개
- **처리된 데이터**: 1,081/1,087 (99.4%)
- **제외된 데이터**: 위도/경도 정보가 없는 6개 역

### 테이블 매핑 정보

| 엑셀 컬럼 | SUBWAY 테이블 컬럼 | 설명                    |
| --------- | ------------------ | ----------------------- |
| 역번호    | PLACE_CODE         | 지하철역 고유 번호      |
| 역사명    | FULL_NAME, NAME    | 지하철역 전체명 및 이름 |
| 노선번호  | LINE_CODE          | 노선 코드               |
| 노선명    | LINE               | 노선 전체명             |
| -         | LINE_SHORT         | 노선 단축명 (자동 생성) |
| 역위도    | LATITUDE           | 위도                    |
| 역경도    | LONGITUDE          | 경도                    |
| -         | USE_YN             | 사용 여부 (기본값: 'Y') |
| -         | REG_DT             | 등록 일시 (NOW())       |

### 노선 매핑 방식

- **엑셀 노선번호 코드**를 키로 사용하여 매핑된 노선명 적용
- **46개 노선번호 코드**에 대한 표준화된 노선명 사용
- **노선 단축명**도 코드별로 미리 정의된 값 사용

### 주요 노선 매핑 예시

| 노선번호 코드 | 노선명         | 노선 단축명 |
| ------------- | -------------- | ----------- |
| I1101         | 경인선         | 경인선      |
| I1103         | 3호선          | 3호선       |
| I11D1         | 신분당선       | 신분당선    |
| I28A1         | 인천국제공항선 | 공항선      |
| I4105         | 분당선         | 분당선      |
| S1102         | 2호선          | 2호선       |
