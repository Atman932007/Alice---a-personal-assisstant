# Alice — Personal AI Assistant

A Jarvis-style voice assistant built for macOS, designed and implemented
independently from scratch. Alice handles conversational queries and voice
interaction using a local LLM backend — no data leaves your machine.

---

## File Structure

```
Alice/
├── static/                  # Static assets
├── tools/                   # Modular tool/skill handlers
├── brain.py                 # Core reasoning and LLM interaction
├── main.py                  # Entry point and main loop
├── server.py                # Local server (API layer)
├── voice_in.py              # Speech-to-text (microphone input)
├── voice_out.py             # Text-to-speech output
├── index_documents.py       # Document indexing for context retrieval
├── memory.json              # Persistent conversation memory
├── kokoro-v1.0.onnx         # Local TTS model (Kokoro)
├── voices-v1.0.bin          # Voice data for Kokoro TTS
└── .env                     # API keys / config (not committed)
```

---

## How It Works

- **Voice input** — `voice_in.py` captures microphone audio and transcribes it
- **Brain** — `brain.py` manages conversation context and sends queries to a local LLM via Ollama
- **Voice output** — `voice_out.py` runs the Kokoro ONNX TTS model locally for speech synthesis
- **Memory** — conversation history is persisted in `memory.json` across sessions
- **Tools** — modular handlers in `tools/` extend Alice's capabilities

---

## Stack

- Python 3.x
- [Ollama](https://ollama.ai) — local LLM runtime (Llama 3.1 / Gemma)
- [Kokoro](https://github.com/thewh1teagle/kokoro-onnx) — offline TTS via ONNX
- `speechrecognition` / `pyaudio` — voice input
- Flask — local server layer

---

## Setup

```bash
# 1. Install Ollama and pull a model
brew install ollama
ollama pull llama3.1

# 2. Clone and install dependencies
git clone https://github.com/YOUR_USERNAME/alice-assistant
cd alice-assistant
pip install -r requirements.txt

# 3. Add your config
cp .env.example .env   # edit as needed

# 4. Run
python main.py
```

---

## Design Decisions

**Why local LLM?** Privacy — Alice handles personal data and runs entirely
offline on Apple Silicon via Ollama.

**Why Kokoro for TTS?** Fully offline, high-quality neural voice synthesis
without any API calls. The ONNX runtime keeps it fast on macOS.

**Why build memory manually?** To understand multi-turn context at the API
level rather than abstracting it away with a framework.

---

## Status

Active personal project. Ongoing additions include smarter tool routing
and document Q&A via `index_documents.py`.

---

## Author

**Atman Kumar Das**  
B.Tech CSE (AI & ML), KIIT University  
[linkedin.com/in/atman-kumar-das-b41623373](https://linkedin.com/in/atman-kumar-das-b41623373)