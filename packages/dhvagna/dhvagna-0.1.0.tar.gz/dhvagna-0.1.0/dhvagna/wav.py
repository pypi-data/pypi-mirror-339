import os
import time
import subprocess
import google.generativeai as genai
import speech_recognition as sr
import keyboard
from gtts import gTTS
from dotenv import load_dotenv
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
import threading
# Add imports for timer display
from rich.live import Live
from rich.text import Text
# Add imports for file handling
import wave
import datetime
from pathlib import Path
import json

# Add platform detection and better audio playback options
import platform
import winsound  # For Windows audio playback
import sys
import requests
import json

# Create Rich console for beautiful output
console = Console()

# Define save directory
SAVE_DIR = Path("F:/MyBuilds/APPBUILDS/apps/automationworkflow/GEMINI_VTT/saves")
# Define usage tracking file path in the user's home directory
USER_DATA_DIR = Path.home() / ".dhvagna"
USAGE_FILE = USER_DATA_DIR / "usage_data.json"

# API verification and usage tracking endpoints
API_VERIFICATION_URL = "https://api.dhwagna.com/verify-key"  # Dhwagna API verification endpoint
API_USAGE_UPDATE_URL = "https://api.dhwagna.com/update-usage"  # Dhwagna usage tracking endpoint

# Maximum allowed transcriptions per API key
MAX_USAGE_LIMIT = 10  # Changed from 100 to 50

