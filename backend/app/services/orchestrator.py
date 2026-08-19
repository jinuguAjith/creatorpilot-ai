"""Implements the STEP 1-12 orchestration flow from docs/AI_WORKFLOW.md:
understand input -> strategy -> poster -> video storyboard -> scenes ->
audio -> voiceover -> compose (FFmpeg, Phase 7) -> store -> return URLs.

Depends only on provider *interfaces* — real vs mock providers are
injected by the caller, so this class is identical in tests and prod.
"""
from dataclasses import dataclass

from app.providers.interfaces import (
    AudioProvider,
    ImageGenerationProvider,
    ModerationProvider,
    TextGenerationProvider,
    TTSProvider,
    VideoGenerationProvider,
)
from app.schemas.campaign import CampaignRequest, GenerationResultResponse, GenerationStatus
from app.core.logging import get_logger

logger = get_logger(__name__)


class ContentModerationError(Exception):
    pass


@dataclass
class Orchestrator:
    text_provider: TextGenerationProvider
    image_provider: ImageGenerationProvider
    video_provider: VideoGenerationProvider
    audio_provider: AudioProvider
    tts_provider: TTSProvider
    moderation_provider: ModerationProvider

    async def run(self, job_id: str, request: CampaignRequest) -> GenerationResultResponse:
        logger.info("generation_started", job_id=job_id)

        # STEP 1 — input moderation gate
        if not await self.moderation_provider.check_input(request.description):
            logger.warning("generation_blocked_moderation", job_id=job_id)
            raise ContentModerationError("Input failed content moderation")

        # STEP 2-3 — campaign strategy (headline, caption, hashtags, storyboard)
        strategy = await self.text_provider.generate_strategy(
            description=request.description,
            industry=request.industry,
            style=request.style,
            audience=request.target_audience,
        )

        poster_url = None
        if "poster" in [o.value for o in request.outputs]:
            # STEP 4 — poster visual (content generated first, then image)
            poster = await self.image_provider.generate_poster(
                strategy, request.aspect_ratio, brand_colors=None
            )
            if not await self.moderation_provider.check_output(poster.image_url):
                raise ContentModerationError("Poster failed output moderation")
            poster_url = poster.image_url

        video_url = None
        if "video" in [o.value for o in request.outputs]:
            # STEP 5-6 — storyboard already in strategy; generate each scene
            scenes = []
            for i, scene_desc in enumerate(strategy.video_storyboard):
                scene = await self.video_provider.generate_scene(scene_desc, request.aspect_ratio)
                scenes.append(scene)
            # STEP 7 — background audio
            await self.audio_provider.select_or_generate_track(mood="cinematic")
            # STEP 9-10 — composition happens in video-engine (FFmpeg), Phase 7.
            # Placeholder URL until that service exists.
            video_url = f"https://mock-cdn.creatorpilot.ai/final/{job_id}.mp4"

        if "voiceover" in [o.value for o in request.outputs] and request.voiceover_language:
            # STEP 8 — optional voice-over
            await self.tts_provider.synthesize(strategy.social_caption, request.voiceover_language)

        logger.info("generation_completed", job_id=job_id)
        return GenerationResultResponse(
            job_id=job_id,
            status=GenerationStatus.completed,
            poster_url=poster_url,
            video_url=video_url,
            caption=strategy.social_caption,
            hashtags=strategy.hashtags,
            cta=strategy.cta,
        )
