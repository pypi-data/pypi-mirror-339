"""Base class for all LLM implementations."""
from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Base class that all LLM implementations must inherit from."""
    
    @abstractmethod
    def ask(self, prompt: str) -> str:
        """Send a prompt to the LLM and return the response.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            The LLM's response as a string
        """
        pass