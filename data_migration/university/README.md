# university 데이터 마이그레이션

## 1. 가상환경 생성 및 활성화

반드시 아래 명령을 실행하기 전에 해당 디렉토리로 이동하세요:

```sh
cd data_migration/university
python3 -m venv university_env
source university_env/bin/activate
```

## 2. 패키지 설치

```sh
pip install -r requirements.txt
```

## 3. 카카오 로컬 API 키 설정

위도/경도 조회를 위해 카카오 로컬 API 키가 필요합니다:

1. [카카오 개발자 센터](https://developers.kakao.com/)에서 애플리케이션을 생성
2. REST API 키를 발급받기
3. 환경변수로 설정:

```sh
export KAKAO_REST_API_KEY="your_kakao_rest_api_key_here"
```

또는 `.env` 파일을 생성하여 설정:

```sh
echo "KAKAO_REST_API_KEY=your_kakao_rest_api_key_here" > .env
```

## 4. API 테스트 (선택사항)

카카오 로컬 API가 제대로 설정되었는지 테스트:

```sh
python test_kakao_api.py
```

## 5. SQL 생성 스크립트 실행

```sh
python generate_university_sql.py
```

## 6. 기능 설명

### 위도/경도 조회 기능

- 학교 주소(ADDRESS)를 기반으로 카카오 로컬 API를 사용하여 위도/경도를 자동 조회
- API 호출 제한을 고려하여 요청 간 0.1초 딜레이 적용
- 조회 실패 시 (0.0, 0.0)으로 설정
- 성공/실패 통계 출력

### 출력 파일

- `output/school_insert.sql`: SCHOOL 테이블 INSERT SQL 파일
- 위도/경도 정보가 포함된 완전한 데이터

---

- `requirements.txt`에 필요한 패키지가 모두 명시되어 있습니다.
- 가상환경을 사용하면 프로젝트별로 독립적인 패키지 관리를 할 수 있습니다.
- 카카오 로컬 API는 일일 300,000회 호출 제한이 있습니다.
