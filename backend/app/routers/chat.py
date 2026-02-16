from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.chat_agent import chat_with_agent

router = APIRouter(
    prefix="/chat",
    tags=["Agent Chat"]
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage]
    context: Optional[Dict[str, str]] = None

@router.post("/send")
def send_chat_message(payload: ChatRequest):
    """
    Send a message to the AI agent with context.
    """
    # Convert Pydantic models to dicts for service
    history_dicts = [{"role": msg.role, "content": msg.content} for msg in payload.history]
    
    response_text = chat_with_agent(
        message=payload.message,
        history=history_dicts,
        context=payload.context
    )
    
    return {"role": "model", "content": response_text}
