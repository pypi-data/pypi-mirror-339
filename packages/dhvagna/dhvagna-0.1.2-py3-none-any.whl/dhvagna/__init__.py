"""
Dhvagna - A multilingual voice transcription tool for Telugu and English.

This package provides functionality for recording and transcribing speech
in both Telugu and English languages using Google's Gemini API.
"""

from .wav import record_audio, transcribe_wav_file, set_custom_prompts, reset_prompts
from .wav import DEFAULT_TRANSCRIPTION_PROMPT, DEFAULT_REFINEMENT_PROMPT_TEMPLATE, DEFAULT_TITLE_FORMAT

__version__ = "0.1.2"
__all__ = [
    "record_audio", 
    "transcribe_wav_file", 
    "set_custom_prompts", 
    "reset_prompts",
    "DEFAULT_TRANSCRIPTION_PROMPT",
    "DEFAULT_REFINEMENT_PROMPT_TEMPLATE",
    "DEFAULT_TITLE_FORMAT"
]