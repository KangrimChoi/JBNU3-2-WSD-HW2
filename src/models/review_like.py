"""Review Like Model"""
from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey, Index, text
from sqlalchemy.orm import relationship
from src.database import Base


class ReviewLike(Base):
    __tablename__ = "review_likes"

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    review_id = Column(BigInteger, ForeignKey("reviews.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    __table_args__ = (
        Index("idx_review_likes_review", "review_id"),
    )

    # Relationships
    user = relationship("User", back_populates="review_likes")
    review = relationship("Review", back_populates="likes")
