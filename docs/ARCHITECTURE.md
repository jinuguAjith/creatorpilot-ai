# CreatorPilot AI - System Architecture

**Version:** 1.0  
**Status:** MVP Architecture  
**Last Updated:** August 2026

---

## 1. System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Flutter Mobile App (Android/iOS)         │   │
│  │  - UI Components (Material 3)                               │   │
│  │  - Local Storage (Hive)                                     │   │
│  │  - Firebase Auth Integration                                │   │
│  │  - App Check (Bot protection)                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTPS + JWT
                               ↓
┌────────────────────────────────────────────────────────────────��────┐
│                     API GATEWAY LAYER                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │          FastAPI Backend (creatorpilot-backend)             │   │
│  │  - Authentication & Authorization                           │   │
│  │  - Request Validation                                       │   │
│  │  - Rate Limiting                                            │   │
│  │  - Request/Response Logging                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ↓                      ↓                      ↓
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Auth Service    │  │  Projects API    │  │  Billing API     │
│  - Firebase Auth │  │  - Create Project│  │  - Check Credits │
│  - Session mgmt  │  │  - Get Projects  │  │  - Reserve       │
│  - Device tokens │  │  - Delete        │  │  - Refund        │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ↓                      ↓                      ↓
┌──────────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Generation API      │  │  Brand Kit API   │  │  Subscription    │
│  - Create Job        │  │  - Save/Load     │  │  - Verify Token  │
│  - Get Status        │  │  - List          │  │  - Update Entitle│
│  - Download Result   │  │  - Delete        │  │  - Manage Plans  │
└──────────────────────┘  └──────────────────┘  └──────────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                               ↓
        ┌──────────────────────────────────────────┐
        │   AI ORCHESTRATOR SERVICE                │
        │  (creatorpilot-ai-orchestrator)          │
        │  ┌────────────────────────────────────┐  │
        │  │ Asynchronous Job Queue             │  │
        │  │ (Redis/Google Task Queue)          │  │
        │  └────────────────────────────────────┘  │
        │  ┌────────────────────────────────────┐  │
        │  │ Pipeline Orchestrator               │  │
        │  │ - Input Moderation                 │  │
        │  │ - Campaign Strategy                │  │
        │  │ - Content Generation Coordinator   │  │
        │  │ - Media Composition                │  │
        │  │ - Output Moderation                │  │
        │  └────────────────────────────────────┘  │
        │  ┌────────────────────────────────────┐  │
        │  │ AI Provider Abstraction Layer      │  │
        │  │ - GoogleGeminiProvider             │  │
        │  │ - GoogleVeoProvider (Video)        │  │
        │  │ - TextToSpeechProvider             │  │
        │  │ - AudioLibraryProvider             │  │
        │  └────────────────────────────────────┘  │
        └──────────────────┬───────────────────────┘
                           │
        ┌──────────────────┼──────────────────────┐
        ↓                  ↓                      ↓
    ┌────────┐         ┌────────┐            ┌────────┐
    │ Google │         │ Google │            │ Audio  │
    │ Gemini │         │  Veo   │            │Library │
    │  APIs  │         │  APIs  │            │ APIs   │
    └────────┘         └────────┘            └────────┘
                           │
                           ↓
                    ┌──────────────┐
                    │ FFmpeg       │
                    │ Media Engine │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │ Firestore│      │   GCS    │      │ Firebase │
  │(Metadata)│      │ (Media)  │      │ Storage  │
  └──────────┘      └──────────┘      └──────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ↓
        ┌──────────────────────────────────┐
        │   CLOUD STORAGE LAYER            │
        │   - Project metadata             │
        │   - Media files (videos/images)  │
        │   - Generation logs              │
        │   - User data                    │
        └──────────────────────────────────┘
