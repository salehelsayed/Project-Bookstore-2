from flask import Blueprint, jsonify, request, session, current_app
from app.services.openai_utils import get_chat_response
from app.services.chroma_utils import get_qa_chain
import os

# Create the Blueprint object
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        # Get book info from session
        book_directory = session.get('book_directory')
        if not book_directory:
            return jsonify({'error': 'Book directory not found in session'}), 400

        # Construct paths and get QA chain
        chroma_db_path = os.path.join(book_directory, "chroma_db")
        collection_name = os.path.basename(book_directory)
        qa_chain = get_qa_chain(chroma_db_path, collection_name)

        # Process the chat message
        data = request.get_json()
        query = data.get('message', '')
        
        if not query:
            return jsonify({'error': 'No message provided'}), 400

        result = qa_chain.invoke({"query": query})
        answer = result["result"]
        sources = result.get("source_documents", [])
        
        # Extract unique page numbers from source documents
        pages = sorted(list(set(
            doc.metadata.get("page") 
            for doc in sources 
            if doc.metadata.get("page") is not None
        )))

        return jsonify({
            'response': answer,
            'pages': pages
        })

    except Exception as e:
        print(f"Error in chat route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
