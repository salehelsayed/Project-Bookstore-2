from app import create_app
from app.models import Book
from sqlalchemy import func

app = create_app()

with app.app_context():
    # Using SQLAlchemy's func.count() for an efficient count query
    book_count = Book.query.with_entities(func.count()).scalar()
    print(f"Total number of books in database: {book_count}")
