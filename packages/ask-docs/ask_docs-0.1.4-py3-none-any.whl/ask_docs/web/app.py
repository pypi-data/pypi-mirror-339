"""FastHTML web app for AskDocs."""
from fasthtml.common import *
from ask_docs.config import get_config
from ask_docs.web.handlers import (
    get_index,
    post_question,
    get_model_info,
    get_templates,
    get_preview,
    get_kb_status
)

def create_app():
    """Create and configure the FastHTML app.
    
    Returns:
        The configured FastHTML app
    """
    config = get_config()
    web_config = config.get("web", {})
    title = web_config.get("title", "AskDocs")
    debug = web_config.get("debug", True)
    
    # Initialize FastHTML app
    app, rt = fast_app(
        title=title,
        pico=True,  # Use Pico CSS for styling
        debug=debug,
    )
    
    # Routes - Server-side only, no JavaScript required
    rt("/")(get_index)
    rt("/ask", methods=["POST"])(post_question)
    rt("/model-info")(get_model_info)
    rt("/templates")(get_templates)
    rt("/preview")(get_preview)
    rt("/kb-status")(get_kb_status)
    
    # Add static file support (if using custom CSS or images)
    @app.route("/static/<path:path>")
    def static_files(path):
        from pathlib import Path
        from flask import send_from_directory
        static_dir = Path(__file__).parent / "static"
        return send_from_directory(static_dir, path)
    
    return app

def serve_app(host=None, port=None):
    """Serve the FastHTML app.
    
    Args:
        host: Host to serve on (defaults to config)
        port: Port to serve on (defaults to config)
    """
    config = get_config()
    web_config = config.get("web", {})
    
    if host is None:
        host = web_config.get("host", "0.0.0.0")
    
    if port is None:
        port = web_config.get("port", 8000)
    
    print(f"Starting AskDocs web server at http://{host}:{port}")
    print("Press Ctrl+C to stop the server")
    
    app = create_app()
    serve(app=app, host=host, port=port)

if __name__ == "__main__":
    serve_app()