# CreatorPilot AI — Mobile (Flutter)

Feature-first Clean Architecture scaffold for the CreatorPilot AI mobile app.

## Status: Phase 1 scaffold — UI flows wired, backend mocked

**IMPLEMENTED**
- Project structure (feature-first, `core/` + `features/*/{data,domain,presentation}`)
- Material 3 dark theme, brand colours
- Navigation for the full V1 flow: splash → login → home → create campaign →
  generation status → result → projects / brand kit / credits
- Campaign creation form covering every field in the spec (description,
  industry, language, style, audience, offer, location, aspect ratio, outputs)
- Mocked auth repository and mocked generation repository so the app runs
  and is demoable **with zero API keys and zero backend**
- One widget test as a template for the suite

**NOT IMPLEMENTED YET (by design — needs your accounts/backend)**
- Firebase project (Auth, Firestore, Storage, App Check) — needs your GCP project
- Real backend calls (FastAPI `POST /v1/campaigns`, job polling/websocket)
- Google Play Billing + server-side purchase verification
- Brand Kit / Projects persistence (currently static placeholders)
- Push notifications for job completion
- Actual AI provider calls — those live in the backend/orchestrator only,
  never in this app

## Run locally

```bash
flutter pub get
flutter run
```

The app boots straight into a working demo using mock data — no `.env`,
no Firebase config needed for UI development.

## Wiring real services (in order)

1. Add `google-services.json` / `GoogleService-Info.plist`, call
   `Firebase.initializeApp()` in `main.dart`.
2. Implement `FirebaseAuthRepository` (implements `AuthRepository`) and swap
   it in at the DI layer — no UI changes needed.
3. Implement `ApiGenerationRepository` calling the FastAPI backend, replacing
   `MockGenerationRepository` the same way.
4. Wire `in_app_purchase` + backend purchase-token verification for billing.

## Testing

```bash
flutter test
```
