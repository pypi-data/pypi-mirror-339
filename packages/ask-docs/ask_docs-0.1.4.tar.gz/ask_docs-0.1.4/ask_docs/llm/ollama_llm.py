"""Ollama LLM implementation."""
import requests
from ask_docs.config import get_model_config
from ask_docs.llm.base import BaseLLM

class OllamaLLM(BaseLLM):
    """Ollama LLM implementation."""
    
    def __init__(self, model=None, base_url=None):
        """Initialize the Ollama LLM.
        
        Args:
            model: The Ollama model to use (defaults to config)
            base_url: The Ollama API base URL (defaults to config)
        """
        config = get_model_config("ollama")
        self.model = model or config.get("model", "llama3")
        self.base_url = base_url or config.get("base_url", "http://localhost:11434")
        self.api_url = f"{self.base_url}/api/generate"
    
    def ask(self, prompt: str) -> str:
        """Send a prompt to Ollama and return the response.
        
        Args:
            prompt: The prompt to send to Ollama
            
        Returns:
            The AI's response as a string
        """
        try:
            response = requests.post(
                self.api_url,
                json={"model": self.model, "prompt": prompt}
            )
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Error: Ollama returned status code {response.status_code}"
        except Exception as e:
            return f"Error with Ollama API: {str(e)}"