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

## 파일 구조

```
subway/
├── subway_env/          # 가상환경 폴더
├── read_subway_data.py  # 메인 프로그램
├── test_subway_lines.py # 노선 딕셔너리 사용 예시
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
