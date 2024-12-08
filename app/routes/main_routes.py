"""
Main route handlers for the bookstore application.

This module handles the main routes for the bookstore application, including:
- Homepage with book listing and search functionality
- Book data retrieval and filtering
- Database seeding from CSV data
"""
import csv
from flask import Blueprint, render_template, request
from app.models import Book
from app.db import db
import os

main = Blueprint('main', __name__)

def seed_database():
    """
    Seed the database with initial book data from books_data.csv.
    This function is called when the application starts if the database is empty.
    """
    if Book.query.first() is None:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
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
                        path=row['file_path'],
                        cover_path=row['image_path'],
                        rating=float(row['rating']),
                        reviews_count=int(row['reviews_count'])
                    )
                    db.session.add(book)
                db.session.commit()

@main.route('/')
def home():
    """
    Display the homepage with initial book listing and filters.
    
    The homepage shows a grid of books with search functionality.
    Books can be filtered by:
    - Search query (matches title or author)
    - Category
    - Language
    
    Returns:
        Rendered template with books and filter options
    """
    # Initialize database if empty
    seed_database()
    
    # Get query parameters
    search_query = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of books per page
    
    # Build query
    query = Book.query
    
    if search_query:
        query = query.filter(
            (Book.title.ilike(f'%{search_query}%')) |
            (Book.author.ilike(f'%{search_query}%'))
        )
    
    # Execute query with pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    books = pagination.items
    
    # Server-side check for cover images
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    
    for book in books:
        if book.cover_path:
            # Ensure the cover_path doesn't start with 'static/'
            if book.cover_path.startswith('static/'):
                book.cover_path = book.cover_path[7:]  # Remove 'static/' prefix
            
            # Check if file exists
            cover_fullpath = os.path.join(static_dir, book.cover_path)
            if not os.path.isfile(cover_fullpath):
                book.cover_path = None
    
    return render_template('main.html',
                         books=books,
                         search_query=search_query,
                         current_page=page,
                         total_pages=pagination.pages)

@main.route('/books')
def list_books():
    """List all books in the library."""
    books = Book.query.all()
    return render_template('main.html', books=books)
