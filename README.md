# ExcelMCP-DEMO

**FP&A test data, capacity scenario & local Power Query agent.**

We used **Cursor** and the **Excel MCP** (Smithery) to generate dummy FP&A data, add a capacity layer, query it in natural language, and package a reusable Power Query. We also **built a local Power Query agent** (self-hosted web app + local LLM) so you can get M code from chat without sending data off your machine.

All data in this repo is **dummy** — no real business logic.

---

## What we did

| Step | Description |
|------|-------------|
| 1 | **Excel MCP** — Connected Cursor to Excel via Smithery for read/write without opening the file. |
| 2 | **FP&A test data** — One denormalized sheet `testData`: entities, regions, departments, product lines, scenarios (Actual, Budget, Forecast, Prior Year), P&L columns, month-level. |
| 3 | **Capacity** — Added scenario “Capacity”, columns Unused Headcount / Unused FTE, and extra rows (dummy unused capacity per month). |
| 4 | **Query in Cursor** — Asked in plain language (e.g. “top 5 unused capacity per month”); AI returned a table via Python/openpyxl. |
| 5 | **Reusable Power Query** — Wrote a `.pq` script and how-to so anyone can run the same “top 5 per month” in Excel. |
| 6 | **Local Power Query agent** — Built a web app in `agent/`: password-protected chat UI, Python backend, **Ollama (local LLM)**. You type requests → get M code. **Already implemented:** self-hosted agent + local LLM (no data leaves your machine). |

---

## Repo contents

| Item | Description |
|------|-------------|
| **testData.xlsx** | One sheet `testData`, ~48k rows dummy FP&A + capacity. |
| **generate_fpna_test_data.py** | Creates the FP&A table (openpyxl). Run with project `.venv`. |
| **enrich_capacity.py** | Adds Capacity scenario and Unused HC/FTE columns to existing `testData.xlsx`. |
| **Top5UnusedCapacityPerMonth.pq** | Power Query M: top 5 by Unused FTE per month. Paste into Excel Power Query Advanced Editor. |
| **HowToRun-Top5Capacity.md** | Steps to run that query in Excel (table name, Advanced Editor, Close & Load). |
| **requirements.txt** | Python: `openpyxl`. |
| **push_excel_to_github.py** | Uploads `testData.xlsx` via GitHub API (for large file). |
| **agent/** | Local Power Query agent (see below). |
| **going-forward.md** | Longer guide: next-phase options, data safety, where the agent runs. |

---

## The agent (self-hosted + local LLM)

We **already implemented** one of the “next steps”: a **self-built agent with a local LLM**. It’s in the **`agent/`** folder.

- **Login** — Password (default `12345`). Wrong password = retry; no access until correct.
- **Chat** — Natural-language requests → Power Query M code. History in session; clearable.

![Agent — Login](https://raw.githubusercontent.com/portal2anti/ExcelMCP-DEMO/main/agent/sc1.png)

![Agent — Chat](https://raw.githubusercontent.com/portal2anti/ExcelMCP-DEMO/main/agent/sc2.png)

- **Stack:** Plain HTML/JS frontend, Python (FastAPI) backend, **Ollama** (e.g. `llama3.2`) on your machine. No Excel or chat data is sent to the cloud.
- **Run:** See **[agent/README.md](agent/README.md)** for Ollama install, venv, and `uvicorn` (or `./run.sh`).

---

## Next steps & scenarios

*(Condensed from [going-forward.md](going-forward.md).)*

**Goal:** Let finance get new Power Queries via a chat-like interface, while safeguarding sensitive data and controlling where the agent runs.

**Options:**

| Option | Where it runs | Data | Best for |
|--------|----------------|------|----------|
| **Cursor (desktop)** | User’s machine | Local only | Power users, no central app. |
| **Your backend + LLM API** | Your server | You control what’s sent to LLM | Full control, compliance. |
| **Vendor (e.g. ChatGPT Team, Copilot)** | Vendor cloud | Per vendor DPA/tenant | Fast rollout. |
| **Local / on‑prem LLM** | Your DC or laptop | Never leaves your network | Strict data residency. |

**We already implemented:** **Self-built agent + local LLM** — the `agent/` app uses Ollama on your machine; no data leaves it. Other paths (Cursor-only, internal app with cloud LLM, vendor chat) are described in **going-forward.md**.

**Data safety:** Don’t send raw workbooks to a public LLM. Use local files, your backend (send only schema/sample to LLM), or a compliant vendor / on‑prem model.

---

*Summary: Cursor + Excel MCP for FP&A test data and capacity; reusable Power Query and how-to; local Power Query agent in `agent/` (Ollama, no data off machine).*
