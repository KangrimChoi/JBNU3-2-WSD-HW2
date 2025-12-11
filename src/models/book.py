"""Book Model"""
from sqlalchemy import Column, BigInteger, String, Text, DECIMAL, Date, TIMESTAMP, text
from sqlalchemy.orm import relationship
from src.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    isbn = Column(String(13), unique=True, nullable=False, index=True)
    cover_image_url = Column(String(255))
    price = Column(DECIMAL(10, 2), nullable=False)
    publication_date = Column(Date)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    deleted_at = Column(TIMESTAMP, nullable=True, index=True)

    # Relationships
    authors = relationship("Author", secondary="book_authors", back_populates="books")
    categories = relationship("Category", secondary="book_categories", back_populates="books")
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="book", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="book", cascade="all, delete-orphan")
    wishlist_items = relationship("WishlistItem", back_populates="book", cascade="all, delete-orphan")
    library_items = relationship("LibraryItem", back_populates="book")
    order_items = relationship("OrderItem", back_populates="book")
