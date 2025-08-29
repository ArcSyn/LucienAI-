# tests/test_spells.py
import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

# Import the functions we want to test
from Lucien import (
    cmd_record_spell, cmd_stop_recording, cmd_cast_spell, 
    cmd_list_spells, cmd_delete_spell, load_spells, save_spells
)

class TestSpells:
    
    def setup_method(self):
        """Setup for each test method"""
        # Create a temporary directory for spells
        self.temp_dir = tempfile.mkdtemp()
        self.spells_file = Path(self.temp_dir) / ".lucien" / "spells.json"
        self.spells_file.parent.mkdir(exist_ok=True)
        
        # Mock the SPELLS_FILE path
        with patch('Lucien.SPELLS_FILE', self.spells_file):
            self.patcher = patch('Lucien.SPELLS_FILE', self.spells_file)
            self.mock_spells_file = self.patcher.start()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        self.patcher.stop()
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_spells_empty(self):
        """Test loading spells when file doesn't exist"""
        spells = load_spells()
        assert spells == {}
    
    def test_load_spells_with_data(self):
        """Test loading spells with existing data"""
        test_spells = {
            "test_spell": {
                "commands": ["echo hello", "echo world"],
                "description": "Test spell",
                "created": "2025-01-01T00:00:00",
                "count": 2
            }
        }
        
        with open(self.spells_file, "w") as f:
            json.dump(test_spells, f)
        
        spells = load_spells()
        assert spells == test_spells
    
    def test_save_spells(self):
        """Test saving spells to file"""
        test_spells = {
            "test_spell": {
                "commands": ["echo hello"],
                "description": "Test spell",
                "created": "2025-01-01T00:00:00",
                "count": 1
            }
        }
        
        success = save_spells(test_spells)
        assert success is True
        
        with open(self.spells_file, "r") as f:
            saved_spells = json.load(f)
        
        assert saved_spells == test_spells
    
    @patch('Lucien.recording_spell', None)
    @patch('Lucien.recorded_commands', [])
    def test_record_spell_success(self):
        """Test starting to record a spell"""
        with patch('Lucien.load_spells') as mock_load:
            mock_load.return_value = {}
            
            from io import StringIO
            import sys
            captured_output = StringIO()
            sys.stdout = captured_output
            
            cmd_record_spell("test_spell")
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            assert "🎬 Recording spell 'test_spell'" in output
    
    @patch('Lucien.recording_spell', None)
    @patch('Lucien.recorded_commands', [])
    def test_record_spell_already_exists(self):
        """Test recording a spell that already exists"""
        existing_spells = {"test_spell": {"commands": [], "description": "existing"}}
        
        with patch('Lucien.load_spells') as mock_load:
            mock_load.return_value = existing_spells
            
            from io import StringIO
            import sys
            captured_output = StringIO()
            sys.stdout = captured_output
            
            cmd_record_spell("test_spell")
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            assert "⚠️ Spell 'test_spell' already exists" in output
    
    @patch('Lucien.recording_spell', 'test_spell')
    @patch('Lucien.recorded_commands', ['echo hello', 'echo world'])
    def test_stop_recording_success(self):
        """Test stopping recording with commands"""
        with patch('Lucien.load_spells') as mock_load, \
             patch('Lucien.save_spells') as mock_save:
            mock_load.return_value = {}
            mock_save.return_value = True
            
            from io import StringIO
            import sys
            captured_output = StringIO()
            sys.stdout = captured_output
            
            cmd_stop_recording("")
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            assert "✅ Spell 'test_spell' saved with 2 commands" in output
            mock_save.assert_called_once()
    
    @patch('Lucien.recording_spell', None)
    def test_stop_recording_no_recording(self):
        """Test stopping recording when not recording"""
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cmd_stop_recording("")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        assert "❌ No spell being recorded" in output
    
    def test_cast_spell_success(self):
        """Test casting an existing spell"""
        test_spell = {
            "commands": ["echo hello", "echo world"],
            "description": "Test spell",
            "created": "2025-01-01T00:00:00",
            "count": 2
        }
        
        with patch('Lucien.load_spells') as mock_load, \
             patch('Lucien.dispatch') as mock_dispatch:
            mock_load.return_value = {"test_spell": test_spell}
            
            from io import StringIO
            import sys
            captured_output = StringIO()
            sys.stdout = captured_output
            
            cmd_cast_spell("test_spell")
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            assert "🔮 Casting spell 'test_spell' (2 commands)..." in output
            assert "✅ Spell 'test_spell' completed!" in output
            assert mock_dispatch.call_count == 2
    
    def test_cast_spell_not_found(self):
        """Test casting a non-existent spell"""
        with patch('Lucien.load_spells') as mock_load:
            mock_load.return_value = {}
            
            from io import StringIO
            import sys
            captured_output = StringIO()
            sys.stdout = captured_output
            
            cmd_cast_spell("nonexistent")
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            assert "❌ Spell 'nonexistent' not found" in output
    
    def test_list_spells_empty(self):
        """Test listing spells when none exist"""
        with patch('Lucien.load_spells') as mock_load:
            mock_load.return_value = {}
            
            from io import StringIO
            import sys
            captured_output = StringIO()
            sys.stdout = captured_output
            
            cmd_list_spells("")
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            assert "No spells recorded yet." in output
    
    def test_list_spells_with_data(self):
        """Test listing spells with existing data"""
        test_spells = {
            "test_spell": {
                "commands": ["echo hello"],
                "description": "Test spell",
                "created": "2025-01-01T00:00:00",
                "count": 1
            }
        }
        
        with patch('Lucien.load_spells') as mock_load:
            mock_load.return_value = test_spells
            
            from io import StringIO
            import sys
            captured_output = StringIO()
            sys.stdout = captured_output
            
            cmd_list_spells("")
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            assert "Available spells:" in output
            assert "📜 test_spell" in output
    
    def test_delete_spell_success(self):
        """Test deleting an existing spell"""
        test_spells = {
            "test_spell": {
                "commands": ["echo hello"],
                "description": "Test spell",
                "created": "2025-01-01T00:00:00",
                "count": 1
            }
        }
        
        with patch('Lucien.load_spells') as mock_load, \
             patch('Lucien.save_spells') as mock_save:
            mock_load.return_value = test_spells
            mock_save.return_value = True
            
            from io import StringIO
            import sys
            captured_output = StringIO()
            sys.stdout = captured_output
            
            cmd_delete_spell("test_spell")
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            assert "✅ Spell 'test_spell' deleted" in output
            mock_save.assert_called_once()
    
    def test_delete_spell_not_found(self):
        """Test deleting a non-existent spell"""
        with patch('Lucien.load_spells') as mock_load:
            mock_load.return_value = {}
            
            from io import StringIO
            import sys
            captured_output = StringIO()
            sys.stdout = captured_output
            
            cmd_delete_spell("nonexistent")
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            assert "❌ Spell 'nonexistent' not found" in output
