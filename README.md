# **🏃‍➡️ 걸음걸이**

**🏆 피로그래밍 22기 최종 프로젝트 작품**

<img width="1694" alt="Image" src="https://github.com/user-attachments/assets/b32fea6b-e243-47f2-babb-a9a0b9b50a4f" />

## **📜 Contents**

1. [Overview](#-Overview)
2. [서비스 화면](#-서비스-화면)
3. [주요 기능](#-주요-기능)
4. [기획 및 설계 산출물](#-기획-및-설계-산출물)
5. [개발 환경](#-개발-환경)
6. [팀 소개](#-팀-소개)

# **👣 Overview**

**🏆 개발 기간: 25.01.27 ~ 25.02.18**

> *멈추지 않을 당신의 걸음을 위한 맞춤형 서비스*
> 

‘걷기’라는 행위에 대한 우리의 관심은 꾸준히 커지고 있지요. 고강도의 러닝부터 가벼운 산책까지, 여러분은 어떤 형태의 걸음을 남기시나요? 그 걸음이 얼마나 모이고 어디서 쌓여갈지, 웹서비스 ‘걸음걸이’와 함께 해요! 데일리 걷기 기록과 월간 관리를 다루는 ‘오늘 걸음’, 걸음코스 추천을 제공하는 ‘어디 걸음’, 러너의 커뮤니티 ‘함께 걸음’과 ‘이달의 걸음왕’ 기능을 통해 나만의 고유한 걸음을 이어가요.

# **👀 서비스 화면**

**홈**

- 로그인 전
    - 어떤 버튼을 누르던 로그인 페이지로 이동
- 로그인 후
    - 걸음 기록 페이지, 함께 걸음, 어디 걸음, 캘린더, 마이 페이지 이동 가능
- ABOUT US
    - 팀 걸음걸이에 대한 정보 제공
<table style="width:100%; text-align:center; vertical-align:middle;">
  <tr>
    <th>랜딩 페이지</th>
    <th>로그인 전</th>
    <th>로그인 후</th>
    <th>ABOUT US</th>
  </tr>
  <tr>
    <td><img width="300" alt="Image" src="https://github.com/user-attachments/assets/cced419e-791a-424b-acae-e1430b091a0c"></td>
    <td><img width="300" alt="Image" src="https://github.com/user-attachments/assets/3c60c8ed-f209-4822-b9ca-d89525ae8915" /></td>
    <td><img width="300" alt="Image" src="https://github.com/user-attachments/assets/04069206-60a9-4bcc-8f08-883edeecdd5e" /></td>
    <td><img width="300" alt="Image" src="https://github.com/user-attachments/assets/27fedc49-a32b-4cdc-b19c-45b72bb12eca" /></td>
  </tr>
</table>

**회원가입 & 로그인 & 로그아웃**

- `네이버, 구글 소셜 로그인` 및 유저 회원가입/로그인
- 로그인을 하면 기록 측정 페이지로 이동

**마이 걸음**

- 지금까지의 이용 횟수, 거리, 칼로리의 총합
- 로그아웃, 회원탈퇴 기능 지원
<table style="width:100%; text-align:center; vertical-align:middle;">
  <tr>
    <th>로그인 페이지</th>
    <th>유저 회원가입 페이지</th>
    <th>마이걸음 페이지</th>
    <th>유저 프로필 변경</th>
  </tr>
  <tr>
    <td><img width="300" alt="Image" src="https://github.com/user-attachments/assets/912cc31c-c59d-4d6a-92bc-caa787437ecc"></td>
    <td><img width="300" alt="Image" src="https://github.com/user-attachments/assets/e787548f-e7b4-4da4-b9ff-d8e83262bbdd" /></td>
    <td><img src="https://github.com/user-attachments/assets/6797ab01-c639-4486-b8dc-a50ec2f7c3c4" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/7807e396-58b8-4477-ad0c-89875fea8682" width="300" alt="Image"></td>
  </tr>
</table>

**걸음기록 측정**

- 걸음기록 시작을 통해 측정 시작
- 시작 이후 3초 2초 1초 표시가 나온 뒤 시작
- 물병을 누르면 일시 정지
<table style="width:100%; text-align:center; vertical-align:middle;">
  <tr>
    <th>걸음기록 시작</th>
    <th>걸음기록 준비 랜딩 페이지</th>
    <th>걸음기록 측정 및 종료</th>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/51253777-68ca-4601-8681-06d86e689161" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/41ae53ea-45ac-4c4f-952e-9adb4742bc7e" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/4ebf779a-3541-4565-bd4b-d0dff7820707" width="300" alt="Image"></td>
  </tr>
</table>

**걸음 캘린더, 오늘걸음**

**[걸음 캘린더]**
- 월별 총 이동거리, 소모 칼로리 정보 제공
- 날짜별 로고의 투명도 통해 오늘걸음 기록 현황 제공
- 날짜별 오늘걸음 페이지와 연동

**[오늘 걸음]**
- 오늘걸음 페이지에서 기록별 이동거리, 평균 속도, 소모 칼로리, 이동경로 등 세부정도 열람
- 기록별 사진과 코멘트 커스텀 기능 제공
<table style="width:100%; text-align:center; vertical-align:middle;">
  <tr>
    <th>걸음 캘린더 페이지</th>
    <th>오늘걸음 페이지</th>
    <th>이동경로 열람</th>
    <th>기록별 사진, 코멘트 커스텀</th>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/2533b4ed-653c-4d11-afdb-2fb2d93381bd" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/e54488b2-e153-4f3e-a8f4-14259e8b1404" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/45b8f1df-06e8-4756-9531-e9b973433547" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/466aaaff-fbc0-4f59-a0d8-8d6fa0184311" width="300" alt="Image"></td>
  </tr>
</table>

**어디 걸음**

- 어디 걸음 메인페이지에서 추천 코스에 대한 전체 정보 열람
- 검색어 / 키워드 / 지도 기반의 걷기 좋은 장소 검색
- 검색 결과로 제공되는 카드를 클릭해 코스에 대한 세부정보 제공
- 코스 제목, 설명 거리, 시간 등 다양한 정보를 입력하여 나만의 추천 코스 등록
<table style="width:100%; text-align:center; vertical-align:middle;">
  <tr>
    <th>나만의 장소 추천</th>
    <th>장소 추천 시 위치 등록</th>
    <th>어디 걸음 메인 페이지</th>
    <th>코스 디테일 페이지</th>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/993d44a9-d7df-46ec-9b39-130ab362e937" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/67249e99-81ea-48d7-804c-63669018cb3a" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/16ca4c92-e158-4657-9659-cf8845050ce4" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/600bf651-7b7a-4911-9b50-c9dd71f05eb2" width="300" alt="Image"></td>
  </tr>
</table>
<table style="width:100%; text-align:center; vertical-align:middle;">
  <tr>
    <th>키워드 기반 코스 검색</th>
    <th>키워드 기반 검색 결과</th>
    <th>지도 마커 기반 코스 검색</th>
    <th>지도 마커 기반 검색 결과</th>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/5cb91a05-a58b-4e19-bbc2-3956e3805044" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/dfaf73f2-4de5-45e2-b330-e88dd6e71f66" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/315316e0-e039-490c-8e88-53eb2c6d7f62" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/d1bbe633-d626-4cca-bf36-6ff6c73dbff4" width="300" alt="Image"></td>
  </tr>
</table>

**함께 걸음, 이달의 걸음왕** 

**[함께 걸음]**
- 포스트 열람 및 작성을 통해 러닝메이트 모집
- 포스트 세부 페이지에서 댓글 기능으로 유저 간 소통

**[이달의 걸음왕]**
- 걸음기록 측정 페이지를 제외한 모든 페이지에서 접속
- 매월 사용자별 총 이동거리 기준 Top5 랭킹과 나의 순위 제공
<table style="width:100%; text-align:center; vertical-align:middle;">
  <tr>
    <th>함께 걸음 메인 페이지</th>
    <th>함께 걸음 포스트 작성</th>
    <th>함께 걸음 포스트 세부 페이지</th>
    <th>이달의 걸음왕</th>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/7e6e2b83-5121-4efd-b5bc-016c522e6f6f" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/e319e0c1-b4cc-4edc-8e52-1b32694b0af2" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/caf6a383-3daa-4d08-95a6-8f377c96cc92" width="300" alt="Image"></td>
    <td><img src="https://github.com/user-attachments/assets/7863555a-8e6b-4762-b836-f170ae8d8de7" width="300" alt="Image"></td>
  </tr>
</table>

# **👣 주요 기능**

- `🏃‍➡️ 걸음 기록`
    - 걸음 기록을 시작함으로써 시간이 흐르고 사용자의 걷기 데이터가 실시간으로 업데이트된다.
    - 물병 버튼을 클릭하면 중간 정지를 할 수 있다.
    - 기록을 종료하고 해당 걸음기록의 이동 거리, 소모 칼로리, 평균 페이스, 경로를 볼 수 있다.
    - 사용자의 사진과 코멘트로 걸음기록을 커스텀할 수 있다.
- `👥 함께 걸음`
    - 같이 걸을 러닝 메이트를 찾는 커뮤니티 페이지
    - 게시글을 직접 작성하거나 댓글 기능을 활용하여 소통할 수 있다.
- `🗺️ 어디 걸음`
    - 다른 사용자가 추천한 걷기 좋은 장소들을 열람할 수 있다.
    - 키워드, 지도의 좌표 선택, 지역 검색을 통해 추천코스를 구체적으로 검색할 수 있다.
    - 다른 사람에게 자신이 좋아하는 장소를 추천할 수 있다.
- `🗓️ 걸음 캘린더`
    - 지금까지의 걸음 기록을 캘린더 형식으로 관리할 수 있다.
    - 기록이 있는 날은 달력의 로고를 통해 파악할 수 있으며, 날짜별 걸은 거리에 따라 로고가 진해진다.
    - 각 월 별 총 소모 칼로리와 이동 거리를 볼 수 있다.
    - 기록이 있는 날짜를 클릭하면 해당 날짜의 걸음 기록 페이지로 이동한다.
- `📒 마이 걸음`
    - 사용자 정보를 볼 수 있다.
    - 프로필 사진, 닉네임을 변경할 수 있다.
    - 로그아웃과 회원탈퇴 기능을 제공한다.

# **🗂️ 기획 및 설계 산출물**

**📍 요구사항 및 기능 명세**

<img width="1195" alt="Image" src="https://github.com/user-attachments/assets/cb32e8a2-46b4-4262-954c-0e5b0315c096" />

**✂️  Wire Frame**

<img width="1195" alt="Image" src="https://github.com/user-attachments/assets/b4e2f608-6d33-4320-9eb8-8e716e308fdd" />

**✨ ER Diagram**

<img width="1195" alt="Image" src="https://github.com/user-attachments/assets/0c825912-1fdf-48ea-b56e-e0ee2d82e4f6" />

# **👣 개발 환경**
**Requirements.txt**

```
Django==4.2.19          # Python 웹 프레임워크 (서버 개발을 위한 필수 패키지)
mysqlclient==2.2.7     # MySQL 데이터베이스 드라이버 (MySQL과 Django 연동용)
asgiref==3.8.1         # Django의 비동기 지원을 위한 라이브러리 (ASGI 표준 지원)
sqlparse==0.5.3        # Django ORM에서 SQL 구문을 분석하고 처리하는 라이브러리
tzdata==2025.1         # 시간대 데이터베이스 (Django에서 시간대를 다룰 때 사용)
requests==2.32.3       # HTTP 요청 라이브러리 (외부 API와 통신할 때 사용, 선택 사항)
python-decouple==3.8   # .env 파일에서 환경 변수 호출 및 관리
django-allauth==65.3.1 # Django 기반의 소셜 로그인 및 인증 기능 지원 (Google, Naver 등)
six==1.17.0            # Python 2와 3 간의 호환성을 위한 유틸리티 라이브러리
pillow==10.4.0
djangorestframework==3.15.2
```

### 🔧 Backend

- Python `3.12.8`
- Django `4.2.19`
- Django Rest Framework `3.15.2`

### 🔭 Frontend

- lang: HTML5, CSS3, JAVASCRIPT

### 🗂️ DB

- MySQL `8.0.41-0ubuntu0.20.04.1`

### 🖥️ Server

- Ubuntu `20.04.6`)
- Nginx `1.18.0`
- Gunicorn `23.0.0`
- HTTPS (TLS `1.3`)

### 🕹️ IDE

- VSCode

### **🤝 협업 플랫폼**

**🎨** 피그마 / **✍️** 노션 / **🗣️** 디스코드

### **🙌 팀 소개**

<table style="width:100%; text-align:center;">
  <tr>
    <th><a href="https://github.com/NamKyeongMin">남경민</a></th>
    <th><a href="https://github.com/Kimgyuilli">김규일</a></th>
    <th><a href="https://github.com/seonjuuu">김선주</a></th>
    <th><a href="https://github.com/parkgunwook0617">박건욱</a></th>
    <th><a href="https://github.com/leexzu1">이주원</a></th>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/a1c31ad2-2512-4757-ab94-ad4c4de8970c" width="140"></td>
    <td><img src="https://github.com/user-attachments/assets/67c09f56-64f8-47cd-9cc0-e02aaf3a0211" width="140"></td>
    <td><img src="https://github.com/user-attachments/assets/1862cde9-e3fb-423a-b1c1-106f3399bac9" width="140"></td>
    <td><img src="https://github.com/user-attachments/assets/31ea1681-89bb-4efc-92f5-f14858589441" width="140"></td>
    <td><img src="https://github.com/user-attachments/assets/9086bdd3-a225-4f60-a94e-acf06d8f947a" width="140"></td>
  </tr>
  <tr>
    <td style="text-align:center;">PM & Design & FE</td>
    <td style="text-align:center;">BE & CI/CD</td>
    <td style="text-align:center;">FE & BE</td>
    <td style="text-align:center;">FE & BE</td>
    <td style="text-align:center;">FE & BE</td>
  </tr>
</table>

### **😃 팀원 역할**

- 남경민
    - 팀장, 기획, 캐릭터 및 UI/UX 디자인 설계, 걸음기록 페이지, 오늘걸음 페이지
- 김규일
    - ERD 설계, 회원 관리, 걸음캘린더 기능, 마이걸음 기능, NAVER CLOUD 서버 배포 및 CICD 설정
- 김선주
    - record 모델, 이달의 걸음왕, 걸음기록 기능, 오늘걸음 기능, NAVER CLOUD 서버 배포
- 박건욱
    - course 모델, 걸음캘린더 페이지, 어디걸음 메인/지도검색/세부/폼
- 이주원
    - post 모델, 메인홈, 함께 걸음, 어디걸음 키워드 검색 기능, 마이걸음 페이지, AboutUs, 내가 작성한 글 페이지