import tkinter as tk
from tkinter import ttk
import threading

from services.audio_service import AudioService
from services.stt_service import STTService
from services.response_service import GPTService
from services.tts_service import TTSService


class AudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio GPT Interface")
        self.root.geometry("850x600")

        # Servicios
        self.audio_service = AudioService()
        self.stt_service = STTService()
        self.gpt_service = GPTService()
        self.tts_service = TTSService()

        # Layout principal
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # =========================
        # COLUMNA IZQUIERDA (Chat)
        # =========================
        left_frame = ttk.Frame(self.root, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew")

        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)

        self.text_area = tk.Text(
            left_frame,
            wrap="word",
            font=("Arial", 12)
        )
        self.text_area.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            left_frame,
            orient="vertical",
            command=self.text_area.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.text_area.config(yscrollcommand=scrollbar.set)

        # =========================
        # COLUMNA DERECHA
        # =========================
        right_frame = ttk.Frame(self.root, padding=10)
        right_frame.grid(row=0, column=1, sticky="nsew")

        right_frame.columnconfigure(0, weight=1)

        for i in range(6):
            right_frame.rowconfigure(i, weight=1)

        self.btn_start = self.crear_boton(
            right_frame, "🎙", "Grabar", 0, self.start_recording
        )
        self.btn_stop = self.crear_boton(
            right_frame, "⏹", "Detener", 1, self.stop_recording
        )
        self.btn_play = self.crear_boton(
            right_frame, "▶", "Reproducir", 2, self.play_audio
        )
        self.btn_delete = self.crear_boton(
            right_frame, "🗑", "Eliminar", 3, self.delete_audio
        )
        self.btn_send = self.crear_boton(
            right_frame, "➤", "Enviar", 4, self.process_audio
        )
        self.close_session = self.crear_boton(
            right_frame, "↪", "Cerrar sesión", 5, self.close_session)

    # =========================
    # BOTÓN FACTORY
    # =========================
    def crear_boton(self, parent, icono, texto, fila, command):
        frame = ttk.Frame(parent)
        frame.grid(row=fila, column=0, sticky="ew", pady=6)
        frame.columnconfigure(0, weight=1)

        boton = tk.Button(
            frame,
            text=icono,
            font=("Arial", 16),
            width=3,
            height=1,
            command=command
        )
        boton.grid(row=0, column=0)

        etiqueta = ttk.Label(
            frame,
            text=texto,
            font=("Arial", 9),
            wraplength=140,
            justify="center"
        )
        etiqueta.grid(row=1, column=0, pady=(3, 0))

        return boton

    # =========================
    # AUDIO CONTROL
    # =========================
    def start_recording(self):
        self.audio_service.start_recording()
        self.append_text("🎙 Grabando...\n")

    def stop_recording(self):
        self.audio_service.stop_recording()
        self.append_text("⏹ Grabación detenida.\n")

    def play_audio(self):
        self.audio_service.play_audio()

    def delete_audio(self):
        self.audio_service.delete_audio()
        self.append_text("🗑 Grabación eliminada.\n")

    # =========================
    # PROCESAMIENTO COMPLETO
    # =========================
    def process_audio(self):
        thread = threading.Thread(target=self._process_audio_thread)
        thread.daemon = True
        thread.start()



    def _process_audio_thread(self):
        try:
            self.root.after(0, lambda: self.append_text("⏳ Transcribiendo...\n"))

            user_text = self.stt_service.transcribe_file(
                self.audio_service.output_file
            )

            self.root.after(
                0,
                lambda: self.append_text(f"\n👤 Usuario:\n{user_text}\n\n")
            )

            # GPT
            self.root.after(0, lambda: self.append_text("🤖 Generando respuesta...\n"))

            assistant_text = self.gpt_service.generate_response(user_text)

            self.root.after(
                0,
                lambda: self.append_text(f"🤖 Asistente:\n{assistant_text}\n\n")
            )

            # TTS sobre respuesta
            self.root.after(0, lambda: self.append_text("🔊 Sintetizando voz...\n"))

            self.tts_service.synthesize(assistant_text)
            self.tts_service.play_audio()

        except Exception as e:
            self.root.after(
                0,
                lambda err=e: self.append_text(f"\n❌ Error:\n{str(err)}\n")
            )

    def close_session(self):
        self.audio_service.delete_audio()
        self.tts_service.delete_audio()
        self.gpt_service.reset_conversation()
        self.root.destroy()

    # =========================
    # UTILIDAD
    # =========================
    def append_text(self, message):
        self.text_area.insert(tk.END, message)
        self.text_area.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioApp(root)
    root.mainloop()
