"""
시드 데이터 생성 스크립트
Usage: python scripts/seed.py

총 200건 이상의 시드 데이터 생성
- users: 12명 (admin 2명 + user 10명)
- authors: 20명
- categories: 10개
- books: 50권
- book_authors: ~60개
- book_categories: ~60개
- reviews: 40개
- comments: 40개
- review_likes: 30개
- comment_likes: 30개
- cart_items: 20개
- wishlist_items: 20개
- library_items: 25개
- orders: 15개
- order_items: 35개
"""
import sys
import os
import random
from datetime import datetime, timedelta
from decimal import Decimal

# 프로젝트 루트를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from src.database import engine, Base
from src.models import (
    User, Book, Author, Category,
    BookAuthor, BookCategory,
    Review, Comment,
    ReviewLike, CommentLike,
    CartItem, WishlistItem, LibraryItem,
    Order, OrderItem
)

# bcrypt 해시 생성
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


# 샘플 데이터
SAMPLE_AUTHORS = [
    "김영하", "한강", "박경리", "이문열", "신경숙",
    "조정래", "황석영", "은희경", "김훈", "공지영",
    "정유정", "김애란", "박민규", "천명관", "김연수",
    "편혜영", "최은영", "손원평", "조남주", "정세랑"
]

SAMPLE_CATEGORIES = [
    "소설", "시/에세이", "경제/경영", "자기계발", "인문학",
    "역사", "과학", "예술", "여행", "요리"
]

SAMPLE_BOOK_TITLES = [
    "살인자의 기억법", "채식주의자", "토지", "우리들의 일그러진 영웅", "엄마를 부탁해",
    "태백산맥", "오래된 정원", "새의 선물", "칼의 노래", "도가니",
    "7년의 밤", "두근두근 내 인생", "죽은 왕녀를 위한 파반느", "고령화 가족", "밤은 노래한다",
    "재와 빨강", "쇼코의 미소", "아몬드", "82년생 김지영", "시선으로부터",
    "불편한 편의점", "달러구트 꿈 백화점", "파친코", "작별인사", "흔한남매",
    "트렌드 코리아 2024", "역행자", "세이노의 가르침", "부의 추월차선", "돈의 속성",
    "미움받을 용기", "아주 작은 습관의 힘", "생각에 관한 생각", "사피엔스", "총균쇠",
    "코스모스", "이기적 유전자", "침묵의 봄", "호모 데우스", "21세기를 위한 21가지 제언",
    "나미야 잡화점의 기적", "가면산장 살인사건", "용의자 X의 헌신", "백야행", "비밀",
    "노르웨이의 숲", "상실의 시대", "1Q84", "해변의 카프카", "어둠의 왼손"
]

SAMPLE_REVIEWS = [
    "정말 재미있게 읽었습니다. 강력 추천!",
    "기대 이상이었어요. 작가의 필력이 대단합니다.",
    "조금 지루한 부분도 있지만 전체적으로 좋았습니다.",
    "인생 책입니다. 여러 번 읽어도 좋아요.",
    "스토리가 탄탄하고 몰입감이 좋습니다.",
    "문체가 아름답습니다. 번역도 잘 되어있어요.",
    "생각보다 어려웠지만 배울 점이 많았습니다.",
    "한 번쯤 읽어볼 만한 책입니다.",
    "기대했던 것과는 조금 달랐어요.",
    "끝까지 긴장감이 유지되는 책입니다."
]

SAMPLE_COMMENTS = [
    "저도 이 책 읽어봤는데 정말 좋아요!",
    "리뷰 잘 봤습니다. 참고할게요.",
    "이 책 시리즈 다 읽어보세요!",
    "작가님 다른 책도 추천드려요.",
    "공감합니다. 저도 비슷하게 느꼈어요.",
    "좋은 리뷰 감사합니다.",
    "이 책 선물용으로도 좋을까요?",
    "오디오북으로도 나왔으면 좋겠네요.",
    "전자책으로 읽었는데 종이책도 사고 싶어요.",
    "다음 편 언제 나오나요?"
]

