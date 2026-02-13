"""
Main Entry Point for Audio GPT Chatbot
Initializes services and launches the GUI
"""

import tkinter as tk
from gui.chat_gui import ChatGUI
from services.audio_service import AudioService
from services.stt_service import STTService
from services.response_service import GPTService
from services.tts_service import TTSService
from utils.logger import get_logger

# Initialize logger for main module
logger = get_logger(__name__)


def main():
    """
    Main function to initialize and run the application.
    Follows dependency injection pattern for better testability.
    """
    logger.info("=" * 60)
    logger.info("Starting Audio GPT Chatbot Application")
    logger.info("=" * 60)
    
    try:
        # Initialize Tkinter root window
        logger.info("Initializing Tkinter root window...")
        root = tk.Tk()
        
        # Initialize all services
        logger.info("Initializing services...")
        logger.debug("Creating AudioService instance")
        audio_service = AudioService()
        
        logger.debug("Creating STTService instance")
        stt_service = STTService()
        
        logger.debug("Creating GPTService instance")
        gpt_service = GPTService()
        
        logger.debug("Creating TTSService instance")
        tts_service = TTSService()
        
        logger.info("All services initialized successfully")
        
        # Create and run GUI with injected services
        logger.info("Creating GUI application...")
        app = ChatGUI(
            root=root,
            audio_service=audio_service,
            stt_service=stt_service,
            gpt_service=gpt_service,
            tts_service=tts_service
        )
        
        # Start the application
        logger.info("Starting application main loop")
        app.run()
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
