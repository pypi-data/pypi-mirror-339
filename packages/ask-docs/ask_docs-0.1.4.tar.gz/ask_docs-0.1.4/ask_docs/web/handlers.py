"""FastHTML request handlers for AskDocs web interface."""
from fasthtml.common import *
from ask_docs.main import ask_question, preview_matches
from ask_docs.config import get_config
from ask_docs.core import kb_info

def get_index(request):
    """Render the index page."""
    config = get_config()
    web_config = config.get("web", {})
    title = web_config.get("title", "AskDocs")
    
    return render_template(
        "index.html", 
        title=title,
        default_model=config["llm"]["default_model"]
    )

def post_question(request):
    """Process a question from the user."""
    question = request.form.get("question", "")
    model = request.form.get("model", None)
    template = request.form.get("template", None)
    
    if not question:
        return render_template(
            "index.html",
            title=get_config().get("web", {}).get("title", "AskDocs"),
            default_model=get_config()["llm"]["default_model"],
            error="Please enter a question"
        )
    
    try:
        # Get the answer
        answer = ask_question(question, model, template)
        
        # Get the matching documents
        matches = preview_matches(question, 3)
        
        # Format matches for template
        match_data = [{"filename": fname, "snippet": snippet} for fname, snippet in matches]
        
        return render_template(
            "index.html",
            title=get_config().get("web", {}).get("title", "AskDocs"),
            default_model=get_config()["llm"]["default_model"],
            question=question,
            answer=answer.replace("\n", "<br>"),
            model=model or get_config()["llm"]["default_model"],
            template=template,
            matches=match_data
        )
    except Exception as e:
        return render_template(
            "index.html",
            title=get_config().get("web", {}).get("title", "AskDocs"),
            default_model=get_config()["llm"]["default_model"],
            question=question,
            model=model,
            template=template,
            error=f"Error: {str(e)}"
        )

def get_model_info(request):
    """Get information about available models."""
    config = get_config()
    
    models = {}
    for provider, provider_config in config["llm"].items():
        if provider == "default_model":
            continue
            
        models[provider] = {
            "model": provider_config.get("model", ""),
            "api_key_set": bool(provider_config.get("api_key")) if provider != "ollama" else True
        }
    
    return render_template(
        "model_info.html",
        title=config.get("web", {}).get("title", "AskDocs") + " - Models",
        default_model=config["llm"]["default_model"],
        models=models
    )

def get_templates(request):
    """Get available prompt templates."""
    config = get_config()
    
    templates = {}
    for name, template in config["prompts"]["templates"].items():
        templates[name] = template
    
    return render_template(
        "templates.html",
        title=config.get("web", {}).get("title", "AskDocs") + " - Templates",
        default_template=config["prompts"]["default_template"],
        templates=templates
    )

def get_preview(request):
    """Preview matching documents for a question."""
    question = request.args.get("question", "")
    top_k = int(request.args.get("top_k", "3"))
    
    if not question:
        return render_template(
            "index.html",
            title=get_config().get("web", {}).get("title", "AskDocs"),
            default_model=get_config()["llm"]["default_model"],
            error="Please enter a question to preview matches"
        )
    
    try:
        matches = preview_matches(question, top_k)
        match_data = [{"filename": fname, "snippet": snippet} for fname, snippet in matches]
        
        return render_template(
            "index.html",
            title=get_config().get("web", {}).get("title", "AskDocs"),
            default_model=get_config()["llm"]["default_model"],
            question=question,
            preview_matches=match_data
        )
    except Exception as e:
        return render_template(
            "index.html",
            title=get_config().get("web", {}).get("title", "AskDocs"),
            default_model=get_config()["llm"]["default_model"],
            question=question,
            error=f"Error: {str(e)}"
        )

def get_kb_status(request):
    """Get knowledge base status."""
    info = kb_info()
    
    return render_template(
        "kb_status.html",
        title=get_config().get("web", {}).get("title", "AskDocs") + " - Knowledge Base",
        kb_exists=info.get("kb_exists", False),
        document_count=info.get("doc_count", 0),
        chunk_count=info.get("metadata", {}).get("num_chunks", 0),
        embedding_model=info.get("metadata", {}).get("embedding_model", None),
        source_dir=info.get("source_dir", "")
    )