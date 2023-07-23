
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
