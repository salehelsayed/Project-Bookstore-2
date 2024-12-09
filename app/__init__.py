"""
Digital Bookstore application package.
"""
from flask import Flask
from dotenv import load_dotenv
import os
from app.db import db, init_db
from app.routes.main_routes import main
from config import STORAGE_DIR

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
    app.config['STORAGE_DIR'] = STORAGE_DIR
    
    # Initialize extensions
    db.init_app(app)
    
    # Ensure the instance folder exists
    with app.app_context():
        init_db()
    
    # Register blueprints
    app.register_blueprint(main)
    
    return app
