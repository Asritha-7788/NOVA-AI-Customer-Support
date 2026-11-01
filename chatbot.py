
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key is missing in .env")

client = genai.Client(api_key=API_KEY)

SYSTEM_INSTRUCTION = """
You are an intelligent, friendly and professional customer support assistant.

Your personality:
- Speak naturally, like a real customer support representative.
- Be polite, empathetic and conversational.
- Never give robotic or one-word answers.

Your responsibilities:
1. Understand the customer's problem.
2. Provide practical solutions.
3. Remember all previous messages in the current conversation.
4. Use previous information when answering follow-up questions.
5. Ask relevant questions if more information is needed.
6. Handle frustrated customers with empathy.
7. Never invent order IDs, payment details or refund confirmations.
8. Escalate complicated issues to human support when appropriate.

Keep your answers clear, helpful and conversational.
"""

def get_response(conversation_history):
    # Keep only the latest 6 messages for faster responses
    recent_history = conversation_history[-6:]
    
    conversation = []
    for message in recent_history:
        if message["role"] == "user":
            speaker = "Customer"
        else:
            speaker = "Assistant"
        conversation.append(f"{speaker}: {message['content']}")
        
    full_prompt = (
        SYSTEM_INSTRUCTION + 
        "\n\nConversation history:\n" + 
        "\n".join(conversation) + 
        "\n\nRespond to the latest customer message in a helpful and concise way."
    )
    
    response = client.interactions.create(
        model="gemini-3.8-flash", 
        input=full_prompt
    )
    
    answer = response.output_text
    if not answer:
        raise ValueError("Gemini returned an empty response.")
        
    return answer.strip()