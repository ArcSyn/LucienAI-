# file_ops.py

import os
import shutil

def _validate_path(filepath):
    """Validate file path to prevent directory traversal attacks."""
    if not filepath:
        raise ValueError("File path cannot be empty")
    
    # Convert to absolute path and resolve any .. or . components
    abs_path = os.path.abspath(filepath)
    
    # Check for suspicious patterns
    if '..' in filepath or filepath.startswith('/') or ':' in filepath[1:]:
        # Allow : only as second character for Windows drive letters
        if not (len(filepath) > 1 and filepath[1] == ':' and filepath[0].isalpha()):
            raise ValueError("Invalid file path detected")
    
    return abs_path

def list_files(directory="."):
    try:
        # Basic validation for directory parameter
        if not directory or len(directory) > 260:  # Windows MAX_PATH limit
            return "⚠️ Invalid directory path"
        
        entries = os.listdir(directory)
        if not entries:
            return "This folder is empty."

        output = []
        for item in entries:
            if os.path.isdir(os.path.join(directory, item)):
                output.append(f"[DIR] {item}/")
            else:
                output.append(item)

        return "\n".join(output)

    except Exception as e:
        return f"⚠️ Error listing files: {e}"


def read_file(filepath):
    try:
        validated_path = _validate_path(filepath)
        
        # Check file size to prevent memory exhaustion
        file_size = os.path.getsize(validated_path)
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            return f"⚠️ File too large: {file_size} bytes (limit: 10MB)"
        
        with open(validated_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip():
            return "⚠️ The file is empty."

        return content

    except FileNotFoundError:
        return f"⚠️ File not found: {filepath}"
    except ValueError as e:
        return f"⚠️ Invalid path: {e}"
    except Exception as e:
        return f"⚠️ Error reading file: {e}"


def write_file(filepath, text):
    try:
        validated_path = _validate_path(filepath)
        
        # Validate content size
        if len(text) > 10 * 1024 * 1024:  # 10MB limit
            return f"⚠️ Content too large: {len(text)} bytes (limit: 10MB)"
        
        with open(validated_path, "w", encoding="utf-8") as f:
            f.write(text)
        return f"✅ File {filepath} has been saved."
    except ValueError as e:
        return f"⚠️ Invalid path: {e}"
    except Exception as e:
        return f"⚠️ Error writing file: {e}"


def append_to_file(filepath, text):
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(text)
        return f"✅ Text appended to {filepath}."
    except Exception as e:
        return f"⚠️ Error appending to file: {e}"


def delete_file(filepath):
    try:
        os.remove(filepath)
        return f"✅ File {filepath} has been deleted."
    except FileNotFoundError:
        return f"⚠️ File not found: {filepath}"
    except Exception as e:
        return f"⚠️ Error deleting file: {e}"


def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        return f"✅ File renamed to {new_name}."
    except Exception as e:
        return f"⚠️ Error renaming file: {e}"


def copy_file(source, destination):
    try:
        shutil.copy2(source, destination)
        return f"✅ File copied to {destination}."
    except Exception as e:
        return f"⚠️ Error copying file: {e}"


def move_file(source, destination):
    try:
        shutil.move(source, destination)
        return f"✅ File moved to {destination}."
    except Exception as e:
        return f"⚠️ Error moving file: {e}"