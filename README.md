# CreatorPilot AI

**Tagline:** One Idea. Complete Content.

**Status:** Phase 0 - Architecture & Documentation Complete ✅

---

## 🎯 Project Overview

CreatorPilot AI is a production-ready AI content creation platform that transforms simple business ideas into complete promotional content packages in minutes.

### What It Does

User provides:
```
"Create a promotional campaign for Bella Aroma restaurant.
Grand opening this Sunday in Bangalore.
20% opening offer.
Luxury Italian restaurant.
Target audience: couples and families."
```

CreatorPilot AI generates:
- 🎨 Professional promotional poster
- 🎬 30-second cinematic video
- 📝 Engaging social media caption
- #️⃣ Trending hashtags
- 🎤 Optional AI voice-over (multiple languages)
- 🎵 Background music
- ✅ Call-to-action

### Target Platforms

- **Primary:** Android via Google Play Store
- **Secondary:** iOS via App Store (V2+)
- **Technology:** Flutter (shared codebase)

---

## 📦 Repository Structure

```
creatorpilot-ai/
├── docs/
│   ├── PRD.md                 ✅ Product Requirements Document
│   ├── ARCHITECTURE.md        ✅ System Architecture & Design
│   ├── DATABASE.md            ✅ Firestore Schema & Security Rules
│   ├── API.md                 ✅ REST API Specification
│   ├── AI_WORKFLOW.md         ✅ AI Generation Pipeline
│   ├── SECURITY.md            ✅ Security Implementation Guide
│   ├── BILLING.md             ✅ Subscription & Credit System
│   └── PLAY_STORE.md          ✅ Google Play Release Checklist
│
├── mobile/                    🚧 Phase 1 (Flutter app)
│   ├── android/
│   ├── ios/
│   └── lib/
│
├── backend/                   🚧 Phase 1 (FastAPI)
│   ├── app/
│   ├── tests/
│   └── requirements.txt
│
├── ai-orchestrator/           🚧 Phase 1 (AI Pipeline)
│   ├── app/
│   ├── tests/
│   └── requirements.txt
│
├── admin/                     🚧 Phase 2 (React/Next.js)
│   ├── app/
│   └── package.json
│
├── infrastructure/            🚧 Phase 1 (Terraform/Cloud)
│   ├── gcp/
│   └── github-actions/
│
└── README.md                  ✅ This file
```

---

## 🏗️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|----------|
| **Mobile** | Flutter 3.x (Dart) | Cross-platform app (Android/iOS) |
| **Backend API** | FastAPI (Python) | User management, project CRUD, billing |
| **AI Orchestration** | FastAPI (Python) | Generation pipeline coordination |
| **Database** | Firestore | User profiles, projects, subscriptions |
| **Storage** | Google Cloud Storage | Media files (posters, videos) |
| **Authentication** | Firebase Auth | Email, Google OAuth, session management |
| **AI Providers** | Google Gemini, Veo | Text, image, video generation |
| **Media Processing** | FFmpeg | Video composition, audio mixing |
| **Admin Dashboard** | Next.js (React) | System monitoring, user management |
| **CI/CD** | GitHub Actions | Automated testing, building, deployment |
| **Deployment** | Google Cloud Run | Containerized services, auto-scaling |

---

## 📚 Phase 0: Architecture & Documentation (COMPLETE ✅)

### What Was Delivered

#### 1. **PRD.md** - Product Requirements
- User flows (onboarding, campaign creation, subscription)
- MVP scope (v1.0 features)
- AI generation strategy
- Credit system (pricing, costs)
- Success metrics

#### 2. **ARCHITECTURE.md** - System Design
- High-level system architecture diagram
- Service breakdown (Mobile, Backend, Orchestrator, Admin)
- API layer design
- Data flow diagrams
- Technology stack details
- Deployment strategy (dev/staging/prod)
- Error handling & scalability

#### 3. **DATABASE.md** - Firestore Schema
- Complete collection structure
- Document schemas with field types
- Firestore security rules
- Composite indexes for performance
- Data retention policies
- Backup & recovery strategy

#### 4. **API.md** - REST Endpoints
- Authentication endpoints
- Projects API (CRUD)
- Generations API (create, status, download)
- Brand Kit API
- Subscriptions & billing APIs
- Admin endpoints
- Request/response contracts

#### 5. **AI_WORKFLOW.md** - Generation Pipeline
- Step-by-step AI workflow (8 steps)
- Detailed implementation for each step
- Prompt templates for Gemini
- Error handling & retry strategies
- Cost estimation ($3.50 per generation)
- Monitoring & logging strategy

#### 6. **SECURITY.md** - Security Implementation
- Authentication & authorization architecture
- JWT token flow
- Input validation (Pydantic models)
- Rate limiting (per-user, per-generation)
- Firestore security rules
- Data encryption (in transit & at rest)
- Content moderation pipeline
- GDPR compliance framework

#### 7. **BILLING.md** - Subscription System
- Credit system (100-625 credits per operation)
- Pricing tiers (Free, Creator, Business, Pro)
- Credit reservation & refund logic
- Google Play Billing integration
- Subscription management workflow
- Apple StoreKit future-proofing
- Financial reporting

