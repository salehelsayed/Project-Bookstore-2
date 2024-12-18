# 5- Test Chroma -  Chat Retrieval & QA Pipeline

**Current Script Description:**

This script sets up a Retrieval-Augmented Generation (RAG) pipeline that leverages locally stored embeddings in a Chroma vector database for semantic retrieval, and then uses an OpenAI language model to generate answers. Unlike direct LLM queries that rely solely on model knowledge, this approach enriches responses with specific context retrieved from your custom documents, enhancing reliability and relevance.

**Key Features:**

1. **Local Vector Database Retrieval:**
   - The script connects to a Chroma vector database stored on your local machine, loaded with document embeddings generated from a SentenceTransformer model.
   - Using these embeddings, it finds the most semantically relevant document chunks to any given user query.

2. **Flexible Embedding Model:**
   - Retrieval is powered by `SentenceTransformerEmbeddings` (e.g., `all-MiniLM-L6-v2`), ensuring compatibility with pre-ingested embeddings.
   - By using the same embedding model at query time that was used during ingestion, you guarantee that vector lookups return the most accurate matches.

3. **OpenAI LLM for Answer Generation:**
   - After retrieving relevant chunks, the script passes the user’s query and the contextual documents to an OpenAI LLM (e.g., GPT-3.5 or GPT-4).
   - The LLM integrates the provided context to produce a final, informative answer. If the LLM lacks sufficient context, it is instructed to say so, minimizing hallucinations.

4. **Configurable Prompt Template:**
   - A prompt template provides structure, ensuring the LLM follows instructions:
     - It encourages the LLM to use given context to answer the question.
     - If the answer is unknown from the context, the LLM should respond accordingly.

5. **Local & Secure:**
   - The embeddings and documents are stored locally with Chroma, ensuring privacy and control over your data.
   - The `.env` file securely holds the OpenAI API key, ensuring the script doesn’t hardcode sensitive credentials.

**Installation Notes:**
- **Sentence Transformers:**  
  Install `sentence-transformers` for embeddings:
  ```bash
  pip install sentence-transformers
  ```
  
- **Chroma:**  
  Install `chromadb` for a local vector store:
  ```bash
  pip install chromadb
  ```
  
- **LangChain & OpenAI Integration:**  
  Ensure `langchain`, `langchain_chroma`, `langchain_openai`, and `python-dotenv` are installed:
  ```bash
  pip install langchain langchain-chroma langchain-openai python-dotenv
  ```

**Usage:**
1. Ensure you have a `.env` file with:
   ```env
   OPENAI_API_KEY=sk-<your_openai_api_key>
   ```
2. Confirm that the `chroma_db` directory and the `Cybersecurity` collection (or your chosen collection name) are correctly populated with embeddings using the same model (`all-MiniLM-L6-v2`).
3. Run the script:
   ```bash
   python chat_test.py
   ```
   
   Replace `chat_test.py` with your actual script name if different.

**Workflow:**
1. **Loading Environment & Keys:**
   - The script loads the `.env` file and sets the `OPENAI_API_KEY`.
   
2. **Initialization of Embeddings & Vectorstore:**
   - Initializes `SentenceTransformerEmbeddings` using the `all-MiniLM-L6-v2` model.
   - Connects to the Chroma vector database with the specified `collection_name` and `persist_directory`.
   
3. **QA Chain Setup:**
   - Constructs a prompt template instructing the LLM on how to use the retrieved context.
   - Creates a `RetrievalQA` chain that:
     - Uses the embeddings to retrieve the top `k` most relevant document chunks.
     - Passes these chunks plus the user’s query to the OpenAI LLM.
   
4. **Interactive Q&A:**
   - The script enters an interactive loop where users can ask questions.
   - For each query:
     - It’s embedded and used to retrieve relevant documents from Chroma.
     - The documents and query form a prompt for the LLM, which generates a context-informed answer.
   - Type `quit` to exit.

**What to Expect as Output:**
- For each user query, the script prints out the answer generated by the OpenAI model, using the retrieved context. If insufficient data is available, the model acknowledges the lack of information.

**Next Steps:**
- Consider refining your prompt template to guide the LLM’s tone, style, and answer length.
- Adjust the number of retrieved documents (`k`) or switch embedding models if you need better retrieval performance.
- Integrate additional data sources or different collections for a richer knowledge base.

**Summary:**
This script demonstrates a robust retrieval and Q&A pipeline. It pairs a locally stored vector database of documents (embedded by `SentenceTransformer`) with a powerful OpenAI LLM for generating high-quality, context-aware answers. With this pipeline, you can provide your users with accurate, contextually grounded responses derived from your own document set, going beyond the LLM’s base knowledge.


```python
import os
from dotenv import load_dotenv
from typing import List
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings

from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate

class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode([text])[0].tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()

def main():
    # Load environment variables (including OPENAI_API_KEY)
    load_dotenv(dotenv_path="C:\\Users\\s\\Desktop\\Windsurf-output\\Project-bookstore-2\\.env", override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    print("Loaded API Key:", api_key)
    os.environ["OPENAI_API_KEY"] = api_key

    # Path to the directory where Chroma database (chroma_db folder) was stored
    chroma_db_path = "C:\\app\\static\\storage\\books\\Cybersecurity\\chroma_db"

    # Use the same embeddings model that was used during ingestion
    embeddings = SentenceTransformerEmbeddings()

    vectorstore = Chroma(
        collection_name="Cybersecurity",
        persist_directory=chroma_db_path,
        embedding_function=embeddings
    )

    # Define a helpful prompt template
    template = """You are a helpful assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say so.

Context:
{context}

Question: {question}
"""
    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

    # Retrieval uses the SentenceTransformer embeddings, final answer uses OpenAI LLM
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": PROMPT}
    )

    print("Welcome! Type your question and press enter. Type 'quit' to exit.")
    while True:
        query = input("\nYour question: ")
        if query.lower().strip() == "quit":
            break
        
        # Here’s what happens:
        # 1. Query is embedded with SentenceTransformerEmbeddings to find relevant docs.
        # 2. Retrieved context and the query are passed to the OpenAI LLM to generate the answer.
        response = qa.invoke({"query": query})
        answer = response["result"]
        print("Answer:", answer)

if __name__ == "__main__":
    main()
```