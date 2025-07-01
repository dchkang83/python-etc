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

## 파일 구조

```
subway/
├── subway_env/          # 가상환경 폴더
├── read_subway_data.py  # 메인 프로그램
├── requirements.txt     # 필요한 라이브러리 목록
└── README.md           # 이 파일
```

## 데이터 정보

- **총 지하철역 수**: 1,087개
- **컬럼 수**: 15개
- **데이터 기준일자**: 2025-04-08
- **포함 정보**: 역번호, 역사명, 노선정보, 위치정보, 연락처 등
