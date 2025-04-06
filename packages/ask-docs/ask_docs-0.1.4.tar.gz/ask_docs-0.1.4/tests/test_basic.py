from ask_docs.core import preview_matches, ask_question
from ask_docs.config import DEFAULT_MODEL

def test_preview_returns_results():
    results = preview_matches("How does WSYNC work?")
    assert isinstance(results, list)
    # Check that the results are tuples of (filename, snippet)
    if results:
        assert all(isinstance(item, tuple) and len(item) == 2 for item in results)
        assert all(isinstance(fname, str) and isinstance(snippet, str) for fname, snippet in results)
    
def test_ask_question_runs():
    result = ask_question("What does STA WSYNC do?", model=DEFAULT_MODEL)
    assert isinstance(result, str)
    assert len(result) > 0

def test_llm_factory():
    """Test that we can get different LLM implementations."""
    from ask_docs.llm import get_llm
    from ask_docs.llm.base import BaseLLM
    
    # Test default model
    llm = get_llm(DEFAULT_MODEL)
    assert isinstance(llm, BaseLLM)
    
    # Test other models if needed
    # (We'll just check that they return an instance - actual API calls require keys)
    models = ["openai", "ollama", "claude", "gemini", "groq"]
    for model in models:
        llm = get_llm(model)
        assert isinstance(llm, BaseLLM)