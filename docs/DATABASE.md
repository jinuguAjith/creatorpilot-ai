# CreatorPilot AI - Database Schema & Design

**Version:** 1.0  
**Status:** MVP Schema  
**Last Updated:** August 2026

---

## 1. Firestore Collections Overview

### Collection Hierarchy

```
firestore/
├── users/
│   ├── {user_id}/
│   │   ├── profile (document)
│   │   ├── subscription (document)
│   │   ├── credits (document)
│   │   └── brand_kits/ (subcollection)
│   │       └── {brand_kit_id}/ (document)
│   │
├── projects/
│   ├── {project_id}/ (document)
│   └── generations/ (subcollection)
│       └── {generation_id}/ (document)
│
├── generations/
│   └── {generation_id}/ (document)
│       └── artifacts/ (subcollection)
│           ├── poster.json
│           ├── video.json
│           └── caption.json
│
├── subscriptions/
│   ├── plans/ (collection)
│   │   └── {plan_id}/ (document)
│   └── user_subscriptions/ (collection)
│       └── {subscription_id}/ (document)
│
├── credit_transactions/
│   └── {transaction_id}/ (document)
│
├── reports/
│   └── {report_id}/ (document)
│
└── admin_config/
    ├── credit_costs/ (document)
    ├── generation_limits/ (document)
    └── feature_flags/ (document)
```

---

## 2. Collection Schemas

### 2.1 `users` Collection

**Path:** `/users/{user_id}`

**Document: `profile`**
```json
{
  "user_id": "firebase-uid-123",
  "email": "user@example.com",
  "display_name": "John Doe",
  "avatar_url": "https://...",
  "phone": "+91-9876543210",
  "country": "IN",
  "language": "en",
  "timezone": "Asia/Kolkata",
  "account_status": "ACTIVE",
  "created_at": "2026-08-18T10:00:00Z",
  "updated_at": "2026-08-18T10:00:00Z",
  "last_login": "2026-08-18T10:00:00Z",
  "onboarding_completed": true,
  "preferences": {
    "notifications_enabled": true,
    "email_frequency": "weekly",
    "theme": "light"
  },
  "metadata": {
    "device_count": 2,
    "last_ip": "203.0.113.45",
    "app_version": "1.0.0"
  }
}
```

**Document: `subscription`**
```json
{
  "user_id": "firebase-uid-123",
  "plan_id": "plan-creator-monthly",
  "plan_name": "CREATOR",
  "status": "ACTIVE",
  "start_date": "2026-08-01T00:00:00Z",
  "renewal_date": "2026-09-01T00:00:00Z",
  "cancellation_date": null,
  "auto_renew": true,
  "purchase_token": "google-play-purchase-token",
  "platform": "android",
  "price_local": {
    "amount": 299,
    "currency": "INR"
  },
  "entitlements": [
    "no_watermark",
    "all_aspect_ratios",
    "monthly_credits_5000"
  ],
  "created_at": "2026-08-01T00:00:00Z",
  "updated_at": "2026-08-18T10:00:00Z"
}
```

**Document: `credits`**
```json
{
  "user_id": "firebase-uid-123",
  "total_purchased": 5000,
  "total_used": 325,
  "available_balance": 4675,
  "reserved": 100,
  "effective_balance": 4575,
  "monthly_limit": 5000,
  "monthly_used": 325,
  "reset_date": "2026-09-01T00:00:00Z",
  "last_transaction_id": "txn-456",
  "last_updated": "2026-08-18T10:30:00Z",
  "expiry_info": {
    "older_credits_expire_at": "2026-09-18T00:00:00Z",
    "expiring_credits_count": 100
  }
}
```

**Subcollection: `brand_kits`**

Path: `/users/{user_id}/brand_kits/{brand_kit_id}`

```json
{
  "brand_kit_id": "bk-001",
  "user_id": "firebase-uid-123",
  "business_name": "Bella Aroma Restaurant",
  "logo_url": "gs://bucket/logos/bk-001/logo.png",
  "colors": {
    "primary": "#8B4513",
    "secondary": "#D4A574",
    "accent": "#FFD700"
  },
  "fonts": {
    "primary": "Playfair Display",
    "secondary": "Open Sans"
  },
  "contact_info": {
    "phone": "+91-98765-43210",
    "email": "hello@bellaaroma.com",
    "address": "123 MG Road, Bangalore, India",
    "website": "https://bellaaroma.com",
    "social_links": {
      "instagram": "@bellaaroma",
      "facebook": "BellaAroma"
    }
  },
  "description": "Luxury Italian cuisine specializing in authentic recipes",
  "is_default": true,
  "created_at": "2026-07-15T00:00:00Z",
  "updated_at": "2026-08-18T10:00:00Z"
}
```

---

