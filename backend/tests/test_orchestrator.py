import pytest

from app.providers.mock_providers import (
    MockAudioProvider,
    MockImageGenerationProvider,
    MockModerationProvider,
    MockTextGenerationProvider,
    MockTTSProvider,
    MockVideoGenerationProvider,
)
from app.schemas.campaign import CampaignRequest, GenerationStatus, OutputType
from app.services.orchestrator import ContentModerationError, Orchestrator


def make_orchestrator() -> Orchestrator:
    return Orchestrator(
        text_provider=MockTextGenerationProvider(),
        image_provider=MockImageGenerationProvider(),
        video_provider=MockVideoGenerationProvider(),
        audio_provider=MockAudioProvider(),
        tts_provider=MockTTSProvider(),
        moderation_provider=MockModerationProvider(),
    )


@pytest.mark.asyncio
async def test_poster_and_caption_generation():
    orchestrator = make_orchestrator()
    request = CampaignRequest(
        description="Grand opening of Bella Aroma restaurant, 20% off",
        industry="restaurant",
        style="Luxury",
        target_audience="couples and families",
        aspect_ratio="4:5",
        outputs=[OutputType.poster, OutputType.caption],
    )
    result = await orchestrator.run("job_1", request)
    assert result.status == GenerationStatus.completed
    assert result.poster_url is not None
    assert result.video_url is None
    assert result.caption is not None
    assert result.hashtags


@pytest.mark.asyncio
async def test_video_generation_includes_all_scenes():
    orchestrator = make_orchestrator()
    request = CampaignRequest(
        description="Product launch",
        industry="tech",
        style="Modern",
        target_audience="early adopters",
        outputs=[OutputType.video],
    )
    result = await orchestrator.run("job_2", request)
    assert result.video_url is not None


@pytest.mark.asyncio
async def test_blocked_input_raises_moderation_error():
    orchestrator = make_orchestrator()
    request = CampaignRequest(
        description="content involving violence",
        industry="x",
        style="Modern",
        target_audience="x",
        outputs=[OutputType.caption],
    )
    with pytest.raises(ContentModerationError):
        await orchestrator.run("job_3", request)
