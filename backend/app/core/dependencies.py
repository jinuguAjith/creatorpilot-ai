from app.core.config import get_settings
from app.providers.gemini_image_provider import GeminiImageGenerationProvider
from app.providers.gemini_text_provider import GeminiTextGenerationProvider
from app.providers.gemini_video_provider import GeminiVideoGenerationProvider
from app.providers.mock_providers import (
    MockAudioProvider, MockImageGenerationProvider, MockModerationProvider,
    MockTextGenerationProvider, MockTTSProvider, MockVideoGenerationProvider,
)
from app.services.orchestrator import Orchestrator

def get_orchestrator():
    s = get_settings()

    if s.gemini_api_key:
        return Orchestrator(
            text_provider=GeminiTextGenerationProvider(),
            image_provider=GeminiImageGenerationProvider(),
            video_provider=GeminiVideoGenerationProvider(),
            audio_provider=MockAudioProvider(),
            tts_provider=MockTTSProvider(),
            moderation_provider=MockModerationProvider(),
        )

    if s.is_production or not s.allow_mock_providers:
        raise RuntimeError("GEMINI_API_KEY is required; mock generation is disabled")

    return Orchestrator(
        text_provider=MockTextGenerationProvider(),
        image_provider=MockImageGenerationProvider(),
        video_provider=MockVideoGenerationProvider(),
        audio_provider=MockAudioProvider(),
        tts_provider=MockTTSProvider(),
        moderation_provider=MockModerationProvider(),
    )
