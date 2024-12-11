"""
PDF text extraction utility using pdfminer.six.
Produces:
- extracted.txt (one normalized page per line)
- extracted_metadata.json (document-level metadata)
"""

import os
from tqdm import tqdm
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import json
from datetime import datetime

def count_pages(pdf_path: str) -> int:
    print("Counting pages...")
    count = 0
    for _ in extract_pages(pdf_path):
        count += 1
    print(f"Found {count} pages")
    return count

def extract_text_from_layout(page_layout) -> str:
    """Extract and normalize text from a single page layout."""
    page_text = []
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            page_text.append(element.get_text())
    combined_text = "".join(page_text)
    # Normalize:
    combined_text = combined_text.strip().lower()
    combined_text = ' '.join(combined_text.split())
    return combined_text

def extract_text_from_pdf(pdf_path: str) -> None:
    try:
        print(f"\nProcessing PDF: {pdf_path}")
        out_dir = os.path.dirname(pdf_path) or '.'
        txt_file_path = os.path.join(out_dir, "extracted.txt")
        json_file_path = os.path.join(out_dir, "extracted_metadata.json")

        print(f"Output text will be saved to: {txt_file_path}")
        total_pages = count_pages(pdf_path)
        print("\nExtracting text...")

        # Document-level metadata
        # doc_title from the PDF name (no extension)
        doc_title = os.path.splitext(os.path.basename(pdf_path))[0]
        processing_date = datetime.now().isoformat()
        language = "english"
        domain = "general"
        start_page = 1
        end_page = total_pages

        doc_metadata = {
            "doc_title": doc_title,
            "processing_date": processing_date,
            "language": language,
            "domain": domain,
            "start_page": start_page,
            "end_page": end_page
        }

        with open(txt_file_path, 'w', encoding='utf-8') as out_file:
            for page_layout in tqdm(extract_pages(pdf_path),
                                    desc="Extracting Pages",
                                    total=total_pages,
                                    unit="page"):
                page_text = extract_text_from_layout(page_layout)
                out_file.write(page_text + "\n")

        # Write metadata JSON
        with open(json_file_path, 'w', encoding='utf-8') as meta_f:
            json.dump(doc_metadata, meta_f, ensure_ascii=False, indent=2)

        print(f"\nExtraction complete! Output saved to: {txt_file_path}")
        print(f"Metadata saved to: {json_file_path}")

    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        raise
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        raise

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m app.services.pdf_extractor <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    extract_text_from_pdf(pdf_path)
