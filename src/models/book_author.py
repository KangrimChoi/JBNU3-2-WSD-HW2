"""Book-Author Junction Table"""
from sqlalchemy import Column, BigInteger, ForeignKey, Index
from src.database import Base


class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id = Column(BigInteger, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    author_id = Column(BigInteger, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (
        Index("idx_book_authors_author", "author_id"),
    )
