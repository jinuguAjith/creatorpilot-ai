from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1 import admin, brand_kit, campaigns, projects, reports
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.security_headers import SecurityHeadersMiddleware
from app.services.media_storage import MediaStorage

settings = get_settings()
configure_logging(debug=settings.debug)
MediaStorage()

app = FastAPI(
    title="CreatorPilot AI Backend",
    version="0.2.0",
    description="Real Gemini/Veo generation backend for CreatorPilot AI.",
)

app.add_middleware(SecurityHeadersMiddleware)
app.mount("/media", StaticFiles(directory=settings.media_dir), name="media")

app.include_router(campaigns.router)
app.include_router(reports.router)
app.include_router(projects.router)
app.include_router(brand_kit.router)
app.include_router(admin.router)

@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "environment": settings.environment,
        "ai_provider": "gemini" if settings.gemini_api_key else "mock",
    }
