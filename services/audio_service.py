import sounddevice as sd
import numpy as np
import wave
import os


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
                print("Audio status:", status)
            if self.recording:
                self.audio_data.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=self.fs,
            channels=1,
            dtype="float32",  # 🔥 importante
            callback=callback
        )

        self.stream.start()
        print("Grabando...")

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
            print("No se capturó audio.")
            return None

        audio = np.concatenate(self.audio_data, axis=0)

        print("Shape:", audio.shape)
        print("Min:", audio.min())
        print("Max:", audio.max())
        print("Duración aprox (seg):", len(audio) / self.fs)

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

        print("Grabación guardada en:", self.output_file)
        return self.output_file

    # =========================
    # REPRODUCIR
    # =========================
    def play_audio(self):
        """
        Reproduce el audio grabado de forma no bloqueante.
        """
        if not os.path.exists(self.output_file):
            print("No hay archivo para reproducir")
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
            print("Reproduciendo audio...")

    # =========================
    # DETENER REPRODUCCIÓN
    # =========================
    def stop_audio(self):
        """
        Detiene cualquier reproducción de audio activa.
        """
        sd.stop()
        print("Reproducción detenida")

    # =========================
    # ELIMINAR
    # =========================
    def delete_audio(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
            print("Archivo eliminado")
        else:
            print("No existe archivo para eliminar")



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
