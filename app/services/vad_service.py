from silero_vad import (
    load_silero_vad,
    get_speech_timestamps
)

import numpy as np


class VoiceActivityDetector:

    def __init__(self):

        self.model = load_silero_vad()

        self.audio_buffer = bytearray()

        self.speech_started = False

    def add_chunk(self, chunk: bytes):

        self.audio_buffer.extend(chunk)

    def user_finished_speaking(self):

        if len(self.audio_buffer) == 0:
            return False

        audio = np.frombuffer(
            self.audio_buffer,
            dtype=np.int16
        ).astype(np.float32)

        audio = audio / 32768.0

        speech = get_speech_timestamps(
            audio,
            self.model,
            sampling_rate=16000
        )

        # User has spoken
        if speech:

            self.speech_started = True

            return False

        # User spoke previously and now silence
        if self.speech_started:

            return True

        # User never spoke
        return False

    def reset(self):

        self.audio_buffer.clear()

        self.speech_started = False