# Database Setup Guide

## Initial Setup

1. The database will be automatically created when the application first runs
2. Make sure you have write permissions in the project directory

## Database Schema

The main model is the `Book` model with the following fields:
- id: Primary key
- title: Book title
- author: Book author
- category: Book category
- language: Book language
- description: Book description
- path: Path to book PDF file
- cover_path: Path to book cover image
- metadata_path: Path to additional metadata (optional)
- rating: Book rating (float)
- reviews_count: Number of reviews
- created_at: Timestamp of when the book was added

## Seeding Test Data

The application includes sample data in `data/books_data.csv`. To seed the database with this data:

1. Ensure the database exists (run the application once if it doesn't)
2. Run the seeding script:
   ```bash
   python seed_data.py
   ```
3. The script will:
   - Check if the database already contains books
   - If empty, load data from books_data.csv
   - Create book records with all necessary fields
   - Print progress as books are added

Note: The seeding script will skip if books already exist in the database.

## Recreating the Database

If you need to recreate the database:

1. Delete the existing `app.db` file
2. Run the application - it will create a new database automatically
3. Run `python seed_data.py` to populate with sample data

## Development Notes

- The database uses SQLite for simplicity
- Database migrations are not implemented in Phase 1
- All database operations are handled through SQLAlchemy ORM
- Sample data is stored in `data/books_data.csv` for consistency
- The seeding process is automated through `seed_data.py`
