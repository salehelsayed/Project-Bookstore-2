# Bookstore Project

A Flask-based digital bookstore application with chat capabilities.

## Project Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
Project-bookstore-2/
  app/              # Main application code
  books/            # Book storage directory
  venv/             # Virtual environment
  app.db            # SQLite database
```

## How to Run

1. Ensure your virtual environment is activated
2. Set required environment variables (see DEVELOPER_NOTES.md)
3. Run the Flask application:
```bash
python app/main.py
```

The application will be available at `http://localhost:5000`
