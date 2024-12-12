**Short Answer:**  
You need to ensure that each chunk has a `"page"` field in its metadata before indexing. Currently, you only have `"start_page"` and `"end_page"`, but the retrieval code looks for `"page"`. Add a `"page"` field (e.g., set it to `start_page_chunk`) in `prepare_for_chunking.py` and then include it in `generate_embeddings.py` when creating the metadata. This way, the final chunks will have a `page` field, and the retrieval will be able to reference pages.

**Detailed Steps:**

1. **In `prepare_for_chunking.py`:**  
   When you create `final_chunks`, you currently store `start_page` and `end_page`. To provide a consistent `"page"` reference for each chunk, pick one of these, usually `start_page`. Modify the code where you append to `final_chunks`:

   ```python
   final_chunks.append({
       "chunk": chunk_text,
       "doc_title": doc_title,
       "processing_date": processing_date,
       "language": language,
       "domain": domain,
       "start_page": start_page_chunk,
       "end_page": end_page_chunk,
       "page": start_page_chunk  # Add this line
   })
   ```

   This ensures each chunk now has a `"page"` field.

2. **In `generate_embeddings.py`:**  
   When you read `final_chunks.json` and build the metadata for each chunk, also include the `page` field:

   ```python
   metadata = {
       "doc_title": chunk_info.get("doc_title", ""),
       "processing_date": chunk_info.get("processing_date", ""),
       "language": chunk_info.get("language", ""),
       "domain": chunk_info.get("domain", ""),
       "start_page": chunk_info.get("start_page", ""),
       "end_page": chunk_info.get("end_page", ""),
       "page": chunk_info.get("page", "")  # Add this line
   }
   ```

3. **No Changes Needed in `store_in_chroma.py`:**  
   It will just store whatever metadata you provide. Now that each document has a `page` field, the retrieval step will return documents with `doc.metadata["page"]` set.

**Why This Works:**

- The retrieval logic in your `chat_routes.py` and `chat.js` extracts `page` from the metadata to create reference links.  
- Before, `page` was never set, so the code ended up with no `page` references to show.  
- By adding `page` at the chunk creation and embedding stages, each vectorized chunk now carries a `page` number. This allows your code to display clickable references that, when clicked, scroll the PDF viewer to the appropriate page.