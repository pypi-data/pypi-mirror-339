"""Google Gemini LLM implementation."""
import google.generativeai as genai
from ask_docs.config import get_model_config
from ask_docs.llm.base import BaseLLM

class GeminiLLM(BaseLLM):
    """Google Gemini LLM implementation."""
    
    def __init__(self, model=None, api_key=None):
        """Initialize the Gemini LLM.
        
        Args:
            model: The Gemini model to use (defaults to config)
            api_key: The Google Gemini API key (defaults to config)
        """
        config = get_model_config("gemini")
        self.model = model or config.get("model", "models/gemini-pro")
        self.api_key = api_key or config.get("api_key")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
    
    def ask(self, prompt: str) -> str:
        """Send a prompt to Gemini and return the response.
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            The AI's response as a string
        """
        if not self.api_key:
            return "Error: Google Gemini API key is not configured."
        
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error with Google Gemini API: {str(e)}"