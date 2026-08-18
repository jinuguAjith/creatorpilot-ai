# CreatorPilot AI - Product Requirements Document

**Tagline:** One Idea. Complete Content.

**Version:** 1.0  
**Status:** MVP Definition  
**Last Updated:** August 2026

---

## 1. Product Vision

Build a production-ready AI content creation platform that allows users to enter a simple business/content idea and automatically generate a complete promotional content package.

### User Value Proposition

Small business owners and content creators can create professional promotional campaigns in minutes without:
- Hiring a graphic designer
- Buying expensive video production software
- Managing multiple tools
- Requiring technical expertise

---

## 2. Core Deliverables

For a single user input, CreatorPilot AI generates:

1. **AI-generated promotional poster**
   - Professional design
   - Brand-aware (logo, colors)
   - Correct aspect ratio
   - CTA and offer highlighted
   - Contact/location included

2. **AI-generated short promotional video**
   - 30 seconds (MVP)
   - 9:16 vertical aspect ratio
   - Scene-based composition
   - Professional transitions
   - Text overlays and subtitles
   - Logo placement

3. **Background music/audio**
   - Licensed or AI-generated
   - Mood-matched (Cinematic, Luxury, Energetic, etc.)
   - Properly mixed

4. **Optional AI voice-over**
   - Multiple languages (English, Telugu, Hindi, Tamil, Kannada)
   - Professional quality
   - Synchronized with video

5. **Social media caption**
   - Platform-appropriate length
   - Engaging copy
   - Brand voice

6. **Hashtags**
   - Relevant and trending
   - Industry-specific

7. **Call-to-Action (CTA)**
   - Conversion-focused
   - Brand-aligned

8. **Download/share options**
   - Direct download
   - Social media sharing
   - Email sharing

---

## 3. Example User Flow

### Input:
```
Create a promotional campaign for Bella Aroma restaurant.
Grand opening this Sunday in Bangalore.
20% opening offer.
Luxury Italian restaurant.
Target audience: couples and families.
```

### Output Package:
- **Poster:** Luxury Italian restaurant design with opening offer, location, and contact
- **Video:** 30-second promo showing restaurant exterior → food prep → signature dish → customer experience → offer → CTA
- **Caption:** "Experience authentic Italian cuisine at Bella Aroma. Grand opening this Sunday with 20% opening offer!"
- **Hashtags:** #BellaAroma #ItalianCuisine #Bangalore #GrandOpening
- **CTA:** "Reserve your table now at [phone/link]"
- **Audio:** Cinematic background music with optional Italian-accented English voice-over

---

## 4. Target Platforms

### Primary
- **Android** via Google Play Store
- Flutter-based for code sharing

### Secondary
- **iOS** via Apple App Store (V2+)
- Same codebase via Flutter

### Not Included (MVP)
- Web app (can be added later)
- Desktop app (can be added later)

---

## 5. User Roles

### Primary User: Content Creator
- Small business owner
- Restaurant, salon, retail, services
- Limited design/video skills
- Wants fast, professional results
- Uses smartphone primarily

### Secondary: Admin/Support
- CreatorPilot team
- Monitor system health
- Review reports
- Manage configurations
- Support users

---

## 6. Core User Flows

### 6.1 Onboarding

```
App Launch
    ↓
Splash Screen: "CreatorPilot AI - One Idea. Complete Content."
    ↓
Authentication
    ├─ Continue with Google
    ├─ Email + Password
    └─ Secure Session
    ↓
Home Screen
    ├─ Create New Campaign [Primary CTA]
    ├─ Recent Projects
    ├─ Credits display
    ├─ Subscription status
    └─ Brand Kit
```

### 6.2 Campaign Creation

