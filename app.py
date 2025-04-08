import os
import re
import uuid
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from agents import Agent, Runner
import asyncio
import json

# Miljövariabler
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Flask-app
app = Flask(__name__)
CORS(app)  # Tillåt anrop från frontend

# Agent-definition
chat_agent = Agent(
    name="Navigator",
    instructions="""
    Du är en assistent för Eklunda kommun. 
    Du kan svara på frågor om organisationen, anställda eller brukare. 
    Du baserar dina svar på datan du får presenterad i prompten. 
    Du är artig och professionell, och svarar som om du vore en anställd.
    """,
    model="gpt-4-turbo",
)

# Enkel minnesstruktur (session_id -> lista med meddelanden)
chat_sessions = {}

# Hjälp: läs JSON och returnera en textsnutt

def read_json_file(filepath, max_items=10):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return json.dumps(data[:max_items], indent=2, ensure_ascii=False)
    except Exception as e:
        return f"⚠️ Kunde inte läsa filen {filepath}: {e}"


def clean_response(text: str) -> str:
    return re.sub(r"【.*?†.*?】", "", text).strip()


# Bygg prompt från historik + datafiler
def get_memory_prompt(session_id, new_input):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    history = chat_sessions[session_id]
    history.append(f"Användare: {new_input}")

    employees_data = read_json_file("db/employees.json")
    brukare_data = read_json_file("db/brukare.json")

    prompt = f"""
Här är information om anställda (utdrag):
{employees_data}

Här är information om brukare (utdrag):
{brukare_data}

Tidigare konversation:
{chr(10).join(history)}

Svara utifrån informationen ovan och på ett vänligt, informativt sätt.
"""

    return prompt


# Spara agentsvar
def save_response_to_memory(session_id, agent_response):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    chat_sessions[session_id].append(f"Agent: {agent_response}")


# Async körning av agent
async def async_generate_response(session_id, user_input):
    full_prompt = get_memory_prompt(session_id, user_input)
    result = await Runner.run(chat_agent, input=full_prompt)
    reply = clean_response(result.final_output)
    save_response_to_memory(session_id, reply)
    return reply


# API endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    session_id = data.get("session_id") or str(uuid.uuid4())

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