### 2.2 `projects` Collection

**Path:** `/projects/{project_id}`

```json
{
  "project_id": "proj-789",
  "user_id": "firebase-uid-123",
  "title": "Bella Aroma Grand Opening Campaign",
  "description": "Promotional campaign for restaurant grand opening",
  "industry": "RESTAURANT",
  "campaign_input": {
    "business_description": "Luxury Italian restaurant, grand opening this Sunday with 20% offer",
    "target_audience": "Couples and families",
    "tone": "Elegant",
    "offer": "20% opening discount",
    "location": "Bangalore, India"
  },
  "brand_kit_id": "bk-001",
  "generation_ids": [
    "gen-1001",
    "gen-1002"
  ],
  "latest_generation_id": "gen-1002",
  "status": "COMPLETED",
  "aspect_ratio": "9:16",
  "created_at": "2026-08-15T14:30:00Z",
  "updated_at": "2026-08-15T14:45:00Z",
  "metadata": {
    "view_count": 12,
    "download_count": 3,
    "share_count": 1
  }
}
```

**Subcollection: `generations`**

Path: `/projects/{project_id}/generations/{generation_id}`

```json
{
  "generation_id": "gen-1002",
  "project_id": "proj-789",
  "user_id": "firebase-uid-123",
  "status": "COMPLETED",
  "outputs_requested": [
    "poster",
    "video",
    "caption"
  ],
  "credits_reserved": 625,
  "credits_used": 625,
  "started_at": "2026-08-15T14:31:00Z",
  "completed_at": "2026-08-15T14:44:00Z",
  "duration_ms": 780000,
  "results": {
    "poster": {
      "gcs_path": "gs://bucket/media/gen-1002/poster.png",
      "download_url": "https://signed-url.../poster.png",
      "size_bytes": 2456789,
      "dimensions": "1080x1920"
    },
    "video": {
      "gcs_path": "gs://bucket/media/gen-1002/video.mp4",
      "download_url": "https://signed-url.../video.mp4",
      "size_bytes": 125000000,
      "dimensions": "1080x1920",
      "duration_seconds": 30,
      "fps": 30
    },
    "caption": {
      "text": "Experience authentic Italian cuisine at Bella Aroma...",
      "hashtags": ["#BellaAroma", "#ItalianCuisine", "#Bangalore"],
      "cta": "Reserve your table now!"
    }
  },
  "error": null,
  "retry_count": 0,
  "orchestrator_job_id": "orch-job-5678"
}
```

---

### 2.3 `generations` Collection (Top-level)

**Path:** `/generations/{generation_id}`

```json
{
  "generation_id": "gen-1002",
  "user_id": "firebase-uid-123",
  "project_id": "proj-789",
  "status": "COMPLETED",
  "step_status": {
    "input_moderation": {
      "status": "COMPLETED",
      "started_at": "2026-08-15T14:31:00Z",
      "completed_at": "2026-08-15T14:31:10Z",
      "error": null
    },
    "campaign_strategy": {
      "status": "COMPLETED",
      "started_at": "2026-08-15T14:31:10Z",
      "completed_at": "2026-08-15T14:32:00Z",
      "data": {
        "headline": "Elegant Dining Awaits",
        "visual_direction": "Warm, sophisticated, cinematic"
      },
      "error": null
    },
    "poster_generation": {
      "status": "COMPLETED",
      "started_at": "2026-08-15T14:32:00Z",
      "completed_at": "2026-08-15T14:35:30Z",
      "error": null
    },
    "video_generation": {
      "status": "COMPLETED",
      "started_at": "2026-08-15T14:35:30Z",
      "completed_at": "2026-08-15T14:42:00Z",
      "error": null
    },
    "media_composition": {
      "status": "COMPLETED",
      "started_at": "2026-08-15T14:42:00Z",
      "completed_at": "2026-08-15T14:44:00Z",
      "error": null
    }
  },
  "cost_estimate": {
    "gemini_calls": 3,
    "gemini_cost_usd": 0.15,
    "veo_calls": 1,
    "veo_cost_usd": 2.50,
    "ffmpeg_seconds": 45,
    "ffmpeg_cost_usd": 0.10,
    "total_cost_usd": 2.75
  },
  "created_at": "2026-08-15T14:30:00Z",
  "updated_at": "2026-08-15T14:44:00Z"
}
```

**Subcollection: `artifacts`**

Path: `/generations/{generation_id}/artifacts/{artifact_id}`

```json
{
  "artifact_id": "poster",
  "generation_id": "gen-1002",
  "type": "image",
  "gcs_path": "gs://bucket/media/gen-1002/poster.png",
  "mime_type": "image/png",
  "size_bytes": 2456789,
  "dimensions": {
    "width": 1080,
    "height": 1920,
    "aspect_ratio": "9:16"
  },
  "metadata": {
    "prompt_used": "Create a luxury Italian restaurant poster...",
    "model": "gemini-pro-vision",
    "generation_time_ms": 8000
  },
  "created_at": "2026-08-15T14:33:00Z"
}
```

