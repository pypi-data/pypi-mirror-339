"""Groq LLM implementation."""
import groq
from ask_docs.config import get_model_config
from ask_docs.llm.base import BaseLLM

class GroqLLM(BaseLLM):
    """Groq LLM implementation."""
    
    def __init__(self, model=None, api_key=None):
        """Initialize the Groq LLM.
        
        Args:
            model: The Groq model to use (defaults to config)
            api_key: The Groq API key (defaults to config)
        """
        config = get_model_config("groq")
        self.model = model or config.get("model", "mixtral-8x7b-32768")
        self.api_key = api_key or config.get("api_key")
        self.client = groq.Groq(api_key=self.api_key) if self.api_key else None
    
    def ask(self, prompt: str) -> str:
        """Send a prompt to Groq and return the response.
        
        Args:
            prompt: The prompt to send to Groq
            
        Returns:
            The AI's response as a string
        """
        if not self.api_key or not self.client:
            return "Error: Groq API key is not configured."
            
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error with Groq API: {str(e)}"