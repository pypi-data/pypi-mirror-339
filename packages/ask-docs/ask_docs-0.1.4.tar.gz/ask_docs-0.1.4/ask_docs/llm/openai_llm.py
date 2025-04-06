"""OpenAI LLM implementation."""
from openai import OpenAI
from ask_docs.config import get_model_config
from ask_docs.llm.base import BaseLLM

class OpenAI_LLM(BaseLLM):
    """OpenAI LLM implementation."""
    
    def __init__(self, model=None, api_key=None):
        """Initialize the OpenAI LLM.
        
        Args:
            model: The OpenAI model to use (defaults to config)
            api_key: The OpenAI API key (defaults to config)
        """
        config = get_model_config("openai")
        self.model = model or config.get("model", "gpt-3.5-turbo")
        self.api_key = api_key or config.get("api_key")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
    
    def ask(self, prompt: str) -> str:
        """Send a prompt to OpenAI and return the response.
        
        Args:
            prompt: The prompt to send to OpenAI
            
        Returns:
            The AI's response as a string
        """
        if not self.api_key or not self.client:
            return "Error: OpenAI API key is not configured."
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with OpenAI API: {str(e)}"