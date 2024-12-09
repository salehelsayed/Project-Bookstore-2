import sqlite3
import csv

# Path to your SQLite database
db_path = 'app.db'

# Path to your CSV file
csv_path = 'data/books_data.csv'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Open the CSV file
with open(csv_path, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)  # Skip the header row
    for row in csvreader:
        # Replace empty strings with None (NULL in SQLite)
        row = [None if field == '' else field for field in row]
        cursor.execute('''
            INSERT INTO book (
                id, title, author, category, language, description, publisher, isbn,
                publish_date, pages, rating, reviews_count, file_path, image_path,
                top_downloads, most_discussed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', row)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data imported successfully!")
