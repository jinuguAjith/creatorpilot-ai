"""Dependency injection wiring. This is the ONLY place that decides
mock vs real providers — services/orchestrator never know which they got.

Real providers (calling Gemini/Veo/TTS) are added here in Phase 4b once
API keys exist in the environment. Until then, every environment
(including staging) safely falls back to mocks rather than silently
failing or crashing on a missing key.
"""
from app.core.config import get_settings
from app.providers.mock_providers import (
    MockAudioProvider,
    MockImageGenerationProvider,
    MockModerationProvider,
    MockTextGenerationProvider,
    MockTTSProvider,
    MockVideoGenerationProvider,
)
from app.services.orchestrator import Orchestrator


def get_orchestrator() -> Orchestrator:
    settings = get_settings()

    # TODO(Phase 4b): if settings.gemini_api_key: use real GeminiTextProvider, etc.
    # Falling back to mocks whenever a key is absent keeps every environment
    # runnable and keeps automated tests free of real, billable AI calls.
    return Orchestrator(
        text_provider=MockTextGenerationProvider(),
        image_provider=MockImageGenerationProvider(),
        video_provider=MockVideoGenerationProvider(),
        audio_provider=MockAudioProvider(),
        tts_provider=MockTTSProvider(),
        moderation_provider=MockModerationProvider(),
    )
