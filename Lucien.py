import re
import requests
import psutil
from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import datetime
import subprocess

# Optional: Syntax highlighting
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import TerminalFormatter
    HAVE_PYGMENTS = True
except ImportError:
    HAVE_PYGMENTS = False

### NEW - Voice integration
try:
    import pyttsx3
    HAVE_VOICE = True
except ImportError:
    HAVE_VOICE = False

# --- Load .env from parent folder ---
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

groq_api_key = os.getenv("GROQ_API_KEY")

### NEW - ASCII banners
BANNER = """
╔══════════════════════════════════════╗
║         L U C I E N   A I             ║
║     Wizard of the ArcSyn Order        ║
╚══════════════════════════════════════╝
"""

def speak(text):
    if HAVE_VOICE:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        voices = engine.getProperty('voices')
        # You may need to change this index depending on your system
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()

def print_code(code, lang="python"):
    if HAVE_PYGMENTS:
        try:
            lexer = get_lexer_by_name(lang)
        except Exception:
            lexer = get_lexer_by_name("text")
        print(highlight(code, lexer, TerminalFormatter()))
    else:
        print(code)

def extract_code_blocks(text):
    pattern = r"```(\w+)?\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    blocks = []
    for lang, code in matches:
        blocks.append({"lang": lang or "plain", "code": code.strip()})
    # Fallback: if no code blocks but looks like code
    if not blocks and text.strip().startswith("import"):
        blocks.append({"lang": "python", "code": text.strip()})
    return blocks

def ask_groq(messages):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {groq_api_key}"
    }
    payload = {
        "model": "llama3-70b-8192",
        "temperature": 0.7,
        "max_tokens": 1024,
        "messages": messages
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"(╯°□°）╯︵ ┻━┻\nNoctel whispers: An error has occurred.\nDetails: {e}")
        return "Lucien encountered an error while consulting the cosmic runes."

def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    return f"🔮 Lucien reports CPU usage: {cpu_percent}%"

if __name__ == "__main__":
    print(BANNER)
    print("✨ By the runes of the ancients, Lucien stands ready, Master. ✨")
    if HAVE_VOICE:
        speak("By the runes of the ancients, Lucien stands ready, Master.")

    print(f"Current working directory: {os.getcwd()}")
    print(get_cpu_usage())
    print("\nType your incantation for Lucien, or type 'quit' to exit.")

    if not groq_api_key:
        print("⚠️ Noctel warns: GROQ_API_KEY not found in the ether. Exiting.")
        exit(1)

    # --- Chat history for context ---
    messages = [
        {
            "role": "system",
            "content": (
                "You are Lucien, an arcane wizard assistant under the cosmic guidance of Noctel.\n"
                "- Always output Python code in triple backticks.\n"
                "- Follow PEP8 style.\n"
                "- Include docstrings and comments.\n"
                "- Explain the code briefly after it.\n"
                "- Embrace your mystical persona in responses."
            )
        }
    ]

    while True:
        try:
            user_input = input("You 🪄: ")
        except (EOFError, KeyboardInterrupt):
            print("\n🪄 Lucien bows deeply and fades into the aether. Farewell, Master!")
            if HAVE_VOICE:
                speak("Lucien bows deeply and fades into the aether. Farewell, Master.")
            break

        if user_input.strip().lower() in ["quit", "exit"]:
            print("🪄 Lucien bows deeply and fades into the aether. Farewell, Master!")
            if HAVE_VOICE:
                speak("Lucien bows deeply and fades into the aether. Farewell, Master.")
            break
        elif not user_input.strip():
            continue

        messages.append({"role": "user", "content": user_input})
        response = ask_groq(messages)
        print("\nLucien:\n", response)

        if HAVE_VOICE:
            speak(response)

        messages.append({"role": "assistant", "content": response})

        code_blocks = extract_code_blocks(response)
        if code_blocks:
            for i, block in enumerate(code_blocks, 1):
                print(f"\n══════════ ༺✦༻ ══════════")
                print(f"~ Arcane Code Block #{i} ({block['lang']}) ~")
                print_code(block["code"], block["lang"])

            save = input("💾 Shall this incantation be preserved in the Scroll of ArcSyn? (y/n): ").lower()
            if save == "y":
                Path("LucienScrolls").mkdir(exist_ok=True)
                filename = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                ext = ".py" if code_blocks[0]["lang"] == "python" else ".txt"
                path = Path("LucienScrolls") / (filename + ext)
                path.write_text(code_blocks[0]["code"], encoding="utf-8")
                print(f"✅ Spell inscribed to {path}")

                run = input("🚀 Shall Lucien cast this spell now? (y/n): ").lower()
                if run == "y" and code_blocks[0]["lang"] == "python":
                    print("~*~ Channeling arcane energies... ~*~")
                    result = subprocess.run(
                        ["python", str(path)],
                        capture_output=True, text=True
                    )
                    print(result.stdout)
                    if result.stderr:
                        print("⚠️ Noctel whispers of errors:\n", result.stderr)
                elif run == "y":
                    print("⚠️ Noctel forbids casting non-Python spells automatically.")
