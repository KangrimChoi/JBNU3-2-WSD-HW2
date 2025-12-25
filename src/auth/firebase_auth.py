"""Firebase Authentication 처리"""
import firebase_admin
from firebase_admin import credentials, auth
from src.config import settings

# Firebase Admin SDK 초기화 (앱이 이미 초기화되지 않았을 때만)
def initialize_firebase():
    """Firebase Admin SDK 초기화"""
    if not firebase_admin._apps:
        # 환경변수에서 Firebase 자격 증명 가져오기
        cred_dict = {
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key": settings.FIREBASE_PRIVATE_KEY,
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
            "token_uri": "https://oauth2.googleapis.com/token",
        }

        # 자격 증명이 모두 설정되어 있는지 확인
        if all([settings.FIREBASE_PROJECT_ID, settings.FIREBASE_PRIVATE_KEY, settings.FIREBASE_CLIENT_EMAIL]):
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        else:
            # Firebase 설정이 없으면 초기화하지 않음 (선택적 기능으로 처리)
            pass


def verify_firebase_token(id_token: str) -> dict:
    """
    Firebase ID Token 검증

    Args:
        id_token: Firebase에서 발급한 ID Token

    Returns:
        dict: 검증된 사용자 정보 (uid, email, name 등)

    Raises:
        ValueError: 토큰이 유효하지 않을 때
    """
    try:
        # Firebase Admin SDK가 초기화되지 않았다면 초기화
        initialize_firebase()

        # ID Token 검증
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid Firebase ID token: {str(e)}")