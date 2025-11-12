# 🔐 Authentication API Guide

## 1️⃣ 회원가입 (Register)

**URL**  
`POST /users/signup/`

**Request Body**
```json
{
  "email": "user@example.com",
  "username": "user@example.com",
  "password": "securepassword1#"
}
Flow
# 북마크 & 마이페이지 백엔드

의약품 서비스에서 북마크, 마이페이지, 인증(Pill/Users) 기능을 담당하는 백엔드입니다.

## 프로젝트 구조

```
.
├── apps/
│   ├── bookmarks/        # 북마크 API
│   ├── mypage/           # /me 프로필 API
│   ├── pills/            # 의약품 데이터 API (feat/pills-api에서 병합)
│   └── users/            # 회원가입/로그인/소셜 로그인 등 인증
├── config/               # Django 설정 (base/dev/prod)
├── docs/                 # 작업 로그 (로컬 관리)
├── docker-compose.dev.yml
├── manage.py
└── pyproject.toml
```

## 빠른 시작

1. 필요한 앱 활성화 (`config/settings/base.py` 참고)
2. `docker-compose.dev.yml` 혹은 로컬 환경에서 DB 실행
3. 데이터베이스 마이그레이션

```bash
poetry install          # 의존성 설치
poetry run python manage.py migrate
poetry run python manage.py runserver
```

## 주요 API

### 북마크 (`apps/bookmarks`)

이메일 인증 완료 후 signup/으로 회원가입 진행

Response 예시

json
- `GET /bookmark` : 로그인 사용자의 북마크 목록 (20개 페이지네이션)
- `POST /bookmark` : 약품 북마크 추가  
  - 이미 존재하면 `409`
  - 20개 초과 시 `201` with `success: false`
- `DELETE /bookmark` : 북마크 삭제 (body에서 `{"item_seq": "P001"}`)

### 마이페이지 (`apps/mypage`)

- `GET /me` : 현재 로그인한 사용자의 프로필 조회
- `PATCH /me/nickname` : 닉네임 수정 (`{"nickname": "새닉"}`)
- `PATCH /me/password` : 비밀번호 수정 (`{"current_password": "...", "new_password": "..."}`)

### 인증 (`apps/users`)

#### 1️⃣ 회원가입 (Register)
- URL: `POST /users/signup/`
- Request Body:

```json
{
  "email": "user@example.com",
  "username": "user@example.com",
  "password": "securepassword1#"
}
2️⃣ 이메일 인증 (Email Verify)
2-1. 인증 코드 발송
URL POST /users/signup/send/

Request Body

json
```

- Flow: `signup/send/` → 이메일 인증 코드 발송 → `signup/verify/` → 인증 코드 검증 → `signup/`으로 회원가입 완료
- Response 예시:

```json
{
  "email": "user@example.com",
  "username": "user@example.com",
  "id": 1
}
Response 예시

json
{
  "message": "인증번호가 발송 되었습니다."
}
2-2. 인증 코드 검증
URL POST /users/signup/verify/

Request Body

json
```

#### 2️⃣ 이메일 인증 (Email Verify)

**2-1. 인증 코드 발송**

- URL: `POST /users/signup/send/`
- Request Body:

```json
{ "email": "user@example.com" }
```

- Response:

```json
{ "message": "인증번호가 발송 되었습니다." }
```

**2-2. 인증 코드 검증**

- URL: `POST /users/signup/verify/`
- Request Body:

```json
{
  "email": "user@example.com",
  "auth_code": "12a3b456"
}
Response 예시

json
{
  "verified": true
}
3️⃣ 일반 로그인 (Login)
URL POST /users/login/

Request Body

json
```

- Response:

```json
{ "verified": true }
```

#### 3️⃣ 일반 로그인 (Login)

- URL: `POST /users/login/`
- Request Body:

```json
{
  "email": "user@example.com",
  "password": "securepassword1#"
}
Response 예시

json
```

- Response:

```json
{
  "message": "Login successful",
  "access": "access_token_string"
}
Notes

JWT Access Token 반환

필요 시 Refresh Token은 쿠키로 저장 가능

