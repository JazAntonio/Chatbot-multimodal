"""
GUI Module for Audio GPT Interface
Handles all UI components and user interactions using Tkinter
"""

import tkinter as tk
from tkinter import ttk
import threading


class ChatGUI:
    """
    Main GUI class for the Audio GPT chatbot interface.
    Separates presentation logic from business logic.
    """
    
    def __init__(self, root, audio_service, stt_service, gpt_service, tts_service):
        """
        Initialize the GUI with required services.
        
        Args:
            root: Tkinter root window
            audio_service: Service for audio recording/playback
            stt_service: Service for speech-to-text
            gpt_service: Service for GPT responses
            tts_service: Service for text-to-speech
        """
        self.root = root
        self.root.title("Audio GPT Interface")
        self.root.geometry("1200x600")  # Ventana más ancha para 3 columnas
        
        # Store service references
        self.audio_service = audio_service
        self.stt_service = stt_service
        self.gpt_service = gpt_service
        self.tts_service = tts_service
        
        # Initialize UI
        self._setup_layout()
        self._create_widgets()
    
    def _setup_layout(self):
        """Configure the main window layout with three columns."""
        # Columna 0: Chat (más ancha)
        self.root.columnconfigure(0, weight=3)
        # Columna 1: Botones (fija)
        self.root.columnconfigure(1, weight=1)
        # Columna 2: Logs del sistema (mediana)
        self.root.columnconfigure(2, weight=2)
        self.root.rowconfigure(0, weight=1)
    
    def _create_widgets(self):
        """Create all UI widgets."""
        self._create_chat_area()
        self._create_control_panel()
        self._create_logs_area()
    
    def _create_chat_area(self):
        """Create the left column with chat text area."""
        left_frame = ttk.Frame(self.root, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        # Text area for chat display
        self.text_area = tk.Text(
            left_frame,
            wrap="word",
            font=("Arial", 12)
        )
        self.text_area.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            left_frame,
            orient="vertical",
            command=self.text_area.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.text_area.config(yscrollcommand=scrollbar.set)
    
    def _create_logs_area(self):
        """Create the right column with system logs."""
        logs_frame = ttk.Frame(self.root, padding=10)
        logs_frame.grid(row=0, column=2, sticky="nsew")
        
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(1, weight=1)
        
        # Título
        logs_title = ttk.Label(
            logs_frame,
            text="📋 Logs del Sistema",
            font=("Arial", 11, "bold")
        )
        logs_title.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Text area for system logs
        self.logs_area = tk.Text(
            logs_frame,
            wrap="word",
            font=("Courier", 9),
            bg="#f5f5f5",
            fg="#333333",
            height=10
        )
        self.logs_area.grid(row=1, column=0, sticky="nsew")
        
        # Scrollbar
        logs_scrollbar = ttk.Scrollbar(
            logs_frame,
            orient="vertical",
            command=self.logs_area.yview
        )
        logs_scrollbar.grid(row=1, column=1, sticky="ns")
        
        self.logs_area.config(yscrollcommand=logs_scrollbar.set)
    
    def _create_control_panel(self):
        """Create the middle column with control buttons divided into sections."""
        right_frame = ttk.Frame(self.root, padding=10)
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        right_frame.columnconfigure(0, weight=1)
        
        # ===========================
        # SECCIÓN 1: CONTROLES DE USUARIO
        # ===========================
        user_section_label = ttk.Label(
            right_frame,
            text="━━━ Usuario ━━━",
            font=("Arial", 10, "bold"),
            anchor="center"
        )
        user_section_label.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Botones de usuario
        self.btn_start = self._create_button(
            right_frame, "🎙", "Grabar", 1, self.start_recording
        )
        self.btn_stop = self._create_button(
            right_frame, "⏹", "Detener", 2, self.stop_recording
        )
        self.btn_play = self._create_button(
            right_frame, "▶", "Reproducir", 3, self.play_audio
        )
        
        # Separador visual
        separator = ttk.Separator(right_frame, orient="horizontal")
        separator.grid(row=4, column=0, sticky="ew", pady=20)
        
        # ===========================
        # SECCIÓN 2: CONTROLES DEL SISTEMA
        # ===========================
        system_section_label = ttk.Label(
            right_frame,
            text="━━━ Sistema ━━━",
            font=("Arial", 10, "bold"),
            anchor="center"
        )
        system_section_label.grid(row=5, column=0, sticky="ew", pady=(0, 10))
        
        # Botones del sistema
        self.btn_pause = self._create_button(
            right_frame, "⏸", "Pausar", 6, self.pause_audio
        )
        self.btn_delete = self._create_button(
            right_frame, "🗑", "Eliminar", 7, self.delete_audio
        )
        self.btn_send = self._create_button(
            right_frame, "➤", "Enviar", 8, self.process_audio
        )
        self.btn_close = self._create_button(
            right_frame, "↪", "Cerrar sesión", 9, self.close_session
        )
    
    def _create_button(self, parent, icon, text, row, command):
        """
        Factory method to create a button with icon and label.
        
        Args:
            parent: Parent widget
            icon: Icon/emoji to display
            text: Label text below button
            row: Row position in grid
            command: Callback function
            
        Returns:
            The created button widget
        """
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky="ew", pady=6)
        frame.columnconfigure(0, weight=1)
        
        button = tk.Button(
            frame,
            text=icon,
            font=("Arial", 16),
            width=3,
            height=1,
            command=command
        )
        button.grid(row=0, column=0)
        
        label = ttk.Label(
            frame,
            text=text,
            font=("Arial", 9),
            wraplength=140,
            justify="center"
        )
        label.grid(row=1, column=0, pady=(3, 0))
        
        return button
    
    # =========================
    # AUDIO CONTROL METHODS
    # =========================
    
    def start_recording(self):
        """Start audio recording."""
        self.audio_service.start_recording()
        self.append_log("🎙 Grabando...\n")
    
    def stop_recording(self):
        """Stop audio recording."""
        self.audio_service.stop_recording()
        self.append_log("⏹ Grabación detenida.\n")
    
    def play_audio(self):
        """Play recorded audio."""
        self.audio_service.play_audio()
    
    def pause_audio(self):
        """
        Toggle pause/resume for audio playback.
        Pauses if playing, resumes if paused.
        """
        # Verificar si el TTS está reproduciendo
        if self.tts_service.is_playing:
            # Pausar
            self.audio_service.stop_audio()
            self.tts_service.stop_audio()
            self.append_log("⏸ Audio pausado.\n")
            # Cambiar botón a "Reanudar"
            self._update_pause_button("▶", "Reanudar")
        else:
            # Reanudar (solo TTS, el audio del usuario se reproduce con el botón "Reproducir")
            if self.tts_service.audio_data is not None:
                self.tts_service.resume_audio()
                self.append_log("▶ Audio reanudado.\n")
                # Cambiar botón a "Pausar"
                self._update_pause_button("⏸", "Pausar")
            else:
                self.append_log("⚠ No hay audio TTS para reanudar.\n")
    
    def _update_pause_button(self, icon, text):
        """
        Update the pause button icon and text.
        
        Args:
            icon: New icon to display
            text: New label text
        """
        # Encontrar el botón y su etiqueta
        for widget in self.btn_pause.master.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(text=icon)
            elif hasattr(widget, 'cget') and widget.cget('text') in ["Pausar", "Reanudar"]:
                widget.config(text=text)
    
    def delete_audio(self):
        """Delete recorded audio file."""
        self.audio_service.delete_audio()
        self.append_log("🗑 Grabación eliminada.\n")
    
    # =========================
    # PROCESSING METHODS
    # =========================
    
    def process_audio(self):
        """
        Process audio through the complete pipeline:
        STT -> GPT -> TTS
        Runs in a separate thread to avoid blocking UI.
        """
        thread = threading.Thread(target=self._process_audio_thread)
        thread.daemon = True
        thread.start()
    
    def _process_audio_thread(self):
        """
        Background thread for audio processing.
        Handles transcription, GPT response, and TTS synthesis.
        """
        try:
            # Step 1: Transcribe audio
            self.root.after(0, lambda: self.append_log("⏳ Transcribiendo...\n"))
            
            user_text = self.stt_service.transcribe_file(
                self.audio_service.output_file
            )
            
            self.root.after(
                0,
                lambda: self.append_text(f"\n👤 Usuario:\n{user_text}\n\n")
            )
            
            # Step 2: Generate GPT response
            self.root.after(0, lambda: self.append_log("🤖 Generando respuesta...\n"))
            
            assistant_text = self.gpt_service.generate_response(user_text)
            
            self.root.after(
                0,
                lambda: self.append_text(f"🤖 Asistente:\n{assistant_text}\n\n")
            )
            
            # Step 3: Synthesize and play TTS
            self.root.after(0, lambda: self.append_log("🔊 Sintetizando voz...\n"))
            
            self.tts_service.synthesize(assistant_text)
            self.tts_service.play_audio()
            
            # Actualizar botón de pausa a estado "Pausar"
            self.root.after(0, lambda: self._update_pause_button("⏸", "Pausar"))
            
        except Exception as e:
            self.root.after(
                0,
                lambda err=e: self.append_text(f"\n❌ Error:\n{str(err)}\n")
            )
    
    def close_session(self):
        """Clean up and close the application."""
        self.audio_service.delete_audio()
        self.tts_service.delete_audio()
        self.gpt_service.reset_conversation()
        self.root.destroy()
    
    # =========================
    # UTILITY METHODS
    # =========================
    
    def append_text(self, message):
        """
        Append text to the chat area and auto-scroll.
        
        Args:
            message: Text to append
        """
        self.text_area.insert(tk.END, message)
        self.text_area.see(tk.END)
    
    def append_log(self, message):
        """
        Append log message to the system logs area and auto-scroll.
        
        Args:
            message: Log message to append
        """
        self.logs_area.insert(tk.END, message)
        self.logs_area.see(tk.END)
    
    def run(self):
        """Start the Tkinter main event loop."""
        self.root.mainloop()
