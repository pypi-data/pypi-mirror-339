#!/usr/bin/env python3
"""Entry point for the audio transcribe package."""

import typer
from rich.console import Console

from audio_transcribe.cli import app

console = Console()

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/]")
        raise typer.Exit(1)
