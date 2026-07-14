import uuid
from pathlib import Path

import edge_tts


AUDIO_DIR = Path("app/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


async def text_to_speech(text: str):

    filename = f"{uuid.uuid4()}.mp3"

    output_path = AUDIO_DIR / filename

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AndrewNeural"
    )

    await communicate.save(str(output_path))

    return output_path