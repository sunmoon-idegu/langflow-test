from fastapi import HTTPException
from typing import Dict, Any

from models.request_models import ChatRequest
from models.response_models import ChatResponse
from services.llm_service import LLMService
from utils.logger import get_logger

logger = get_logger(__name__)

class ChatController:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        """
        Process a chat request and return the response.
        """
        try:
            logger.info(f"Processing chat with {len(request.messages)} messages")
            
            # Validate request
            self._validate_chat_request(request)
            
            # Process with LLM service
            response = await self.llm_service.chat(
                messages=request.messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                model=request.model
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat controller: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check the health status of the chat service.
        """
        return {
            "status": "healthy",
            "service": "chat",
            "llm_service_available": self.llm_service.is_available()
        }
    
    def _validate_chat_request(self, request: ChatRequest) -> None:
        """
        Validate the chat request.
        """
        if not request.messages:
            raise HTTPException(status_code=400, detail="Messages cannot be empty")
        
        if len(request.messages) == 0:
            raise HTTPException(status_code=400, detail="At least one message is required")
        
        # Check if all messages have required fields
        for i, message in enumerate(request.messages):
            if not message.role or not message.content:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Message {i} must have both role and content"
                )
            
            if message.role not in ["user", "assistant", "system"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Message {i} has invalid role: {message.role}. Must be 'user', 'assistant', or 'system'"
                )
