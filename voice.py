from io import BytesIO
from gtts import gTTS
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def speech_to_text(audio_bytes):

    response = client.models.generate_content(
       model="gemini-3.8-flash",
        contents=[
            types.Part.from_bytes(
                data=audio_bytes,
                mime_type="audio/wav"
            ),
            "Transcribe the audio accurately. Return only the spoken words."
        ]
    )

    return response.text.strip()


def text_to_speech(text):

    audio_buffer = BytesIO()

    speech = gTTS(
        text=text,
        lang="en"
    )

    speech.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    return audio_buffer