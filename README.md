# LucienAI (a.k.a. Noctel)

LucienAI (code name “Noctel”) is a mystical AI coding companion built to help developers code faster, smarter, and with a touch of wizardry.

Currently running on Groq’s free API, Lucien can:
- Respond to your coding questions
- Generate Python code
- Save generated code into files
- Execute code directly from the console

All from a lightweight terminal-based interface.

---

## Features

✅ Communicates via Groq’s LLM (LLaMa3-70B)  
✅ Detects code blocks in LLM responses  
✅ Optionally saves and runs code automatically  
✅ Displays CPU usage stats

---

## Future Goals

Lucien is only getting started. Planned magical upgrades include:

✨ **Voice Interaction**  
- Integrate Text-to-Speech (TTS) for Lucien’s voice
- Add “wizard voice” options for extra flair

🪄 **Magical GUI**  
- Design a GUI inspired by mystical, arcane aesthetics (think anime spell effects or Doctor Strange vibes!)
- Use generative art tools for custom visuals
- Dark mode by default, obviously

🎛 **Automation & Productivity**  
- Automate workflows in Ableton Live and other music production tools
- Build project-specific coding workflows
- Context-aware assistance (detect what project or app you’re working on)

🤖 **Self-Improvement**  
- Allow Lucien to write or modify its own codebase (under controlled conditions!)
- Train custom prompts for more advanced, personalized assistance

---

## Config & Running

```ini
# Required for Groq API access
GROQ_API_KEY=your_groq_api_key_here

# Optional configuration
USE_INTERNET=true
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions  # default
OLLAMA_URL=http://localhost:11434/api/chat                   # default
MEMORY_FILE=lucien_memory.json                               # default
```

```bash
# Install dependencies
pip install -r requirements.txt

# Dev deps
pip install -r requirements-dev.txt

# Run tests (skips unavailable services automatically)
pytest -q

# Start Lucien AI
python Lucien.py
```

**Service notes:**
- Groq requires `GROQ_API_KEY`
- Ollama optional (local)
- Tests skip gracefully if services are down

**Example commands:**
```bash
> help
> remember Important note
> ai groq Explain Python decorators
> ai ollama Summarize this text
> internet off
```
Credits
Original coding and concept: ArcSyn (Luis Colon)

Inspiration drawn from various Python and AI community examples

Groq API documentation and OpenAI API structures informed early design

No official affiliation with Groq or OpenAI.

License
MIT License 
Copyright (c) 2025 ArcSyn (Luis Colon)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---
