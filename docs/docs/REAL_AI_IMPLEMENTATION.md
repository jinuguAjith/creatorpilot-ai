# CreatorPilot AI — real AI generation

This change removes the production placeholder path.

Flow:
1. Gemini 3.7 Flash creates the campaign strategy.
2. Gemini 3 Pro Image creates the premium 4K poster.
3. Veo 3.1 creates five 8-second 9:16 scenes at 1080p.
4. The first Veo scene can use the generated poster as its starting image.
5. FFmpeg concatenates the five scenes into an approximately 40-second video.
6. FastAPI serves generated media under `/media`.

Set `GEMINI_API_KEY` only on the backend.

Example:
Small hotel named Spice Garden Hotel in Hyderabad. Grand Opening on 30
August 2026. 20% OFF during opening week. Target families, couples,
students and local food lovers. Premium modern warm realistic advertising.

For local development:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

For Docker, FFmpeg is installed automatically.

Do not commit `.env` or API keys.
