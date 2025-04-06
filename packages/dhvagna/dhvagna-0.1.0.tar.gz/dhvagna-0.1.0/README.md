# Dhvagna

A powerful multilingual voice transcription tool that supports both Telugu and English speech, powered by Google's Gemini AI. Dhvagna makes it easy to transcribe speech from both recordings and live microphone input, with support for customizable prompts and formatting.

## 🔑 API Key Required

To use Dhvagna, you need a valid API key with the following requirements:

1. **Valid API key format**: All API keys must start with `dk-` followed by a unique alphanumeric string
2. **Limited usage**: Each API key is limited to 100 transcriptions
3. **Verification**: API keys are verified with our servers

### How to obtain an API key:

Visit [https://github.com/gnanesh-16/Dhwagna](https://github.com/gnanesh-16/Dhwagna) to register and receive your API key.

### Setting up your API key:

```bash
# On Windows (Command Prompt)
set DHVGNA_API_KEY=dk-your_unique_key_here

# On Windows (PowerShell)
$env:DHVGNA_API_KEY="dk-your_unique_key_here"

# On Linux/MacOS
export DHVGNA_API_KEY="dk-your_unique_key_here"
```

Alternatively, you can create a `.env` file in your project directory:
```
DHVGNA_API_KEY=dk-your_unique_key_here
```

### Usage tracking:

The package tracks usage against your API key quota. You'll receive notifications about:
- Remaining transcriptions at startup
- Updated count after each transcription
- Errors when your limit is reached

## 🌟 Features

- **Multilingual Support**: Transcribe both Telugu and English speech with high accuracy
- **Multiple Input Methods**:
  - Live microphone recording with simple keyboard controls
  - Process existing WAV audio files
- **Smart Language Detection**: Automatically detects whether the speech is in Telugu or English
- **Advanced Processing**:
  - Raw transcription preserving original speech patterns
  - Refined output with improved grammar and formatting
  - Customizable prompts for different use cases
- **Flexible Output**:
  - Customizable title formatting
  - Both raw and refined transcriptions
  - Automatic file saving with timestamps
- **Easy-to-Use Interface**:
  - Simple keyboard controls ('K' to start/stop recording)
  - Progress indicators and timers
  - Beautiful console output with color coding
- **API Key Management**:
  - Secure API key validation
  - Usage tracking with quota limits
  - Graceful error handling for exceeded quotas

## 📦 Installation

```bash
pip install dhvagna
```

## 🚀 Quick Start

### Basic Usage

```python
from dhvagna import record_audio, transcribe_wav_file

# Make sure you've set your DHVGNA_API_KEY environment variable first!
# The key must start with 'dk-' and be registered with our service

# Record and transcribe from microphone
record_audio()

# Or transcribe an existing WAV file
result = transcribe_wav_file("path/to/audio.wav")
```

### Advanced Usage with Customization

```python
from dhvagna import set_custom_prompts, record_audio

# Customize for academic transcription
academic_prompt = """
Transcribe this academic content. The speech may be in Telugu or English.
Identify the language and indicate it with [LANGUAGE: Telugu] or [LANGUAGE: English].
Focus on:
- Technical terminology
- Citations and references
- Research methodologies
"""

academic_title = "📚 Academic {language} Transcription"

# Set custom prompts and title
set_custom_prompts(
    new_transcription_prompt=academic_prompt,
    new_title_format=academic_title
)

# Record with academic settings
record_audio()
```

## 🛠️ API Key Troubleshooting

If you encounter API key issues:

1. **Invalid key format**: Ensure your key starts with `dk-`
2. **Verification failure**: Check that your key is registered in our system
3. **Usage limit exceeded**: Contact us to upgrade your plan if you need more than 100 transcriptions
4. **Server connection issues**: The package will run in offline mode with limited functionality if it can't connect to our servers

## 🎯 Use Cases

1. **Academic Research**
   - Transcribe research presentations
   - Document academic discussions
   - Record seminar content

2. **Medical Transcription**
   - Patient consultations
   - Medical dictations
   - Clinical observations

3. **Legal Documentation**
   - Court proceedings
   - Client interviews
   - Legal consultations

4. **General Purpose**
   - Meeting minutes
   - Interviews
   - Personal notes

## 🛠️ Customization Options

### 1. Transcription Prompts
Customize how the initial transcription is processed:
```python
set_custom_prompts(new_transcription_prompt="Your custom prompt here")
```

### 2. Refinement Templates
Control how the transcription is refined:
```python
template = """
Refine this {language} text: "{text}"
Include your refinement instructions here.
"""
set_custom_prompts(new_refinement_prompt_template=template)
```

### 3. Title Formatting
Customize the display title:
```python
set_custom_prompts(new_title_format="✨ Custom {language} Title")
```

## 📝 Requirements

- Python 3.7+
- Microphone (for recording features)
- Internet connection (for AI processing and API key verification)
- WAV file support
- Valid Dhvagna API key

## 🔧 Technical Details

- Uses Google's Gemini AI for advanced language processing
- Supports WAV audio format
- Real-time audio processing
- Automatic language detection
- Multi-threaded recording handling
- Smart error recovery and fallback options
- Secure API key validation and usage tracking

## 🌐 Links

- GitHub: [https://github.com/gnanesh-16/Dhwagna](https://github.com/gnanesh-16/Dhwagna)
- Author: Gnox79

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.