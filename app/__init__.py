"""
Digital Bookstore application package.
"""
from flask import Flask
from dotenv import load_dotenv, find_dotenv
import os

# Find and load the .env file
print("Debug - Current working directory:", os.getcwd())
dotenv_path = find_dotenv(raise_error_if_not_found=True)
print(f"Debug - Found .env at: {dotenv_path}")

# Load environment variables with the found path
success = load_dotenv(dotenv_path=dotenv_path, verbose=True, override=True)
print(f"Debug - Load_dotenv success: {success}")
print(f"Debug - Environment after loading:")
print(f"Debug - OPENAI_API_KEY exists: {'OPENAI_API_KEY' in os.environ}")
print(f"Debug - All environment variables:", list(os.environ.keys()))

from app.db import db, init_db
from app.routes.main_routes import main
from app.routes.chat_routes import chat_bp
from config import STORAGE_DIR
import openai

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
    app.config['STORAGE_DIR'] = STORAGE_DIR
    
    # Set OpenAI API key
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    print(f"Debug - First 10 chars of API key: {openai_api_key[:10]}")
    
    # Ensure we're not using a default or placeholder value
    if openai_api_key.startswith('your-api'):
        raise ValueError("Invalid API key detected: using placeholder value")
        
    app.config['OPENAI_API_KEY'] = openai_api_key
    openai.api_key = openai_api_key  # Set it globally for the openai package
    
    # Initialize extensions
    db.init_app(app)
    
    # Ensure the instance folder exists
    with app.app_context():
        init_db()
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(chat_bp)
    
    return app
