from pathlib import Path
from uuid import uuid4
from app.core.config import get_settings

class MediaStorage:
    def __init__(self):
        s = get_settings()
        self.root = Path(s.media_dir)
        self.base_url = s.media_base_url.rstrip("/")
        for folder in ("posters", "videos", "scenes", "audio", "voiceovers"):
            (self.root / folder).mkdir(parents=True, exist_ok=True)

    def save_file(self, folder: str, source_path: str, extension: str) -> tuple[str, str]:
        name = f"{uuid4().hex}.{extension.lstrip('.')}"
        target = self.root / folder / name
        target.write_bytes(Path(source_path).read_bytes())
        return str(target), f"{self.base_url}/{folder}/{name}"