```
Create Campaign
    ↓
Campaign Details Form
    ├─ Business/content description (textarea)
    ├─ Industry (dropdown)
    ├─ Language (dropdown)
    ├─ Tone/style (Luxury, Modern, Cinematic, Minimal, Energetic, Professional, Festival, Elegant)
    ├─ Target audience (textarea)
    ├─ Offer/details (textarea)
    ├─ Location (text)
    └─ Select Outputs [Checkboxes]
        ├─ ☑ Poster
        ├─ ☑ Video
        ├─ ☑ Caption
        ├─ ☐ Voice-over
        └─ [Optional] Include in Brand Kit
    ↓
Select Aspect Ratio
    ├─ 9:16 (Instagram Stories, TikTok, Reels)
    ├─ 1:1 (Square)
    ├─ 4:5 (Instagram Feed)
    └─ 16:9 (YouTube, Desktop)
    ↓
[Calculate Credits Required]
    ↓
[Verify Credits Available]
    ↓
[Generate] Button
    ↓
Generation Progress Screen
    ├─ Step 1: Understanding your request... ✓
    ├─ Step 2: Creating campaign strategy... ⏳
    ├─ Step 3: Generating copy...
    ├─ Step 4: Generating poster...
    ├─ Step 5: Generating video...
    └─ Step 6: Finalizing...
    ↓
Generation Complete
    ├─ View Poster
    ├─ Play Video
    ├─ Read Caption
    ├─ Download All
    ├─ Share
    └─ Save to Projects
```

### 6.3 Project Management

```
Projects / History
    ↓
Project List
    ├─ [Project Card]
    │   ├─ Thumbnail (poster preview)
    │   ├─ Title
    │   ├─ Date created
    │   ├─ Industry
    │   └─ Actions [Preview] [Download] [Share] [Regenerate] [Delete]
    ├─ Filter by date/industry
    └─ Search
    ↓
Project Details
    ├─ Campaign input
    ├─ Poster (view/download)
    ├─ Video (play/download)
    ├─ Caption (copy/share)
    ├─ Metadata (generation status, credits used)
    └─ Actions [Regenerate] [Report] [Delete]
```

### 6.4 Brand Kit

```
Brand Kit
    ↓
Save/Edit Brand Information
    ├─ Business name
    ├─ Logo (upload)
    ├─ Primary colour (color picker)
    ├─ Secondary colour (color picker)
    ├─ Accent colour (color picker)
    ├─ Font preference (dropdown)
    ├─ Website URL
    ├─ Phone number
    ├─ Address
    ├─ Social media links (Instagram, Facebook, etc.)
    ├─ Brand description (textarea)
    └─ [Save]
    ↓
Brand Kit is automatically used in all future generations
```

### 6.5 Subscription & Credits

```
Credits Screen
    ├─ Credits Balance (e.g., "245 credits remaining")
    ├─ Subscription Status (Free/Creator/Business/Pro)
    ├─ Next billing date
    ├─ Current plan benefits
    └─ [Upgrade Plan] or [Manage Subscription]
    ↓
Subscription Details
    ├─ Plan comparison
    │   ├─ FREE
    │   │   ├─ Limited monthly credits
    │   │   ├─ Watermark
    │   │   └─ 1:1, 4:5 aspect ratios only
    │   ├─ CREATOR (₹299/month)
    │   │   ├─ 5,000 credits/month
    │   │   ├─ No watermark
    │   │   └─ All aspect ratios
    │   ├─ BUSINESS (₹999/month)
    │   │   ├─ 15,000 credits/month
    │   │   ├─ Priority support
    │   │   └─ Team members (limited)
    │   └─ PRO (₹2,499/month)
    │       ├─ Unlimited credits/month
    │       ├─ Priority support
    │       ├─ Team members (unlimited)
    │       └─ Custom integrations
    ├─ Credit costs reference
    │   ├─ Poster: 100 credits
    │   ├─ Video 30s: 500 credits
    │   ├─ Video 60s: 800 credits
    │   ├─ Caption: 25 credits
    │   ├─ Voice-over: 100 credits
    │   └─ Regenerate: 50 credits (half price)
    └─ [Choose Plan] (Google Play Billing)
```

