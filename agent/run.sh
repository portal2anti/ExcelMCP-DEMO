#!/bin/bash
# Run Power Query Agent (start Ollama first in another terminal: ollama serve && ollama pull llama3.2)
cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements.txt
fi
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
