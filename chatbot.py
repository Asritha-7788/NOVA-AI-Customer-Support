
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Load API key from Streamlit Cloud Secrets or local .env
try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
except Exception:
    GEMINI_API_KEY = None

GEMINI_API_KEY = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing.")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Model configuration
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

SYSTEM_INSTRUCTION = """
You are NOVA, an intelligent, friendly and professional
customer support assistant.

Your personality:
- Speak naturally, like a real customer support representative.
- Be polite, empathetic and conversational.
- Never give robotic or one-word answers.

Your responsibilities:
1. Understand the customer's problem.
2. Provide practical solutions.
3. Remember previous messages in the current conversation.
4. Use previous information when answering follow-up questions.
5. Ask relevant questions if more information is needed.
6. Handle frustrated customers with empathy.
7. Never invent order IDs, payment details or refund confirmations.
8. Escalate complicated issues to human support when appropriate.

Keep your answers clear, helpful and conversational.
"""


def get_response(conversation_history):

    # Keep the latest 6 messages for faster processing
    recent_history = conversation_history[-6:]

    conversation = []

    for message in recent_history:

        role = message.get("role", "user")
        content = message.get("content", "")

        if not content:
            continue

        # Gemini uses "model" instead of "assistant"
        speaker = "model" if role == "assistant" else "user"

        conversation.append({
            "role": speaker,
            "parts": [{"text": str(content)}]
        })

    if not conversation:
        return "Hello! I'm NOVA. How can I help you today?"

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=conversation,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "temperature": 0.7,
                "max_output_tokens": 300
            }
        )

        answer = response.text

        if not answer:
            raise ValueError("Gemini returned an empty response.")

        return answer.strip()

    except Exception as e:
        print(f"NOVA Gemini Error: {e}")
        return (
            "I'm sorry, I'm having trouble processing "
            "your request right now. Please try again."
        )
