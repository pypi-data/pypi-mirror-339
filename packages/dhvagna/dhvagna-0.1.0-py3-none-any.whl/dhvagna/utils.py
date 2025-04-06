import os
import wave
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
import speech_recognition as sr
from pathlib import Path
from .wav import record_audio, transcribe_wav_file

console = Console()

SAVE_DIR = Path("saves")
if not SAVE_DIR.exists():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]Created save directory: {SAVE_DIR}[/]")

# These functions are imported from wav.py for a cleaner API
# The implementations in wav.py will be used