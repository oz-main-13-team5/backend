# 북마크 (Bookmarks) 앱

## 📋 개요

사용자가 즐겨찾기로 등록한 약품 정보를 관리하는 앱입니다.

## 🗂️ 파일 구조

```
apps/bookmarks/
├── __init__.py
├── apps.py
├── admin.py
├── models.py
├── serializers.py
├── views.py
├── urls.py
└── README.md
```

## 📝 주요 기능

### 1. 북마크 조회 (GET /bookmark)
- 현재 로그인한 사용자의 북마크 목록 조회
- 페이지네이션 지원 (20개씩)

### 2. 북마크 추가 (POST /bookmark)
- 약품을 북마크에 추가
- 최대 20개까지 저장 가능
- 20개 초과 시 `201`과 함께 `success: false` 응답
- 중복 북마크 시 `409` 응답

### 3. 북마크 삭제 (DELETE /bookmark)
- Body에 `{"item_seq": "P001"}`를 보내 북마크에서 해당 약품 제거

## 🔧 설정

### settings.py에 앱 등록

```python
INSTALLED_APPS = [
    # ... 기존 앱들 ...
    'apps.bookmarks',
]
```

### 메인 urls.py에 연결

```python
from django.urls import path, include

urlpatterns = [
    # ... 기존 URL들 ...
    path('', include('apps.bookmarks.urls')),
]
```

## 🗄️ 데이터베이스

### 마이그레이션

```bash
python manage.py makemigrations bookmarks
python manage.py migrate
```

### 테이블 구조

- **테이블명**: `bookmark`
- **컬럼**:
  - `id`: INT (PK, AUTO_INCREMENT)
  - `user_id`: UUID (FK → users.id)
  - `item_seq`: TEXT (FK → pill_items.item_seq)

## ⚠️ 주의사항

1. **PillItem 모델 확인 필요**
   - `apps.pills.models.PillItem` 모델이 존재해야 함
   - 모델명이 다르면 `models.py`의 ForeignKey 참조 수정 필요

2. **인증 필수**
   - 모든 API는 로그인한 사용자만 접근 가능
   - JWT 토큰 인증 필요

3. **테이블 명세서 준수**
   - 테이블 구조는 테이블 명세서에 정의된 대로 구현됨
   - 변경 시 팀원들과 협의 필요

## 📚 참고 문서

- `docs/1차_작업내용.md`, `docs/2차_작업내용.md`, `docs/3차_작업내용.md`
