"""
Example showing how to customize prompts and settings in Dhvagna.

This example demonstrates:
1. Setting up your API key
2. Viewing and customizing transcription prompts
3. Customizing refinement templates
4. Customizing title formats
"""

import os
from dhvagna import (
    record_audio, 
    transcribe_wav_file, 
    set_custom_prompts,
    reset_prompts,
    DEFAULT_TRANSCRIPTION_PROMPT,
    DEFAULT_REFINEMENT_PROMPT_TEMPLATE,
    DEFAULT_TITLE_FORMAT
)

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

def show_current_settings():
    """Display all current prompt and title settings"""
    print("\n=== Current Transcription Prompt ===")
    print("-" * 40)
    print(DEFAULT_TRANSCRIPTION_PROMPT)
    
    print("\n=== Current Refinement Template ===")
    print("-" * 40)
    print(DEFAULT_REFINEMENT_PROMPT_TEMPLATE)
    
    print("\n=== Current Title Format ===")
    print("-" * 40)
    print(DEFAULT_TITLE_FORMAT)

def main():
    print("===== Dhvagna Customization Example =====")
    
    # First, verify API key is set
    if not check_api_key():
        return
    
    # Show current settings
    print("\nStep 1: Current default settings")
    show_current_settings()
    
    # Let's customize for technical documentation
    print("\nStep 2: Setting up technical documentation transcription")
    
    technical_prompt = """
Transcribe this technical content. The speech may be in Telugu or English.
Identify the language and indicate it with [LANGUAGE: Telugu] or [LANGUAGE: English].
Focus on capturing:
- Code snippets and technical terms
- API references and documentation
- Software architecture descriptions
- Implementation details
- Technical specifications
"""
    
    technical_template = """
Here is a technical transcription in {language}: "{text}"

Please refine this text while:
1. Maintaining all technical terms and code references exactly
2. Using proper technical writing style
3. Organizing content logically
4. Adding appropriate technical formatting
5. Preserving all technical specifications

Return the refined technical documentation in {language}.
"""
    
    technical_title = "💻 Technical {language} Documentation"
    
    # Set all custom options
    set_custom_prompts(
        new_transcription_prompt=technical_prompt,
        new_refinement_prompt_template=technical_template,
        new_title_format=technical_title
    )
    print("\n✅ Technical documentation settings configured!")
    
    # Try the custom settings
    print("\nStep 3: Test the technical documentation settings")
    print("\nOptions:")
    print("1. Record technical documentation")
    print("2. Transcribe technical recording")
    print("3. Reset to default settings")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        print("\nPress 'K' to start recording technical documentation")
        print("Press 'K' again to stop")
        record_audio()
        
    elif choice == "2":
        file_path = input("\nEnter the path to your technical WAV file: ")
        if file_path.strip():
            result = transcribe_wav_file(file_path.strip())
            if result:
                original, refined, language = result
                print(f"\nTranscription successful!")
                print(f"Detected language: {language}")
    
    elif choice == "3":
        # Reset everything to defaults
        reset_prompts()
        print("\n✅ All settings reset to defaults!")
        print("Run the example again to try different settings.")
    
    else:
        print("\nExiting the customization example.")

if __name__ == "__main__":
    main()