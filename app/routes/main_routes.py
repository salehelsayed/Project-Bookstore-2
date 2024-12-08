"""
Main route handlers for the bookstore application.
"""
from flask import Blueprint, render_template
from app.models import Book
from app.db import db

main = Blueprint('main', __name__)

@main.route('/books')
def list_books():
    """List all books in the library."""
    books = Book.query.all()
    return render_template('main.html', books=books)
