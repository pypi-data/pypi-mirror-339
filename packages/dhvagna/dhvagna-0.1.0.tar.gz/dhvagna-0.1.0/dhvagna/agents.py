from .utils import record_audio, transcribe_wav_file
from .wav import set_custom_prompts, reset_prompts, DEFAULT_TRANSCRIPTION_PROMPT, DEFAULT_REFINEMENT_PROMPT_TEMPLATE

def dhvagna_agents(start: bool):
    """Main entry point for the Dhvagna package."""
    if start:
        print("Welcome to Dhvagna! Choose an option:")
        print("1. Record audio using microphone")
        print("2. Transcribe existing .wav file")
        print("3. Show default prompts")
        print("4. Customize prompts")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            record_audio()
        elif choice == "2":
            file_path = input("Enter the full path to your .wav file: ")
            transcribe_wav_file(file_path.strip())
        elif choice == "3":
            print("\n=== Default Transcription Prompt ===")
            print(DEFAULT_TRANSCRIPTION_PROMPT)
            print("\n=== Default Refinement Prompt Template ===")
            print(DEFAULT_REFINEMENT_PROMPT_TEMPLATE)
        elif choice == "4":
            customize_prompts()
        else:
            print("Invalid choice. Please run the program again and select a valid option.")

def customize_prompts():
    """Helper function to customize the prompts used by Dhvagna."""
    print("\nCustomize Prompts")
    print("=================")
    print("1. Customize transcription prompt")
    print("2. Customize refinement prompt template")
    print("3. Reset prompts to defaults")
    print("4. Back to main menu")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        print("\nCurrent transcription prompt:")
        print("-----------------------------")
        print(DEFAULT_TRANSCRIPTION_PROMPT)
        print("\nEnter your new transcription prompt (or press Enter to keep current):")
        new_prompt = input("> ").strip()
        
        if new_prompt:
            set_custom_prompts(new_transcription_prompt=new_prompt)
            print("Transcription prompt updated successfully!")
        
    elif choice == "2":
        print("\nCurrent refinement prompt template:")
        print("--------------------------------")
        print(DEFAULT_REFINEMENT_PROMPT_TEMPLATE)
        print("\nEnter your new refinement prompt template (must include {language} and {text} placeholders):")
        new_template = input("> ").strip()
        
        if new_template:
            if "{language}" in new_template and "{text}" in new_template:
                set_custom_prompts(new_refinement_prompt_template=new_template)
                print("Refinement prompt template updated successfully!")
            else:
                print("Error: Template must contain {language} and {text} placeholders.")
                
    elif choice == "3":
        reset_prompts()
        print("All prompts have been reset to defaults.")
        
    elif choice == "4":
        return
    
    else:
        print("Invalid choice.")