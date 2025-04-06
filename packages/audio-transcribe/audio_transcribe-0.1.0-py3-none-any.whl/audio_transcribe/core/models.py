"""Model definitions for the audio transcribe package."""

from enum import Enum


class ModelSize(str, Enum):
    """Whisper model sizes"""

    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
