# services/tts_service.py

import os
import base64
import requests
import sounddevice as sd
import soundfile as sf


class TTSService:
    def __init__(self, output_file="response.wav"):
        self.api_key = os.getenv("INWORLD_API_KEY")
        if not self.api_key:
            raise ValueError("INWORLD_API_KEY no encontrada en variables de entorno")

        self.output_file = output_file

        # Configuración Inworld
        self.tts_url = "https://api.inworld.ai/tts/v1/voice"
        self.voice_id = "Hana"
        self.model_id = "inworld-tts-1.5-mini"

    def synthesize(self, text):
        """
        Convierte texto en audio usando Inworld TTS
        y guarda el archivo WAV.
        """

        if not text.strip():
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

        response = requests.post(self.tts_url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        audio_base64 = data["audioContent"]
        audio_bytes = base64.b64decode(audio_base64)

        with open(self.output_file, "wb") as f:
            f.write(audio_bytes)

        return self.output_file

    def play_audio(self):
        """
        Reproduce el audio generado de forma no bloqueante.
        """

        if not os.path.exists(self.output_file):
            raise FileNotFoundError("No existe archivo TTS")

        data, fs = sf.read(self.output_file, dtype="float32")
        sd.play(data, fs)
        # No usar sd.wait() para permitir que la UI siga respondiendo
        print("Reproduciendo audio TTS...")

    def stop_audio(self):
        """
        Detiene la reproducción del audio TTS
        """
        sd.stop()

    def delete_audio(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
