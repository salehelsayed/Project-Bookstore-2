# 4- Store In Chroma

**Current Script Description (`store_in_chroma.py`):**

This script takes the output produced by `generate_embeddings.py`—specifically `chroma_input.json`—from a given directory and inserts its data into a Chroma vector database. By doing so, it sets the stage for efficient semantic retrieval, allowing you to later query the database with user questions and retrieve the most relevant chunks for context.

**Key Features:**

1. **Directory-Based Input & Output:**
   You provide a directory path that contains:
   - `chroma_input.json`: Produced by `generate_embeddings.py`, containing documents, metadata, IDs, and embeddings.
   
   The script expects this file to be present in the specified directory. It also uses a `chroma_db` folder within the same directory to store the Chroma database.

2. **Local Vector Database with Chroma:**
   The script uses Chroma’s Python client to create or load a persistent vector database inside the provided directory. This ensures that each directory (representing one book) maintains its own dedicated Chroma instance, fully local and self-contained.

3. **Batch Insertion with a Progress Bar:**
   To provide user feedback and handle large datasets gracefully, the script inserts embeddings in batches and displays a progress bar (via `tqdm`). This way, you can track the insertion progress in real-time.

4. **Overwriting Existing Database:**
   If a Chroma database (`chroma_db`) already exists in the directory, the script removes it first to ensure a clean slate. Running the script again overwrites the old database with the new data from `chroma_input.json`.

5. **Metadata & Document Retrieval:**
   Along with embeddings, the script stores documents and their metadata. This information can later be retrieved alongside embeddings, enabling enriched search results that are both semantically similar and contextually informative.

**Installation Notes:**
- `chromadb` library: `pip install chromadb`
- `tqdm` for progress bar: `pip install tqdm`
- Everything runs locally; no external services are required.

**Usage:**
```bash
python -m app.services.store_in_chroma "path/to/directory"
```

Where `directory` contains:
- `chroma_input.json` (produced by `generate_embeddings.py`)

**How It Works Internally:**

1. **Loading Chroma Input:**
   The script reads `chroma_input.json`, extracting arrays of documents, metadata, IDs, and embeddings.

2. **Preparing the Chroma Database:**
   It checks if a `chroma_db` folder already exists and deletes it to ensure a fresh database. It then initializes a `PersistentClient` pointing to this directory, creating a new Chroma vector database instance.

3. **Batch Insertion & Progress Monitoring:**
   The script inserts embeddings in batches of a set size (e.g., 100 documents per batch), updating the progress bar after each batch is processed. This provides a responsive and user-friendly experience.

4. **Ready for Semantic Retrieval:**
   Once data insertion is complete, the database is stored locally in `chroma_db`. This vector database can be queried by downstream steps—such as a retrieval pipeline integrated with a language model—to answer user queries with contextually relevant chunks.

**What to Expect as Output:**
After running `store_in_chroma.py`, you get a `chroma_db` folder inside your directory. This folder contains the persistent vector database files managed by Chroma. Your embeddings and associated documents/metadata are now indexed and ready for retrieval.

**Next Steps:**
- With embeddings stored in Chroma, you can implement a retrieval step that queries this database given a user’s question.
- After retrieving the top relevant chunks, pass them to an LLM’s Q&A chain to produce context-informed answers.
- This approach completes the pipeline—from raw PDF text to user-interactive semantic search and question answering.

**Summary:**
`store_in_chroma.py` takes the embedding data prepared by `generate_embeddings.py` and inserts it into a local Chroma database, ensuring quick and semantic-rich retrieval. With progress indication, local persistence, and isolated per-book databases, it sets the stage for sophisticated semantic querying and Q&A experiences grounded in the original PDF content.