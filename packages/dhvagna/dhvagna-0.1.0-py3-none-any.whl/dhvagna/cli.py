import argparse
import os
from .wav import record_audio, transcribe_wav_file

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Dhvagna - Multilingual Voice Transcription Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Record command
    record_parser = subparsers.add_parser("record", help="Record audio from microphone and transcribe")
    
    # Transcribe command
    transcribe_parser = subparsers.add_parser("transcribe", help="Transcribe an existing .wav file")
    transcribe_parser.add_argument("file_path", type=str, help="Path to the .wav file to transcribe")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute the appropriate command
    if args.command == "record":
        record_audio()
    elif args.command == "transcribe":
        if not os.path.exists(args.file_path):
            print(f"Error: File not found at {args.file_path}")
            return
        if not args.file_path.lower().endswith('.wav'):
            print(f"Error: File must be a .wav file. Found: {args.file_path}")
            return
        transcribe_wav_file(args.file_path)
    else:
        # Default behavior if no command is provided
        parser.print_help()

if __name__ == "__main__":
    main()