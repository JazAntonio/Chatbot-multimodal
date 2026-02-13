"""
Validation utilities for the Audio GPT chatbot.
Provides reusable validation functions.
"""

import os
from pathlib import Path
from typing import Optional
from .exceptions import ValidationError


def validate_file_exists(file_path: str, file_type: str = "File") -> None:
    """
    Validate that a file exists.
    
    Args:
        file_path: Path to the file
        file_type: Type of file for error message
        
    Raises:
        ValidationError: If file doesn't exist
    """
    if not os.path.exists(file_path):
        raise ValidationError(f"{file_type} not found: {file_path}")


def validate_audio_file(file_path: str) -> None:
    """
    Validate that an audio file exists and has correct extension.
    
    Args:
        file_path: Path to the audio file
        
    Raises:
        ValidationError: If file is invalid
    """
    validate_file_exists(file_path, "Audio file")
    
    valid_extensions = ['.wav', '.mp3', '.flac', '.ogg']
    file_ext = Path(file_path).suffix.lower()
    
    if file_ext not in valid_extensions:
        raise ValidationError(
            f"Invalid audio file extension: {file_ext}. "
            f"Expected one of: {', '.join(valid_extensions)}"
        )


def validate_api_key(api_key: Optional[str], service_name: str) -> None:
    """
    Validate that an API key is present and not empty.
    
    Args:
        api_key: The API key to validate
        service_name: Name of the service for error message
        
    Raises:
        ValidationError: If API key is invalid
    """
    if not api_key or not api_key.strip():
        raise ValidationError(
            f"{service_name} API key is missing or empty. "
            f"Please check your .env file."
        )


def validate_positive_int(value: int, name: str) -> None:
    """
    Validate that a value is a positive integer.
    
    Args:
        value: The value to validate
        name: Name of the value for error message
        
    Raises:
        ValidationError: If value is not a positive integer
    """
    if not isinstance(value, int) or value <= 0:
        raise ValidationError(
            f"{name} must be a positive integer, got: {value}"
        )


def validate_sample_rate(sample_rate: int) -> None:
    """
    Validate audio sample rate.
    
    Args:
        sample_rate: Sample rate in Hz
        
    Raises:
        ValidationError: If sample rate is invalid
    """
    valid_rates = [8000, 16000, 22050, 44100, 48000]
    
    if sample_rate not in valid_rates:
        raise ValidationError(
            f"Invalid sample rate: {sample_rate}. "
            f"Expected one of: {', '.join(map(str, valid_rates))}"
        )
