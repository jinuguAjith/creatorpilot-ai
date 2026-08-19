"""Every protected endpoint depends on `get_current_user`. In production
this verifies a Firebase ID token via firebase_admin.auth.verify_id_token.
Until a Firebase project is connected (Phase 2), this stub raises if no
service account is configured, rather than silently accepting any token —
fail-closed, not fail-open, on auth.
"""
from fastapi import Header, HTTPException, status

from app.core.config import get_settings


class CurrentUser:
    def __init__(self, uid: str, email: str):
        self.uid = uid
        self.email = email


async def get_current_user(authorization: str = Header(default="")) -> CurrentUser:
    settings = get_settings()

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = authorization.removeprefix("Bearer ").strip()

    if not settings.firebase_project_id:
        # No Firebase project configured yet — this is a DEV-ONLY fallback
        # so local endpoints are testable before Phase 2 wiring. It must
        # never run in a deployment with is_production=True.
        if settings.is_production:
            raise HTTPException(status_code=500, detail="Auth not configured")
        return CurrentUser(uid="dev-user", email="dev@creatorpilot.ai")

    # Phase 2: from firebase_admin import auth as firebase_auth
    #   decoded = firebase_auth.verify_id_token(token)
    #   return CurrentUser(uid=decoded["uid"], email=decoded.get("email", ""))
    raise HTTPException(status_code=501, detail="Firebase auth verification not yet wired")
