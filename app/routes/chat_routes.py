from flask import Blueprint, jsonify, request, session, current_app
from app.services.openai_utils import get_chat_response
from app.services.chroma_utils import get_qa_chain
from flask import current_app

import os

chat = Blueprint('chat', __name__)

@chat.route('/chat', methods=['POST'])
def chat_endpoint():
    print(f"Debug - API Key in chat endpoint: {current_app.config.get('OPENAI_API_KEY')[:10]}...")
    
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    # Retrieve book_directory from session (already set in main_routes.py)
    book_directory = session.get('book_directory')
    if not book_directory:
        return jsonify({'error': 'Book directory not found in session'}), 400

    # Construct chroma_db_path and collection_name
    chroma_db_path = os.path.join(book_directory, "chroma_db")
    collection_name = os.path.basename(book_directory)

    # Debug prints
    print(f"Debug - book_directory: {book_directory}")
    print(f"Debug - chroma_db_path: {chroma_db_path}")
    print(f"Debug - collection_name: {collection_name}")
    print(f"Debug - Message: {data['message']}")

    # Get the QA chain for this book
    qa = get_qa_chain(chroma_db_path, collection_name)

    # Get response using QA chain
    response = get_chat_response(data['message'], qa)
    print(f"Debug - Response: {response}")
    return jsonify({'response': response})