---

## 7. AI Generation Strategy

### 7.1 Orchestration Architecture

The AI generation must NOT expose keys or credentials to the mobile app.

```
Flutter Mobile App
    ↓ (HTTPS, Authenticated)
CreatorPilot Backend (FastAPI)
    ↓ (Internal, Secure)
AI Orchestrator Service
    ├─ Input Validation & Moderation
    ├─ Campaign Strategy Engine
    ├─ Content Generation Coordinator
    ├─ Image/Video Generation Pipeline
    ├─ Media Composition Engine
    └─ Output Moderation & Storage
    ↓
AI Providers (API Keys secured in backend)
    ├─ Google Gemini (text, image generation)
    ├─ Google Veo / Video Gen (video generation)
    ├─ TTS (voice-over)
    └─ Audio Library (music)
    ↓
Cloud Storage (GCS / Firebase Storage)
    ↓
Firestore (Metadata only)
    ↓
Results returned to Mobile App
```

### 7.2 Generation Pipeline

**Step 1: Input Processing**
- Validate user input
- Check available credits
- Reserve credits (lock, not deduct yet)
- Create generation job record

**Step 2: Campaign Strategy**
- Analyze business description, industry, audience
- Generate:
  - Headline
  - Subheadline
  - CTA
  - Social caption
  - Hashtags
  - Visual direction (color palette, mood, composition)
  - Video storyboard (scene-by-scene breakdown)

**Step 3: Poster Generation**
- Use visual direction from Step 2
- Generate poster image via Google Gemini or similar
- Ensure:
  - Correct aspect ratio
  - Logo placement (if in Brand Kit)
  - Brand colors used
  - Professional typography
  - No spelling errors
  - CTA prominent
  - Offer visible

**Step 4: Video Storyboard Expansion**
- Break down into individual scenes
- For each scene, generate:
  - Visual description
  - Duration (milliseconds)
  - Suggested transitions
  - Text overlays
  - Camera direction

**Step 5: Video Scene Generation**
- Use Google Veo or supported video API
- Generate each scene video clip
- Sequences: exterior → interior → product/service → customers → offer → CTA
- Handle failures gracefully (retry, fallback)

**Step 6: Audio Selection/Generation**
- Determine mood from campaign strategy
- Select licensed music OR generate via AI
- Ensure:
  - Royalty-free or properly licensed
  - Duration matches video
  - Mood appropriate

**Step 7: Voice-over (Optional)**
- If user selected voice-over:
  - Convert caption text to natural speech
  - Support multiple languages
  - Sync with video timing
  - Add emotional nuance

**Step 8: Media Composition**
- Use FFmpeg to combine:
  - Video scenes (with transitions)
  - Audio (background music)
  - Voice-over (if present)
  - Logo overlays
  - Text overlays & subtitles
  - CTA frames
  - Proper color grading

**Step 9: Final MP4 Generation**
- Encode to:
  - Format: MP4 (H.264)
  - Resolution: 1080p (height varies by aspect ratio)
  - Bitrate: Optimized for mobile
  - Frame rate: 30fps
  - Audio: AAC, normalized levels

**Step 10: Output Validation**
- Check file integrity
- Verify aspect ratio
- Confirm duration
- Test playback

**Step 11: Cloud Storage**
- Upload to Firebase Storage or GCS
- Generate secure, time-limited download URLs
- Store metadata in Firestore:
  - Project ID
  - File paths
  - URLs
  - Generation timestamp
  - Credits consumed

**Step 12: Finalize**
- Mark generation as COMPLETED
- Finalize credit usage (convert reserved → used)
- Return URLs to mobile app
- Notify user

---

## 8. Generation Statuses

Asynchronous jobs must track state:

