# tests/test_integrations.py
import os
import pytest

from Lucien import chat_groq, chat_ollama

@pytest.mark.skipif(os.getenv("GROQ_API_KEY") is None, reason="GROQ key not set")
def test_groq_api_connection():
    try:
        out = chat_groq([{"role": "user", "content": "ping"}])
        assert isinstance(out, str) and len(out) > 0
    except RuntimeError as e:
        if "404" in str(e) or "401" in str(e):
            pytest.skip(f"API connection failed: {e}")
        else:
            raise

@pytest.mark.skipif(os.getenv("OLLAMA_URL") is None, reason="Ollama not configured")
def test_ollama_api_connection():
    try:
        out = chat_ollama([{"role": "user", "content": "ping"}])
        assert isinstance(out, str) and len(out) > 0
    except RuntimeError as e:
        if "404" in str(e) or "Connection" in str(e):
            pytest.skip(f"Ollama not available: {e}")
        else:
            raise
