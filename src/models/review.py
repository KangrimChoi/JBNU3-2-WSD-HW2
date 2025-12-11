"""Review Model"""
from sqlalchemy import Column, BigInteger, Integer, Text, TIMESTAMP, ForeignKey, Index, text
from sqlalchemy.orm import relationship
from src.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(BigInteger, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    __table_args__ = (
        Index("idx_reviews_user_book", "user_id", "book_id"),
        Index("idx_reviews_book", "book_id"),
        Index("idx_reviews_rating", "rating"),
    )

    # Relationships
    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")
    likes = relationship("ReviewLike", back_populates="review", cascade="all, delete-orphan")
