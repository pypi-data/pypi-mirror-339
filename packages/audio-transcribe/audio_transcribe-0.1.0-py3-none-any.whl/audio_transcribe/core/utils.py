"""Utility functions for the audio transcribe package."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from rich.console import Console

# Initialize rich console for better output
console = Console()


def get_timestamp() -> str:
    """Generate a timestamp string for filenames.

    Returns:
        A formatted timestamp string.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_transcription(text: str, output_path: Path) -> None:
    """Save transcription text to a file.

    Args:
        text: The transcribed text to save
        output_path: Path where the text will be saved
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    console.print(f"✅ Transcription saved to: [bold cyan]{output_path}[/]")


def save_json_result(result: Dict[str, Any], output_path: Path) -> None:
    """Save transcription result as JSON.

    Args:
        result: The transcription result dictionary
        output_path: Path where the JSON will be saved
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    console.print(f"📊 JSON data saved to: [bold cyan]{output_path}[/]")