```

---

## 2. Service Architecture

### 2.1 Mobile Application (Flutter)

**Responsibilities:**
- User authentication UI (Google OAuth, Email)
- Campaign creation form
- Display generation progress
- Download/share results
- Brand Kit management
- Project history browsing
- Subscription management UI

**Technology Stack:**
- **Framework:** Flutter 3.x+ (Dart)
- **State Management:** Provider + Riverpod
- **Local Storage:** Hive (offline-first)
- **Network:** Dio (HTTP client)
- **Authentication:** Firebase Auth + Google Sign-In
- **Analytics:** Firebase Analytics
- **Crash Reporting:** Firebase Crashlytics
- **UI:** Material 3, Custom widgets

**Project Structure:**
```
mobile/
├── lib/
│   ├── main.dart
│   ├── config/
│   │   ├── app_config.dart
│   │   ├── firebase_config.dart
│   │   └── env/
│   │       ├── dev.dart
│   │       ├── staging.dart
│   │       └── prod.dart
│   ├── core/
│   │   ├── constants/
│   │   ├── extensions/
│   │   ├── theme/
│   │   └── utils/
│   ├── data/
│   │   ├── datasources/
│   │   │   ├── remote/
│   │   │   └── local/
│   │   ├── models/
│   │   └── repositories/
│   ├── domain/
│   │   ├── entities/
│   │   ├── repositories/
│   │   └── usecases/
│   ├── presentation/
│   │   ├── pages/
│   │   ├── widgets/
│   │   └── providers/
│   └── services/
│       ├── auth_service.dart
│       ├── api_service.dart
│       └── storage_service.dart
├── test/
├── pubspec.yaml
└── README.md
```

### 2.2 Backend API (FastAPI)

**Responsibilities:**
- Request authentication & authorization
- User management
- Project CRUD operations
- Generation job dispatch
- Subscription verification with Google Play
- Credit management
- Admin operations

**Technology Stack:**
- **Framework:** FastAPI (Python 3.11+)
- **Async Runtime:** asyncio + uvicorn
- **Validation:** Pydantic v2
- **Database ORM:** Firestore SDK
- **Job Queue:** Google Cloud Tasks (or Redis)
- **Authentication:** Firebase Admin SDK
- **Monitoring:** Google Cloud Logging
- **HTTP Client:** httpx (async)

**API Endpoints Structure:**
```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── projects.py
│   │   │   │   ├── generations.py
│   │   │   │   ├── brand_kits.py
│   │   │   │   ├── subscriptions.py
│   │   │   │   ├── billing.py
│   │   │   │   └── admin.py
│   │   │   └── schemas/
│   │   │       ├── auth_schema.py
│   │   │       ├── project_schema.py
│   │   │       ├── generation_schema.py
│   │   │       └── ...
│   │   └── health.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   ├── exceptions.py
│   │   └── constants.py
│   ├── models/
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── generation.py
│   │   ├── brand_kit.py
│   │   └── ...
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── project_service.py
│   │   ├── generation_service.py
│   │   ├── subscription_service.py
│   │   ├── billing_service.py
│   │   ├── credit_service.py
│   │   └── moderation_service.py
│   ├── integrations/
│   │   ├── firebase.py
│   │   ├── google_play.py
│   │   └── orchestrator_client.py
│   └── utils/
│       ├── validators.py
│       ├── helpers.py
│       └── enums.py
├── tests/
├── requirements.txt
├── Dockerfile
└── README.md
```

### 2.3 AI Orchestrator Service

**Responsibilities:**
- Receive generation requests
- Coordinate AI provider calls
- Manage asynchronous pipeline
- Compose media files
- Store results
- Handle failures and retries

**Technology Stack:**
- **Framework:** FastAPI (Python 3.11+)
- **Job Processing:** Google Cloud Tasks or Celery
- **AI Providers:** Google Gemini SDK, Google Veo API
- **Media Processing:** FFmpeg-python
- **Storage:** Google Cloud Storage SDK
- **Database:** Firestore
- **Monitoring:** Google Cloud Logging, Structured JSON logs

**Service Structure:**
```
ai-orchestrator/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── core/
│   │   ├── pipeline.py (Main orchestration)
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── constants.py
│   ├── providers/
│   │   ├── base.py (Abstract base)
│   │   ├── gemini.py
│   │   ├── veo.py
│   │   ├── tts.py
│   │   ├── audio_library.py
│   │   └── provider_factory.py
│   ├── steps/
│   │   ├── input_moderation.py
│   │   ├── campaign_strategy.py
│   │   ├── poster_generation.py
│   │   ├── video_generation.py
│   │   ├── audio_selection.py
│   │   ├── voiceover_generation.py
│   │   ├── media_composition.py
│   │   ├── output_moderation.py
│   │   └── storage.py
│   ├── media/
│   │   ├── ffmpeg_engine.py
│   │   ├── audio_mixer.py
│   │   └── video_composer.py
│   ├── models/
│   │   ├── generation_job.py
│   │   ├── campaign_strategy.py
│   │   ├── media_asset.py
│   │   └── generation_error.py
│   ├── integrations/
│   │   ├── firestore.py
│   │   ├── gcs.py
│   │   └── google_play.py
│   └── utils/
│       ├── validators.py
│       └── helpers.py
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

