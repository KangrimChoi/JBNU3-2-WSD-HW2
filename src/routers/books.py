#외부 모듈
from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

#내부 모듈
from src.database import get_db
from src.schema.books import BookCreate, BookCreateResponse
from src.schema.common import APIResponse, ErrorResponse
from src.models.book import Book
from src.models.author import Author
from src.models.category import Category
from src.auth.jwt import get_current_admin_user
from src.models.user import User


router = APIRouter(prefix="/api/books", tags=["Books"])

# ==================== 도서 CRUD ====================

# Create (도서 등록) - 관리자 전용
@router.post(
    "/",
    summary="도서 등록 (관리자)",
    response_model=APIResponse[BookCreateResponse],
    status_code=status.HTTP_201_CREATED
)
async def create_book(
    request: Request,
    book_data: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    새로운 도서를 등록합니다.
    - 관리자 권한 필요
    - ISBN 중복 검사
    - 저자/카테고리가 없으면 자동 생성
    """
    # ISBN 중복 검사
    existing_book = db.query(Book).filter(Book.isbn == book_data.isbn).first()
    if existing_book:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorResponse(
                timestamp=datetime.now(),
                path=str(request.url.path),
                status=409,
                code="DUPLICATE_ISBN",
                message="이미 등록된 ISBN입니다",
                details={"isbn": book_data.isbn}
            ).model_dump(mode="json")
        )

    # 저자 처리 (없으면 생성)
    authors = []
    for author_name in book_data.authors:
        author = db.query(Author).filter(Author.name == author_name).first()
        if not author:
            author = Author(name=author_name)
            db.add(author)
            db.flush()  # ID 할당을 위해 flush
        authors.append(author)

    # 카테고리 처리 (없으면 생성)
    categories = []
    for category_name in book_data.categories:
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.flush()
        categories.append(category)

    # 도서 생성
    new_book = Book(
        title=book_data.title,
        description=book_data.description,
        isbn=book_data.isbn,
        cover_image_url=book_data.cover_image_url,
        price=book_data.price,
        publication_date=book_data.publication_date
    )
    new_book.authors = authors
    new_book.categories = categories

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    # 응답 생성
    response_data = BookCreateResponse(
        id=new_book.id,
        title=new_book.title,
        categories=[cat.name for cat in new_book.categories],
        authors=[auth.name for auth in new_book.authors],
        description=new_book.description,
        isbn=new_book.isbn,
        cover_image_url=new_book.cover_image_url,
        price=new_book.price,
        publication_date=new_book.publication_date,
        created_at=new_book.created_at
    )

    return APIResponse(
        is_success=True,
        message="도서가 성공적으로 등록되었습니다.",
        payload=response_data
    )
