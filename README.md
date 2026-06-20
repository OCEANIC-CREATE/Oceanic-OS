# Oceanic-OS

💧 Oceanic-OS is a seed project for building a living platform around identity, memory, dashboards, and trusted agency.

## Mission

- Build slowly.
- Observe deeply.
- Ship continuously.
- Preserve trust.
- Maintain agency.
- Repair often.
- Learn forever.

## Focus

### Today
- Identity
- Memory
- Dashboard

### This year
- Agents
- Knowledge
- Automation

### This decade
- Ecosystem

### Lifetime
- Stewardship

## Protocol

`ReturnToSilence()`

## Structure

- `docs/` — mission, roadmap, design notes, and principles.
- `src/` — module scaffolding for core missions and chapters.
- `src/oceanic_os/` — full-stack prototype package for identity, memory, dashboard, and ecosystem.
- `web/` — static frontend served by the application.
- `tests/` — API and module tests.
- `Makefile` — developer workflows.
- `requirements.txt` — installable dependencies.
- `.gitignore` — sensible defaults for future code.
- `pyproject.toml` — Python package metadata.

## Getting Started

1. Install Python 3.11 or newer.
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run tests: `pytest`

## Run locally

Start the backend:

```bash
uvicorn oceanic_os.api:app --reload
```

Open the app dashboard:

```bash
http://127.0.0.1:8000/
```

Explore the API with interactive documentation:

```bash
http://127.0.0.1:8000/docs         # Swagger UI
http://127.0.0.1:8000/redoc        # ReDoc
```

## API Features

- **Identities**: Full CRUD operations (Create, Read, Update, Delete)
- **Search**: Filter identities by name or email
- **Memory**: Record and retrieve event timeline
- **Dashboard**: Live summary of system state
- **Auto Documentation**: Interactive Swagger UI and ReDoc

## Next step

Begin by expanding one of the core modules into a small working experience: an identity model, memory store, or dashboard view.

---

## Values

1. Trust first.
2. Agency always.
3. Systems that are easy to understand and fix.
4. Growth through iteration, not haste.

> Oceanic-OS is intentionally minimal at launch. The first work is to plant clarity, structure, and a path for the next wave of development.
