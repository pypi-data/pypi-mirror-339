"""Document retrieval functions for AskDocs.

This module provides functions for loading documents, chunking them, and retrieving
the most relevant chunks for a given query using semantic search when available,
with fallback to lexical search.
"""
import difflib
import os
import time
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

from ask_docs.config import get_rag_config

# Default chunk size and overlap for text splitting
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

def load_documents(source_dir: Optional[str] = None, recursive: bool = True) -> List[Dict[str, str]]:
    """Load all documents from the source directory, including subdirectories.
    
    Args:
        source_dir: Directory containing the documents to load, or None to use configured dir
        recursive: Whether to recursively search subdirectories (default: True)
        
    Returns:
        List of dictionaries with filename and content
    """
    config = get_rag_config()
    if source_dir is None:
        source_dir = config["source_dir"]
    
    # Ensure the directory exists
    os.makedirs(source_dir, exist_ok=True)
    
    docs = []
    # Use ** for recursive glob if recursive=True, otherwise use *
    glob_pattern = "**/*" if recursive else "*"
    
    for path in Path(source_dir).glob(glob_pattern):
        if path.is_file():
            try:
                # Get relative path from source_dir for better identification
                rel_path = path.relative_to(source_dir)
                
                # Skip hidden files and directories
                if any(part.startswith('.') for part in path.parts):
                    continue
                
                text = path.read_text(encoding="utf-8")
                docs.append({
                    "filename": str(rel_path),
                    "content": text,
                    "filepath": str(path),
                    "file_type": path.suffix.lower()
                })
            except UnicodeDecodeError:
                # Skip binary files
                pass
    return docs

def split_text_into_chunks(text: str, chunk_size: int = None, 
                          chunk_overlap: int = None) -> List[str]:
    """Split text into overlapping chunks of specified size.
    
    Args:
        text: Text to split
        chunk_size: Maximum size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    # Get from config if not specified
    config = get_rag_config()
    if chunk_size is None:
        chunk_size = config.get("chunk_size", DEFAULT_CHUNK_SIZE)
    if chunk_overlap is None:
        chunk_overlap = config.get("chunk_overlap", DEFAULT_CHUNK_OVERLAP)
    
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        
        # Try to find a sentence break near the end
        if end < len(text):
            sentence_break = max(
                text.rfind('. ', start, end),
                text.rfind('? ', start, end),
                text.rfind('! ', start, end),
                text.rfind('\n', start, end)
            )
            
            if sentence_break != -1 and sentence_break > start + chunk_size // 2:
                end = sentence_break + 1
        
        chunks.append(text[start:end])
        
        # Move start to account for overlap
        start = start + chunk_size - chunk_overlap
    
    return chunks

def create_document_chunks(docs: List[Dict[str, str]], 
                          chunk_size: Optional[int] = None,
                          chunk_overlap: Optional[int] = None) -> List[Dict[str, Any]]:
    """Split documents into chunks for more precise retrieval.
    
    Args:
        docs: List of document dictionaries
        chunk_size: Size of document chunks
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of document chunk dictionaries
    """
    chunked_docs = []
    
    for doc in docs:
        text = doc["content"]
        chunks = split_text_into_chunks(text, chunk_size, chunk_overlap)
        
        for i, chunk in enumerate(chunks):
            chunked_docs.append({
                "filename": doc["filename"],
                "content": chunk,
                "chunk_id": i,
                "filepath": doc.get("filepath", ""),
                "file_type": doc.get("file_type", "")
            })
    
    return chunked_docs

def get_best_chunks_lexical(docs: List[Dict[str, str]], query: str, top_n: int = 4) -> List[Dict[str, Any]]:
    """Get the best matching chunks from the documents based on lexical similarity.
    
    Args:
        docs: List of documents to search
        query: Query string to match against
        top_n: Number of top matches to return
        
    Returns:
        List of the top matching documents
    """
    # Use difflib's SequenceMatcher for lexical similarity
    return sorted(
        docs, 
        key=lambda d: difflib.SequenceMatcher(None, query.lower(), d["content"].lower()).ratio(), 
        reverse=True
    )[:top_n]

def get_best_chunks(
    docs: List[Dict[str, str]], 
    query: str, 
    top_n: int = 4,
    embedding_model: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get the best matching chunks from the documents for a given query.
    
    This is the main retrieval function that attempts to use semantic search 
    if possible, falling back to lexical search if not.
    
    Args:
        docs: List of documents to search
        query: Query string to match against
        top_n: Number of top matches to return
        embedding_model: Name of the embedding model to use
        
    Returns:
        List of the top matching documents
    """
    # If docs is empty, return empty list
    if not docs:
        return []
    
    # Check if documents are already chunked
    if not any("chunk_id" in doc for doc in docs):
        docs = create_document_chunks(docs)
    
    # Get embedding model from config if not specified
    if embedding_model is None:
        config = get_rag_config()
        embedding_model = config.get("embedding_model", "all-MiniLM-L6-v2")
    
    try:
        # Try to use semantic search if embeddings libraries are available
        import numpy as np
        
        try:
            # Try to use SentenceTransformers if available
            from sentence_transformers import SentenceTransformer
            
            model = SentenceTransformer(embedding_model)
            query_embedding = model.encode(query)
            
            # Compute embeddings for all docs if not already embedded
            if not any("embedding" in doc for doc in docs):
                contents = [doc["content"] for doc in docs]
                embeddings = model.encode(contents)
                for i, doc in enumerate(docs):
                    doc["embedding"] = embeddings[i]
            
            # Compute cosine similarity
            for doc in docs:
                doc_embedding = doc["embedding"]
                similarity = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
                )
                doc["similarity"] = float(similarity)  # Convert to float for JSON serialization
            
            # Sort by similarity
            return sorted(docs, key=lambda d: d["similarity"], reverse=True)[:top_n]
            
        except ImportError:
            # Fall back to lexical search if no embedding library
            return get_best_chunks_lexical(docs, query, top_n)
    
    except ImportError:
        # Fall back to lexical search if numpy is not available
        return get_best_chunks_lexical(docs, query, top_n)
    
