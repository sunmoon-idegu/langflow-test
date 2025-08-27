import os
from typing import List
import openai
from fastapi import HTTPException

from models.request_models import ChatMessage
from models.response_models import ChatResponse
from utils.logger import get_logger

logger = get_logger(__name__)

class LLMService:
    """Simple LLM service that handles chat requests."""
    
    def __init__(self):
        self.client = None
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key:
            try:
                self.client = openai.OpenAI(api_key=api_key)
                logger.info("OpenAI service initialized")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        else:
            logger.warning("No OpenAI API key found. Using mock responses.")
    
    async def chat(
        self,
        messages: List[ChatMessage],
        max_tokens: int = 100,
        temperature: float = 0.7,
        model: str = "gpt-3.5-turbo"
    ) -> ChatResponse:
        """Process a chat request and return the response."""
        try:
            if self.client:
                # Use OpenAI
                logger.info(f"Processing chat with OpenAI model: {model}")
                
                # Convert messages to OpenAI format
                openai_messages = [
                    {"role": msg.role, "content": msg.content} for msg in messages
                ]
                
                # Make API call
                response = self.client.chat.completions.create(
                    model=model,
                    messages=openai_messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                
                # Extract response
                response_text = response.choices[0].message.content
                tokens_used = response.usage.total_tokens if response.usage else None
                
                logger.info(f"OpenAI response generated successfully. Tokens used: {tokens_used}")
                
                return ChatResponse(
                    response=response_text,
                    model_used=model,
                    tokens_used=tokens_used
                )
            else:
                # Use mock response
                logger.info("Using mock response (no API key configured)")
                return self._generate_mock_response(messages, model)
                
        except Exception as e:
            logger.error(f"Error in LLM service: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing chat request: {str(e)}"
            )
    
    def _generate_mock_response(self, messages: List[ChatMessage], model: str) -> ChatResponse:
        """Generate a mock response when no API key is available."""
        import random
        
        # Get the last user message
        user_messages = [msg for msg in messages if msg.role == "user"]
        if user_messages:
            last_message = user_messages[-1].content
        else:
            last_message = "Hello"
        
        # Create a mock response
        responses = [
            "I understand your request and will help you with that.",
            "Based on the information provided, here's what I can suggest.",
            "That's an interesting question. Here's my perspective:",
            "I can help you with that. Here's what you need to know:",
            "Let me provide you with a comprehensive answer:"
        ]
        
        base_response = random.choice(responses)
        words = last_message.split()[:5]  # Take first 5 words
        context = " ".join(words)
        
        response_text = f"{base_response} Regarding '{context}', here's what I can tell you: This is a mock response for demonstration purposes."
        
        return ChatResponse(
            response=response_text,
            model_used=f"mock-{model}",
            tokens_used=None
        )
    
    def is_available(self) -> bool:
        """Check if the service is available."""
        return True  # Always available, either with OpenAI or mock
