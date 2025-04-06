"""Prompt builder for AskDocs."""
from typing import List, Dict, Any, Optional
from ask_docs.config import get_prompt_template

def build_prompt(
    chunks: List[Dict[str, Any]], 
    query: str,
    template_name: Optional[str] = None,
    additional_context: Optional[str] = None
) -> str:
    """Build a prompt to send to the LLM using the matched document chunks.
    
    Args:
        chunks: List of document chunks to include in the prompt
        query: The user's query
        template_name: Name of the template to use (isolation, complementary, or supplementary)
        additional_context: Additional context to include in the prompt
        
    Returns:
        A formatted prompt string
    """
    # Prepare the context from the chunks
    chunk_texts = []
    for c in chunks:
        # Format the chunk with metadata
        chunk_text = f"File: {c['filename']}\n{c['content']}"
        chunk_texts.append(chunk_text)
    
    # Join all chunks with clear separation
    context = "\n\n" + "\n\n".join(chunk_texts)
    
    # Add additional context if provided
    if additional_context:
        context = f"{additional_context}\n\n{context}"
    
    # Get the appropriate template
    template = get_prompt_template(template_name)
    
    # Format the template with the context and query
    prompt = template.format(context=context, query=query)
    
    return prompt

def build_evaluation_prompt(query: str, answer: str, chunks: List[Dict[str, Any]]) -> str:
    """Build a prompt for evaluating the relevance of document chunks.
    
    Args:
        query: The user's query
        answer: The generated answer
        chunks: The document chunks used to generate the answer
        
    Returns:
        A prompt for evaluating the relevance of the chunks
    """
    # Create a context string that includes all chunks with clear identifiers
    chunk_texts = []
    for i, c in enumerate(chunks):
        # Format the chunk with metadata
        chunk_text = f"DOCUMENT {i+1}: {c['filename']}\n{c['content']}"
        chunk_texts.append(chunk_text)
    
    context = "\n\n".join(chunk_texts)
    
    # Create the evaluation prompt
    return f"""
You are an expert at evaluating document relevance for question answering.

USER QUESTION: {query}

DOCUMENTS PROVIDED:
{context}

GENERATED ANSWER: 
{answer}

Please evaluate:
1. RELEVANCE SCORE (0-10): How relevant were the provided documents to answering the question?
2. COVERAGE SCORE (0-10): How much of the information needed to answer the question was present in the documents?
3. REFERENCE ANALYSIS: List which documents were referenced in the answer, and which were not used.
4. CONFIDENCE SCORE (0-10): Based on the documents and answer quality, how confident are you in this answer?
5. IMPROVEMENT SUGGESTIONS: What additional information would have improved the answer?

Provide your evaluation in JSON format:
"""