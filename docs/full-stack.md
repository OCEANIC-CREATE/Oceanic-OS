# Full Stack Prototype

Oceanic-OS now includes a minimal full-stack ecosystem with a backend API and a static dashboard served by the backend.

## Backend

- FastAPI application in `src/oceanic_os/api.py`
- Endpoints:
  - `GET /health`
  - `GET /dashboard`
  - `GET /identities`
  - `POST /identity`

## Frontend

- Static dashboard in `web/index.html`
- Served from the backend at `/static/index.html`
- Minimal client-side code for inspecting live state

## Local developer commands

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the API (development mode):

```bash
uvicorn oceanic_os.api:app --reload
```

Open the dashboard at `http://127.0.0.1:8000/`

Run tests:

```bash
pytest
```

## API usage example

See `docs/api-example.md` for a small `curl` and Python example that exercises the identity endpoints.

## CI

A GitHub Actions workflow is included at `.github/workflows/ci.yml` to run tests on pushes and PRs.

## Why this matters

This full-stack ecosystem gives Oceanic-OS a coherent launchpoint:
- identity model
- memory store
- dashboard summary
- backend-hosted UI surface

From here, the system can grow into agents, knowledge, automation, ecosystem, and stewardship without losing the initial full-stack shape.
