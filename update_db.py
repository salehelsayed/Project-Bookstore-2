from app import create_app
from app.db import db

app = create_app()

with app.app_context():
    # Drop all tables and recreate them with the new schema
    db.drop_all()
    db.create_all()
    print("Database schema updated successfully!")
