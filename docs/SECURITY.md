# CreatorPilot AI - Security Implementation Guide

**Version:** 1.0  
**Status:** MVP Security  
**Last Updated:** August 2026

---

## 1. Security Principles

### Core Rules

1. **Never expose AI API keys** in mobile app code
2. **Never expose Firebase service account keys** anywhere
3. **Validate every input** - assume all user input is untrusted
4. **Authenticate all requests** - use Firebase Auth + JWT
5. **Authorize all operations** - verify user owns resource
6. **Encrypt in transit** - HTTPS only, no HTTP
7. **Encrypt at rest** - use Google Cloud encryption
8. **Log securely** - never log secrets or sensitive data
9. **Rate limit** - prevent abuse and brute force
10. **Principle of least privilege** - minimal permissions

---

## 2. API Key Management

### ❌ WRONG: Keys in code

```dart
// DON'T DO THIS!
const GEMINI_API_KEY = "AIzaSy...";  // EXPOSED!
const FIREBASE_DB_URL = "https://...";  // EXPOSED!
```

### ✅ RIGHT: Keys in backend only

**Backend (FastAPI):**
```python
# Use Google Cloud Secret Manager
from google.cloud import secretmanager

def get_api_key(secret_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    project_id = "creatorpilot-prod"
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

GEMINI_API_KEY = get_api_key("gemini-api-key")
```

**Mobile App (Flutter):**
```dart
// DON'T store API keys!
// Make all requests to backend instead

// Instead of calling Gemini directly:
// ❌ final response = await geminiClient.generate("...");

// Do this:
// ✅ final response = await apiClient.post("/api/v1/generations", {...});
```

---

## 3. Authentication Architecture

### Authentication Flow

```
1. User signs in via Flutter app
   ↓
2. Firebase Auth (client SDK) handles OAuth/Email login
   ↓
3. Firebase returns ID Token (signed JWT)
   ↓
4. Mobile app sends ID Token to backend in Authorization header
   ↓
5. Backend verifies ID Token with Firebase Admin SDK
   ↓
6. Backend generates short-lived JWT (15 min)
   ↓
7. Mobile app stores JWT in secure storage (not SharedPreferences)
   ↓
8. Mobile app uses JWT for subsequent API calls
   ↓
9. JWT expires → Mobile app calls /auth/refresh-token
   ↓
10. Backend validates refresh token, issues new JWT
```

### JWT Structure

```python
JWT Payload:
{
  "user_id": "firebase-uid-123",
  "email": "user@example.com",
  "iat": 1692345600,  # Issued at
  "exp": 1692346500,  # Expires in 900 seconds (15 min)
  "aud": "creatorpilot-mobile",
  "iss": "creatorpilot-backend"
}

Signed with RSA-256 (backend's private key)
Verified with backend's public key
```

---

## 4. Authorization & Access Control

### Resource Ownership Checks

```python
from fastapi import Depends, HTTPException

async def verify_project_ownership(project_id: str, user_id: str):
    """
    Verify user owns this project before allowing access
    """
    project = await db.collection("projects").document(project_id).get()
    
    if not project.exists:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.data()["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    return project

@app.get("/api/v1/projects/{project_id}")
async def get_project(
    project_id: str,
    current_user = Depends(get_current_user)
):
    # This will raise 403 if user doesn't own project
    project = await verify_project_ownership(project_id, current_user["user_id"])
    return project
```

### Role-Based Access Control (Admin)

```python
async def verify_admin(user_id: str):
    """
    Check if user has admin role
    """
    user = await db.collection("users").document(user_id).get()
    
    if not user.data().get("role") == "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return user

@app.get("/api/v1/admin/reports")
async def list_reports(
    current_user = Depends(get_current_user),
    admin_user = Depends(verify_admin)
):
    # Only accessible by admins
    reports = await db.collection("reports").get()
    return reports
```

---

## 5. Input Validation

### Pydantic Models (FastAPI)

```python
from pydantic import BaseModel, Field, validator, constr
from typing import Optional

class CampaignInput(BaseModel):
    business_description: constr(min_length=10, max_length=500)
    industry: str = Field(..., regex="^[A-Z_]+$")  # Enum values
    target_audience: constr(min_length=5, max_length=200)
    tone: str = Field(..., regex="^[A-Za-z]+$")
    offer: Optional[constr(max_length=100)]
    location: constr(max_length=100)
    
    @validator('business_description', 'target_audience', 'offer')
    def no_html_tags(cls, v):
        if '<' in v or '>' in v or 'script' in v.lower():
            raise ValueError('HTML tags not allowed')
        return v
    
    @validator('industry')
    def valid_industry(cls, v):
        ALLOWED = ["RESTAURANT", "RETAIL", "SALON", "FITNESS", ...]
        if v not in ALLOWED:
            raise ValueError(f'Invalid industry. Allowed: {ALLOWED}')
        return v

class GenerationRequest(BaseModel):
    project_id: str = Field(..., regex="^proj-[a-z0-9]+$")
    outputs: list = Field(..., min_items=1, max_items=4)
    aspect_ratio: str = Field(..., regex="^[0-9]+:[0-9]+$")
    voiceover_language: Optional[str] = None
    
    @validator('outputs')
    def valid_outputs(cls, v):
        ALLOWED = {"poster", "video", "caption", "voiceover"}
        invalid = set(v) - ALLOWED
        if invalid:
            raise ValueError(f'Invalid outputs: {invalid}')
        return v
```

