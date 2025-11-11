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

signup/send/ → 이메일로 인증 코드 발송

signup/verify/ → 인증 코드 검증 후 이메일 유효성 확인

이메일 인증 완료 후 signup/으로 회원가입 진행

Response 예시

json
{
  "email": "user@example.com",
  "username": "user@example.com",
  "id": 1
}
2️⃣ 이메일 인증 (Email Verify)
2-1. 인증 코드 발송
URL POST /users/signup/send/

Request Body

json
{
  "email": "user@example.com"
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
{
  "email": "user@example.com",
  "password": "securepassword1#"
}
Response 예시

json
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

Kakao Callback: GET /users/social/kakao/callback/?code=...

Response 예시

json
{
  "message": "Google Login Success",
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "email": "user@gmail.com"
}
Notes

소셜 로그인 시 유저가 없으면 새로 생성됨

Kakao는 프로필 사진과 닉네임만 받아옴

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