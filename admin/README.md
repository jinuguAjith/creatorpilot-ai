# CreatorPilot AI — Admin (Phase 12 frontend)

## Status: functional, single-file, no build step — talks to the real backend API

**IMPLEMENTED**
- Dashboard: total/successful/failed generations, success rate, credits
  consumed, open reports count — all live from `GET /v1/admin/stats`
- Reports: list by status (open/reviewed/all), mark as reviewed
- Credits: manual grant/deduct for a given user ID
- Configuration: read-only view of credit costs and subscription plans

**Intentional shortcut, not an oversight:** this is one HTML file using
React via CDN (`<script>` tags, Babel in-browser), not a Next.js project.
For an internal ops tool with four screens, a build pipeline is overhead
without payoff yet. If/when this grows (auth, more views, a design system),
migrate to `admin/` as a proper Vite or Next.js app — the component
structure here maps over directly.

**NOT IMPLEMENTED YET**
- Login screen — currently hardcodes the same `dev-token` bearer the
  backend's dev auth stub accepts. Needs a real login view once Firebase
  Auth + admin custom claims exist (Phase 2)
- AI cost, storage usage, revenue, subscriber counts — need Firestore
  aggregation and Google Play Billing data (Phases 10–11)
- Editable credit config / plan config (currently read-only, matching
  the backend's read-only endpoints)
- User management (view/disable accounts) and failed-job retry —
  backend endpoints for these don't exist yet either

## Run it

Just open the file — no install, no build:

```bash
open admin/index.html          # macOS
start admin/index.html         # Windows
```

Make sure the backend is running first (`uvicorn app.main:app --reload`
from `backend/`, defaults to `http://localhost:8000`). If your backend
runs elsewhere, set it before opening:

```html
<script>window.CREATORPILOT_API_BASE = "http://localhost:9000";</script>
```
(add this line in `index.html`, right before the React script tags)
