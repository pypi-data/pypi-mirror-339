# Contributing to AskDocs

Thank you for considering contributing to AskDocs! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- A clear title and description
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Any relevant error messages or screenshots

### Suggesting Enhancements

Enhancement suggestions are welcome. Please include:

- A clear description of the enhancement
- The motivation for the enhancement
- How it would benefit users

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature
3. Add your changes
4. Run tests to ensure everything works
5. Submit a pull request

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ask-docs.git
   cd ask-docs
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run tests:
   ```bash
   pytest
   ```

4. Format code:
   ```bash
   ruff format .
   ```

5. Lint code:
   ```bash
   ruff check .
   ```

6. Clean up build artifacts after building/publishing:
   ```bash
   # Remove build artifacts
   python cleanup.py
   
   # Remove everything including knowledge base and config files
   python cleanup.py --all
   ```

## Project Structure

```
ask_docs/
├── core/               # Core functionality
├── llm/                # LLM integrations
├── cli/                # CLI interface
├── web/                # Web interface
└── tui/                # Text User Interface
```

### Adding a New LLM Provider

1. Create a new file in the `llm/` directory (e.g., `llm/new_provider_llm.py`)
2. Implement the `BaseLLM` interface
3. Update `llm/__init__.py` to include your new provider
4. Add any necessary configuration to `config.py`
5. Add tests for your new provider

### Extending the Web Interface

The web interface uses FastHTML. To add new features:

1. Add new handlers in `web/handlers.py`
2. Register routes in `web/app.py`
3. Add any necessary templates or static files

### Extending the TUI

The Text User Interface uses Textual. To add new features:

1. Modify the app in `tui/app.py`
2. Add new screens or widgets as needed
3. Update CSS styles in `tui/style.css`

## Documentation

Please document your code with docstrings following the Google Python Style Guide.

## Testing

- Write tests for new features
- Ensure all tests pass before submitting a pull request
- Add both unit tests and integration tests as appropriate

Thank you for contributing to AskDocs!