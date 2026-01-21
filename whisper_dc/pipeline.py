import asyncio
import concurrent.futures
import io
import os

import discord
import librosa
import soundfile as sf
from dotenv import load_dotenv
from pywhispercpp.model import Model

load_dotenv()

MODEL_NAME = os.environ.get("MODEL_NAME", "large-v3-turbo-q8_0")
TARGET_SAMPLE_RATE = 16000
N_THREADS = os.environ.get("N_THREADS", 6)
LANGUAGE = os.environ.get("LANGUAGE", "pl")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
model = Model(MODEL_NAME, n_threads=int(N_THREADS))

# The following is to make sure only one instance of the model is loaded
# and the transcription tasks are queued
pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)


def transcribe(model, buffer):
    data, sample_rate = sf.read(buffer)
    if data.ndim > 1:
        data = data.T

    data_resampled = librosa.resample(data, orig_sr=sample_rate, target_sr=TARGET_SAMPLE_RATE)

    segments = model.transcribe(data_resampled, language=LANGUAGE)

    transcription = "\n".join(
        f"`[{segment.t0:.2f}s -> {segment.t1/100:.2f}s]` {segment.text}"
        for segment in segments
    )
    return transcription


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(".ogg"):
                buffer = io.BytesIO()
                await attachment.save(buffer)

                transcription = await asyncio.get_running_loop().run_in_executor(
                    pool, transcribe, model, buffer
                )

                await message.reply(transcription, mention_author=False)


def main():
    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
