"""Tests for LLM implementations."""
import pytest
from unittest.mock import patch, MagicMock

from ask_docs.llm.base import BaseLLM
from ask_docs.llm import get_llm
from ask_docs.llm.openai_llm import OpenAI_LLM
from ask_docs.llm.ollama_llm import OllamaLLM
from ask_docs.llm.anthropic_llm import ClaudeLLM
from ask_docs.llm.gemini_llm import GeminiLLM
from ask_docs.llm.groq_llm import GroqLLM

def test_get_llm():
    """Test that get_llm returns the correct LLM implementation."""
    llm = get_llm("openai")
    assert isinstance(llm, OpenAI_LLM)
    
    llm = get_llm("ollama")
    assert isinstance(llm, OllamaLLM)
    
    llm = get_llm("claude")
    assert isinstance(llm, ClaudeLLM)
    
    llm = get_llm("gemini")
    assert isinstance(llm, GeminiLLM)
    
    llm = get_llm("groq")
    assert isinstance(llm, GroqLLM)

def test_get_llm_invalid():
    """Test that get_llm raises an error for invalid model."""
    with pytest.raises(ValueError):
        get_llm("invalid_model")

# OpenAI LLM Tests
@patch('ask_docs.llm.openai_llm.OpenAI')
def test_openai_llm(mock_openai):
    """Test the OpenAI LLM implementation."""
    # Setup mock
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "This is a test response"
    mock_client.chat.completions.create.return_value = mock_response
    
    # Test
    llm = OpenAI_LLM(api_key="test_key")
    response = llm.ask("Test prompt")
    
    # Verify
    assert response == "This is a test response"
    mock_client.chat.completions.create.assert_called_once()

@patch('ask_docs.llm.openai_llm.OpenAI')
def test_openai_llm_no_api_key(mock_openai):
    """Test OpenAI LLM with no API key."""
    llm = OpenAI_LLM(api_key=None)
    response = llm.ask("Test prompt")
    
    assert "Error: OpenAI API key is not configured" in response
    mock_openai.assert_not_called()

# Ollama LLM Tests
@patch('ask_docs.llm.ollama_llm.requests.post')
def test_ollama_llm(mock_post):
    """Test the Ollama LLM implementation."""
    # Setup mock
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "This is a test response"}
    mock_post.return_value = mock_response
    
    # Test
    llm = OllamaLLM()
    response = llm.ask("Test prompt")
    
    # Verify
    assert response == "This is a test response"
    mock_post.assert_called_once()

@patch('ask_docs.llm.ollama_llm.requests.post')
def test_ollama_llm_error(mock_post):
    """Test Ollama LLM error handling."""
    # Setup mock to raise an exception
    mock_post.side_effect = Exception("Test error")
    
    # Test
    llm = OllamaLLM()
    response = llm.ask("Test prompt")
    
    # Verify
    assert "Error with Ollama API: Test error" in response