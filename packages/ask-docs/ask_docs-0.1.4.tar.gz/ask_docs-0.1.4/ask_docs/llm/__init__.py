from ask_docs.llm.openai_llm import OpenAI_LLM
from ask_docs.llm.ollama_llm import OllamaLLM
from ask_docs.llm.anthropic_llm import ClaudeLLM
from ask_docs.llm.gemini_llm import GeminiLLM
from ask_docs.llm.groq_llm import GroqLLM

def get_llm(model: str):
    if model == "openai":
        return OpenAI_LLM()
    elif model == "ollama":
        return OllamaLLM()
    elif model == "claude":
        return ClaudeLLM()
    elif model == "gemini":
        return GeminiLLM()
    elif model == "groq":
        return GroqLLM()
    else:
        raise ValueError(f"Unsupported model: {model}")