"""Video launch utilities."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


class VideoLauncher:
    """Launches the inauguration video with the default system player."""

    def build_launch_command(self, video_path: Path) -> list[str]:
        path = str(video_path)
        if sys.platform.startswith("win"):
            return ["cmd", "/c", "start", "", path]
        if sys.platform == "darwin":
            return ["open", path]
        return ["xdg-open", path]

    def launch(self, video_path: Path) -> subprocess.Popen:
        command = self.build_launch_command(video_path)
        try:
            return subprocess.Popen(command, shell=False)
        except OSError as exc:
            raise RuntimeError(f"Unable to launch video: {video_path}") from exc
