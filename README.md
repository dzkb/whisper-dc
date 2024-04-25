# Whisper-powered Voice Message Transcriber

This repository contains code of a simple Discord bot that reacts to voice messages, transcribes them, and sends the transcription as the reply to the original voice message.

The speech-to-text model used is a pre-trained [OpenAI's Whisper](https://github.com/openai/whisper) model (specifically [`large V3`](https://huggingface.co/openai/whisper-large-v3)), using the code from [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper).

# Usage

- Install Python (3.11 at least)
- Install [Poetry](https://python-poetry.org/)
- Install dependencies: `poetry install`
- Activate the Poetry-created virtualenv: `poetry shell`
- Set `DISCORD_TOKEN` environment variable to your Discord Bot's Token.
- Run the code: `python main.py`

The bot reacts to discord messages that have an audio attachment with .ogg extension.
