"""Core functionality for AskDocs."""

from ask_docs.core.document_retrieval import (
    build_knowledge_base,
    get_matching_documents,
    kb_info
)
from ask_docs.core.query_processor import (
    process_query,
    ask_question,
    preview_matches,
    build_or_rebuild_kb,
    get_kb_info
)
from ask_docs.core.prompt_builder import build_prompt

__all__ = [
    "build_knowledge_base",
    "get_matching_documents",
    "process_query",
    "ask_question",
    "preview_matches",
    "build_or_rebuild_kb",
    "get_kb_info",
    "build_prompt",
    "kb_info"
]