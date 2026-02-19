# ExcelMCP-DEMO — FP&A test data & capacity demo

A small demo project: we used **Cursor** (the AI IDE) and the **Excel MCP server** (via Smithery) to generate fake FP&A-style data, add a “capacity” layer, query it in natural language, and then package a reusable Excel query for colleagues.

Everything in this repo is **dummy data** — no real business relations, no real numbers. It’s only for trying out the workflow and sharing the query.

---

## What we did (overview)

1. **Connected Excel via Smithery MCP**  
   We added the Excel MCP server to Cursor so the AI could work with Excel (read/write) without opening the file manually.

2. **Generated FP&A test data**  
   We created a single, big denormalized table (`testData`) with fake financial planning data: entities, regions, departments, product lines, scenarios (Actual, Budget, Forecast, Prior Year), and P&L-style columns (Revenue, COGS, OpEx, EBITDA, Headcount, etc.) at month level.

3. **Enriched with fake “capacity”**  
   We added a **Capacity** scenario and two columns — **Unused Headcount** and **Unused FTE** — plus extra rows that represent “unused capacity” per month. Again, this is dummy data; there are no real relations or logic behind the numbers.

4. **Queried the data in Cursor (LLM mode)**  
   We asked Cursor in plain language (e.g. “top 5 unused capacity per month, where are they?”). The AI read the Excel file (via Python/openpyxl in this setup), ran the logic, and returned a table in chat. That’s the “query data in LLM mode” part.

5. **Prepared a reusable Excel query and guide**  
   So a colleague can get the same result without Cursor, we wrote a **Power Query** script and a short **how-to**: they open their copy of the file, run the query in Excel, and get the same “top 5 unused capacity per month” view.

---

## What’s in this repo

| Item | What it is |
|------|------------|
| **testData.xlsx** | The main output: one sheet `testData` with ~48k rows of dummy FP&A + capacity data. |
| **generate_fpna_test_data.py** | Python script that creates the initial FP&A table (and can include the Capacity scenario). Uses `openpyxl`; run with the project’s `.venv`. |
| **enrich_capacity.py** | Python script that adds the Capacity scenario and the columns Unused Headcount / Unused FTE to an existing `testData.xlsx`. |
| **Top5UnusedCapacityPerMonth.pq** | Power Query (M) script: “top 5 unused capacity per month” by Unused FTE (then Unused Headcount). Your colleague can paste this into Excel’s Power Query Advanced Editor. |
| **HowToRun-Top5Capacity.md** | Step-by-step guide for running that query in Excel (table name, Advanced Editor, Close & Load). |
| **requirements.txt** | Python dependency: `openpyxl` (for generating and enriching the Excel file). |

---

## Important details (so nothing is missed)

- **Excel MCP** was added in Cursor via Smithery (`smithery mcp add haris-musa/excel-mcp-server --client cursor`). After adding, we used Python + openpyxl in the project to generate and enrich the file; the MCP can be used for other Excel operations from Cursor as needed.
- **Data is denormalized**: one row per combination of dimensions (Entity, Region, Department, Product Line, Scenario, Year, Period). No separate “fact” and “dimension” tables — everything is in one sheet for simplicity.
- **Capacity** is implemented as an extra **scenario** (“Capacity”) and two **columns** (Unused Headcount, Unused FTE). Capacity rows have financials set to 0 and Comment like “Unused capacity (month)”. Relations between capacity and other rows are not modeled; it’s dummy data.
- **Query in Cursor**: We didn’t use the Excel MCP to run the “top 5 per month” logic; we used a small Python snippet (e.g. in the chat) that loads `testData.xlsx`, filters Scenario = Capacity, sorts, groups by month, and takes top 5. That’s what we mean by “query data in LLM mode” — you describe what you want in chat, and the AI produces the code and the result.
- **Reuse in Excel**: The `.pq` file is the “pure query” — no Cursor, no Python. Your colleague only needs their copy of the workbook and the steps in **HowToRun-Top5Capacity.md** (name the table `testData`, paste the M code, Close & Load).

---

## How to regenerate or enrich (for you)

- **Full regenerate** (FP&A + Capacity in one go):  
  `python generate_fpna_test_data.py`  
  (use the repo’s virtualenv: e.g. `.venv/bin/python generate_fpna_test_data.py`.)

- **Only add capacity** to an existing `testData.xlsx`:  
  `python enrich_capacity.py`  
  (same: run with `.venv` and ensure `testData.xlsx` is in the project folder.)

- **Dependencies**:  
  `pip install -r requirements.txt` (or use the existing `.venv`).

---

## Handing off to a colleague

Give them:

1. Their copy of **testData.xlsx** (or the same structure).
2. The file **Top5UnusedCapacityPerMonth.pq** (the Power Query script).
3. The file **HowToRun-Top5Capacity.md** (or the same instructions in an email).

They don’t need Cursor, Python, or this repo — just Excel and the two files above.

---

*Summary: We used Cursor and the Excel MCP to generate and enrich dummy FP&A test data, queried it in natural language in Cursor, then packaged a standalone Excel Power Query and a short guide so a colleague can run the same “top 5 unused capacity per month” on their own copy of the file.*
