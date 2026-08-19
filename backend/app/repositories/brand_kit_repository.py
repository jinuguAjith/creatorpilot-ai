"""Repository for `brand_kits/{userId}` — one brand kit per user (V1 scope).
Every future generation reads this to auto-fill business name, colours,
logo, contact details into the campaign request (per spec section 9).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BrandKit:
    user_id: str
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


class BrandKitRepository(ABC):
    @abstractmethod
    async def get(self, user_id: str) -> BrandKit | None: ...

    @abstractmethod
    async def upsert(self, brand_kit: BrandKit) -> BrandKit: ...


class InMemoryBrandKitRepository(BrandKitRepository):
    def __init__(self):
        self._store: dict[str, BrandKit] = {}

    async def get(self, user_id: str) -> BrandKit | None:
        return self._store.get(user_id)

    async def upsert(self, brand_kit: BrandKit) -> BrandKit:
        self._store[brand_kit.user_id] = brand_kit
        return brand_kit


_brand_kit_repo_singleton = InMemoryBrandKitRepository()


def get_brand_kit_repository() -> BrandKitRepository:
    return _brand_kit_repo_singleton
