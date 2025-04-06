"""Tests for document retrieval functions."""
import os
import tempfile
import pytest
from pathlib import Path
from ask_docs.core.document_retrieval import load_documents, get_best_chunks

def test_load_documents_empty_dir():
    """Test loading documents from an empty directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        docs = load_documents(temp_dir)
        assert isinstance(docs, list)
        assert len(docs) == 0

def test_load_documents():
    """Test loading documents from a directory with files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        file1 = Path(temp_dir) / "test1.txt"
        file2 = Path(temp_dir) / "test2.txt"
        
        file1.write_text("This is test file 1.")
        file2.write_text("This is test file 2.")
        
        docs = load_documents(temp_dir)
        
        assert isinstance(docs, list)
        assert len(docs) == 2
        
        # Check document structure
        for doc in docs:
            assert "filename" in doc
            assert "content" in doc
            assert doc["filename"] in ["test1.txt", "test2.txt"]
            if doc["filename"] == "test1.txt":
                assert doc["content"] == "This is test file 1."
            else:
                assert doc["content"] == "This is test file 2."

def test_load_documents_skips_binary():
    """Test that load_documents skips binary files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        text_file = Path(temp_dir) / "text.txt"
        binary_file = Path(temp_dir) / "binary.bin"
        
        text_file.write_text("This is a text file.")
        # Write some binary data
        with open(binary_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03')
        
        docs = load_documents(temp_dir)
        
        assert len(docs) == 1
        assert docs[0]["filename"] == "text.txt"

def test_get_best_chunks():
    """Test getting best chunks based on a query."""
    docs = [
        {"filename": "file1.txt", "content": "This is about Atari missiles."},
        {"filename": "file2.txt", "content": "WSYNC register helps with synchronization."},
        {"filename": "file3.txt", "content": "Player graphics are for sprites."},
    ]
    
    # Test with a query about WSYNC
    query = "How does WSYNC work?"
    results = get_best_chunks(docs, query)
    
    assert len(results) == 3  # Should return all since we have only 3 docs
    # The best match should be file2.txt since it contains "WSYNC"
    assert results[0]["filename"] == "file2.txt"
    
    # Test with a different query
    query = "How to draw a missile?"
    results = get_best_chunks(docs, query)
    
    assert len(results) == 3
    # The best match should be file1.txt since it contains "missiles"
    assert results[0]["filename"] == "file1.txt"
    
    # Test with top_n parameter
    results = get_best_chunks(docs, query, top_n=1)
    assert len(results) == 1
    assert results[0]["filename"] == "file1.txt"