```
REQUESTED
    ↓ (Backend received, credits reserved)
QUEUED
    ↓ (Waiting for resources)
PROCESSING
    ↓ (AI calls in progress)
GENERATING
    ↓ (Media generation)
COMPOSING
    ↓ (Combining assets)
COMPLETED
    ↓ (Success, results ready)

OR

FAILED
    ↓ (Error occurred, credits refunded)
```

Mobile app polls or receives push notifications for status updates.

---

## 9. Credit System

### 9.1 Pricing Tiers

| Plan | Cost | Monthly Credits | Features |
|------|------|-----------------|----------|
| **FREE** | ₹0 | 500 | Limited aspect ratios, watermark |
| **CREATOR** | ₹299 | 5,000 | All aspect ratios, no watermark |
| **BUSINESS** | ₹999 | 15,000 | Priority support, team features |
| **PRO** | ₹2,499 | Unlimited | Full feature set, custom integrations |

### 9.2 Credit Costs

| Operation | Credits | Notes |
|-----------|---------|-------|
| Poster generation | 100 | Text-to-image |
| Video generation (30s) | 500 | Scene-based composition |
| Video generation (60s) | 800 | Longer duration, higher cost |
| Caption generation | 25 | Text content |
| Voice-over (per language) | 100 | TTS processing |
| Regenerate campaign | 50 | Discount: half price of originals |
| Music/audio | 0 | Included in video cost |

### 9.3 Credit Reservation Flow

1. **User initiates generation** with selected outputs
2. **Backend calculates total credits**
   ```
   Poster (100) + Video (500) + Caption (25) = 625 credits
   ```
3. **Check available balance**
   - If insufficient: reject, show upgrade prompt
   - If sufficient: proceed
4. **Reserve credits** (lock in database, mark as pending)
5. **Execute generation**
6. **On success**: Finalize reserved credits → Used
7. **On partial failure**: Refund unused portion, charge used portion
8. **On complete failure**: Refund all reserved credits

**Goal:** Prevent double-charging and ensure transparent credit management.

---

## 10. Subscription & Payment

### 10.1 Google Play Billing Integration

- **Never trust the client alone** for subscription verification
- Flow:
  ```
  Google Play App Store
      ↓
  User purchases subscription
      ↓
  Google Play returns purchase token
      ↓
  Mobile app sends token to backend
      ↓
  Backend verifies token with Google Play API
      ↓
  Backend grants credits/subscription entitlement
      ↓
  Mobile app receives confirmation
  ```

### 10.2 Abstraction for Apple StoreKit

Design payment layer so Apple StoreKit can be added without major refactoring:

```
PaymentService (abstract)
    ├─ GooglePlayBillingService (iOS/Android compatible)
    ├─ AppleStoreKitService (future)
    └─ LocalPaymentService (testing)
```

---

## 11. Security Requirements

### 11.1 Critical Rules

- **Never expose AI API keys** in Flutter app
- **Never expose Firebase service account** keys
- **Validate every backend request**
- **Authenticate all protected APIs** (Firebase Auth)
- **Authorize access**: Users can only access their own projects
- **Rate limits**: Prevent abuse (e.g., 5 generation requests/minute per user)
- **Generation limits**: Max 100 generations/month per free user
- **File validation**: Uploaded files validated for type, size, content
- **Upload limits**: Max file size (e.g., logo: 5MB)
- **Media scanning**: Scan generated content for harmful/NSFW material
- **Cloud storage security**: Firebase security rules, signed URLs with expiry
- **App Check**: Implement Firebase App Check to prevent bot abuse
- **Logging**: Structured logs, never log secrets or sensitive user data

### 11.2 Data Classification

| Level | Examples | Handling |
|-------|----------|----------|
| **Public** | App version, feature list | Log freely |
| **Internal** | User ID, subscription status | Log with context, no full records |
| **Sensitive** | API keys, passwords, tokens | Never log |
| **Private** | User campaign content | Log only errors, not content |

---

## 12. AI Safety & Content Moderation

### 12.1 Input Moderation

