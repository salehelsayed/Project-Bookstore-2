# 2- Prepare for Chunking

**Current Script Description (`prepare_for_chunking.py`):**

This script reads the standardized output files from `pdf_extractor.py`, specifically `extracted.txt` and `extracted_metadata.json`, both located in a given directory. It then transforms the extracted text into token-limited, sentence-based chunks with a configurable overlap. The chunking process uses `nltk` to split text into sentences and `tiktoken` to measure token counts, ensuring each chunk aligns well with language model tokenization.

**Key Features:**

1. **Input Directory:**  
   Instead of passing file names individually, you provide a directory path containing:
   - `extracted.txt`: One page of normalized text per line, produced by `pdf_extractor.py`.
   - `extracted_metadata.json`: Document-level metadata, also from `pdf_extractor.py`.

   The script assumes these standard file names are present in the specified directory.

2. **Sentence-Based Chunking with Overlap:**  
   Pages are read line-by-line, then `nltk.sent_tokenize()` splits each line’s text into sentences. By working at the sentence level, chunks become more semantically coherent. The script also introduces overlapping tokens between chunks, ensuring that contextual information near chunk boundaries is preserved.

3. **Token-Based Control with `tiktoken`:**  
   Each sentence’s length is measured in tokens using `tiktoken`. The script hardcodes `chunk_size` and `overlap` (e.g., `chunk_size = 500` tokens and `overlap = 50` tokens), making chunks consistently sized according to language model token standards. This improves compatibility with LLM embedding and retrieval steps.

4. **Hardcoded Parameters & No Per-Page Metadata:**  
   Currently, `chunk_size` and `overlap` are not passed as arguments; they are constants within the script. There is no `content_type` or other page-level metadata at this stage—only document-level metadata and page range references are included.

5. **Progress Bar for User Feedback:**  
   The script includes a progress bar (via `tqdm`) that updates as sentences are processed into chunks. This provides a clear indication of the script’s progress and performance when dealing with long documents.

6. **Minimal Document-Level Metadata and Page References:**  
   The final chunks reference `start_page` and `end_page` to indicate which pages contributed sentences to that chunk. Document-level metadata like `doc_title`, `processing_date`, `language`, and `domain` is preserved from the metadata file. This helps maintain traceability back to the source PDF without cluttering output with unused page-level fields.

**Installation Notes:**
- `nltk` for sentence tokenization. Ensure `punkt` is downloaded.
- `tiktoken` for token counting.
- `tqdm` for displaying a progress bar.
- Everything runs locally; no external APIs are required.

**Usage:**
```bash
python -m app.services.prepare_for_chunking "path/to/directory"
```

Where `directory` contains:
- `extracted.txt`
- `extracted_metadata.json`

**How It Works Internally:**

1. **Reading and Sentence Tokenizing Text:**
   The script reads all pages from `extracted.txt`, tokenizes each line into sentences, and combines all sentences from the entire document into a single list.

2. **Chunking with Overlap:**
   Using `tiktoken`, it measures each sentence’s length in tokens. Sentences are accumulated until reaching the `chunk_size` limit, then a chunk is finalized. The script then rewinds by `overlap` tokens (approximated by sentence boundaries) before starting the next chunk, preserving context at chunk edges.

3. **Metadata Integration:**
   Document-level metadata is loaded from `extracted_metadata.json`. Although no `content_type` or page-level fields are included, the script records which pages each chunk spans (`start_page`, `end_page`) and appends `doc_title`, `processing_date`, `language`, and `domain` to each chunk.

**What to Expect as Output (The “chunk_text” Step):**
After running `prepare_for_chunking.py`, you get a `final_chunks.json` file in the same directory. This JSON file contains an array of chunk objects, each with fields like:

```json
{
  "chunk": "this is the text of one chunk...",
  "doc_title": "the document title",
  "processing_date": "2023-08-30T12:34:56",
  "language": "english",
  "domain": "general",
  "start_page": 10,
  "end_page": 12
}
```

No `content_type` or page-level metadata is included at this stage.

**Next Steps:**
This `final_chunks.json` can now be used by downstream processes, such as:
- Generating embeddings for each chunk using a language model’s embedding API.
- Indexing chunks for retrieval in a Q&A system.
- Future enhancements might add `content_type` classification, advanced filtering, or integration with other tools for improved semantic structuring.

**Summary:**
`prepare_for_chunking.py` takes standardized extraction results from `pdf_extractor.py` and produces coherent, token-limited chunks suited for LLM-based retrieval scenarios. With sentence-level boundaries, token-level control, overlapping context, and a progress bar, it lays a strong foundation for subsequent steps in the pipeline.