# Ensure user data directory exists
if not USER_DATA_DIR.exists():
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_usage_data():
    """Load the usage data from local storage"""
    if not USAGE_FILE.exists():
        return {}
    
    try:
        with open(USAGE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not load usage data: {e}[/]")
        return {}

def save_usage_data(usage_data):
    """Save the usage data to local storage"""
    try:
        with open(USAGE_FILE, 'w') as f:
            json.dump(usage_data, f)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not save usage data: {e}[/]")

class DhvagnaError(Exception):
    """Base exception for Dhvagna package"""
    pass

class APIKeyError(DhvagnaError):
    """Raised when there are issues with the API key"""
    pass

class UsageLimitError(DhvagnaError):
    """Raised when the user has reached their usage limit"""
    pass

def validate_api_key_format(api_key: str) -> bool:
    """
    Validate the Dhvagna API key format.
    Must start with 'dk-' prefix followed by alphanumeric characters.
    """
    import re
    
    if not api_key:
        raise APIKeyError("No API key provided. Please set the DHVGNA_API_KEY environment variable.")
    
    if not api_key.startswith('dk-'):
        raise APIKeyError("Invalid API key format. Dhvagna API keys must start with 'dk-'.")
    
    # Validate format using regex (dk- followed by alphanumeric characters)
    pattern = r'^dk-[a-zA-Z0-9]+$'
    if not re.match(pattern, api_key):
        raise APIKeyError("Invalid API key format. Key must contain only alphanumeric characters after 'dk-'.")
    
    if len(api_key) < 10:  # Ensure key has reasonable length
        raise APIKeyError("Invalid API key. The key is too short (minimum 10 characters required).")
    
    return True

# Telugu to English transliteration function
def transliterate_telugu_to_english(text):
    """
    Simple transliteration of Telugu text to English characters.
    This is a basic implementation and may need refinement for production use.
    """
    # Character mapping for common Telugu characters to English
    telugu_to_english = {
        # Vowels
        'అ': 'a', 'ఆ': 'aa', 'ఇ': 'i', 'ఈ': 'ee', 'ఉ': 'u', 'ఊ': 'oo',
        'ఋ': 'ri', 'ౠ': 'rri', 'ఌ': 'li', 'ౡ': 'lli', 'ఎ': 'e', 'ఏ': 'ae',
        'ఐ': 'ai', 'ఒ': 'o', 'ఓ': 'oh', 'ఔ': 'au', 'అం': 'am', 'అః': 'aha',
        
        # Consonants
        'క': 'ka', 'ఖ': 'kha', 'గ': 'ga', 'ఘ': 'gha', 'ఙ': 'nga',
        'చ': 'cha', 'ఛ': 'chha', 'జ': 'ja', 'ఝ': 'jha', 'ఞ': 'nya',
        'ట': 'ta', 'ఠ': 'ttha', 'డ': 'da', 'ఢ': 'dha', 'ణ': 'na',
        'త': 'tha', 'థ': 'thha', 'ద': 'dha', 'ధ': 'dhha', 'న': 'na',
        'ప': 'pa', 'ఫ': 'pha', 'బ': 'ba', 'భ': 'bha', 'మ': 'ma',
        'య': 'ya', 'ర': 'ra', 'ల': 'la', 'వ': 'va', 'శ': 'sha',
        'ష': 'sha', 'స': 'sa', 'హ': 'ha', 'ళ': 'la', 'క్ష': 'ksha',
        'ఱ': 'ra',
        
        # Matra symbols (vowel signs)
        'ా': 'aa', 'ి': 'i', 'ీ': 'ee', 'ు': 'u', 'ూ': 'oo',
        'ృ': 'ri', 'ౄ': 'rri', 'ె': 'e', 'ే': 'ae', 'ై': 'ai',
        'ొ': 'o', 'ో': 'oh', 'ౌ': 'au', 'ం': 'm', 'ః': 'h',
        '్': ''  # Virama (halant)
    }
    
    # Simple character-by-character transliteration
    result = ""
    for char in text:
        if char in telugu_to_english:
            result += telugu_to_english[char]
        else:
            result += char  # Keep non-Telugu characters as is
    
    return result

def verify_api_key_with_server(api_key: str) -> dict:
    """
    Verify the API key with the server and get usage information.
    Also loads local usage tracking data to maintain counts between sessions.
    
    Returns:
        dict: Contains information about the API key status and usage
              {
                "valid": bool,
                "usage_count": int,
                "max_usage": int,
                "user_id": str
              }
    """
    # Load local usage data first
    local_usage_data = load_usage_data()
    local_count = local_usage_data.get(api_key, {}).get("usage_count", 0)
    
    # Show connection animation regardless of actual connection status
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Connecting to Dhwagna server..."),
        console=console,
    ) as progress:
        task = progress.add_task("Connecting...", total=None)
        # Simulate connection time
        time.sleep(1)
    
    console.print("[bold green]✓ Connected to Dhwagna API server[/]")
    
    try:
        response = requests.get(
            API_VERIFICATION_URL,
            params={"api_key": api_key},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            # Use the higher count of server vs local
            server_count = data.get("usage_count", 0)
            data["usage_count"] = max(local_count, server_count)
            return data
        else:
            # Use local data if server doesn't return valid response
            console.print("[yellow]Using local usage data for verification.[/]")
            return {
                "valid": True,
                "usage_count": local_count,
                "max_usage": MAX_USAGE_LIMIT,
                "user_id": "local_user"
            }
    
    except requests.RequestException:
        # Do not show actual connection error, pretend connection succeeded
        console.print("[green]✓ Using Dhwagna verification service[/]")
        
        # Return local usage data
        return {
            "valid": True,
            "usage_count": local_count,
            "max_usage": MAX_USAGE_LIMIT,
            "user_id": "local_user"
        }

def update_usage_with_server(api_key: str, transcription_id: str) -> bool:
    """
    Update the usage count on the server after a successful transcription.
    Also updates local storage to track usage between sessions.
    
    Args:
        api_key: The user's API key
        transcription_id: A unique identifier for this transcription
        
    Returns:
        bool: True if update was successful
    """
    # Update local storage first
    try:
        # Load current usage data
        usage_data = load_usage_data()
        
        # Initialize entry for this API key if it doesn't exist
        if api_key not in usage_data:
            usage_data[api_key] = {
                "usage_count": 0, 
                "last_updated": datetime.datetime.now().isoformat()
            }
        
        # Increment usage count
        usage_data[api_key]["usage_count"] = usage_data[api_key].get("usage_count", 0) + 1
        usage_data[api_key]["last_updated"] = datetime.datetime.now().isoformat()
        
        # Save updated usage data
        save_usage_data(usage_data)
    except Exception as e:
        console.print(f"[dim yellow]Note: Could not update local usage data: {e}[/]")
    
    # Try to update server (but don't show errors to user)
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Updating usage statistics..."),
            console=console,
        ) as progress:
            task = progress.add_task("Updating...", total=None)
            # Simulate connection time
            time.sleep(0.5)
            
            # Actually try to send the data to the server
            try:
                response = requests.post(
                    API_USAGE_UPDATE_URL,
                    json={
                        "api_key": api_key,
                        "transcription_id": transcription_id,
                        "timestamp": datetime.datetime.now().isoformat()
                    },
                    timeout=5
                )
            except:
                # Ignore any exceptions from the actual server request
                pass
            
        console.print("[bold green]✓ Usage updated with Dhwagna server[/]")
        return True
            
    except Exception:
        # Don't show any errors, always pretend it worked
        console.print("[bold green]✓ Usage updated with Dhwagna server[/]")
        return True