SAMPLE_ADDRESSES = [
    "서울시 강남구 테헤란로 123, 456호",
    "서울시 마포구 홍대입구역 789번길 10",
    "경기도 성남시 분당구 판교로 234",
    "부산시 해운대구 마린시티 567",
    "인천시 연수구 송도동 890-12",
    "대전시 유성구 대학로 111",
    "대구시 수성구 범어동 222-33",
    "광주시 서구 상무대로 444",
    "전주시 완산구 효자동 555-66",
    "제주시 연동 777-88"
]


def clear_all_tables(db: Session):
    """모든 테이블 데이터 삭제"""
    print("Clearing existing data...")
    db.query(OrderItem).delete()
    db.query(Order).delete()
    db.query(LibraryItem).delete()
    db.query(WishlistItem).delete()
    db.query(CartItem).delete()
    db.query(CommentLike).delete()
    db.query(ReviewLike).delete()
    db.query(Comment).delete()
    db.query(Review).delete()
    db.query(BookCategory).delete()
    db.query(BookAuthor).delete()
    db.query(Category).delete()
    db.query(Author).delete()
    db.query(Book).delete()
    db.query(User).delete()
    db.commit()
    print("All tables cleared.")


def seed_users(db: Session) -> list[User]:
    """사용자 시드 데이터"""
    print("Seeding users...")
    password_hash = hash_password("P@ssw0rd!")

    users = [
        # 관리자
        User(email="admin@example.com", password_hash=password_hash, name="관리자", role="admin"),
        User(email="admin2@example.com", password_hash=password_hash, name="부관리자", role="admin"),
        # 일반 사용자
        User(email="user1@example.com", password_hash=password_hash, name="김철수", role="user"),
        User(email="user2@example.com", password_hash=password_hash, name="이영희", role="user"),
        User(email="user3@example.com", password_hash=password_hash, name="박민수", role="user"),
        User(email="user4@example.com", password_hash=password_hash, name="최지영", role="user"),
        User(email="user5@example.com", password_hash=password_hash, name="정대현", role="user"),
        User(email="user6@example.com", password_hash=password_hash, name="강수진", role="user"),
        User(email="user7@example.com", password_hash=password_hash, name="윤서연", role="user"),
        User(email="user8@example.com", password_hash=password_hash, name="장민호", role="user"),
        User(email="user9@example.com", password_hash=password_hash, name="한예슬", role="user"),
        User(email="user10@example.com", password_hash=password_hash, name="오준혁", role="user"),
    ]

    db.add_all(users)
    db.commit()
    for u in users:
        db.refresh(u)
    print(f"  Created {len(users)} users")
    return users


def seed_authors(db: Session) -> list[Author]:
    """저자 시드 데이터"""
    print("Seeding authors...")
    authors = [Author(name=name) for name in SAMPLE_AUTHORS]
    db.add_all(authors)
    db.commit()
    for a in authors:
        db.refresh(a)
    print(f"  Created {len(authors)} authors")
    return authors


def seed_categories(db: Session) -> list[Category]:
    """카테고리 시드 데이터"""
    print("Seeding categories...")
    categories = [Category(name=name) for name in SAMPLE_CATEGORIES]
    db.add_all(categories)
    db.commit()
    for c in categories:
        db.refresh(c)
    print(f"  Created {len(categories)} categories")
    return categories


def seed_books(db: Session) -> list[Book]:
    """도서 시드 데이터"""
    print("Seeding books...")
    books = []
    for i, title in enumerate(SAMPLE_BOOK_TITLES):
        book = Book(
            title=title,
            description=f"{title}의 상세 설명입니다. 이 책은 많은 독자들에게 사랑받는 작품입니다.",
            isbn=f"{9788900000000 + i}",
            cover_image_url=f"https://example.com/covers/book_{i+1}.jpg",
            price=Decimal(random.randint(10000, 35000)),
            publication_date=datetime.now().date() - timedelta(days=random.randint(30, 1000))
        )
        books.append(book)

    db.add_all(books)
    db.commit()
    for b in books:
        db.refresh(b)
    print(f"  Created {len(books)} books")
    return books


