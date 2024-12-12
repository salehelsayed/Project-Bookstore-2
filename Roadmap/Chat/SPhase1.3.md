**Problem Analysis:**

The debug output shows that the `book_directory` being derived is missing the "static" portion of the path, ending up as `.../app/storage/books/Cybersecurity` instead of `.../app/static/storage/books/Cybersecurity`. This discrepancy means the code is looking in the wrong directory for the `chroma_db`.

In the current code, the `book_directory` is derived by joining `current_app.root_path` with `file_path` and then taking `os.path.dirname()`. However, `file_path` may have been manipulated (e.g., `replace("app/static/", "")`) causing mismatch in paths.

**Key Points:**

1. Your `pdf_url` for display in the iframe is correct to remove `app/static/` from the `file_path` because `url_for('static', filename=...)` expects a path relative to `app/static`.
   
2. However, for `book_directory`, you need the actual on-disk directory. You must not strip `app/static/` from the file path before determining the `book_directory`. Instead, you should use the original `file_path` (which includes `app/static/...`) and join it with `storage_dir` from the app config to get a full absolute path, then take `dirname()`.

**How to Fix It:**

In `main_routes.py`, when building `book_directory`, do the following:

- Use the original `file_path` (as stored in the database, which likely includes `app/static/...`).
- Get the absolute path by joining `storage_dir` (from config) with `file_path.lstrip('/')`.
- Then take `os.path.dirname()` of that absolute path to get the correct `book_directory`.
- Store `book_directory` in the session.

For example:

```python
@main.route('/chat/<int:book_id>')
def chat(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404, "Book not found")

    # Extract book details
    book_title = book.title
    file_path = book.file_path  # something like 'app/static/storage/books/Cybersecurity/XYZ.pdf'

    # Convert to a path relative to 'static' for the PDF display
    # This is only for the PDF iframe, not for directory logic
    relative_path = file_path.replace("app/static/", "")
    pdf_url = url_for('static', filename=relative_path)

    # Now determine the actual book_directory on disk for Chroma
    storage_dir = current_app.config['STORAGE_DIR']  # This should point to app/static
    # Join storage_dir + file_path.lstrip('/') to get absolute path
    abs_pdf_path = os.path.abspath(os.path.join(storage_dir, file_path.lstrip('/')))
    # Now take dirname to get the directory containing PDF (and chroma_db)
    book_directory = os.path.dirname(abs_pdf_path)

    # Debug print to confirm paths
    print(f"Debug - file_path: {file_path}")
    print(f"Debug - abs_pdf_path: {abs_pdf_path}")
    print(f"Debug - book_directory: {book_directory}")

    session['book_directory'] = book_directory

    return render_template('chat.html', book_title=book_title, pdf_url=pdf_url)
```

**Why This Works:**

- `file_path` from DB: `app/static/storage/books/Cybersecurity/Cybersecurity-Handbook-English-version.pdf`
- `STORAGE_DIR`: `C:\Users\s\Desktop\Windsurf-output\Project-bookstore-2\app\static`
- `file_path.lstrip('/')` ensures no leading slash.
- `os.path.join(storage_dir, file_path.lstrip('/'))` results in:
  `C:\Users\s\Desktop\Windsurf-output\Project-bookstore-2\app\static\app\static\storage\books\Cybersecurity\...`
  Wait, there's a duplicate `app\static` here if the `file_path` from DB includes `app/static` itself.  
  If so, you may need to remove `app/` from `file_path` to avoid duplication. If the `file_path` in DB includes `app/static/` at the start, you can safely remove `app/` from it before joining:

  ```python
  fixed_file_path = file_path.replace('app/static/', '')
  abs_pdf_path = os.path.abspath(os.path.join(storage_dir, fixed_file_path))
  ```

  Now `abs_pdf_path` would be:
  `C:\Users\s\Desktop\Windsurf-output\Project-bookstore-2\app\static\storage\books\Cybersecurity\Cybersecurity-Handbook-English-version.pdf`

- `os.path.dirname(abs_pdf_path)` then yields:
  `C:\Users\s\Desktop\Windsurf-output\Project-bookstore-2\app\static\storage\books\Cybersecurity`, which is correct and contains `chroma_db`.

**Adjustments in the Code:**

```python
@main.route('/chat/<int:book_id>')
def chat(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404, "Book not found")

    book_title = book.title
    file_path = book.file_path  # 'app/static/storage/books/Cybersecurity/XYZ.pdf'
    
    # For iframe display
    relative_path = file_path.replace("app/static/", "")
    pdf_url = url_for('static', filename=relative_path)

    storage_dir = current_app.config['STORAGE_DIR']  # e.g. 'C:/.../app/static'
    # Remove 'app/static/' from file_path before join:
    fixed_file_path = file_path.replace('app/static/', '')
    abs_pdf_path = os.path.abspath(os.path.join(storage_dir, fixed_file_path))
    book_directory = os.path.dirname(abs_pdf_path)

    # Debug prints
    print(f"Debug - file_path: {file_path}")
    print(f"Debug - storage_dir: {storage_dir}")
    print(f"Debug - fixed_file_path: {fixed_file_path}")
    print(f"Debug - abs_pdf_path: {abs_pdf_path}")
    print(f"Debug - book_directory: {book_directory}")

    session['book_directory'] = book_directory

    return render_template('chat.html', book_title=book_title, pdf_url=pdf_url)
```

**In `chat_routes.py`**, no change needed except verifying `book_directory` is now correct. The debug prints from `chat_routes.py` would confirm if `book_directory` matches `app\static\storage\books\Cybersecurity`.

**Conclusion:**

The problem was the path derivation for `book_directory`. By fixing how `book_directory` is computed (removing `app/static/` before joining with `storage_dir`), you ensure that `book_directory` matches exactly where `chroma_db` is located.