def build_knowledge_base(
    source_dir: Optional[str] = None, 
    save_embeddings: bool = True, 
    embedding_model: Optional[str] = None,
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
    force: bool = False
) -> Dict[str, Any]:
    """Build a knowledge base from documents in the source directory.
    
    Args:
        source_dir: Directory containing the documents to load
        save_embeddings: Whether to save embeddings for future use
        embedding_model: Name of the sentence-transformers model to use
        chunk_size: Size of document chunks
        chunk_overlap: Overlap between chunks
        force: Force rebuild even if no changes detected
        
    Returns:
        List of document chunk dictionaries
    """
    # Get configuration
    config = get_rag_config()
    if source_dir is None:
        source_dir = config["source_dir"]
    if embedding_model is None:
        embedding_model = config.get("embedding_model", "all-MiniLM-L6-v2")
    if chunk_size is None:
        chunk_size = config.get("chunk_size", DEFAULT_CHUNK_SIZE)
    if chunk_overlap is None:
        chunk_overlap = config.get("chunk_overlap", DEFAULT_CHUNK_OVERLAP)
    kb_dir = config.get("kb_dir", ".kb")
    
    # Ensure the source directory exists
    os.makedirs(source_dir, exist_ok=True)
    
    # Directory for KB files
    kb_path_dir = os.path.join(source_dir, kb_dir)
    os.makedirs(kb_path_dir, exist_ok=True)
    
    # File paths
    kb_path = os.path.join(kb_path_dir, "knowledge_base.json")
    metadata_path = os.path.join(kb_path_dir, "metadata.json")
    
    # Load documents
    docs = load_documents(source_dir, recursive=True)
    
    # Check if we need to rebuild by comparing hashes of document contents
    if not force and os.path.exists(kb_path) and os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            
            # Compute new hash of all documents
            doc_hash = hashlib.md5()
            for doc in docs:
                doc_hash.update(doc["content"].encode())
                doc_hash.update(doc["filename"].encode())
            current_hash = doc_hash.hexdigest()
            
            # If hash matches and parameters match, we can reuse existing KB
            if (metadata.get("hash") == current_hash and 
                metadata.get("embedding_model") == embedding_model and
                metadata.get("chunk_size") == chunk_size and
                metadata.get("chunk_overlap") == chunk_overlap):
                
                print(f"No changes detected in documents. Using existing knowledge base.")
                with open(kb_path, "r") as f:
                    return json.load(f)
                
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            # If any error occurs, rebuild the knowledge base
            pass
    
    # Create document chunks
    chunked_docs = create_document_chunks(docs, chunk_size, chunk_overlap)
    
    # Try to compute embeddings if available
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
        
        print(f"Computing embeddings using model: {embedding_model}")
        model = SentenceTransformer(embedding_model)
        
        # Compute embeddings for all chunks
        contents = [doc["content"] for doc in chunked_docs]
        embeddings = model.encode(contents)
        
        for i, doc in enumerate(chunked_docs):
            doc["embedding"] = embeddings[i].tolist()  # Convert to list for serialization
        
        # Save embeddings if requested
        if save_embeddings:
            # Save knowledge base
            with open(kb_path, "w") as f:
                json.dump(chunked_docs, f)
            
            # Compute hash of all documents for change detection
            doc_hash = hashlib.md5()
            for doc in docs:
                doc_hash.update(doc["content"].encode())
                doc_hash.update(doc["filename"].encode())
            
            # Save metadata
            metadata = {
                "hash": doc_hash.hexdigest(),
                "created_at": time.time(),
                "embedding_model": embedding_model,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "num_docs": len(docs),
                "num_chunks": len(chunked_docs),
                "source_dir": source_dir
            }
            
            with open(metadata_path, "w") as f:
                json.dump(metadata, f)
    
    except ImportError:
        # Continue without embeddings if libraries not available
        print("Warning: sentence-transformers not installed. Using lexical search only.")
        
        # Still save the chunked documents if requested
        if save_embeddings:
            with open(kb_path, "w") as f:
                json.dump(chunked_docs, f)
            
            # Compute hash for change detection
            doc_hash = hashlib.md5()
            for doc in docs:
                doc_hash.update(doc["content"].encode())
                doc_hash.update(doc["filename"].encode())
            
            # Save metadata without embedding info
            metadata = {
                "hash": doc_hash.hexdigest(),
                "created_at": time.time(),
                "embedding_model": None,  # No embedding model used
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "num_docs": len(docs),
                "num_chunks": len(chunked_docs),
                "source_dir": source_dir
            }
            
            with open(metadata_path, "w") as f:
                json.dump(metadata, f)
    
    return chunked_docs

