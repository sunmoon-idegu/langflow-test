from pydantic import BaseModel, Field
from typing import Optional

class ChatResponse(BaseModel):
    """Model for chat response."""
    response: str = Field(..., description="Generated response text")
    model_used: str = Field(..., description="Model that was used for generation")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used in the request")
    
    class Config:
        schema_extra = {
            "example": {
                "response": "FastAPI is a modern, fast web framework for building APIs with Python based on standard Python type hints.",
                "model_used": "gpt-3.5-turbo",
                "tokens_used": 25
            }
        }