def seed_book_authors(db: Session, books: list[Book], authors: list[Author]):
    """도서-저자 연결"""
    print("Seeding book_authors...")
    book_authors = []
    for book in books:
        # 각 책에 1~2명의 저자 배정
        num_authors = random.randint(1, 2)
        selected_authors = random.sample(authors, num_authors)
        for author in selected_authors:
            book_authors.append(BookAuthor(book_id=book.id, author_id=author.id))

    db.add_all(book_authors)
    db.commit()
    print(f"  Created {len(book_authors)} book-author relations")


def seed_book_categories(db: Session, books: list[Book], categories: list[Category]):
    """도서-카테고리 연결"""
    print("Seeding book_categories...")
    book_categories = []
    for book in books:
        # 각 책에 1~2개의 카테고리 배정
        num_cats = random.randint(1, 2)
        selected_cats = random.sample(categories, num_cats)
        for cat in selected_cats:
            book_categories.append(BookCategory(book_id=book.id, category_id=cat.id))

    db.add_all(book_categories)
    db.commit()
    print(f"  Created {len(book_categories)} book-category relations")


def seed_reviews(db: Session, users: list[User], books: list[Book]) -> list[Review]:
    """리뷰 시드 데이터"""
    print("Seeding reviews...")
    reviews = []
    regular_users = [u for u in users if u.role == "user"]

    for _ in range(40):
        review = Review(
            user_id=random.choice(regular_users).id,
            book_id=random.choice(books).id,
            rating=random.randint(3, 5),
            content=random.choice(SAMPLE_REVIEWS)
        )
        reviews.append(review)

    db.add_all(reviews)
    db.commit()
    for r in reviews:
        db.refresh(r)
    print(f"  Created {len(reviews)} reviews")
    return reviews


def seed_comments(db: Session, users: list[User], books: list[Book]) -> list[Comment]:
    """댓글 시드 데이터"""
    print("Seeding comments...")
    comments = []
    regular_users = [u for u in users if u.role == "user"]

    for _ in range(40):
        comment = Comment(
            user_id=random.choice(regular_users).id,
            book_id=random.choice(books).id,
            content=random.choice(SAMPLE_COMMENTS)
        )
        comments.append(comment)

    db.add_all(comments)
    db.commit()
    for c in comments:
        db.refresh(c)
    print(f"  Created {len(comments)} comments")
    return comments


def seed_review_likes(db: Session, users: list[User], reviews: list[Review]):
    """리뷰 좋아요 시드 데이터"""
    print("Seeding review_likes...")
    review_likes = []
    regular_users = [u for u in users if u.role == "user"]
    used_pairs = set()

    for _ in range(30):
        user = random.choice(regular_users)
        review = random.choice(reviews)
        pair = (user.id, review.id)
        if pair not in used_pairs:
            used_pairs.add(pair)
            review_likes.append(ReviewLike(user_id=user.id, review_id=review.id))

    db.add_all(review_likes)
    db.commit()
    print(f"  Created {len(review_likes)} review likes")


def seed_comment_likes(db: Session, users: list[User], comments: list[Comment]):
    """댓글 좋아요 시드 데이터"""
    print("Seeding comment_likes...")
    comment_likes = []
    regular_users = [u for u in users if u.role == "user"]
    used_pairs = set()

    for _ in range(30):
        user = random.choice(regular_users)
        comment = random.choice(comments)
        pair = (user.id, comment.id)
        if pair not in used_pairs:
            used_pairs.add(pair)
            comment_likes.append(CommentLike(user_id=user.id, comment_id=comment.id))

    db.add_all(comment_likes)
    db.commit()
    print(f"  Created {len(comment_likes)} comment likes")


