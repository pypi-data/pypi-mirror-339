"""Setup script for the audio_transcribe package."""

from pathlib import Path

from setuptools import find_packages, setup

# Read the contents of README.md file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="audio_transcribe",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer",
        "openai-whisper",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "audio-transcribe=audio_transcribe.cli:app",
        ],
    },
    python_requires=">=3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for transcribing audio files using OpenAI's Whisper model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/audio_transcribe",
    keywords=["audio", "transcription", "whisper", "openai", "speech-to-text"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/audio_transcribe/issues",
        "Source": "https://github.com/yourusername/audio_transcribe",
    },
)
