# CreatorPilot AI - Billing & Subscription System

**Version:** 1.0  
**Status:** MVP Billing  
**Last Updated:** August 2026

---

## 1. Credit System Overview

### Purpose

Credits abstract the complexity of AI costs from users while maintaining profitability:

```
AI Provider Cost (variable)  →  Credits (fixed conversion)  →  User charges (plan-based)

Example:
Gemini call costs $0.05  →  5 credits  →  User with Creator plan has 5000 credits/month
```

### Credit Allocation by Plan

| Plan | Monthly Credits | Price (INR) | Cost per Credit | Watermark | Aspect Ratios |
|------|-----------------|-------------|-----------------|-----------|---------------|
| **FREE** | 500 | ₹0 | Free | Yes | Limited (1:1, 4:5) |
| **CREATOR** | 5,000 | ₹299 | ₹0.06 | No | All |
| **BUSINESS** | 15,000 | ₹999 | ₹0.07 | No | All |
| **PRO** | Unlimited | ₹2,499 | N/A | No | All |

---

## 2. Credit Costs

### Fixed Costs (Non-negotiable)

```json
{
  "poster_generation": 100,
  "video_30_seconds": 500,
  "video_60_seconds": 800,
  "caption_generation": 25,
  "voiceover_30_seconds": 100,
  "voiceover_per_additional_language": 50,
  "regenerate_discount": 0.5
}
```

### Calculation Examples

**Example 1: Complete Campaign (Poster + Video + Caption)**
```
Poster:        100 credits
Video (30s):   500 credits
Caption:        25 credits
                 ──────────
Total:         625 credits
```

**Example 2: With Voice-Over**
```
Poster:           100 credits
Video (30s):      500 credits
Caption:           25 credits
Voice-over:       100 credits
                   ──────────
Total:           725 credits
```

**Example 3: Regenerate Campaign**
```
Original cost:   625 credits
Regenerate (50%):312 credits  ← Cheaper to encourage iterations
```

---

## 3. Credit Reservation & Refund Logic

### Reservation Flow

```
1. User requests generation
   ↓
2. Backend calculates required credits
   ↓
3. Check available balance
   ├─ If insufficient → Reject request
   ├─ If sufficient → RESERVE credits (lock in DB)
   ↓
4. Enqueue generation job
   ↓
5. Job processing...
   ↓
6. On SUCCESS:
   ├─ FINALIZE reserved credits → USED
   └─ Update Firestore with transaction
   ↓
7. On FAILURE:
   ├─ REFUND partial credits (if partial success)
   ├─ REFUND all credits (if complete failure)
   └─ Log error for audit
```

### Database Operations

**Step 1: Check & Reserve**
```python
async def reserve_credits(user_id: str, required_credits: int) -> bool:
    """
    Atomically check balance and reserve credits
    """
    user_ref = db.collection("users").document(user_id)
    
    @firestore.transactional
    async def check_and_reserve(transaction):
        user_doc = await transaction.get(user_ref)
        available = user_doc.data()["credits"]["available_balance"]
        
        if available < required_credits:
            raise InsufficientCreditsError(f"Need {required_credits}, have {available}")
        
        # Atomically update
        new_balance = available - required_credits
        new_reserved = user_doc.data()["credits"]["reserved"] + required_credits
        
        transaction.update(user_ref, {
            "credits.available_balance": new_balance,
            "credits.reserved": new_reserved,
            "credits.last_updated": datetime.utcnow()
        })
        
        return True
    
    transaction = db.transaction()
    return await check_and_reserve(transaction)
```

