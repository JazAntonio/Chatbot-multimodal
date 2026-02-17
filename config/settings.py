"""
Centralized configuration management for the Audio GPT chatbot.
Loads and validates environment variables and application settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


class Settings:
    """
    Centralized configuration class.
    Loads settings from environment variables with validation.
    """
    
    def __init__(self):
        """Initialize settings by loading environment variables."""
        # Load .env file
        load_dotenv()
        
        # API Configuration
        self.openai_api_key = self._get_required_env("OPENAI_API_KEY")
        self.inworld_api_key = self._get_required_env("INWORLD_API_KEY")
        
        # Audio Configuration
        self.audio_sample_rate = int(os.getenv("AUDIO_SAMPLE_RATE", "44100"))
        self.audio_channels = int(os.getenv("AUDIO_CHANNELS", "1"))
        self.audio_dtype = os.getenv("AUDIO_DTYPE", "float32")
        
        # File Paths
        self.user_audio_file = os.getenv("USER_AUDIO_FILE", "output.wav")
        self.tts_audio_file = os.getenv("TTS_AUDIO_FILE", "response.wav")
        
        # OpenAI Configuration
        self.openai_stt_model = os.getenv("OPENAI_STT_MODEL", "gpt-4o-mini-transcribe")
        self.openai_gpt_model = os.getenv("OPENAI_GPT_MODEL", "gpt-5-nano")
        self.openai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "1.0"))
        
        # Inworld TTS Configuration
        self.inworld_tts_url = os.getenv(
            "INWORLD_TTS_URL",
            "https://api.inworld.ai/tts/v1/voice"
        )
        self.inworld_voice_id = os.getenv("INWORLD_VOICE_ID", "Hana")
        self.inworld_model_id = os.getenv("INWORLD_MODEL_ID", "inworld-tts-1.5-mini")
        
        # GUI Configuration
        self.window_width = int(os.getenv("WINDOW_WIDTH", "1200"))
        self.window_height = int(os.getenv("WINDOW_HEIGHT", "600"))
        self.window_title = os.getenv("WINDOW_TITLE", "Audio GPT Interface")
        
        # Logging Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "chatbot.log")
        self.log_max_bytes = int(os.getenv("LOG_MAX_BYTES", "10485760"))  # 10MB
        self.log_backup_count = int(os.getenv("LOG_BACKUP_COUNT", "3"))
        
        # Security Configuration
        self.security_level = os.getenv("SECURITY_LEVEL", "MEDIUM")
        self.max_input_length = int(os.getenv("MAX_INPUT_LENGTH", "2000"))
        self.max_tokens_per_message = int(os.getenv("MAX_TOKENS_PER_MESSAGE", "500"))
        self.enable_prompt_injection_detection = os.getenv(
            "ENABLE_PROMPT_INJECTION_DETECTION", "true"
        ).lower() == "true"
        self.enable_content_moderation = os.getenv(
            "ENABLE_CONTENT_MODERATION", "true"
        ).lower() == "true"
        self.rate_limit_messages_per_minute = int(
            os.getenv("RATE_LIMIT_MESSAGES_PER_MINUTE", "10")
        )
        self.custom_blacklist_patterns = os.getenv("CUSTOM_BLACKLIST_PATTERNS", "")
        
        # System Prompt
        self.system_prompt = os.getenv(
            "SYSTEM_PROMPT",
            "You are a helpful assistant, please provide only short and concise answers."
        )
    
    def _get_required_env(self, key: str) -> str:
        """
        Get a required environment variable.
        
        Args:
            key: Environment variable name
            
        Returns:
            Environment variable value
            
        Raises:
            ValueError: If the environment variable is not set
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(
                f"Required environment variable '{key}' is not set. "
                f"Please check your .env file."
            )
        return value
    
    def __repr__(self):
        """String representation (hides sensitive data)."""
        return (
            f"Settings("
            f"openai_api_key='***', "
            f"inworld_api_key='***', "
            f"audio_sample_rate={self.audio_sample_rate}, "
            f"window_size={self.window_width}x{self.window_height}"
            f")"
        )


# Global settings instance
settings = Settings()
