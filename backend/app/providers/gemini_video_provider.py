import asyncio
from pathlib import Path
from google import genai
from google.genai import types
from app.core.config import get_settings
from app.providers.interfaces import VideoSceneAsset
from app.services.media_storage import MediaStorage

class GeminiVideoGenerationProvider:
    def __init__(self):
        s = get_settings()
        if not s.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is required")
        self.client = genai.Client(api_key=s.gemini_api_key)
        self.settings = s
        self.storage = MediaStorage()

    async def generate_scene(
        self, scene_description, aspect_ratio, *,
        scene_index=0, resolution="1080p", duration_seconds=8,
        reference_image_path=None, campaign_context=""
    ):
        if resolution in {"1080p", "4k"}:
            duration_seconds = 8

        prompt = f"""
Create a premium commercial social-media video scene.

CAMPAIGN: {campaign_context}
SCENE: {scene_description}

Style: photorealistic commercial cinematography, premium brand film,
cinematic lighting, natural motion, realistic physics, crisp details,
professional camera movement, refined color grading.

Audio: subtle background music and natural ambient sound matching the scene.
No spoken dialogue unless explicitly requested.

Avoid: blurry output, flicker, warped objects, duplicate people, malformed
hands, unnatural motion, random text, watermark, cartoon or illustration.
"""

        cfg = types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            duration_seconds=str(duration_seconds),
            number_of_videos=1,
        )

        def start():
            image = None
            if reference_image_path and Path(reference_image_path).exists():
                from PIL import Image
                image = Image.open(reference_image_path)
            return self.client.models.generate_videos(
                model=self.settings.gemini_video_model,
                prompt=prompt,
                image=image,
                config=cfg,
            )

        operation = await asyncio.to_thread(start)
        deadline = asyncio.get_running_loop().time() + self.settings.generation_timeout_seconds

        while not operation.done:
            if asyncio.get_running_loop().time() > deadline:
                raise TimeoutError("Veo generation timed out")
            await asyncio.sleep(10)
            operation = await asyncio.to_thread(self.client.operations.get, operation)

        if getattr(operation, "error", None):
            raise RuntimeError(f"Veo generation failed: {operation.error}")

        generated = operation.response.generated_videos[0]
        tmp = self.storage.root / "scenes" / f"veo-{scene_index}-{id(operation)}.mp4"

        def download():
            self.client.files.download(file=generated.video)
            generated.video.save(tmp)

        await asyncio.to_thread(download)
        local, url = self.storage.save_file("videos", str(tmp), "mp4")
        tmp.unlink(missing_ok=True)

        return VideoSceneAsset(scene_index=scene_index, clip_url=url, local_path=local)