**Step 2: Finalize on Success**
```python
async def finalize_credits(user_id: str, generation_id: str, credits_used: int):
    """
    Mark reserved credits as used
    """
    user_ref = db.collection("users").document(user_id)
    
    @firestore.transactional
    async def finalize(transaction):
        user_doc = await transaction.get(user_ref)
        credits = user_doc.data()["credits"]
        
        # Move from reserved to used
        new_reserved = credits["reserved"] - credits_used
        new_used = credits["total_used"] + credits_used
        
        transaction.update(user_ref, {
            "credits.reserved": new_reserved,
            "credits.total_used": new_used,
            "credits.last_updated": datetime.utcnow()
        })
        
        # Create transaction record
        transaction.set(
            db.collection("credit_transactions").document(),
            {
                "user_id": user_id,
                "type": "DEBIT",
                "amount": credits_used,
                "reason": "GENERATION_COMPLETED",
                "generation_id": generation_id,
                "status": "FINALIZED",
                "created_at": datetime.utcnow()
            }
        )
    
    transaction = db.transaction()
    return await finalize(transaction)
```

**Step 3: Refund on Failure**
```python
async def refund_credits(user_id: str, generation_id: str, credits_to_refund: int, reason: str):
    """
    Return reserved credits to available balance
    """
    user_ref = db.collection("users").document(user_id)
    
    @firestore.transactional
    async def refund(transaction):
        user_doc = await transaction.get(user_ref)
        credits = user_doc.data()["credits"]
        
        # Move from reserved back to available
        new_available = credits["available_balance"] + credits_to_refund
        new_reserved = credits["reserved"] - credits_to_refund
        
        transaction.update(user_ref, {
            "credits.available_balance": new_available,
            "credits.reserved": new_reserved,
            "credits.last_updated": datetime.utcnow()
        })
        
        # Create refund record
        transaction.set(
            db.collection("credit_transactions").document(),
            {
                "user_id": user_id,
                "type": "CREDIT",
                "amount": credits_to_refund,
                "reason": f"REFUND__{reason}",
                "generation_id": generation_id,
                "status": "REFUNDED",
                "created_at": datetime.utcnow()
            }
        )
    
    transaction = db.transaction()
    return await refund(transaction)
```

---

## 4. Google Play Billing Integration

### Verification Flow

```
1. User purchases subscription in Google Play Store (mobile)
   ↓
2. Google returns purchase token to mobile app
   ↓
3. Mobile app sends token to backend: POST /api/v1/subscriptions/verify-purchase
   ↓
4. Backend verifies token with Google Play API
   ↓
5. Backend grants credits/subscription entitlements to user
   ↓
6. Mobile app confirmed (no need to store tokens locally)
```

### Backend Verification

```python
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
import googleapiclient.discovery

class GooglePlayBillingService:
    def __init__(self):
        self.credentials = Credentials.from_service_account_file(
            "service_account_key.json",
            scopes=["https://www.googleapis.com/auth/androidpublisher"]
        )
        self.androidpublisher = googleapiclient.discovery.build(
            "androidpublisher", "v3", credentials=self.credentials
        )
    
    async def verify_subscription_purchase(
        self,
        package_name: str,
        subscription_id: str,
        purchase_token: str
    ) -> SubscriptionPurchase:
        """
        Verify purchase with Google Play API
        """
        request = self.androidpublisher.purchases().subscriptions().get(
            packageName=package_name,
            subscriptionId=subscription_id,
            token=purchase_token
        )
        
        result = request.execute()
        
        # Validate purchase state
        if result["purchaseState"] != "Purchased":  # Not "Pending" or "Canceled"
            raise InvalidPurchaseError(f"Invalid purchase state: {result['purchaseState']}")
        
        # Check if subscription is active
        if result["autoRenewing"] == False and result["expiryTimeMillis"] < time.time() * 1000:
            raise ExpiredSubscriptionError("Subscription has expired")
        
        return SubscriptionPurchase(
            user_id=current_user["user_id"],
            subscription_id=subscription_id,
            status="ACTIVE",
            purchase_time=result["startTimeMillis"],
            expiry_time=result["expiryTimeMillis"],
            auto_renew=result["autoRenewing"]
        )

@app.post("/api/v1/subscriptions/verify-purchase")
async def verify_purchase(
    request_body: VerifyPurchaseRequest,
    current_user = Depends(get_current_user)
):
    """
    Verify Google Play purchase and grant entitlements
    """
    try:
        # Verify with Google
        purchase = await billing_service.verify_subscription_purchase(
            package_name=request_body.package_name,
            subscription_id=request_body.product_id,
            purchase_token=request_body.purchase_token
        )
        
        # Get plan details
        plan = await db.collection("subscriptions/plans")\
            .document(get_plan_by_product_id(request_body.product_id)).get()
        
        # Grant subscription
        await grant_subscription(
            user_id=current_user["user_id"],
            plan_id=plan.id,
            purchase=purchase
        )
        
        return {
            "success": True,
            "subscription_id": plan.id,
            "credits_granted": plan.data()["features"]["monthly_credits"]
        }
    
    except InvalidPurchaseError as e:
        logger.warning(f"Invalid purchase: {e}")
        raise HTTPException(status_code=400, detail="Invalid purchase token")
    
    except ExpiredSubscriptionError:
        raise HTTPException(status_code=400, detail="Subscription has expired")
```

