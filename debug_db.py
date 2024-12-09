from app import create_app
from app.models import Book
from sqlalchemy import func

app = create_app()

with app.app_context():
    # Get count using both methods
    count_method1 = len(Book.query.all())
    count_method2 = Book.query.with_entities(func.count()).scalar()
    
    print(f"Count using .all(): {count_method1}")
    print(f"Count using count(): {count_method2}")
    
    # Show all books in database
    print("\nAll books in database:")
    print("-" * 50)
    for book in Book.query.all():
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")
        print("-" * 50)