#### 8. **PLAY_STORE.md** - Release Checklist
- Pre-release preparation (app signing, assets)
- Store listing configuration
- In-app purchases & subscriptions setup
- Testing & compliance checklist
- Release channels (internal → closed → open → production)
- Launch day operations
- Success metrics (installs, retention, revenue)

---

## 🚀 Phase 1: Repository Scaffolding (NEXT)

### Timeline: Weeks 1-2

**Goals:**
- Create project folder structure
- Set up Flutter app scaffold
- Set up FastAPI backend template
- Set up GitHub Actions workflows
- Configure Firebase & GCP projects
- Implement local development environment

**Deliverables:**
- [ ] Flutter app with Material 3 theme
- [ ] FastAPI backend with basic routes
- [ ] Docker configuration for backend
- [ ] GitHub Actions CI/CD pipeline
- [ ] Firebase emulator setup
- [ ] Development documentation

**Output:** Empty but structurally complete codebase ready for Phase 2

---

## 🔐 Phase 2: Authentication (Weeks 2-3)

**Goals:**
- Firebase Auth integration (mobile + backend)
- JWT token generation & validation
- Session management
- Password reset flow
- Google OAuth integration

**Status:** Planned

---

## 📋 Phase 3: Campaign Creation (Weeks 3-4)

**Goals:**
- Campaign form UI (Flutter)
- Campaign input validation
- API endpoint for creating campaigns
- Project storage in Firestore
- Brand Kit setup flow

**Status:** Planned

---

## 🎨 Phase 4-7: AI Generation Pipeline (Weeks 5-8)

**Phase 4:** Poster Generation  
**Phase 5:** Video Generation  
**Phase 6:** Audio & Voice-Over  
**Phase 7:** Media Composition (FFmpeg)  

**Status:** Planned

---

## 💳 Phase 8-9: Credits & Subscriptions (Weeks 9-10)

**Phase 8:** Credit System Implementation  
**Phase 9:** Google Play Billing Integration  

**Status:** Planned

---

## ⚙️ Phase 10-11: Admin & Monitoring (Weeks 11-12)

**Phase 10:** Admin Dashboard (React/Next.js)  
**Phase 11:** Monitoring & Logging (Google Cloud)  

**Status:** Planned

---

## 🧪 Phase 12-14: Testing & Hardening (Weeks 13-14)

**Phase 12:** Unit & Integration Tests  
**Phase 13:** Security Audit & Penetration Testing  
**Phase 14:** Performance Optimization  

**Status:** Planned

---

## 📦 Phase 15: Google Play Release (Week 15)

**Goals:**
- Internal testing track
- Closed beta testing
- Open beta testing
- Production release
- Staged rollout (10% → 50% → 100%)

**Status:** Planned

---

## 📊 Success Criteria for V1 Release

### Functional Requirements ✅
- [x] Architecture documented
- [x] Database schema defined
- [x] API contracts specified
- [x] AI workflow designed
- [ ] Mobile app builds successfully
- [ ] Backend API functional
- [ ] Authentication works
- [ ] Campaign generation works
- [ ] Poster generation works
- [ ] Video generation works
- [ ] Subscriptions verified
- [ ] Credits system functional

### Quality Requirements
- [ ] Flutter tests pass (widget + integration)
- [ ] Backend tests pass (unit + API)
- [ ] Crash rate < 0.1%
- [ ] ANR rate < 0.05%
- [ ] Generation success rate > 95%
- [ ] API latency p95 < 3 seconds

### Security & Compliance
- [ ] Security audit passed
- [ ] GDPR compliance verified
- [ ] No hardcoded secrets
- [ ] HTTPS enforced
- [ ] Rate limiting active

### Google Play Requirements
- [ ] App icon & feature graphic provided
- [ ] Screenshots & descriptions approved
- [ ] Privacy policy live
- [ ] Terms of service live
- [ ] Content rating questionnaire completed
- [ ] App Bundle (.aab) built & signed
- [ ] Testing tracks completed

---

## 🛠️ Getting Started

### Prerequisites

```bash
# Install Flutter
flutter --version  # Should be 3.x+

# Install Python
python --version   # Should be 3.11+

# Install Docker
docker --version

# Install GCP CLI
gcloud --version

# Install Node.js (for admin dashboard)
node --version     # Should be 18+
```

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/jinuguAjith/creatorpilot-ai.git
cd creatorpilot-ai

# Set up development environment variables
cp .env.example .env
# Edit .env with your credentials

# Set up Firebase emulator
firebase emulators:start

# Start mobile app (requires Android emulator or device)
cd mobile
flutter run -d emulator-5554

# Start backend API (in separate terminal)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Start AI Orchestrator (in separate terminal)
cd ai-orchestrator
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

---

## 📖 Documentation

All architecture and design documentation is in the `/docs` folder:

