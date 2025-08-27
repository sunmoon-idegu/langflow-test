# Simple Language Model API

A clean, well-structured FastAPI application for language model interactions with proper separation of concerns.

## Architecture

This application follows a clean architecture pattern with the following structure:

```
langflow-test/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
├── routers/               # HTTP routing layer
│   └── chat_router.py     # Chat endpoint routes
├── controllers/           # Business logic layer
│   └── chat_controller.py # Chat request handling
├── models/                # Data models layer
│   ├── request_models.py  # Request data models
│   └── response_models.py # Response data models
├── services/              # External service layer
│   └── llm_service.py     # Simple LLM service
├── config/                # Configuration layer
│   └── settings.py        # Application settings
└── utils/                 # Utility functions
    └── logger.py          # Logging utilities
```

## Features

- ✅ **Clean Architecture**: Proper separation of concerns
- ✅ **Simple Service Layer**: Easy to understand and maintain
- ✅ **Dependency Injection**: Easy to test and maintain
- ✅ **Mock Responses**: Works without API keys for testing
- ✅ **Proper Logging**: Structured logging throughout the application
- ✅ **Configuration Management**: Environment-based configuration
- ✅ **Input Validation**: Comprehensive request validation
- ✅ **Error Handling**: Proper error responses
- ✅ **API Documentation**: Auto-generated with FastAPI

## Installation

1. **Clone and navigate to the project**:
   ```bash
   cd langflow-test
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional):
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

## Usage

### Running the Application

```bash
# Run with Python
python main.py

# Or with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### API Endpoints

#### 1. **Health Check**
```bash
GET /health
```

#### 2. **Chat Service Health**
```bash
GET /chat/health
```

#### 3. **Chat with Language Model**
```bash
POST /chat
```

**Request Body**:
```json
{
  "messages": [
    {"role": "user", "content": "What is FastAPI?"}
  ],
  "max_tokens": 100,
  "temperature": 0.7,
  "model": "gpt-3.5-turbo"
}
```

**Response**:
```json
{
  "response": "FastAPI is a modern, fast web framework...",
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 25
}
```

### Examples

#### Single Message
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "messages": [{"role": "user", "content": "What is Python?"}],
       "max_tokens": 100
     }'
```

#### Multi-turn Conversation
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "messages": [
         {"role": "user", "content": "Hello!"},
         {"role": "assistant", "content": "Hi there! How can I help you?"},
         {"role": "user", "content": "Explain machine learning"}
       ],
       "max_tokens": 150
     }'
```

### Testing

Run the test script to verify everything works:

```bash
python test_api.py
```

## Architecture Benefits

### 1. **Routers** (`/routers`)
- Handle HTTP routing and request/response formatting
- Keep routing logic separate from business logic
- Easy to add new endpoints

### 2. **Controllers** (`/controllers`)
- Handle business logic and request validation
- Coordinate between different services
- Keep business rules centralized

### 3. **Models** (`/models`)
- Define data structures for requests and responses
- Provide validation and documentation
- Keep data contracts consistent

### 4. **Services** (`/services`)
- Simple service that receives requests and returns responses
- Handles external API calls (OpenAI) or generates mock responses
- Easy to understand and maintain

### 5. **Config** (`/config`)
- Centralized configuration management
- Environment-based settings
- Easy to modify application behavior

### 6. **Utils** (`/utils`)
- Shared utility functions
- Consistent logging across the application
- Reusable helper functions

## Adding New Features

### Adding a New Endpoint

1. **Add route** in `/routers/chat_router.py`:
   ```python
   @router.get("/new-endpoint")
   async def new_endpoint():
       return {"message": "New endpoint"}
   ```

2. **Add controller method** in `/controllers/chat_controller.py`:
   ```python
   def new_feature(self):
       return {"status": "implemented"}
   ```

3. **Add service method** in `/services/llm_service.py`:
   ```python
   async def new_service_method(self):
       # Implementation
       pass
   ```

### Adding a New LLM Provider

Simply modify the `LLMService` class in `/services/llm_service.py`:

```python
class LLMService:
    def __init__(self):
        # Initialize your preferred LLM provider
        pass
    
    async def chat(self, messages, **kwargs):
        # Call your preferred LLM provider
        pass
```

## Configuration

The application uses environment variables for configuration:

- `OPENAI_API_KEY`: Your OpenAI API key
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

## Development

### Project Structure Benefits

1. **Maintainability**: Clear separation of concerns
2. **Testability**: Easy to unit test each layer
3. **Scalability**: Easy to add new features
4. **Readability**: Clear code organization
5. **Simplicity**: Simple service layer that's easy to understand

This architecture makes it easy to:
- Add new endpoints
- Modify the LLM service
- Add new features
- Test individual components
- Maintain and debug the application

## Flow

```
Request → Router → Controller → Service → Response
```

1. **Router** receives HTTP request
2. **Controller** validates and processes the request
3. **Service** handles the LLM interaction
4. **Response** flows back through the same path
