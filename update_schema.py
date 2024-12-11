"""
Script to manually update the SQLite database schema.
"""

import sqlite3

# Path to your SQLite database
db_path = 'app.db'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Rename the existing table
cursor.execute('ALTER TABLE book RENAME TO book_old;')

# 2. Create the new table with updated schema
cursor.execute('''
CREATE TABLE book (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  category TEXT NOT NULL,
  language TEXT NOT NULL,
  description TEXT,
  publisher TEXT,
  isbn TEXT,
  publish_date TEXT,
  pages INTEGER,
  rating REAL,
  reviews_count INTEGER,
  file_path TEXT NOT NULL,
  image_path TEXT,
  top_downloads INTEGER,
  most_discussed INTEGER
);
''')

# 3. Copy data from old table to new table
cursor.execute('''
INSERT INTO book (
  id, title, author, category, language, description, publisher,
  isbn, publish_date, pages, rating, reviews_count, file_path,
  image_path, top_downloads, most_discussed
)
SELECT
  id, title, author, category, language, description, publisher,
  isbn, publish_date, pages, rating, reviews_count, file_path,
  image_path, top_downloads, most_discussed
FROM book_old;
''')

# 4. Drop the old table
cursor.execute('DROP TABLE book_old;')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database schema updated successfully!") 