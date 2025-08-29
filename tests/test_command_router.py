# tests/test_command_router.py
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

from Lucien import dispatch, COMMANDS, cmd_remember, cmd_show_memory, cmd_clear_memory, cmd_ai, cmd_help

def test_command_registration():
    """Test that commands are properly registered"""
    assert "remember" in COMMANDS
    assert "show memory" in COMMANDS
    assert "clear memory" in COMMANDS
    assert "help" in COMMANDS
    assert "ai" in COMMANDS

def test_dispatch_unknown_command():
    """Test dispatch with unknown command"""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        dispatch("unknown_command")
        output = fake_out.getvalue()
        # Should fall back to AI chat for unknown commands
        assert len(output) > 0

def test_dispatch_exit_commands():
    """Test dispatch with exit commands"""
    result = dispatch("quit")
    assert result == "EXIT"
    
    result = dispatch("exit")
    assert result == "EXIT"
    
    result = dispatch("bye")
    assert result == "EXIT"

def test_memory_commands():
    """Test memory-related commands"""
    # Test remember command
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cmd_remember("Test memory note")
        output = fake_out.getvalue()
        assert "Memory saved" in output
    
    # Test show memory command
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cmd_show_memory("")
        output = fake_out.getvalue()
        # Should show the memory we just saved
        assert "Test memory note" in output
    
    # Test clear memory command
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cmd_clear_memory("")
        output = fake_out.getvalue()
        assert "Memory cleared" in output

def test_command_with_spaces():
    """Test commands that contain spaces"""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        dispatch("show memory")
        output = fake_out.getvalue()
        # Should show memory output
        assert len(output) > 0

def test_ai_command():
    """Test AI command with different providers"""
    with patch('Lucien.chat_groq') as mock_groq, \
         patch('Lucien.chat_ollama') as mock_ollama, \
         patch('sys.stdout', new=StringIO()) as fake_out:
        
        mock_groq.return_value = "Groq response"
        mock_ollama.return_value = "Ollama response"
        
        # Test Groq
        cmd_ai("groq Hello")
        mock_groq.assert_called_once()
        
        # Test Ollama
        cmd_ai("ollama Hello")
        mock_ollama.assert_called_once()
        
        # Test invalid provider
        cmd_ai("invalid Hello")
        output = fake_out.getvalue()
        assert "Provider must be 'groq' or 'ollama'" in output

def test_help_command():
    """Test help command output"""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cmd_help("")
        output = fake_out.getvalue()
        assert "Available commands:" in output
        assert "Memory:" in output
        assert "Files:" in output
        assert "System:" in output
        assert "AI:" in output
        assert "Control:" in output

def test_command_argument_parsing():
    """Test command argument parsing"""
    # Test command with no arguments
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cmd_remember("")
        output = fake_out.getvalue()
        assert "Usage: remember" in output
    
    # Test command with arguments
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cmd_remember("Valid argument")
        output = fake_out.getvalue()
        assert "Memory saved" in output
