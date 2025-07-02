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

## 3. SQL 생성 스크립트 실행

```sh
python generate_university_sql.py
```

---

- `requirements.txt`에 필요한 패키지가 모두 명시되어 있습니다.
- 가상환경을 사용하면 프로젝트별로 독립적인 패키지 관리를 할 수 있습니다.
