# Egomoyak Backend

Django + DRF 기반의 Egomoyak 백엔드 API 서버입니다. 이메일 인증을 통한 회원가입, JWT 인증 로그인/로그아웃, 소셜 로그인(Google/Kakao), 사용자 탈퇴(소프트 삭제)와 알약 정보 조회/검색 API를 제공합니다.

- Python 3.12+
- Django 5.x, Django REST framework
- Simple JWT
- PostgreSQL


## 목차
- 프로젝트 구조
- 빠른 시작(로컬 개발)
- 환경 변수(.env) 설정
- 실행 방법
- API 개요 및 예시
  - 인증/사용자 API
  - 알약(Pills) API
- 개발 가이드(코드 스타일/테스트)
- 배포 힌트


## 프로젝트 구조
루트 일부만 발췌
- config: 장고 설정(base/dev/prod), URL
- apps/users: 사용자 모델/시리얼라이저/서비스/뷰(회원가입, 로그인, 이메일 인증, 로그아웃, 탈퇴, 소셜 로그인, 토큰 리프레시)
- apps/pills: PillItem 모델과 리스트/상세/검색 API
- manage.py: 개발/운영 실행 헬퍼(run_dev, run_prod) 포함
- pyproject.toml: Poetry 의존성


## 빠른 시작(로컬 개발)
사전 요구사항
- Python 3.12+
- PostgreSQL (DB/유저 생성 권한)
- Poetry (권장)

설치
1) 의존성 설치
- Poetry 사용 시:
  - poetry install
- pip 사용 시(선택):
  - pip install -r requirements.txt (동봉돼 있지 않으므로 권장은 Poetry)

2) DB 준비(PostgreSQL)
- DB 생성 및 접근 정보 준비(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

3) 환경 파일 생성
- 루트에 .env.dev 생성(아래 샘플 참조)

4) 마이그레이션 & 슈퍼유저(선택)
- python manage.py migrate
- python manage.py createsuperuser

5) 서버 실행
- python manage.py runserver  또는  python manage.py run_dev

기본 설정은 개발 환경(config.settings.dev)을 사용합니다.


## 환경 변수(.env) 설정
config/settings/base.py는 ENV_FILE 환경변수를 통해 .env.dev 등 파일을 로드합니다. 기본값은 .env.dev 입니다.

샘플(.env.dev)
- SECRET_KEY=장고_시크릿키
- DEBUG=True

- DB_NAME=egomoyak
- DB_USER=postgres
- DB_PASSWORD=postgres
- DB_HOST=127.0.0.1
- DB_PORT=5432

이메일(개발 기본 콘솔 백엔드 사용)
- 별도 설정 없이 콘솔로 전송 로그가 출력됩니다.
- 실서버에서 SMTP를 사용하려면 base.py 주석 블록의 SMTP 설정을 활성화하고 관련 ENV를 구성하세요.

구글 OAuth
- GOOGLE_CLIENT_ID=...
- GOOGLE_CLIENT_SECRET=...
- GOOGLE_REDIRECT_URI=http://localhost:8000/users/social/google/callback/
- GOOGLE_TOKEN_URL=https://oauth2.googleapis.com/token
- GOOGLE_USERINFO_URL=https://www.googleapis.com/oauth2/v2/userinfo

카카오 OAuth
- KAKAO_CLIENT_ID=...
- KAKAO_CLIENT_SECRET=...
- KAKAO_REDIRECT_URI=http://localhost:8000/users/social/kakao/callback/
- KAKAO_TOKEN_URL=https://kauth.kakao.com/oauth/token
- KAKAO_USERINFO_URL=https://kapi.kakao.com/v2/user/me

기타
- ENV_FILE=.env.dev (manage.py의 run_dev/run_prod에서 설정되며, 기본은 .env.dev)


## 실행 방법
개발 서버
- python manage.py runserver
- 또는 헬퍼: python manage.py run_dev

운영(예시)
- python manage.py run_prod  (DJANGO_SETTINGS_MODULE은 별도 설정을 고려하세요)


