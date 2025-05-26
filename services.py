from sqlalchemy.orm import Session
from models import Reader, Book, Review
from database import db
from sqlalchemy import func

class BookService:
    def __init__(self):
        self.session = db.get_session()
    
    def add_book(self, title: str, author: str, genre: str = None) -> Book:
        book = Book(title=title, author=author, genre=genre)
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book
    
    def get_all_books(self):
        return self.session.query(Book).all()
    
    def get_book_by_id(self, book_id: int):
        return self.session.query(Book).filter(Book.id == book_id).first()
    
    def delete_book(self, book_id: int) -> bool:
        book = self.get_book_by_id(book_id)
        if book:
            self.session.delete(book)
            self.session.commit()
            return True
        return False
    
    def get_book_stats(self, book_id: int):
        book = self.get_book_by_id(book_id)
        if not book:
            return None
        
        review_count = self.session.query(Review).filter(Review.book_id == book_id).count()
        avg_rating = self.session.query(func.avg(Review.rating)).filter(Review.book_id == book_id).scalar()
        
        return {
            'book': book,
            'review_count': review_count,
            'average_rating': round(avg_rating, 2) if avg_rating else 0
        }

class ReaderService:
    def __init__(self):
        self.session = db.get_session()
    
    def register_reader(self, name: str) -> Reader:
        existing_reader = self.session.query(Reader).filter(Reader.name == name).first()
        if existing_reader:
            return existing_reader
        
        reader = Reader(name=name)
        self.session.add(reader)
        self.session.commit()
        self.session.refresh(reader)
        return reader
    
    def get_reader_by_name(self, name: str):
        return self.session.query(Reader).filter(Reader.name == name).first()
    
    def get_reader_reviews(self, reader_id: int):
        return self.session.query(Review).filter(Review.reader_id == reader_id).all()

class ReviewService:
    def __init__(self):
        self.session = db.get_session()
    
    def add_review(self, book_id: int, reader_id: int, rating: int, comment: str = None) -> Review:
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        review = Review(book_id=book_id, reader_id=reader_id, rating=rating, comment=comment)
        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)
        return review
    
    def get_book_reviews(self, book_id: int):
        return self.session.query(Review).filter(Review.book_id == book_id).all()