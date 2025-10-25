# CrewAI POC — Researcher + Writer + Reviewer

A minimal multi‑agent **CrewAI** proof‑of‑concept that assembles three agents:
- **Researcher** — finds sources and extracts key points
- **Writer** — drafts a concise article
- **Reviewer** — critiques and improves the draft

No paid search API needed. Uses **duckduckgo-search** for web results and a simple **requests + BeautifulSoup** fetcher.

---

## 🔧 Stack
- Python 3.11+
- [crewai](https://github.com/crewAIInc/crewAI)
- duckduckgo-search, requests, beautifulsoup4
- dotenv for local config

---

## 🚀 Quickstart

```bash
# 1) Create and activate a virtualenv (recommended)
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) (Optional) Set your model provider via .env
cp .env.example .env
# Then edit .env as needed

# 4) Run
python main.py --topic "LLM observability best practices"
```

The output artifacts are written to `./outputs/`.

---

## ⚙️ Configuration

Edit **.env** (or set environment variables):

- `MODEL_PROVIDER`: one of `openai` or `ollama` (default: `openai`)
- `OPENAI_API_KEY`: required if `MODEL_PROVIDER=openai`
- `OPENAI_MODEL`: default `gpt-4o-mini`
- `OLLAMA_MODEL`: default `llama3.1:8b`
- `MAX_TOKENS`: default `2000`
- `TEMPERATURE`: default `0.2`

> You can run fully offline by setting `MODEL_PROVIDER=ollama` and ensuring the model is pulled locally:
> ```bash
> ollama pull llama3.1:8b
> ```

---

## 🧠 What it does

Given a `--topic`, the crew will:

1. **Researcher**: search the web and fetch a few pages, then summarize bullet points with citations.
2. **Writer**: draft a clear 600–800 word post using the researcher’s notes.
3. **Reviewer**: critique, fix gaps, tighten language, and produce the final article.

Artifacts:
- `outputs/research_notes.md`
- `outputs/draft.md`
- `outputs/final.md`

---

## 📁 Project layout

```
.
├── main.py
├── agents.py
├── tasks.py
├── tools/
│   ├── web_search.py
│   └── __init__.py
├── outputs/                # generated files
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🧪 Example

```bash
python main.py --topic "Vector databases vs RAG over relational stores"
```

---

## 🐛 Troubleshooting

- If CrewAI API changes, pin the version in `requirements.txt` or adapt imports.
- If DuckDuckGo throttles, reduce `max_results` in `web_search.search_web`.
- Network‑blocked environments can still run with a **local topic** (the writer/reviewer will function, but research will be shallow).

---

## 📜 License

MIT


---

## 🖼️ Streamlit UI

Run an interactive front-end:

```bash
streamlit run streamlit_app.py
```

In the sidebar, pick **Model Provider** (OpenAI or Ollama), set model names, max tokens, and temperature.
Enter a topic and press **Run Crew**. Results are saved to `outputs/` and displayed inline.

---

## 🧩 How It Works (Visual Overview)

```
+------------+       +------------+       +------------+
| Researcher | ----> |   Writer   | ----> |  Reviewer  |
+------------+       +------------+       +------------+
      |                    |                   |
      v                    v                   v
 research_notes.md      draft.md            final.md

- Researcher searches web, fetches pages, and summarizes key points with citations.
- Writer drafts a concise article based on research notes.
- Reviewer critiques and improves the draft for the final article.
```

---

### 🧠 Architecture Overview

```
+------------------------+    +------------------------+    +------------------------+
|        [ UI LAYER ]     |    |        [ APP CORE ]     |    |       [ ARTIFACTS ]    |
|                        |    |                        |    |                        |
|  Streamlit Frontend     |    |  main.py               |    |  outputs/               |
|  - Model selection      |    |  - Orchestrates agents |    |  - research_notes.md    |
|  - Topic input          |    |  - Runs Researcher     |    |  - draft.md             |
|  - Run button           |    |  - Runs Writer         |    |  - final.md             |
|                        |    |  - Runs Reviewer       |    |                        |
+------------------------+    +------------------------+    +------------------------+

+------------------------+    +------------------------+    +------------------------+
|      [ TOOLS ]          |    |     [ AGENTS ]          |    |      [ CONFIG ]         |
|                        |    |                        |    |                        |
|  tools/web_search.py    |    |  agents.py              |    |  .env                   |
|  - DuckDuckGo search    |    |  - Researcher agent     |    |  - MODEL_PROVIDER       |
|  - HTTP fetcher         |    |  - Writer agent         |    |  - OPENAI_API_KEY       |
|                        |    |  - Reviewer agent       |    |  - OPENAI_MODEL         |
+------------------------+    +------------------------+    +------------------------+
```

---

### 🗂️ File Map at a Glance

```
.
├── main.py                # Orchestration entrypoint
├── agents.py              # Agent definitions (Researcher, Writer, Reviewer)
├── tasks.py               # Task logic and prompts
├── tools/                 # Utility tools
│   ├── web_search.py      # DuckDuckGo search and fetch utilities
│   └── __init__.py
├── outputs/               # Generated artifacts
│   ├── research_notes.md  # Researcher output
│   ├── draft.md           # Writer output
│   └── final.md           # Reviewer output
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
└── README.md              # This file
```

---

### 🔁 Sequence (Step-by-Step)

1. User inputs a topic via CLI or Streamlit UI.
2. `main.py` invokes the Researcher agent.
3. Researcher searches the web, fetches pages, and extracts bullet points with citations.
4. Researcher writes `research_notes.md`.
5. `main.py` invokes the Writer agent with research notes.
6. Writer drafts a 600–800 word article in `draft.md`.
7. `main.py` invokes the Reviewer agent with the draft.
8. Reviewer critiques and improves the draft, producing `final.md`.
9. Artifacts are saved in `outputs/` and optionally displayed in UI.

---

### 📊 Data Flow

```
[ User Input ]
     |
     v
[ main.py ]
     |
     v
+-----------------+
| Researcher Agent|
+-----------------+
     |
     v
research_notes.md
     |
     v
+-------------+
| Writer Agent|
+-------------+
     |
     v
draft.md
     |
     v
+--------------+
| Reviewer Agent|
+--------------+
     |
     v
final.md
     |
     v
[ Outputs Directory ]
```

---

### ⚙️ Configuration Knobs

| Variable          | Description                          | Default        |
|-------------------|----------------------------------|----------------|
| MODEL_PROVIDER    | Choose model backend: openai/ollama| openai         |
| OPENAI_API_KEY    | API key for OpenAI (required if openai)| (none)        |
| OPENAI_MODEL      | OpenAI model name                  | gpt-4o-mini    |
| OLLAMA_MODEL      | Ollama model name                  | llama3.1:8b    |
| MAX_TOKENS        | Max tokens per completion          | 2000           |
| TEMPERATURE       | Sampling temperature               | 0.2            |
