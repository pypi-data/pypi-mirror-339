"""FFmpeg converter package."""

__version__ = "0.3.6"

from .audio import AudioConverter
from .video import VideoConverter

__all__ = ["AudioConverter", "VideoConverter"]
