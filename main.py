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


def main():
    """
    Main function to initialize and run the application.
    Follows dependency injection pattern for better testability.
    """
    # Initialize Tkinter root window
    root = tk.Tk()
    
    # Initialize all services
    audio_service = AudioService()
    stt_service = STTService()
    gpt_service = GPTService()
    tts_service = TTSService()
    
    # Create and run GUI with injected services
    app = ChatGUI(
        root=root,
        audio_service=audio_service,
        stt_service=stt_service,
        gpt_service=gpt_service,
        tts_service=tts_service
    )
    
    # Start the application
    app.run()


if __name__ == "__main__":
    main()
