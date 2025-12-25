# pytest 설정 및 공통 fixture
# 외부 모듈
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 내부 모듈
from src.main import app
from src.database import Base, get_db
from src.models.user import User
from src.models.book import Book
from src.models.author import Author
from src.models.category import Category
from src.auth.password import hash_password

# 테스트용 DB 설정 (TEST_DB_* 환경변수 사용, 프로덕션 DB와 분리)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "rootpassword")
DB_NAME = "test_wsd_db"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """테스트용 DB 세션"""
    # 테스트 시작 전: 모든 테이블의 데이터 삭제
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

        # 테스트 종료 후: 모든 테이블의 데이터 삭제 (스키마는 유지)
        with engine.begin() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            for table in reversed(Base.metadata.sorted_tables):
                conn.execute(text(f"TRUNCATE TABLE {table.name}"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))


@pytest.fixture(scope="function")
def client(db_session):
    """테스트 클라이언트"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """테스트용 일반 사용자"""
    user = User(
        email="user1@example.com",
        password_hash=hash_password("P@ssw0rd!"),
        name="Test User",
        role="user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin(db_session):
    """테스트용 관리자"""
    admin = User(
        email="admin@example.com",
        password_hash=hash_password("P@ssw0rd!"),
        name="Test Admin",
        role="admin"
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def user_token(client, test_user):
    """일반 사용자 JWT 토큰"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "user1@example.com",
            "password": "P@ssw0rd!"
        }
    )
    return response.json()["payload"]["access_token"]


@pytest.fixture
def admin_token(client, test_admin):
    """관리자 JWT 토큰"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "admin@example.com",
            "password": "P@ssw0rd!"
        }
    )
    return response.json()["payload"]["access_token"]


@pytest.fixture
def test_book(db_session):
    """테스트용 도서"""
    # 저자 생성
    author = Author(name="Test Author")
    db_session.add(author)
    db_session.flush()

    # 카테고리 생성
    category = Category(name="Fiction")
    db_session.add(category)
    db_session.flush()

    # 도서 생성
    book = Book(
        title="Test Book",
        description="This is a test book",
        isbn="9780123456789",
        cover_image_url="http://example.com/cover.jpg",
        price=19.99,
        publication_date="2024-01-01"
    )
    book.authors.append(author)
    book.categories.append(category)

    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    return book
