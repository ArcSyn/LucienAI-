
import sys
import os
import json
from typing import Optional, Dict, Any
from pathlib import Path

# Add repo root to sys.path only if needed; document why.
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from core.file_ops import list_files, read_file, write_file, append_to_file, delete_file, rename_file, copy_file, move_file
from core.code_execution import run_python_code
from core.file_extended import exists, size, batch_rename, zip_folder, unzip_file, replace_text, count_lines, find_large
from core.system_extended import disk_space, cpu_usage, shell, rand_pass, open_url, open_file_in_vscode
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration & Environment ---
# Prefer environment variables. Optionally support .env if python-dotenv is installed.
def _getenv(name: str, default: Optional[str] = None) -> Optional[str]:
    val = os.getenv(name)
    if val is None:
        return default
    return val

# OpenAI-compatible Groq endpoint
GROQ_API_URL = _getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
OLLAMA_URL   = _getenv("OLLAMA_URL",   "http://localhost:11434/api/chat")

# NEVER hardcode secrets; rotate if previously committed.
GROQ_API_KEY = _getenv("GROQ_API_KEY")  # required if using Groq

# Feature flags
USE_INTERNET = _getenv("USE_INTERNET", "true").lower() == "true"
DEFAULT_TIMEOUT = 30  # seconds

HEADERS_GROQ = {
    "Authorization": f"Bearer {GROQ_API_KEY}" if GROQ_API_KEY else "",
    "Content-Type": "application/json",
    "User-Agent": "LucienCLI/1.0 (+https://github.com/ArcSyn/LucienCLI)"
}

# Validate required configuration
if not GROQ_API_KEY:
    print("⚠️ Warning: GROQ_API_KEY not found in environment variables.")
    print("Please create a .env file with your API key or set it as an environment variable.")
    print("See .env.example for template.")

# Path to Lucien's memory file:
MEMORY_FILE = _getenv("MEMORY_FILE", "lucien_memory.json")

# Lucien's system prompt
system_prompt = """
You are Lucien, a modern wizard AI coding assistant.
Keep responses concise and practical.
"""

# ============
# MEMORY HANDLING
# ============

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(mem):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2)

memory = load_memory()

# ============
# LLM HANDLERS
# ============



# ============
# IMPROVED LLM HANDLERS (Generic API functions)
# ============

