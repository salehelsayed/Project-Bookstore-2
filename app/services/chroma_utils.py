# chroma_utils.py
import os
from typing import List
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from langchain_openai import ChatOpenAI
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

    # System instruction included at top of both templates
    # system_instruction = "Act as an expert. Reply to questions about this document. Self-reflect on your answers."
    system_instruction = (
    "You are a friendly, expert assistant. "
    "First, read the user’s query and the provided context carefully and reason silently before writing your final answer. "
    "When formulating your response, use Markdown to present information clearly. "
    "If the response benefits from headings, bullet points, or code blocks, include them. "
    "If the user’s question is unclear, ask for clarification rather than making unfounded assumptions."
)

    template = f"""{system_instruction}
Context:
{{context}}

Question: {{question}}
"""
    

    refine_template = f"""{system_instruction}
Refine the original answer based on additional context.

Existing answer:
{{existing_answer}}

Additional context:
{{context}}

Question: {{question}}
"""
    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
    REFINE_PROMPT = PromptTemplate(
        template=refine_template,
        input_variables=["existing_answer", "context", "question"]
    )

    openai_api_key = current_app.config.get('OPENAI_API_KEY')
    print(f"Debug - Using API key (first 10 chars): {openai_api_key[:10] if openai_api_key else 'None'}")

    # Initialize ChatOpenAI without prefix_messages
    llm = ChatOpenAI(
        api_key=openai_api_key,
        model_name="gpt-4o-mini",
        temperature=0.3,
        max_tokens=1200,
        streaming=True
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="refine",
        retriever=retriever,
        chain_type_kwargs={
            "question_prompt": PROMPT,
            "refine_prompt": REFINE_PROMPT,
            "document_variable_name": "context"
        },
        return_source_documents=True
    )

    return qa
