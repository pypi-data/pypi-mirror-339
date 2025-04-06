"""Query processor for AskDocs."""
import os
import json
import time
from typing import List, Tuple, Dict, Any, Optional

from ask_docs.llm import get_llm
from ask_docs.core.document_retrieval import (
    load_documents,
    get_best_chunks,
    build_knowledge_base,
    load_knowledge_base
)
from ask_docs.core.prompt_builder import build_prompt, build_evaluation_prompt
from ask_docs.config import get_default_model, get_source_dir, get_rag_config

# Knowledge base cache to avoid reloading for multiple queries
_knowledge_base_cache = None

def get_knowledge_base(rebuild: bool = False) -> List[Dict[str, Any]]:
    """Get the knowledge base, loading or building it if necessary.
    
    Args:
        rebuild: Force rebuilding the knowledge base
        
    Returns:
        The knowledge base as a list of document chunks
    """
    global _knowledge_base_cache
    
    if _knowledge_base_cache is None or rebuild:
        try:
            # Try to load pre-built knowledge base first
            _knowledge_base_cache = load_knowledge_base()
        except Exception:
            # Fall back to building on the fly
            docs = load_documents()
            _knowledge_base_cache = get_best_chunks(docs, "")  # Empty query to just chunk documents
    
    return _knowledge_base_cache

def ask_question(
    question: str, 
    model: Optional[str] = None,
    rebuild_kb: bool = False,
    template_name: Optional[str] = None,
    evaluate: bool = False,
    source_dir: Optional[str] = None
) -> Dict[str, Any]:
    """Ask a question using the document knowledge base.
    
    Args:
        question: The question to ask
        model: The LLM model to use
        rebuild_kb: Whether to rebuild the knowledge base
        template_name: Which prompt template to use
        evaluate: Whether to evaluate confidence and relevance
        source_dir: Override the source directory
        
    Returns:
        Dictionary with answer and optionally evaluation metrics
    """
    # Use default model if not specified
    if model is None:
        model = get_default_model()
    
    # Get knowledge base
    global _knowledge_base_cache
    if source_dir is not None:
        # If source directory is specified, load from there
        kb = load_knowledge_base(source_dir)
    else:
        # Otherwise use cached knowledge base
        kb = get_knowledge_base(rebuild=rebuild_kb)
    
    # Get best chunks for this question
    chunks = get_best_chunks(kb, question)
    
    # Build prompt with the best chunks
    prompt = build_prompt(chunks, question, template_name)
    
    # Get LLM and ask the question
    llm = get_llm(model)
    answer = llm.ask(prompt)
    
    # Prepare result
    result = {
        "answer": answer,
        "model": model,
        "num_chunks": len(chunks),
        "chunks": [
            {"filename": c["filename"], "snippet": c["content"][:200] + "..."} 
            for c in chunks
        ]
    }
    
    # Evaluate answer if requested
    if evaluate:
        # Use the same LLM to evaluate the answer
        eval_prompt = build_evaluation_prompt(question, answer, chunks)
        eval_result = llm.ask(eval_prompt)
        
        # Try to parse JSON response
        try:
            # Extract JSON part of the response
            json_str = eval_result
            if "```json" in eval_result:
                json_str = eval_result.split("```json")[1].split("```")[0].strip()
            elif "```" in eval_result:
                json_str = eval_result.split("```")[1].strip()
                
            evaluation = json.loads(json_str)
            result["evaluation"] = evaluation
        except (json.JSONDecodeError, IndexError):
            # If JSON parsing fails, include the raw evaluation
            result["evaluation"] = {
                "raw": eval_result,
                "error": "Failed to parse evaluation as JSON"
            }
    
    return result

