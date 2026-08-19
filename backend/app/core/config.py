from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All secrets come from environment / secret manager — never hardcoded.
    Local dev uses `.env` (gitignored); staging/prod use injected env vars
    from the deployment platform's secret store.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"  # development | staging | production
    debug: bool = True

    # Firebase / GCP
    firebase_project_id: str = ""
    google_application_credentials: str = ""

    # AI providers — names only, never keys, live in code. Keys are read
    # from env/secret manager at call time inside providers/*.
    gemini_api_key: str = ""
    video_gen_api_key: str = ""
    tts_api_key: str = ""

    # JWT / session
    jwt_secret: str = "dev-only-insecure-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Rate limiting / cost control
    max_generations_per_user_per_day: int = 10
    max_video_duration_seconds: int = 60
    generation_timeout_seconds: int = 300
    job_retry_limit: int = 2

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
