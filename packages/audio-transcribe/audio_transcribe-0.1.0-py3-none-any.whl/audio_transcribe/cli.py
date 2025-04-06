"""Command-line interface for audio transcription."""

import typer
from pathlib import Path
from typing import List, Optional
from rich.console import Console

from audio_transcribe.core import ModelSize, Transcriber

# Initialize rich console for better output
console = Console()
app = typer.Typer(help="Transcribe audio files using OpenAI's Whisper model")


@app.command()
def transcribe(
    audio_path: Path = typer.Argument(
        ..., exists=True, readable=True, help="Path to the audio file to transcribe"
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Directory to save the transcription (default: same as audio file)",
    ),
    model_size: ModelSize = typer.Option(
        ModelSize.BASE, "--model", "-m", help="Whisper model size to use"
    ),
    language: Optional[str] = typer.Option(
        None,
        "--language",
        "-l",
        help="Language of the audio (e.g., 'en', 'fr', 'zh'). If not specified, Whisper will auto-detect.",
    ),
    task: str = typer.Option(
        "transcribe",
        "--task",
        "-t",
        help="Task to perform: 'transcribe' or 'translate' (translates to English)",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    save_json: bool = typer.Option(
        False,
        "--save-json",
        "-j",
        help="Also save the full transcription result as JSON",
    ),
) -> None:
    """Transcribe an audio file using OpenAI's Whisper model.

    This tool supports various audio formats including MP3, WAV, OGG, and more.
    The transcription is saved as a text file, with an optional JSON output for detailed results.
    """
    # Prepare output directory
    if output_dir is None:
        output_dir = audio_path.parent

    # Initialize transcriber and process file
    transcriber = Transcriber(model_size=model_size)
    transcriber.transcribe_file(
        audio_path=audio_path,
        output_dir=output_dir,
        language=language,
        task=task,
        verbose=verbose,
        save_json=save_json,
    )


@app.command()
def batch(
    audio_dir: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=True,
        file_okay=False,
        help="Directory containing audio files to transcribe",
    ),
    output_dir: Path = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Directory to save the transcriptions (default: audio_dir/transcriptions)",
    ),
    model_size: ModelSize = typer.Option(
        ModelSize.BASE, "--model", "-m", help="Whisper model size to use"
    ),
    extensions: List[str] = typer.Option(
        ["mp3", "wav", "m4a", "ogg", "flac"],
        "--extensions",
        "-e",
        help="Audio file extensions to process",
    ),
) -> None:
    """Batch transcribe multiple audio files in a directory.

    This command will process all supported audio files in the specified directory.
    """
    # Prepare output directory
    if output_dir is None:
        output_dir = audio_dir / "transcriptions"

    # Initialize transcriber and process directory
    transcriber = Transcriber(model_size=model_size)
    transcriber.batch_transcribe(
        audio_dir=audio_dir,
        output_dir=output_dir,
        extensions=extensions,
    )
