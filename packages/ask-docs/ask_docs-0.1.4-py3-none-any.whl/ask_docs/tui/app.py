"""Textual TUI application for AskDocs."""
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, Input, Button, Select, Static, Label, TextArea, OptionList, LoadingIndicator

from ask_docs.config import get_config, get_default_model
from ask_docs.main import ask_question, preview_matches, get_kb_info
from ask_docs.core import build_knowledge_base

class ResultScreen(Screen):
    """Screen to display the result of a query."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
    ]
    
    def __init__(self, question: str, answer: str, matches: list, model: str):
        """Initialize the result screen.
        
        Args:
            question: The question that was asked
            answer: The answer from the LLM
            matches: List of matching documents
            model: The model used for the answer
        """
        super().__init__()
        self.question = question
        self.answer = answer
        self.matches = matches
        self.model = model
    
    def compose(self) -> ComposeResult:
        """Compose the result screen."""
        yield Header(show_clock=True)
        
        with Container(id="result-container"):
            yield Label(f"Question: {self.question}", classes="question")
            
            yield Label("Answer:", classes="section-header")
            with Container(classes="answer-container"):
                yield Static(self.answer, classes="answer")
            
            yield Label("Sources:", classes="section-header")
            with Container(classes="sources-container"):
                if not self.matches:
                    yield Static("No matching documents found.")
                else:
                    for filename, snippet in self.matches:
                        with Container(classes="source-item"):
                            yield Label(filename, classes="source-filename")
                            yield Static(snippet, classes="source-snippet")
            
            yield Label(f"Model: {self.model}", classes="model-info")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.title = "AskDocs - Result"


class PreviewScreen(Screen):
    """Screen to display document matches for a query."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
    ]
    
    def __init__(self, question: str, matches: list):
        """Initialize the preview screen.
        
        Args:
            question: The question for the preview
            matches: List of matching documents
        """
        super().__init__()
        self.question = question
        self.matches = matches
    
    def compose(self) -> ComposeResult:
        """Compose the preview screen."""
        yield Header(show_clock=True)
        
        with Container(id="preview-container"):
            yield Label(f"Preview matches for: {self.question}", classes="question")
            
            with Container(classes="matches-container"):
                if not self.matches:
                    yield Static("No matching documents found.")
                else:
                    for filename, snippet in self.matches:
                        with Container(classes="match-item"):
                            yield Label(filename, classes="match-filename")
                            yield Static(snippet, classes="match-snippet")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.title = "AskDocs - Preview Matches"


class LoadingScreen(ModalScreen):
    """Loading screen with a message."""
    
    def __init__(self, message: str = "Processing..."):
        """Initialize the loading screen.
        
        Args:
            message: The message to display
        """
        super().__init__()
        self.message = message
    
    def compose(self) -> ComposeResult:
        """Compose the loading screen."""
        with Container(classes="loading-container"):
            yield LoadingIndicator()
            yield Static(self.message, classes="loading-message")


