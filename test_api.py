import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Health Check:")
        print(json.dumps(response.json(), indent=2))
        print()
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure it's running on http://localhost:8000")
        return False

def test_chat_single():
    """Test single message chat."""
    try:
        data = {
            "messages": [
                {"role": "user", "content": "What is FastAPI?"}
            ],
            "max_tokens": 100,
            "temperature": 0.7,
            "model": "gpt-3.5-turbo"
        }
        
        response = requests.post(f"{BASE_URL}/chat", json=data)
        print("Single Message Chat:")
        print(json.dumps(response.json(), indent=2))
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing single chat: {e}")
        return False

def test_chat_conversation():
    """Test multi-turn conversation."""
    try:
        data = {
            "messages": [
                {"role": "user", "content": "Hello!"},
                {"role": "assistant", "content": "Hi there! How can I help you today?"},
                {"role": "user", "content": "Can you explain Python programming?"}
            ],
            "max_tokens": 150,
            "temperature": 0.7,
            "model": "gpt-3.5-turbo"
        }
        
        response = requests.post(f"{BASE_URL}/chat", json=data)
        print("Multi-turn Conversation:")
        print(json.dumps(response.json(), indent=2))
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing conversation: {e}")
        return False

def test_chat_health():
    """Test chat service health."""
    try:
        response = requests.get(f"{BASE_URL}/chat/health")
        print("Chat Service Health:")
        print(json.dumps(response.json(), indent=2))
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing chat health: {e}")
        return False

if __name__ == "__main__":
    print("Testing Restructured Language Model API\n")
    
    tests = [
        ("Health Check", test_health),
        ("Chat Service Health", test_chat_health),
        ("Single Message Chat", test_chat_single),
        ("Multi-turn Conversation", test_chat_conversation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
        print("-" * 50)
    
    print("\nTest Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
