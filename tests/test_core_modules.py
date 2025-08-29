# tests/test_core_modules.py
import pytest
import tempfile
import os
from pathlib import Path

from core.file_ops import list_files, read_file, write_file, delete_file
from core.system_extended import rand_pass, disk_space, cpu_usage

def test_file_operations():
    """Test basic file operations"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        test_file = f.name
        test_content = "Hello, Lucien!"
    
    try:
        # Test write_file
        result = write_file(test_file, test_content)
        assert "saved" in result.lower()
        
        # Test read_file
        content = read_file(test_file)
        assert test_content in content
        
        # Test list_files (should include our test file)
        files = list_files(os.path.dirname(test_file))
        assert os.path.basename(test_file) in files
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            delete_file(test_file)

def test_system_functions():
    """Test system utility functions"""
    # Test password generation
    password = rand_pass(10)
    assert len(password) == 10
    assert isinstance(password, str)
    
    # Test disk space (should return a string)
    disk_info = disk_space()
    assert isinstance(disk_info, str)
    assert "GB" in disk_info or "MB" in disk_info
    
    # Test CPU usage (should return a string)
    cpu_info = cpu_usage()
    assert isinstance(cpu_info, str)
    assert "CPU" in cpu_info

def test_file_ops_error_handling():
    """Test error handling in file operations"""
    # Test reading non-existent file
    result = read_file("nonexistent_file_12345.txt")
    assert "not found" in result.lower() or "error" in result.lower()
    
    # Test listing non-existent directory
    result = list_files("nonexistent_directory_12345")
    assert "error" in result.lower()
