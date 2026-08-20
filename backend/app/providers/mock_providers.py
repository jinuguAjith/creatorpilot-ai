"""Safe non-billable providers used only for local tests when Gemini is absent."""
import asyncio
import uuid

from app.providers.interfaces import (
    AudioAsset, AudioProvider, CampaignStrategy, ImageGenerationProvider,
    ModerationProvider, PosterAsset, TextGenerationProvider, TTSProvider,
    VideoGenerationProvider, VideoSceneAsset, VoiceoverAsset,
)

class MockTextGenerationProvider(TextGenerationProvider):
    async def generate_strategy(self, description, industry, style, audience):
        await asyncio.sleep(0.01)
        return CampaignStrategy(
            headline=description[:60],
            subheadline=f"Perfect for {audience}",
            cta="Learn more",
            social_caption=description,
            hashtags=[f"#{industry.replace(' ', '')}", "#CreatorPilotAI"],
            visual_direction=f"{style} commercial advertising",
            video_storyboard=["Opening shot", "Product close-up", "Customer experience",
                              "Offer reveal", "Call to action"],
        )

class MockImageGenerationProvider(ImageGenerationProvider):
    async def generate_poster(
        self, strategy, aspect_ratio, brand_colors=None, *,
        resolution="4K", campaign_context="", industry="", location="", offer_details=""
    ):
        await asyncio.sleep(0.01)
        return PosterAsset(
            image_url=f"https://mock-cdn.creatorpilot.ai/posters/{uuid.uuid4()}.png"
        )

class MockVideoGenerationProvider(VideoGenerationProvider):
    async def generate_scene(
        self, scene_description, aspect_ratio, *,
        scene_index=0, resolution="1080p", duration_seconds=8,
        reference_image_path=None, campaign_context=""
    ):
        await asyncio.sleep(0.01)
        return VideoSceneAsset(
            scene_index=scene_index,
            clip_url=f"https://mock-cdn.creatorpilot.ai/scenes/{uuid.uuid4()}.mp4",
        )

class MockAudioProvider(AudioProvider):
    async def select_or_generate_track(self, mood):
        return AudioAsset(audio_url=f"https://mock-cdn.creatorpilot.ai/audio/{mood}.mp3")

class MockTTSProvider(TTSProvider):
    async def synthesize(self, text, language):
        return VoiceoverAsset(
            audio_url=f"https://mock-cdn.creatorpilot.ai/voiceover/{uuid.uuid4()}.mp3",
            language=language,
        )

class MockModerationProvider(ModerationProvider):
    _BLOCKED_TERMS = {"violence", "hate", "explicit"}

    async def check_input(self, text):
        return not any(x in text.lower() for x in self._BLOCKED_TERMS)

    async def check_output(self, asset_url):
        return True
