from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Reader(Base):
    __tablename__ = 'readers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    
    reviews = relationship("Review", back_populates="reader")

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    genre = Column(String(50), nullable=True)
    
    reviews = relationship("Review", back_populates="book")

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    reader_id = Column(Integer, ForeignKey('readers.id'), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 scale
    comment = Column(Text, nullable=True)
    
    book = relationship("Book", back_populates="reviews")
    reader = relationship("Reader", back_populates="reviews")