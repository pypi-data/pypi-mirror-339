"""Tests for web interface."""
import pytest
from unittest.mock import patch, MagicMock
from starlette.testclient import TestClient

from ask_docs.web.app import create_app
from ask_docs.main import ask_question, preview_matches

@pytest.fixture
def client():
    """Create a test client for the web app."""
    app = create_app()
    return TestClient(app)

def test_index_route(client):
    """Test the index route returns a 200 status code."""
    response = client.get("/")
    assert response.status_code == 200
    content = response.text.lower()
    
    # Check that the page contains the expected elements
    assert "docbuddy" in content
    assert "question" in content
    assert "model" in content
    assert "ask" in content

@patch('ask_docs.main.ask_question')
def test_ask_question_route(mock_ask, client):
    """Test the ask question route."""
    # Setup mock
    mock_ask.return_value = "This is a test answer."
    
    # Make the request
    response = client.post(
        "/ask",
        data={"question": "How to implement a REST API?", "model": "openai"}
    )
    
    # Verify
    assert response.status_code == 200
    assert "This is a test answer." in response.text.replace('&lt;br&gt;', '')
    assert "How to implement a REST API?" in response.text
    mock_ask.assert_called_once()

@patch('ask_docs.main.preview_matches')
def test_preview_route(mock_preview, client):
    """Test the preview route."""
    # Setup mock
    mock_preview.return_value = [
        ("file1.txt", "This is sample content from file 1."),
        ("file2.txt", "This is sample content from file 2.")
    ]
    
    # Make the request
    response = client.get(
        "/preview",
        params={"question": "How to implement a REST API?"}
    )
    
    # Verify
    assert response.status_code == 200
    assert "Document Matches" in response.text
    assert "file1.txt" in response.text
    assert "file2.txt" in response.text
    assert "This is sample content from file 1." in response.text
    mock_preview.assert_called_once()

def test_model_info_route(client):
    """Test the model info route."""
    # Make the request
    response = client.get("/model-info")
    
    # Verify
    assert response.status_code == 200
    assert "Available Models" in response.text
    assert "OpenAI" in response.text.lower() or "openai" in response.text.lower()
    assert "Ollama" in response.text.lower() or "ollama" in response.text.lower()
    assert "Claude" in response.text.lower() or "claude" in response.text.lower()
    assert "Gemini" in response.text.lower() or "gemini" in response.text.lower() 
    assert "Groq" in response.text.lower() or "groq" in response.text.lower()