"""Configuration for the IEEE Inauguration System."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for the inauguration system."""

    title: str = "IEEE WIE Aadhya Inauguration System"
    event_name: str = "IEEE Women in Engineering - Aadhya"
    video_file: str = "assets/inauguration_video.mp4"
    logo_file: str = "assets/event_logo.png"
    camera_index: int = 0
    required_consecutive_detections: int = 8
    detection_loop_interval_ms: int = 40


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = AppConfig()
