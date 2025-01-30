```markdown
# 📌 Django에서 MySQL 데이터베이스 연결하기

Django 프로젝트에서 MySQL 데이터베이스를 설정하고 연결하는 방법을 단계별로 설명합니다.

---

## 📌 1. MySQL 설치 및 실행 확인

MySQL이 설치되지 않았다면 먼저 설치해야 합니다.  
설치 후 MySQL 서버가 실행 중인지 확인하세요.

```bash
mysql --version
sudo systemctl status mysql  # (Linux, macOS에서 MySQL이 실행 중인지 확인)
```

MySQL 서버가 실행되지 않았다면 다음 명령어로 실행합니다.

```bash
sudo systemctl start mysql  # (Linux, macOS)
```

---

## 📌 2. MySQL 데이터베이스 및 사용자 생성

터미널에서 MySQL에 접속한 후, 사용할 데이터베이스와 사용자를 생성합니다.

```sql
-- MySQL 접속
mysql -u root -p  # (비밀번호 입력)



-- 데이터베이스 생성(처음 한번만 하면 됨)
CREATE DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 새로운 사용자 생성 및 권한 부여
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON mydb.* TO 'myuser'@'localhost';
FLUSH PRIVILEGES;

-- 종료
EXIT;
```

---

## 📌 3. 패키지 설치

pip install -r requirements.txt


## 📌 4. Django 데이터베이스 마이그레이션

설정이 완료되면 데이터베이스를 초기화합니다.

```bash
# 마이그레이션 파일 생성
python manage.py makemigrations

# 데이터베이스에 적용
python manage.py migrate
```

⚠️ 만약 `django.db.utils.OperationalError: (2002, "Can't connect to MySQL server")` 오류가 발생하면 MySQL이 실행 중인지 확인하세요.

---

## 📌 5. MySQL DB 연결 테스트

Django에서 MySQL이 정상적으로 연결되었는지 확인합니다.

```bash
python manage.py dbshell
```

또는, Django 쉘에서 직접 데이터베이스 쿼리를 실행해볼 수도 있습니다.

```bash
python manage.py shell
```

```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SHOW TABLES;")
print(cursor.fetchall())  # 현재 데이터베이스의 테이블 목록 확인
```

---

## ✅ 완료!

이제 Django와 MySQL이 정상적으로 연결되었습니다. 🎉  
이제 모델을 정의하고 ORM을 사용하여 데이터를 저장하고 불러올 수 있습니다!

---


.env 파일을 만들어야 함
# Secret key for Django
SECRET_KEY=(django 시크릿 키)

# MySQL Database
DB_NAME=(사용할 db 이름)

DB_USER=(유저 이름)

DB_PASSWORD=(유저 비밀번호)

DB_HOST=localhost

DB_PORT=3306

# Naver API Keys
NAVER_CLIENT_ID=(네이버 앱 id)

NAVER_CLIENT_SECRET= (네이버 앱 secret)

NAVER_REDIRECT_URI=http://127.0.0.1:8000/naver/callback/


---
GOOGLE_CLIENT_ID=(구글 프로젝트 id)

GOOGLE_CLIENT_SECRET=(구글 프로젝트 secret)

GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/google/callback/


---
EMAIL_HOST_USER=(본인 google_email)

EMAIL_HOST_PASSWORD=(본인 앱 비밀번호)
>>>>>>> a9f5eca401704ba3699938789a58d0770892dc1a