### File Upload Validation

```python
MAX_FILE_SIZE_MB = 5
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/webp"}

async def upload_logo(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    # Check file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")
    
    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=415, detail="Invalid file type")
    
    # Scan for malicious content
    if await is_malicious(contents):
        raise HTTPException(status_code=400, detail="Malicious content detected")
    
    # Upload to secure GCS bucket
    gcs_path = await gcs_client.upload_secure(
        bucket="creatorpilot-logos",
        user_id=current_user["user_id"],
        file_data=contents
    )
    
    return {"url": gcs_path}
```

---

## 6. Rate Limiting

### Request Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/v1/generations")
@limiter.limit("5/minute")  # 5 requests per minute
async def create_generation(
    request: Request,
    generation_request: GenerationRequest,
    current_user = Depends(get_current_user)
):
    # Per-user rate limiting
    user_id = current_user["user_id"]
    
    # Check daily limit
    today = datetime.utcnow().date()
    count = await db.collection("generations")\
        .where("user_id", "==", user_id)\
        .where("created_at", ">", datetime.combine(today, datetime.min.time()))\
        .count().get()
    
    daily_limit = get_user_daily_limit(current_user)
    if count[0][0].value >= daily_limit:
        raise HTTPException(
            status_code=429,
            detail=f"Daily limit of {daily_limit} generations reached"
        )
    
    # Process request
    ...
```

### Generation Rate Limiting

```python
class GenerationLimiter:
    """
    Enforce per-user generation limits
    """
    
    LIMITS = {
        "FREE": {"daily": 2, "monthly": 5, "concurrent": 1},
        "CREATOR": {"daily": 50, "monthly": 100, "concurrent": 3},
        "BUSINESS": {"daily": 200, "monthly": 500, "concurrent": 5},
        "PRO": {"daily": None, "monthly": None, "concurrent": 10},
    }
    
    async def check_limits(self, user_id: str, subscription_tier: str) -> bool:
        limits = self.LIMITS[subscription_tier]
        
        # Check concurrent generations
        active_count = await db.collection("generations")\
            .where("user_id", "==", user_id)\
            .where("status", "==", "PROCESSING")\
            .count().get()
        
        if active_count[0][0].value >= limits["concurrent"]:
            raise HTTPException(status_code=429, detail="Concurrent generation limit reached")
        
        # Check daily limit
        if limits["daily"]:
            today = datetime.utcnow().date()
            daily_count = await self.count_generations_since(
                user_id,
                datetime.combine(today, datetime.min.time())
            )
            if daily_count >= limits["daily"]:
                raise HTTPException(status_code=429, detail="Daily limit reached")
        
        # Check monthly limit
        if limits["monthly"]:
            month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
            monthly_count = await self.count_generations_since(user_id, month_start)
            if monthly_count >= limits["monthly"]:
                raise HTTPException(status_code=429, detail="Monthly limit reached")
        
        return True
```

---

## 7. Firestore Security Rules

**See DATABASE.md Section 4 for complete security rules.**

Key highlights:
- Users can only read/write their own documents
- Admins can read reports and user data
- All write operations go through backend only (not client)
- Sensitive fields are protected

---

## 8. Data Encryption

### In Transit

```
✅ ALL API communication: HTTPS/TLS 1.2+
✅ Firestore: Encrypted over HTTPS
✅ GCS: Encrypted over HTTPS
✅ No plain HTTP fallback
```

### At Rest

```python
# Google Cloud automatically encrypts data at rest
# But we can enable customer-managed encryption:

from google.cloud import kms_v1

# Encrypt sensitive fields before storing in Firestore
async def encrypt_sensitive_data(user_id: str, data: dict):
    """
    Encrypt PII before storing
    """
    kms_client = kms_v1.KeyManagementServiceClient()
    
    # Fields to encrypt
    sensitive_fields = ["phone", "email", "address"]
    
    encrypted_data = data.copy()
    for field in sensitive_fields:
        if field in encrypted_data:
            ciphertext = kms_client.encrypt(
                key_name=f"projects/creatorpilot-prod/locations/global/keyRings/creatorpilot/cryptoKeys/data-key",
                plaintext=encrypted_data[field].encode()
            )
            encrypted_data[field] = base64.b64encode(ciphertext.ciphertext).decode()
    
    return encrypted_data
