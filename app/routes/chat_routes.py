"""
Chat functionality route handlers.
"""
from flask import Blueprint, jsonify, request
from app.services.openai_utils import get_chat_response

chat = Blueprint('chat', __name__)

@chat.route('/chat', methods=['POST'])
def chat_endpoint():
    """Handle chat messages and return AI responses."""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    response = get_chat_response(data['message'])
    return jsonify({'response': response})
