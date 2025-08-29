# Contributing to LucienAI

Thank you for your interest in contributing to LucienAI! This document provides guidelines for contributors.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LucienAI
   ```

2. **Set up development environment**
   ```bash
   # Option 1: Use the setup script
   python setup_dev.py
   
   # Option 2: Manual setup
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   cp env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

3. **Run tests**
   ```bash
   pytest -v
   ```

## Code Style

- Use 4 spaces for indentation (no tabs)
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Keep line length under 88 characters (Black default)

## Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Tests should skip gracefully if services are unavailable
- Use pytest markers for different test types:
  - `@pytest.mark.integration` for integration tests
  - `@pytest.mark.slow` for slow tests
  - `@pytest.mark.groq` for Groq API tests
  - `@pytest.mark.ollama` for Ollama tests

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest -v`
6. Run linting: `flake8 .`
7. Commit your changes: `git commit -m "Add feature description"`
8. Push to your fork: `git push origin feature/your-feature`
9. Submit a pull request

## Environment Variables

For local development, create a `.env` file with:

```ini
GROQ_API_KEY=your_groq_api_key_here
USE_INTERNET=true
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
OLLAMA_URL=http://localhost:11434/api/chat
MEMORY_FILE=lucien_memory.json
```

**Never commit your actual API keys to the repository!**

## Available Commands

- `make help` - Show available commands
- `make install` - Install dependencies
- `make test` - Run all tests
- `make test-quick` - Run tests excluding integration tests
- `make lint` - Run linting
- `make format` - Format code with Black
- `make clean` - Clean up cache files
- `make run` - Run Lucien AI
- `make setup` - Initial development setup

## Questions?

If you have questions about contributing, please open an issue on GitHub.
