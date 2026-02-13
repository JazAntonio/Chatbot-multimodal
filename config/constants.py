"""
Global constants for the Audio GPT chatbot.
"""

# Application Info
APP_NAME = "Audio GPT Chatbot"
APP_VERSION = "2.0.0"

# UI Constants
CHAT_COLUMN_WEIGHT = 3
BUTTONS_COLUMN_WEIGHT = 2
LOGS_COLUMN_WEIGHT = 1

# Button Labels
BTN_RECORD = "Grabar"
BTN_STOP = "Detener"
BTN_PLAY = "Reproducir"
BTN_DELETE = "Eliminar"
BTN_PAUSE = "Pausar"
BTN_RESUME = "Reanudar"
BTN_SEND = "Enviar"
BTN_CLOSE = "Cerrar sesión"

# Section Labels
SECTION_USER = "━━━ Usuario ━━━"
SECTION_SYSTEM = "━━━ Sistema ━━━"
LOGS_TITLE = "📋 Logs del Sistema"

# Status Messages
MSG_RECORDING = "🎙 Grabando...\n"
MSG_STOPPED = "⏹ Grabación detenida.\n"
MSG_DELETED = "🗑 Grabación eliminada.\n"
MSG_PAUSED = "⏸ Audio pausado.\n"
MSG_RESUMED = "▶ Audio reanudado.\n"
MSG_NO_TTS = "⚠ No hay audio TTS para reanudar.\n"
MSG_TRANSCRIBING = "⏳ Transcribiendo...\n"
MSG_GENERATING = "🤖 Generando respuesta...\n"
MSG_SYNTHESIZING = "🔊 Sintetizando voz...\n"

# Chat Messages
CHAT_USER_PREFIX = "\n👤 Usuario:\n"
CHAT_ASSISTANT_PREFIX = "🤖 Asistente:\n"
CHAT_ERROR_PREFIX = "\n❌ Error:\n"

# Audio Constants
AUDIO_ENCODING_LINEAR16 = "LINEAR16"
AUDIO_DTYPE_FLOAT32 = "float32"
AUDIO_DTYPE_INT16 = "int16"

# File Extensions
EXT_WAV = ".wav"
EXT_LOG = ".log"
