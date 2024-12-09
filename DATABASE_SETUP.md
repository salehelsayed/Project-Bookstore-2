# Database Setup Guide

## Initial Setup

1. The database will be automatically created when the application first runs
2. Make sure you have write permissions in the project directory
3. The application uses SQLAlchemy ORM for database operations

## Database Schema

The main model is the `Book` model with the following fields:
- `id`: Primary key
- `title`: Book title (required)
- `author`: Book author (required)
- `category`: Book category (required)
- `language`: Book language (required)
- `description`: Book description (Text field, optional)
- `publisher`: Publisher name (optional)
- `isbn`: ISBN number (optional)
- `publish_date`: Publication date (optional)
- `pages`: Number of pages (optional)
- `path`: Path to book PDF file (stored as file_path in CSV)
- `cover_path`: Path to book cover image (stored as image_path in CSV)
- `rating`: Book rating (float, defaults to 0.0)
- `reviews_count`: Number of reviews (integer, defaults to 0)
- `created_at`: Timestamp of when the book was added (auto-generated)

## Project Structure

```
project_root/
├── app/
│   ├── routes/
│   │   ├── main_routes.py    # Main routes for book listing and search
│   │   └── chat_routes.py    # Chat functionality routes
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css     # Core styles
│   │   │   ├── cards.css    # Book card styles
│   │   │   ├── filters.css  # Filter sidebar styles
│   │   │   └── chat.css     # Chat interface styles
│   │   ├── js/             # JavaScript files
│   │   └── images/         # Image assets
│   └── templates/
│       ├── base.html       # Base template
│       ├── main.html       # Homepage template
│       └── chat.html       # Chat interface template
├── data/
│   └── books_data.csv      # Sample book data
└── app.db                  # SQLite database file
```

## Seeding Test Data

The application includes sample data in `data/books_data.csv`. The database is automatically seeded when:
1. The application starts
2. The database is empty (no existing books)

The seeding process:
- Reads data from books_data.csv
- Creates book records with all fields
- Handles data type conversions (e.g., string to float for ratings)
- Commits all records to the database

### Sample Data Format (books_data.csv)
The CSV file contains the following columns:
- title
- author
- category
- language
- description
- publisher
- isbn
- publish_date
- pages
- rating (float)
- reviews_count (integer)
- file_path (path to PDF file)
- image_path (path to cover image)

## Recreating the Database

To recreate the database:

1. Delete the existing `app.db` file
2. Restart the application
   - The database will be automatically created
   - Sample data will be seeded from books_data.csv

## Development Notes

- Using SQLite with SQLAlchemy ORM
- Automatic database seeding on startup
- CSV data stored in `data/books_data.csv`
- Enhanced error handling for:
  - Database connections
  - File operations
  - Data type conversions
  - Missing required fields

## Features Implemented

- Automatic database creation and seeding
- Book search functionality
- Category and language filtering
- Rating and review display
- Book cover image support
- Download functionality for PDF files
- Chat interface for book discussions
