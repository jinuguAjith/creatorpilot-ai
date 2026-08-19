from fastapi import FastAPI

from app.api.v1 import admin, brand_kit, campaigns, projects, reports
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.security_headers import SecurityHeadersMiddleware

settings = get_settings()
configure_logging(debug=settings.debug)

app = FastAPI(
    title="CreatorPilot AI Backend",
    version="0.1.0",
    description="Backend for CreatorPilot AI — never exposes AI provider keys to clients.",
)

app.add_middleware(SecurityHeadersMiddleware)

app.include_router(campaigns.router)
app.include_router(reports.router)
app.include_router(projects.router)
app.include_router(brand_kit.router)
app.include_router(admin.router)


@app.get("/healthz")
async def healthz():
    return {"status": "ok", "environment": settings.environment}