- Check user input for:
  - Hate speech
  - Violence
  - Illegal activities
  - Spam/abuse
- Flag high-risk inputs
- Reject or prompt user

### 12.2 Output Moderation

- Scan generated images/videos for:
  - NSFW content
  - Explicit material
  - Copyright infringement flags
  - Quality issues
- Return to user for review

### 12.3 Reporting System

Provide "Report AI Output" button on generated content:

```
[Report] button
    ↓
Report form
    ├─ Reason (dropdown)
    │   ├─ Inappropriate content
    │   ├─ Copyright issue
    │   ├─ Poor quality
    │   ├─ Incorrect information
    │   └─ Other
    ├─ Additional comments (optional)
    └─ [Submit]
    ↓
Report stored in Firestore
    ↓
Admin dashboard notified
    ↓
Admin reviews and takes action
```

---

## 13. Admin Dashboard

### 13.1 Key Metrics

```
Overview
├─ Total Users (all-time, active this month)
├─ Active Users (last 7 days, last 30 days)
├─ Subscribers (by plan: Free, Creator, Business, Pro)
├─ Revenue (monthly, YTD)
├─ Credits Consumed (monthly total)
├─ AI Generations (successful, failed, pending)
├─ Success Rate (%)
├─ Storage Used (GB)
└─ Estimated AI Cost (from provider bills)
```

### 13.2 Admin Capabilities

- **Users**
  - Search by email/ID
  - View subscription status
  - View credit balance
  - Adjust credits (add/subtract)
  - Disable account
  - View generation history
  - View reports submitted by user

- **Reports**
  - List all AI output reports
  - View flagged content
  - Filter by reason/date
  - Mark as reviewed
  - Take action (keep/remove/investigate)
  - Email user if needed

- **Failed Jobs**
  - Filter by error type
  - View error logs
  - Retry generation
  - Refund credits manually
  - Investigate issues

- **Configuration**
  - Edit credit costs
  - Edit subscription plans/pricing
  - Configure generation limits
  - Manage AI provider settings
  - View API usage by provider
  - Set maintenance mode

- **Monitoring**
  - API latency (p50, p95, p99)
  - Generation latency by step
  - Error rates
  - Crash reports
  - Storage usage trends
  - AI cost trends

---

## 14. Observability & Logging

### 14.1 Structured Logging

Every significant event logged as JSON:

```json
{
  "timestamp": "2026-08-18T10:30:00Z",
  "level": "INFO",
  "service": "ai-orchestrator",
  "event": "generation_started",
  "user_id": "user-123",
  "project_id": "proj-456",
  "outputs": ["poster", "video", "caption"],
  "estimated_credits": 625,
  "generation_id": "gen-789"
}
```

### 14.2 Metrics to Track

- **API Performance**
  - Request latency (ms)
  - Response codes (2xx, 4xx, 5xx)
  - Throughput (requests/sec)

- **Generation Pipeline**
  - Step latency (strategy, poster, video, composition, etc.)
  - Success/failure rate per step
  - Retry counts
  - Total generation time

- **AI Provider Health**
  - API latency per provider
  - Error rate per provider
  - Cost per generation
  - Token usage (Gemini)

- **Storage**
  - Total GCS usage (GB)
  - Storage growth trend
  - Cleanup stats (old files deleted)

- **User Behavior**
  - Campaigns created per day
  - Most popular industry
  - Most popular style
  - Aspect ratio distribution
  - Regeneration rate

---

## 15. Testing Strategy

### 15.1 Test Types

| Type | Scope | Tools | Example |
|------|-------|-------|----------|
| **Unit** | Single functions/methods | Dart/Python unittest | Test credit calculation |
| **Integration** | Component interaction | Dart/Python + Firebase emulator | Test auth + DB |
| **API** | Backend endpoints | Postman/pytest | Test /generate endpoint |
| **Widget** | UI components | Flutter widget tests | Test campaign form |
| **E2E** | Full user flow | Flutter integration tests | Create campaign → download |
| **Performance** | Load/stress | k6/Locust | 100 concurrent generations |
| **Security** | Vulnerabilities | Manual + SAST tools | JWT validation, SQL injection |

