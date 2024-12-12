You’ll need to run the scripts in the following order to regenerate and overwrite the Chroma database for a given book directory:

1. **prepare_for_chunking.py**:  
   - **Purpose:** Reads `extracted.txt` and `extracted_metadata.json` to produce `final_chunks.json`.
   - **Command:**  
     ```bash
     python -m app.services.prepare_for_chunking <path_to_book_directory>
     ```
   - **Example:**  
     ```bash
     python -m app.services.prepare_for_chunking "C:\Users\s\Desktop\Windsurf-output\Project-bookstore-2\app\static\storage\books\Cybersecurity"
     ```
   Ensure that `extracted.txt` and `extracted_metadata.json` are already in the provided directory.

2. **generate_embeddings.py**:  
   - **Purpose:** Takes `final_chunks.json` and generates `chroma_input.json` containing embeddings and metadata.
   - **Command:**  
     ```bash
     python -m app.services.generate_embeddings <path_to_book_directory>
     ```
   - **Example:**  
     ```bash
     python -m app.services.generate_embeddings "C:\Users\s\Desktop\Windsurf-output\Project-bookstore-2\app\static\storage\books\Cybersecurity"
     ```

3. **store_in_chroma.py**:  
   - **Purpose:** Uses `chroma_input.json` to create or overwrite a local Chroma DB (`chroma_db` folder) in the specified directory.
   - **Command:**  
     ```bash
     python -m app.services.store_in_chroma <path_to_book_directory>
     ```
   - **Example:**  
     ```bash
     python -m app.services.store_in_chroma "C:\Users\s\Desktop\Windsurf-output\Project-bookstore-2\app\static\storage\books\Cybersecurity"
     ```

**Order:**  
1. Run `prepare_for_chunking.py` to produce `final_chunks.json`.  
2. Run `generate_embeddings.py` to produce `chroma_input.json`.  
3. Run `store_in_chroma.py` to create/overwrite the Chroma database.

**Important Note:**  
- Running `store_in_chroma.py` will overwrite the existing Chroma database in the specified directory, ensuring the new embeddings and metadata from the current run are stored.  
- Always ensure that `final_chunks.json` and `chroma_input.json` are updated (by running the previous steps) before storing them into Chroma.