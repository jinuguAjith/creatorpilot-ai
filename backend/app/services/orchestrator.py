from dataclasses import dataclass
from app.core.logging import get_logger
from app.providers.interfaces import (
    AudioProvider, ImageGenerationProvider, ModerationProvider,
    TextGenerationProvider, TTSProvider, VideoGenerationProvider,
)
from app.schemas.campaign import CampaignRequest, GenerationResultResponse, GenerationStatus
from app.services.video_composer import VideoComposer

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

    async def run(self, job_id, request: CampaignRequest):
        if not await self.moderation_provider.check_input(request.description):
            raise ContentModerationError("Input failed content moderation")

        strategy = await self.text_provider.generate_strategy(
            request.description, request.industry, request.style, request.target_audience
        )

        outputs = {x.value for x in request.outputs}
        poster_url = None
        poster_path = None

        if "poster" in outputs or "video" in outputs:
            poster = await self.image_provider.generate_poster(
                strategy,
                request.aspect_ratio if request.aspect_ratio in {"1:1", "4:5", "9:16", "16:9"} else "4:5",
                None,
                resolution="4K",
                campaign_context=request.description,
                industry=request.industry,
                location=request.location,
                offer_details=request.offer_details,
            )
            if not await self.moderation_provider.check_output(poster.image_url):
                raise ContentModerationError("Poster failed output moderation")
            poster_url = poster.image_url
            poster_path = poster.local_path

        video_url = None
        if "video" in outputs:
            scenes = []
            for i, scene_text in enumerate(strategy.video_storyboard[:5]):
                scenes.append(
                    await self.video_provider.generate_scene(
                        scene_text,
                        "9:16",
                        scene_index=i,
                        resolution="1080p",
                        duration_seconds=8,
                        reference_image_path=poster_path if i == 0 else None,
                        campaign_context=request.description,
                    )
                )
            video_url = await VideoComposer().compose(scenes)

        if "voiceover" in outputs and request.voiceover_language:
            await self.tts_provider.synthesize(strategy.social_caption, request.voiceover_language)

        return GenerationResultResponse(
            job_id=job_id,
            status=GenerationStatus.completed,
            poster_url=poster_url,
            video_url=video_url,
            caption=strategy.social_caption,
            hashtags=strategy.hashtags,
            cta=strategy.cta,
        )