### 2.4 Admin Dashboard (React/Next.js)

**Responsibilities:**
- Display system metrics
- User management
- Report review
- Configuration management
- Job monitoring

**Technology Stack:**
- **Framework:** Next.js 14+ (React)
- **Styling:** Tailwind CSS
- **State:** React Query + Zustand
- **Charts:** Recharts
- **Authentication:** NextAuth.js + Firebase

**Project Structure:**
```
admin/
├── app/
│   ├── layout.tsx
│   ├── dashboard/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── components/
│   ├── users/
│   ├── reports/
│   ├── jobs/
│   ├── configuration/
│   └── analytics/
├── components/
├── hooks/
├── lib/
├── types/
└── public/
```

---

## 3. API Layer Design

### 3.1 Authentication & Security

**Flow:**
```
1. User signs up/logs in via Firebase Auth
2. Mobile app receives Firebase ID Token
3. Mobile app sends token in Authorization header: Bearer <token>
4. Backend validates token with Firebase Admin SDK
5. Backend generates custom JWT (short-lived)
6. Mobile app uses JWT for subsequent requests
```

**Middleware Stack:**
```python
app.add_middleware(CORSMiddleware)  # CORS
app.add_middleware(HTTPException)   # Error handling
app.add_middleware(AuthMiddleware)  # JWT validation
app.add_middleware(RateLimitMiddleware)  # Rate limiting
app.add_middleware(RequestLogging)  # Structured logging
```

### 3.2 Core API Endpoints

**Authentication:**
```
POST   /api/v1/auth/login
POST   /api/v1/auth/login-google
POST   /api/v1/auth/refresh-token
POST   /api/v1/auth/logout
POST   /api/v1/auth/delete-account
```

**Projects:**
```
GET    /api/v1/projects
GET    /api/v1/projects/{project_id}
POST   /api/v1/projects
PUT    /api/v1/projects/{project_id}
DELETE /api/v1/projects/{project_id}
```

**Generations:**
```
POST   /api/v1/generations
GET    /api/v1/generations/{generation_id}
GET    /api/v1/generations/{generation_id}/status
DOWNLOAD /api/v1/generations/{generation_id}/poster
DOWNLOAD /api/v1/generations/{generation_id}/video
```

**Brand Kit:**
```
GET    /api/v1/brand-kit
PUT    /api/v1/brand-kit
POST   /api/v1/brand-kit/upload-logo
```

**Subscriptions:**
```
GET    /api/v1/subscriptions/current
POST   /api/v1/subscriptions/verify-purchase
POST   /api/v1/subscriptions/cancel
GET    /api/v1/subscriptions/plans
```

**Billing & Credits:**
```
GET    /api/v1/billing/credits
GET    /api/v1/billing/transactions
POST   /api/v1/billing/check-credit-availability
```

**Reports:**
```
POST   /api/v1/reports
GET    /api/v1/reports (admin only)
```

---

## 4. Data Flow Diagram

### Campaign Creation Flow

