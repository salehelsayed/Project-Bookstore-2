"""
Database seeding script for the bookstore application.
This script reads data from data/books_data.csv and populates the database.
"""
import csv
import os
from app import create_app
from app.models import Book
from app.db import db

def seed_database():
    """Seed the database with data from books_data.csv."""
    app = create_app()
    
    with app.app_context():
        # Check if database is already populated
        if Book.query.first() is not None:
            print("Database already contains books. Skipping seeding.")
            return

        csv_path = os.path.join('data', 'books_data.csv')
        if not os.path.exists(csv_path):
            print(f"Error: {csv_path} not found!")
            return

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    book = Book(
                        title=row['title'],
                        author=row['author'],
                        category=row['category'],
                        language=row['language'],
                        description=row['description'],
                        path=row['file_path'],
                        cover_path=row['image_path'],
                        rating=float(row['rating']),
                        reviews_count=int(row['reviews_count'])
                    )
                    db.session.add(book)
                    print(f"Added book: {book.title} by {book.author}")
                
                db.session.commit()
                print("Database seeding completed successfully!")
        
        except Exception as e:
            print(f"Error seeding database: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    seed_database()
