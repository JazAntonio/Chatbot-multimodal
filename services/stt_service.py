import os
import tempfile
from dotenv import load_dotenv
from openai import OpenAI
from utils.logger import get_logger
from security.input_sanitizer import InputSanitizer
from security.prompt_injection_detector import PromptInjectionDetector
from utils.exceptions import ValidationError

# Initialize logger
logger = get_logger(__name__)


class STTService:
    def __init__(self, enable_security: bool = True, security_level: str = "MEDIUM"):
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OPENAI_API_KEY no encontrada en el archivo .env")

        self.client = OpenAI(api_key=api_key)
        
        # Initialize security components
        self.enable_security = enable_security
        if self.enable_security:
            max_input_length = int(os.getenv("MAX_INPUT_LENGTH", "2000"))
            self.sanitizer = InputSanitizer(max_length=max_input_length)
            self.injection_detector = PromptInjectionDetector(security_level=security_level)
            logger.info(f"STTService initialized with security enabled (level: {security_level})")
        else:
            self.sanitizer = None
            self.injection_detector = None
            logger.info("STTService initialized without security")
        
        logger.info("STTService initialized successfully")

    def transcribe_file(self, file_path: str) -> str:
        """
        Transcribe un archivo de audio usando OpenAI STT.
        Retorna el texto transcrito.
        """
        logger.debug(f"Transcribing audio file: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"Audio file not found: {file_path}")
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        try:
            with open(file_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=audio_file
                )
            
            transcribed_text = transcription.text
            logger.info(f"Transcription successful: {len(transcribed_text)} characters")
            logger.debug(f"Transcribed text: {transcribed_text[:100]}...")  # Log first 100 chars
            
            # Apply security validation if enabled
            if self.enable_security:
                transcribed_text = self._validate_and_sanitize(transcribed_text)
            
            return transcribed_text
            
        except ValidationError as e:
            logger.error(f"Security validation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Transcription failed: {e}", exc_info=True)
            raise

    def transcribe_bytes(self, audio_bytes: bytes, suffix=".wav") -> str:
        """
        Transcribe audio directamente desde memoria.
        Se crea un archivo temporal compatible.
        """
        logger.debug(f"Transcribing audio from bytes ({len(audio_bytes)} bytes)")

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_path = temp_audio.name

        try:
            text = self.transcribe_file(temp_path)
            logger.info("Transcription from bytes completed successfully")
        finally:
            os.remove(temp_path)
            logger.debug(f"Temporary file removed: {temp_path}")

        return text
    
    def _validate_and_sanitize(self, text: str) -> str:
        """
        Validate and sanitize transcribed text for security.
        
        Args:
            text: Transcribed text to validate
            
        Returns:
            Sanitized text
            
        Raises:
            ValidationError: If text contains prompt injection attempts
        """
        # Sanitize input
        sanitized_text = self.sanitizer.sanitize(text)
        
        # Check for prompt injection
        detection_result = self.injection_detector.detect(sanitized_text)
        
        if detection_result.is_threat:
            logger.warning(
                f"Prompt injection detected in transcription! "
                f"Level: {detection_result.threat_level.name}, "
                f"Reason: {detection_result.reason}"
            )
            raise ValidationError(
                f"Security threat detected in audio transcription: {detection_result.reason}. "
                f"Please try again with different content."
            )
        
        return sanitized_text


# # Test ##
# stt = STTService()
# texto = stt.transcribe_file("../sample1.wav")
#
# print("Transcripción:")
# print(texto)