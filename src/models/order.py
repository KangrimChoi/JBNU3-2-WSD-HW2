"""Order Model"""
from sqlalchemy import Column, BigInteger, DECIMAL, Enum, Text, TIMESTAMP, ForeignKey, Index, text
from sqlalchemy.orm import relationship
from src.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(
        Enum("pending", "paid", "shipped", "delivered", "cancelled"),
        nullable=False,
        default="pending"
    )
    shipping_address = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    __table_args__ = (
        Index("idx_orders_user", "user_id"),
        Index("idx_orders_status", "status"),
        Index("idx_orders_created_at", "created_at"),
    )

    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