## API 개요 및 예시
Base URL: http://localhost:8000

### 인증/사용자
1) 이메일 인증 코드 발송
- POST /users/signup/send/
- Body
  - { "email": "user@example.com" }
- Response
  - { "message": "인증번호가 발송 되었습니다." }

2) 이메일 인증 코드 검증
- POST /users/signup/verify/
- Body
  - { "email": "user@example.com", "auth_code": "a1b2c3" }
- Response
  - { "verified": true }

3) 회원가입
- POST /users/signup/
- Body
  - { "email": "user@example.com", "username": "user@example.com", "password": "Secure1#pass" }
- 비밀번호 정책: 영문/숫자/특수문자 각각 최소 1자 포함, 길이 8~64자
- Response
  - { "email": "user@example.com", "username": "user@example.com", "id": "UUID" }
  - 가입 전 이메일 인증이 완료되어야 합니다.

4) 로그인(JWT)
- POST /users/login/
- Body
  - { "email": "user@example.com", "password": "Secure1#pass" }
- Response
  - { "message": "Login Success", "access": "<JWT_ACCESS>" }
  - refresh_token은 httpOnly 쿠키로 설정됩니다.

5) 토큰 리프레시(SimpleJWT 기본 뷰)
- POST /users/login/token/refresh/
- Body
  - { "refresh": "<JWT_REFRESH>" }
- Response
  - { "access": "<NEW_ACCESS>" }

6) 로그아웃
- POST /users/logout/
- Header
  - Authorization: Bearer <ACCESS>
- Body
  - { "refresh_token": "<JWT_REFRESH>" }
- Response
  - { "message": "Logout successful" }

7) 회원 탈퇴(소프트 삭제)
- DELETE /users/signout/
- Header
  - Authorization: Bearer <ACCESS>
- Response
  - { "회원 탈퇴가 완료되었습니다." }

8) 소셜 로그인
- GET /users/social/google/login/ → auth_url 반환
- GET /users/social/google/callback/?code=...
- GET /users/social/kakao/login/ → auth_url 반환
- GET /users/social/kakao/callback/?code=...
- 콜백 응답 예시
  - { "message": "Google Login Success", "access_token": "<JWT_ACCESS>", "refresh_token": "<JWT_REFRESH>", "email": "user@gmail.com" }

주의
- 소셜 로그인 시 기존 유저가 없으면 생성됩니다.


### 알약(Pills)
공통: 인증 없어도 조회 가능(IsAuthenticatedOrReadOnly)

1) 리스트 페이지네이션
- GET /pills/page/{page}/
- Response 예시
  - { "page": 1, "limit": 20, "total": 123, "pills": [ ... ] }

2) 상세
- GET /pills/{item_seq}/
- Response 예시: PillDetailSerializer 형태

3) 검색 + 페이지네이션
- GET /pills/search/{keyword}/page/{page}/
- Response 예시
  - { "keyword": "감기", "page": 1, "total": 5, "pills": [ ... ] }


## cURL 예시
- 로그인
  - curl -X POST http://localhost:8000/users/login/ -H "Content-Type: application/json" -d '{"email":"user@example.com","password":"Secure1#pass"}'
- 탈퇴
  - curl -X DELETE http://localhost:8000/users/signout/ -H "Authorization: Bearer <ACCESS>"
- 알약 검색
  - curl http://localhost:8000/pills/search/%EA%B0%90%EA%B8%B0/page/1/


## 개발 가이드
- 포매팅: black, flake8 (pyproject.toml dev 그룹)
- 테스트: pytest/pytest-django 사용 가능
  - pytest
- 커밋 전 마이그레이션 상태 확인: python manage.py makemigrations --check


## 배포 힌트
- settings/prod.py 사용 시 DJANGO_SETTINGS_MODULE=config.settings.prod 구성
- ALLOWED_HOSTS, DEBUG, SECRET_KEY, DB, SMTP, OAuth 등 환경 변수 필수 구성
- gunicorn, psycopg2-binary는 prod 그룹 의존성에 포함