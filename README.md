# Batch Audio Synthesis & Pipeline Automation

An automated audio generation and batch processing system built with Streamlit, Python, and ElevenLabs API to convert structured text and literary datasets into high-fidelity voice assets.

## Features
- Automated multi-file processing from Excel sheets and Word documents
- Integration with ElevenLabs API for multi-voice allocation and credit-safe synthesis
- Audio file extraction, validation, and batch compression into zip archives

## Tech Stack
- Python
- Streamlit
- ElevenLabs API
- Pandas & OpenPyXL

## Setup & Running
1. Clone the repository:
   ```bash
   git clone [https://github.com/deepthik575-lgtm/audio-synthesis-pipeline.git](https://github.com/deepthik575-lgtm/audio-synthesis-pipeline.git)
   cd audio-synthesis-pipeline
   Install dependencies:


pip install -r requirements.txt
Set up your Streamlit secrets in .streamlit/secrets.toml:

Ini, TOML
ELEVEN_API_KEY = "your_api_key_here"
Run the application:


streamlit run main.py
