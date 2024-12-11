"""
prepare_for_chunking.py

Reads:
- extracted.txt (one line per page, produced by pdf_extractor.py)
- extracted_metadata.json (document-level metadata)

Performs:
- Sentence-based token-limited chunking with overlapping tokens.
- Uses nltk and tiktoken for token counting and sentence segmentation.
- Outputs final_chunks.json containing the resulting chunks with minimal metadata.

This script assumes 'extracted.txt' and 'extracted_metadata.json' are present
in the provided directory. It will read these files, chunk the text, and write 'final_chunks.json'.
"""

import sys
import os
import json
import nltk
from nltk.tokenize import sent_tokenize
import tiktoken
from tqdm import tqdm

# Hardcoded settings for now
CHUNK_SIZE = 500
OVERLAP = 50

def ensure_nltk_punkt():
    """Ensure NLTK punkt tokenizer is downloaded."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt', quiet=True)
        print("Download complete!")

def load_metadata(json_path: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def chunk_with_overlap_indexed(sentences, encoder, chunk_size=500, overlap=50):
    """
    Similar to previous chunk_with_overlap but returns sentence indexes.
    Also includes a progress bar for monitoring chunking progress.
    """
    indexed_chunks = []
    current_sentence_idxs = []
    current_tokens_count = 0

    # Initialize progress bar for sentence processing
    pbar = tqdm(total=len(sentences), desc="Chunking Sentences", unit="sent")

    i = 0
    while i < len(sentences):
        sent = sentences[i]
        sent_tokens = len(encoder.encode(sent))
        if current_tokens_count + sent_tokens > chunk_size:
            # finalize chunk
            indexed_chunks.append(current_sentence_idxs[:])

            # overlap
            overlap_sents = []
            tokens_count_for_overlap = 0
            for idx in reversed(current_sentence_idxs):
                t_count = len(encoder.encode(sentences[idx]))
                if tokens_count_for_overlap + t_count < overlap:
                    overlap_sents.insert(0, idx)
                    tokens_count_for_overlap += t_count
                else:
                    break

            current_sentence_idxs = overlap_sents[:]
            current_tokens_count = sum(len(encoder.encode(sentences[s_idx])) for s_idx in current_sentence_idxs)

            if sent_tokens > chunk_size:
                # large sentence alone
                if current_sentence_idxs:
                    indexed_chunks.append(current_sentence_idxs[:])
                    current_sentence_idxs = []
                    current_tokens_count = 0
                indexed_chunks.append([i])
                i += 1
            else:
                current_sentence_idxs.append(i)
                current_tokens_count += sent_tokens
                i += 1
        else:
            current_sentence_idxs.append(i)
            current_tokens_count += sent_tokens
            i += 1

        pbar.update(1)

    if current_sentence_idxs:
        indexed_chunks.append(current_sentence_idxs)

    pbar.close()
    return indexed_chunks

if __name__ == "__main__":
    ensure_nltk_punkt()

    if len(sys.argv) != 2:
        print("Usage: python -m app.services.prepare_for_chunking <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    txt_path = os.path.join(directory, "extracted.txt")
    json_path = os.path.join(directory, "extracted_metadata.json")

    if not os.path.exists(txt_path):
        print(f"Error: extracted.txt not found in {directory}")
        sys.exit(1)
    if not os.path.exists(json_path):
        print(f"Error: extracted_metadata.json not found in {directory}")
        sys.exit(1)

    metadata = load_metadata(json_path)
    doc_title = metadata["doc_title"]
    processing_date = metadata["processing_date"]
    language = metadata["language"]
    domain = metadata["domain"]
    start_page = metadata["start_page"]
    end_page = metadata["end_page"]

    encoder = tiktoken.get_encoding("cl100k_base")

    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Sentence tokenize each page line
    page_sentence_map = []
    for page_idx, line in enumerate(lines, start=1):
        line = line.strip()
        sentences = sent_tokenize(line)
        page_sentence_map.append((page_idx, sentences))

    # Flatten into a single sequence of (page_idx, sentence)
    all_sentences = []
    for page_idx, sents in page_sentence_map:
        for s in sents:
            all_sentences.append((page_idx, s))

    just_sentences = [s for (_, s) in all_sentences]
    indexed_chunks = chunk_with_overlap_indexed(just_sentences, encoder, chunk_size=CHUNK_SIZE, overlap=OVERLAP)

    final_chunks = []
    for ch in indexed_chunks:
        chunk_sents = [all_sentences[idx] for idx in ch]
        pages_in_chunk = [p for (p,_) in chunk_sents]
        start_page_chunk = min(pages_in_chunk)
        end_page_chunk = max(pages_in_chunk)

        chunk_text = ' '.join(s for (_, s) in chunk_sents)

        final_chunks.append({
            "chunk": chunk_text,
            "doc_title": doc_title,
            "processing_date": processing_date,
            "language": language,
            "domain": domain,
            "start_page": start_page_chunk,
            "end_page": end_page_chunk
        })

    print(f"Created {len(final_chunks)} chunks.")
    for i, c in enumerate(final_chunks[:3]):
        print(json.dumps(c, ensure_ascii=False, indent=2))

    out_json_path = os.path.join(directory, "final_chunks.json")
    with open(out_json_path, 'w', encoding='utf-8') as out_f:
        json.dump(final_chunks, out_f, ensure_ascii=False, indent=2)
    print(f"All chunks saved to {out_json_path}")
