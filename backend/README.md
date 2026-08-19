# CreatorPilot AI — Backend (FastAPI)

## Status: Phase 4 (AI orchestration, mocked providers) — tested, working

**IMPLEMENTED (12/12 tests passing)**
- FastAPI app with `/healthz`, `POST /v1/campaigns`, `GET /v1/generations/{id}`, `POST /v1/reports`
- Provider abstraction (`app/providers/interfaces.py`) for text, image, video,
  audio, TTS, and moderation — swappable without touching orchestration code
- Mock providers implementing the full STEP 1–12 workflow from
  `docs/AI_WORKFLOW.md`, with input/output moderation gates
- Credit service implementing reserve → finalize / refund, tested against
  insufficient-balance, double-refund, and finalize-then-refund cases
- Structured logging (`structlog`) with automatic secret redaction
- Config via environment variables only — `.env.example` provided, real
  `.env` gitignored, no secrets ever committed
- Dockerfile for containerized deployment

**NOT IMPLEMENTED YET (needs your accounts/infra)**
- Real Firebase Auth token verification (`app/core/auth.py` has a fail-closed
  dev-only stub — see TODO comment for the 3-line Phase 2 swap)
- Real Gemini / Veo / TTS provider implementations (`app/core/dependencies.py`
  has the exact TODO for where they plug in once you have API keys)
- Firestore persistence (jobs/credits currently in-memory, reset on restart)
- Async job queue (Celery/Cloud Tasks) — campaigns currently run inline,
  synchronously, since providers are mocked and fast; real video generation
  needs a queue per the spec's async job requirement
- FFmpeg composition service (`video-engine/`, Phase 7)
- Google Play purchase-token verification (Phase 11)

## Run locally

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API docs.
Auth: any request needs `Authorization: Bearer <anything>` in development
mode (no real Firebase project configured yet) — this only works when
`ENVIRONMENT=development`, and is hard-blocked in production.

## Test

```bash
python3 -m pytest tests/ -v
```