class KBInfoScreen(Screen):
    """Screen to display knowledge base information."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("b", "build_kb", "Build KB"),
    ]
    
    def __init__(self):
        """Initialize the KB info screen."""
        super().__init__()
        self.kb_info = {}
    
    def compose(self) -> ComposeResult:
        """Compose the KB info screen."""
        yield Header(show_clock=True)
        
        with Container(id="kb-info-container"):
            yield Label("Knowledge Base Information", classes="screen-title")
            
            with Container(id="kb-info-content"):
                # Content will be populated in on_mount
                pass
            
            with Horizontal(classes="buttons"):
                yield Button("Build KB", id="build-kb-button", variant="primary")
                yield Button("Back", id="back-button")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.title = "AskDocs - Knowledge Base Info"
        self.update_kb_info()
    
    def update_kb_info(self) -> None:
        """Update the KB info content."""
        self.kb_info = get_kb_info()
        
        # Clear existing content
        content = self.query_one("#kb-info-content")
        content.remove_children()
        
        # Add new content
        source_dir = self.kb_info.get("source_dir", "")
        content.mount(Label(f"Source Directory: {source_dir}", classes="kb-info-item"))
        
        doc_count = self.kb_info.get("doc_count", 0)
        content.mount(Label(f"Document Count: {doc_count}", classes="kb-info-item"))
        
        kb_exists = self.kb_info.get("kb_exists", False)
        if kb_exists:
            metadata = self.kb_info.get("metadata", {})
            chunk_count = metadata.get("num_chunks", 0)
            content.mount(Label(f"Chunk Count: {chunk_count}", classes="kb-info-item"))
            
            embedding_model = metadata.get("embedding_model", "None (using lexical search)")
            content.mount(Label(f"Embedding Model: {embedding_model}", classes="kb-info-item"))
            
            content.mount(Label("Status: Knowledge base is built", classes="kb-info-status success"))
        else:
            content.mount(Label("Status: Knowledge base not built", classes="kb-info-status error"))
            content.mount(Label("Run 'Build KB' to create the knowledge base.", classes="kb-info-hint"))
    
    def action_build_kb(self) -> None:
        """Build the knowledge base."""
        async def build_kb_task() -> None:
            # Show loading screen
            loading = LoadingScreen("Building knowledge base...")
            self.app.push_screen(loading)
            
            try:
                # Build the knowledge base
                build_knowledge_base()
                
                # Update KB info
                self.update_kb_info()
            finally:
                # Remove loading screen
                self.app.pop_screen()
        
        self.run_worker(build_kb_task())
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "build-kb-button":
            self.action_build_kb()
        elif event.button.id == "back-button":
            self.app.pop_screen()


class AskDocsApp(App):
    """AskDocs TUI application."""
    
    TITLE = "AskDocs"
    SUB_TITLE = "Document Assistant"
    CSS_PATH = "style.css"
    
    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
        Binding("q", "quit", "Quit"),
        Binding("k", "show_kb_info", "KB Info"),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the app layout."""
        yield Header(show_clock=True)
        
        with Container(id="main-container"):
            yield Label("Ask a question about your documentation", classes="intro")
            
            with Container(id="input-container"):
                yield Input(placeholder="Enter your question...", id="question-input")
                
                with Horizontal(id="controls"):
                    with Vertical(id="model-selector"):
                        yield Label("Model:")
                        yield Select(
                            [(model, model) for model in ["openai", "claude", "gemini", "groq", "ollama"]],
                            value=get_default_model(),
                            id="model-select"
                        )
                    
                    with Vertical(id="template-selector"):
                        yield Label("Template:")
                        yield Select(
                            [
                                ("Default", ""),
                                ("Isolation", "isolation"),
                                ("Complementary", "complementary"),
                                ("Supplementary", "supplementary")
                            ],
                            value="",
                            id="template-select"
                        )
                
                with Horizontal(id="buttons"):
                    yield Button("Ask", id="ask-button", variant="primary")
                    yield Button("Preview Matches", id="preview-button")
                    yield Button("KB Info", id="kb-info-button")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.title = "AskDocs - Document Assistant"
        self.query_one("#question-input").focus()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "ask-button":
            await self.ask_question()
        elif event.button.id == "preview-button":
            await self.preview_matches()
        elif event.button.id == "kb-info-button":
            self.action_show_kb_info()
    
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submitted events."""
        if event.input.id == "question-input":
            await self.ask_question()
    
    async def ask_question(self) -> None:
        """Handle asking a question."""
        question = self.query_one("#question-input").value
        if not question:
            return
        
        model = self.query_one("#model-select").value
        template = self.query_one("#template-select").value
        
        async def ask_task() -> None:
            # Show loading screen
            loading = LoadingScreen("Asking question...")
            self.push_screen(loading)
            
            try:
                # Get answer from AskDocs
                answer = ask_question(question, model, template)
                
                # Get matching documents
                matches = preview_matches(question, 3)
                
                # Show result screen
                result_screen = ResultScreen(question, answer, matches, model)
                self.switch_screen(result_screen)
            except Exception as e:
                # Handle errors
                error_msg = f"Error: {str(e)}"
                self.notify(error_msg, title="Error", severity="error")
            finally:
                # Remove loading screen
                self.pop_screen()
        
        self.run_worker(ask_task())
    
    async def preview_matches(self) -> None:
        """Handle previewing matches."""
        question = self.query_one("#question-input").value
        if not question:
            return
        
        async def preview_task() -> None:
            # Show loading screen
            loading = LoadingScreen("Finding matches...")
            self.push_screen(loading)
            
            try:
                # Get matching documents
                matches = preview_matches(question, 5)
                
                # Show preview screen
                preview_screen = PreviewScreen(question, matches)
                self.switch_screen(preview_screen)
            except Exception as e:
                # Handle errors
                error_msg = f"Error: {str(e)}"
                self.notify(error_msg, title="Error", severity="error")
            finally:
                # Remove loading screen
                self.pop_screen()
        
        self.run_worker(preview_task())
    
    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark
    
    def action_show_kb_info(self) -> None:
        """Show knowledge base information."""
        self.push_screen(KBInfoScreen())


def run_app() -> None:
    """Run the AskDocs TUI app."""
    app = AskDocsApp()
    app.run()