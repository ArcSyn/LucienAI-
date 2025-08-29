# code_execution.py

import subprocess
import tempfile
import os
import re

# Dangerous imports and functions to block
BLOCKED_IMPORTS = [
    'os', 'sys', 'subprocess', 'shutil', 'importlib', '__import__',
    'eval', 'exec', 'compile', 'open', 'file', 'input', 'raw_input'
]

BLOCKED_PATTERNS = [
    r'__.*__',  # Dunder methods
    r'\..*os.*',  # OS access through modules
    r'subprocess',
    r'system\(',
    r'popen\(',
    r'eval\(',
    r'exec\(',
    r'compile\(',
]

def _validate_code(code):
    """Validate Python code to prevent dangerous operations."""
    if not code or not code.strip():
        raise ValueError("Code cannot be empty")
    
    if len(code) > 10000:  # 10KB limit
        raise ValueError("Code too long (limit: 10KB)")
    
    # Check for blocked imports
    for blocked in BLOCKED_IMPORTS:
        if re.search(rf'\b{re.escape(blocked)}\b', code, re.IGNORECASE):
            raise ValueError(f"Blocked import/function: {blocked}")
    
    # Check for blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE):
            raise ValueError(f"Blocked pattern detected: {pattern}")
    
    return code

def run_python_code(code):
    """
    Safely execute Python code in a subprocess with security restrictions.

    Args:
        code (str): Python code to execute.

    Returns:
        dict: stdout and stderr as strings.
    """
    try:
        # Validate code before execution
        validated_code = _validate_code(code)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(validated_code)
            temp_filename = temp_file.name

        try:
            result = subprocess.run(
                ["python", temp_filename],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=tempfile.gettempdir()  # Run in temp directory
            )
            stdout = result.stdout
            stderr = result.stderr
        except subprocess.TimeoutExpired:
            stdout = ""
            stderr = "⚠️ Code execution timeout (10 seconds)"
        except Exception as e:
            stdout = ""
            stderr = f"⚠️ Execution error: {e}"
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_filename)
            except:
                pass

        return {"stdout": stdout, "stderr": stderr}
    
    except ValueError as e:
        return {"stdout": "", "stderr": f"⚠️ Security validation failed: {e}"}