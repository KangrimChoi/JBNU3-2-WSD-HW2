"""Wishlist Item Model"""
from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey, Index, text
from sqlalchemy.orm import relationship
from src.database import Base


class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    book_id = Column(BigInteger, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    __table_args__ = (
        Index("idx_wishlist_items_book", "book_id"),
    )

    # Relationships
    user = relationship("User", back_populates="wishlist_items")
    book = relationship("Book", back_populates="wishlist_items")
