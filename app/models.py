"""
SQLAlchemy models for the application.
"""
from .db import db
from datetime import datetime

class Book(db.Model):
    """
    Book model representing a book in the digital library.
    
    Attributes:
        id (int): Primary key
        title (str): Book title
        author (str): Book author
        path (str): Path to the book PDF file
        cover_path (str): Path to the book cover image
        metadata_path (str): Path to additional metadata (optional)
        created_at (datetime): Timestamp of when the book was added
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    path = db.Column(db.String(500), nullable=False, unique=True)
    cover_path = db.Column(db.String(500))
    metadata_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'