def preview_matches(
    question: str, 
    top_n: int = 4, 
    source_dir: Optional[str] = None
) -> List[Tuple[str, str]]:
    """Preview the top matching documents for a question.
    
    Args:
        question: The question to match against
        top_n: Number of top matches to return
        source_dir: Override the source directory
        
    Returns:
        List of (filename, snippet) tuples
    """
    # Get knowledge base
    if source_dir is not None:
        # If source directory is specified, load from there
        kb = load_knowledge_base(source_dir)
    else:
        # Otherwise use cached knowledge base
        kb = get_knowledge_base()
    
    # Get best chunks for this question
    chunks = get_best_chunks(kb, question, top_n)
    
    # Format the results
    return [
        (c["filename"], c["content"][:200] + ("..." if len(c["content"]) > 200 else "")) 
        for c in chunks
    ]

def build_or_rebuild_kb(
    save_embeddings: bool = True, 
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
    embedding_model: Optional[str] = None,
    force: bool = False,
    source_dir: Optional[str] = None
) -> int:
    """Build or rebuild the knowledge base.
    
    This function is useful for CLI commands or scheduled tasks
    to rebuild the knowledge base from scratch.
    
    Args:
        save_embeddings: Whether to save embeddings to disk
        chunk_size: Size of document chunks
        chunk_overlap: Overlap between chunks
        embedding_model: Name of the embedding model to use
        force: Force rebuild even if no changes detected
        source_dir: Override the source directory
        
    Returns:
        Number of chunks in the knowledge base
    """
    global _knowledge_base_cache
    
    # Force rebuild
    _knowledge_base_cache = None
    
    # Build knowledge base with embeddings if available
    kb = build_knowledge_base(
        source_dir=source_dir,
        save_embeddings=save_embeddings,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        embedding_model=embedding_model,
        force=force
    )
    
    # Update cache
    _knowledge_base_cache = kb
    
    return len(kb)

def process_query(
    question: str, 
    model: Optional[str] = None,
    template_name: Optional[str] = None,
    source_dir: Optional[str] = None
) -> str:
    """Process a query and return the answer.
    
    This is a simpler interface that just returns the answer string.
    
    Args:
        question: The question to ask
        model: The LLM model to use
        template_name: Which prompt template to use
        source_dir: Override the source directory
        
    Returns:
        The answer as a string
    """
    result = ask_question(
        question=question,
        model=model,
        template_name=template_name,
        source_dir=source_dir
    )
    
    return result["answer"]

def get_kb_info(source_dir: Optional[str] = None) -> Dict[str, Any]:
    """Get information about the knowledge base.
    
    Args:
        source_dir: Override the source directory
        
    Returns:
        Dictionary with information about the knowledge base
    """
    # Get configuration
    config = get_rag_config()
    if source_dir is None:
        source_dir = config["source_dir"]
    kb_dir = config.get("kb_dir", ".kb")
    
    # Ensure the source directory exists
    os.makedirs(source_dir, exist_ok=True)
    
    kb_path = os.path.join(source_dir, kb_dir, "knowledge_base.json")
    metadata_path = os.path.join(source_dir, kb_dir, "metadata.json")
    
    result = {
        "source_dir": source_dir,
        "kb_exists": os.path.exists(kb_path),
        "metadata_exists": os.path.exists(metadata_path),
    }
    
    if os.path.exists(kb_path):
        kb_size = os.path.getsize(kb_path) / (1024 * 1024)  # Size in MB
        result["kb_size_mb"] = kb_size
        
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                result["metadata"] = metadata
            except (json.JSONDecodeError, FileNotFoundError) as e:
                result["metadata_error"] = str(e)
    
    # Count documents
    doc_count = 0
    for root, _, files in os.walk(source_dir):
        if os.path.basename(root) == kb_dir:  # Skip .kb directory
            continue
        for file in files:
            if file.startswith("."):  # Skip hidden files
                continue
            doc_count += 1
    
    result["doc_count"] = doc_count
    
    # Get sample documents
    sample_docs = []
    for root, _, files in os.walk(source_dir):
        if os.path.basename(root) == kb_dir or len(sample_docs) >= 5:  # Skip .kb directory and limit to 5 samples
            continue
        for file in files:
            if file.startswith("."):  # Skip hidden files
                continue
            rel_path = os.path.relpath(os.path.join(root, file), source_dir)
            sample_docs.append(rel_path)
            if len(sample_docs) >= 5:
                break
    
    result["sample_docs"] = sample_docs
    
    return result