---

## 5. Subscription Management

### Granting Subscription

```python
async def grant_subscription(
    user_id: str,
    plan_id: str,
    purchase: SubscriptionPurchase
):
    """
    Update user subscription status and credits
    """
    user_ref = db.collection("users").document(user_id)
    plan_ref = db.collection("subscriptions/plans").document(plan_id)
    
    plan = await plan_ref.get()
    plan_data = plan.data()
    
    renewal_date = datetime.fromtimestamp(purchase.expiry_time / 1000)
    monthly_credits = plan_data["features"]["monthly_credits"]
    
    # Update user subscription
    await user_ref.update({
        "subscription": {
            "plan_id": plan_id,
            "plan_name": plan_data["name"],
            "status": "ACTIVE",
            "start_date": datetime.utcnow(),
            "renewal_date": renewal_date,
            "purchase_token": purchase.purchase_token,
            "platform": "android"
        },
        "credits.total_purchased": firebase.firestore.Increment(monthly_credits),
        "credits.available_balance": firebase.firestore.Increment(monthly_credits),
        "credits.monthly_limit": monthly_credits,
        "credits.monthly_used": 0,
        "credits.reset_date": renewal_date
    })
    
    # Log transaction
    await db.collection("credit_transactions").add({
        "user_id": user_id,
        "type": "CREDIT",
        "amount": monthly_credits,
        "reason": f"SUBSCRIPTION__{plan_data['name']}",
        "status": "COMPLETED",
        "created_at": datetime.utcnow()
    })
```

### Canceling Subscription

```python
async def cancel_subscription(user_id: str):
    """
    Cancel user subscription (but allow credits to be used)
    """
    user_ref = db.collection("users").document(user_id)
    
    # Get current subscription
    user = await user_ref.get()
    subscription = user.data()["subscription"]
    
    # Update subscription status
    await user_ref.update({
        "subscription.status": "CANCELED",
        "subscription.cancellation_date": datetime.utcnow(),
        "subscription.auto_renew": False
    })
    
    # Log cancellation
    logger.info({
        "event": "subscription_canceled",
        "user_id": user_id,
        "plan_id": subscription["plan_id"],
        "timestamp": datetime.utcnow().isoformat()
    })
```

### Handling Subscription Renewal

```python
class SubscriptionRenewalScheduler:
    """
    Background job to handle subscription renewals
    Runs daily to check for expiring subscriptions
    """
    
    async def check_renewals(self):
        # Find subscriptions expiring in next 7 days
        tomorrow = datetime.utcnow() + timedelta(days=1)
        week_later = tomorrow + timedelta(days=6)
        
        subscriptions = await db.collection("users")\
            .where("subscription.renewal_date", ">", tomorrow)\
            .where("subscription.renewal_date", "<", week_later)\
            .where("subscription.auto_renew", "==", True)\
            .stream()
        
        for sub in subscriptions:
            user_id = sub.id
            plan_id = sub.data()["subscription"]["plan_id"]
            
            # Grant new credits
            plan = await db.collection("subscriptions/plans").document(plan_id).get()
            monthly_credits = plan.data()["features"]["monthly_credits"]
            
            await db.collection("users").document(user_id).update({
                "credits.monthly_used": 0,
                "credits.reset_date": datetime.utcnow() + timedelta(days=30),
                "credits.available_balance": firebase.firestore.Increment(monthly_credits)
            })
```

