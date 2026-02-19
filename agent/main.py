"""
Power Query agent backend: chat with local Ollama, returns Power Query M code.
Serves static frontend and /api/chat. Optional auth via PASSWORD env.
"""
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests

app = FastAPI(title="Power Query Agent")

# Default password 12345; override with PASSWORD env (empty or unset = use 12345)
AGENT_PASSWORD = (os.environ.get("PASSWORD") or "").strip() or "12345"
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

SYSTEM_PROMPT = """You are a Power Query (M language) assistant. You only output valid Power Query M code.
- Assume the data is in a table named "testData" in the current workbook unless the user says otherwise.
- Output only the M code, optionally with short comments. No markdown code fences unless the user asks.
- If the user describes columns (e.g. Entity, Region, Scenario, Unused FTE), use those names in the query.
- For "top N" requests, use Table.FirstN and sorting. For filters, use Table.SelectRows."""


class ChatMessage(BaseModel):
    message: str
    history: list[dict[str, str]] | None = None  # [{"role":"user","content":"..."},{"role":"assistant","content":"..."}]


class ChatResponse(BaseModel):
    reply: str
    model: str


class AuthBody(BaseModel):
    password: str


@app.post("/api/auth")
async def auth(body: AuthBody):
    """Verify password. Returns 200 if correct, 401 if wrong. Frontend uses this before showing chat."""
    if not AGENT_PASSWORD:
        return {"ok": True}
    if body.password.strip() != AGENT_PASSWORD:
        raise HTTPException(status_code=401, detail="Wrong password. Try again.")
    return {"ok": True}


def check_auth(authorization: str | None = Header(default=None)):
    if not AGENT_PASSWORD:
        return True
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization")
    token = authorization.replace("Bearer ", "").strip()
    if token != AGENT_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
    return True


@app.get("/")
async def index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(body: ChatMessage, _: bool = Depends(check_auth)):
    parts = [SYSTEM_PROMPT]
    if body.history:
        for h in body.history[-10:]:  # last 10 turns
            role = "User" if h.get("role") == "user" else "Assistant"
            parts.append(f"{role}:\n{h.get('content', '')}")
    parts.append(f"\nUser request:\n{body.message}\n\nPower Query M code:")
    prompt = "\n\n".join(parts)
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        reply = data.get("response", "").strip()
        if not reply:
            reply = "(No response from model.)"
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot reach Ollama. Is it running? Start with: ollama serve && ollama run " + OLLAMA_MODEL,
        )
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Ollama request timed out.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ChatResponse(reply=reply, model=OLLAMA_MODEL)


@app.get("/api/config")
async def config():
    return {"authRequired": bool(AGENT_PASSWORD)}


@app.get("/api/health")
async def health():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        return {"ollama": "ok", "models": models}
    except Exception as e:
        return {"ollama": "error", "detail": str(e)}


# Mount static after routes so / doesn't get overridden
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
