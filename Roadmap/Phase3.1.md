# Phase 3.1: Implement Filter Sidebar on Homepage

**Summary of Actions:**

- **Update `main.html`**: Incorporate the HTML code for the filter component as shown in Phase3.1.md. **[+]**

- **Create/Modify `filters.css`**: Add the CSS styles to style the filter component, ensuring it matches the aesthetic of your application. **[+]**

- **Modify `main_routes.py`**: Update the route handling to accept and process the filter parameters (language and rating) from the GET request when the "Apply Filters" button is pressed. **[+]**

- **Ensure `Book` Model Supports Filtering**: Verify that the `Book` model has the necessary fields and that you can query books based on `language` and `rating`. **[+]**

Below is a refined approach that incorporates your requests:

- Use simpler, well-known terms for the filters:  
  - **Language** remains the same (clear and universal). **[+]**
  - **Rating** remains the same (users understand star ratings). **[+]**
  - **Most Downloaded** → **Top Downloads** (communicates popularity by download count). **[+]**
  - **Most Chatted** → **Most Discussed** (communicates popularity by how much it’s talked about). **[+]**

- Only **Language** and **Rating** will be included in the "Apply Filters" request for now, since you haven’t implemented **Top Downloads** and **Most Discussed** in the database yet. **[+]**
  
- Make the **"Apply Filters"** button use the same accent color as your brand color (assuming the blue used for other UI elements) and add a subtle shadow to the filter card for a cleaner, modern look. **[+]**

### Example Implementation

**HTML (within `main.html`):**
```jinja2
<div class="filter-column">
    <div class="filter-card">
        <h3 class="filter-title">Filters</h3>

        <!-- Language Filter -->
        <div class="filter-section">
            <label for="language-select" class="filter-label">Language</label>
            <select id="language-select" name="language" class="filter-select">
                <option value="">All Languages</option>
                <option value="en">English</option>
                <option value="fr">French</option>
                <!-- Add more languages as needed -->
            </select>
        </div>

        <!-- Rating Filter -->
        <div class="filter-section">
            <span class="filter-label">Rating</span>
            <label class="rating-option">
                <input type="radio" name="rating" value="5">
                <span class="stars">★★★★★</span>
            </label>
            <label class="rating-option">
                <input type="radio" name="rating" value="4">
                <span class="stars">★★★★☆</span>
            </label>
            <label class="rating-option">
                <input type="radio" name="rating" value="3">
                <span class="stars">★★★☆☆</span>
            </label>
        </div>

        <!-- Future Filters (Top Downloads, Most Discussed) -->
        <!-- Not implemented yet, so no name attribute and not included in form submission -->
        <div class="filter-section future-filters">
            <span class="filter-label">Additional Filters</span>
            <div class="disabled-filter">
                <span class="filter-name">Top Downloads (Coming Soon)</span>
            </div>
            <div class="disabled-filter">
                <span class="filter-name">Most Discussed (Coming Soon)</span>
            </div>
        </div>

        <!-- Apply Filters Button -->
        <!-- Wrap the filters in a form to submit language and rating -->
        <form action="{{ url_for('main.home') }}" method="GET" class="apply-filters-form">
            <!-- Hidden fields to preserve search or other params if necessary -->
            {% if search_query %}
            <input type="hidden" name="search" value="{{ search_query }}">
            {% endif %}

            <button type="submit" class="btn apply-filters-btn" aria-label="Apply Filters">Apply Filters</button>
        </form>
    </div>
</div>
```

**CSS (e.g., in `filters.css`):**
```css
.filter-column {
    width: 250px;
    padding: 16px;
    box-sizing: border-box;
}

.filter-card {
    background: #fff;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* subtle shadow */
    padding: 16px;
}

.filter-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 12px;
    border-bottom: 1px solid #E2E8F0;
    padding-bottom: 8px;
}

.filter-section {
    margin-bottom: 16px;
}

.filter-label {
    display: block;
    margin-bottom: 8px;
    font-size: 14px;
    font-weight: 500;
    color: #2D3748; /* Dark gray for text */
}

.filter-select {
    width: 100%;
    padding: 8px;
    border: 1px solid #CBD5E0;
    border-radius: 4px;
    font-size: 14px;
    color: #2D3748;
}

.rating-option {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
}

.rating-option input[type=radio] {
    margin-right: 8px;
}

.stars {
    font-size: 14px;
    color: #FFD700; /* Gold for stars */
}

.future-filters .disabled-filter {
    color: #A0AEC0; /* Gray text, indicating not active */
    font-size: 14px;
    margin-bottom: 8px;
}

.apply-filters-form {
    margin-top: 20px;
    text-align: center;
}

.apply-filters-btn {
    background-color: #3182CE; /* Same accent blue as the rest of the UI */
    color: #fff;
    font-size: 14px;
    font-weight: 500;
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
    text-align: center;
}

.apply-filters-btn:hover {
    background-color: #2C5282;
}

.apply-filters-btn:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(49,130,206,0.4);
}
```

### Explanation

- **Unified Color and Aesthetics:**  
  The "Apply Filters" button now matches the accent blue color used across your UI elements. This ensures consistency and a cohesive brand feeling. **[+]**
  
- **Future Filters (Top Downloads, Most Discussed):**  
  We’ve listed them as “Coming Soon” and grayed them out. Since they are not implemented, they have no `name` attribute and won’t be included in the GET request. They serve as a placeholder to inform users that more filters will be available later. **[+]**
  
- **User-Friendly Terminology:**  
  - “Language” and “Rating” are straightforward. **[+]**
  - “Top Downloads” and “Most Discussed” are simple, descriptive terms that convey their purpose. **[+]**

- **Simple UI with Clear Hierarchy:**  
  The card has a title (“Filters”), each filter category is labeled clearly, and the “Apply Filters” button stands out at the bottom. The subtle box shadow adds a touch of depth to the filter card, making it visually distinct from the background. **[+]**

**Result:**  
You get a cleaner, more intuitive filter panel with the currently functional filters (Language and Rating) clearly available and more advanced filtering options (Top Downloads, Most Discussed) foreshadowed without clutter or user confusion.