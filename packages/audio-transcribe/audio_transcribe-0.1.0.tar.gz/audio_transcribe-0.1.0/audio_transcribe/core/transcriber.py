"""Core transcription functionality."""

import time
from pathlib import Path
from typing import Dict, Any, Optional, List

import whisper
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)

from audio_transcribe.core.models import ModelSize
from audio_transcribe.core.utils import get_timestamp, save_transcription, save_json_result

# Initialize rich console for better output
console = Console()


class Transcriber:
    """Handles audio transcription using OpenAI's Whisper model."""

    def __init__(self, model_size: ModelSize = ModelSize.BASE):
        """Initialize the transcriber with the specified model size.

        Args:
            model_size: The Whisper model size to use
        """
        self.model_size = model_size
        self.model = None

    def load_model(self) -> None:
        """Load the Whisper model with progress indication."""
        if self.model is not None:
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task_id = progress.add_task(
                f"Loading Whisper model ({self.model_size.value})...", total=None
            )
            self.model = whisper.load_model(self.model_size.value)
            progress.update(task_id, completed=True)

    def transcribe_file(
        self,
        audio_path: Path,
        output_dir: Path,
        language: Optional[str] = None,
        task: str = "transcribe",
        verbose: bool = False,
        save_json: bool = False,
    ) -> Dict[str, Any]:
        """Transcribe a single audio file.

        Args:
            audio_path: Path to the audio file
            output_dir: Directory to save the transcription
            language: Language of the audio (auto-detect if None)
            task: Task to perform ('transcribe' or 'translate')
            verbose: Enable verbose output
            save_json: Also save the full transcription result as JSON

        Returns:
            The transcription result dictionary
        """
        start_time = time.time()

        # Ensure model is loaded
        if self.model is None:
            self.load_model()

        # Prepare output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate output filenames
        audio_filename = audio_path.stem
        timestamp = get_timestamp()
        output_text_path = output_dir / f"{audio_filename}_transcript_{timestamp}.txt"
        output_json_path = output_dir / f"{audio_filename}_transcript_{timestamp}.json"

        # Set up transcription options
        options: Dict[str, Any] = {"task": task, "verbose": verbose}

        if language:
            options["language"] = language

        # Transcribe
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold green]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task_id = progress.add_task(f"Transcribing {audio_path.name}", total=None)
            result = self.model.transcribe(str(audio_path), **options)
            progress.update(task_id, completed=True)

        # Save transcription text
        save_transcription(result["text"], output_text_path)

        # Optionally save JSON result
        if save_json:
            save_json_result(result, output_json_path)

        # Print completion summary
        elapsed_time = time.time() - start_time
        console.print(f"⏱️  Total processing time: [bold]{elapsed_time:.2f}[/] seconds")

        return result

    def batch_transcribe(
        self,
        audio_dir: Path,
        output_dir: Path,
        extensions: List[str] = ["mp3", "wav", "m4a", "ogg", "flac"],
    ) -> None:
        """Batch transcribe multiple audio files in a directory.

        Args:
            audio_dir: Directory containing audio files
            output_dir: Directory to save the transcriptions
            extensions: Audio file extensions to process
        """
        # Prepare output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Find all audio files with matching extensions
        audio_files = []
        for ext in extensions:
            audio_files.extend(list(audio_dir.glob(f"*.{ext}")))

        if not audio_files:
            console.print(
                "[bold red]No audio files found with the specified extensions![/]"
            )
            return

        console.print(f"Found [bold cyan]{len(audio_files)}[/] audio files to process.")

        # Ensure model is loaded
        if self.model is None:
            self.load_model()

        # Process each file
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            batch_task = progress.add_task("Processing files", total=len(audio_files))

            for audio_file in audio_files:
                progress.update(batch_task, description=f"Transcribing {audio_file.name}")

                # Generate output path
                output_path = output_dir / f"{audio_file.stem}_transcript.txt"

                # Transcribe
                result = self.model.transcribe(str(audio_file))

                # Save transcription
                save_transcription(result["text"], output_path)

                # Update progress
                progress.update(batch_task, advance=1)

        console.print("[bold green]✅ Batch transcription completed![/]")