```
┌──────────────────────────────────────────────────────────────┐
│ User fills campaign form & submits                           │
│ (description, industry, tone, outputs, aspect ratio)        │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────────┐
│ Mobile App: Calculate required credits                       │
│ POST /api/v1/billing/check-credit-availability              │
└────────────────────────┬─────────────────────────────────────┘
                         │
            ┌────────────┴────────────┐
            │                         │
      Sufficient            Insufficient
            │                         │
            ↓                         ↓
    ┌──────────────┐          ┌──────────────┐
    │ Proceed      │          │ Show upgrade │
    └──────┬───────┘          │ dialog       │
           │                  └──────────────┘
           ↓
┌──────────────────────────────────────────────────────────────┐
│ Mobile App: Create generation request                        │
│ POST /api/v1/generations                                    │
│ {                                                            │
│   "campaign_input": {...},                                 │
│   "outputs": ["poster", "video", "caption"],               │
│   "aspect_ratio": "9:16"                                   │
│ }                                                            │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────────┐
│ Backend: Validate request                                    │
│ - Authenticate user (JWT)                                    │
│ - Validate campaign input (no profanity, reasonable length)  │
│ - Reserve credits in Firestore                              │
│ - Create generation record (status: REQUESTED)              │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────────┐
│ Backend: Enqueue job to AI Orchestrator                     │
│ - Send to Google Cloud Tasks / Redis                        │
│ - Return generation_id to mobile app                        │
│ - Status: QUEUED                                            │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────────┐
│ Mobile App: Poll generation status                          │
│ GET /api/v1/generations/{generation_id}/status             │
│ Every 2-5 seconds until completion                          │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────────┐
│ AI Orchestrator: Process job                                │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Step 1: Input Moderation (filter harmful content)    │  │
│ │ Status: PROCESSING                                     │  │
│ └────────────────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Step 2: Campaign Strategy (call Gemini)              │  │
│ │ Returns: headline, copy, visual direction             │  │
│ │ Status: PROCESSING                                     │  │
│ └────────────────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Step 3: Poster Generation (call Gemini image gen)    │  │
│ │ Status: GENERATING                                     │  │
│ │ Upload to GCS                                          │  │
│ └────────────────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Step 4: Video Scene Generation (call Veo API)        │  │
│ │ For each scene: generate video clip                    │  │
│ │ Status: GENERATING                                     │  │
│ │ Upload each to GCS                                     │  │
│ └────────────────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Step 5: Audio Selection (query audio library)         │  │
│ │ Match mood to available audio tracks                   │  │
│ │ Status: PROCESSING                                     │  │
│ └────────────────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Step 6: Voice-Over (if selected, call TTS)           │  │
│ │ Convert caption to speech                              │  │
│ │ Upload to GCS                                          │  │
│ │ Status: PROCESSING                                     │  │
│ └────────────────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Step 7: Media Composition (FFmpeg)                    │  │
│ │ Combine video + audio + voice + text overlays         │  │
│ │ Add transitions, color grading, logo                   │  │
│ │ Status: COMPOSING                                      │  │
│ │ Output: Final MP4                                      │  │
│ └────────────────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Step 8: Output Moderation                             │  │
│ │ Scan for NSFW, quality checks                          │  │
│ │ Status: PROCESSING                                     │  │
│ └────────────────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Step 9: Storage & Finalization                        │  │
│ │ Store all assets in GCS                                │  │
│ │ Update Firestore with file URLs                        │  │
│ │ Finalize credits (reserved → used)                     │  │
│ │ Status: COMPLETED                                      │  │
│ └────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────────┐
│ Backend: Poll orchestrator result                           │
│ When complete, update generation status to COMPLETED        │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────────┐
│ Mobile App: Receives COMPLETED status                       │
│ Download URLs ready (poster, video, caption)                │
│ Display results with [Download] [Share] buttons             │
└──────────────────────────────────────────────────────────────┘
```

---

## 5. Technology Stack Summary

| Layer | Component | Technology | Language |
|-------|-----------|------------|----------|
| **Frontend** | Mobile App | Flutter 3.x | Dart |
| **Frontend** | Admin Dashboard | Next.js 14 | TypeScript/React |
| **Backend** | API Server | FastAPI | Python 3.11+ |
| **Orchestration** | AI Pipeline | FastAPI | Python 3.11+ |
| **Database** | User/Project Data | Firestore | - |
| **Storage** | Media Files | Google Cloud Storage | - |
| **AI Providers** | Text/Image Gen | Google Gemini API | - |
| **AI Providers** | Video Gen | Google Veo API | - |
| **AI Providers** | Voice-Over | Google Cloud TTS | - |
| **Media Processing** | Video Composition | FFmpeg | C/C++ |
| **Job Queue** | Async Jobs | Google Cloud Tasks | - |
| **Authentication** | Identity | Firebase Auth | - |
| **Monitoring** | Logging | Google Cloud Logging | - |
| **Analytics** | User Events | Firebase Analytics | - |
| **CI/CD** | Automation | GitHub Actions | YAML |
| **Container** | Deployment | Docker | Dockerfile |
| **Orchestration** | Cloud | Google Cloud Run | - |

---

## 6. Deployment Architecture

### 6.1 Development Environment

```
Local Machine
├── Flutter Mobile App (emulator/device)
├── FastAPI Backend (localhost:8000)
├── AI Orchestrator (localhost:8001)
└── Firebase Emulator Suite
    ├── Auth emulator
    ├── Firestore emulator
    └── Storage emulator
```

