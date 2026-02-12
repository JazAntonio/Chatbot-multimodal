import os
import tempfile
from dotenv import load_dotenv
from openai import OpenAI


class STTService:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY no encontrada en el archivo .env")

        self.client = OpenAI(api_key=api_key)

    def transcribe_file(self, file_path: str) -> str:
        """
        Transcribe un archivo de audio usando OpenAI STT.
        Retorna el texto transcrito.
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        with open(file_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )

        return transcription.text

    def transcribe_bytes(self, audio_bytes: bytes, suffix=".wav") -> str:
        """
        Transcribe audio directamente desde memoria.
        Se crea un archivo temporal compatible.
        """

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_path = temp_audio.name

        try:
            text = self.transcribe_file(temp_path)
        finally:
            os.remove(temp_path)

        return text


# # Test ##
# stt = STTService()
# texto = stt.transcribe_file("../sample1.wav")
#
# print("Transcripción:")
# print(texto)