"""
PyQt6 GUI Module for Audio GPT Interface
Modern GUI implementation with customizable theming support
"""

import sys
import logging
import threading
from typing import Dict, Any
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QTextCursor

from utils.logger import get_logger
from utils.theme_loader import load_theme

logger = get_logger(__name__)


class LogSignal(QObject):
    """Signal emitter for thread-safe logging to GUI."""
    log_message = pyqtSignal(str)


class QTextEditLogger(logging.Handler):
    """Custom logging handler that writes to a QTextEdit widget."""
    
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.signal = LogSignal()
        self.signal.log_message.connect(self._append_log)
    
    def emit(self, record):
        """Emit a log record to the QTextEdit widget."""
        try:
            msg = self.format(record)
            self.signal.log_message.emit(msg)
        except Exception:
            self.handleError(record)
    
    def _append_log(self, msg):
        """Append message to the text widget (runs in main thread)."""
        self.text_widget.append(msg)
        # Auto-scroll to bottom
        self.text_widget.moveCursor(QTextCursor.MoveOperation.End)


class ChatGUIQt(QMainWindow):
    """
    Main PyQt6 GUI class for the Audio GPT chatbot interface.
    Supports customizable theming and background images.
    """
    
    def __init__(self, audio_service, stt_service, gpt_service, tts_service, theme_path=None):
        """
        Initialize the PyQt6 GUI with required services.
        
        Args:
            audio_service: Service for audio recording/playback
            stt_service: Service for speech-to-text
            gpt_service: Service for GPT responses
            tts_service: Service for text-to-speech
            theme_path: Optional path to custom theme file
        """
        super().__init__()
        
        # Store service references
        self.audio_service = audio_service
        self.stt_service = stt_service
        self.gpt_service = gpt_service
        self.tts_service = tts_service
        
        # Load theme
        self.theme = load_theme(theme_path)
        logger.info(f"Theme loaded: {self.theme.get('theme_info', {}).get('name', 'Unknown')}")
        
        # Initialize UI
        self._setup_window()
        self._create_widgets()
        self._apply_theme()
        self._setup_gui_logging()
        
        logger.info("ChatGUIQt initialized successfully")
    
    def _setup_window(self):
        """Configure the main window properties."""
        window_config = self.theme["window"]
        self.setWindowTitle(window_config["title"])
        self.resize(window_config["width"], window_config["height"])
        
        # Set window background color
        self.setStyleSheet(f"QMainWindow {{ background-color: {window_config['background_color']}; }}")
    
    def _create_widgets(self):
        """Create all UI widgets."""
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create three columns
        self._create_chat_area(main_layout)
        self._create_control_panel(main_layout)
        self._create_logs_area(main_layout)
    
    def _create_chat_area(self, parent_layout):
        """Create the left column with chat text area."""
        chat_frame = QFrame()
        chat_layout = QVBoxLayout(chat_frame)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        
        # Chat text area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        chat_layout.addWidget(self.chat_area)
        
        # Add to parent with stretch factor
        parent_layout.addWidget(chat_frame, 3)
    
    def _create_logs_area(self, parent_layout):
        """Create the right column with system logs."""
        logs_frame = QFrame()
        logs_layout = QVBoxLayout(logs_frame)
        logs_layout.setContentsMargins(0, 0, 0, 0)
        logs_layout.setSpacing(5)
        
        # Title label
        logs_title = QLabel("📋 Logs del Sistema")
        logs_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        logs_layout.addWidget(logs_title)
        
        # Logs text area
        self.logs_area = QTextEdit()
        self.logs_area.setReadOnly(True)
        logs_layout.addWidget(self.logs_area)
        
        # Add to parent with stretch factor
        parent_layout.addWidget(logs_frame, 2)
    
    def _create_control_panel(self, parent_layout):
        """Create the middle column with control buttons."""
        control_frame = QFrame()
        control_layout = QVBoxLayout(control_frame)
        control_layout.setSpacing(10)
        control_layout.setContentsMargins(10, 10, 10, 10)
        
        # User controls section
        user_label = QLabel("━━━ Usuario ━━━")
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(user_label)
        
        self.btn_record = self._create_button("🎙", "Grabar", self.start_recording)
        control_layout.addWidget(self.btn_record)
        
        self.btn_stop = self._create_button("⏹", "Detener", self.stop_recording)
        control_layout.addWidget(self.btn_stop)
        
        self.btn_play = self._create_button("▶", "Reproducir", self.play_audio)
        control_layout.addWidget(self.btn_play)
        
        self.btn_delete = self._create_button("🗑", "Eliminar", self.delete_audio)
        control_layout.addWidget(self.btn_delete)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        control_layout.addWidget(separator)
        
        # System controls section
        system_label = QLabel("━━━ Sistema ━━━")
        system_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(system_label)
        
        self.btn_pause = self._create_button("⏸", "Pausar", self.pause_audio)
        control_layout.addWidget(self.btn_pause)
        
        self.btn_send = self._create_button("➤", "Enviar", self.process_audio)
        control_layout.addWidget(self.btn_send)
        
        self.btn_close = self._create_button("↪", "Cerrar sesión", self.close_session)
        control_layout.addWidget(self.btn_close)
        
        # Add stretch to push buttons to top
        control_layout.addStretch()
        
        # Set fixed width for control panel
        control_frame.setFixedWidth(180)
        parent_layout.addWidget(control_frame)
    
    def _create_button(self, icon, text, callback):
        """
        Create a styled button with icon and text.
        
        Args:
            icon: Icon/emoji to display
            text: Button text
            callback: Function to call on click
            
        Returns:
            QPushButton widget
        """
        button = QPushButton(f"{icon}\n{text}")
        button.clicked.connect(callback)
        button.setMinimumHeight(60)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button
    
    def _apply_theme(self):
        """Apply theme styles to all widgets."""
        # Chat area styling
        chat_config = self.theme["chat_area"]
        chat_style = f"""
            QTextEdit {{
                background-color: {chat_config['background_color']};
                color: {chat_config['text_color']};
                font-family: {chat_config['font_family']};
                font-size: {chat_config['font_size']}pt;
                padding: {chat_config['padding']}px;
                border: none;
        """
        
        # Add background image if specified
        if chat_config.get('background_image'):
            chat_style += f"""
                background-image: url({chat_config['background_image']});
                background-repeat: {chat_config.get('background_repeat', 'no-repeat')};
                background-position: {chat_config.get('background_position', 'center')};
            """
        
        chat_style += "}"
        self.chat_area.setStyleSheet(chat_style)
        
        # Logs area styling
        logs_config = self.theme["logs_area"]
        logs_style = f"""
            QTextEdit {{
                background-color: {logs_config['background_color']};
                color: {logs_config['text_color']};
                font-family: {logs_config['font_family']};
                font-size: {logs_config['font_size']}pt;
                padding: {logs_config['padding']}px;
                border: 1px solid {logs_config['border_color']};
                border-radius: 4px;
            }}
        """
        self.logs_area.setStyleSheet(logs_style)
        
        # Button styling
        btn_config = self.theme["control_panel"]
        button_style = f"""
            QPushButton {{
                background-color: {btn_config['button_color']};
                color: {btn_config['button_text_color']};
                border: none;
                border-radius: {btn_config['button_border_radius']}px;
                font-size: 11pt;
                font-weight: bold;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: {btn_config['button_hover_color']};
            }}
            QPushButton:pressed {{
                background-color: {btn_config['button_pressed_color']};
            }}
        """
        
        # Apply to all buttons
        for button in [self.btn_record, self.btn_stop, self.btn_play, self.btn_delete,
                      self.btn_pause, self.btn_send, self.btn_close]:
            button.setStyleSheet(button_style)
        
        logger.debug("Theme styles applied to all widgets")
    
    def _setup_gui_logging(self):
        """Setup custom logging handler for GUI."""
        gui_handler = QTextEditLogger(self.logs_area)
        gui_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        gui_handler.setFormatter(formatter)
        
        # Add to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(gui_handler)
        
        logger.debug("GUI logging handler configured")
    
    # =========================
    # AUDIO CONTROL METHODS
    # =========================
    
    def start_recording(self):
        """Start audio recording."""
        logger.info("User initiated recording")
        self.audio_service.start_recording()
    
    def stop_recording(self):
        """Stop audio recording."""
        logger.info("User stopped recording")
        self.audio_service.stop_recording()
    
    def play_audio(self):
        """Play recorded audio."""
        logger.info("User requested audio playback")
        self.audio_service.play_audio()
    
    def pause_audio(self):
        """Toggle pause/resume for audio playback."""
        if self.tts_service.is_playing:
            logger.info("Pausing audio playback")
            self.audio_service.stop_audio()
            self.tts_service.stop_audio()
            self.btn_pause.setText("▶\nReanudar")
        else:
            if self.tts_service.audio_data is not None:
                logger.info("Resuming audio playback")
                self.tts_service.resume_audio()
                self.btn_pause.setText("⏸\nPausar")
            else:
                logger.warning("No TTS audio available to resume")
    
    def delete_audio(self):
        """Delete recorded audio file."""
        logger.info("User requested audio deletion")
        self.audio_service.delete_audio()
    
    def process_audio(self):
        """Process audio through the complete pipeline: STT -> GPT -> TTS."""
        logger.info("Starting audio processing pipeline")
        thread = threading.Thread(target=self._process_audio_thread)
        thread.daemon = True
        thread.start()
    
    def _process_audio_thread(self):
        """Background thread for audio processing."""
        try:
            # Step 1: Transcribe audio
            logger.info("Step 1/3: Starting transcription")
            
            user_text = self.stt_service.transcribe_file(
                self.audio_service.output_file
            )
            
            self.chat_area.append(f"\n👤 Usuario:\n{user_text}\n")
            
            # Step 2: Generate GPT response
            logger.info("Step 2/3: Generating GPT response")
            
            assistant_text = self.gpt_service.generate_response(user_text)
            
            self.chat_area.append(f"🤖 Asistente:\n{assistant_text}\n")
            
            # Step 3: Synthesize and play TTS
            logger.info("Step 3/3: Synthesizing speech")
            
            self.tts_service.synthesize(assistant_text)
            self.tts_service.play_audio()
            
            self.btn_pause.setText("⏸\nPausar")
            
            logger.info("Audio processing pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"Audio processing failed: {e}", exc_info=True)
            self.chat_area.append(f"\n❌ Error:\n{str(e)}\n")
    
    def close_session(self):
        """Clean up and close the application."""
        logger.info("Closing session and cleaning up resources")
        self.audio_service.delete_audio()
        self.tts_service.delete_audio()
        self.gpt_service.reset_conversation()
        logger.info("Application shutdown complete")
        self.close()
    
    def append_text(self, message):
        """
        Append text to the chat area.
        
        Args:
            message: Text to append
        """
        self.chat_area.append(message)
    
    def run(self):
        """Show the window (called by main.py)."""
        self.show()
