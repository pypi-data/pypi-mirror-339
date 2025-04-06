"""Tests for CLI functionality."""
import pytest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from ask_docs.cli.main import app
from ask_docs.core import ask_question, preview_matches

runner = CliRunner()

@patch('ask_docs.cli.main.ask_question')
def test_cli_ask(mock_ask):
    """Test the CLI ask command."""
    # Setup mock
    mock_ask.return_value = "This is a mock answer."
    
    # Run the CLI command
    result = runner.invoke(app, ["ask", "How does WSYNC work?"])
    
    # Verify
    assert result.exit_code == 0
    mock_ask.assert_called_once_with("How does WSYNC work?", "openai")
    assert "This is a mock answer." in result.stdout

@patch('ask_docs.cli.main.ask_question')
def test_cli_ask_with_model(mock_ask):
    """Test the CLI ask command with a specified model."""
    # Setup mock
    mock_ask.return_value = "This is a mock answer."
    
    # Run the CLI command
    result = runner.invoke(app, ["ask", "How does WSYNC work?", "--model", "ollama"])
    
    # Verify
    assert result.exit_code == 0
    mock_ask.assert_called_once_with("How does WSYNC work?", "ollama")
    assert "This is a mock answer." in result.stdout

def test_cli_list_models():
    """Test the CLI list-models command."""
    # Run the CLI command
    result = runner.invoke(app, ["list-models"])
    
    # Verify
    assert result.exit_code == 0
    assert "openai" in result.stdout
    assert "ollama" in result.stdout
    assert "claude" in result.stdout
    assert "gemini" in result.stdout
    assert "groq" in result.stdout

@patch('ask_docs.cli.main.preview_matches')
def test_cli_preview(mock_preview):
    """Test the CLI preview command."""
    # Setup mock
    mock_preview.return_value = [
        ("file1.txt", "This is sample content from file 1."),
        ("file2.txt", "This is sample content from file 2.")
    ]
    
    # Run the CLI command
    result = runner.invoke(app, ["preview", "How does WSYNC work?"])
    
    # Verify
    assert result.exit_code == 0
    mock_preview.assert_called_once_with("How does WSYNC work?")
    assert "file1.txt" in result.stdout
    assert "file2.txt" in result.stdout
    assert "This is sample content from file 1." in result.stdout
    assert "This is sample content from file 2." in result.stdout