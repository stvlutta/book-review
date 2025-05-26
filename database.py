from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Reader, Book, Review
import os

DATABASE_URL = "sqlite:///book_reviews.db"

class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.init_db()
    
    def init_db(self):
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        return self.SessionLocal()

db = Database()