---

### 2.4 `subscriptions/plans` Collection

**Path:** `/subscriptions/plans/{plan_id}`

```json
{
  "plan_id": "plan-creator-monthly",
  "name": "CREATOR",
  "tier": 1,
  "price": {
    "amount": 299,
    "currency": "INR",
    "billing_period": "MONTHLY"
  },
  "google_play_product_id": "com.creatorpilot.creator.monthly",
  "features": {
    "monthly_credits": 5000,
    "no_watermark": true,
    "all_aspect_ratios": true,
    "priority_support": false,
    "team_members": 1
  },
  "limits": {
    "concurrent_generations": 3,
    "daily_generations": 50,
    "max_video_duration_seconds": 30
  },
  "is_active": true,
  "description": "For individual creators",
  "created_at": "2026-07-01T00:00:00Z",
  "updated_at": "2026-08-18T10:00:00Z"
}
```

---

### 2.5 `credit_transactions` Collection

**Path:** `/credit_transactions/{transaction_id}`

```json
{
  "transaction_id": "txn-456",
  "user_id": "firebase-uid-123",
  "type": "DEBIT",
  "amount": 625,
  "previous_balance": 5300,
  "new_balance": 4675,
  "reason": "GENERATION_COMPLETED",
  "generation_id": "gen-1002",
  "project_id": "proj-789",
  "status": "COMPLETED",
  "metadata": {
    "outputs": ["poster", "video", "caption"],
    "breakdown": {
      "poster": 100,
      "video": 500,
      "caption": 25
    }
  },
  "created_at": "2026-08-15T14:44:00Z"
}
```

---

### 2.6 `reports` Collection

**Path:** `/reports/{report_id}`

```json
{
  "report_id": "rpt-001",
  "user_id": "firebase-uid-123",
  "generation_id": "gen-1002",
  "type": "INAPPROPRIATE_CONTENT",
  "description": "Generated image contains sensitive content",
  "status": "PENDING",
  "severity": "HIGH",
  "evidence_url": "https://signed-url.../gen-1002/poster.png",
  "admin_notes": null,
  "resolution": null,
  "created_at": "2026-08-15T15:00:00Z",
  "updated_at": "2026-08-15T15:00:00Z"
}
```

---

### 2.7 `admin_config` Collection

**Document: `credit_costs`**

Path: `/admin_config/credit_costs`

```json
{
  "poster": 100,
  "video_30s": 500,
  "video_60s": 800,
  "caption": 25,
  "voiceover": 100,
  "regenerate": 50,
  "last_updated_at": "2026-08-18T10:00:00Z",
  "last_updated_by": "admin-user-1"
}
```

**Document: `generation_limits`**

Path: `/admin_config/generation_limits`

```json
{
  "free_user": {
    "monthly_generations": 5,
    "daily_generations": 2,
    "concurrent_jobs": 1
  },
  "creator_user": {
    "monthly_generations": 100,
    "daily_generations": 50,
    "concurrent_jobs": 3
  },
  "business_user": {
    "monthly_generations": 500,
    "daily_generations": 200,
    "concurrent_jobs": 5
  },
  "pro_user": {
    "monthly_generations": null,
    "daily_generations": null,
    "concurrent_jobs": 10
  },
  "last_updated_at": "2026-08-18T10:00:00Z"
}
```

---

## 3. Firestore Indexes

### Composite Indexes (Required)

| Collection | Fields | Order | Purpose |
|---|---|---|---|
| `projects` | `user_id` | Asc | List user's projects |
| `projects` | `user_id`, `created_at` | Asc, Desc | Get recent projects |
| `generations` | `user_id`, `status` | Asc, Asc | Get pending generations |
| `generations` | `user_id`, `created_at` | Asc, Desc | Generation history |
| `credit_transactions` | `user_id`, `created_at` | Asc, Desc | Transaction history |
| `reports` | `status`, `created_at` | Asc, Desc | Unreviewed reports |

### Single Field Indexes

```
Collections with single-field indexes on:
- user_id (all collections)
- status (generations, reports)
- created_at (all collections)
- updated_at (frequently filtered collections)
```

---

