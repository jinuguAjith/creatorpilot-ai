from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.auth import CurrentUser, get_current_user
from app.repositories.brand_kit_repository import (
    BrandKit,
    BrandKitRepository,
    get_brand_kit_repository,
)

router = APIRouter(prefix="/v1/brand-kit", tags=["brand-kit"])


class BrandKitPayload(BaseModel):
    business_name: str = ""
    logo_url: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None
    accent_color: str | None = None
    font_preference: str | None = None
    website: str | None = None
    phone: str | None = None
    address: str | None = None
    description: str | None = None


@router.get("", response_model=BrandKitPayload | None)
async def get_brand_kit(
    user: CurrentUser = Depends(get_current_user),
    repo: BrandKitRepository = Depends(get_brand_kit_repository),
):
    kit = await repo.get(user.uid)
    if not kit:
        return None
    return BrandKitPayload(**{k: v for k, v in kit.__dict__.items() if k != "user_id"})


@router.put("", response_model=BrandKitPayload)
async def upsert_brand_kit(
    payload: BrandKitPayload,
    user: CurrentUser = Depends(get_current_user),
    repo: BrandKitRepository = Depends(get_brand_kit_repository),
):
    kit = BrandKit(user_id=user.uid, **payload.model_dump())
    saved = await repo.upsert(kit)
    return BrandKitPayload(**{k: v for k, v in saved.__dict__.items() if k != "user_id"})
