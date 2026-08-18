# CreatorPilot AI - API Specification

**Version:** 1.0  
**Status:** MVP Endpoints  
**Last Updated:** August 2026

---

## 1. API Overview

### Base URL

- **Development:** `http://localhost:8000/api/v1`
- **Staging:** `https://staging-api.creatorpilot.ai/api/v1`
- **Production:** `https://api.creatorpilot.ai/api/v1`

### Authentication

All requests require Firebase ID Token in Authorization header:

```
Authorization: Bearer <firebase-id-token>
```

Backend validates token with Firebase Admin SDK and returns JWT for subsequent requests.

### Response Format

```json
{
  "success": true,
  "data": { /* response payload */ },
  "error": null,
  "timestamp": "2026-08-18T10:00:00Z",
  "request_id": "req-abc123"
}
```

### Error Response

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INSUFFICIENT_CREDITS",
    "message": "You don't have enough credits for this operation",
    "details": {
      "required": 625,
      "available": 500
    }
  },
  "timestamp": "2026-08-18T10:00:00Z",
  "request_id": "req-abc123"
}
```

---

## 2. Authentication Endpoints

### 2.1 POST /auth/login

**Email/Password Login**

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user_id": "firebase-uid-123",
    "email": "user@example.com",
    "display_name": "John Doe",
    "jwt_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "expires_in_seconds": 900,
    "subscription": {
      "plan_id": "plan-creator-monthly",
      "status": "ACTIVE"
    }
  }
}
```

---

### 2.2 POST /auth/login-google

**Google OAuth Login**

**Request:**
```json
{
  "id_token": "google-oauth-id-token"
}
```

**Response (200):**
Same as POST /auth/login

---

### 2.3 POST /auth/refresh-token

**Refresh JWT Token**

**Request:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "jwt_token": "eyJhbGc...",
    "expires_in_seconds": 900
  }
}
```

---

## 3. Projects Endpoints

### 3.1 GET /projects

**List User Projects**

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)
- `sort_by`: Field to sort (default: created_at)
- `order`: ASC or DESC (default: DESC)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "projects": [
      {
        "project_id": "proj-001",
        "title": "Bella Aroma Campaign",
        "industry": "RESTAURANT",
        "status": "COMPLETED",
        "created_at": "2026-08-15T14:30:00Z",
        "thumbnail_url": "https://...",
        "latest_generation_id": "gen-1002"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 5,
      "total_items": 98
    }
  }
}
```

---

### 3.2 GET /projects/{project_id}

**Get Project Details**

**Response (200):**
```json
{
  "success": true,
  "data": {
    "project_id": "proj-001",
    "title": "Bella Aroma Campaign",
    "description": "Grand opening promotional campaign",
    "industry": "RESTAURANT",
    "campaign_input": {
      "business_description": "...",
      "target_audience": "...",
      "offer": "20% discount"
    },
    "status": "COMPLETED",
    "generations": [
      {
        "generation_id": "gen-1002",
        "status": "COMPLETED",
        "created_at": "2026-08-15T14:30:00Z",
        "results": {
          "poster_url": "https://...",
          "video_url": "https://...",
          "caption": "...",
          "hashtags": ["#BellaAroma", "..."]
        }
      }
    ],
    "created_at": "2026-08-15T14:30:00Z",
    "updated_at": "2026-08-15T14:45:00Z"
  }
}
```

---

### 3.3 POST /projects

**Create New Project**

**Request:**
```json
{
  "title": "Bella Aroma Campaign",
  "industry": "RESTAURANT",
  "campaign_input": {
    "business_description": "Luxury Italian restaurant, grand opening...",
    "target_audience": "Couples and families",
    "tone": "Elegant",
    "offer": "20% discount",
    "location": "Bangalore, India"
  },
  "brand_kit_id": "bk-001"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "project_id": "proj-001",
    "title": "Bella Aroma Campaign",
    "status": "DRAFT",
    "created_at": "2026-08-18T10:00:00Z"
  }
}
```

---

### 3.4 DELETE /projects/{project_id}

**Delete Project**

**Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Project deleted successfully"
  }
}
```

---

## 4. Generations Endpoints

### 4.1 POST /generations

**Create Generation Job**

**Request:**
```json
{
  "project_id": "proj-001",
  "outputs": ["poster", "video", "caption"],
  "aspect_ratio": "9:16",
  "voiceover_language": null
}
```

**Response (202):**
```json
{
  "success": true,
  "data": {
    "generation_id": "gen-1002",
    "status": "QUEUED",
    "estimated_credits": 625,
    "estimated_duration_seconds": 60,
    "created_at": "2026-08-18T10:00:00Z"
  }
}
```

**Error (400):**
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_CREDITS",
    "message": "You need 625 credits but only have 500 available"
  }
}
```

---

### 4.2 GET /generations/{generation_id}/status

**Get Generation Status**

**Response (200):**
```json
{
  "success": true,
  "data": {
    "generation_id": "gen-1002",
    "status": "COMPOSING",
    "progress": 85,
    "current_step": "media_composition",
    "step_status": {
      "input_moderation": "COMPLETED",
      "campaign_strategy": "COMPLETED",
      "poster_generation": "COMPLETED",
      "video_generation": "COMPLETED",
      "media_composition": "IN_PROGRESS"
    },
    "elapsed_time_seconds": 45,
    "estimated_time_remaining_seconds": 15,
    "error": null
  }
}
```

---

### 4.3 GET /generations/{generation_id}

**Get Generation Results**

**Response (200):**
```json
{
  "success": true,
  "data": {
    "generation_id": "gen-1002",
    "status": "COMPLETED",
    "results": {
      "poster": {
        "url": "https://signed-url-expires-1h.../poster.png",
        "dimensions": "1080x1920",
        "size_mb": 2.3
      },
      "video": {
        "url": "https://signed-url-expires-1h.../video.mp4",
        "dimensions": "1080x1920",
        "duration_seconds": 30,
        "fps": 30,
        "size_mb": 125
      },
      "caption": {
        "text": "Experience authentic Italian cuisine at Bella Aroma. Grand opening this Sunday with 20% special offer!",
        "hashtags": ["#BellaAroma", "#ItalianCuisine", "#Bangalore", "#GrandOpening"],
        "cta": "Reserve your table now at Bella Aroma!"
      },
      "voiceover": null
    },
    "credits_used": 625,
    "created_at": "2026-08-15T14:30:00Z",
    "completed_at": "2026-08-15T14:44:00Z"
  }
}
```

---

## 5. Brand Kit Endpoints

### 5.1 GET /brand-kit

**Get User's Brand Kit**

**Response (200):**
```json
{
  "success": true,
  "data": {
    "brand_kit_id": "bk-001",
    "business_name": "Bella Aroma Restaurant",
    "logo_url": "https://...",
    "colors": {
      "primary": "#8B4513",
      "secondary": "#D4A574",
      "accent": "#FFD700"
    },
    "contact_info": {
      "phone": "+91-98765-43210",
      "email": "hello@bellaaroma.com",
      "address": "123 MG Road, Bangalore",
      "website": "https://bellaaroma.com"
    },
    "created_at": "2026-07-15T00:00:00Z"
  }
}
```

---

### 5.2 PUT /brand-kit

**Update Brand Kit**

**Request:**
```json
{
  "business_name": "Bella Aroma Restaurant",
  "colors": {
    "primary": "#8B4513",
    "secondary": "#D4A574",
    "accent": "#FFD700"
  },
  "contact_info": {
    "phone": "+91-98765-43210",
    "email": "hello@bellaaroma.com",
    "address": "123 MG Road, Bangalore"
  }
}
```

**Response (200):**
Same as GET /brand-kit

---

### 5.3 POST /brand-kit/upload-logo

**Upload Logo**

**Request:** Multipart form data
```
Content-Type: multipart/form-data
- file: <binary-image-data>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "logo_url": "https://...",
    "size_bytes": 256000
  }
}
```

---

## 6. Subscriptions Endpoints

### 6.1 GET /subscriptions/current

**Get Current Subscription**

**Response (200):**
```json
{
  "success": true,
  "data": {
    "plan_id": "plan-creator-monthly",
    "plan_name": "CREATOR",
    "status": "ACTIVE",
    "renewal_date": "2026-09-01T00:00:00Z",
    "price": {
      "amount": 299,
      "currency": "INR"
    },
    "entitlements": [
      "no_watermark",
      "all_aspect_ratios",
      "monthly_credits_5000"
    ]
  }
}
```

