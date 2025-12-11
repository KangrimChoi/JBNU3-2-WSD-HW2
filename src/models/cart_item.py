"""Cart Item Model"""
from sqlalchemy import Column, BigInteger, Integer, TIMESTAMP, ForeignKey, Index, text
from sqlalchemy.orm import relationship
from src.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    book_id = Column(BigInteger, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    __table_args__ = (
        Index("idx_cart_items_book", "book_id"),
    )

    # Relationships
    user = relationship("User", back_populates="cart_items")
    book = relationship("Book", back_populates="cart_items")