```

---

## 9. Logging & Audit

### What to Log

```python
# ✅ DO log:
logger.info({
    "event": "user_login",
    "user_id": user_id,
    "timestamp": datetime.utcnow().isoformat(),
    "ip_address": request.client.host,
    "status": "success"
})

logger.warning({
    "event": "invalid_login_attempt",
    "email": email_provided,
    "attempt_count": 5,
    "ip_address": request.client.host
})

# ❌ DON'T log:
# - API keys or tokens
# - Passwords
# - User campaign content (use summary instead)
# - Card numbers or payment info
```

### Audit Trail

```python
async def log_audit_event(
    event_type: str,
    user_id: str,
    resource_id: Optional[str],
    action: str,
    result: str,
    details: dict
):
    """
    Log all security-relevant events for compliance
    """
    await db.collection("audit_logs").add({
        "event_type": event_type,
        "user_id": user_id,
        "resource_id": resource_id,
        "action": action,
        "result": result,  # success, failure
        "details": details,
        "timestamp": datetime.utcnow(),
        "ip_address": get_client_ip(),
        "user_agent": get_user_agent()
    })
```

---

## 10. Content Moderation

### Input Moderation Pipeline

```python
class ModerationService:
    async def moderate_input(self, text: str) -> ModerationResult:
        """
        Check user input against policies
        """
        
        # 1. Check for banned words
        if self.contains_banned_words(text):
            return ModerationResult(approved=False, reason="Inappropriate language")
        
        # 2. Check toxicity via Google Perspective API
        scores = await self.perspective_api.analyze(text)
        if scores["TOXICITY"] > 0.8:
            return ModerationResult(approved=False, reason="Toxic content")
        
        # 3. Check for spam patterns
        if self.is_spam(text):
            return ModerationResult(approved=False, reason="Spam detected")
        
        # 4. Check for profanity
        if self.contains_profanity(text):
            return ModerationResult(approved=False, reason="Profanity detected")
        
        return ModerationResult(approved=True)
```

### Output Moderation

```python
class SafetyChecker:
    async def check_image(self, gcs_path: str) -> bool:
        """
        Scan generated images for NSFW content
        """
        from google.cloud import vision_v1
        
        client = vision_v1.ImageAnnotatorClient()
        
        image = vision_v1.Image(source=vision_v1.ImageSource(gcs_image_uri=gcs_path))
        response = client.safe_search_detection(image=image)
        safe = response.safe_search_annotation
        
        # Check each unsafe category
        if safe.adult == vision_v1.Likelihood.VERY_LIKELY:
            return False
        if safe.racy == vision_v1.Likelihood.VERY_LIKELY:
            return False
        
        return True
```

---

## 11. Compliance & Privacy

### GDPR Compliance

```python
# User can request their data
async def export_user_data(user_id: str) -> dict:
    """
    GDPR: Right to data portability
    """
    user_data = await db.collection("users").document(user_id).get()
    projects = await db.collection("projects").where("user_id", "==", user_id).stream()
    generations = await db.collection("generations").where("user_id", "==", user_id).stream()
    
    return {
        "user_profile": user_data.to_dict(),
        "projects": [p.to_dict() for p in projects],
        "generations": [g.to_dict() for g in generations],
        "exported_at": datetime.utcnow().isoformat()
    }

# User can request deletion
async def delete_user_account(user_id: str):
    """
    GDPR: Right to be forgotten
    """
    # Mark account as deleted (soft delete for 30 days)
    await db.collection("users").document(user_id).update({
        "account_status": "DELETED",
        "deleted_at": datetime.utcnow(),
        "deletion_requested_at": datetime.utcnow()
    })
    
    # Actually delete after 30 days (via scheduled job)
```

---

## 12. Security Checklist

- [ ] All API keys stored in Cloud Secret Manager
- [ ] Firebase security rules enforced
- [ ] JWT tokens have short expiry (15 min)
- [ ] All inputs validated and sanitized
- [ ] Rate limiting enabled
- [ ] HTTPS enforced
- [ ] Audit logging configured
- [ ] Content moderation pipeline active
- [ ] GDPR/Privacy policy compliance
- [ ] Annual security audit scheduled
- [ ] Dependency vulnerability scanning
- [ ] SAST (Static Analysis) tools configured
- [ ] Admin console password policies enforced
- [ ] Database backups encrypted
- [ ] Incident response plan documented

---

## Document Status

**PHASE 0 STATUS: SECURITY DOCUMENTED**

- ✅ Authentication & authorization designed
- ✅ Input validation specified
- ✅ Rate limiting strategy defined
- ✅ Data encryption requirements set
- ✅ Logging & audit policies established
- ✅ Compliance framework outlined
- ✅ Security checklist created
- ⏳ Ready for billing documentation

---

**Next:** BILLING.md - Subscription management, credit system, and payment processing.
