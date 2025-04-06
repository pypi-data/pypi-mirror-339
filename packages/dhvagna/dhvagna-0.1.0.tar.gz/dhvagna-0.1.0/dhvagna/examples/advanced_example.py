"""
Advanced example showcasing all Dhvagna features together.

This example demonstrates:
1. API key validation and setup
2. Multiple customization profiles (Academic, Medical, Legal)
3. Custom title formats
4. Profile switching and resetting
5. Practical transcription scenarios
"""

import os
from rich.console import Console
from rich.panel import Panel
from dhvagna import (
    record_audio, 
    transcribe_wav_file, 
    set_custom_prompts,
    reset_prompts,
    DEFAULT_TRANSCRIPTION_PROMPT,
    DEFAULT_REFINEMENT_PROMPT_TEMPLATE,
    DEFAULT_TITLE_FORMAT
)

# Create Rich console for beautiful output
console = Console()

class TranscriptionProfile:
    """Represents a complete transcription configuration profile"""
    def __init__(self, name, prompt, template, title_format, description):
        self.name = name
        self.prompt = prompt
        self.template = template
        self.title_format = title_format
        self.description = description
    
    def apply(self):
        """Apply this profile's settings"""
        set_custom_prompts(
            new_transcription_prompt=self.prompt,
            new_refinement_prompt_template=self.template,
            new_title_format=self.title_format
        )

# Define specialized transcription profiles
PROFILES = {
    "academic": TranscriptionProfile(
        name="Academic",
        prompt="""
Transcribe this academic content with high precision. The speech may be in Telugu or English.
Identify the language and indicate it with [LANGUAGE: Telugu] or [LANGUAGE: English].
Focus on capturing:
- Technical and academic terminology
- Research methodologies and findings
- Statistical data and measurements
- Citations and references
- Mathematical equations and formulas
""",
        template="""
Here is an academic transcription in {language}: "{text}"

Please refine this content while:
1. Maintaining academic rigor and technical accuracy
2. Preserving all citations and references
3. Structuring into proper academic sections
4. Formatting mathematical notations correctly
5. Using formal academic language appropriate for {language}

Return the refined academic text in {language}.
""",
        title_format="🎓 Academic {language} Transcript",
        description="Optimized for research presentations, lectures, and academic discussions"
    ),
    
    "medical": TranscriptionProfile(
        name="Medical",
        prompt="""
Transcribe this medical content with precision. The speech may be in Telugu or English.
Identify the language and indicate it with [LANGUAGE: Telugu] or [LANGUAGE: English].
Focus on capturing:
- Medical terminology and procedures
- Patient symptoms and conditions
- Treatment plans and medications
- Vital signs and measurements
- Healthcare instructions
""",
        template="""
Here is a medical transcription in {language}: "{text}"

Please refine this content while:
1. Maintaining all medical terms exactly as spoken
2. Organizing into clear clinical sections
3. Using standard medical abbreviations
4. Preserving all numerical values
5. Using professional medical language in {language}

Return the refined medical text in {language}.
""",
        title_format="⚕️ Medical {language} Report",
        description="Optimized for clinical notes, patient consultations, and medical dictations"
    ),
    
    "legal": TranscriptionProfile(
        name="Legal",
        prompt="""
Transcribe this legal content with precision. The speech may be in Telugu or English.
Identify the language and indicate it with [LANGUAGE: Telugu] or [LANGUAGE: English].
Focus on capturing:
- Legal terminology and citations
- Case references and precedents
- Court proceedings and testimonies
- Legal arguments and reasoning
- Procedural details
""",
        template="""
Here is a legal transcription in {language}: "{text}"

Please refine this content while:
1. Maintaining all legal terms and references
2. Using proper legal formatting
3. Preserving case citations and precedents
4. Structuring arguments logically
5. Using formal legal language in {language}

Return the refined legal text in {language}.
""",
        title_format="⚖️ Legal {language} Transcript",
        description="Optimized for court proceedings, legal consultations, and case documentation"
    )
}

def check_api_key():
    """Verify API key is properly set"""
    api_key = os.getenv('DHVGNA_API_KEY')
    if not api_key:
        console.print(Panel(
            "[bold red]ERROR: DHVGNA_API_KEY environment variable not found![/]\n\n"
            "To set your API key:\n"
            "1. Get your API key from: [link]https://github.com/gnanesh-16/Dhwagna[/link]\n\n"
            "2. Set it as an environment variable:\n"
            "   [yellow]Windows (Command Prompt):[/]\n"
            "   set DHVGNA_API_KEY=your_api_key_here\n\n"
            "   [yellow]Windows (PowerShell):[/]\n"
            "   $env:DHVGNA_API_KEY=\"your_api_key_here\"\n\n"
            "   [yellow]Linux/MacOS:[/]\n"
            "   export DHVGNA_API_KEY=\"your_api_key_here\"\n\n"
            "Or create a [bold].env[/] file in your project directory with:\n"
            "DHVGNA_API_KEY=your_api_key_here",
            title="🔑 API Key Required",
            border_style="red"
        ))
        return False
    return True

def show_profiles():
    """Display available transcription profiles"""
    console.print("\n[bold cyan]Available Transcription Profiles:[/]")
    for key, profile in PROFILES.items():
        console.print(f"\n[bold green]{profile.name}[/] ([yellow]{key}[/])")
        console.print(f"[dim]{profile.description}[/]")

def main():
    console.print(Panel(
        "[bold cyan]Welcome to the Advanced Dhvagna Example![/]\n\n"
        "This example demonstrates all features including:\n"
        "• Specialized transcription profiles\n"
        "• Custom formatting options\n"
        "• Multiple use cases\n"
        "• Profile switching",
        title="🚀 Advanced Features Demo",
        border_style="green"
    ))
    
    # First, verify API key is set
    if not check_api_key():
        return
    
    while True:
        console.print("\n[bold cyan]Choose an option:[/]")
        console.print("1. View available profiles")
        console.print("2. Apply a profile and record")
        console.print("3. Apply a profile and transcribe file")
        console.print("4. Reset to default settings")
        console.print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            show_profiles()
            
        elif choice == "2" or choice == "3":
            show_profiles()
            profile_key = input("\nEnter profile key (academic/medical/legal): ").lower()
            
            if profile_key in PROFILES:
                profile = PROFILES[profile_key]
                profile.apply()
                console.print(f"\n[green]✓[/] Applied [bold]{profile.name}[/] profile!")
                
                if choice == "2":
                    console.print("\nPress 'K' to start recording")
                    console.print("Press 'K' again to stop")
                    record_audio()
                else:
                    file_path = input("\nEnter the path to your WAV file: ")
                    if file_path.strip():
                        result = transcribe_wav_file(file_path.strip())
                        if result:
                            original, refined, language = result
                            console.print(f"\n[green]✓[/] Transcription successful!")
                            console.print(f"[blue]Detected language:[/] {language}")
            else:
                console.print("[red]Invalid profile key. Please try again.[/]")
        
        elif choice == "4":
            reset_prompts()
            console.print("\n[green]✓[/] Reset to default settings!")
        
        elif choice == "5":
            console.print(Panel(
                "[bold green]Thank you for trying the advanced features![/]\n"
                "Visit [link]https://github.com/gnanesh-16/Dhwagna[/link] for more information.",
                title="👋 Goodbye",
                border_style="cyan"
            ))
            break
        
        else:
            console.print("[red]Invalid choice. Please try again.[/]")

if __name__ == "__main__":
    main()