### 15.2 Mock AI Providers

For automated tests, use mock implementations:

```python
class AIProviderInterface:
    async def generate_text(self, prompt: str) -> str: ...
    async def generate_image(self, prompt: str) -> bytes: ...
    async def generate_video(self, prompt: str) -> bytes: ...

class MockGeminiProvider(AIProviderInterface):
    async def generate_text(self, prompt: str) -> str:
        return "Mock response: Campaign Strategy"
    async def generate_image(self, prompt: str) -> bytes:
        return create_placeholder_image()  # Small PNG for tests
    async def generate_video(self, prompt: str) -> bytes:
        return create_placeholder_video()  # Small MP4 for tests
```

### 15.3 Critical User Flow Tests

- [x] User can sign up with email
- [x] User can authenticate with Google
- [x] User can create campaign
- [x] Poster generation works end-to-end
- [x] Video generation job created successfully
- [x] Video generation completes asynchronously
- [x] Credit reservation prevents overspend
- [x] Subscription verification works
- [x] Failed generation refunds credits
- [x] Admin can view user reports
- [x] Admin can adjust user credits

---

## 16. MVP Scope (V1.0)

### Included:

- ✅ Authentication (Email + Google)
- ✅ Campaign creation form
- ✅ AI campaign planning
- ✅ Poster generation
- ✅ 30-second video generation (scene-based)
- ✅ Caption generation
- ✅ Audio/music integration
- ✅ Project history & management
- ✅ Download & share
- ✅ Brand Kit
- ✅ Credit system
- ✅ Google Play Billing (subscriptions)
- ✅ Basic admin dashboard
- ✅ Reporting (user reports AI output)
- ✅ Security & authentication

### NOT Included (V2+):

- ❌ Social media scheduling (direct publishing)
- ❌ Instagram/TikTok API integration
- ❌ Advanced video editor
- ❌ Team collaboration
- ❌ Enterprise billing
- ❌ Multi-provider AI orchestration (only Google initially)
- ❌ iOS release (prepare for, don't release in V1)
- ❌ Web admin dashboard (mobile-first)
- ❌ 60-second videos
- ❌ Custom fonts upload
- ❌ Animation timeline editor

---

## 17. Success Metrics (Post-MVP)

- User can create a professional campaign in < 3 minutes
- Generated poster quality score > 8/10 (user feedback)
- Generated video play rate > 70% (completed watch)
- Subscription conversion rate > 5%
- Generation success rate > 95%
- API latency p95 < 2 seconds
- Video generation < 60 seconds (30-second video)
- User retention (30 days) > 30%

---

## 18. Glossary

| Term | Definition |
|------|------------|
| **Campaign** | A single user request with complete output package |
| **Generation** | The AI processing job for a campaign |
| **Project** | Saved campaign in user history |
| **Credits** | Virtual currency for AI usage (consumed per generation) |
| **Brand Kit** | User's saved branding (logo, colors, info) |
| **Aspect Ratio** | Video/image dimension ratio (9:16, 1:1, etc.) |
| **Storyboard** | Scene-by-scene breakdown of video |
| **Composition** | Combining video/audio/text into final MP4 |
| **Orchestrator** | Backend service coordinating AI calls |
| **Moderation** | Scanning content for policy violations |

---

## Document Status

**PHASE 0 STATUS: ARCHITECTURE DEFINED**

- ✅ Product vision clear
- ✅ User flows mapped
- ✅ Technology stack defined
- ✅ Credit system designed
- ✅ Security requirements listed
- ✅ AI orchestration pipeline documented
- ⏳ Ready for implementation

---

**Next:** Architecture document detailing system design, API contracts, and database schema.
