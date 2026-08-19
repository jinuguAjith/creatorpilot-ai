# CreatorPilot AI — Backend (FastAPI)

## Status: Phases 3–4, 6, 8–10, 12–13 — tested, working (28/28 tests passing)

**IMPLEMENTED**
- FastAPI app: `/healthz`, `POST /v1/campaigns`, `GET /v1/generations/{id}`,
  `POST /v1/reports`, `GET/DELETE /v1/projects`, `GET/PUT /v1/brand-kit`,
  full `/v1/admin/*` suite
- Provider abstraction (`app/providers/interfaces.py`) for text, image, video,
  audio, TTS, and moderation — swappable without touching orchestration code
- Mock providers implementing the full STEP 1–12 workflow from
  `docs/AI_WORKFLOW.md`, with input/output moderation gates
- **Async job processing (Phase 6)**: `POST /v1/campaigns` returns `QUEUED`
  immediately; a background task walks the job through
  PROCESSING → GENERATING → COMPOSING → COMPLETED/FAILED
- Repository pattern for projects, brand kits, and reports (`app/repositories/`)
  — in-memory now, Firestore-shaped interfaces, per-user isolation enforced
- Credit service implementing reserve → finalize / refund, tested against
  insufficient-balance, double-refund, and finalize-then-refund cases
- **Admin dashboard API (Phase 12)**: `/v1/admin/stats` (generation counts,
  success rate, credits consumed, open reports), report review queue with
  resolve action, credit config/plans read, manual credit adjustment —
  all gated by `require_admin` RBAC dependency
- **Security hardening (Phase 13)**: per-user daily generation rate limit
  (spec section 27 cost control), input length/shape validation on every
  campaign/report field (spec section 14), baseline security response
  headers on every response
- Structured logging (`structlog`) with automatic secret redaction
- Config via environment variables only — `.env.example` provided, real
  `.env` gitignored, no secrets ever committed
- Dockerfile for containerized deployment

**NOT IMPLEMENTED YET (needs your accounts/infra)**
- Real Firebase Auth token verification AND real RBAC via custom claims
  (`app/core/auth.py`, `app/core/rbac.py` both have fail-closed dev-only
  stubs — see TODO comments for the Phase 2 swap)
- Real Gemini / Veo / TTS provider implementations (`app/core/dependencies.py`
  has the exact TODO for where they plug in once you have API keys)
- Firestore persistence (jobs/credits/projects/brand-kits/reports currently
  in-memory, reset on restart — repository/service interfaces are already
  Firestore-shaped so this is a swap, not a rewrite)
- Durable job queue (Cloud Tasks/Celery) — `job_manager.py` uses FastAPI's
  `BackgroundTasks` as a stepping stone
- Redis-backed rate limiting — current limiter is in-process only and
  under-counts once you run more than one backend instance
- FFmpeg composition service (`video-engine/`, Phase 7 — deliberately not
  built until real scene/audio assets exist to test against; see its README)
- Google Play purchase-token verification (Phase 11)
- Admin dashboard *frontend* (Phase 12 backend is done; no React/Next.js UI yet)

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
