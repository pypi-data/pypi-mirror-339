"""
Simple example showing basic usage of Dhvagna.

This demonstrates:
1. Setting up your API key
2. Basic recording and transcription
3. Simple prompt customization
"""

import os
from dhvagna import record_audio, transcribe_wav_file, set_custom_prompts

def verify_api_key():
    """Make sure API key is set up correctly"""
    api_key = os.getenv('DHVGNA_API_KEY')
    if not api_key:
        print("\n❌ Error: DHVGNA_API_KEY not found!")
        print("\nGet your API key from:")
        print("https://github.com/gnanesh-16/Dhvagna")
        print("\nThen set it in your environment:")
        print('export DHVGNA_API_KEY="your_api_key_here"')
        return False
    if not api_key.startswith('dk'):
        print("\n❌ Error: Invalid API key format!")
        print("Dhvagna API keys must start with 'dk'")
        return False
    return True

def main():
    print("===== Dhvagna Quick Start =====")
    
    # Check API key first
    if not verify_api_key():
        return
    
    # Set up a simple custom prompt (optional)
    custom_prompt = """
Transcribe this content in Telugu or English.
Identify the language as [LANGUAGE: Telugu] or [LANGUAGE: English].
Capture the speech exactly as spoken.
"""
    set_custom_prompts(new_transcription_prompt=custom_prompt)
    
    # Show options
    print("\nWhat would you like to do?")
    print("1. Record new audio")
    print("2. Transcribe WAV file")
    
    choice = input("\nChoice (1 or 2): ")
    
    if choice == "1":
        print("\nRecording:")
        print("1. Press 'K' to start")
        print("2. Speak your content")
        print("3. Press 'K' again to stop")
        record_audio()
    
    elif choice == "2":
        file_path = input("\nEnter WAV file path: ")
        if file_path.strip():
            print("\nTranscribing file...")
            transcribe_wav_file(file_path.strip())
    
    else:
        print("\n❌ Invalid choice")

if __name__ == "__main__":
    main()