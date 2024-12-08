# Developer Notes

## Directory Structure

- `app/`: Contains the main application code
  - `main.py`: Application entry point and configuration
  - `db.py`: Database configuration and utilities
  - `models.py`: SQLAlchemy models
  - `routes/`: Route handlers for different features
  - `services/`: Utility services for OpenAI and Chroma
  - `static/`: Static assets (CSS, JavaScript)
  - `templates/`: HTML templates

- `books/`: Storage for book files and metadata
  - Each book has its own directory with PDF, cover image, and vector store data
  
- `templates/`: Jinja2 templates for rendering pages
- `static/`: Static assets organized by type (css, js)

## Environment Variables

The following environment variables need to be set:
- `OPENAI_API_KEY`: Your OpenAI API key for chat functionality
- `FLASK_ENV`: Set to 'development' for development mode
- `SECRET_KEY`: Flask session secret key

Store these in a `.env` file (not committed to version control) or set them in your environment.

## Configuration

Main application configuration is handled in `app/main.py`. Any changes to app configuration should be made here.
