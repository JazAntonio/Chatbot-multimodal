"""
Custom exceptions for the Audio GPT chatbot.
Provides specific exception types for better error handling.
"""


class ChatbotBaseException(Exception):
    """Base exception for all chatbot-related errors."""
    pass


class ConfigurationError(ChatbotBaseException):
    """Raised when there's a configuration error."""
    pass


class AudioServiceError(ChatbotBaseException):
    """Raised when there's an error in the audio service."""
    pass


class STTServiceError(ChatbotBaseException):
    """Raised when there's an error in the speech-to-text service."""
    pass


class GPTServiceError(ChatbotBaseException):
    """Raised when there's an error in the GPT service."""
    pass


class TTSServiceError(ChatbotBaseException):
    """Raised when there's an error in the text-to-speech service."""
    pass


class ValidationError(ChatbotBaseException):
    """Raised when validation fails."""
    pass
