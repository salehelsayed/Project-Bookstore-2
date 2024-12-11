"""
Main route handlers for the bookstore application.

This module handles the main routes for the bookstore application, including:
- Homepage with book listing and search functionality
- Book data retrieval and filtering
- Database seeding from CSV data
"""
import csv
from flask import Blueprint, render_template, request, send_file, abort, current_app, url_for
from app.models import Book
from app.db import db
import os
from werkzeug.utils import safe_join

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
                        file_path=row['file_path'],
                        image_path=row['image_path'],
                        rating=float(row['rating']),
                        reviews_count=int(row['reviews_count'])
                    )
                    db.session.add(book)
                db.session.commit()

@main.route('/')
def home():
    """
    Display the homepage with book listings and filters.

    Supports filtering by:
    - Search query: Matches title or author.
    - Language: Filters books by selected language.
    - Rating: Filters books with a rating greater than or equal to the selected rating.

    Returns:
        Rendered HTML template for the homepage.
    """
    # Initialize database if empty
    seed_database()
    
    # Get query parameters
    search_query = request.args.get('search', '').strip()
    language = request.args.get('language', '').strip()
    rating = request.args.get('rating', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of books per page
    
    # Build query
    query = Book.query
    
    if search_query:
        query = query.filter(
            (Book.title.ilike(f'%{search_query}%')) |
            (Book.author.ilike(f'%{search_query}%'))
        )
    if language:
        # Filter books by the selected language
        query = query.filter(Book.language == language)
    if rating:
        # Filter books with a rating greater than or equal to the selected rating
        query = query.filter(Book.rating >= float(rating))

    # Execute query with pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    books = pagination.items
    
    # Server-side check for cover images
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    
    for book in books:
        if book.image_path:
            # Ensure the image_path doesn't start with 'static/'
            if book.image_path.startswith('static/'):
                book.image_path = book.image_path[7:]  # Remove 'static/' prefix
            
            # Check if file exists
            cover_fullpath = os.path.join(static_dir, book.image_path)
            if not os.path.isfile(cover_fullpath):
                book.image_path = None
    
    return render_template('main.html',
                         books=books,
                         search_query=search_query,
                         language=language,
                         rating=rating,
                         current_page=page,
                         total_pages=pagination.pages)

@main.route('/books')
def list_books():
    """List all books in the library."""
    books = Book.query.all()
    return render_template('main.html', books=books)

@main.route('/book/<int:book_id>/download')
def download_book(book_id):
    # Get the book from the database
    book = Book.query.get(book_id)
    if not book:
        abort(404, "Book not found")
    
    # Remove leading slashes from file path
    file_path = book.file_path.lstrip('/')
    
    # Get the storage directory from app config
    storage_dir = current_app.config['STORAGE_DIR']
    
    # Construct the absolute path to the PDF file
    pdf_path = safe_join(storage_dir, file_path)
    
    if pdf_path is None:
        abort(400, "Invalid file path")
    
    # Convert to absolute path
    pdf_path = os.path.abspath(pdf_path)
    
    # Print the path for debugging (remove in production)
    print(f"Attempting to access PDF at: {pdf_path}")
    
    # Check if the file exists
    if not os.path.isfile(pdf_path):
        abort(404, "File not found")
    
    # Return the file as an attachment
    return send_file(pdf_path, as_attachment=True, download_name=os.path.basename(pdf_path))

@main.route('/chat/<int:book_id>')
def chat(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404, "Book not found")

    # Extract book details
    book_title = book.title
    file_path = book.file_path
    relative_path = file_path.replace("app/static/", "")
    pdf_url = url_for('static', filename=relative_path)

    return render_template('chat.html', book_title=book_title, pdf_url=pdf_url)
