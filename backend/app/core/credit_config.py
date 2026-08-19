"""Single source of truth for credit costs. Admin dashboard (Phase 12)
reads/writes this same structure (backed by Firestore `config/credits` doc
in production); this in-memory default is used until that's wired.
"""
from pydantic import BaseModel


class CreditConfig(BaseModel):
    poster: int = 5
    video_30_sec: int = 25
    video_60_sec: int = 45
    voiceover: int = 8
    regenerate: int = 5


class PlanConfig(BaseModel):
    name: str
    monthly_price_inr: int
    monthly_credits: int
    watermark: bool = False


DEFAULT_CREDIT_CONFIG = CreditConfig()

DEFAULT_PLANS = [
    PlanConfig(name="free", monthly_price_inr=0, monthly_credits=20, watermark=True),
    PlanConfig(name="creator", monthly_price_inr=299, monthly_credits=150),
    PlanConfig(name="business", monthly_price_inr=999, monthly_credits=600),
    PlanConfig(name="pro", monthly_price_inr=2499, monthly_credits=2000),
]


def get_credit_config() -> CreditConfig:
    # Phase 10: fetch from Firestore config doc with in-memory cache +
    # short TTL so admin changes propagate without a redeploy.
    return DEFAULT_CREDIT_CONFIG
