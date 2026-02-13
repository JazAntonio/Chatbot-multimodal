import os
import tempfile
from dotenv import load_dotenv
from openai import OpenAI
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


class STTService:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OPENAI_API_KEY no encontrada en el archivo .env")

        self.client = OpenAI(api_key=api_key)
        logger.info("STTService initialized successfully")

    def transcribe_file(self, file_path: str) -> str:
        """
        Transcribe un archivo de audio usando OpenAI STT.
        Retorna el texto transcrito.
        """
        logger.debug(f"Transcribing audio file: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"Audio file not found: {file_path}")
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        try:
            with open(file_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=audio_file
                )
            
            logger.info(f"Transcription successful: {len(transcription.text)} characters")
            logger.debug(f"Transcribed text: {transcription.text[:100]}...")  # Log first 100 chars
            return transcription.text
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}", exc_info=True)
            raise

    def transcribe_bytes(self, audio_bytes: bytes, suffix=".wav") -> str:
        """
        Transcribe audio directamente desde memoria.
        Se crea un archivo temporal compatible.
        """
        logger.debug(f"Transcribing audio from bytes ({len(audio_bytes)} bytes)")

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_path = temp_audio.name

        try:
            text = self.transcribe_file(temp_path)
            logger.info("Transcription from bytes completed successfully")
        finally:
            os.remove(temp_path)
            logger.debug(f"Temporary file removed: {temp_path}")

        return text


# # Test ##
# stt = STTService()
# texto = stt.transcribe_file("../sample1.wav")
#
# print("Transcripción:")
# print(texto)