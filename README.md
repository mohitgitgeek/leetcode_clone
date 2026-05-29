# leetcode_clone

A LeetCode-inspired clone — **"CodeSage"** — that helps you solve coding problems, with an AI acting as a guide.

## Architecture (frontend + backend + DB + ML)

- **Frontend:** `docs/index.html` — a dark-themed code editor that shows the problem, submits your solution,
  and displays the verdict, AI feedback, complexity, ML difficulty, runtime, and your level.
- **Backend:** FastAPI (`backend/`) with `/api/submit`, `/api/problem`, `/api/stats/{user}`, `/api/health`.
- **Code judge:** `services/judge_engine.py` runs your Python solution against `test_cases/sample_input_output.json`
  (cross-platform — uses the current interpreter, 5s timeout).
- **AI engine + Machine Learning:** `services/ai_engine.py` blends static heuristics with a scikit-learn
  **RandomForest** that predicts a difficulty tier (Easy / Medium / Hard) from structural code features.
- **Storage / DB:** `db/redis_client.py` uses **Redis** when available (via `docker-compose`) and transparently
  **falls back to an in-process store** when it isn't — so per-user progress/levels persist with zero setup.

## Run it locally (no Docker needed)

```sh
cd backend
pip install -r requirements.txt
uvicorn main:app --reload          # serves http://localhost:8000  (docs at /docs)
```

Then open `docs/index.html` in a browser (it talks to `http://localhost:8000` by default).

## Run with Docker (Redis-backed)

```sh
docker-compose up --build          # backend on :8000, Redis on :6379
```
