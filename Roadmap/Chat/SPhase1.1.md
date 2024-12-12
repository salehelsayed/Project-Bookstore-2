Below are step-by-step instructions for the developer on how to integrate the Chroma vector database retrieval and OpenAI LLM interaction dynamically based on the user’s chosen PDF/book. This involves creating `chroma_utils.py` and `openai_utils.py` services, adapting the `chat_routes.py` endpoint, and ensuring the chosen PDF/book’s directory determines the `chroma_db_path` and `collection_name`.

**High-Level Changes:**

1. **`chroma_utils.py`:**  
   - A function to initialize the Chroma vectorstore given a `book_directory` (where the PDF and `chroma_db` reside).  
   - Dynamically set `collection_name` to be the last directory name of `book_directory`.  
   - Return a `retriever` or `qa` chain ready to answer queries.

2. **`openai_utils.py`:**  
   - A function `get_chat_response(message, retriever)` that uses LangChain’s RetrievalQA or a similar chain to get responses from the LLM based on retrieved chunks.
   - Remove hardcoded logic and allow the function to use the provided retriever.

3. **`chat_routes.py`:**  
   - Modify the `/chat` POST endpoint to retrieve the correct `book_directory` and thus `retriever` from the session or request context.  
   - Pass the `retriever` to `get_chat_response()` so each user query is answered in context of that book’s embeddings.

**Detailed Instructions:**

### 1. Determining `book_directory` and Storing It

When the user navigates to `/chat/<book_id>` (in `main_routes.py` or wherever you define the chat page route), you already retrieve the `book_title` and `pdf_url`. You also know the `file_path` from the database for the chosen book. From `file_path`, derive `book_directory`:

```python
# Example in main_routes.py or a similar route file
book = Book.query.get(book_id)
file_path = book.file_path  # e.g., "app/static/storage/books/Cybersecurity/Cybersecurity-Handbook-English-version.pdf"
book_directory = os.path.dirname(file_path)  # e.g. "app/static/storage/books/Cybersecurity"
```

Store `book_directory` in the user’s session or pass it as a hidden field in the chat page. For simplicity, assume you store it in session:

```python
from flask import session
session['book_directory'] = book_directory
```

This ensures when the user sends messages to `/chat`, you know which directory to use.

### 2. Creating `chroma_utils.py`

**`chroma_utils.py`** (in `app/services/chroma_utils.py`):

```python
import os
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, text: str):
        return self.model.encode([text])[0].tolist()

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

def get_retriever_for_book(book_directory: str):
    """
    Given a book_directory (where PDF and chroma_db are located), return a retriever (or QA chain) for that book.
    """
    # chroma_db_path is always book_directory/chroma_db
    chroma_db_path = os.path.join(book_directory, "chroma_db")

    # Collection name is the last directory name
    collection_name = os.path.basename(book_directory)

    embeddings = SentenceTransformerEmbeddings()

    vectorstore = Chroma(
        collection_name=collection_name,
        persist_directory=chroma_db_path,
        embedding_function=embeddings
    )

    # Define the prompt template
    template = """You are a helpful assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say so.

Context:
{context}

Question: {question}
"""
    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

    # Build the QA chain
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa
```

This function `get_retriever_for_book` returns a `qa` chain that can be used to invoke `qa.invoke({"query": message})`.

### 3. Updating `openai_utils.py`

**`openai_utils.py`** (in `app/services/openai_utils.py`):

```python
def get_chat_response(message: str, qa_chain):
    """
    Given a message (user query) and a qa_chain (RetrievalQA chain),
    return the LLM's answer.
    """
    response = qa_chain.invoke({"query": message})
    return response["result"]
```

Here, we remove any hardcoding and simply rely on the provided `qa_chain`.

### 4. Modifying `chat_routes.py`

Currently, `chat_routes.py` uses `get_chat_response(data['message'])` without context. Now we must:

- Retrieve `book_directory` from session.
- Call `get_retriever_for_book(book_directory)` from `chroma_utils.py`.
- Call `get_chat_response(message, qa_chain)` from `openai_utils.py`.

**`chat_routes.py`**:
```python
from flask import Blueprint, jsonify, request, session
from app.services.chroma_utils import get_retriever_for_book
from app.services.openai_utils import get_chat_response

chat = Blueprint('chat', __name__)

@chat.route('/chat', methods=['POST'])
def chat_endpoint():
    """Handle chat messages and return AI responses."""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    # Retrieve book_directory from session
    book_directory = session.get('book_directory')
    if not book_directory:
        return jsonify({'error': 'Book directory not found in session'}), 400

    # Get the QA chain for this book
    qa_chain = get_retriever_for_book(book_directory)

    # Get response using QA chain
    response = get_chat_response(data['message'], qa_chain)
    return jsonify({'response': response})
```

**Note:** Ensure that in `main_routes.py` (or wherever you render `chat.html`), you set `session['book_directory']` when the user lands on the `chat` page:

```python
@main.route('/chat/<int:book_id>')
def show_chat(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404, "Book not found")
    file_path = book.file_path
    book_directory = os.path.dirname(file_path)
    session['book_directory'] = book_directory

    # pdf_url calculation...
    return render_template('chat.html', book_title=book.title, pdf_url=pdf_url)
```

### 5. Result

Now, when the user is on `chat.html` and sends a message via `POST /chat`, the backend:

- Uses `book_directory` from the session to initialize the QA chain from `chroma_utils`.
- Retrieves the correct embeddings from `chroma_db` in `book_directory`.
- Passes user query plus retrieved context to the LLM in `get_chat_response`.
- Returns an answer grounded in that specific PDF’s vector store.

This allows multiple books to be supported dynamically. Each `chat.html` instance corresponds to a chosen book, and by setting `session['book_directory']` accordingly, you ensure the correct `chroma_db` and `collection_name` are used.

---

**In Summary:**
- `chroma_utils.py` contains logic to build a retrieval QA chain from the book’s `chroma_db`.
- `openai_utils.py` provides a `get_chat_response(message, qa_chain)` that uses the chain.
- `chat_routes.py` retrieves the correct `qa_chain` based on `book_directory` stored in `session`.
- `chat.html` and `chat.js` remain largely unchanged, only now the backend can answer queries about the chosen book’s PDF content.