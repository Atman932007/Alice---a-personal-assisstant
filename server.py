from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import sys
import os
import socket

# Add Alice folder to path so brain.py can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brain import ask_Alice, clear_memory

app = FastAPI()

# Serve the static folder (index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── Request model ──
class Question(BaseModel):
    question: str

# ── Routes ──

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/ask")
def ask(q: Question):
    print(f"\n[Phone] Question: {q.question}")
    answer = ask_Alice(q.question)
    print(f"[Phone] Answer: {answer}")
    return {"answer": answer}

@app.post("/forget")
def forget():
    clear_memory()
    return {"status": "Memory cleared sir."}

@app.get("/status")
def status():
    return {"status": "Alice is online sir."}

# ── Get real WiFi IP automatically ──
def get_local_ip():
    try:
        # ✅ This always gets the correct WiFi IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# ── Start server ──
if __name__ == "__main__":

    # ✅ Always detects correct IP automatically
    local_ip = get_local_ip()

    print("\n" + "="*50)
    print("  ALICE SERVER STARTING...")
    print("="*50)
    print(f"\n  Open this on your phone:")
    print(f"\n  >>> http://{local_ip}:8000 <<<")
    print(f"\n  Local Mac access:")
    print(f"  http://localhost:8000")
    print(f"\n  Make sure phone and Mac are on same WiFi!")
    print("="*50 + "\n")

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )