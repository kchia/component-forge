# AGENTS.md

## Cursor Cloud specific instructions

### Services overview

| Service | Port | How to run |
|---|---|---|
| PostgreSQL 16 | 5432 | `docker compose up -d` (from repo root) |
| Qdrant | 6333/6334 | `docker compose up -d` (from repo root) |
| Redis 7 | 6379 | `docker compose up -d` (from repo root) |
| FastAPI backend | 8000 | `cd backend && ./venv/bin/uvicorn src.main:app --reload` |
| Next.js frontend | 3000 | `cd app && npm run dev` |

See `CLAUDE.md` for full architecture details and `Makefile` for standard commands (`make install`, `make dev`, `make test`, `make lint`).

### Non-obvious caveats

- **Docker in Cloud VM**: Docker must be started manually (`sudo dockerd &>/tmp/dockerd.log &`) and the socket needs `sudo chmod 666 /var/run/docker.sock` before non-root use. The daemon config uses `fuse-overlayfs` storage driver and `iptables-legacy` for nested container compatibility.
- **python-multipart**: The `requirements.txt` does not list `python-multipart`, but FastAPI requires it at startup for form/file upload routes. It must be installed separately: `cd backend && ./venv/bin/pip install python-multipart`.
- **black/isort not in requirements.txt**: The linting tools `black` and `isort` referenced by `make lint` are not in `requirements.txt`. Install them in the venv: `cd backend && ./venv/bin/pip install black isort`.
- **Backend venv activation**: In non-interactive shells, use `./venv/bin/<command>` instead of `source venv/bin/activate && <command>`.
- **Backend graceful degradation**: The backend starts even without `OPENAI_API_KEY`, `LANGCHAIN_API_KEY`, or external services. AI features will fail but the health endpoint and API docs work.
- **Pre-existing test failures**: Both backend (23 failures out of 584) and frontend (268 failures out of 685) have pre-existing test failures unrelated to environment setup. The frontend Storybook tests require a running Storybook server.
- **Frontend ESLint**: `npm run lint` (in `/app`) reports pre-existing `@typescript-eslint/no-explicit-any` errors (80 errors). These are in the existing codebase.
- **Env files**: Copy from examples before first run: `cp backend/.env.example backend/.env` and `cp app/.env.local.example app/.env.local`.
