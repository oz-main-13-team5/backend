# 북마크 & 마이페이지 기능

## 프로젝트 개요

의약품 정보 서비스의 북마크 및 마이페이지 기능 구현

## 프로젝트 구조

```
.
├── apps/
│   ├── bookmarks/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── mypage/
│       ├── __init__.py
│       ├── apps.py
│       ├── serializers.py
│       ├── urls.py
│       └── views.py
├── docs/                 # 로컬 작업 로그 (git 미추적)
├── .gitignore
└── README.md
```

## 빠른 시작

### 1. 앱 등록 (settings.py)

```python
INSTALLED_APPS = [
    # ... 기존 앱들 ...
    'apps.bookmarks',
]
```

### 2. URL 설정 (프로젝트 메인 urls.py)

```python
from django.urls import path, include

urlpatterns = [
    # ... 기존 URL들 ...
    path('', include('apps.bookmarks.urls')),
]
```

### 3. 마이그레이션

```bash
python manage.py makemigrations bookmarks
python manage.py migrate
```

## API 엔드포인트

### 북마크

- `GET /bookmark` - 북마크 목록 조회
- `POST /bookmark` - 북마크 추가
- `DELETE /bookmark` - 북마크 삭제
  - 중복 등록 시 `409` 반환
  - 20개 이상 등록 시 `201`과 함께 `success: false` 응답

### 마이페이지

- `GET /me` - 사용자 프로필 조회
- `PATCH /me` - 닉네임/비밀번호 수정 (`updated_fields` 반환)

## 주의사항

1. **PillItem 모델 확인 필요**
   - `apps.pills.models.PillItem` 모델이 존재해야 함
   - 모델명이 다르면 `apps/bookmarks/models.py`의 ForeignKey 참조 수정 필요

2. **인증 필수**
   - 모든 API는 로그인한 사용자만 접근 가능
   - JWT 토큰 인증 필요

3. **테이블 명세서 준수**
   - 테이블 구조는 테이블 명세서에 정의된 대로 구현됨
   - 변경 시 팀원들과 협의 필요

## 📚 참고 문서

- `apps/bookmarks/README.md`: 앱별 구성과 사용법
- `apps/mypage/`: 마이페이지 앱 구성
- `docs/` 폴더: 작업 로그 (로컬에서만 관리, Git 미추적)