- **[PRD.md](docs/PRD.md)** - Product vision and requirements
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design
- **[DATABASE.md](docs/DATABASE.md)** - Database schema
- **[API.md](docs/API.md)** - API specifications
- **[AI_WORKFLOW.md](docs/AI_WORKFLOW.md)** - Generation pipeline
- **[SECURITY.md](docs/SECURITY.md)** - Security implementation
- **[BILLING.md](docs/BILLING.md)** - Subscription system
- **[PLAY_STORE.md](docs/PLAY_STORE.md)** - Release requirements

---

## 🤝 Contributing

### Git Workflow

```bash
# Create feature branch
git checkout -b feat/authentication

# Make changes, commit with meaningful messages
git commit -m "feat: add Firebase auth integration"

# Push and create PR
git push origin feat/authentication
# Create PR on GitHub
```

### Commit Message Format

```
feat: add user authentication
fix: resolve API timeout issue
docs: update database schema documentation
test: add unit tests for credit system
refactor: optimize video composition logic
style: format code with black and dartfmt
```

---

## 🐛 Issues & Support

- **Bug Reports:** Create issue with reproduction steps
- **Feature Requests:** Create issue with detailed description
- **Questions:** Use GitHub Discussions

---

## 📞 Team Contacts

- **Product Owner:** Ajith (GitHub: @jinuguAjith)
- **Lead Architect:** (To be assigned)
- **Engineering Team:** (To be assigned)

---

## 📄 License

TBD - Choose appropriate license (MIT, Apache 2.0, GPL, proprietary, etc.)

---

## 🎉 Phase 0 Summary

### What's Complete

✅ **Architecture Documentation** (8 detailed documents)  
✅ **Technology Stack** (All components selected)  
✅ **Database Design** (Firestore schema + security rules)  
✅ **API Specification** (All endpoints defined)  
✅ **AI Pipeline** (8-step generation workflow)  
✅ **Security Framework** (Authentication, authorization, encryption)  
✅ **Billing System** (Credits, subscriptions, Google Play)  
✅ **Release Plan** (Google Play checklist)  
✅ **Folder Structure** (Repository organized)  

### What's Next

🚧 **Phase 1** - Repository Scaffolding (1-2 weeks)  
🚧 **Phase 2** - Authentication (2-3 weeks)  
🚧 **Phases 3-15** - Feature implementation & testing  

**Target MVP Release:** ~15 weeks  
**Target Google Play Launch:** ~16 weeks  

---

## 📈 Progress Tracker

| Phase | Title | Status | ETA |
|-------|-------|--------|-----|
| 0 | Architecture & Documentation | ✅ Complete | - |
| 1 | Repository Scaffolding | 🚧 Ready | Week 1-2 |
| 2 | Authentication | 🔜 Planned | Week 2-3 |
| 3 | Campaign Creation | 🔜 Planned | Week 3-4 |
| 4 | Poster Generation | 🔜 Planned | Week 5 |
| 5 | Video Generation | 🔜 Planned | Week 6 |
| 6 | Audio & Voice-Over | 🔜 Planned | Week 7 |
| 7 | Media Composition | 🔜 Planned | Week 8 |
| 8 | Credit System | 🔜 Planned | Week 9 |
| 9 | Google Play Billing | 🔜 Planned | Week 10 |
| 10 | Admin Dashboard | 🔜 Planned | Week 11 |
| 11 | Monitoring & Logging | 🔜 Planned | Week 12 |
| 12 | Testing | 🔜 Planned | Week 13 |
| 13 | Security Audit | 🔜 Planned | Week 14 |
| 14 | Performance Optimization | 🔜 Planned | Week 14 |
| 15 | Google Play Release | 🔜 Planned | Week 15-16 |

---

## ⚠️ Important Notes

1. **This is NOT a toy application.** Architecture supports production scale.
2. **Security is built-in**, not an afterthought. See SECURITY.md.
3. **AI costs are real.** $3.50 per generation. Billing system compensates.
4. **Never commit secrets.** Use Google Cloud Secret Manager.
5. **Test with real data.** Use Firebase emulator locally.
6. **Google Play is strict.** Follow PLAY_STORE.md exactly.

---

## 🎯 Quick Links

- 📖 [Full Documentation](docs/)
- 🏗️ [Architecture Diagram](docs/ARCHITECTURE.md#1-system-overview)
- 🗄️ [Database Schema](docs/DATABASE.md#2-collection-schemas)
- 🔌 [API Reference](docs/API.md)
- 🤖 [AI Workflow](docs/AI_WORKFLOW.md)
- 🔐 [Security Guide](docs/SECURITY.md)
- 💰 [Billing Details](docs/BILLING.md)
- 📱 [Play Store Guide](docs/PLAY_STORE.md)

---

**Last Updated:** August 18, 2026  
**Repository:** https://github.com/jinuguAjith/creatorpilot-ai  
**Status:** Phase 0 Complete ✅ → Ready for Phase 1  

---

## 🚀 Ready to Build?

All documentation is complete. The architecture is solid. The technology stack is finalized.

**Next Step:** Begin Phase 1 - Repository Scaffolding

Let's build something amazing! 🎉
