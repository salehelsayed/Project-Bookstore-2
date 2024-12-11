# 3- Generate Embeddings

**Current Script Description (`generate_embeddings.py`):**

This script reads the output produced by `prepare_for_chunking.py`—specifically `final_chunks.json`—from a specified directory and uses a local embedding model (from `sentence-transformers`) to convert each text chunk into a vector representation (an embedding). These embeddings capture the semantic meaning of the chunks, enabling downstream similarity-based retrieval tasks such as semantic search or Q&A.

**Key Features:**

1. **Directory-Based Input/Output:**
   Instead of passing individual file names, you provide a directory path that contains:
   - `final_chunks.json`: Produced by `prepare_for_chunking.py`, containing the processed text chunks.
   
   The script assumes `final_chunks.json` is present in the given directory and will generate `chroma_input.json` in the same directory as output.

2. **Local Embedding Generation with Sentence-Transformers:**
   The script relies on a pretrained Sentence-Transformers model (e.g., `all-MiniLM-L6-v2`) to produce embeddings locally. This avoids external API calls or service dependencies, keeping the process offline and self-contained.

3. **Token-Level Alignment via Sentence-Transformers:**
   Models like `all-MiniLM-L6-v2` are optimized for producing high-quality sentence embeddings. By using these models, your chunks—already aligned to language model token boundaries—are now mapped into a semantic vector space efficiently and accurately.

4. **Progress Bar for User Feedback:**
   The embedding generation step can be time-consuming for large documents. Enabling `show_progress_bar=True` when calling `model.encode()` displays a progress bar, providing real-time feedback on how many embeddings have been processed.

5. **Preparing Data for Chroma:**
   After generating embeddings, the script converts them to a JSON-serializable format and stores:
   - `documents`: The chunk texts from `final_chunks.json`
   - `metadatas`: Their associated document-level metadata
   - `ids`: Unique identifiers for each chunk
   - `embeddings`: The numerical vectors themselves

   This collection of data is saved as `chroma_input.json`, which can be later provided to `store_in_chroma.py` (or similar) for insertion into a vector database like Chroma.

**Installation Notes:**
- `sentence-transformers`: `pip install sentence-transformers`
- Model downloads automatically on first run if you have internet access.
- Once downloaded, no further external calls are needed.

**Usage:**
```bash
python -m app.services.generate_embeddings "path/to/directory"
```

Where `directory` contains:
- `final_chunks.json` (produced by `prepare_for_chunking.py`)

**How It Works Internally:**

1. **Loading Final Chunks:**
   The script reads `final_chunks.json` and extracts `documents`, `metadatas`, and `ids` from the chunk information.

2. **Embedding Generation:**
   Using a Sentence-Transformers model, it encodes each chunk text into an embedding. The progress bar displays how many documents have been processed, ensuring transparency and user feedback.

3. **JSON Output for Downstream Steps:**
   After embeddings are computed, the script compiles all data (chunks, metadata, ids, and embeddings) into `chroma_input.json`. This file is a ready-to-use package of data for inserting into a vector database.

**What to Expect as Output:**
After running `generate_embeddings.py`, you get `chroma_input.json` in the same directory. It contains fields:

```json
{
  "documents": [...],
  "metadatas": [...],
  "ids": [...],
  "embeddings": [[...], [...], ...]
}
```

These arrays correspond to each chunk’s text, metadata, IDs, and embeddings, respectively. The embeddings are stored as lists of floats, making them easily ingestible by Chroma or other vector databases.

**Next Steps:**
- Provide `chroma_input.json` to `store_in_chroma.py` (or a similar script) to insert the embeddings and their associated data into a vector database.
- After indexing, your system can efficiently retrieve the most relevant chunks for a user’s query.
- Finally, integrate a Q&A chain with an LLM to answer user questions using these retrieved chunks as context.

**Summary:**
`generate_embeddings.py` takes the chunks prepared by `prepare_for_chunking.py` and turns them into semantic embeddings using a local Sentence-Transformers model. With progress indication, local processing, and a clear output format, it bridges the gap between raw text chunks and a vector database-ready data package, setting the stage for semantic search and Q&A capabilities.