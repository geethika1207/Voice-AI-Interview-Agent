from deepgram import DeepgramClient, PrerecordedOptions
import os
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

deepgram = DeepgramClient(DEEPGRAM_API_KEY)


async def speech_to_text(file_path: str) -> str:
    with open(file_path, "rb") as audio:
        buffer = audio.read()

    payload = {
        "buffer": buffer,
        "mimetype": "audio/mp3"
    }

    options = PrerecordedOptions(
        model="nova-2",
        smart_format=True
    )

    response = deepgram.listen.prerecorded.v("1").transcribe_file(
        payload,
        options
    )

    return response["results"]["channels"][0]["alternatives"][0]["transcript"]