# services/response_service.py

import os
from openai import OpenAI
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


class GPTService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Historial básico tipo chat
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant, please provide only short and concise answers."}
        ]
        logger.info("GPTService initialized successfully")

    def generate_response(self, user_text: str) -> str:
        if not user_text.strip():
            logger.error("Empty text sent to GPT")
            raise ValueError("Texto vacío enviado a GPT")

        # Agregar mensaje del usuario al historial
        self.messages.append({"role": "user", "content": user_text})
        logger.debug(f"User message added to conversation: {user_text[:50]}...")

        try:
            logger.info("Generating GPT response...")
            response = self.client.chat.completions.create(
                model="gpt-5-nano",
                messages=self.messages,
                temperature=1
            )

            assistant_text = response.choices[0].message.content
            logger.info(f"GPT response generated: {len(assistant_text)} characters")
            logger.debug(f"GPT response: {assistant_text[:100]}...")

            # Guardar respuesta en historial
            self.messages.append({"role": "assistant", "content": assistant_text})

            return assistant_text
            
        except Exception as e:
            logger.error(f"GPT response generation failed: {e}", exc_info=True)
            raise

    def reset_conversation(self):
        self.messages = [
            {"role": "system", "content": "Eres un asistente útil y conciso."}
        ]
        logger.info("Conversation history reset")
