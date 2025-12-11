"""Comment Like Model"""
from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey, Index, text
from sqlalchemy.orm import relationship
from src.database import Base


class CommentLike(Base):
    __tablename__ = "comment_likes"

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    comment_id = Column(BigInteger, ForeignKey("comments.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    __table_args__ = (
        Index("idx_comment_likes_comment", "comment_id"),
    )

    # Relationships
    user = relationship("User", back_populates="comment_likes")
    comment = relationship("Comment", back_populates="likes")
