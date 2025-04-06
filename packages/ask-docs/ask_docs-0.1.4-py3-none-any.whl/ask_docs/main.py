"""Main module for AskDocs API."""

from ask_docs.core import process_query, get_matching_documents, kb_info
from ask_docs.config import get_default_model, get_prompt_template

def ask_question(question: str, model: str = None, template_name: str = None) -> str:
    """Ask a question using AskDocs.
    
    Args:
        question: The question to ask
        model: The LLM model to use (defaults to config)
        template_name: The prompt template to use (defaults to config)
        
    Returns:
        The answer to the question
    """
    if model is None:
        model = get_default_model()
        
    return process_query(question, model, template_name)

def preview_matches(question: str, top_k: int = 3) -> list:
    """Preview the top matching documents for a question.
    
    Args:
        question: The question to preview matches for
        top_k: The number of matches to return
        
    Returns:
        List of (filename, snippet) tuples for the top matches
    """
    return get_matching_documents(question, top_k)

def get_kb_info() -> dict:
    """Get information about the knowledge base.
    
    Returns:
        Dict containing information about the knowledge base
    """
    return kb_info()