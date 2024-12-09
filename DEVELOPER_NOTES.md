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

## Adding New Filters

To add a new filter to the application, follow these steps:

1. **Update the HTML Form:**

   - In `main.html`, add a new input element within the `filters-form`.
   - Assign a `name` attribute to the input that will be used as the query parameter in the backend.

2. **Update the JavaScript:**

   - No additional changes are needed if the input is within the `filters-form`.
   - The existing JavaScript will automatically pick up new form inputs.

3. **Update the Backend Route:**

   - In `main_routes.py`, update both the `home()` and `books()` routes.
   - Retrieve the new filter parameter using `request.args.get('parameter_name')`.
   - Add the necessary filtering logic to the SQLAlchemy query.

4. **Update the Templates:**

   - If the filter affects the display (e.g., showing new data), update `book_grid.html` accordingly.

5. **Testing:**

   - Verify that the filter works both with page reloads and with AJAX (dynamic updates).

## Example

For a new filter called "Category":

- **HTML:**
  ```html
  <div class="filter-section">
      <label for="category-select" class="filter-label">Category</label>
      <select id="category-select" name="category" class="filter-select">
          <option value="">All Categories</option>
          <option value="Programming">Programming</option>
          <!-- Add more categories -->
      </select>
  </div>
  ```

- **Backend:**
  ```python
  category = request.args.get('category', '').strip()
  if category:
      query = query.filter(Book.category == category)
  ```

---

By following these steps, you can seamlessly add new filters to the application.
