"""
Input Sanitizer
Sanitizes and normalizes user input to prevent injection attacks.
"""

import re
import unicodedata
from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)


class InputSanitizer:
    """
    Sanitizes user input by:
    - Normalizing unicode characters
    - Removing control characters
    - Truncating excessive length
    - Neutralizing potentially dangerous sequences
    """
    
    def __init__(self, max_length: int = 2000):
        """
        Initialize the sanitizer.
        
        Args:
            max_length: Maximum allowed input length
        """
        self.max_length = max_length
        logger.info(f"InputSanitizer initialized with max_length: {max_length}")
    
    def sanitize(self, text: str, preserve_newlines: bool = True) -> str:
        """
        Sanitize input text.
        
        Args:
            text: Input text to sanitize
            preserve_newlines: Whether to preserve newline characters
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        original_length = len(text)
        
        # Step 1: Normalize unicode
        text = self._normalize_unicode(text)
        
        # Step 2: Remove control characters
        text = self._remove_control_characters(text, preserve_newlines)
        
        # Step 3: Normalize whitespace
        text = self._normalize_whitespace(text, preserve_newlines)
        
        # Step 4: Remove escape sequences
        text = self._remove_escape_sequences(text)
        
        # Step 5: Truncate if too long
        if len(text) > self.max_length:
            logger.warning(f"Input truncated from {len(text)} to {self.max_length} characters")
            text = text[:self.max_length]
        
        # Step 6: Strip leading/trailing whitespace
        text = text.strip()
        
        if len(text) != original_length:
            logger.debug(f"Input sanitized: {original_length} -> {len(text)} characters")
        
        return text
    
    def _normalize_unicode(self, text: str) -> str:
        """
        Normalize unicode characters to prevent homograph attacks.
        Uses NFKC normalization to convert visually similar characters.
        """
        # NFKC: Compatibility decomposition, followed by canonical composition
        normalized = unicodedata.normalize('NFKC', text)
        
        # Remove zero-width characters that could hide content
        zero_width_chars = [
            '\u200B',  # Zero-width space
            '\u200C',  # Zero-width non-joiner
            '\u200D',  # Zero-width joiner
            '\uFEFF',  # Zero-width no-break space
        ]
        for char in zero_width_chars:
            normalized = normalized.replace(char, '')
        
        return normalized
    
    def _remove_control_characters(self, text: str, preserve_newlines: bool) -> str:
        """
        Remove control characters except newlines and tabs if specified.
        """
        allowed_chars = {'\n', '\r', '\t'} if preserve_newlines else set()
        
        # Remove control characters (ASCII 0-31 and 127)
        cleaned = ''.join(
            char for char in text
            if char in allowed_chars or not unicodedata.category(char).startswith('C')
        )
        
        return cleaned
    
    def _normalize_whitespace(self, text: str, preserve_newlines: bool) -> str:
        """
        Normalize whitespace characters.
        """
        if preserve_newlines:
            # Replace multiple spaces with single space, but preserve newlines
            text = re.sub(r'[ \t]+', ' ', text)
            # Replace multiple newlines with double newline (paragraph break)
            text = re.sub(r'\n{3,}', '\n\n', text)
        else:
            # Replace all whitespace with single space
            text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def _remove_escape_sequences(self, text: str) -> str:
        """
        Remove or neutralize escape sequences that could be used for injection.
        """
        # Remove ANSI escape sequences
        text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
        
        # Remove backslash escape sequences (but keep literal backslashes)
        # This prevents things like \x00, \u0000, etc.
        text = re.sub(r'\\[xX][0-9a-fA-F]{2}', '', text)  # Hex escapes
        text = re.sub(r'\\[uU][0-9a-fA-F]{4}', '', text)  # Unicode escapes
        text = re.sub(r'\\[0-7]{1,3}', '', text)  # Octal escapes
        
        return text
    
    def validate_length(self, text: str) -> bool:
        """
        Check if text length is within acceptable limits.
        
        Args:
            text: Text to validate
            
        Returns:
            True if length is acceptable, False otherwise
        """
        return len(text) <= self.max_length
    
    def detect_suspicious_encoding(self, text: str) -> bool:
        """
        Detect if text contains suspicious encoding patterns.
        
        Args:
            text: Text to check
            
        Returns:
            True if suspicious encoding detected, False otherwise
        """
        suspicious_patterns = [
            r'\\x[0-9a-fA-F]{2}',  # Hex encoding
            r'\\u[0-9a-fA-F]{4}',  # Unicode escapes
            r'%[0-9a-fA-F]{2}',    # URL encoding
            r'&#\d+;',             # HTML numeric entities
            r'&[a-zA-Z]+;',        # HTML named entities
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, text):
                logger.warning(f"Suspicious encoding pattern detected: {pattern}")
                return True
        
        return False
    
    def remove_repeated_characters(self, text: str, max_repetition: int = 3) -> str:
        """
        Remove excessive character repetition (e.g., 'aaaaaaa' -> 'aaa').
        
        Args:
            text: Text to process
            max_repetition: Maximum allowed character repetition
            
        Returns:
            Text with limited character repetition
        """
        pattern = r'(.)\1{' + str(max_repetition) + r',}'
        replacement = r'\1' * max_repetition
        return re.sub(pattern, replacement, text)
    
    def sanitize_strict(self, text: str) -> str:
        """
        Apply strict sanitization for high-security scenarios.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Strictly sanitized text
        """
        # Apply normal sanitization
        text = self.sanitize(text, preserve_newlines=False)
        
        # Remove repeated characters
        text = self.remove_repeated_characters(text, max_repetition=2)
        
        # Remove special characters except basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Limit consecutive punctuation
        text = re.sub(r'([.,!?-]){3,}', r'\1\1', text)
        
        return text
