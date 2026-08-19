"""Provider abstraction layer. Every AI capability the orchestrator needs
is defined as an interface here. Real implementations (Gemini, Veo, TTS)
live in provider-specific modules and are selected via dependency
injection in Phase 4b — never imported directly by services/orchestrator.

This lets automated tests run against MockXProvider with zero real AI
calls, and lets a future provider swap (e.g. Veo -> another video model)
happen without touching orchestration logic.
"""
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
    video_storyboard: list[str]  # one entry per scene


@dataclass
class PosterAsset:
    image_url: str


@dataclass
class VideoSceneAsset:
    scene_index: int
    clip_url: str


@dataclass
class AudioAsset:
    audio_url: str


@dataclass
class VoiceoverAsset:
    audio_url: str
    language: str


class TextGenerationProvider(ABC):
    """Generates campaign strategy text (headline, caption, storyboard)."""

    @abstractmethod
    async def generate_strategy(
        self, description: str, industry: str, style: str, audience: str
    ) -> CampaignStrategy: ...


class ImageGenerationProvider(ABC):
    @abstractmethod
    async def generate_poster(
        self, strategy: CampaignStrategy, aspect_ratio: str, brand_colors: list[str] | None
    ) -> PosterAsset: ...


class VideoGenerationProvider(ABC):
    @abstractmethod
    async def generate_scene(self, scene_description: str, aspect_ratio: str) -> VideoSceneAsset: ...


class AudioProvider(ABC):
    @abstractmethod
    async def select_or_generate_track(self, mood: str) -> AudioAsset: ...


class TTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str, language: str) -> VoiceoverAsset: ...


class ModerationProvider(ABC):
    @abstractmethod
    async def check_input(self, text: str) -> bool: ...  # True = safe

    @abstractmethod
    async def check_output(self, asset_url: str) -> bool: ...  # True = safe
