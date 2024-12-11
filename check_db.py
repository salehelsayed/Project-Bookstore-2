from app import create_app
from app.models import Book
from app.db import db
import os

app = create_app()

with app.app_context():
    # Print database URL
    print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Additional debugging output
    print("Attempting to query all books...")
    
    # Check if database file exists
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app.db'))
    print(f"Database path: {db_path}")
    print(f"Database file exists: {os.path.exists(db_path)}")

    # Try to query books
    try:
        books = Book.query.all()
        print(f"\nTotal books in database: {len(books)}")

        if not books:
            print("No books found in the database!")
        else:
            print("\nFirst 3 Books from Database:")
            print("-" * 50)
            for book in books[:3]:
                print(f"Title: {book.title}")
                print(f"Author: {book.author}")
                print(f"Top Downloads: {book.top_downloads}")
                print(f"Most Discussed: {book.most_discussed}")
                print("-" * 50)
    except Exception as e:
        print(f"Error querying database: {str(e)}")
        print("Ensure the database schema is up to date and matches the models.")
