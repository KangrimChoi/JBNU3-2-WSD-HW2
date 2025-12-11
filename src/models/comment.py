"""Comment Model"""
from sqlalchemy import Column, BigInteger, Text, TIMESTAMP, ForeignKey, Index, text
from sqlalchemy.orm import relationship
from src.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(BigInteger, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    __table_args__ = (
        Index("idx_comments_user", "user_id"),
        Index("idx_comments_book", "book_id"),
    )

    # Relationships
    user = relationship("User", back_populates="comments")
    book = relationship("Book", back_populates="comments")
    likes = relationship("CommentLike", back_populates="comment", cascade="all, delete-orphan")