def load_knowledge_base(source_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load a pre-built knowledge base if available, or build one if not.
    
    Args:
        source_dir: Directory containing the documents
        
    Returns:
        List of document chunk dictionaries
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
    
    if os.path.exists(kb_path):
        try:
            import json
            import numpy as np
            
            # Load the knowledge base
            with open(kb_path, "r") as f:
                chunked_docs = json.load(f)
            
            # Load metadata if available
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                print(f"Using knowledge base with {metadata.get('num_chunks', len(chunked_docs))} chunks")
                print(f"Created at: {time.ctime(metadata.get('created_at', 0))}")
                
                if metadata.get('embedding_model'):
                    print(f"Embedding model: {metadata.get('embedding_model')}")
                else:
                    print("No embeddings - using lexical search only")
            
            # Convert embedding lists back to numpy arrays if needed
            try:
                from sentence_transformers import SentenceTransformer
                for doc in chunked_docs:
                    if "embedding" in doc:
                        doc["embedding"] = np.array(doc["embedding"])
            except ImportError:
                pass
            
            return chunked_docs
            
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            # Fall back to building knowledge base if loading fails
            return build_knowledge_base(source_dir)
    else:
        print("No existing knowledge base found. Building...")
        # Build knowledge base if not found
        return build_knowledge_base(source_dir)

def kb_info(source_dir: Optional[str] = None) -> Dict[str, Any]:
    """Get information about the knowledge base.
    
    Args:
        source_dir: Directory containing the documents
        
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
    
    # Check for docs in the source directory
    docs = load_documents(source_dir, recursive=True)
    
    # Sample a few document paths for display
    sample_docs = [doc["filename"] for doc in docs[:5]]
    
    result = {
        "source_dir": source_dir,
        "doc_count": len(docs),
        "sample_docs": sample_docs,
        "kb_exists": os.path.exists(kb_path),
        "metadata_exists": os.path.exists(metadata_path)
    }
    
    # Add metadata if available
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            result["metadata"] = metadata
            result["kb_size_mb"] = os.path.getsize(kb_path) / (1024 * 1024)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    return result

def get_matching_documents(query: str, top_n: int = 3, source_dir: Optional[str] = None) -> List[Tuple[str, str]]:
    """Get matching documents for a query.
    
    Args:
        query: The query to match against documents
        top_n: Number of top matches to return
        source_dir: Directory containing the documents (optional)
        
    Returns:
        List of (filename, snippet) tuples
    """
    # Load the knowledge base
    chunks = load_knowledge_base(source_dir)
    
    # Get the best matching chunks
    best_chunks = get_best_chunks(chunks, query, top_n)
    
    # Return the best matches as (filename, content) tuples
    return [(chunk["filename"], chunk["content"]) for chunk in best_chunks]