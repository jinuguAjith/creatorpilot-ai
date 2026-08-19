"""Mock implementations of every provider interface. Used for:
  - local development without any AI API keys
  - automated tests (unit/integration) — never make real, billable AI calls
  - CI pipelines

Swap for real providers via the DI wiring in app/core/dependencies.py once
GEMINI_API_KEY / VIDEO_GEN_API_KEY / TTS_API_KEY are present in the
environment for a given deployment (staging/production).
"""
import asyncio
import uuid

from app.providers.interfaces import (
    AudioAsset,
    AudioProvider,
    CampaignStrategy,
    ImageGenerationProvider,
    ModerationProvider,
    PosterAsset,
    TextGenerationProvider,
    TTSProvider,
    VideoGenerationProvider,
    VideoSceneAsset,
    VoiceoverAsset,
)


class MockTextGenerationProvider(TextGenerationProvider):
    async def generate_strategy(self, description, industry, style, audience) -> CampaignStrategy:
        await asyncio.sleep(0.05)
        return CampaignStrategy(
            headline=f"{description[:40]}...",
            subheadline=f"Perfect for {audience}",
            cta="Book now",
            social_caption=f"Something special is happening. {description[:60]}",
            hashtags=["#GrandOpening", f"#{industry.replace(' ', '')}"],
            visual_direction=f"{style} visual style, warm inviting tones",
            video_storyboard=[
                "Establishing shot",
                "Product / experience close-up",
                "People enjoying the experience",
                "Offer callout",
                "Call to action",
            ],
        )


class MockImageGenerationProvider(ImageGenerationProvider):
    async def generate_poster(self, strategy, aspect_ratio, brand_colors) -> PosterAsset:
        await asyncio.sleep(0.05)
        return PosterAsset(image_url=f"https://mock-cdn.creatorpilot.ai/posters/{uuid.uuid4()}.png")


class MockVideoGenerationProvider(VideoGenerationProvider):
    async def generate_scene(self, scene_description, aspect_ratio) -> VideoSceneAsset:
        await asyncio.sleep(0.05)
        return VideoSceneAsset(scene_index=0, clip_url=f"https://mock-cdn.creatorpilot.ai/scenes/{uuid.uuid4()}.mp4")


class MockAudioProvider(AudioProvider):
    async def select_or_generate_track(self, mood) -> AudioAsset:
        await asyncio.sleep(0.02)
        return AudioAsset(audio_url=f"https://mock-cdn.creatorpilot.ai/audio/{mood}.mp3")


class MockTTSProvider(TTSProvider):
    async def synthesize(self, text, language) -> VoiceoverAsset:
        await asyncio.sleep(0.02)
        return VoiceoverAsset(audio_url=f"https://mock-cdn.creatorpilot.ai/voiceover/{uuid.uuid4()}.mp3", language=language)


class MockModerationProvider(ModerationProvider):
    _BLOCKED_TERMS = {"violence", "hate", "explicit"}

    async def check_input(self, text: str) -> bool:
        lowered = text.lower()
        return not any(term in lowered for term in self._BLOCKED_TERMS)

    async def check_output(self, asset_url: str) -> bool:
        return True
