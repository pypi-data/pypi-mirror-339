"""Tests for prompt builder."""
from ask_docs.core.prompt_builder import build_prompt

def test_build_prompt():
    """Test building a prompt from document chunks."""
    chunks = [
        {
            "filename": "file1.txt",
            "content": "This is the content of file 1."
        },
        {
            "filename": "file2.txt",
            "content": "This is the content of file 2."
        }
    ]
    
    query = "What are the contents of these files?"
    
    prompt = build_prompt(chunks, query)
    
    # Check that the prompt contains the expected elements
    assert "You are an Atari 2600 programming assistant" in prompt
    assert "File: file1.txt" in prompt
    assert "This is the content of file 1." in prompt
    assert "File: file2.txt" in prompt
    assert "This is the content of file 2." in prompt
    assert f"Question: {query}" in prompt
    assert "Answer:" in prompt

def test_build_prompt_empty_chunks():
    """Test building a prompt with no document chunks."""
    chunks = []
    query = "What is an Atari 2600?"
    
    prompt = build_prompt(chunks, query)
    
    # Check that the prompt still contains the essential elements
    assert "You are an Atari 2600 programming assistant" in prompt
    assert f"Question: {query}" in prompt
    assert "Answer:" in prompt

def test_build_prompt_special_characters():
    """Test building a prompt with special characters in query and chunks."""
    chunks = [
        {
            "filename": "special_chars.txt",
            "content": "Contains special characters: !@#$%^&*()"
        }
    ]
    
    query = "How do I handle the special characters: !@#$%^&*()?"
    
    prompt = build_prompt(chunks, query)
    
    # Check that special characters are preserved
    assert "Contains special characters: !@#$%^&*()" in prompt
    assert "How do I handle the special characters: !@#$%^&*()?" in prompt