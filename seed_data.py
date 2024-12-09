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
    """
    Seed the database with initial book data from books_data.csv.
    This function is called when the application starts if the database is empty.
    """
    if Book.query.first() is None:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                               'data', 'books_data.csv')
        
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    book = Book(
                        title=row['title'],
                        author=row['author'],
                        category=row['category'],
                        language=row['language'],
                        description=row['description'],
                        file_path=row['file_path'],
                        image_path=row['image_path'],
                        rating=float(row['rating']) if row['rating'] else None,
                        reviews_count=int(row['reviews_count']) if row['reviews_count'] else 0
                    )
                    db.session.add(book)
                db.session.commit()

if __name__ == '__main__':
    seed_database()