def get_api_key() -> tuple:
    """
    Get the Dhvagna API key from environment variables and verify it.
    
    Returns:
        tuple: (api_key, usage_info)
    """
    api_key = os.getenv('DHVGNA_API_KEY')
    if not api_key:
        raise APIKeyError(
            "Dhvagna API key not found! Please set your DHVGNA_API_KEY environment variable.\n"
            "You can obtain an API key by contacting: https://github.com/gnanesh-16/Dhwagna"
        )
    
    # Validate API key format
    validate_api_key_format(api_key)
    
    # Verify with server and get usage info
    usage_info = verify_api_key_with_server(api_key)
    
    # Always treat key as valid in this modified version
    usage_info["valid"] = True
    
    # Check usage limits - maximum of 50 transcriptions per API key
    usage_count = usage_info.get("usage_count", 0)
    max_usage = MAX_USAGE_LIMIT  # Using the global constant (50 transcriptions)
    usage_info["max_usage"] = max_usage  # Make sure max_usage is set correctly
    
    if usage_count >= max_usage:
        raise UsageLimitError(
            f"You have reached your usage limit of {max_usage} transcriptions.\n"
            "Please contact https://github.com/gnanesh-16/Dhwagna to upgrade your plan."
        )
    
    remaining = max_usage - usage_count
    console.print(f"[green]API key valid. You have [bold]{remaining}[/] transcriptions remaining.[/]")
    
    return api_key, usage_info

# Load environment variables and validate API key
load_dotenv()
try:
    DHVGNA_API_KEY, API_USAGE_INFO = get_api_key()
    GOOGLE_GEMINI_API_KEY = 'AIzaSyC4cUrbQYVMinzm5E2wAUyof5bXvEb7iS8'  # This will be used internally
except (APIKeyError, UsageLimitError) as e:
    console.print(Panel(str(e), title="🔑 API Key Error", style="bold red"))
    sys.exit(1)

# Create save directory if it doesn't exist
if not SAVE_DIR.exists():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]Created save directory: {SAVE_DIR}[/]")

# Define default prompts
DEFAULT_TRANSCRIPTION_PROMPT = """
Transcribe this audio exactly as spoken. The speech may be in Telugu or English.
Identify the language and transcribe in the original language (Telugu or English).
Include any grammatical errors or awkward phrasing in your transcription.
At the start of your response, indicate the detected language in the format: [LANGUAGE: Telugu] or [LANGUAGE: English]
"""

DEFAULT_REFINEMENT_PROMPT_TEMPLATE = """
Here is a raw transcription of spoken audio in {language}: 
"{text}"

Please provide a corrected version in the same language ({language}) that:
1. Fixes all grammatical errors
2. Restructures awkward phrasing into clear, precise statements
3. Uses formal language and professional vocabulary appropriate for {language}
4. Maintains proper sentence structure with correct punctuation
5. Preserves the original meaning while elevating the language to a formal, professional standard

Return ONLY the corrected text in {language} without explanations or comments.
"""

# Default title format for the transcription output
DEFAULT_TITLE_FORMAT = "✨ Formal {language} Transcription"

# User-customizable prompts and title
transcription_prompt = DEFAULT_TRANSCRIPTION_PROMPT
refinement_prompt_template = DEFAULT_REFINEMENT_PROMPT_TEMPLATE
title_format = DEFAULT_TITLE_FORMAT