### 6.2 Staging Environment

```
Google Cloud (staging-creatorpilot)
├── Cloud Run
│   ├── Backend API (fastapi-backend-staging)
│   ├── AI Orchestrator (ai-orchestrator-staging)
│   └── Admin Dashboard (admin-dashboard-staging)
├── Firestore (staging database)
├── Cloud Storage (staging-media)
├── Cloud Tasks (job queue)
└── Cloud Logging & Monitoring
```

### 6.3 Production Environment

```
Google Cloud (prod-creatorpilot)
├── Cloud Run (auto-scaling)
│   ├── Backend API
│   ├── AI Orchestrator (multiple replicas)
│   └── Admin Dashboard
├── Firestore (production database with backups)
├── Cloud Storage (production-media with CDN)
├── Cloud Tasks (job queue with retries)
├── Cloud SQL (backups)
├── Cloud KMS (key management)
├── Cloud Armor (DDoS protection)
├── Cloud Monitoring (metrics & alerts)
└── Cloud Logging (audit & application logs)
```

---

## 7. Scalability Considerations

### 7.1 Horizontal Scaling

- **Backend API:** Cloud Run auto-scales based on CPU/memory
- **AI Orchestrator:** Multiple workers process jobs from queue
- **Database:** Firestore auto-scales for reads/writes
- **Storage:** GCS handles unlimited concurrent uploads

### 7.2 Performance Optimization

- **Caching:** Redis for session cache, Firestore caching rules
- **CDN:** Cloud CDN for media delivery
- **Compression:** Gzip compression for API responses
- **Async:** Async/await throughout backend
- **Job batching:** Group small AI calls where applicable

### 7.3 Cost Control

- **Rate limiting:** Per-user request limits
- **Generation limits:** Max concurrent jobs
- **Provider fallback:** Use cheaper providers when possible
- **Media cleanup:** Delete old temporary files
- **AI cost monitoring:** Track spending per provider

---

## 8. Error Handling & Retry Strategy

### 8.1 Backend API Errors

```python
class ErrorResponse:
    error_code: str  # "AUTH_FAILED", "INSUFFICIENT_CREDITS", etc.
    message: str  # User-friendly message
    details: dict  # Technical details for logging
    timestamp: datetime
    request_id: str  # For tracing
```

### 8.2 Generation Job Failures

**Retry Logic:**
- Step 1-5: Retry up to 3 times with exponential backoff
- Step 6+: Retry once (avoid infinite loops on media)
- If all retries fail: Mark FAILED, refund credits

**Fallback Strategy:**
- Poster gen fails: Return template-based design
- Video gen fails: Return image slideshow
- Audio not found: Use default background music
- Voice-over fails: Skip voice, continue with video

---

## 9. Security Architecture

### 9.1 Authentication

```
┌─────────────────┐
│  Mobile App     │
│  (User input)   │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────────┐
│  Firebase Authentication            │
│  - Email/Password or Google OAuth   │
│  - Generates Firebase ID Token      │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│  Mobile sends ID Token to Backend   │
│  Authorization: Bearer <token>      │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│  Backend verifies with Firebase     │
│  Admin SDK (server-side validation) │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│  Backend generates short-lived JWT  │
│  (15 min expiry) + Refresh Token    │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│  Mobile stores JWT in secure store  │
│  (Secure storage, not SharedPrefs)  │
└────────┬────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│  Subsequent requests use JWT        │
│  Backend validates JWT signature    │
└─────────────────────────────────────┘
```

### 9.2 Authorization

- **Resource ownership:** User can only access their own projects
- **Admin access:** Role-based access control in admin dashboard
- **API scopes:** Each endpoint has specific permission checks

### 9.3 Data Protection

- **Firestore Security Rules:** Field-level encryption where needed
- **GCS Security:** Signed URLs with time-based expiry (1 hour)
- **HTTPS only:** All API communication encrypted
- **Secrets management:** Google Cloud Secret Manager

---

## Document Status

**PHASE 0 STATUS: ARCHITECTURE DESIGNED**

- ✅ System overview documented
- ✅ Service architecture defined
- ✅ API layer designed
- ✅ Data flow mapped
- ✅ Technology stack detailed
- ✅ Deployment strategy defined
- ✅ Security architecture outlined
- ⏳ Ready for database schema design

---

**Next:** DATABASE.md - Firestore schema, collections, indexes, and security rules.
