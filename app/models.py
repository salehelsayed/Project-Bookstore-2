"""
SQLAlchemy models for the application.
"""
from .db import db
from datetime import datetime
from sqlalchemy import Date

class Book(db.Model):
    """
    Book model representing a book in the library.

    Attributes:
        id (int): Primary key.
        title (str): Title of the book.
        author (str): Author of the book.
        category (str): Category or genre of the book.
        language (str): Language of the book.
        description (str): Short description or summary of the book.
        file_path (str): Path to the book file in storage.
        image_path (str): Path to the book cover image.
        rating (float): Average rating of the book.
        reviews_count (int): Number of reviews the book has received.
    """
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    language = db.Column(db.String(50))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    rating = db.Column(db.Float)
    reviews_count = db.Column(db.Integer)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'
