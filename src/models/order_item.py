"""Order Item Model"""
from sqlalchemy import Column, BigInteger, Integer, DECIMAL, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from src.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(BigInteger, ForeignKey("books.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(DECIMAL(10, 2), nullable=False)

    __table_args__ = (
        UniqueConstraint("order_id", "book_id", name="idx_order_items_order_book"),
        Index("idx_order_items_order", "order_id"),
        Index("idx_order_items_book", "book_id"),
    )

    # Relationships
    order = relationship("Order", back_populates="items")
    book = relationship("Book", back_populates="order_items")
