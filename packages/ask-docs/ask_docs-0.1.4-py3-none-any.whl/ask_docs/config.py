"""Configuration for AskDocs.

This module provides the configuration system for AskDocs, supporting both
configuration files (config.json) and environment variables.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default configuration values
DEFAULT_CONFIG = {
    # LLM Provider settings
    "llm": {
        "default_model": "openai",  # Default LLM provider to use
        "openai": {
            "model": "gpt-3.5-turbo"
        },
        "ollama": {
            "model": "llama3",
            "base_url": "http://localhost:11434"
        },
        "claude": {
            "model": "claude-3-haiku-20240307"
        },
        "gemini": {
            "model": "models/gemini-pro"
        },
        "groq": {
            "model": "mixtral-8x7b-32768"
        }
    },
    
    # RAG settings
    "rag": {
        "source_dir": "docs",  # Directory containing documents
        "chunk_size": 1000,    # Size of document chunks in characters
        "chunk_overlap": 200,  # Overlap between chunks in characters
        "embedding_model": "all-MiniLM-L6-v2",  # Default embedding model
        "kb_dir": ".kb",       # Subdirectory name for knowledge base files
    },
    
    # Prompt templates
    "prompts": {
        "default_template": "isolation",  # Which template to use by default
        "templates": {
            "isolation": """
You are a helpful assistant. Use the following files to help answer the question.
Do not use any other information beyond what is provided in these files.

{context}

Question: {query}
Answer:
""",
            "complementary": """
You are a helpful assistant. First, try to answer using the following files as references.
If these files don't contain the information needed to answer the question, then use your
general knowledge to provide the best possible answer.

{context}

Question: {query}
Answer:
""",
            "supplementary": """
You are a helpful assistant. Use both the following files AND your general knowledge
to provide the most helpful and accurate answer possible.

{context}

Question: {query}
Answer:
"""
        }
    },
    
    # Web interface settings
    "web": {
        "title": "AskDocs",
        "host": "0.0.0.0",
        "port": 8000,
        "debug": True
    },
    
    # CLI settings
    "cli": {
        "show_progress": True
    }
}

# Paths to search for config.json
CONFIG_PATHS = [
    Path.cwd() / "config.json",                 # Current directory
    Path.home() / ".docbuddy" / "config.json",  # User's home directory
    Path(__file__).parent.parent / "config.json"  # Package directory
]

# Loaded configuration
_config = None

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json and environment variables.
    
    Looks for config.json in several locations and merges with environment variables.
    Environment variables take precedence over the config file.
    
    Returns:
        Dict containing the configuration
    """
    global _config
    
    if _config is not None:
        return _config
    
    # Start with default config
    config = DEFAULT_CONFIG.copy()
    
    # Try to load from config.json
    for config_path in CONFIG_PATHS:
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    loaded_config = json.load(f)
                
                # Deep merge with default config
                _deep_merge(config, loaded_config)
                break
            except json.JSONDecodeError:
                print(f"Warning: Could not parse config file {config_path}")
    
    # Override with environment variables
    # LLM settings
    config["llm"]["default_model"] = os.getenv("DOCBUDDY_DEFAULT_MODEL", config["llm"]["default_model"])
    config["llm"]["openai"]["model"] = os.getenv("OPENAI_MODEL", config["llm"]["openai"]["model"])
    config["llm"]["ollama"]["model"] = os.getenv("OLLAMA_MODEL", config["llm"]["ollama"]["model"])
    config["llm"]["claude"]["model"] = os.getenv("CLAUDE_MODEL", config["llm"]["claude"]["model"])
    config["llm"]["gemini"]["model"] = os.getenv("GEMINI_MODEL", config["llm"]["gemini"]["model"])
    config["llm"]["groq"]["model"] = os.getenv("GROQ_MODEL", config["llm"]["groq"]["model"])
    
    # RAG settings
    config["rag"]["source_dir"] = os.getenv("DOCBUDDY_SOURCE_DIR", config["rag"]["source_dir"])
    
    # API keys
    config["llm"]["openai"]["api_key"] = os.getenv("OPENAI_API_KEY")
    config["llm"]["claude"]["api_key"] = os.getenv("CLAUDE_API_KEY")
    config["llm"]["gemini"]["api_key"] = os.getenv("GEMINI_API_KEY")
    config["llm"]["groq"]["api_key"] = os.getenv("GROQ_API_KEY")
    
    _config = config
    return config

def get_config() -> Dict[str, Any]:
    """Get the current configuration.
    
    Returns:
        Dict containing the configuration
    """
    return load_config()

def get_source_dir() -> str:
    """Get the document source directory.
    
    Returns:
        Path to the document source directory
    """
    config = get_config()
    return config["rag"]["source_dir"]

def get_prompt_template(template_name: Optional[str] = None) -> str:
    """Get a prompt template by name.
    
    Args:
        template_name: Name of the template to get, or None for default template
        
    Returns:
        The prompt template string
    """
    config = get_config()
    if template_name is None:
        template_name = config["prompts"]["default_template"]
    
    return config["prompts"]["templates"].get(
        template_name, 
        config["prompts"]["templates"]["isolation"]  # Fallback to isolation template
    )

def get_default_model() -> str:
    """Get the default LLM model.
    
    Returns:
        The default model name
    """
    config = get_config()
    return config["llm"]["default_model"]

def get_model_config(model_name: str) -> Dict[str, Any]:
    """Get configuration for a specific model.
    
    Args:
        model_name: Name of the model to get configuration for
        
    Returns:
        Dict containing the model configuration
    """
    config = get_config()
    return config["llm"].get(model_name, {})

def get_rag_config() -> Dict[str, Any]:
    """Get RAG configuration.
    
    Returns:
        Dict containing the RAG configuration
    """
    config = get_config()
    return config["rag"]

def _deep_merge(dest: Dict[str, Any], src: Dict[str, Any]) -> None:
    """Deep merge two dictionaries.
    
    Args:
        dest: Destination dictionary to merge into
        src: Source dictionary to merge from
    """
    for key, value in src.items():
        if key in dest and isinstance(dest[key], dict) and isinstance(value, dict):
            _deep_merge(dest[key], value)
        else:
            dest[key] = value

# Constants (for backward compatibility)
DEFAULT_MODEL = get_default_model()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
OLLAMA_MODEL = get_model_config("ollama").get("model", "llama3")
OPENAI_MODEL = get_model_config("openai").get("model", "gpt-3.5-turbo")
CLAUDE_MODEL = get_model_config("claude").get("model", "claude-3-haiku-20240307")
GEMINI_MODEL = get_model_config("gemini").get("model", "models/gemini-pro")
GROQ_MODEL = get_model_config("groq").get("model", "mixtral-8x7b-32768")