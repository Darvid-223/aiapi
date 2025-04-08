import os
import re
import uuid
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from agents import Agent, Runner
import asyncio

# Miljövariabler
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# Flask-app
app = Flask(__name__)
CORS(app)  # Tillåt anrop från frontend


# Agent-definition
chat_agent = Agent(
    name="Navigator",
    instructions="Du är en assistent för Eklunda kommun med tillgång till fil-sökverktyg. Använd de uppladdade dokumenten för att svara på frågor om organisationen, anställda eller brukare och annat relevant. Du svarar som att du är en anställd assistent, inte som en dator.",
    model="gpt-4-turbo",  # eller gpt-3.5-turbo om du vill
)


# Enkel minnesstruktur (session_id -> lista med meddelanden)
chat_sessions = {}


def clean_response(text: str) -> str:
    return re.sub(r"【.*?†.*?】", "", text).strip()


# Bygg prompt från historik
def get_memory_prompt(session_id, new_input):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    history = chat_sessions[session_id]
    history.append(f"Användare: {new_input}")
    prompt = "\n".join(history)
    return prompt


# Spara agentsvar
def save_response_to_memory(session_id, agent_response):
    chat_sessions[session_id].append(f"Agent: {agent_response}")


# Async körning av agent
async def async_generate_response(session_id, user_input):
    prompt = get_memory_prompt(session_id, user_input)
    result = await Runner.run(chat_agent, input=prompt)
    reply = clean_response(result.final_output)
    save_response_to_memory(session_id, reply)
    return reply


# API endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    session_id = data.get("session_id") or str(uuid.uuid4())  # generera nytt om inget skickas

    if not user_input:
        return jsonify({"error": "Tomt meddelande"}), 400

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reply = loop.run_until_complete(async_generate_response(session_id, user_input))
        return jsonify({"reply": reply, "session_id": session_id})
    except Exception as e:
        print("❌ Fel:", e)
        return jsonify({"error": "Serverfel", "details": str(e)}), 500

@app.route("/")
def index():
    return render_template("index.html")

debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"

if __name__ == "__main__":
    app.run(debug=debug_mode)
