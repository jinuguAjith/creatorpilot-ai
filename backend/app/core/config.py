from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    debug: bool = True
    firebase_project_id: str = ""
    google_application_credentials: str = ""

    gemini_api_key: str = ""
    gemini_text_model: str = "gemini-3.7-flash"
    gemini_image_model: str = "gemini-3.1-flash-image"
    gemini_premium_image_model: str = "gemini-3-pro-image"
    gemini_video_model: str = "veo-3.1-generate-preview"

    default_image_size: str = "4K"
    default_video_resolution: str = "1080p"
    media_dir: str = "/tmp/creatorpilot-media"
    media_base_url: str = "http://localhost:8000/media"

    max_generations_per_user_per_day: int = 10
    max_video_duration_seconds: int = 60
    generation_timeout_seconds: int = 900
    job_retry_limit: int = 2
    allow_mock_providers: bool = True

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

@lru_cache
def get_settings() -> Settings:
    return Settings()
