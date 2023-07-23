## Cafe operation Service

### 참고사항
- 개발 과정에서 고려한 사항은 git issues 확인부탁드립니다. [이슈](https://github.com/robert-min/cafe_operation/issues)
- 서비스 테스트 방법은 README.md 아래 서비스 테스트 방법 확인부탁드립니다.

<br>

### File Tree

```
./
├── Dockerfile                      - backend Dockerfile
├── README.md                       - README
├── app.py                          - run server file
├── conf/
│   └── conf.json                   - sql conf file
├── entrypoint.sh                   - Docker entrypoint
├── requirements.txt                - requirements file
├── src/
│   ├── README.md                   - SQL DDL
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py             - api init file
│   │   ├── auth.py                 - auth api file
│   │   └── item.py                 - item api file
│   ├── lib/
│   │   ├── __init__.py             - api init file
│   │   ├── db_connect.py           - db connection module file
│   │   ├── encrypt.py              - password encryption module file
│   │   ├── model.py                - db ORM model file
│   │   ├── util.py                 - utils module file
│   │   └── validator.py            - API validation module file
│   └── test/
│       ├── __init__.py
│       ├── api_test/
│       │   ├── __init__.py
│       │   ├── auth_test.py        - auth api test file
│       │   └── item_test.py        - item api test file
│       └── unit_test/
│           ├── __init__.py
│           ├── db_connect_test.py  - db connection test code file
│           ├── encrypt_test.py     - encryption test code file
│           └── util_test.py        - util test code file
└── test.sh                         - run test script
```

<br>

### 서비스 테스트 방법

#### 1. Docker 컨테이너 실행
- 서버에 Docker 설치 및 실행이 되어 있어야 합니다.
- docker hub에서 아래 이미지를 바로 `pull`한 후 실행할 수 있습니다.
```sh
 
sudo docker run -d -p 8000:8000 --name cafe_op robertmin/cafe_opreation_backend:0.0.0

```

#### 2. 컨테이너 접속 후 테스트 진행
- 테스트 스크립트로 전체 테스트 진행
```sh
 
# 위의 docker 컨테이너 실행 확인 후 컨테이너 접속
sudo docker exec -it cafe_op bash

# 현재 경로에 test.sh 파일 확인
./test.sh

```
- 수동으로 실행
```sh
 
# 위의 docker 컨테이너 실행 확인 후 컨테이너 접속
sudo docker exec -it cafe_op bash

# src 폴더로 이동
cd src

# test 코드 실행
# unit test
python -m unittest test/unit_test/db_connect_test.py
python -m unittest test/unit_test/encrypt_test.py
python -m unittest test/unit_test/util_test.py

# api test
python -m pytest test/api_test/auth_test.py
python -m pytest test/api_test/item_test.py

```
