import google.generativeai as genai
from typing import List, Dict, Optional
from app.core.config import settings

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

GEMINI_MODEL_NAME = settings.GEMINI_MODEL_NAME

def chat_with_agent(
    message: str,
    history: List[Dict[str, str]],
    context: Optional[Dict[str, str]] = None
) -> str:
    """
    Chat with the agent.
    context keys: 'selected_file_path', 'selected_file_content', 'project_structure'
    """
    
    system_instruction = """
You are an expert AI software developer assistant in an IDE.
You help users write, debug, and understand code.
You have access to the current file content and project structure.
Be concise, helpful, and technically accurate.
If you suggest code changes, provide them in code blocks.
"""

    # Build context string
    context_str = ""
    if context:
        if context.get('selected_file_path'):
            context_str += f"\n\n--- CURRENT FILE: {context['selected_file_path']} ---\n"
            content = context.get('selected_file_content', '')
            # Truncate if too long?
            if len(content) > 20000:
                content = content[:20000] + "...(truncated)"
            context_str += content + "\n\n"
        
        if context.get('project_structure'):
            context_str += f"\n\n--- PROJECT STRUCTURE ---\n{context['project_structure']}\n\n"

    # Start chat
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME, system_instruction=system_instruction)
        
        # Convert history format
        # History is list of {role: 'user'|'model', parts: [text]}
        gemini_history = []
        for msg in history:
            gemini_history.append({
                "role": msg["role"],
                "parts": [msg["content"]]
            })
            
        chat = model.start_chat(history=gemini_history)
        
        # Send message with context
        full_message = message
        if context_str:
            full_message = f"{context_str}\n\nUser Question: {message}"
            
        response = chat.send_message(full_message)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
