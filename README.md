# Whisper-powered Voice Message Transcriber

This repository contains code of a simple Discord bot that reacts to voice messages, transcribes them, and sends the transcription as a reply to the original voice message.

The speech-to-text model used is a pre-trained [OpenAI's Whisper](https://github.com/openai/whisper) model (specifically [`large V3`](https://huggingface.co/openai/whisper-large-v3)), using the code from [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper).

# Usage

- Install Python (3.11 at least)
- Install [Poetry](https://python-poetry.org/)
- Install dependencies: `poetry install`
- Activate the Poetry-created virtualenv: `poetry shell`
- Set `DISCORD_TOKEN` environment variable to your Discord Bot's Token.
- Run the code: `python main.py`

The bot reacts to discord messages that have an audio attachment with .ogg extension.

# Configuration

The bot supports the following environment variables:

- `DISCORD_TOKEN` (required) - the token used to authenticate the bot
- `MODEL_NAME` - the name of the model to be loaded by `faster-whisper` from Hugging Face Hub. Refer to the original repository to learn more about available pre-trained models. Default: `large-v3`
- `LANGUAGE` - the language for which transcription should be done. If not set, the language is detected for each transcription.

Currently, the model is configured to run on the CPU. For CUDA-enabled deployments, refer to the original `faster-whisper` repository.