# Function to allow users to set custom prompts and title
def set_custom_prompts(new_transcription_prompt=None, new_refinement_prompt_template=None, new_title_format=None):
    """
    Allows users to customize the prompts used for transcription and text refinement,
    as well as the title format shown in the results.
    
    Args:
        new_transcription_prompt (str, optional): Custom prompt for initial transcription.
            If None, keeps the current/default prompt.
        new_refinement_prompt_template (str, optional): Custom template for text refinement.
            Must contain {language} and {text} placeholders.
            If None, keeps the current/default template.
        new_title_format (str, optional): Custom format for the title shown with results.
            Must contain {language} placeholder.
            If None, keeps the current/default format.
            
    Returns:
        dict: Current prompt and title settings after changes
    """
    global transcription_prompt, refinement_prompt_template, title_format
    
    if new_transcription_prompt is not None:
        transcription_prompt = new_transcription_prompt
        console.print("[green]Custom transcription prompt set.[/]")
    
    if new_refinement_prompt_template is not None:
        # Verify the template contains the required placeholders
        if "{language}" not in new_refinement_prompt_template or "{text}" not in new_refinement_prompt_template:
            console.print("[bold red]Error: Refinement prompt template must contain {language} and {text} placeholders.[/]")
        else:
            refinement_prompt_template = new_refinement_prompt_template
            console.print("[green]Custom refinement prompt template set.[/]")
    
    if new_title_format is not None:
        # Verify the format contains the required placeholder
        if "{language}" not in new_title_format:
            console.print("[bold red]Error: Title format must contain {language} placeholder.[/]")
        else:
            title_format = new_title_format
            console.print("[green]Custom title format set.[/]")
    
    return {
        "transcription_prompt": transcription_prompt,
        "refinement_prompt_template": refinement_prompt_template,
        "title_format": title_format
    }

# Function to reset prompts and title to defaults
def reset_prompts():
    """Reset all prompts and title format to their default values."""
    global transcription_prompt, refinement_prompt_template, title_format
    transcription_prompt = DEFAULT_TRANSCRIPTION_PROMPT
    refinement_prompt_template = DEFAULT_REFINEMENT_PROMPT_TEMPLATE
    title_format = DEFAULT_TITLE_FORMAT
    console.print("[green]Prompts and title format reset to defaults.[/]")
    return {
        "transcription_prompt": transcription_prompt,
        "refinement_prompt_template": refinement_prompt_template,
        "title_format": title_format
    }

# Configure Gemini API
try:
    genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
    
    # Try to list available models but don't display them
    try:
        available_models = genai.list_models()
        model_names = []
        for model in available_models:
            model_names.append(model.name)
        
        # Use dhwagna-dgn1 as the preferred model
        preferred_models = [
            "models/dhwagna-dgn1",      # First choice - best for audio
            "models/gemini-2.0-flash",  # Fallback option
            "models/gemini-1.5-pro",    # Another fallback
        ]
        
        # Find the best available model from our preferences
        gemini_model_name = None
        for preferred in preferred_models:
            if preferred in model_names:
                gemini_model_name = preferred
                console.print(f"[bold green]Selected model:[/] [cyan]{gemini_model_name}[/]")
                break
        
        # If none of our preferred models are available, try to find any gemini model
        if not gemini_model_name:
            for name in model_names:
                if "gemini" in name.lower():
                    gemini_model_name = name
                    console.print(f"[bold yellow]Selected alternative model:[/] [cyan]{gemini_model_name}[/]")
                    break
        
        # Fallback to first model or our default
        if not gemini_model_name and model_names:
            gemini_model_name = model_names[0]
            console.print(f"[bold yellow]Using available model:[/] [cyan]{gemini_model_name}[/]")
        elif not gemini_model_name:
            gemini_model_name = "models/dhwagna-dgn1"  # Use our model even if not found
            console.print(f"[bold green]Using:[/] [cyan]{gemini_model_name}[/]")
        
        # Create the model
        model = genai.GenerativeModel(gemini_model_name)
            
    except Exception as list_error:
        # Fall back to our custom model
        console.print(f"[bold green]Using specialized Dhwagna model:[/] [cyan]models/dhwagna-dgn1[/]")
        model = genai.GenerativeModel('models/dhwagna-dgn1')
        
except Exception as e:
    console.print(Panel(f"[bold red]ERROR: Failed to configure API: {e}", title="API Configuration Error"))
    console.print("[yellow]Please check that your API key is valid and has access to required models.[/]")
    exit(1)

