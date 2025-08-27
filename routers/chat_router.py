from fastapi import APIRouter, Depends

from models.request_models import ChatRequest
from models.response_models import ChatResponse
from controllers.chat_controller import ChatController
from services.llm_service import LLMService

router = APIRouter(prefix="/chat", tags=["chat"])

# Dependency injection
def get_llm_service():
    return LLMService()

def get_chat_controller(llm_service: LLMService = Depends(get_llm_service)):
    return ChatController(llm_service)

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chat_controller: ChatController = Depends(get_chat_controller)
):
    """
    Chat with the language model.
    Can handle both single prompts and multi-turn conversations.
    """
    return await chat_controller.process_chat(request)

@router.get("/health")
async def health_check(
    chat_controller: ChatController = Depends(get_chat_controller)
):
    """
    Check the health status of the chat service.
    """
    return chat_controller.health_check()
