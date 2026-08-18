# CreatorPilot AI - Google Play Store Release Checklist

**Version:** 1.0  
**Status:** Pre-Release Planning  
**Last Updated:** August 2026

---

## 1. Pre-Release Preparation

### 1.1 Application Setup

- [ ] **Package Name Finalized**
  - Package: `com.creatorpilot.app`
  - Must be unique, reverse-domain format
  - Cannot be changed after first release
  - Register at Google Play Console

- [ ] **App Signing Key Created**
  - Generate release keystore:
    ```bash
    keytool -genkey -v -keystore creatorpilot-release.keystore \
      -keyalg RSA -keysize 2048 -validity 10000 \
      -alias creatorpilot-release
    ```
  - Store securely (never commit to Git)
  - Back up in secure location
  - Keystore password saved in secret manager

- [ ] **Gradle Configuration**
  ```gradle
  android {
    compileSdkVersion 34
    minSdkVersion 24
    targetSdkVersion 34
    
    signingConfigs {
      release {
        storeFile file("creatorpilot-release.keystore")
        storePassword System.getenv("KEYSTORE_PASSWORD")
        keyAlias System.getenv("KEY_ALIAS")
        keyPassword System.getenv("KEY_PASSWORD")
      }
    }
    
    buildTypes {
      release {
        signingConfig signingConfigs.release
        minifyEnabled true
        shrinkResources true
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
      }
    }
  }
  ```

- [ ] **Android App Bundle (.aab) Built**
  ```bash
  flutter build appbundle --release
  # Output: build/app/outputs/bundle/release/app-release.aab
  ```

- [ ] **Google Play Developer Account**
  - Account created at play.google.com/console
  - Payment method added
  - Merchant account registered

---

### 1.2 Application Assets

#### Branding

- [ ] **App Icon (512x512 px)**
  - High quality PNG
  - No transparent areas (solid background)
  - Recognizable at small sizes
  - Should reflect "CreatorPilot AI" branding
  - File: `icon_512x512.png`

- [ ] **Feature Graphic (1024x500 px)**
  - Showcase app's main features
  - Professional design
  - Visible on app store listing
  - File: `feature_graphic.png`

#### Screenshots

- [ ] **Phone Screenshots (min 2, max 8)**
  - Dimensions: 1080x1920 px (9:16 aspect ratio)
  - Minimum 2 required, recommended 4-5
  - Should show:
    1. Campaign creation form
    2. Generation in progress
    3. Generated results (poster + video)
    4. Project history
    5. Brand Kit setup
  - Include text overlays explaining features
  - Files: `screenshot_1.png`, `screenshot_2.png`, etc.

- [ ] **Tablet Screenshots (optional)**
  - Dimensions: 1440x2560 px (9:16 aspect ratio)
  - Recommended but not required for MVP

#### Descriptions

- [ ] **Short Description (80 characters max)**
  ```
  "One Idea. Complete Content. AI-powered promotional campaigns in minutes."
  ```

- [ ] **Full Description (4000 characters max)**
  ```
  CreatorPilot AI transforms your business ideas into complete promotional 
  content packages in minutes.
  
  FEATURES:
  ✓ AI-Generated Professional Posters
    Create stunning promotional posters with your brand colors, logo, and 
    call-to-action. Perfect for Instagram, Facebook, and printing.
  
  ✓ 30-Second Promotional Videos
    Get cinematic, scene-based video campaigns with professional transitions,
    music, and optional voice-over in multiple languages.
  
  ✓ Social Media Captions
    Automatically generate engaging Instagram/TikTok captions with hashtags
    and CTAs optimized for your industry.
  
  ✓ Multi-Language Voice-Over
    Add professional AI voice-overs in English, Telugu, Hindi, Tamil, Kannada
    and more. Perfectly synchronized with your video.
  
  ✓ Brand Kit
    Save your business branding (logo, colors, contact info, fonts) and 
    reuse across all future campaigns.
  
  ✓ Project History
    Browse, download, and share all your generated campaigns. Regenerate
    with new variations anytime.
  
  SUBSCRIPTIONS:
  - FREE: 500 monthly credits with watermark
  - CREATOR: ₹299/month for 5,000 credits, no watermark
  - BUSINESS: ₹999/month for 15,000 credits, priority support
  - PRO: ₹2,499/month unlimited credits
  
  PERFECT FOR:
  ✓ Restaurants & Cafes
  ✓ E-commerce & Retail Stores  
  ✓ Salons & Spas
  ✓ Fitness & Wellness Centers
  ✓ Services & Agencies
  ✓ Event Organizers
  ✓ Content Creators
  
  No design experience needed. No expensive video software required.
  Just describe your campaign, and CreatorPilot AI handles the rest.
  ```

---

## 2. Store Listing Configuration

### 2.1 Basic Store Listing

- [ ] **App Title**
  ```
  CreatorPilot AI - Content Creator
  ```
  (Max 50 characters)