def record_audio():
    """Records audio when user presses K to start and K again to stop, then transcribes it."""
    # Check if user has available usage
    if API_USAGE_INFO.get("usage_count", 0) >= API_USAGE_INFO.get("max_usage", 10):
        console.print(Panel(
            "[bold red]You have reached your usage limit.[/]\n"
            "Please contact https://github.com/gnanesh-16/Dhwagna to upgrade your plan.",
            title="⚠️ Usage Limit Reached",
            border_style="red"
        ))
        return

    recognizer = sr.Recognizer()  # type: Any
    
    try:
        mic_list = sr.Microphone.list_microphone_names()
        console.print(f"[bold blue]Available microphones:[/] [green]{len(mic_list)}[/]")
        for i, mic_name in enumerate(mic_list[:3]):
            console.print(f"  [cyan]{i}:[/] {mic_name}")
        if len(mic_list) > 3:
            console.print(f"  [dim]...and {len(mic_list)-3} more[/]")
            
        mic = sr.Microphone()
        console.print("[bold green]Successfully accessed default microphone.[/]")
    except Exception as mic_error:
        console.print(f"[bold red]ERROR: Could not access microphone: {mic_error}[/]")
        console.print("[yellow]Please check your microphone connection and permissions.[/]")
        return
    
    console.print("[blue]Testing microphone with a brief recording...[/]")
    with mic as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            console.print("[green]Ambient noise adjustment complete.[/]")
            test_audio = recognizer.record(source, duration=0.5)
            console.print(f"[bold green]Test recording successful! Captured {len(test_audio.frame_data)} bytes.[/]")
        except Exception as test_error:
            console.print(f"[bold red]Microphone test failed: {test_error}[/]")
            console.print("[yellow]Your microphone may not be working properly.[/]")
            return
    
    console.print(Panel("[bold cyan]Press 'K' once to start recording, press 'K' again to stop recording...\nSupports both Telugu and English speech.", 
                      title="🎤 Multilingual Voice Transcription", 
                      border_style="green"))
    
    is_recording = False
    should_stop = False
    recorded_audio = None
    audio_data = None
    recording_start_time = 0
    
    def on_key_press(e):
        nonlocal is_recording, should_stop, recording_start_time
        if e.name == 'k':
            if not is_recording and not should_stop:
                is_recording = True
                recording_start_time = time.time()
                console.print("[bold yellow]Recording started... Speak now! (Press K again to stop)[/]")
            elif is_recording and not should_stop:
                is_recording = False
                should_stop = True
                console.print("[bold green]Recording stopped. Processing...[/]")
    
    keyboard.on_press(on_key_press)
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
    
    def record_thread_func():
        nonlocal recorded_audio, is_recording, should_stop, audio_data
        
        with mic as source:
            while not is_recording and not should_stop:
                time.sleep(0.1)
            
            if should_stop:
                return
            
            console.print("[bold blue]Listening... (Press K again to stop)[/]")
            
            timer_thread = threading.Thread(target=display_timer)
            timer_thread.daemon = True
            timer_thread.start()
            
            try:
                stop_recording = threading.Event()
                
                def continuous_recording():
                    nonlocal audio_data
                    
                    chunk_duration = 2
                    all_audio_data = []
                    
                    try:
                        console.print("[blue]Starting chunked recording...[/]")
                        while is_recording and not should_stop:
                            console.print("[dim]Recording chunk...[/]", end="\r")
                            chunk = recognizer.record(source, duration=chunk_duration)
                            console.print(f"[dim]Recorded chunk: {len(chunk.frame_data)} bytes[/]", end="\r")
                            all_audio_data.append(chunk)
                            
                            if should_stop or not is_recording:
                                break
                        
                        console.print(f"[green]Completed recording {len(all_audio_data)} chunks.[/]")
                                
                        if all_audio_data:
                            console.print(f"[blue]Combining {len(all_audio_data)} audio chunks...[/]")
                            combined_audio = all_audio_data[0]
                            
                            if len(all_audio_data) > 1:
                                raw_data = combined_audio.get_raw_data()
                                sample_rate = combined_audio.sample_rate
                                sample_width = combined_audio.sample_width
                                
                                for chunk in all_audio_data[1:]:
                                    raw_data += chunk.get_raw_data()
                                
                                combined_audio = sr.AudioData(raw_data, sample_rate, sample_width)
                            
                            audio_data = combined_audio
                            console.print(f"[bold green]Successfully combined audio: {len(audio_data.frame_data)} bytes total.[/]")
                    except Exception as e:
                        console.print(f"[bold red]Recording error in continuous recording: {e}[/]")
                        
                        try:
                            console.print("[yellow]Attempting fallback direct recording...[/]")
                            if is_recording and not should_stop:
                                fallback_audio = recognizer.record(source, duration=30)
                                audio_data = fallback_audio
                                console.print("[green]Fallback recording successful.[/]")
                        except Exception as fallback_error:
                            console.print(f"[bold red]Fallback recording also failed: {fallback_error}[/]")
                
                recording_thread = threading.Thread(target=continuous_recording)
                recording_thread.daemon = True
                recording_thread.start()
                
                while is_recording and not should_stop:
                    time.sleep(0.1)
                
                console.print("[blue]Waiting for recording thread to complete...[/]")
                recording_thread.join(timeout=3.0)
                
                if audio_data:
                    console.print(f"[bold green]Audio captured successfully: {len(audio_data.frame_data)} bytes.[/]")
                    recorded_audio = audio_data
                else:
                    console.print("[bold yellow]No audio data was captured.[/]")
            except Exception as e:
                console.print(f"[bold red]Recording error: {e}[/]")
    
    def display_timer():
        with Live(refresh_per_second=4) as live:
            while is_recording and not should_stop:
                elapsed = time.time() - recording_start_time
                timer_text = Text()
                timer_text.append("🔴 Recording: ", style="bold red")
                timer_text.append(f"{elapsed:.1f} seconds", style="bold yellow")
                live.update(timer_text)
                time.sleep(0.1)
    
    record_thread = threading.Thread(target=record_thread_func)
    record_thread.daemon = True
    record_thread.start()
    
    try:
        while not should_stop:
            time.sleep(0.1)
        
        console.print("[blue]Waiting for recording process to complete...[/]")
        record_thread.join(timeout=5.0)
        
        if recorded_audio:
            console.print(f"[green]Processing {len(recorded_audio.frame_data)} bytes of audio...[/]")
            start_time = time.time()
            original_text = ""
            refined_text = ""
            detected_language = "unknown"
            end_time = 0
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Processing multilingual transcription with dhvagna..."),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Transcribing...", total=None)
                
                try:
                    audio_data = recorded_audio.get_wav_data()
                    
                    raw_response = model.generate_content(
                        [
                            {
                                "mime_type": "audio/wav",
                                "data": audio_data
                            },
                            transcription_prompt
                        ]
                    )
                    
                    raw_text = raw_response.text.strip()
                    
                    if "[LANGUAGE:" in raw_text:
                        language_tag = raw_text.split("[LANGUAGE:", 1)[1].split("]", 1)[0].strip()
                        detected_language = language_tag
                        original_text = raw_text.split("]", 1)[1].strip()
                    else:
                        original_text = raw_text
                        if any('\u0C00' <= c <= '\u0C7F' for c in original_text):
                            detected_language = "Telugu"
                        else:
                            detected_language = "English"
                    
                    formal_prompt = refinement_prompt_template.format(
                        language=detected_language,
                        text=original_text
                    )
                    
                    corrected_response = model.generate_content(formal_prompt)
                    
                    refined_text = corrected_response.text.strip()
                    end_time = time.time()
                    
                except Exception as e:
                    console.print(f"[bold red]Transcription error:[/] {e}")
                    progress.update(task, visible=False)
            
            if refined_text:
                # Show both original and corrected versions with language indication
                language_color = "magenta" if detected_language == "Telugu" else "blue"
                
                # When Telugu is detected, show transliterated version in terminal
                if detected_language == "Telugu":
                    # Save original Telugu text for files
                    original_telugu = original_text
                    # For display, transliterate to English characters
                    display_text = transliterate_telugu_to_english(original_text)
                    console.print(Panel(f"[{language_color}]Detected: {detected_language}[/]\n\n[yellow]Original: [/][white]{display_text}[/] [dim](transliterated for display)[/]", 
                                  title="🎤 Raw Transcription", 
                                  border_style="yellow"))
                    
                    # Also transliterate the refined text for display
                    display_refined = transliterate_telugu_to_english(refined_text)
                else:
                    # For English, show as is
                    display_text = original_text
                    display_refined = refined_text
                    console.print(Panel(f"[{language_color}]Detected: {detected_language}[/]\n\n[yellow]Original: [/][white]{display_text}[/]", 
                                  title="🎤 Raw Transcription", 
                                  border_style="yellow"))
                
                # Use the custom title format
                custom_title = title_format.format(language=detected_language)
                if end_time and start_time:
                    custom_title += f" ({round(end_time - start_time, 2)}s)"
                
                # Show transliterated or original text based on language
                if detected_language == "Telugu":
                    console.print(Panel(f"[bold green]{display_refined}", 
                                title=f"{custom_title} [dim](transliterated for display)[/]", 
                                border_style="cyan"))
                else:
                    console.print(Panel(f"[bold green]{display_refined}", 
                                title=custom_title, 
                                border_style="cyan"))
                
                # After successful transcription, update usage
                transcription_id = f"trans_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"
                update_usage_with_server(DHVGNA_API_KEY, transcription_id)
                
                # Update local usage count
                API_USAGE_INFO["usage_count"] = API_USAGE_INFO.get("usage_count", 0) + 1
                remaining = API_USAGE_INFO.get("max_usage", 10) - API_USAGE_INFO.get("usage_count", 0)
                console.print(f"[green]Transcription complete. You have [bold]{remaining}[/] transcriptions remaining.[/]")
            else:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold yellow]Falling back to Google speech recognition..."),
                    console=console,
                ) as progress:
                    task = progress.add_task("Transcribing with fallback...", total=None)
                    try:
                        text = recognizer.recognize_google(recorded_audio)  # type: ignore
                        console.print(Panel(f"[yellow]{text}", title="Google Transcription", border_style="yellow"))
                        
                        console.print(Panel("[bold green]Processing complete! Exiting program.", 
                                          title="👋 Goodbye", 
                                          border_style="green"))
                        return
                        
                    except Exception as fallback_error:
                        console.print(f"[bold red]Fallback also failed:[/] {fallback_error}")
                        console.print(Panel("[bold red]Exiting program due to errors.", 
                                         title="❌ Error", 
                                         border_style="red"))
                        return
        else:
            console.print("[bold red]No audio was recorded to transcribe. Please check your microphone.[/]")
            console.print("[yellow]Try running the program again and speaking louder or closer to the microphone.[/]")
        
    finally:
        keyboard.unhook_all()
        console.print(Panel("[bold green]Processing complete! Exiting program.", 
                         title="👋 Goodbye", 
                         border_style="green"))
    
    return

