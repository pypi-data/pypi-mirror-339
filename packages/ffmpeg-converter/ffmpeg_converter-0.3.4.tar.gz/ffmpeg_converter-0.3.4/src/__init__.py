"""FFmpeg converter package."""

__version__ = "0.3.4"

from .audio import AudioConverter
from .video import VideoConverter

__all__ = ["AudioConverter", "VideoConverter"]
