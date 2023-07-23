#!/bin/bash

cd ./src

# unit test
python -m unittest test/unit_test/db_connect_test.py
python -m unittest test/unit_test/encrypt_test.py
python -m unittest test/unit_test/util_test.py

# api test
python -m pytest test/api_test/auth_test.py
python -m pytest test/api_test/item_test.py

# 테스트가 성공적으로 완료되었는지 확인
if [ $? -eq 0 ]; then
    echo "Test all success."
else
    echo "Test Failed."
fi
