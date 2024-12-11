Below are the modifications and instructions focused on switching the chat column to the middle, placing the PDF viewer on the right, and adding a draggable resizer between them. This builds upon the previous code, adjusting layout and adding a resizable divider.

---

### Updated Layout Requirements

**Old Layout:**  
**(Sidebar | PDF Viewer | Chat)**

**New Layout:**  
**(Sidebar | Chat Window | PDF Viewer)**

- The sidebar remains on the left, fixed width.
- The chat window is now in the middle and can have a flexible width.
- The PDF viewer is on the right side.
- A vertical resizer (a draggable bar) between the chat and the PDF viewer allows the user to adjust widths.

### Step-by-Step Developer Plan

#### 1. Adjusting `chat.html`

**Goal:** Reorder columns and add a resizer handle.

**Key Changes:**
- The order of columns will now be: Sidebar, Chat, Resizer, PDF Viewer.
- Insert a `div` with a class like `vertical-resizer` between the chat and PDF viewer.

**Example `chat.html`:**
```html
{% extends "base.html" %}
{% block content %}
<div class="chat-container">
  <!-- Sidebar (Left) -->
  <div class="sidebar">
    <h2>{{ book_title }}</h2>
    <button class="toggle-sidebar">Hide Sidebar</button>
  </div>

  <!-- Chat (Middle) -->
  <div class="chat-window">
    <div class="messages" id="messages"></div>
    <form class="chat-input-form">
      <input type="text" name="user_query" class="chat-input" placeholder="Ask any question...">
      <button type="submit" class="chat-send-btn">Send</button>
    </form>
  </div>

  <!-- Vertical Resizer -->
  <div class="vertical-resizer" id="vertical-resizer"></div>

  <!-- PDF Viewer (Right) -->
  <div class="pdf-viewer">
    <!-- PDF embedding logic will be added later -->
    <iframe src="{{ pdf_url }}#view=Fit" class="pdf-iframe"></iframe>
  </div>
</div>
{% endblock %}
```

**Explanation:**
- `.sidebar` on the left.
- `.chat-window` in the center.
- `.vertical-resizer` as a small vertical bar between `.chat-window` and `.pdf-viewer`.
- `.pdf-viewer` on the right.

#### 2. Updating `chat.css`

**Goal:** Use a flex layout that allows flexible widths and incorporate the resizer. The `.vertical-resizer` will appear as a vertical bar that the user can click and drag.

**Example `chat.css`:**
```css
.chat-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 250px;
  border-right: 1px solid #E2E8F0;
  padding: 16px;
  overflow-y: auto;
}

.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-right: 1px solid #E2E8F0;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.chat-input-form {
  display: flex;
  padding: 8px;
  border-top: 1px solid #E2E8F0;
}

.chat-input {
  flex: 1;
  padding: 8px;
  margin-right: 8px;
  border: 1px solid #CBD5E0;
  border-radius: 4px;
}

.chat-send-btn {
  background: #3182CE;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
}

/* Vertical Resizer */
.vertical-resizer {
  width: 5px;
  cursor: col-resize;
  background: #CBD5E0;
  /* Indicates draggable area */
}

.pdf-viewer {
  width: 400px; /* Initial width */
  position: relative;
  overflow: hidden;
}

.pdf-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .chat-container {
    flex-direction: column;
  }
  .sidebar, .chat-window, .vertical-resizer, .pdf-viewer {
    width: 100%;
    height: auto;
  }
}
```

**Explanation:**
- `.chat-container` is a flex container.  
- `.chat-window` flexes to fill available space between the fixed-width sidebar and PDF viewer.  
- `.vertical-resizer` is a draggable area.  
- `.pdf-viewer` starts with a fixed width (e.g., 400px). The user can drag the resizer to adjust.

#### 3. Implementing the Resizer Logic in JavaScript

**Goal:** Allow the user to click and drag the `.vertical-resizer` to adjust the `.pdf-viewer` width. We can put this logic in `chat.js`.

**Example `chat.js`:**
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const resizer = document.getElementById('vertical-resizer');
  const pdfViewer = document.querySelector('.pdf-viewer');
  const chatWindow = document.querySelector('.chat-window');

  let isResizing = false;
  let startX = 0;
  let startWidth = 0;

  resizer.addEventListener('mousedown', (e) => {
    isResizing = true;
    startX = e.clientX;
    startWidth = pdfViewer.offsetWidth;
    document.body.style.cursor = 'col-resize';
  });

  document.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    const dx = e.clientX - startX;
    const newWidth = startWidth - dx; // since we want to reduce pdfViewer width if we move left
    if (newWidth > 200 && newWidth < 800) { // Just bounds for sanity
      pdfViewer.style.width = newWidth + 'px';
    }
  });

  document.addEventListener('mouseup', () => {
    isResizing = false;
    document.body.style.cursor = 'default';
  });
});
```

**Explanation:**
- On `mousedown` on the resizer, record initial positions.
- On `mousemove`, adjust `pdfViewer` width dynamically.
- On `mouseup`, stop resizing.

#### 4. Connecting the "Chat" Button to the Book

In `main.html`, modify the “Chat” button so it links to `url_for('main.chat', book_id=book.id)`:

```html
<div class="book-card-footer">
  <button class="btn chat-btn" onclick="window.location.href='{{ url_for('main.chat', book_id=book.id) }}'">Chat</button>
  <a href="{{ url_for('main.download_book', book_id=book.id) }}" class="btn download-btn">Download</a>
</div>
```

In `main_routes.py`, ensure you have a `@main.route('/chat/<int:book_id>')` that sets `book_title`, `pdf_url`, etc., as previously described. No changes needed here beyond verifying that this route returns `chat.html`.

---

### Summary of Changes

1. **`chat.html` & `chat.css`:**  
   Reorder columns: Sidebar | Chat | Resizer | PDF.  
   Use a vertical resizer div.  
   Adjust CSS for a flex layout that supports resizing.

2. **Resizer Logic in `chat.js`:**  
   Add simple JS code to handle `mousedown`, `mousemove`, `mouseup` on `.vertical-resizer` to dynamically change PDF viewer width.

3. **"Chat" Button Routing:**  
   Ensure “Chat” button in `main.html` redirects to `GET /chat/<book_id>`, which displays `chat.html` for the chosen book.

With these steps, the chat column is now in the middle, the PDF viewer is on the right, and the user can drag a handle to adjust sizes, all while maintaining the previously described chat functionality.