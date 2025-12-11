"""Library Item Model"""
from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey, Index, text
from sqlalchemy.orm import relationship
from src.database import Base


class LibraryItem(Base):
    __tablename__ = "library_items"

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), primary_key=True)
    book_id = Column(BigInteger, ForeignKey("books.id", ondelete="RESTRICT"), primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    __table_args__ = (
        Index("idx_library_items_book", "book_id"),
    )

    # Relationships
    user = relationship("User", back_populates="library_items")
    book = relationship("Book", back_populates="library_items")
