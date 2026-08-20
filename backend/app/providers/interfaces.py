from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class CampaignStrategy:
    headline: str
    subheadline: str
    cta: str
    social_caption: str
    hashtags: list[str]
    visual_direction: str
    video_storyboard: list[str]

@dataclass
class PosterAsset:
    image_url: str
    local_path: str | None = None

@dataclass
class VideoSceneAsset:
    scene_index: int
    clip_url: str
    local_path: str | None = None

@dataclass
class AudioAsset:
    audio_url: str

@dataclass
class VoiceoverAsset:
    audio_url: str
    language: str

class TextGenerationProvider(ABC):
    @abstractmethod
    async def generate_strategy(self, description, industry, style, audience) -> CampaignStrategy: ...

class ImageGenerationProvider(ABC):
    @abstractmethod
    async def generate_poster(
        self, strategy, aspect_ratio, brand_colors, *,
        resolution="4K", campaign_context="", industry="", location="", offer_details=""
    ) -> PosterAsset: ...

class VideoGenerationProvider(ABC):
    @abstractmethod
    async def generate_scene(
        self, scene_description, aspect_ratio, *,
        scene_index=0, resolution="1080p", duration_seconds=8,
        reference_image_path=None, campaign_context=""
    ) -> VideoSceneAsset: ...

class AudioProvider(ABC):
    @abstractmethod
    async def select_or_generate_track(self, mood) -> AudioAsset: ...

class TTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text, language) -> VoiceoverAsset: ...

class ModerationProvider(ABC):
    @abstractmethod
    async def check_input(self, text: str) -> bool: ...

    @abstractmethod
    async def check_output(self, asset_url: str) -> bool: ...
