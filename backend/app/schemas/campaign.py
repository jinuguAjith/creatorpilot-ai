from enum import Enum
from pydantic import BaseModel, Field, field_validator


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
    description: str = Field(..., min_length=1, max_length=2000)
    industry: str = Field(..., max_length=100)
    language: str = Field(default="English", max_length=50)
    style: str = Field(..., max_length=50)
    target_audience: str = Field(..., max_length=300)
    offer_details: str = Field(default="", max_length=500)
    location: str = Field(default="", max_length=200)
    aspect_ratio: str = Field(default="9:16", max_length=10)
    outputs: list[OutputType] = Field(..., min_length=1, max_length=4)
    voiceover_language: str | None = Field(default=None, max_length=50)

    @field_validator("outputs")
    @classmethod
    def outputs_must_be_unique(cls, v: list[OutputType]) -> list[OutputType]:
        if len(set(v)) != len(v):
            raise ValueError("outputs must not contain duplicates")
        return v


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
    job_id: str = Field(..., max_length=100)
    reason: str = Field(..., min_length=1, max_length=1000)