## 4. Firestore Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Helper function to check if user is authenticated
    function isAuthenticated() {
      return request.auth != null;
    }

    // Helper to get user ID from auth
    function getUserId() {
      return request.auth.uid;
    }

    // Helper to check if user is admin
    function isAdmin() {
      return get(/databases/{database}/documents/users/{getUserId()}).data.role == 'admin';
    }

    // Users collection - own profile only
    match /users/{userId} {
      allow read: if isAuthenticated() && getUserId() == userId;
      allow create: if isAuthenticated() && getUserId() == userId;
      allow update: if isAuthenticated() && getUserId() == userId;
      allow delete: if false; // Never delete via Firestore

      // Brand kits subcollection
      match /brand_kits/{brandKitId} {
        allow read: if isAuthenticated() && getUserId() == userId;
        allow create: if isAuthenticated() && getUserId() == userId;
        allow update: if isAuthenticated() && getUserId() == userId;
        allow delete: if isAuthenticated() && getUserId() == userId;
      }
    }

    // Projects collection
    match /projects/{projectId} {
      allow read: if isAuthenticated() && getUserId() == resource.data.user_id;
      allow create: if isAuthenticated() && getUserId() == request.resource.data.user_id;
      allow update: if isAuthenticated() && getUserId() == resource.data.user_id;
      allow delete: if isAuthenticated() && getUserId() == resource.data.user_id;

      // Generations subcollection
      match /generations/{generationId} {
        allow read: if isAuthenticated() && getUserId() == resource.data.user_id;
        allow create: if isAuthenticated() && getUserId() == request.resource.data.user_id;
        allow update: if isAuthenticated() && getUserId() == resource.data.user_id;
      }
    }

    // Generations collection (top-level)
    match /generations/{generationId} {
      allow read: if isAuthenticated() && getUserId() == resource.data.user_id;
      allow create: if false; // Created via backend only
      allow update: if false; // Updated via backend only

      // Artifacts subcollection
      match /artifacts/{artifactId} {
        allow read: if isAuthenticated() && getUserId() == get(/databases/{database}/documents/generations/{generationId}).data.user_id;
      }
    }

    // Credit transactions - read-only for users
    match /credit_transactions/{transactionId} {
      allow read: if isAuthenticated() && getUserId() == resource.data.user_id;
      allow create, update, delete: if false; // Backend only
    }

    // Reports collection
    match /reports/{reportId} {
      allow read: if isAuthenticated() && (getUserId() == resource.data.user_id || isAdmin());
      allow create: if isAuthenticated() && getUserId() == request.resource.data.user_id;
      allow update: if isAdmin();
      allow delete: if isAdmin();
    }

    // Subscriptions collection - read-only
    match /subscriptions/{document=**} {
      allow read: if isAuthenticated();
      allow write: if false; // Backend only
    }

    // Admin config - read for admins, write for backend
    match /admin_config/{document=**} {
      allow read: if isAdmin();
      allow write: if false; // Backend service account only
    }
  }
}
```

---

## 5. Data Retention & Cleanup

### Automatic Cleanup Policies

| Data | Retention | Action |
|------|-----------|--------|
| Temp media files (failed jobs) | 7 days | Delete from GCS |
| Generation artifacts | 1 year | Archive to cold storage |
| Logs | 90 days | Archive, then delete |
| Credit transaction history | 3 years | Keep for accounting |
| User deleted accounts | 30 days | Full deletion |
| Failed job records | 6 months | Aggregate & delete |

---

## 6. Backup & Recovery

### Firestore Backups

- **Frequency:** Daily automated backups
- **Retention:** 30-day rolling window
- **Location:** Multi-region (US + EU)
- **Recovery:** Point-in-time recovery available

### GCS Media Backups

- **Versioning:** Enabled
- **Lifecycle rules:** Move to Coldline after 90 days
- **Replication:** Cross-region redundancy

---

## 7. Scalability Considerations

### Document Size Limits

- Keep documents < 1MB
- Use subcollections for large arrays
- Reference media URLs instead of embedding

### Pagination

```dart
// Firestore query with pagination
Query baseQuery = FirebaseFirestore.instance
    .collection('projects')
    .where('user_id', isEqualTo: userId)
    .orderBy('created_at', descending: true);

// First page
QuerySnapshot first = await baseQuery.limit(20).get();

// Next page (use last document)
if (first.docs.isNotEmpty) {
  QuerySnapshot next = await baseQuery
      .startAfterDocument(first.docs.last)
      .limit(20)
      .get();
}
```

### Real-time Listeners

For generation status updates:

```dart
FirebaseFirestore.instance
    .collection('generations')
    .doc(generationId)
    .snapshots()
    .listen((snapshot) {
  // Update UI with status
});
```

---

## Document Status

**PHASE 0 STATUS: DATABASE SCHEMA DEFINED**

- ✅ Collection structure designed
- ✅ Document schemas specified
- ✅ Firestore indexes planned
- ✅ Security rules written
- ✅ Data retention policies defined
- ✅ Backup strategy documented
- ⏳ Ready for API specification

---

**Next:** API.md - RESTful API endpoint specifications and request/response contracts.