- [ ] **Short Description**
  ```
  One Idea. Complete Content. Create promotional campaigns with AI
  ```
  (Max 80 characters)

- [ ] **Full Description** (see above)

- [ ] **Category**
  - Primary: `Business`
  - Secondary: `Productivity`

- [ ] **Content Rating Questionnaire**
  - Completed and submitted
  - Result: General Audiences (or higher if applicable)

---

### 2.2 Privacy & Security

- [ ] **Privacy Policy URL**
  ```
  https://creatorpilot.ai/privacy
  ```
  - Must be publicly accessible
  - Clearly describe data collection
  - Address GDPR compliance
  - Include right to deletion

- [ ] **Terms of Service URL**
  ```
  https://creatorpilot.ai/terms
  ```
  - Cover user obligations
  - Intellectual property rights
  - Limitation of liability

- [ ] **Data Safety Section**
  - [ ] Data collected:
    - User ID & email (Authentication)
    - Campaign input text (Generation)
    - Subscription info (Payment)
    - Device identifiers (Analytics)
  - [ ] Data not shared with third parties (except payment processors)
  - [ ] Users can request data deletion
  - [ ] Data encrypted in transit (HTTPS)
  - [ ] Data encrypted at rest (Cloud)

- [ ] **Permissions Justification**
  - `INTERNET` - API communication
  - `CAMERA` - (if adding logo upload)
  - `READ_EXTERNAL_STORAGE` - (if adding media import)
  - `WRITE_EXTERNAL_STORAGE` - Download results

---

### 2.3 Target Audience & Content Rating

- [ ] **Target Audience**
  - Ages: 13+
  - Maturity: General
  - Inappropriate content: None

- [ ] **Content Rating Form**
  - Violence: No
  - Adult content: No
  - Profanity: No
  - Alcohol/tobacco: No
  - Gambling: No

---

## 3. In-App Purchases & Subscriptions

### 3.1 Subscription Products

- [ ] **CREATOR (Monthly)**
  - Product ID: `com.creatorpilot.creator.monthly`
  - Price: ₹299
  - Billing period: Monthly
  - Description: "5,000 credits/month, no watermark"
  - Status: Active

- [ ] **BUSINESS (Monthly)**
  - Product ID: `com.creatorpilot.business.monthly`
  - Price: ₹999
  - Billing period: Monthly
  - Description: "15,000 credits/month, priority support"
  - Status: Active

- [ ] **PRO (Monthly)**
  - Product ID: `com.creatorpilot.pro.monthly`
  - Price: ₹2,499
  - Billing period: Monthly
  - Description: "Unlimited credits/month"
  - Status: Active

### 3.2 Subscription Management

- [ ] **Free Trial**
  - Consider 7-day free trial to reduce friction
  - Converts users before first charge
  - Requires clear terms

- [ ] **Subscription Billing Terms**
  - Clearly displayed before purchase
  - User must explicitly agree
  - Can cancel anytime
  - Recurring billing clearly stated

---

## 4. Testing & Compliance

### 4.1 Functional Testing

- [ ] **Authentication**
  - [ ] Email signup works
  - [ ] Google OAuth works
  - [ ] Login/logout works
  - [ ] JWT token refresh works

- [ ] **Campaign Creation**
  - [ ] Form validation works
  - [ ] Brand Kit saves correctly
  - [ ] Can select outputs
  - [ ] Can select aspect ratio

- [ ] **Generation**
  - [ ] Credits check works
  - [ ] Generation starts
  - [ ] Status polling works
  - [ ] Results download works
  - [ ] Retry on failure works

- [ ] **Subscription**
  - [ ] Can view plans
  - [ ] Can purchase via Google Play
  - [ ] Credits granted after purchase
  - [ ] Can cancel subscription

- [ ] **Payments**
  - [ ] Test purchases with Google Play test account
  - [ ] Confirm credits appear immediately
  - [ ] Test subscription cancellation
  - [ ] Test failed payment handling

### 4.2 Device Testing

- [ ] **Devices Tested**
  - [ ] Pixel 4a (mid-range)
  - [ ] Samsung Galaxy A12 (budget)
  - [ ] OnePlus 9 (flagship)
  - [ ] Tablet (if applicable)

- [ ] **Android Versions**
  - [ ] Android 7.0 (API 24, minimum)
  - [ ] Android 10 (API 29)
  - [ ] Android 13 (API 33)
  - [ ] Android 14 (API 34, latest)

- [ ] **Network Conditions**
  - [ ] WiFi
  - [ ] 4G
  - [ ] Poor connectivity (network throttling)
  - [ ] No connectivity (offline handling)

### 4.3 Compliance Testing

- [ ] **Policy Compliance**
  - [ ] No malware/trojans
  - [ ] No deceptive practices
  - [ ] No spam
  - [ ] Proper ad disclosure (if any ads)

- [ ] **Content Policies**
  - [ ] No hate speech
  - [ ] No violence
  - [ ] No adult content
  - [ ] No misleading claims

