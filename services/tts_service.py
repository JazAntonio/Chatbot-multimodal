# services/tts_service.py

import os
import base64
import requests
import sounddevice as sd
import soundfile as sf
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


class TTSService:
    def __init__(self, output_file="response.wav"):
        self.api_key = os.getenv("INWORLD_API_KEY")
        if not self.api_key:
            logger.error("INWORLD_API_KEY not found in environment variables")
            raise ValueError("INWORLD_API_KEY no encontrada en variables de entorno")

        self.output_file = output_file

        # Configuración Inworld
        self.tts_url = "https://api.inworld.ai/tts/v1/voice"
        self.voice_id = "Hana"
        self.model_id = "inworld-tts-1.5-mini"
        
        # Estado de reproducción para pause/resume
        self.is_playing = False
        self.audio_data = None
        self.sample_rate = None
        
        logger.info(f"TTSService initialized with voice: {self.voice_id}")

    def synthesize(self, text):
        """
        Convierte texto en audio usando Inworld TTS
        y guarda el archivo WAV.
        """
        logger.debug(f"Synthesizing text: {text[:50]}...")

        if not text.strip():
            logger.error("Empty text provided for TTS")
            raise ValueError("Texto vacío para TTS")

        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "voiceId": self.voice_id,
            "modelId": self.model_id,
            "audioConfig": {
                "audioEncoding": "LINEAR16"
            }
        }

        try:
            logger.info("Sending TTS request to Inworld API...")
            response = requests.post(self.tts_url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            audio_base64 = data["audioContent"]
            audio_bytes = base64.b64decode(audio_base64)

            with open(self.output_file, "wb") as f:
                f.write(audio_bytes)
            
            logger.info(f"TTS audio saved to: {self.output_file}")
            return self.output_file
            
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}", exc_info=True)
            raise

    def play_audio(self):
        """
        Reproduce el audio generado de forma no bloqueante.
        """

        if not os.path.exists(self.output_file):
            logger.error(f"TTS audio file not found: {self.output_file}")
            raise FileNotFoundError("No existe archivo TTS")

        # Cargar y guardar datos de audio para pause/resume
        self.audio_data, self.sample_rate = sf.read(self.output_file, dtype="float32")
        sd.play(self.audio_data, self.sample_rate)
        self.is_playing = True
        # No usar sd.wait() para permitir que la UI siga respondiendo
        logger.info("Playing TTS audio")

    def stop_audio(self):
        """
        Detiene la reproducción del audio TTS
        """
        sd.stop()
        self.is_playing = False
        logger.info("TTS audio playback stopped")
    
    def resume_audio(self):
        """
        Reanuda la reproducción del audio TTS desde el inicio.
        """
        if self.audio_data is not None and self.sample_rate is not None:
            sd.play(self.audio_data, self.sample_rate)
            self.is_playing = True
            logger.info("Resuming TTS audio playback")

    def delete_audio(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
            logger.info(f"TTS audio file deleted: {self.output_file}")