---

## 6. Apple StoreKit Integration (Future)

### Design for Future Support

```python
from abc import ABC, abstractmethod

class BillingProvider(ABC):
    """
    Abstract payment provider interface
    """
    
    @abstractmethod
    async def verify_purchase(self, purchase_token: str, product_id: str):
        pass
    
    @abstractmethod
    async def cancel_subscription(self, subscription_id: str):
        pass

class GooglePlayBillingProvider(BillingProvider):
    async def verify_purchase(self, purchase_token: str, product_id: str):
        # Google Play implementation
        ...

class AppleStoreKitProvider(BillingProvider):
    """
    Future: Apple StoreKit 2 implementation
    Same interface, different backend
    """
    async def verify_purchase(self, purchase_token: str, product_id: str):
        # Apple StoreKit implementation
        ...

# Factory pattern for provider selection
class BillingProviderFactory:
    @staticmethod
    def get_provider(platform: str) -> BillingProvider:
        if platform == "android":
            return GooglePlayBillingProvider()
        elif platform == "ios":
            return AppleStoreKitProvider()
        else:
            raise ValueError(f"Unknown platform: {platform}")
```

---

## 7. Payment Processing

### Payment Flow (Android - Google Play)

```
User selects subscription
    ↓
Google Play handles payment securely
    ├─ User enters payment method (stored securely by Google)
    ├─ Google authenticates payment
    └─ Google handles recurring charges
    ↓
Google returns purchase token
    ↓
Mobile app verifies with backend
    ↓
Backend verifies with Google Play API
    ↓
Backend grants credits & updates subscription
    ↓
User can now generate content
```

### Webhook Handling (Real-time Updates)

```python
@app.post("/api/v1/webhooks/google-play")
async def handle_google_play_webhook(request: Request):
    """
    Handle real-time subscription events from Google Play
    (cancellation, renewal, account hold, etc.)
    """
    body = await request.json()
    
    # Verify webhook signature
    if not verify_webhook_signature(body, request.headers):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse event
    event_type = body["eventType"]
    subscription_notification = json.loads(body["subscriptionNotification"])
    
    if event_type == "13":  # SUBSCRIPTION_REVOKED
        await revoke_subscription(subscription_notification)
    
    elif event_type == "12":  # SUBSCRIPTION_EXPIRED
        await handle_subscription_expiry(subscription_notification)
    
    elif event_type == "4":  # SUBSCRIPTION_RENEWED
        await handle_subscription_renewal(subscription_notification)
    
    return {"status": "received"}
```

---

## 8. Financial Reporting

### Revenue Tracking

```python
async def get_revenue_report(start_date: date, end_date: date) -> RevenueReport:
    """
    Generate revenue report for accounting
    """
    transactions = await db.collection("credit_transactions")\
        .where("type", "==", "DEBIT")\
        .where("created_at", ">", start_date)\
        .where("created_at", "<", end_date)\
        .stream()
    
    total_credits_sold = 0
    total_revenue_inr = 0
    
    for txn in transactions:
        if txn.data()["reason"].startswith("SUBSCRIPTION__"):
            total_revenue_inr += txn.data()["amount"]  # Already in INR
    
    return RevenueReport(
        period_start=start_date,
        period_end=end_date,
        total_revenue_inr=total_revenue_inr,
        total_transactions=len(transactions),
        active_subscriptions=await count_active_subscriptions(end_date)
    )
```

---

## Document Status

**PHASE 0 STATUS: BILLING SYSTEM DESIGNED**

- ✅ Credit system architecture defined
- ✅ Reservation & refund logic specified
- ✅ Google Play Billing integration designed
- ✅ Subscription management workflow documented
- ✅ Apple StoreKit future-proofing included
- ✅ Financial reporting framework outlined
- ⏳ Ready for Google Play release checklist

---

**Next:** PLAY_STORE.md - Google Play release requirements and checklist.
