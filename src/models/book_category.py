"""Book-Category Junction Table"""
from sqlalchemy import Column, BigInteger, ForeignKey, Index
from src.database import Base


class BookCategory(Base):
    __tablename__ = "book_categories"

    book_id = Column(BigInteger, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(BigInteger, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (
        Index("idx_book_categories_category", "category_id"),
    )
