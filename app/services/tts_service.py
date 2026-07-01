import edge_tts
import uuid
from pathlib import Path


# Folder where generated audio files will be stored
AUDIO_DIR = Path("app/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


async def text_to_speech(text: str):
    """
    Converts text into speech using Edge-TTS.
    Returns the generated audio filename.
    """

    filename = f"{uuid.uuid4()}.mp3"
    output_path = AUDIO_DIR / filename

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AndrewNeural"
    )

    await communicate.save(str(output_path))

    return filename