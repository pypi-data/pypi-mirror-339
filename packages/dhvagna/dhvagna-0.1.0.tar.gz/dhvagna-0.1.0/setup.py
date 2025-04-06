from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dhvagna",
    version="0.1.0",
    author="Gnox79",
    description="A multilingual voice transcription tool for Telugu and English",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnanesh-16/Dhwagna",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=[
        "google-generativeai>=0.3.2",
        "SpeechRecognition>=3.10.0",
        "keyboard>=0.13.5",
        "gTTS>=2.4.0",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "pathlib>=1.0.1",
        "wave>=0.0.2",
        "pyaudio>=0.2.14"  # Required by SpeechRecognition for microphone access
    ],
    entry_points={
        "console_scripts": [
            "dhvagna=dhvagna.cli:main",
        ],
    },
)