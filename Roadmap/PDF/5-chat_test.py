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
    chroma_db_path = "C:\\Users\\s\\Desktop\\Windsurf-output\\Project-bookstore-2\\app\\static\\storage\\books\\Cybersecurity\\chroma_db"

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
