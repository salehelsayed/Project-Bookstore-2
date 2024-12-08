#### Phase 2: Basic Homepage & Data Loading

**Goal:** Display initial books on `/` following UI guidelines.

**Steps:**

1. **Add main_routes.py & main.html:**
    
    - `/` loads `main.html`, shows some static books.
    - In **DEVELOPER_NOTES.md**, mention that `main_routes.py` handles homepage logic.
    - In code docstrings, explain the route’s query logic.
2. **Templates & Static Assets Setup:**
    
    - Use `base.html`, `main.css`, `filters.css`, `cards.css`.
    - In **UI_GUIDE.md**, document class naming, styling rules, and layout approaches used in `main.html`.
    - In HTML comments, reference corresponding CSS classes as per **UI_GUIDE.md** guidelines.
3. **Load Sample Data into app.db:**
    
    - Insert sample books manually or via a simple script.
    - In **DATABASE_SETUP.md**, add instructions for this initial data seeding process.

**Documentation Status After Phase 2:**

- **UI_GUIDE.md**: Now explains basic styling conventions and references classes used in `main.html`.
- **DATABASE_SETUP.md**: Includes steps on how to seed initial data.

---

#### Mock Data Setup (Seeding the Database with Test Data)

**Goal:** Introduce a small `mock_data.csv` and a `seed_data.py` to test layout and downloading early.

**Steps:**

1. **MOCK_DATA_SETUP.md Creation:**
    - Add instructions for creating `mock_data.csv` and running `seed_data.py`.
    - Explain how to place a real PDF and cover image in `books/<book_id>/`.
2. **Test the Layout & Download:**
    - Run the app, confirm mock data and PDF download work.
    - If adjustments are needed, update **MOCK_DATA_SETUP.md** accordingly.

**Documentation Status After Mock Setup:**

- **MOCK_DATA_SETUP.md**: Details how to add mock data, run `seed_data.py`, and test the UI and download feature.

---
