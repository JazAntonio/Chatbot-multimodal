#!/usr/bin/env python3
"""
Quick test script to demonstrate the logging system.
This script shows how logs appear in both console and file.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import get_logger

# Create logger
logger = get_logger(__name__)

def main():
    """Test the logging system with various log levels."""
    
    print("\n" + "="*60)
    print("LOGGING SYSTEM TEST")
    print("="*60 + "\n")
    
    logger.info("Starting logging system test...")
    logger.debug("This is a DEBUG message (only in file)")
    logger.info("This is an INFO message (console + file)")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    
    # Simulate some operations
    logger.info("Simulating service initialization...")
    logger.info("AudioService initialized")
    logger.info("STTService initialized")
    logger.info("GPTService initialized")
    logger.info("TTSService initialized")
    
    logger.info("All services initialized successfully")
    
    # Simulate an operation
    logger.info("Processing user request...")
    logger.debug("User input: 'Hello, how are you?'")
    logger.info("Transcription completed")
    logger.info("Generating GPT response...")
    logger.info("GPT response generated: 42 characters")
    logger.info("Synthesizing speech...")
    logger.info("TTS audio saved to: response.wav")
    
    logger.info("Logging system test completed successfully!")
    
    print("\n" + "="*60)
    print("Check the logs directory for the log file:")
    print("  - logs/chatbot.log")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
