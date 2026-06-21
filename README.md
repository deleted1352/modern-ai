# Modern AI — Course Assignments

A collection of hands-on exercises for modern AI and LLM development. The repository is organized by week:

| Directory | Description |
|-----------|-------------|
| [`week1/`](week1/) | LLM prompting techniques (chain-of-thought, RAG, tool calling, reflexion, etc.) |
| [`week2/`](week2/) | **Action Item Extractor** — FastAPI + SQLite app that turns free-form notes into checklists |

The Week 2 application is the primary full-stack project: a FastAPI backend with SQLite persistence, heuristic and LLM-powered extraction, and a lightweight HTML frontend.

---

## Project Overview (Week 2)

The **Action Item Extractor** accepts pasted meeting notes or task lists and returns structured action items. Two extraction strategies are available:

1. **Heuristic** — rule-based parsing of bullets, checkboxes, and keyword prefixes (`todo:`, `action:`, etc.).
2. **LLM (Ollama)** — uses a local `llama3` model via [Ollama](https://ollama.com/) to infer action items from unstructured text.

Notes and extracted items are stored in SQLite. The frontend supports live checkbox toggling and browsing saved note history.

### Architecture

```
week2/
├── app/
│   ├── main.py              # FastAPI app, static file serving
│   ├── db.py                # SQLite helpers (notes + action_items tables)
│   ├── routers/
│   │   ├── notes.py         # Note CRUD, LLM extraction, list-all endpoint
│   │   └── action_items.py  # Heuristic extraction, item listing, done toggle
│   └── services/
│       └── extract.py       # extract_action_items() + extract_action_items_llm()
├── frontend/
│   └── index.html           # Single-page UI
├── data/
│   └── app.db               # SQLite database (created at runtime)
└── tests/
    └── test_extract.py      # Unit tests for extraction logic
```

---

## Environment Setup

These steps target **Python 3.12**. Run all commands from the repository root (`modern-ai/`).

### 1. Install Anaconda

Download and install [Anaconda Individual Edition](https://www.anaconda.com/download), then open a new terminal so `conda` is on your `PATH`.

### 2. Create and activate a Conda environment

```bash
conda create -n moderndev python=3.12 -y
conda activate moderndev
```

### 3. Install Poetry

**macOS / Linux:**

```bash
curl -sSL https://install.python-poetry.org | python -
```

**Windows (PowerShell):**

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Ensure Poetry is on your `PATH`, then verify:

```bash
poetry --version
```

### 4. Install project dependencies

With the `moderndev` environment active:

```bash
poetry install --no-interaction
```

### 5. (Optional) Set up Ollama for LLM extraction

LLM extraction requires a running Ollama server and the `llama3` model:

```bash
# Install Ollama from https://ollama.com/download
ollama pull llama3
ollama serve   # if not already running as a background service
```

---

## Running the Application

From the repository root with `moderndev` activated:

```bash
poetry run uvicorn week2.app.main:app --reload
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

Interactive API docs are available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## API Endpoint Roadmap

### Notes (`/notes`)

| Method | Path | Description | Request body |
|--------|------|-------------|--------------|
| `POST` | `/notes` | Create a note and extract action items via **heuristics** | `{ "content": "..." }` |
| `POST` | `/notes/extract-llm` | Create a note and extract action items via **Ollama LLM** | `{ "content": "..." }` |
| `GET` | `/notes` | List all saved notes with nested action items | — |
| `GET` | `/notes/{note_id}` | Fetch a single note by ID | — |

**Example — LLM extraction:**

```bash
curl -X POST http://127.0.0.1:8000/notes/extract-llm \
  -H "Content-Type: application/json" \
  -d '{"content": "- [ ] Set up database\n- Write tests"}'
```

**Example — list all notes:**

```bash
curl http://127.0.0.1:8000/notes
```

### Action Items (`/action-items`)

| Method | Path | Description | Request body |
|--------|------|-------------|--------------|
| `POST` | `/action-items/extract` | Extract items via heuristics; optionally save as a note | `{ "text": "...", "save_note": true }` |
| `GET` | `/action-items` | List action items (optional `?note_id=` filter) | — |
| `POST` | `/action-items/{id}/done` | Mark an action item done/undone | `{ "done": true }` |

### Frontend wiring

| UI control | HTTP call |
|------------|-----------|
| **Extract (Heuristic)** | `POST /action-items/extract` with `{ text, save_note }` |
| **Extract (LLM AI)** | `POST /notes/extract-llm` with `{ content }` |
| **📋 List All Notes** | `GET /notes` |

---

## Testing

Tests live in `week2/tests/` and use **pytest**. LLM tests mock `week2.app.services.extract.chat` so no live Ollama server is required.

Run the full test suite:

```bash
poetry run pytest week2/tests/ -v
```

Run only extraction tests:

```bash
poetry run pytest week2/tests/test_extract.py -v
```

### Test coverage highlights

- Heuristic bullet/checkbox parsing
- LLM JSON array parsing from mocked Ollama responses
- Empty/whitespace input short-circuit (no LLM call)
- Graceful handling of Ollama connection errors

---

## Development Tooling

| Tool | Purpose |
|------|---------|
| **Poetry** | Dependency management (`pyproject.toml`) |
| **pytest** | Unit testing |
| **black** | Code formatting |
| **ruff** | Linting |
| **pre-commit** | Git hooks (optional) |

Format and lint (optional):

```bash
poetry run black .
poetry run ruff check .
```

---

## Week 1 — LLM Prompting Playground

See [`week1/README.md`](week1/README.md) and [`week1/assignment.md`](week1/assignment.md) for standalone Python scripts covering:

- Chain-of-thought prompting
- K-shot prompting
- Self-consistency
- RAG
- Tool calling
- Reflexion

Week 1 scripts are run directly with Python (e.g. `python week1/chain_of_thought.py`) and do not require the FastAPI server.

---

## License

Course assignment repository — see upstream course materials for usage terms.
