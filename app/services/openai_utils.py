# openai_utils.py
import os
from langchain.chains import RetrievalQA
from flask import current_app

def get_chat_response(query: str, qa_chain: RetrievalQA) -> str:
    """
    Given a user query and a RetrievalQA chain, get a response from the LLM.
    
    Args:
        query (str): The user's question.
        qa_chain (RetrievalQA): The QA chain with LLM and vectorstore integrated.

    Returns:
        str: The AI-generated answer.
    """
    # Debug the API key
    api_key = current_app.config.get('OPENAI_API_KEY')
    print(f"Debug - API Key in get_chat_response: {api_key[:10] if api_key else 'None'}...")
    
    response = qa_chain.invoke({"query": query})
    return response["result"]


