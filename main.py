import os
import base64
import requests
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
from openai import OpenAI
from dotenv import load_dotenv

# =========================
# CARGAR VARIABLES .env
# =========================

load_dotenv()  # Busca automáticamente archivo .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INWORLD_API_KEY = os.getenv("INWORLD_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no encontrada en .env")

if not INWORLD_API_KEY:
    raise ValueError("INWORLD_API_KEY no encontrada en .env")

client = OpenAI(api_key=OPENAI_API_KEY)

INWORLD_TTS_URL = "https://api.inworld.ai/tts/v1/voice"
VOICE_ID = "Dennis"
MODEL_ID = "inworld-tts-1.5-mini"


# =========================
# 1. TRANSCRIPCIÓN
# =========================

def transcribir_audio(ruta_audio):
    with open(ruta_audio, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )
    return transcript.text


# =========================
# 2. GENERAR RESPUESTA
# =========================

def generar_respuesta(prompt_usuario):
    response = client.responses.create(
        model="gpt-5",
        input=prompt_usuario
    )
    return response.output_text


# =========================
# 3. INWORLD TTS
# =========================

def sintetizar_inworld(texto):
    headers = {
        "Authorization": f"Basic {INWORLD_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": texto,
        "voiceId": VOICE_ID,
        "modelId": MODEL_ID,
        "audioConfig": {
            "audioEncoding": "LINEAR16"
        }
    }

    response = requests.post(INWORLD_TTS_URL, json=payload, headers=headers)
    #print("Status:", response.status_code)
    #print("Respuesta servidor:", response.text)
    response.raise_for_status()

    data = response.json()
    audio_base64 = data["audioContent"]
    audio_bytes = base64.b64decode(audio_base64)

    with open("respuesta.wav", "wb") as f:
        f.write(audio_bytes)

    return "respuesta.wav"


# =========================
# 4. REPRODUCCIÓN
# =========================

def reproducir_audio(ruta_wav):
    samplerate, data = wavfile.read(ruta_wav)
    sd.play(data, samplerate)
    sd.wait()


# =========================
# PIPELINE
# =========================

def pipeline(ruta_audio_usuario):
    print("Transcribiendo...")
    texto_usuario = transcribir_audio("./sample1.wav")
    print("Usuario:", texto_usuario)

    print("Generando respuesta...")
    respuesta_texto = generar_respuesta(texto_usuario)
    print("GPT:", respuesta_texto)

    #respuesta_texto = "This is only for test the inworld API."

    print("Sintetizando...")
    ruta_audio = sintetizar_inworld(respuesta_texto)

    print("Reproduciendo...")
    reproducir_audio(ruta_audio)


if __name__ == "__main__":
    pipeline("audio_usuario.wav")
