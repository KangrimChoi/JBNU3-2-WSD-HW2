from pydantic import BaseModel, EmailStr, Field


# ==================== Request Schemas ====================
class AuthLogin(BaseModel):
    """로그인 요청"""
    email: EmailStr = Field(..., json_schema_extra={"example": "user@example.com", "description": "사용자 이메일"})
    password: str = Field(..., min_length=8, max_length=100, json_schema_extra={"example": "p@ssw0rd!", "description": "사용자 비밀번호"})


class TokenRefresh(BaseModel):
    """토큰 갱신 요청"""
    refresh_token: str = Field(..., json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIs...", "description": "Refresh Token"})


class FirebaseLogin(BaseModel):
    """Firebase 로그인 요청"""
    id_token: str = Field(..., json_schema_extra={"example": "eyJhbGciOiJSUzI1NiIs...", "description": "Firebase ID Token"})

# ==================== Response Schemas ====================
class LoginResponse(BaseModel):
    """로그인 응답"""
    access_token: str = Field(..., json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIs...", "description": "Access Token"})
    refresh_token: str = Field(..., json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIs...", "description": "Refresh Token"})
    token_type: str = Field(default="bearer", json_schema_extra={"example": "bearer", "description": "토큰 타입"})


class TokenRefreshResponse(BaseModel):
    """토큰 갱신 응답"""
    access_token: str = Field(..., json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIs...", "description": "새 Access Token"})
    token_type: str = Field(default="bearer", json_schema_extra={"example": "bearer", "description": "토큰 타입"})