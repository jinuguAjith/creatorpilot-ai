from enum import Enum
from pydantic import BaseModel


class OutputType(str, Enum):
    poster = "poster"
    video = "video"
    caption = "caption"
    voiceover = "voiceover"


class GenerationStatus(str, Enum):
    requested = "REQUESTED"
    queued = "QUEUED"
    processing = "PROCESSING"
    generating = "GENERATING"
    composing = "COMPOSING"
    completed = "COMPLETED"
    failed = "FAILED"


class CampaignRequest(BaseModel):
    description: str
    industry: str
    language: str = "English"
    style: str
    target_audience: str
    offer_details: str = ""
    location: str = ""
    aspect_ratio: str = "9:16"
    outputs: list[OutputType]
    voiceover_language: str | None = None


class CampaignJobResponse(BaseModel):
    job_id: str
    status: GenerationStatus
    credits_reserved: int


class GenerationResultResponse(BaseModel):
    job_id: str
    status: GenerationStatus
    poster_url: str | None = None
    video_url: str | None = None
    caption: str | None = None
    hashtags: list[str] | None = None
    cta: str | None = None
    error_message: str | None = None


class ReportRequest(BaseModel):
    job_id: str
    reason: str
