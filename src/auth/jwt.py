"""JWT token utilities"""
#외부 모듈
from datetime import datetime, timedelta, timezone
from typing import Optional, Any

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session

#내부 모듈
from src.config import settings
from src.database import get_db
from src.models.user import User
from src.redis import is_token_blacklisted


class APIException(Exception):
    """API 예외 - ErrorResponse 형식에 맞는 커스텀 예외 for 전역 에러 처리"""
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Access Token 생성"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Refresh Token 생성"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str, token_type: str = "access") -> dict:
    """토큰 검증 및 페이로드 반환"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != token_type:
            raise APIException(
                status_code=401,
                code="UNAUTHORIZED",
                message="Invalid token type"
            )
        return payload
    except ExpiredSignatureError:
        raise APIException(
            status_code=401,
            code="TOKEN_EXPIRED",
            message="Token has expired"
        )
    except JWTError:
        raise APIException(
            status_code=401,
            code="UNAUTHORIZED",
            message="Invalid token"
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """현재 인증된 사용자 반환"""
    token = credentials.credentials

    # 블랙리스트 확인
    if is_token_blacklisted(token):
        raise APIException(
            status_code=401,
            code="TOKEN_BLACKLISTED",
            message="Token has been revoked"
        )

    payload = verify_token(token, "access")

    user_id = payload.get("sub")
    if user_id is None:
        raise APIException(
            status_code=401,
            code="UNAUTHORIZED",
            message="Invalid token payload"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise APIException(
            status_code=401,
            code="USER_NOT_FOUND",
            message="User not found"
        )

    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """현재 인증된 관리자 사용자 반환"""
    if str(current_user.role) != "admin":
        raise APIException(
            status_code=403,
            code="FORBIDDEN",
            message="Admin access required"
        )
    return current_user
