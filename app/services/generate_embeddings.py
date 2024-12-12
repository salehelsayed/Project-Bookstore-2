import sys
import os
import json
from sentence_transformers import SentenceTransformer

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m app.services.generate_embeddings <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]

    # Paths for input and output files
    final_chunks_path = os.path.join(directory, "final_chunks.json")
    chroma_input_path = os.path.join(directory, "chroma_input.json")

    if not os.path.exists(final_chunks_path):
        print(f"Error: final_chunks.json not found in {directory}")
        sys.exit(1)

    # Load final_chunks from JSON
    with open(final_chunks_path, 'r', encoding='utf-8') as f:
        final_chunks = json.load(f)

    # Extract the chunk texts and associated metadata
    documents = []
    metadatas = []
    ids = []

    for i, chunk_info in enumerate(final_chunks):
        chunk_text = chunk_info["chunk"]
        metadata = {
            "doc_title": chunk_info.get("doc_title", ""),
            "processing_date": chunk_info.get("processing_date", ""),
            "language": chunk_info.get("language", ""),
            "domain": chunk_info.get("domain", ""),
            "start_page": chunk_info.get("start_page", ""),
            "end_page": chunk_info.get("end_page", ""),
            "page": chunk_info.get("page", "")
        }

        documents.append(chunk_text)
        metadatas.append(metadata)
        ids.append(f"chunk_{i}")

    # Load a local embedding model from sentence-transformers
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    print("Generating embeddings...")
    # Enable progress bar by passing show_progress_bar=True
    embeddings = model.encode(documents, convert_to_numpy=True, show_progress_bar=True)
    print("Embeddings generated.")

    # Convert embeddings (numpy array) to a list of lists for JSON serialization
    embeddings_list = embeddings.tolist()

    # Prepare the data to be saved
    data_to_save = {
        "documents": documents,
        "metadatas": metadatas,
        "ids": ids,
        "embeddings": embeddings_list
    }

    # Save to a JSON file for later use with store_in_chroma.py
    with open(chroma_input_path, 'w', encoding='utf-8') as out_f:
        json.dump(data_to_save, out_f, ensure_ascii=False, indent=2)

    print(f"Data prepared and saved to {chroma_input_path}.")
    print("This file can now be provided to store_in_chroma.py for insertion into Chroma.")
