import asyncio
from google import genai
from google.genai import types
from app.core.config import get_settings
from app.providers.interfaces import PosterAsset
from app.services.media_storage import MediaStorage

class GeminiImageGenerationProvider:
    def __init__(self):
        s = get_settings()
        if not s.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is required")
        self.client = genai.Client(api_key=s.gemini_api_key)
        self.settings = s
        self.storage = MediaStorage()

    async def generate_poster(
        self, strategy, aspect_ratio, brand_colors=None, *,
        resolution="4K", campaign_context="", industry="", location="", offer_details=""
    ):
        prompt = f"""
Create a premium commercial advertising poster.

CAMPAIGN: {campaign_context}
INDUSTRY: {industry}
LOCATION: {location}
OFFER: {offer_details}

HEADLINE: {strategy.headline}
SUBHEADLINE: {strategy.subheadline}
CTA: {strategy.cta}

VISUAL DIRECTION:
{strategy.visual_direction}

Make it photorealistic, premium, cinematic, sharp, HDR, realistic materials,
professional advertising photography, strong visual hierarchy, clean negative
space, polished typography and an immediately usable social-media composition.

NEGATIVE CONSTRAINTS:
blurry, low resolution, pixelated, cartoon, illustration, distorted objects,
duplicate people, malformed hands, random text, gibberish, watermark,
oversaturation, clutter, cheap stock-photo appearance.

Only use supplied campaign facts. Do not invent phone numbers, prices, dates,
addresses or offers.
"""
        model = self.settings.gemini_premium_image_model if resolution == "4K" else self.settings.gemini_image_model

        def call():
            return self.client.models.generate_content(
                model=model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    response_format={"image": {
                        "aspect_ratio": aspect_ratio,
                        "image_size": resolution,
                    }},
                ),
            )

        response = await asyncio.to_thread(call)
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                tmp = self.storage.root / "posters" / f"tmp-{id(image)}.png"
                image.save(tmp)
                local, url = self.storage.save_file("posters", str(tmp), "png")
                tmp.unlink(missing_ok=True)
                return PosterAsset(image_url=url, local_path=local)

        raise RuntimeError("Gemini returned no image")
