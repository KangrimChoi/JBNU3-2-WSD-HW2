"""Author Model"""
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from src.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    books = relationship("Book", secondary="book_authors", back_populates="authors")
