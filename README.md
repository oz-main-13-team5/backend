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

- `GET /bookmark` : 로그인 사용자의 북마크 목록 (20개 페이지네이션)
- `POST /bookmark` : 약품 북마크 추가  
  - 이미 존재하면 `409`  
  - 20개 초과 시 `201` with `success: false`
- `DELETE /bookmark` : 북마크 삭제 (body에서 `id`)

### 마이페이지 (`apps/mypage`)

- `GET /me` : 현재 로그인한 사용자의 프로필 조회
- `PATCH /me` : 닉네임·비밀번호 수정 (`updated_fields` 배열 반환)

### 인증 (`apps/users`)

1. **회원가입**
   - `POST /users/signup/`
   - 이메일 인증 흐름: `signup/send/` → `signup/verify/` → `signup/`
2. **이메일 인증**
   - `POST /users/signup/send/` : 인증번호 발송
   - `POST /users/signup/verify/` : 인증번호 검증
3. **일반 로그인**
   - `POST /users/login/` → JWT Access Token 발급
4. **소셜 로그인**
   - `GET /users/social/<provider>/login/` : 각 플랫폼 인증 URL 반환

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