---

### 6.2 GET /subscriptions/plans

**List Available Plans**

**Response (200):**
```json
{
  "success": true,
  "data": {
    "plans": [
      {
        "plan_id": "plan-free",
        "name": "FREE",
        "price": { "amount": 0, "currency": "INR" },
        "monthly_credits": 500,
        "features": ["limited_aspect_ratios", "watermark"]
      },
      {
        "plan_id": "plan-creator-monthly",
        "name": "CREATOR",
        "price": { "amount": 299, "currency": "INR" },
        "monthly_credits": 5000,
        "features": ["no_watermark", "all_aspect_ratios"]
      }
    ]
  }
}
```

---

### 6.3 POST /subscriptions/verify-purchase

**Verify Google Play Purchase**

**Request:**
```json
{
  "purchase_token": "google-play-purchase-token",
  "product_id": "com.creatorpilot.creator.monthly",
  "package_name": "com.creatorpilot.app"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "subscription_id": "sub-123",
    "status": "ACTIVE",
    "plan_id": "plan-creator-monthly",
    "credits_granted": 5000,
    "renewal_date": "2026-09-01T00:00:00Z"
  }
}
```

---

## 7. Billing Endpoints

### 7.1 GET /billing/credits

**Get Credit Balance**

**Response (200):**
```json
{
  "success": true,
  "data": {
    "total_balance": 4675,
    "reserved": 100,
    "available": 4575,
    "monthly_limit": 5000,
    "monthly_used": 325,
    "reset_date": "2026-09-01T00:00:00Z"
  }
}
```

---

### 7.2 GET /billing/transactions

**List Credit Transactions**

**Query Parameters:**
- `limit`: Number of items (default: 50)
- `offset`: Pagination offset

**Response (200):**
```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "transaction_id": "txn-456",
        "type": "DEBIT",
        "amount": 625,
        "reason": "GENERATION_COMPLETED",
        "previous_balance": 5300,
        "new_balance": 4675,
        "created_at": "2026-08-15T14:44:00Z"
      }
    ]
  }
}
```

---

### 7.3 POST /billing/check-credit-availability

**Check If Credits Available**

**Request:**
```json
{
  "required_credits": 625,
  "outputs": ["poster", "video", "caption"]
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "available": true,
    "current_balance": 4675,
    "required": 625,
    "shortfall": 0
  }
}
```

---

## 8. Reports Endpoints

### 8.1 POST /reports

**Submit AI Output Report**

**Request:**
```json
{
  "generation_id": "gen-1002",
  "type": "INAPPROPRIATE_CONTENT",
  "description": "Generated video contains sensitive material"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "report_id": "rpt-001",
    "status": "PENDING",
    "created_at": "2026-08-15T15:00:00Z"
  }
}
```

---

## 9. Admin Endpoints (Protected)

### 9.1 GET /admin/users

**List Users (Admin Only)**

**Query Parameters:**
- `page`: Page number
- `search`: Email search

**Response (200):**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "user_id": "firebase-uid-123",
        "email": "user@example.com",
        "subscription_status": "ACTIVE",
        "credits_balance": 4675,
        "created_at": "2026-08-01T00:00:00Z",
        "last_login": "2026-08-18T10:00:00Z"
      }
    ]
  }
}
```

---

### 9.2 GET /admin/reports

**List AI Output Reports (Admin Only)**

**Response (200):**
```json
{
  "success": true,
  "data": {
    "reports": [
      {
        "report_id": "rpt-001",
        "user_id": "firebase-uid-123",
        "generation_id": "gen-1002",
        "type": "INAPPROPRIATE_CONTENT",
        "status": "PENDING",
        "created_at": "2026-08-15T15:00:00Z"
      }
    ]
  }
}
```

---

## Document Status

**PHASE 0 STATUS: API SPECIFICATION COMPLETE**

- ✅ Authentication endpoints documented
- ✅ Projects API designed
- ✅ Generations API documented
- ✅ Subscriptions API specified
- ✅ Billing API outlined
- ✅ Admin endpoints included
- ⏳ Ready for AI workflow documentation

---

**Next:** AI_WORKFLOW.md - Detailed AI generation pipeline and orchestration logic.
