# 1- PDF Extractor

**Current Script Description (`pdf_extractor.py`):**

This script uses `pdfminer.six` to efficiently extract text from a PDF and write it to a standard output format without storing large amounts of data in memory. For each page, it normalizes and immediately writes the extracted text to an `extracted.txt` file, ensuring minimal memory usage. Additionally, it produces an `extracted_metadata.json` file with simple, document-level metadata for reference. No page-level metadata or `content_type` classification is included at this stage.

**Key Features:**

1. **Standardized Output Files:**  
   When run on a given PDF, the script creates:
   - `extracted.txt`: Contains one line per page, with normalized text.
   - `extracted_metadata.json`: Contains document-level metadata such as `doc_title`, `processing_date`, `language`, `domain`, and the `start_page`/`end_page` of the PDF.

2. **Memory Efficiency:**  
   The script processes the PDF page-by-page using `pdfminer.six`. It extracts and writes text for each page immediately, never holding the entire PDF’s content in memory at once. This approach is well-suited for large documents.

3. **Progress Bar with `tqdm`:**  
   Before extraction, the script counts the number of pages. Using this count, it displays a progress bar showing how many pages have been processed and how many remain, providing clear feedback during long extractions.

4. **Document-Level Metadata Only:**  
   The metadata file focuses on overall document information (e.g., `doc_title`, `processing_date`, `language`, `domain`), as well as the start and end page numbers of the PDF. No page-level entries or `content_type` fields are present yet, keeping the metadata simple and straightforward.

5. **No Large In-Memory Strings:**  
   Instead of returning all the extracted text at the end, the script writes out a `.txt` file line-by-line. Future steps (like sentence-based chunking or semantic classification) can operate directly on the `extracted.txt` file and the `extracted_metadata.json` data, enhancing modularity and scalability.

**Installation Notes:**  
- `pdfminer.six`: `pip install pdfminer.six`  
- `tqdm`: `pip install tqdm`

**Usage Example:**
```bash
python -m app.services.pdf_extractor "path/to/your/document.pdf"
```
The script will produce:
- `extracted.txt`: One page of extracted, normalized text per line.
- `extracted_metadata.json`: Document-level metadata, no pages dictionary at this time.

**Next Steps:**
At this point, the output is minimal and focused solely on raw text extraction and basic metadata. In the future, you can extend the pipeline by:
- Adding `content_type` detection (via heuristics or an LLM-based classifier).
- Introducing page-level metadata or other fields.
- Performing more advanced, semantic-based chunking in subsequent scripts.

**Summary:**
`pdf_extractor.py` provides a clean, memory-efficient starting point for PDF text extraction. It standardizes output file names (`extracted.txt`, `extracted_metadata.json`), ensures minimal memory usage, and offers a simple, document-level metadata file. This solid foundation makes it easier to integrate later enhancements for retrieval, classification, or Q&A tasks.