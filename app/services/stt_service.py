import os
import asyncio
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)

load_dotenv()


class SpeechToText:

    def __init__(self):

        config = DeepgramClientOptions(
            options={"keepalive": "true"}
        )

        self.client = DeepgramClient(
            os.getenv("DEEPGRAM_API_KEY"),
            config
        )

        self.connection = None

        # Stores one utterance
        self.transcript = []

    async def connect(self):

        self.connection = self.client.listen.live.v("1")

        async def on_message(result, **kwargs):

            sentence = (
                result.channel.alternatives[0].transcript
            )

            if sentence and result.is_final:
                self.transcript.append(sentence)

        self.connection.on(
            LiveTranscriptionEvents.Transcript,
            on_message
        )

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            smart_format=True,
            punctuate=True,
            interim_results=True,
        )

        success = self.connection.start(options)

        if not success:
            raise RuntimeError("Failed to start Deepgram connection")
    async def send_chunk(self, chunk: bytes):

        if self.connection is None:
            raise RuntimeError("Deepgram connection not started.")

        self.connection.send(chunk)

    async def get_transcript(self):

        if not self.transcript:
            return ""

        return " ".join(self.transcript)

    async def reset_transcript(self):

        self.transcript.clear()

    async def close(self):

        if self.connection:

            self.connection.finish()

            self.connection = None
            
# DEEPGRAM STT CONNECTION CODE FOR AUDIO FILE UPLOAD

# from deepgram import DeepgramClient, PrerecordedOptions
# import os
# from dotenv import load_dotenv

# load_dotenv()

# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# deepgram = DeepgramClient(DEEPGRAM_API_KEY)


# async def speech_to_text(file_path: str) -> str:
#     with open(file_path, "rb") as audio:
#         buffer = audio.read()

#     payload = {
#         "buffer": buffer,
#         "mimetype": "audio/mp3"
#     }

#     options = PrerecordedOptions(
#         model="nova-2",
#         smart_format=True
#     )

#     response = deepgram.listen.prerecorded.v("1").transcribe_file(
#         payload,
#         options
#     )

#     return response["results"]["channels"][0]["alternatives"][0]["transcript"]