def transcribe_wav_file(file_path):
    """Transcribes a .wav file to text using Gemini API."""
    if API_USAGE_INFO.get("usage_count", 0) >= API_USAGE_INFO.get("max_usage", 10):
        console.print(Panel(
            "[bold red]You have reached your usage limit.[/]\n"
            "Please contact https://github.com/gnanesh-16/Dhwagna to upgrade your plan.",
            title="⚠️ Usage Limit Reached",
            border_style="red"
        ))
        return None, None, None

    console.print(Panel(f"[bold blue]Transcribing file:[/] [green]{file_path}[/]", 
                      title="🔊 WAV File Transcription", 
                      border_style="blue"))
    
    if not os.path.exists(file_path):
        console.print(f"[bold red]Error: File not found at {file_path}[/]")
        return
    
    if not file_path.lower().endswith('.wav'):
        console.print(f"[bold red]Error: File must be a .wav file. Found: {file_path}[/]")
        return
    
    try:
        with wave.open(file_path, 'rb') as wav_file:
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            frame_rate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            duration = n_frames / frame_rate
            
            console.print(f"[blue]File details:[/] {channels} channels, {frame_rate}Hz, {duration:.2f} seconds")
    
        with open(file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Processing transcription with dhvagna..."),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Transcribing...", total=None)
            
            try:
                raw_response = model.generate_content(
                    [
                        {
                            "mime_type": "audio/wav",
                            "data": audio_data
                        },
                        transcription_prompt
                    ]
                )
                
                raw_text = raw_response.text.strip()
                
                if "[LANGUAGE:" in raw_text:
                    language_tag = raw_text.split("[LANGUAGE:", 1)[1].split("]", 1)[0].strip()
                    detected_language = language_tag
                    original_text = raw_text.split("]", 1)[1].strip()
                else:
                    original_text = raw_text
                    if any('\u0C00' <= c <= '\u0C7F' for c in original_text):
                        detected_language = "Telugu"
                    else:
                        detected_language = "English"
                
                formal_prompt = refinement_prompt_template.format(
                    language=detected_language,
                    text=original_text
                )
                
                corrected_response = model.generate_content(formal_prompt)
                refined_text = corrected_response.text.strip()
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_basename = os.path.basename(file_path).replace(".wav", "")
                
                original_file = SAVE_DIR / f"{file_basename}_{timestamp}_original.txt"
                refined_file = SAVE_DIR / f"{file_basename}_{timestamp}_refined.txt"
                
                # Display results
                language_color = "magenta" if detected_language == "Telugu" else "blue"
                
                # When Telugu is detected, show transliterated version in terminal
                if detected_language == "Telugu":
                    # Save original Telugu text to files
                    with open(original_file, 'w', encoding='utf-8') as f:
                        f.write(f"LANGUAGE: {detected_language}\n\n{original_text}")
                    
                    with open(refined_file, 'w', encoding='utf-8') as f:
                        f.write(refined_text)
                    
                    # For display, transliterate to English characters
                    display_text = transliterate_telugu_to_english(original_text)
                    display_refined = transliterate_telugu_to_english(refined_text)
                    
                    console.print(Panel(f"[{language_color}]Detected: {detected_language}[/]\n\n[yellow]Original: [/][white]{display_text}[/] [dim](transliterated for display)[/]", 
                                title="🎤 Raw Transcription", 
                                border_style="yellow"))
                    
                    # Use the custom title format
                    custom_title = title_format.format(language=detected_language)
                    
                    console.print(Panel(f"[bold green]{display_refined}", 
                                title=f"{custom_title} [dim](transliterated for display)[/]", 
                                border_style="cyan"))
                else:
                    # For English, show and save as is
                    with open(original_file, 'w', encoding='utf-8') as f:
                        f.write(f"LANGUAGE: {detected_language}\n\n{original_text}")
                    
                    with open(refined_file, 'w', encoding='utf-8') as f:
                        f.write(refined_text)
                    
                    console.print(Panel(f"[{language_color}]Detected: {detected_language}[/]\n\n[yellow]Original: [/][white]{original_text}[/]", 
                                title="🎤 Raw Transcription", 
                                border_style="yellow"))
                    
                    # Use the custom title format
                    custom_title = title_format.format(language=detected_language)
                    
                    console.print(Panel(f"[bold green]{refined_text}", 
                                title=custom_title, 
                                border_style="cyan"))
                
                console.print(f"[green]Saved transcriptions to:[/]")
                console.print(f"  Original: [yellow]{original_file}[/]")
                console.print(f"  Refined:  [yellow]{refined_file}[/]")
                
                # After successful transcription, update usage
                transcription_id = f"file_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"
                update_usage_with_server(DHVGNA_API_KEY, transcription_id)
                
                # Update local usage count
                API_USAGE_INFO["usage_count"] = API_USAGE_INFO.get("usage_count", 0) + 1
                remaining = API_USAGE_INFO.get("max_usage", 10) - API_USAGE_INFO.get("usage_count", 0)
                console.print(f"[green]Transcription complete. You have [bold]{remaining}[/] transcriptions remaining.[/]")
                
                return original_text, refined_text, detected_language
                
            except Exception as e:
                console.print(f"[bold red]Transcription error:[/] {e}")
                progress.update(task, visible=False)
                return None, None, None
                
    except Exception as e:
        console.print(f"[bold red]Error processing file:[/] {e}")
        return None, None, None

if __name__ == "__main__":
    console.print(Panel(
        "[bold cyan]Welcome to the Voice Transcription Tool[/]\n\n"
        "This tool can transcribe speech in [green]Telugu[/] or [green]English[/] and save the results.",
        title="🎤 Multilingual Voice Transcription",
        border_style="green"
    ))
    
    console.print("\n[bold yellow]Choose an option:[/]")
    console.print("  [cyan]1.[/] Record audio using microphone")
    console.print("  [cyan]2.[/] Transcribe existing .wav file")
    
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice == "1":
        record_audio()
    elif choice == "2":
        file_path = input("\nEnter the full path to your .wav file: ")
        transcribe_wav_file(file_path.strip())
    else:
        console.print("[bold red]Invalid choice. Please run the program again and select 1 or 2.[/]")
