"""Redis client for token management"""
import redis
from src.config import settings


# Redis 클라이언트 생성
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)


# ==================== Access Token 블랙리스트 ====================

def blacklist_access_token(token: str, expires_in: int) -> None:
    """Access Token을 블랙리스트에 추가 (로그아웃 시)"""
    redis_client.setex(f"blacklist:{token}", expires_in, "1")


def is_token_blacklisted(token: str) -> bool:
    """토큰이 블랙리스트에 있는지 확인"""
    return redis_client.exists(f"blacklist:{token}") > 0


# ==================== Refresh Token 관리 ====================

def store_refresh_token(user_id: int, token: str, expires_in: int) -> None:
    """Refresh Token을 Redis에 저장"""
    redis_client.setex(f"refresh:{user_id}", expires_in, token)


def get_refresh_token(user_id: int) -> str | None:
    """저장된 Refresh Token 조회"""
    return redis_client.get(f"refresh:{user_id}")


def delete_refresh_token(user_id: int) -> None:
    """Refresh Token 삭제 (로그아웃 시)"""
    redis_client.delete(f"refresh:{user_id}")


def is_valid_refresh_token(user_id: int, token: str) -> bool:
    """Refresh Token이 유효한지 확인"""
    stored_token = get_refresh_token(user_id)
    return stored_token == token
