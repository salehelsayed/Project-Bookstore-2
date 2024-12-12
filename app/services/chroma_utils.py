# chroma_utils.py
import os
from typing import List
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from flask import current_app

class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode([text])[0].tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()

def get_qa_chain(chroma_db_path: str, collection_name: str):
    """
    Given a chroma_db_path and a collection_name, return a RetrievalQA chain.
    
    Args:
        chroma_db_path (str): Path to the chroma_db directory
        collection_name (str): Name of the collection, usually the book directory name

    Returns:
        RetrievalQA: The constructed QA chain
    """
    embeddings = SentenceTransformerEmbeddings()

    vectorstore = Chroma(
        collection_name=collection_name,
        persist_directory=chroma_db_path,
        embedding_function=embeddings
    )

    # Test retrieval directly
    test_query = "What is the book about?"
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.get_relevant_documents(test_query)
    print(f"Debug - Retrieving docs for test query '{test_query}': {docs}")

    template = """You are a helpful assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say so.

Context:
{context}

Question: {question}
"""
    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

    openai_api_key = current_app.config.get('OPENAI_API_KEY')
    print(f"Debug - Using API key (first 10 chars): {openai_api_key[:10] if openai_api_key else 'None'}")

    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(api_key=openai_api_key, temperature=0),
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa
