# Database Setup Guide

## Initial Setup

1. The database will be automatically created when the application first runs
2. Make sure you have write permissions in the project directory

## Database Schema

The main model is the `Book` model with the following fields:
- id: Primary key
- title: Book title
- author: Book author
- path: Path to book PDF file
- cover_path: Path to book cover image
- metadata_path: Path to additional metadata (optional)

## Recreating the Database

If you need to recreate the database:

1. Delete the existing `app.db` file
2. Run the application - it will create a new database automatically
3. Any existing book records will need to be re-added

## Development Notes

- The database uses SQLite for simplicity
- Database migrations are not implemented in Phase 1
- All database operations are handled through SQLAlchemy ORM
