import sounddevice as sd
import numpy as np
import wave
import os
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


class AudioService:
    def __init__(self, samplerate=44100):
        self.fs = samplerate
        self.recording = False
        self.audio_data = []
        self.stream = None
        self.output_file = "output.wav"

    # =========================
    # GRABAR
    # =========================
    def start_recording(self):
        self.recording = True
        self.audio_data = []

        def callback(indata, frames, time, status):
            if status:
                logger.warning(f"Audio callback status: {status}")
            if self.recording:
                self.audio_data.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=self.fs,
            channels=1,
            dtype="float32",  # 🔥 importante
            callback=callback
        )

        self.stream.start()
        logger.info("Audio recording started")

    # =========================
    # DETENER Y GUARDAR
    # =========================
    def stop_recording(self):
        if not self.recording:
            return None

        self.recording = False
        self.stream.stop()
        self.stream.close()

        if not self.audio_data:
            logger.warning("No audio data captured during recording")
            return None

        audio = np.concatenate(self.audio_data, axis=0)

        duration = len(audio) / self.fs
        logger.debug(f"Audio shape: {audio.shape}, Min: {audio.min():.4f}, Max: {audio.max():.4f}")
        logger.info(f"Recording duration: {duration:.2f} seconds")

        # Normalización
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val

        # Convertir a int16
        audio_int16 = np.int16(audio * 32767)

        with wave.open(self.output_file, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16 bits
            wf.setframerate(self.fs)
            wf.writeframes(audio_int16.tobytes())

        logger.info(f"Recording saved to: {self.output_file}")
        return self.output_file

    # =========================
    # REPRODUCIR
    # =========================
    def play_audio(self):
        """
        Reproduce el audio grabado de forma no bloqueante.
        """
        if not os.path.exists(self.output_file):
            logger.warning(f"Audio file not found: {self.output_file}")
            return

        with wave.open(self.output_file, "rb") as wf:
            frames = wf.readframes(wf.getnframes())
            audio = np.frombuffer(frames, dtype=np.int16)

            # Convertir a float32 para reproducir
            audio = audio.astype(np.float32) / 32767

            # 🔥 Asegurar forma correcta (mono)
            audio = audio.reshape(-1, 1)

            # Reproducir sin bloquear (sin sd.wait())
            sd.play(audio, wf.getframerate())
            logger.info("Playing recorded audio")

    # =========================
    # DETENER REPRODUCCIÓN
    # =========================
    def stop_audio(self):
        """
        Detiene cualquier reproducción de audio activa.
        """
        sd.stop()
        logger.info("Audio playback stopped")

    # =========================
    # ELIMINAR
    # =========================
    def delete_audio(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
            logger.info(f"Audio file deleted: {self.output_file}")
        else:
            logger.warning("No audio file to delete")



# import time
#
# def test():
#     audio = AudioService()
#
#     print("Iniciando grabación por 3 segundos...")
#     audio.start_recording()
#
#     time.sleep(5)
#
#     print("Deteniendo grabación...")
#     audio.stop_recording()
#
#     print("Reproduciendo audio...")
#     audio.play_audio()
#
#     # time.sleep(2)
#
#     print("Eliminando archivo...")
#     audio.delete_audio()
#
#     print("Prueba finalizada.")
#
#
# if __name__ == "__main__":
#     test()
