from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    """Model for a single chat message."""
    role: str = Field(..., description="Role of the message sender (user, assistant, system)")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    """Model for chat request."""
    messages: List[ChatMessage] = Field(..., description="List of chat messages")
    max_tokens: Optional[int] = Field(100, description="Maximum number of tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Temperature for response randomness (0.0 to 2.0)")
    model: Optional[str] = Field("gpt-3.5-turbo", description="Model to use for generation")
    
    class Config:
        schema_extra = {
            "example": {
                "messages": [
                    {"role": "user", "content": "What is FastAPI?"}
                ],
                "max_tokens": 100,
                "temperature": 0.7,
                "model": "gpt-3.5-turbo"
            }
        }
