import sys
import os
import json
import shutil
import chromadb
from tqdm import tqdm

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m app.services.store_in_chroma <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    chroma_input_path = os.path.join(directory, "chroma_input.json")

    if not os.path.exists(chroma_input_path):
        print(f"Error: chroma_input.json not found in {directory}")
        sys.exit(1)

    # Load the data from chroma_input.json
    with open(chroma_input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    documents = data["documents"]
    metadatas = data["metadatas"]
    ids = data["ids"]
    embeddings = data["embeddings"]  # list of lists of floats

    # Directory for Chroma's local database
    persist_dir = os.path.join(directory, "chroma_db")

    # Check if there's an existing database and overwrite it if yes
    if os.path.exists(persist_dir):
        print("Existing Chroma database found. Removing it to overwrite...")
        shutil.rmtree(persist_dir)

    # Initialize a new PersistentClient
    client = chromadb.PersistentClient(path=persist_dir)

    # Create or get a collection for this book
    collection_name = os.path.basename(os.path.normpath(directory))
    collection = client.get_or_create_collection(collection_name)

    print(f"Storing data in Chroma collection '{collection_name}'...")

    # Insert data in batches with a progress bar
    batch_size = 100
    total = len(documents)

    pbar = tqdm(total=total, desc="Inserting Embeddings into Chroma", unit="doc")

    for start_idx in range(0, total, batch_size):
        end_idx = min(start_idx + batch_size, total)
        batch_docs = documents[start_idx:end_idx]
        batch_meta = metadatas[start_idx:end_idx]
        batch_ids = ids[start_idx:end_idx]
        batch_embs = embeddings[start_idx:end_idx]

        collection.add(
            documents=batch_docs,
            metadatas=batch_meta,
            ids=batch_ids,
            embeddings=batch_embs
        )

        pbar.update(len(batch_docs))

    pbar.close()

    # Persistence is automatic with PersistentClient
    print("Data added to Chroma successfully!")
    print(f"Chroma database stored at: {persist_dir}")