- [ ] **Privacy & Security**
  - [ ] No hardcoded API keys
  - [ ] HTTPS for all communications
  - [ ] No unnecessary permissions requested
  - [ ] No data sold to third parties

- [ ] **Ads & Monetization**
  - [ ] (If applicable) Ad networks approved
  - [ ] (If applicable) Ad frequency reasonable
  - [ ] (If applicable) Ad targeting compliant

---

## 5. Release Channels

### 5.1 Internal Testing

**Timeline: Week 1-2**

- [ ] Build deployed to internal testing track
- [ ] Internal team tests all flows
- [ ] Bugs logged and fixed
- [ ] Ready for closed testing

### 5.2 Closed Testing (Closed Beta)

**Timeline: Week 2-3**

- [ ] 10-50 testers invited (friends, beta users)
- [ ] Collects feedback on usability
- [ ] 1-2 week testing period
- [ ] Critical bugs fixed
- [ ] Ready for open testing

### 5.3 Open Testing (Open Beta)

**Timeline: Week 3-4**

- [ ] Released to anyone who wants to test
- [ ] Public app store visibility marked "Beta"
- [ ] Real user feedback collected
- [ ] Analytics enabled
- [ ] Stability verified
- [ ] Ready for production

### 5.4 Production Release

**Timeline: Week 4+**

- [ ] App promoted from beta to production
- [ ] Available to all users
- [ ] Staged rollout (start at 10%, then 50%, then 100%)
- [ ] Monitor crash rates and user feedback
- [ ] Rollback plan ready if needed

---

## 6. Release Management

### 6.1 Pre-Release Checklist

**1 Week Before Launch:**

- [ ] All bugs fixed and tested
- [ ] Performance optimized (crash rate < 0.5%)
- [ ] No hardcoded test values
- [ ] Analytics configured
- [ ] Crash reporting enabled
- [ ] Rate limiting configured
- [ ] Support email functional
- [ ] Documentation updated
- [ ] Team briefed on support escalation

**1 Day Before Launch:**

- [ ] Final QA pass completed
- [ ] Backup plan ready
- [ ] Team on-call for launch day
- [ ] Status page prepared
- [ ] Support message templates ready

### 6.2 Launch Day Operations

- [ ] Monitor crash reports in real-time
- [ ] Monitor user feedback in store reviews
- [ ] Monitor API performance (latency, errors)
- [ ] Monitor generation success rate
- [ ] Team available for rapid hotfixes
- [ ] Daily metrics reviewed

### 6.3 Post-Launch Monitoring (First 30 days)

- [ ] Crash rate target: < 0.1%
- [ ] ANR (App Not Responding) target: < 0.05%
- [ ] Generation success rate: > 95%
- [ ] API latency p95: < 3 seconds
- [ ] User retention day 1: > 20%
- [ ] User retention day 7: > 5%

---

## 7. Version & Updates

### 7.1 Version Numbering

```
Format: MAJOR.MINOR.PATCH
Example: 1.0.0

1 = First production release
0 = No minor features yet
0 = No patches yet

Next:
1.0.1 = Bug fix
1.1.0 = New feature (voice-over languages)
2.0.0 = Major redesign
```

### 7.2 Update Cadence

- **Critical Security Updates**: ASAP
- **Bug Fixes**: 1-2 week cycles
- **Feature Releases**: Monthly (if planned)
- **OS Updates**: Quarterly (Android version support)

---

## 8. Success Metrics (Post-Launch)

### 8.1 Installation & Engagement

- Target: 1,000+ installs in first month
- Target: 30% day-1 retention
- Target: 10% day-7 retention
- Target: 5% day-30 retention

### 8.2 Monetization

- Target: 5% conversion to paid (subscriptions)
- Target: 50% of paid users keep subscription > 30 days
- Target: Average revenue per user (ARPU) > ₹50

### 8.3 Quality

- Target: Rating > 4.2 stars
- Target: Crash rate < 0.1%
- Target: User support responses < 24 hours

---

## Document Status

**PHASE 0 STATUS: PLAY STORE CHECKLIST READY**

- ✅ Pre-release preparation defined
- ✅ Assets requirements specified
- ✅ Store listing template created
- ✅ Testing & compliance checklist documented
- ✅ Release channels defined
- ✅ Launch operations outlined
- ✅ Success metrics established
- ✅ Ready for Phase 1 implementation

---

## PHASE 0 COMPLETE

**All documentation delivered:**

1. ✅ **PRD.md** - Product vision & user flows
2. ✅ **ARCHITECTURE.md** - System design
3. ✅ **DATABASE.md** - Firestore schema & security
4. ✅ **API.md** - Backend endpoint specifications
5. ✅ **AI_WORKFLOW.md** - Generation pipeline
6. ✅ **SECURITY.md** - Security implementation
7. ✅ **BILLING.md** - Subscription & credit system
8. ✅ **PLAY_STORE.md** - Release requirements

**Next Phase: PHASE 1 - Repository Scaffolding & Project Structure**

Ready to begin implementation.
