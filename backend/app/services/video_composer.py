import asyncio
import shutil
import subprocess
from pathlib import Path
from uuid import uuid4
from app.core.config import get_settings
from app.providers.interfaces import VideoSceneAsset
from app.services.media_storage import MediaStorage

class VideoComposer:
    async def compose(self, scenes: list[VideoSceneAsset]) -> str:
        if not scenes:
            raise ValueError("No video scenes to compose")
        if not shutil.which("ffmpeg"):
            raise RuntimeError("FFmpeg is required")

        storage = MediaStorage()
        work = Path(get_settings().media_dir) / "scenes" / f"compose-{uuid4().hex}"
        work.mkdir(parents=True, exist_ok=True)

        try:
            ordered = sorted(scenes, key=lambda x: x.scene_index)
            for i, scene in enumerate(ordered):
                if not scene.local_path:
                    raise RuntimeError(f"Scene {i} has no local path")
                shutil.copy2(scene.local_path, work / f"{i:02d}.mp4")

            concat = work / "concat.txt"
            concat.write_text(
                "".join(
                    f"file '{(work / f'{i:02d}.mp4').as_posix()}'\n"
                    for i in range(len(ordered))
                ),
                encoding="utf-8",
            )

            output = work / "final.mp4"

            def run():
                subprocess.run(
                    ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                     "-i", str(concat), "-c", "copy", str(output)],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

            await asyncio.to_thread(run)
            _, url = storage.save_file("videos", str(output), "mp4")
            return url
        finally:
            shutil.rmtree(work, ignore_errors=True)
