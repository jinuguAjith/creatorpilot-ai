import asyncio
import json
from google import genai
from google.genai import types
from app.core.config import get_settings
from app.providers.interfaces import CampaignStrategy, TextGenerationProvider

class GeminiTextGenerationProvider(TextGenerationProvider):
    def __init__(self):
        s = get_settings()
        if not s.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is required")
        self.client = genai.Client(api_key=s.gemini_api_key)
        self.model = s.gemini_text_model

    async def generate_strategy(self, description, industry, style, audience):
        prompt = f"""
You are CreatorPilot AI's senior advertising creative director.

Idea: {description}
Industry: {industry}
Style: {style}
Audience: {audience}

Return ONLY valid JSON with:
headline, subheadline, cta, social_caption, hashtags,
visual_direction, video_storyboard.

Rules:
- Make it specific to the business and offer.
- Never invent dates, prices, phone numbers or addresses.
- hashtags must contain 5-10 strings beginning with #.
- video_storyboard must contain exactly 5 detailed cinematic scenes.
- Every scene must preserve the same business identity and visual language.
"""
        def call():
            return self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema={
                        "type": "object",
                        "properties": {
                            "headline": {"type": "string"},
                            "subheadline": {"type": "string"},
                            "cta": {"type": "string"},
                            "social_caption": {"type": "string"},
                            "hashtags": {"type": "array", "items": {"type": "string"}},
                            "visual_direction": {"type": "string"},
                            "video_storyboard": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": [
                            "headline", "subheadline", "cta", "social_caption",
                            "hashtags", "visual_direction", "video_storyboard"
                        ],
                    },
                ),
            )

        response = await asyncio.to_thread(call)
        if not response.text:
            raise RuntimeError("Gemini returned an empty strategy")

        data = json.loads(response.text)
        scenes = data["video_storyboard"]
        if len(scenes) < 5:
            raise RuntimeError("Gemini returned fewer than five video scenes")

        return CampaignStrategy(
            headline=data["headline"],
            subheadline=data["subheadline"],
            cta=data["cta"],
            social_caption=data["social_caption"],
            hashtags=data["hashtags"],
            visual_direction=data["visual_direction"],
            video_storyboard=scenes[:5],
        )
