# CreatorPilot AI — Backend (FastAPI)

## Status: Phases 3–4, 6, 8–9 — tested, working (17/17 tests passing)

**IMPLEMENTED**
- FastAPI app: `/healthz`, `POST /v1/campaigns`, `GET /v1/generations/{id}`,
  `POST /v1/reports`, `GET/DELETE /v1/projects`, `GET/PUT /v1/brand-kit`
- Provider abstraction (`app/providers/interfaces.py`) for text, image, video,
  audio, TTS, and moderation — swappable without touching orchestration code
- Mock providers implementing the full STEP 1–12 workflow from
  `docs/AI_WORKFLOW.md`, with input/output moderation gates
- **Async job processing (Phase 6)**: `POST /v1/campaigns` returns `QUEUED`
  immediately; a background task walks the job through
  PROCESSING → GENERATING → COMPOSING → COMPLETED/FAILED
- Repository pattern for projects and brand kits (`app/repositories/`) —
  in-memory now, same interface Firestore implementations plug into later,
  with per-user isolation already enforced (can't fetch another user's
  project by guessing an ID)
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
- Firestore persistence (jobs/credits/projects/brand-kits currently
  in-memory, reset on restart — repository/service interfaces are already
  Firestore-shaped so this is a swap, not a rewrite)
- Durable job queue (Cloud Tasks/Celery) — `job_manager.py` uses FastAPI's
  `BackgroundTasks` as a stepping stone; real video generation needs jobs
  that survive a server restart, which this doesn't yet
- FFmpeg composition service (`video-engine/`, Phase 7 — deliberately not
  built until real scene/audio assets exist to test against; see its README)
- Google Play purchase-token verification (Phase 11)
- Admin dashboard (Phase 12)

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
