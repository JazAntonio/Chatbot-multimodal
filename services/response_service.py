# services/response_service.py

import os
from openai import OpenAI


class GPTService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Historial básico tipo chat
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant, please provide only short and concise answers."}
        ]

    def generate_response(self, user_text: str) -> str:
        if not user_text.strip():
            raise ValueError("Texto vacío enviado a GPT")

        # Agregar mensaje del usuario al historial
        self.messages.append({"role": "user", "content": user_text})

        response = self.client.chat.completions.create(
            model="gpt-5-nano",
            messages=self.messages,
            temperature=1
        )

        assistant_text = response.choices[0].message.content

        # Guardar respuesta en historial
        self.messages.append({"role": "assistant", "content": assistant_text})

        return assistant_text

    def reset_conversation(self):
        self.messages = [
            {"role": "system", "content": "Eres un asistente útil y conciso."}
        ]
