"""CreatorPilot AI — Video Engine

Owns FFmpeg-based media composition: combining generated video scenes,
background audio, optional voice-over, logo overlay, text overlays,
subtitles, and transitions into a final MP4.

STATUS: PLANNED, not implemented.

This is deliberately not built yet because it needs real scene/audio
assets from real AI providers to develop and test against meaningfully —
composing mock placeholder URLs together doesn't validate anything.
Build this once Phase 4b (real Gemini/Veo/TTS providers) exists.

Intended interface (called by backend/app/services/orchestrator.py once
scenes + audio are generated):

    def compose_video(
        scene_clip_paths: list[str],
        audio_path: str,
        voiceover_path: str | None,
        logo_path: str | None,
        text_overlays: list[TextOverlay],
        aspect_ratio: str,
        output_path: str,
    ) -> str:
        '''Runs ffmpeg to concatenate scenes, mix audio/voiceover, burn in
        text overlays and logo, and write output_path. Returns output_path.'''

Suggested approach:
- Use `ffmpeg-python` or raw subprocess calls to `ffmpeg` binary
- Run as a separate worker process/service (not inline in the API request
  path) since composition is CPU-bound and can take tens of seconds
- Pull inputs from Cloud Storage, push output back to Cloud Storage,
  store only the resulting URL in Firestore (per docs/DATABASE.md)
- Enforce docs/SECURITY.md limits: max input file size, max duration,
  validate that inputs are actual media files before invoking ffmpeg
"""
