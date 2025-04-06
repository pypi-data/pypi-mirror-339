"""
Basic example showing how to use the Dhvagna package.

This example demonstrates:
1. Setting up your API key
2. Basic recording and transcription
3. Error handling for missing API key
"""

import os
from dhvagna import record_audio, transcribe_wav_file

def check_api_key():
    """Check if API key is properly set"""
    api_key = os.getenv('DHVGNA_API_KEY')
    if not api_key:
        print("\n❌ Error: DHVGNA_API_KEY environment variable not found!")
        print("\nTo set your API key:")
        print("1. Get your API key from: https://github.com/gnanesh-16/Dhwagna")
        print("\n2. Set it as an environment variable:")
        print("   Windows (Command Prompt):")
        print("   set DHVGNA_API_KEY=your_api_key_here")
        print("\n   Windows (PowerShell):")
        print('   $env:DHVGNA_API_KEY="your_api_key_here"')
        print("\n   Linux/MacOS:")
        print('   export DHVGNA_API_KEY="your_api_key_here"')
        print("\nOr create a .env file in your project directory with:")
        print("DHVGNA_API_KEY=your_api_key_here")
        return False
    return True

def main():
    print("===== Dhvagna Basic Usage Example =====")
    
    # First, verify API key is set
    if not check_api_key():
        return
    
    # Present options to user
    print("\nWhat would you like to do?")
    print("1. Record audio from microphone")
    print("2. Transcribe a WAV file")
    
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice == "1":
        print("\nPress 'K' to start recording")
        print("Press 'K' again to stop recording")
        record_audio()
        
    elif choice == "2":
        file_path = input("\nEnter the path to your WAV file: ")
        if file_path.strip():
            result = transcribe_wav_file(file_path.strip())
            if result:
                original, refined, language = result
                print(f"\nTranscription successful!")
                print(f"Detected language: {language}")
    
    else:
        print("\n❌ Invalid choice. Please run the example again and select 1 or 2.")

if __name__ == "__main__":
    main()