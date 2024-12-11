"""
Main entry point for the Bookstore application.
Initializes Flask app and configures all necessary extensions.
"""
from flask import Flask, render_template
from dotenv import load_dotenv
import os
from app.db import db, init_db
from app.routes.main_routes import main

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
    
    # Initialize extensions
    db.init_app(app)
    
    # Ensure the instance folder exists
    with app.app_context():
        init_db()
    
    # Register blueprints
    app.register_blueprint(main)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
