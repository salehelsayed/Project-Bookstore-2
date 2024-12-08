"""
Database configuration and initialization module.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    """Initialize the database and create all tables."""
    from . import models
    db.create_all()
