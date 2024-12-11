Below are the steps and code changes you should implement to allow users to download the book’s PDF when clicking the "Download" button. This approach assumes:

- You have a `file_path` column in your `Book` model that stores the relative path to the book’s PDF.
- The PDF files are stored in a known directory on the server.
- You will create a new route to serve the file as a download.
- You will use `safe_join` to prevent directory traversal attacks.
- You will modify `main.html` to turn the "Download" button into a link or give it a URL that points to this new download route.

### Steps

1. **Add a Download Route in `main_routes.py`:**  
   You’ll create a new route, for example: `/book/<int:book_id>/download`. When a user visits this URL, it will:
   - Query the database for the book by `book_id`.
   - Use the `file_path` from the database to locate the PDF file.
   - Use `safe_join` to safely construct the full file path.
   - Return the file as a downloadable attachment using `send_file`.

2. **Ensure Your Files Are in a Known Directory:**  
   Decide where your PDFs live. For example, if they’re in `project_root/storage/books/...`, ensure `storage` is accessible and you know its absolute path. Adjust `safe_join` usage accordingly.

3. **Import Required Functions:**  
   From Flask, import `send_file` or `send_from_directory`. From `werkzeug.utils`, import `safe_join`.

4. **Modify the “Download” Button in `main.html`:**  
   Instead of a `<button>` with no event, turn it into a link (`<a>`) pointing to the new download route. For example:
   ```html
   <a href="{{ url_for('main.download_book', book_id=book.id) }}" class="btn download-btn">Download</a>
   ```
   
   This ensures that clicking the button leads to the `download_book` route.

### Example Code Changes

**In `main_routes.py`:**
```python
import os
from flask import Blueprint, render_template, request, abort, send_file, current_app, url_for
from werkzeug.utils import safe_join
from app.models import Book
from app.db import db

main = Blueprint('main', __name__)

@main.route('/book/<int:book_id>/download')
def download_book(book_id):
    # Get the book from the database
    book = Book.query.get(book_id)
    if not book:
        abort(404, "Book not found")
    
    # The file_path in the database might be something like "storage/books/Category/PDF_File.pdf"
    # Construct the absolute path using safe_join
    # Suppose your PDFs are in app.root_path (project root), adjust if needed
    pdf_path = safe_join(current_app.root_path, book.file_path)

    # Check if file exists
    if not os.path.isfile(pdf_path):
        abort(404, "File not found")

    # Return the file as an attachment
    return send_file(pdf_path, as_attachment=True, download_name=os.path.basename(pdf_path))
```

**In `main.html`:**
```html
<div class="book-card-footer">
    <!-- Instead of a <button>, use an <a> tag linking to the download route -->
    <a href="{{ url_for('main.download_book', book_id=book.id) }}" class="btn download-btn">
        Download
    </a>
</div>
```

### Explanation:

- **`safe_join`**: This function safely joins one or more path components to `current_app.root_path`, ensuring a malicious user can’t manipulate the URL to access files outside your intended directory.
- **`send_file`**: This Flask helper sends a file back to the client. The `as_attachment=True` parameter forces the browser to present a download dialog.
- **`download_name`**: Optionally specify a `download_name` (available in newer Flask versions) so the file will have a friendly filename in the user’s download prompt.

### Conclusion

By updating `main_routes.py` to provide a `/book/<int:book_id>/download` route and changing your “Download” button into a link that calls `url_for('main.download_book', book_id=book.id)`, you ensure that the user can download the PDF file corresponding to that book. Using `safe_join` and `send_file` ensures security and a proper download experience.