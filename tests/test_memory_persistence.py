# tests/test_memory_persistence.py
import pytest
import tempfile
import os
import json
from unittest.mock import patch

from Lucien import load_memory, save_memory

def test_memory_persistence():
    """Test memory save and load functionality"""
    # Create a temporary memory file with proper JSON content
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_memory_file = f.name
        # Write valid JSON to the file
        f.write('{"notes": []}')
    
    try:
        # Test with original memory file path
        with patch('Lucien.MEMORY_FILE', temp_memory_file):
            # Test loading existing memory
            memory = load_memory()
            assert isinstance(memory, dict)
            assert "notes" in memory
            
            # Test saving memory
            test_memory = {"notes": ["Test note 1", "Test note 2"]}
            save_memory(test_memory)
            
            # Test loading saved memory
            loaded_memory = load_memory()
            assert loaded_memory == test_memory
            assert "notes" in loaded_memory
            assert len(loaded_memory["notes"]) == 2
            
    finally:
        # Cleanup
        if os.path.exists(temp_memory_file):
            try:
                os.unlink(temp_memory_file)
            except:
                pass

def test_memory_file_not_exists():
    """Test loading memory when file doesn't exist"""
    with tempfile.TemporaryDirectory() as temp_dir:
        non_existent_file = os.path.join(temp_dir, "nonexistent_memory.json")
        
        with patch('Lucien.MEMORY_FILE', non_existent_file):
            memory = load_memory()
            assert isinstance(memory, dict)
            assert len(memory) == 0

def test_memory_save_load_cycle():
    """Test complete save/load cycle with complex data"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_memory_file = f.name
    
    try:
        with patch('Lucien.MEMORY_FILE', temp_memory_file):
            # Complex memory structure
            complex_memory = {
                "notes": ["Note 1", "Note 2", "Note 3"],
                "settings": {"theme": "dark", "language": "en"},
                "history": [{"timestamp": "2024-01-01", "action": "test"}]
            }
            
            # Save
            save_memory(complex_memory)
            
            # Load and verify
            loaded = load_memory()
            assert loaded == complex_memory
            assert loaded["notes"] == ["Note 1", "Note 2", "Note 3"]
            assert loaded["settings"]["theme"] == "dark"
            
    finally:
        if os.path.exists(temp_memory_file):
            os.unlink(temp_memory_file)
