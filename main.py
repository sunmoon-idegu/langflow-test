from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers.chat_router import router as chat_router
from config.settings import settings
from utils.logger import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging(settings.log_level)

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Include routers
app.include_router(chat_router)

@app.get("/")
def read_root():
    return {"message": "Simple Language Model API is running!"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "api_title": settings.api_title,
        "api_version": settings.api_version,
        "openai_configured": bool(settings.openai_api_key)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        log_level=settings.log_level.lower()
    )
