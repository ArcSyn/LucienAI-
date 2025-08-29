# tests/test_git_integration.py
import pytest
from unittest.mock import patch, MagicMock
import subprocess

# Import the functions we want to test
from Lucien import cmd_git_status, cmd_git_add, cmd_git_commit, cmd_git_push, cmd_git_pull, cmd_git_log

class TestGitIntegration:
    
    @patch('subprocess.run')
    def test_git_status_clean(self, mock_run):
        """Test git status when working directory is clean"""
        mock_run.return_value = MagicMock(
            stdout="",
            stderr="",
            returncode=0
        )
        
        # Capture print output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cmd_git_status("")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        assert "✅ Working directory clean" in output
        mock_run.assert_called_once_with(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, check=True
        )
    
    @patch('subprocess.run')
    def test_git_status_modified(self, mock_run):
        """Test git status when there are modified files"""
        mock_run.return_value = MagicMock(
            stdout=" M README.md\nA  new_file.py",
            stderr="",
            returncode=0
        )
        
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cmd_git_status("")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        assert "Modified files:" in output
        assert " M README.md" in output
        assert "A  new_file.py" in output
    
    @patch('subprocess.run')
    def test_git_add_success(self, mock_run):
        """Test git add with valid files"""
        mock_run.return_value = MagicMock(
            stdout="",
            stderr="",
            returncode=0
        )
        
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cmd_git_add("README.md test.py")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        assert "✅ Staged 2 file(s)" in output
        mock_run.assert_called_once_with(
            ["git", "add", "README.md", "test.py"],
            capture_output=True, text=True, check=True
        )
    
    @patch('subprocess.run')
    def test_git_add_no_files(self, mock_run):
        """Test git add with no files specified"""
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cmd_git_add("")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        assert "Usage: git add <files>" in output
        mock_run.assert_not_called()
    
    @patch('subprocess.run')
    def test_git_log_success(self, mock_run):
        """Test git log with commits"""
        mock_run.return_value = MagicMock(
            stdout="abc1234 feat: add new feature\ndef5678 fix: bug fix",
            stderr="",
            returncode=0
        )
        
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cmd_git_log("")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        assert "Recent commits:" in output
        assert "abc1234 feat: add new feature" in output
        mock_run.assert_called_once_with(
            ["git", "log", "--oneline", "-10"],
            capture_output=True, text=True, check=True
        )
    
    @patch('subprocess.run')
    def test_git_command_error(self, mock_run):
        """Test git command when git is not available"""
        mock_run.side_effect = FileNotFoundError()
        
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cmd_git_status("")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        assert "❌ Error: Git not installed" in output
    
    @patch('subprocess.run')
    def test_git_command_failure(self, mock_run):
        """Test git command when it fails"""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git", stderr="fatal: not a git repository")
        
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cmd_git_status("")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        assert "❌ Error: Not a git repository" in output
