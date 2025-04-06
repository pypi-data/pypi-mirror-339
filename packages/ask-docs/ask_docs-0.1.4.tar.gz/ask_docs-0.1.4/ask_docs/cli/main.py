"""Command-line interface for AskDocs."""
import os
import sys
import typer
import json
from typing import Optional
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich.json import JSON
from rich.progress import Progress, SpinnerColumn, TextColumn

from ask_docs.core import (
    ask_question, 
    preview_matches, 
    build_or_rebuild_kb, 
    get_kb_info
)
from ask_docs.config import (
    get_config, 
    get_default_model, 
    get_source_dir, 
    get_rag_config
)

# Create the main app with subcommands
app = typer.Typer(
    help="AskDocs: A document assistant powered by LLMs and RAG",
    add_completion=False,
)

# Create subcommands
tui_app = typer.Typer(help="Terminal User Interface for AskDocs")
web_app = typer.Typer(help="Web Interface for AskDocs")

# Add the subcommands to the main app
app.add_typer(tui_app, name="tui")
app.add_typer(web_app, name="web")

@app.command()
def ask(
    question: str, 
    model: str = typer.Option(None, "--model", "-m", help="LLM model to use (openai, ollama, claude, gemini, groq)"),
    rebuild: bool = typer.Option(False, "--rebuild", "-r", help="Rebuild knowledge base before answering"),
    template: str = typer.Option(None, "--template", "-t", help="Prompt template to use (isolation, complementary, supplementary)"),
    evaluate: bool = typer.Option(False, "--evaluate", "-e", help="Evaluate answer quality and confidence"),
    source_dir: str = typer.Option(None, "--source-dir", "-d", help="Source directory for documents"),
    output_json: bool = typer.Option(False, "--json", "-j", help="Output results as JSON"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show verbose output")
):
    """Ask a question about your documents."""
    console = Console()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        progress.add_task(description="Processing question...", total=None)
        result = ask_question(
            question=question, 
            model=model, 
            rebuild_kb=rebuild,
            template_name=template,
            evaluate=evaluate,
            source_dir=source_dir
        )
    
    # Output as JSON if requested
    if output_json:
        print(json.dumps(result, indent=2))
        return
    
    # Print rich formatted output
    answer = result["answer"]
    model_used = result["model"]
    
    print("\n[yellow]Question:[/yellow]")
    print(f"{question}")
    
    print("\n[yellow]Answer:[/yellow]")
    print(f"{answer}")
    
    # Print source information if verbose
    if verbose:
        print("\n[yellow]Sources:[/yellow]")
        for chunk in result["chunks"]:
            print(Panel(chunk["snippet"], title=chunk["filename"], expand=False))
    
    # Print evaluation if available
    if "evaluation" in result:
        eval_data = result["evaluation"]
        
        if "error" in eval_data:
            # If JSON parsing failed
            print("\n[yellow]Evaluation (raw):[/yellow]")
            print(eval_data["raw"])
        else:
            # Print structured evaluation
            print("\n[yellow]Evaluation:[/yellow]")
            
            eval_table = Table(show_header=False)
            eval_table.add_column("Metric", style="cyan")
            eval_table.add_column("Value")
            
            # Add all evaluation metrics to the table
            for key, value in eval_data.items():
                if isinstance(value, (str, int, float)):
                    eval_table.add_row(key.replace("_", " ").title(), str(value))
            
            console.print(eval_table)
            
            # Print any complex fields separately
            for key, value in eval_data.items():
                if isinstance(value, (dict, list)):
                    print(f"\n[cyan]{key.replace('_', ' ').title()}:[/cyan]")
                    print(JSON(json.dumps(value)))
    
    # Print model information
    print(f"\n[dim]Model: {model_used}[/dim]")

@app.command()
def list_models():
    """List available LLM models."""
    config = get_config()
    
    print("\n[yellow]Available LLM Models:[/yellow]")
    
    table = Table()
    table.add_column("Provider", style="cyan")
    table.add_column("Model")
    table.add_column("API Key Set", style="green")
    
    for provider, provider_config in config["llm"].items():
        if provider == "default_model":
            continue
            
        # Check if this provider has an API key configured
        api_key_set = "✓" if provider_config.get("api_key") else "✗"
        if provider == "ollama":
            api_key_set = "N/A (local)"
            
        model_name = provider_config.get("model", "unknown")
        
        # Mark the default provider
        if provider == config["llm"]["default_model"]:
            provider = f"{provider} (default)"
            
        table.add_row(provider, model_name, api_key_set)
    
    console = Console()
    console.print(table)
    
    print("\n[dim]Set the default model in config.json or with DOCBUDDY_DEFAULT_MODEL env var[/dim]")

@app.command()
def preview(
    question: str,
    top_n: int = typer.Option(4, "--top", "-n", help="Number of top matches to return"),
    source_dir: str = typer.Option(None, "--source-dir", "-d", help="Source directory for documents"),
    output_json: bool = typer.Option(False, "--json", "-j", help="Output results as JSON")
):
    """Preview the top matching documents for a question."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Finding matches...", total=None)
        matches = preview_matches(question, top_n, source_dir)
    
    # Output as JSON if requested
    if output_json:
        json_result = [{"filename": fname, "snippet": snippet} for fname, snippet in matches]
        print(json.dumps(json_result, indent=2))
        return
    
    print("\n[yellow]Question:[/yellow]")
    print(f"{question}")
    
    print("\n[yellow]Top Matches:[/yellow]")
    if not matches:
        print("[italic]No matches found.[/italic]")
    else:
        for fname, snippet in matches:
            print(Panel(snippet.strip(), title=fname, expand=False))

@app.command()
def build_kb(
    save_embeddings: bool = typer.Option(True, "--save-embeddings/--no-save-embeddings", 
                                        help="Save embeddings for future use"),
    chunk_size: int = typer.Option(None, "--chunk-size", "-c", 
                                  help="Size of document chunks"),
    chunk_overlap: int = typer.Option(None, "--chunk-overlap", "-o", 
                                     help="Overlap between chunks"),
    embedding_model: str = typer.Option(None, "--embedding-model", "-m", 
                                       help="Embedding model to use for semantic search"),
    force: bool = typer.Option(False, "--force", "-f", 
                              help="Force rebuild even if no changes detected"),
    source_dir: str = typer.Option(None, "--source-dir", "-d",
                                   help="Source directory for documents")
):
    """Build or rebuild the knowledge base.
    
    This command processes all documents in your source directory, 
    splits them into chunks, and optionally computes embeddings for semantic search.
    """
    console = Console()
    config = get_rag_config()
    
    if source_dir is None:
        source_dir = config["source_dir"]
    if chunk_size is None:
        chunk_size = config["chunk_size"]
    if chunk_overlap is None:
        chunk_overlap = config["chunk_overlap"]
    if embedding_model is None:
        embedding_model = config["embedding_model"]
    
    print("[yellow]Building knowledge base...[/yellow]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
        console=console
    ) as progress:
        task = progress.add_task(description="Processing documents...", total=None)
        
        # Show configuration
        progress.console.print(f"[cyan]Configuration:[/cyan]")
        progress.console.print(f"  Source directory: {source_dir}")
        progress.console.print(f"  Chunk size: {chunk_size}")
        progress.console.print(f"  Chunk overlap: {chunk_overlap}")
        progress.console.print(f"  Embedding model: {embedding_model}")
        progress.console.print("")
        
        num_chunks = build_or_rebuild_kb(
            save_embeddings=save_embeddings,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            embedding_model=embedding_model,
            force=force,
            source_dir=source_dir
        )
        
        progress.update(task, description="Knowledge base built successfully!")
    
    print(f"[green]Knowledge base built with {num_chunks} chunks.[/green]")
    
    # Explain what was done
    if save_embeddings:
        print("[cyan]Embeddings saved to disk. Future queries will be faster![/cyan]")
    else:
        print("[cyan]Embeddings were computed but not saved to disk.[/cyan]")
    
    # Print path info
    kb_dir = config.get("kb_dir", ".kb")
    print(f"\n[yellow]Knowledge base location:[/yellow]")
    print(f"{source_dir}/{kb_dir}/knowledge_base.json")

@app.command()
def check_embedding_libs():
    """Check if embedding libraries are installed."""
    libraries = []
    
    # Check for numpy
    try:
        import numpy
        libraries.append("[green]numpy: Installed[/green]")
    except ImportError:
        libraries.append("[red]numpy: Not installed[/red]")
    
    # Check for sentence-transformers
    try:
        import sentence_transformers
        libraries.append("[green]sentence-transformers: Installed[/green]")
        
        # Show available models
        print("\n[yellow]Available Embedding Models (sample):[/yellow]")
        print("- all-MiniLM-L6-v2 (default, fast)")
        print("- all-mpnet-base-v2 (more accurate, slower)")
        print("- paraphrase-multilingual-MiniLM-L12-v2 (multilingual)")
    except ImportError:
        libraries.append("[red]sentence-transformers: Not installed[/red] (needed for semantic search)")
    
    print("\n[yellow]Embedding Libraries:[/yellow]")
    for lib in libraries:
        print(lib)
    
    if any("[red]" in lib for lib in libraries):
        print("\n[yellow]Install semantic search dependencies with:[/yellow]")
        print("pip install docbuddy[embeddings]")
        print("\nor manually:")
        print("pip install numpy sentence-transformers")
        
@app.command()
def kb_info(
    source_dir: str = typer.Option(None, "--source-dir", "-d", help="Source directory for documents"),
    output_json: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
):
    """Show information about the current knowledge base."""
    info = get_kb_info(source_dir)
    
    # Output as JSON if requested
    if output_json:
        print(json.dumps(info, indent=2))
        return
    
    console = Console()
    source_dir = info["source_dir"]
    
    print(f"[yellow]Knowledge Base Information:[/yellow]")
    print(f"Source directory: {source_dir}")
    
    if not info["kb_exists"]:
        print("[yellow]No knowledge base found.[/yellow]")
        print("Run 'docbuddy build-kb' to build a knowledge base.")
        
        # Print document info if available
        if info["doc_count"] > 0:
            print(f"\nDocuments in source directory: {info['doc_count']}")
            
            if info["sample_docs"]:
                print("\n[cyan]Sample documents:[/cyan]")
                for doc in info["sample_docs"]:
                    print(f"- {doc}")
                
                if info["doc_count"] > len(info["sample_docs"]):
                    print(f"... and {info['doc_count'] - len(info['sample_docs'])} more")
        else:
            print("\n[red]No documents found in source directory.[/red]")
            print(f"Add documents to {source_dir} and then run 'docbuddy build-kb'")
        
        return
    
    # Knowledge base exists
    kb_size = info.get("kb_size_mb", 0)
    print(f"Knowledge base size: {kb_size:.2f} MB")
    
    if not info["metadata_exists"]:
        print("[yellow]No metadata file found for the knowledge base.[/yellow]")
        print("This may be an older format knowledge base. Rebuild recommended.")
    else:
        metadata = info.get("metadata", {})
        
        if metadata:
            # Create a nice table for the metadata
            table = Table(title="Knowledge Base Metadata")
            table.add_column("Property", style="cyan")
            table.add_column("Value")
            
            # Add the metadata fields
            created_at = metadata.get("created_at", 0)
            if created_at:
                import time
                table.add_row("Created", time.ctime(created_at))
                
            table.add_row("Documents", str(metadata.get("num_docs", "Unknown")))
            table.add_row("Chunks", str(metadata.get("num_chunks", "Unknown")))
            table.add_row("Chunk Size", str(metadata.get("chunk_size", "Unknown")))
            table.add_row("Chunk Overlap", str(metadata.get("chunk_overlap", "Unknown")))
            
            embedding_model = metadata.get("embedding_model")
            if embedding_model:
                table.add_row("Embedding Model", embedding_model)
            else:
                table.add_row("Embedding Model", "[yellow]None (using lexical search)[/yellow]")
                
            console.print(table)
    
    # Print document info
    print(f"\nDocuments in source directory: {info['doc_count']}")
    
    if info["sample_docs"]:
        print("\n[cyan]Sample documents:[/cyan]")
        for doc in info["sample_docs"]:
            print(f"- {doc}")
        
        if info["doc_count"] > len(info["sample_docs"]):
            print(f"... and {info['doc_count'] - len(info['sample_docs'])} more")

@app.command()
def config_info(
    output_json: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
):
    """Show configuration information."""
    config = get_config()
    
    # Output as JSON if requested
    if output_json:
        print(json.dumps(config, indent=2))
        return
    
    console = Console()
    
    print(f"[yellow]Configuration Information:[/yellow]")
    
    # Show LLM configuration
    table = Table(title="LLM Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value")
    
    table.add_row("Default Model", config["llm"]["default_model"])
    for provider, provider_config in config["llm"].items():
        if provider == "default_model":
            continue
            
        if isinstance(provider_config, dict) and "model" in provider_config:
            table.add_row(f"{provider.title()} Model", provider_config["model"])
    
    console.print(table)
    
    # Show RAG configuration
    table = Table(title="RAG Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value")
    
    for key, value in config["rag"].items():
        table.add_row(key.replace("_", " ").title(), str(value))
    
    console.print(table)
    
    # Show prompt template configuration
    table = Table(title="Prompt Templates")
    table.add_column("Template", style="cyan")
    table.add_column("Description")
    
    default_template = config["prompts"]["default_template"]
    
    for template_name in config["prompts"]["templates"]:
        description = ""
        if template_name == "isolation":
            description = "Uses only document knowledge"
        elif template_name == "complementary":
            description = "Uses documents first, then general knowledge if needed"
        elif template_name == "supplementary":
            description = "Combines document knowledge with general knowledge"
            
        # Mark the default template
        if template_name == default_template:
            template_name = f"{template_name} (default)"
            
        table.add_row(template_name, description)
    
    console.print(table)
    
    # Show configuration sources
    print("\n[yellow]Configuration Sources:[/yellow]")
    print("Default: Built-in defaults")
    
    for path in [os.path.expanduser("~/.docbuddy/config.json"), "config.json"]:
        if os.path.exists(path):
            print(f"File: {path}")
    
    print("Environment: Environment variables take precedence")

# TUI subcommand
@tui_app.callback(invoke_without_command=True)
def tui_main(
    ctx: typer.Context,
):
    """Launch the Terminal User Interface for AskDocs."""
    # Only continue if this is the command being invoked
    if ctx.invoked_subcommand is None:
        try:
            # Import the run_app function from the TUI module
            from ask_docs.tui.app import run_app
            # Run the TUI app
            run_app()
        except ImportError:
            print("[red]Error: Textual library is required for the TUI.[/red]")
            print("Install it with: [bold]pip install textual>=0.52.1[/bold]")
            sys.exit(1)
        except Exception as e:
            print(f"[red]Error launching TUI: {str(e)}[/red]")
            sys.exit(1)


# Web subcommand
@web_app.callback(invoke_without_command=True)
def web_main(
    ctx: typer.Context,
    host: str = typer.Option(None, "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(None, "--port", "-p", help="Port to listen on"),
):
    """Launch the Web Interface for AskDocs."""
    # Only continue if this is the command being invoked
    if ctx.invoked_subcommand is None:
        try:
            # Import the serve_app function from the web module
            from ask_docs.web.app import serve_app
            # Run the web app
            serve_app(host=host, port=port)
        except ImportError:
            print("[red]Error: FastHTML is required for the web interface.[/red]")
            print("Install it with: [bold]pip install python-fasthtml[/bold]")
            sys.exit(1)
        except Exception as e:
            print(f"[red]Error launching web interface: {str(e)}[/red]")
            sys.exit(1)


if __name__ == "__main__":
    app()