def chat_groq(messages, model="llama3-8b", temperature=0.2) -> str:
    """
    Calls Groq's OpenAI-compatible chat API and returns assistant content.
    Raises RuntimeError with readable message on failures.
    """
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set. Export it or add to your environment.")
    import requests
    payload = {"model": model, "messages": messages, "temperature": float(temperature)}
    try:
        resp = requests.post(GROQ_API_URL, json=payload, headers=HEADERS_GROQ, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        try:
            data = resp.json()
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Groq: invalid JSON response: {e}") from e
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Groq: unexpected response format: {data}") from e
    except requests.RequestException as e:
        raise RuntimeError(f"Groq request failed: {e}") from e

def chat_ollama(messages, model="llama3", temperature=0.2) -> str:
    """
    Calls local Ollama chat endpoint and returns assistant content.
    """
    import requests
    payload = {"model": model, "messages": messages, "options": {"temperature": float(temperature)}}
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()
        try:
            result = r.json()
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Ollama: invalid JSON response: {e}") from e
        try:
            return result["message"]["content"]
        except KeyError as e:
            raise RuntimeError(f"Ollama: unexpected response format: {result}") from e
    except requests.RequestException as e:
        raise RuntimeError(f"Ollama request failed: {e}") from e

# ============
# COMMAND ROUTER
# ============

COMMANDS = {}

def command(name):
    """Decorator to register commands in the router."""
    def _wrap(fn):
        COMMANDS[name] = fn
        return fn
    return _wrap

@command("remember")
def cmd_remember(args: str) -> None:
    """Persist a memory entry: remember <text>"""
    text = args.strip()
    if not text:
        print("Usage: remember <text>")
        return
    memory.setdefault("notes", []).append(text)
    save_memory(memory)
    print("✅ Memory saved.")

@command("show memory")
def cmd_show_memory(args: str) -> None:
    """Show all saved memories"""
    notes = memory.get("notes", [])
    if notes:
        for i, note in enumerate(notes, 1):
            print(f"{i}. {note}")
    else:
        print("No memories saved yet.")

@command("clear memory")
def cmd_clear_memory(args: str) -> None:
    """Clear all saved memories"""
    memory["notes"] = []
    save_memory(memory)
    print("✅ Memory cleared.")

@command("list files")
def cmd_list_files(args: str) -> None:
    """List files in directory: list files [path]"""
    path = args.strip() if args.strip() else "."
    print(list_files(path))

@command("read file")
def cmd_read_file(args: str) -> None:
    """Read file contents: read file <path>"""
    if not args.strip():
        print("Usage: read file <path>")
        return
    print(read_file(args.strip()))

@command("write file")
def cmd_write_file(args: str) -> None:
    """Write content to file: write file <path>"""
    if not args.strip():
        print("Usage: write file <path>")
        return
    print("Enter text. Empty line to finish.")
    text = "\n".join(iter(input, ""))
    print(write_file(args.strip(), text))

@command("delete file")
def cmd_delete_file(args: str) -> None:
    """Delete a file: delete file <path>"""
    if not args.strip():
        print("Usage: delete file <path>")
        return
    if input(f"Delete {args.strip()}? (y/n): ").lower() == "y":
        print(delete_file(args.strip()))
    else:
        print("Cancelled.")

@command("disk space")
def cmd_disk_space(args: str) -> None:
    """Show disk space usage"""
    print(disk_space())

@command("cpu usage")
def cmd_cpu_usage(args: str) -> None:
    """Show CPU usage"""
    print(cpu_usage())

@command("run shell")
def cmd_run_shell(args: str) -> None:
    """Run shell command: run shell <command>"""
    if not args.strip():
        print("Usage: run shell <command>")
        return
    print(shell(args.strip()))

@command("generate password")
def cmd_generate_password(args: str) -> None:
    """Generate random password: generate password [length]"""
    try:
        length = int(args.strip()) if args.strip() else 16
        print(rand_pass(length))
    except ValueError:
        print("Usage: generate password [length] (length must be a number)")

@command("open url")
def cmd_open_url(args: str) -> None:
    """Open URL in browser: open url <url>"""
    if not args.strip():
        print("Usage: open url <url>")
        return
    print(open_url(args.strip()))

@command("open file")
def cmd_open_file(args: str) -> None:
    """Open file in VS Code: open file <path>"""
    if not args.strip():
        print("Usage: open file <path>")
        return
    print(open_file_in_vscode(args.strip()))

@command("run python")
def cmd_run_python(args: str) -> None:
    """Execute Python code interactively"""
    print("Enter Python code. Blank line to execute.")
    code = "\n".join(iter(input, ""))
    out = run_python_code(code)
    print(out["stdout"], out["stderr"])

@command("ai")
def cmd_ai(args: str) -> None:
    """AI chat with specific provider: ai <provider:groq|ollama> <prompt>"""
    parts = args.split(maxsplit=1)
    if len(parts) < 2:
        print("Usage: ai <groq|ollama> <prompt>")
        return
    provider, prompt = parts[0], parts[1]
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    try:
        if provider == "groq":
            out = chat_groq(messages, model="llama3-70b-8192", temperature=0.5)
        elif provider == "ollama":
            out = chat_ollama(messages, model="llama3", temperature=0.5)
        else:
            print("Provider must be 'groq' or 'ollama'")
            return
        print(out)
    except RuntimeError as e:
        print(f"❌ {e}")

@command("help")
def cmd_help(args: str) -> None:
    """Show available commands"""
    print("Available commands:")
    print("  Memory:")
    print("    remember <text>     - Save a memory note")
    print("    show memory         - Display all saved memories")
    print("    clear memory        - Clear all memories")
    print("  Files:")
    print("    list files [path]   - List files in directory")
    print("    read file <path>    - Read file contents")
    print("    write file <path>   - Write content to file")
    print("    delete file <path>  - Delete a file")
    print("  System:")
    print("    disk space          - Show disk usage")
    print("    cpu usage           - Show CPU usage")
    print("    run shell <cmd>     - Execute shell command")
    print("    generate password [len] - Generate random password")
    print("    open url <url>      - Open URL in browser")
    print("    open file <path>    - Open file in VS Code")
    print("    run python          - Execute Python code")
    print("  AI:")
    print("    ai <provider> <prompt> - Chat with specific AI provider")
    print("    (any other text)    - Chat with default AI")
    print("  Control:")
    print("    internet on/off     - Toggle internet mode")
    print("    quit/exit/bye       - Exit Lucien")
    print("    help                - Show this help")

def dispatch(line: str) -> None:
    """Dispatch command to appropriate handler."""
    if not line:
        return
    
    # Handle special cases first
    if line.lower() in ["quit", "exit", "bye"]:
        print("Farewell, brave wizard.")
        save_memory(memory)
        return "EXIT"
    
    # Try to find exact command match first
    name, *rest = line.split(maxsplit=1)
    args = rest[0] if rest else ""
    
    # Check for exact command match
    fn = COMMANDS.get(name)
    if fn:
        fn(args)
        return
    
    # Check for commands with spaces (like "show memory")
    for cmd_name, fn in COMMANDS.items():
        if line.startswith(cmd_name + " "):
            args = line[len(cmd_name):].strip()
            fn(args)
            return
    
    # Fallback to AI chat
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": line}
        ]
        
        if USE_INTERNET:
            resp = chat_groq(messages, model="llama3-70b-8192", temperature=0.5)
        else:
            resp = chat_ollama(messages, model="llama3", temperature=0.5)
        print(resp)
    except RuntimeError as e:
        print(f"⚠️ {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

# ============
# MAIN LOOP
# ============

def main():
    """Main interactive loop for Lucien AI."""
    global USE_INTERNET  # Declare once at the top to cover all branches
    
    print("""
+======================================+
|         L U C I E N   A I            |
|     Wizard of the ArcSyn Order       |
+======================================+
""")

    print("*** Lucien stands ready. Type your command or 'quit' to exit. ***")
    print("Type 'help' for available commands.")

    try:
        while True:
            try:
                line = input("You >>> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nFarewell, brave wizard.")
                save_memory(memory)
                break
            
            if line.lower() == "internet on":
                USE_INTERNET = True
                print("✅ Internet mode ON.")
                continue
            if line.lower() == "internet off":
                USE_INTERNET = False
                print("✅ Internet mode OFF.")
                continue
            
            result = dispatch(line)
            if result == "EXIT":
                break

    except KeyboardInterrupt:
        print("\nFarewell, brave wizard.")
        save_memory(memory)

if __name__ == "__main__":
    main()