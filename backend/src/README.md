## DB DDL
- user 계정 정보 테이블
```sql
 
-- 테이블 생성
CREATE TABLE user_auth (
seq BIGINT(11) NOT NULL AUTO_INCREMENT,
phone_number VARCHAR(200) NOT NULL,
password VARCHAR(500) NOT NULL,
timestamp VARCHAR(200) NOT NULL,
PRIMARY KEY(seq)
);

-- 인덱스 생성
CREATE INDEX idx_user_auth ON user_auth (phone_number);

```
- user item 정보 테이블
```sql
 
-- DB 한글 설정
ALTER DATABASE cafe CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
-- 테이블 생성
CREATE TABLE user_item (
seq BIGINT(11) NOT NULL AUTO_INCREMENT,
phone_number VARCHAR(200) NOT NULL,
category VARCHAR(200) NOT NULL,
selling_price BIGINT(11) NOT NULL,
cost_price BIGINT(11) NOT NULL,
name VARCHAR(200) NOT NULL,
description VARCHAR(1000),
barcode VARCHAR(200) NOT NULL,
expiration_date VARCHAR(200) NOT NULL,
size VARCHAR(100) NOT NULL,
search_initial VARCHAR(200) NOT NULL,
PRIMARY KEY(seq)
) CHARSET=utf8mb4;

-- 인덱스 생성
CREATE INDEX idx_user_item ON user_item (seq, phone_number);
CREATE INDEX idx_user_item_name ON user_item (name, search_initial);

```

