"""Role-based access control. Real implementation (Phase 2) reads a custom
claim (`role: admin`) set on the Firebase user via firebase_admin.auth
.set_custom_user_claims — never trusts a client-supplied role field.

Until Firebase is wired, this dev-only allowlist grants admin to a fixed
set of UIDs so the admin API is buildable/testable now.
"""
from fastapi import Depends, HTTPException, status

from app.core.auth import CurrentUser, get_current_user
from app.core.config import get_settings

# Phase 2: replace with Firebase custom claims check. Never accept a role
# field from the request body/headers — that would let any client grant
# itself admin.
_DEV_ADMIN_UIDS = {"dev-user"}


async def require_admin(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    settings = get_settings()
    if settings.is_production:
        # Production must have real claims-based checks wired before this
        # dependency is safe to use — fail closed rather than falling back
        # to the dev allowlist.
        raise HTTPException(status_code=501, detail="Admin RBAC not yet wired for production")

    if user.uid not in _DEV_ADMIN_UIDS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user
