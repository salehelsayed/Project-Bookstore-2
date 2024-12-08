"""
OpenAI integration utilities.
"""
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_chat_response(message: str) -> str:
    """
    Get a response from OpenAI's chat model.
    
    Args:
        message (str): User's input message
        
    Returns:
        str: AI-generated response
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response: {str(e)}"