4️⃣ 소셜 로그인 (Google / Kakao)
4-1. 로그인 URL 조회
Google Login: GET /users/social/google/login/

Kakao Login: GET /users/social/kakao/login/

Response 예시

json
{
  "auth_url": "https://accounts.google.com/o/oauth2/auth..."
}
4-2. 콜백 (Callback)
Google Callback: GET /users/social/google/callback/?code=...
```

- Notes
  - JWT Access Token 반환
  - 필요 시 Refresh Token은 쿠키에 저장 가능

#### 4️⃣ 소셜 로그인 (Google / Kakao)

**4-1. 인증 URL 조회**

- `GET /users/social/google/login/`
- `GET /users/social/kakao/login/`
- Response:

```json
{ "auth_url": "https://accounts.google.com/o/oauth2/auth..." }
```

**4-2. 콜백 (Callback)**

Response 예시

json
- Google: `GET /users/social/google/callback/?code=...`
- Kakao: `GET /users/social/kakao/callback/?code=...`
- Response:

```json
{
  "message": "Google Login Success",
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "email": "user@gmail.com"
}
Notes
```

- Notes
  - 소셜 로그인 시 기존 유저가 없으면 자동 생성
  - Kakao는 닉네임/프로필 이미지만 받아와도 동작

#### 5️⃣ 로그아웃 (Logout)

- URL: `POST /users/logout/`
- Request Body:

```json
{ "refresh_token": "사용자의 refresh token" }
```

5️⃣ 로그아웃 (Logout)
URL POST /users/logout/

Request Body

json
{
  "refresh_token": "사용자의 refresh token"
}
Response 예시

json
{
  "message": "Logout successful"
}
6️⃣ 회원 탈퇴 (User Deactivate)
URL DELETE /users/signout/

Permissions

로그인 필요

Response 예시

json
{
  "회원 탈퇴가 완료되었습니다."
}
Notes

소프트 삭제 처리 (soft_delete)

DB에서 완전히 삭제되지 않고 비활성화 상태
---

# My Requests API

## 개요
로그인한 사용자가 자신이 요청한 이미지 검색 내역을 확인할 수 있는 API입니다.  
- 신청했던 이미지 URL과 처리 상태(`status`)를 최신순으로 10개씩 페이지네이션(`records` 배열)으로 반환합니다.  
- 처리 상태(`status`)는 처리중(`pending`), 완료됨(`completed`), 실패함(`completed_failed`)입니다.
- 처리 결과가 성공(`completed`)일 경우, 매핑 기능을 통해 특정 약품의 `item_seq` 값으로 변환되어 출력됩니다.
##프론트 처리 요청
- `item_seq`를 이용해 **pills 앱의 상세 API**(`/pills/<item_seq>/`)로 이동할 수 있습니다.  
- 매핑표에 없는 값은 `"결과 없음"`으로 처리됩니다.
- Response:

```json
{ "message": "Logout successful" }
```

#### 6️⃣ 회원 탈퇴 (User Deactivate)

- URL: `DELETE /users/signout/`
- 권한: 로그인 필요
- Response:

```json
{ "회원 탈퇴가 완료되었습니다." }
```

- Notes
  - 소프트 삭제 처리 → DB에서는 비활성화 상태로 유지

### 의약품 (`apps/pills`)

- 기본 목록, 상세, 검색 (`views/pill_list_view.py`, `pill_detail_view.py`, `pill_search_view.py`)
- 북마크 기능과 테스트에서 `PillItem` 모델을 바로 사용 가능

## 오늘(2차) 작업 요약

- 북마크 API에 20개 제한 + 중복 체크 추가
- `/me` 조회/수정 시리얼라이저·뷰·URL 구성
- 작업 로그를 `docs/1차_작업내용.md`, `docs/2차_작업내용.md`로 정리
- `feat/pills-api` 브랜치 내용을 병합해 `PillItem` 모델과 인증/설정 파일 확보

## 다음 단계

1. `config/urls.py`와 메인 프로젝트에서 `/me`, 북마크, pills 라우트 확인
2. `apps.pills.models.PillItem`을 이용한 북마크/마이페이지 테스트 작성
3. Postman 등으로 명세서 응답 형식 검증 후 문서화 보완
