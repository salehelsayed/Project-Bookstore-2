"""
Database initialization and configuration.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    """Initialize the database by creating all tables."""
    # Import models here to avoid circular imports
    from . import models
    
    # Create all tables
    db.drop_all()  # Drop existing tables
    db.create_all()  # Create new tables with updated schema