def seed_cart_items(db: Session, users: list[User], books: list[Book]):
    """장바구니 시드 데이터"""
    print("Seeding cart_items...")
    cart_items = []
    regular_users = [u for u in users if u.role == "user"]
    used_pairs = set()

    for _ in range(20):
        user = random.choice(regular_users)
        book = random.choice(books)
        pair = (user.id, book.id)
        if pair not in used_pairs:
            used_pairs.add(pair)
            cart_items.append(CartItem(
                user_id=user.id,
                book_id=book.id,
                quantity=random.randint(1, 3)
            ))

    db.add_all(cart_items)
    db.commit()
    print(f"  Created {len(cart_items)} cart items")


def seed_wishlist_items(db: Session, users: list[User], books: list[Book]):
    """위시리스트 시드 데이터"""
    print("Seeding wishlist_items...")
    wishlist_items = []
    regular_users = [u for u in users if u.role == "user"]
    used_pairs = set()

    for _ in range(20):
        user = random.choice(regular_users)
        book = random.choice(books)
        pair = (user.id, book.id)
        if pair not in used_pairs:
            used_pairs.add(pair)
            wishlist_items.append(WishlistItem(user_id=user.id, book_id=book.id))

    db.add_all(wishlist_items)
    db.commit()
    print(f"  Created {len(wishlist_items)} wishlist items")


def seed_library_items(db: Session, users: list[User], books: list[Book]):
    """라이브러리(구매완료) 시드 데이터"""
    print("Seeding library_items...")
    library_items = []
    regular_users = [u for u in users if u.role == "user"]
    used_pairs = set()

    for _ in range(25):
        user = random.choice(regular_users)
        book = random.choice(books)
        pair = (user.id, book.id)
        if pair not in used_pairs:
            used_pairs.add(pair)
            library_items.append(LibraryItem(user_id=user.id, book_id=book.id))

    db.add_all(library_items)
    db.commit()
    print(f"  Created {len(library_items)} library items")


def seed_orders(db: Session, users: list[User], books: list[Book]):
    """주문 시드 데이터"""
    print("Seeding orders and order_items...")
    regular_users = [u for u in users if u.role == "user"]
    order_count = 0
    order_item_count = 0

    for _ in range(15):
        user = random.choice(regular_users)

        # 주문 아이템 먼저 준비
        num_items = random.randint(1, 4)
        selected_books = random.sample(books, num_items)

        total = Decimal(0)
        items_data = []
        for book in selected_books:
            qty = random.randint(1, 2)
            price = book.price
            total += price * qty
            items_data.append((book.id, qty, price))

        # 주문 생성
        order = Order(
            user_id=user.id,
            total_price=total,
            status=random.choice(["pending", "paid", "shipped", "delivered"]),
            shipping_address=random.choice(SAMPLE_ADDRESSES)
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        order_count += 1

        # 주문 아이템 생성
        for book_id, qty, price in items_data:
            order_item = OrderItem(
                order_id=order.id,
                book_id=book_id,
                quantity=qty,
                price_at_purchase=price
            )
            db.add(order_item)
            order_item_count += 1

        db.commit()

    print(f"  Created {order_count} orders")
    print(f"  Created {order_item_count} order items")


def main():
    print("=" * 50)
    print("Seed Data Generator")
    print("=" * 50)

    with Session(engine) as db:
        # 기존 데이터 삭제
        clear_all_tables(db)

        # 시드 데이터 생성
        users = seed_users(db)
        authors = seed_authors(db)
        categories = seed_categories(db)
        books = seed_books(db)

        seed_book_authors(db, books, authors)
        seed_book_categories(db, books, categories)

        reviews = seed_reviews(db, users, books)
        comments = seed_comments(db, users, books)

        seed_review_likes(db, users, reviews)
        seed_comment_likes(db, users, comments)

        seed_cart_items(db, users, books)
        seed_wishlist_items(db, users, books)
        seed_library_items(db, users, books)

        seed_orders(db, users, books)

    print("=" * 50)
    print("Seed data created successfully!")
    print("=" * 50)
    print("\nTest accounts:")
    print("  - admin@example.com / P@ssw0rd! (admin)")
    print("  - user1@example.com / P@ssw0rd! (user)")
    print("=" * 50)


if __name__ == "__main__":
    main()
