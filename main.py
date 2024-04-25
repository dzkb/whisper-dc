import asyncio
import concurrent.futures
import io
import os

import discord
from faster_whisper import WhisperModel

MODEL_NAME = os.environ.get("MODEL_NAME", "large-v3")
LANGUAGE = os.environ.get("LANGUAGE")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def transcribe(model, buffer):
    segments, _ = model.transcribe(buffer, beam_size=5, language=LANGUAGE)

    transcription = "\n".join(
        f"`[{segment.start:.2f}s -> {segment.end:.2f}s]` {segment.text}"
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


if __name__ == "__main__":
    # The following is to make sure only one instance of the model is loaded
    # and the transcription tasks are queued
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    model = WhisperModel(MODEL_NAME, compute_type="int8")

    client.run(DISCORD_TOKEN)
